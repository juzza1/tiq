#!/usr/bin/python

import math 
from PIL import Image
import numpy as np
import scipy.spatial as spspat
import png
import sys
import time

import palettes

start_time = time.time()

def now(what):
    print what, "after", time.time() - start_time, "seconds"

def euc_distance(x1, x2, x3, y1, y2, y3):
    return math.sqrt((x1-y1)**2 + (x2-y2)**2 + (x3-y3)**2)

def replace_colors(inim, outim, mapping):
    inpix = inim.load()
    outpix = outim.load()
    for i in range(inim.size[1]):
        for n in range (inim.size[0]):
            outpix[n, i] = mapping[inpix[n, i]]
    return outpix

def read_rgb(imagename):
    #with Image.open(imagename) as im:
    im = Image.open(imagename)
    im = im.convert('RGB')
    return im

def uniq_colors(im):
    colors = [i[1] for i in im.getcolors(maxcolors=16777216)]
    return colors

def quant_ttd(colors, palette):
    mapping = {}
    for i in colors:
        quantized_min = 255
        for index, color in enumerate(palette):
            quantized = euc_distance(*i+color)
            if quantized < quantized_min:
                quantized_min = quantized
                mapping[i] = index
    return mapping

# Get input image name from command line, first parameter
imagename = str(sys.argv[1])
outimagename = str(sys.argv[2])

im = read_rgb(imagename)

quantpal = palettes.pals('dos_full')
outpal = palettes.pals('dos_full', 'raw')

imuniq = uniq_colors(im)
now("Unique colors found")


palar = np.array(quantpal)
imar = np.array(imuniq)

dists = spspat.distance.cdist(imar, palar, metric='euclidean')
now("Dists calculated")

immap = {}
for i, e in enumerate(imuniq):
    immap[e] = np.argmin(dists[i])

#immap = quant_ttd(imuniq, quantpal)
now("Quantization done after")

outimg = Image.new('P', im.size, None)

imout = replace_colors(im, outimg, immap)

outimg.putpalette(outpal)

outimg.save(outimagename)
now("Save done after")
