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
    2.4  Notes about special colors
3   Known issues
4   Frequently Asked Questions
5   Credits
6   Contact information
    6.1  Bug reports
    6.2  Other problems
    6.3  General enquiries
7   License
8   Obtaining the source


-------
1 About
-------

TIQ is a tool which converts most image types into TTD-compatible 256-colour
images. Output works for any image type which supports palettes. For NewGRF
usage, PCX or PNG is the obvious choice. If STDOUT is chosen for output, the
format will be PNG. More info about file formats:
http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html


---------------------
2 General information
---------------------

2.1 Required python packages
----------------
- Pillow

2.2 Recommended python packages
----------------
- Numpy
- Scipy
Having these packages available will greatly increase quantization speed.

2.2 Installation
----------------
There is no installer. Only thing required to run the program is to download it
from the devzone repository.
Cloning with mercurial: "hg clone http://hg.openttdcoop.org/tiq"

2.3 Usage
---------
usage: tiq.py [-h] [-a] [-c] [-w | -dt | -wt] infile outfile

Convert images to TTD-paletted images. By default, the dos palette is used.

positional arguments:
  infile                The input file. Use "-" to read from standard input.
  outfile               The output file. Use "-" to write to standard output.
                        In this case, the format will be PNG.

optional arguments:
  -h, --help            show this help message and exit
  -a, --no-action-colors
                        Don't use action colors.
  -c, --no-cc-colors    Don't use cc colors.
  -w, --windows         Use windows palette
  -dt, --dos-toyland    Use dos toyland palette
  -wt, --windows-toyland
                        Use windows toyland palette

2.4 Notes about special colors
---------
Some special colors are never quantized into, unless the color in the input
file matches the special color 1:1. These include action colors, cc (blue)
colors, background blue and pure white. Additionally, action and cc colors can
be omitted altogether with optional parameters.

The legacy API pink colors are never used in the actual image, as they are
considered unsafe.


--------------
3 Known issues
--------------


----------------------------
4 Frequently Asked Questions
----------------------------


---------
5 Credits
---------

juzza1 (Jussi Virtanen)


---------------------
6 Contact information
---------------------

6.1 Bug reports
---------------
Please report any bugs you find at
  bug tracker: http://dev.openttdcoop.org/projects/tiq

Always included a detailed description of the bug. Also state the exact version
of this program.

6.2 General enquiries
---------------------

I'm on irc at irc.otfc.net, at #openttd and #openttdcoop.devzone

You can also contact me via private message at www.tt-forums.net, or file an
issue at the project devzone site.


---------
7 License
---------
                                                                              
TIQ - TTD Image Quantizer                                                     
                                                                              
by juzza1                                                                     
                                                                              
To the extent possible under law, the author(s) have dedicated all copyright  
and related and neighboring rights to this software to the public domain      
worldwide. This software is distributed without any warranty.                 
                                                                              
You should have received a copy of the CC0 Public Domain Dedication along     
with this software. If not, see                                               
<http://creativecommons.org/publicdomain/zero/1.0/>.                          


----------------------
8 Obtaining the source
----------------------

The source code can be obtained from the #openttdcoop DevZone
via source browser:
    http://dev.openttdcoop.org/projects/tiq/repository
or via mercurial checkout:
    hg clone http://hg.openttdcoop.org/tiq
