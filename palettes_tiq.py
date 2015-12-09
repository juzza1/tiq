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
from PIL import Image

import palettes_ttd


class TiqPalette:

    def __init__(self, palette, act, neutral, onecc, pink, twocc):
        self.palette = palette
        self.rgb_to_i = {c: i for i, c in enumerate(self.palette)}
        self.getr = lambda args: {color for r in args \
                                  for color in self.palette[r[0] : r[1]+1]}
        self.ranges = {
            "ACT": {"colors": self.getr(act),
                    "desc": "Animated colors (water, lights etc.)"},
            "BG": {"colors": {palette[0]},
                   "desc": "Background blue, transparent ingame."},
            "NEUTRAL": {"colors": self.getr(neutral),
                        "desc": "Colors with no special behaviour."},
            "NONE": {"colors": set(),
                     "desc": "No colors."},
            "ONECC": {"colors": self.getr(onecc),
                      "desc": "Primary company colors."},
            "PINK": {"colors": self.getr(pink),
                     "desc": ("Legacy pink system colors. Undefined ingame "
                              "behaviour, do not use unless you know what you "
                              "are doing.")},
            "TWOCC": {"colors": self.getr(twocc),
                      "desc": "Secondary company colors."},
            "WHITE": {"colors": {palette[255]},
                      "desc": "Pure white."}
        }

dos_spec = {"act": [(227, 254)],
            "neutral": [(1, 197), (206, 214)],
            "onecc": [(198, 205)],
            "pink": [(216, 226)],
            "twocc": [(80, 87)]}
win_spec = {"act": [(217, 244)],
            "neutral": [(10, 197), (206, 216), (245, 245)],
            "onecc": [(198, 205)],
            "pink": [(1, 9), (246, 254)],
            "twocc": [(80, 87)]}

palettes = {
    "DOS": TiqPalette(palette=palettes_ttd.dos, **dos_spec),
    "WIN": TiqPalette(palette=palettes_ttd.win, **win_spec),
    "DOS_TOYLAND": TiqPalette(palette=palettes_ttd.dos_toyland, **dos_spec),
    "WIN_TOYLAND": TiqPalette(palette=palettes_ttd.win_toyland, **win_spec)
}
