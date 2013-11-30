TIQ - TTD Image Quantizer
===========================

----------
0 Contents
----------

1   About
2   General information
    2.1  Requirements
    2.2  Installation
    2.3  Usage
3   Known issues
4   Background information
5   Frequently Asked Questions
6   Credits
7   Contact information
    7.1  Bug reports
    7.2  Other problems
    7.3  General enquiries
8   License
9   Obtaining the source


-------
1 About
-------

TIQ is a tool which converts most image types into TTD-compatible 256-colour
images. Output works for any image type which supports palettes. For NewGRF
usage, PCX or PNG is the obvious choice. More info about file formats:
http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html


---------------------
2 General information
---------------------

2.1 Requirements
----------------
- Python. Tested only on 2.7.6, but other versions should work too.
- Following Python packages: Pillow, Numpy, Scipy. Manual installation with 
  pip: "pip install pillow numpy scipy"


2.2 Installation
----------------
There is no installer. Only thing required to run the program is to download
it from the devzone repository.
Cloning with mercurial: "hg clone http://hg.openttdcoop.org/tiq"

2.3 Usage
---------
The program can only be used from the command line. To run it with the python
interpreter: "python tiq.py inimage outimage"

Required parameters:
    inimage: The name of the input image
    outimage: The name of the output image

Optional parameters:
    --noact, -n: Don't use action colors. Default behaviour is to use action
    colors, but only if the source image has 1:1 color match for the action
    color.
    --win, -w: Use the windows TTD palette. Default behaviour is to use the DOS
    palette.
    --help, -h: Interactive help


--------------
3 Known issues
--------------


----------------------------
4 Background information
----------------------------

How the program works (roughly)
- Read image, convert it to RGB image irregardless of source format
- Get the unique colors of the image
- Check if the image has transparent blue (255, 0, 0), also check for action
  colors if --noact is not used
- If any of these colors is found, save the mapping of these colors into
  dictionary 1.
- Find the closest match from the palette for every unique color in the image,
  and save this mapping into dictionary 2. In this stage, transparent blue,
  pink colors and action colors are omitted.
- Update mapping 2. with mapping 1.
- Get the palette indexes for every color in mapping 2.
- Replace every pixel in the source image, using mapping 2. to find the correct
  match for each pixel
- Save the output image as an 8-bit 256-color paletted image


----------------------------
5 Frequently Asked Questions
----------------------------


---------
6 Credits
---------

juzza1 (Jussi Virtanen)


---------------------
7 Contact information
---------------------

7.1 Bug reports
---------------
Please report any bugs you find at
  bug tracker: http://dev.openttdcoop.org/projects/tiq

Always included a detailed description of the bug. Also state the exact version
of this program.

7.2 General enquiries
---------------------

I'm on irc at irc.otfc.net, at channels #openttd and #openttdcoop.devzone

You can also contact me via private message at www.tt-forums.net, or file an
issue at the project devzone site.


---------
8 License
---------

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


----------------------
9 Obtaining the source
----------------------

The source code can be obtained from the #openttdcoop DevZone
via source browser:
    http://dev.openttdcoop.org/projects/tiq/repository
or via mercurial checkout:
    hg clone http://hg.openttdcoop.org/tiq
