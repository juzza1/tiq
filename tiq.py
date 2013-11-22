#!/usr/bin/python

import math 
import png
import sys

import palettes

def chunks(l):
    return [tuple(l[i:i+3]) for i in range(0, len(l), 3)]
# Function to remove every 4th item from list, used to remove alpha channel as any 8bpp images for ttd should not contain transparent pixels.
def del_alpha(l):
    del l[3::4]
    return l

def euc_distance(x1, x2, x3, y1, y2, y3):
    return math.sqrt((x1-y1)**2 + (x2-y2)**2 + (x3-y3)**2)

def img_size(inimg):
    width = len(inimg[0])
    height = len(inimg)
    size = width, height
    return size

def png_to_3tuples(infile, typ=0):
    pixels = []

    with open(infile, 'rb') as f:
        r = png.Reader(file=f)
        img = r.asRGBA8()
        # img[2] is a list of arrays, use tolist to convert it to a normal list
        for i in img[2]:
            # We need to know the height too, so append to remember pixel row info.
            pixels.append(i.tolist())
        for n,i in enumerate(pixels):
            del_alpha(i)
            pixels[n] = chunks(i)
        return pixels

# Get input image name from command line, first parameter
inimagename = str(sys.argv[1])

img = png_to_3tuples(inimagename)
#print img
setim = []
for i in img:
    setim.extend(i)
setim = set(setim)
#print setim
pal = palettes.pals('dos')

colorsdict = {}
outimg = []
# Quantization (nearest colour)
for i in setim:
    quantized_min = 255
    for e,j in enumerate(pal):
        quantized = euc_distance(*i+j)
        if quantized < quantized_min:
            quantized_min = quantized
            colorsdict[i] = e

# Replace pure white with almost-white to prevent grfcoded whine (convert palette entry 255 to 15)
for i in colorsdict:
    if colorsdict[i] == 255:
        colorsdict[i] = 15
#print colorsdict 

for i in img:
    for n,e in enumerate(i):
        i[n] = (colorsdict[e])
#print img

with open(inimagename, 'wb') as f:
    r = png.Writer(size=img_size(img), palette=pal)
    r.write(f, img)
