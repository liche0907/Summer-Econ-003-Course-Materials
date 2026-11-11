#!/usr/bin/env python3
"""
Cut a chapter's theme image into the title-slide triangle.

    python3 make_title_triangle.py "Resources/CoverArt/Chapter Art/ch04_....png" 4

Why this script exists
----------------------
The chapter title slide carries one picture in the bottom-right corner, clipped by
PowerPoint to `prstGeom prst="rtTriangle"` with `flipH="1"`.  Two things follow, and
both are easy to get wrong by eye:

1.  `flipH` mirrors geometry AND content, so the visible wedge corresponds to the
    source image's **lower-LEFT** triangle — everything above the top-left →
    bottom-right diagonal is thrown away.
2.  What the audience sees is that wedge **mirrored**.

So the safe move is to cut the triangle here, look at the preview, and only then put
it in the deck.  Outputs:

    Resources/CoverArt/chNN_title_triangle.png    the cut image, to embed
    Resources/CoverArt/chNN_title_preview.png     what the slide will actually show

Options
-------
--pan   -1.0 … 1.0   slide the crop window left/right before cutting (default 0)
--tilt  -1.0 … 1.0   slide it up/down (default 0, i.e. keep the bottom of the frame)
--zoom  >= 1.0       crop in before cutting, to push the subject below the diagonal
--flip               mirror the SOURCE before cutting.  Use this whenever the image
                     contains text, a logo or anything else that must not read
                     backwards, and note that it also changes which half of the picture
                     survives - see below.
--bg    #RRGGBB      flood the discarded corner with this colour instead of alpha

What --flip actually does, because it is not obvious
---------------------------------------------------
Without it, the slide shows the source's LEFT side, mirrored: every word in the picture
reads backwards.  With it, the two mirrors cancel and the slide shows the source's RIGHT
side the right way round.  So --flip changes two things at once - the text reads
correctly, AND the subject that fills the fat end of the wedge comes from the opposite
edge of the photograph.  Ch07's trading-floor source needed it: unflipped, the wedge was
a backwards restaurant logo; flipped, it is the price board and a trader, reading
correctly.
"""
import argparse, os, sys
from PIL import Image, ImageDraw

# The picture placeholder on the title slide, in EMU — see claude/title-slide-art.md
EXT_CX, EXT_CY = 3015574, 2254385
TARGET_AR = EXT_CX / EXT_CY          # 1.3376, i.e. 4:3
LONG_EDGE = 1800                     # output width; 4:3 at this size is plenty


def frame(img, ar=TARGET_AR, pan=0.0, tilt=0.0, zoom=1.0):
    """Centre-crop `img` to aspect `ar`, then apply zoom/pan/tilt."""
    w, h = img.size
    # Largest window of aspect `ar` that FITS INSIDE w x h.  If the source is
    # NARROWER than the target, width binds; otherwise height binds.  The
    # comparison used to be the wrong way round, so a portrait source produced a
    # crop box wider than the image and PIL padded the overhang with BLACK.
    cw, ch = (w, w / ar) if w / h < ar else (h * ar, h)
    cw, ch = cw / zoom, ch / zoom
    x = (w - cw) / 2 + pan * (w - cw) / 2
    y = (h - ch) / 2 + tilt * (h - ch) / 2
    x = max(0, min(w - cw, x))
    y = max(0, min(h - ch, y))
    return img.crop((round(x), round(y), round(x + cw), round(y + ch)))


def cut(img, bg=None):
    """Keep the lower-left triangle; discard everything above the main diagonal.

    Vertices (0,0)-(0,h)-(w,h).  That is precisely the region PowerPoint will show
    once the shape is mirrored.
    """
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon([(0, 0), (0, h), (w, h)], fill=255)
    out = Image.new("RGBA", (w, h), (bg + (255,)) if bg else (0, 0, 0, 0))
    out.paste(img.convert("RGBA"), (0, 0), mask)
    return out


def hexrgb(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("chapter", type=int)
    ap.add_argument("--pan", type=float, default=0.0)
    ap.add_argument("--tilt", type=float, default=0.0)
    ap.add_argument("--zoom", type=float, default=1.0)
    ap.add_argument("--flip", action="store_true",
                    help="mirror the source first, so on-image text reads correctly")
    ap.add_argument("--bg", default=None, help="#RRGGBB to flood the cut corner")
    ap.add_argument("--outdir", default=".")
    a = ap.parse_args()

    src = Image.open(a.source).convert("RGB")
    if a.flip:
        src = src.transpose(Image.FLIP_LEFT_RIGHT)
    framed = frame(src, pan=a.pan, tilt=a.tilt, zoom=a.zoom)
    framed = framed.resize((LONG_EDGE, round(LONG_EDGE / TARGET_AR)), Image.LANCZOS)

    tri = cut(framed, hexrgb(a.bg) if a.bg else None)
    stem = f"ch{a.chapter:02d}_title"
    out = os.path.join(a.outdir, stem + "_triangle.png")
    tri.save(out)

    # What the slide will show: the same wedge, mirrored.
    prev = tri.transpose(Image.FLIP_LEFT_RIGHT)
    flat = Image.new("RGB", prev.size, (0x00, 0x3D, 0xA5))
    flat.paste(prev, (0, 0), prev)
    pv = os.path.join(a.outdir, stem + "_preview.png")
    flat.save(pv)

    print(f"source     {src.size[0]}x{src.size[1]}" + ("  (mirrored)" if a.flip else ""))
    print(f"cut        {out}")
    print(f"preview    {pv}   <- check the subject is inside the wedge")


if __name__ == "__main__":
    main()
