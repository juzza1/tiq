#!/usr/bin/env python
#
# TIQ - TTD Image Quantizer
#
# by juzza1
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty. 
#
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>. 
#
import argparse
import collections
import math 
from PIL import Image
from StringIO import StringIO
import sys
import time

from palette import palettes

def now(event):
    """Print time elapsed so far with a variable message."""
    print event, "after", time.time() - start_time, "seconds"

def euc_distance(x, y):
    """Euclidean distance between two points in 3-dimensional space"""
    formula = (x[0]-y[0])**2 + (x[1]-y[1])**2 + (x[2]-y[2])**2
    result = math.sqrt(formula)
    return result

def replace_colors(img_in, palette, mapping):
    """
    Insert pixels into the new image, using a mapping to choose the best
    replacement from the TTD palette for each unique color.
    """
    pixels_in = img_in.load()
    # Flatten the palette from a list of 3-tuples to a list of integer values
    img_out = Image.new('P', img_in.size, color=None)
    img_out.putpalette(palette)
    pixels_out = img_out.load()
    for y in range(img_in.size[1]):
        for x in range (img_in.size[0]):
            pixels_out[x, y] = mapping[pixels_in[x, y]]
    return img_out

def convert(img, bg):
    """
    Force the image to RGB mode.

    For RGBA images, convert all transparent pixels to bg color.
    """
    if img.mode == 'RGBA':
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range (img.size[0]):
                if pixels[x, y][3] < 255:
                    pixels[x, y] = bg
        img = img.convert('RGB')
    else:
        img = img.convert('RGB')
    return img

def get_unique_colors(img):
    """Make a list of all the unique colors in the image"""
    # getcolors returns (count, pixel) we don't care about the count, at least
    # not for now
    colors = [i[1] for i in img.getcolors(maxcolors=img.size[0]*img.size[1])]
    return colors

def indexify(mapping, palette):
    """Translate RGB values to palette indices"""
    for i in mapping:
        mapping[i] = palette.index(mapping[i])
    return mapping

def quant_brute(colors, palette):
    """
    Calculate the closest match between the unique colors in the source image
    and the chosen TTD palette using simple iteration.
    """
    mapping = {}
    best_match = 0
    for color in colors:
        quantized_min = 255
        for entry in palette:
            quantized = euc_distance(color, entry)
            if quantized < quantized_min:
                quantized_min = quantized
                best_match = entry
        mapping[color] = best_match
    return mapping

def quant_sp(colors, palette):
    """
    Calculate the closest match between the unique colors in the source image
    and the chosen TTD palette using numpy arrays and scipy spatial distance
    module. Around 500% faster than the "brute" method.
    """
    try:
        __import__('numpy')
        __import__('scipy')
    except ImportError:
        pass
    else:
        import numpy as np
        import scipy.spatial

        colors_numpy = np.array(colors)
        palette_numpy = np.array(palette)
        # dists holds the values of all the distances between the points in
        # array 1 and array 2
        dists = scipy.spatial.distance.cdist(colors_numpy, palette_numpy,
                'euclidean')
        mapping = {}
        # np.argmin(dists[index]) gets the lowest euclidean distance for this
        # unique color, which is also the palette index. The palette color is
        # then retrieved with the index value.
        for index, item in enumerate(colors):
            mapping[item] = palette[np.argmin(dists[index])]
        return mapping

def flatten(list_):
    """Flatten lists of tuples into a list of tuples"""
    for i in list_:
        if isinstance(i, collections.Iterable) and not isinstance(i, tuple):
            for j in flatten(i):
                yield j
        else:
            yield i

def update_constant_colors(mapping, colors):
    """
    Add values to color mapping.

    Some special colors, namely the background color and action colors should
    never be quantized into. Therefore we add these colors to the final mapping
    after quantization.
    """
    cols = {}
    for i in colors:
        cols[i] = i
    mapping.update(cols)
    return mapping

def main(img, palette, ignored_colors=None):
    """
    The main method for quantization that combines all the required methods.
    """
    img = convert(img, palette.bg)
    colors = get_unique_colors(img)
    try:
        __import__('numpy')
        __import__('scipy')
    except ImportError:
        mapping = quant_brute(colors, palette.neutral)
    else:
        mapping = quant_sp(colors, palette.neutral)
    no_quant_colors = [palette.bg, palette.onecc, palette.act, palette.white]
    # flatten returns a generator, so convert it to list
    no_quant_colors = list(flatten(no_quant_colors))
    if ignored_colors:
        for i in flatten(ignored_colors):
            no_quant_colors.remove(i)
    mapping = update_constant_colors(mapping, no_quant_colors)
    mapping = indexify(mapping, palette.full)
    img = replace_colors(img, palette.raw, mapping)
    return img

def parse_arguments():
    """Command-line argument parsing"""

    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter, description=(
            "Convert images to TTD-paletted PNGs. By default, the dos palette "
            "is used."))

    parser.add_argument('infile', help=
            'The input file. Use "-" to read from standard input.')
    parser.add_argument('outfile', help=(
            'The output file, saved as png regardless of input-file\n'
            'extension. Use "-" to write to standard output.'))

    parser.add_argument('-a', '--no-action-colors', action='store_true',
            help="Don't use action colors.")
    parser.add_argument('-c', '--no-cc-colors', action='store_true',
            help="Don't use cc colors.")

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-w', '--windows', action='store_true',
            help="Use windows palette")
    group.add_argument('-dt', '--dos-toyland', action='store_true',
            help="Use dos toyland palette")
    group.add_argument('-wt', '--windows-toyland', action='store_true',
            help="Use windows toyland palette")

    args = parser.parse_args()

    if args.infile == '-':
        in_ = StringIO(sys.stdin.read())
    else:
        in_ = args.infile
    img = Image.open(in_)

    if args.windows:
        pal = palettes['win']
    elif args.dos_toyland:
        pal = palettes['dos_toyland']
    elif args.windows_toyland:
        pal = palettes['win_toyland']
    else:
        pal = palettes['dos']
    
    ignored_colors = []
    if args.no_action_colors:
        ignored_colors.extend(pal.act)
    if args.no_cc_colors:
        ignored_colors.extend(pal.onecc)

    img = main(img, pal, ignored_colors)

    if args.outfile== '-':
        out = sys.stdout
    else:
        out = args.outfile
    img.save(out, option='optimize')

if __name__ == '__main__':
    parse_arguments()
