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

TIQ is a tool which converts most image types into TTD-compatible
8-bit paletted images. Output works for any image type which supports
palettes. If STDOUT is chosen for output, the format will be PNG. More
info about file formats:
http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html


---------------------
2 General information
---------------------

2.1 Requiremets
----------------
Required python packages
- Pillow

Recommended python packages
- Numpy
- Scipy

Having these packages available will greatly increase quantization speed.

2.2 Installation
----------------
There is no installer. Only thing required to run the program is to 
download it from the devzone repository.
Cloning with mercurial: "hg clone http://hg@hg.openttdcoop.org/tiq"

2.3 Usage
---------
Up-to-date help can be viewed with with tiq -h.


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
Please report any bugs you find at bug tracker:
http://dev.openttdcoop.org/projects/tiq

Always included a detailed description of the bug. Also state the 
exact version of this program.

6.2 General enquiries
---------------------
I'm on irc at irc.otfc.net, at #openttd and #openttdcoop.devzone

You can also contact me via private message at www.tt-forums.net, or
file an issue at the project devzone site.


---------
7 License
---------
                                                                              
TIQ - TTD Image Quantizer                                                     
                                                                              
by juzza1                                                                     
                                                                              
To the extent possible under law, the author(s) have dedicated all
copyright and related and neighboring rights to this software to the
public domain worldwide. This software is distributed without any
warranty.
                                                                              
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
