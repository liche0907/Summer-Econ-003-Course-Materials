#!/usr/bin/env python3
"""Compute --pan/--tilt for make_title_triangle.py from a desired subject placement.

The wedge keeps the framed image's LOWER-LEFT triangle, so a subject survives only if
window_y > window_x.  Putting it LEFT and LOW in the crop window is what gets it into
the fat end.  Coordinates are given in the FLIPPED image when --flip is used.
"""
import sys
W, H = 612, 407
AR = 3015574 / 2254385
cw0, ch0 = (W, W / AR) if W / H < AR else (H * AR, H)

def aim(tx, ty, wx, wy, zoom):
    cw, ch = cw0 / zoom, ch0 / zoom
    cx = tx * W - (wx - 0.5) * cw
    cy = ty * H - (wy - 0.5) * ch
    pan = (cx - W / 2) / ((W - cw) / 2)
    tilt = (cy - H / 2) / ((H - ch) / 2)
    return max(-1, min(1, pan)), max(-1, min(1, tilt))

if __name__ == "__main__":
    tx, ty, wx, wy, z = map(float, sys.argv[1:6])
    p, t = aim(tx, ty, wx, wy, z)
    print("--pan %.3f --tilt %.3f --zoom %.2f" % (p, t, z))
