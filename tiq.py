#!/usr/bin/python

import argparse
import math 
from PIL import Image
import numpy as np
import scipy.spatial as spspat
import sys
import time

import palettes

start_time = time.time()

def now(what):
    "Print time elapsed so far with a variable message"
    pass
    #print what, "after", time.time() - start_time, "seconds"

def euc_distance(x1, x2, x3, y1, y2, y3):
    "Eucledian distance between two points in 3-dimensional space"
    return math.sqrt((x1-y1)**2 + (x2-y2)**2 + (x3-y3)**2)

def replace_colors(inim, outim, mapping):
    """Insert pixels into the new image, using a mapping to choose the
    best replacement from the TTD palette for each unique color"""
    inpix = inim.load()
    outpix = outim.load()
    for i in range(inim.size[1]):
        for n in range (inim.size[0]):
            outpix[n, i] = mapping[inpix[n, i]]

def read_rgb(imagename):
    "Read image and make sure it's in RGB format"
    im = Image.open(imagename)
    im = im.convert('RGB')
    return im

def uniq_colors(im):
    "Make a list of all the unique colors in the image"
    colors = [i[1] for i in im.getcolors(maxcolors=256**3)]
    return colors

def quant_brute(colors, palette):
    """Calculate the closest match between the unique colors in the source
    image and the chosen TTD palette using simple iteration."""
    mapping = {}
    for i in colors:
        quantized_min = 255
        for index, color in enumerate(palette):
            quantized = euc_distance(*i+color)
            if quantized < quantized_min:
                quantized_min = quantized
                mapping[i] = index
    return mapping

def quant_np(colors, palette):
    """Calculate the closest match between the unique colors in the source
    image and the chosen TTD palette using numpy arrays and scipy
    spatial distance module. Much faster than the "brute" method."""
    imar = np.array(colors)
    palar = np.array(palette)
    dists = spspat.distance.cdist(imar, palar, metric='euclidean')
    mapping = {}
    for index, item in enumerate(colors):
        mapping[item] = np.argmin(dists[index])
    return mapping

# Argument parsing
parser = argparse.ArgumentParser(description=
                    'Convert RGB images to TTD-paletted images.')
parser.add_argument('inimage', help="name of the input image")
parser.add_argument('outimage', help="name of the output image")
parser.add_argument('-w', '--winpal', action='store_true',
                    help="use windows palette instead of dos palette")
parser.add_argument('-n', '--noact', action='store_true',
                    help="disable all action colors")
args = parser.parse_args()

imagename = args.inimage
outimagename = args.outimage

if args.winpal:
    outpal = palettes.pals('win', 'raw')
    if args.noact:
        quantpal = palettes.pals('win', 'noact')
    else:
        quantpal = palettes.pals('win', 'nopink')
else:
    outpal = palettes.pals('dos', 'raw')
    if args.noact:
        quantpal = palettes.pals('dos', 'noact')
    else:
        quantpal = palettes.pals('dos', 'nopink')

im = read_rgb(imagename)
now("Image read after")

imuniq = uniq_colors(im)
now("Unique colors found after")

immap = quant_np(imuniq, quantpal)
now("Quantization done after")

outimg = Image.new('P', im.size, None)
outimg.putpalette(outpal)
replace_colors(im, outimg, immap)
now("Output pixels filled after")

outimg.save(outimagename)
now("Save done after")
