#!/usr/bin/env python3
"""Clip an image to the ECON 003 title-slide triangle.

The deck's title slide holds a picture in a right triangle anchored to the bottom-right
corner (prstGeom rtTriangle + flipH). This produces that same wedge as a standalone PNG
with transparency, so it can be dropped onto any surface as a plain rectangular picture.

    python3 make_triangle.py in.png out.png [--mirror] [--focus X,Y]

--mirror     pre-mirror the source, matching what flipH does inside the deck
--focus      normalised point (0-1) of the source to keep centred in the visible wedge
"""
import sys
from PIL import Image, ImageDraw

W, H = 1400, 1047          # 3.297in x 2.465in, the placeholder's own aspect


def fit(img, w, h, focus=(0.5, 0.5)):
    """cover-fit img into w x h, biased so `focus` stays in frame"""
    sr, tr = img.width / img.height, w / h
    if sr > tr:                                   # source wider -> crop sides
        nw = int(img.height * tr)
        x = int(focus[0] * img.width - nw / 2)
        x = max(0, min(img.width - nw, x))
        box = (x, 0, x + nw, img.height)
    else:                                         # source taller -> crop top/bottom
        nh = int(img.width / tr)
        y = int(focus[1] * img.height - nh / 2)
        y = max(0, min(img.height - nh, y))
        box = (0, y, img.width, y + nh)
    return img.resize((w, h), Image.LANCZOS, box=box)


def triangle(src_path, out_path, mirror=False, focus=(0.5, 0.5)):
    img = Image.open(src_path).convert("RGBA")
    if mirror:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        focus = (1 - focus[0], focus[1])
    img = fit(img, W, H, focus)

    # visible wedge: bottom-right corner. vertices (W,0) (W,H) (0,H)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon([(W, 0), (W, H), (0, H)], fill=255)
    img.putalpha(mask)
    img.save(out_path)
    return out_path


if __name__ == "__main__":
    a = sys.argv[1:]
    src, out = a[0], a[1]
    mirror = "--mirror" in a
    focus = (0.5, 0.5)
    if "--focus" in a:
        fx, fy = a[a.index("--focus") + 1].split(",")
        focus = (float(fx), float(fy))
    print("wrote", triangle(src, out, mirror, focus))
