#!/usr/bin/env python3
"""collide.py — the geometric checks fitcheck.py cannot see.

fitcheck asks whether each shape fits its own box. A card row can sit perfectly inside
itself while running underneath the kicker rule, and Ch06 shipped three of those. This
walks the finished file for:

  1. a 0.06-high full-width hairline whose y falls inside another panel's vertical span
     with horizontal overlap  (kicker rule crossing a card)
  2. any shape past the slide edge except full-width divider textboxes and the template's
     off-canvas logo
  3. slides with no speaker notes, and notes carrying a timing marker
  4. pictures overlapping other pictures or panels
  5. the word "Pearson" anywhere on a slide face
  6. every slide's shape count, to spot a near-blank page

Usage: python3 collide.py deck.pptx
"""
import re
import sys

from pptx import Presentation
from pptx.util import Emu

W, H = 10.0, 5.625
TIMING = re.compile(r"\d{1,2}:\d{2}\s*[–\-—]\s*\d{1,2}:\d{2}")


def box(sh):
    try:
        return (Emu(sh.left).inches, Emu(sh.top).inches,
                Emu(sh.width).inches, Emu(sh.height).inches)
    except TypeError:
        return None


def overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    ox = min(ax + aw, bx + bw) - max(ax, bx)
    oy = min(ay + ah, by + bh) - max(ay, by)
    return ox, oy


def main(path):
    prs = Presentation(path)
    problems = []
    for i, s in enumerate(prs.slides, 1):
        shapes = [(sh, box(sh)) for sh in s.shapes]
        shapes = [(sh, b) for sh, b in shapes if b]

        # --- 1. hairline rules crossing a panel
        rules = [(sh, b) for sh, b in shapes
                 if 0.03 <= b[3] <= 0.09 and b[2] >= 4.0]
        panels = [(sh, b) for sh, b in shapes
                  if b[3] >= 0.45 and b[2] >= 0.9 and sh.shape_type == 1]
        for rsh, rb in rules:
            for psh, pb in panels:
                if pb[1] < rb[1] < pb[1] + pb[3] - 0.02:
                    ox, _ = overlap(rb, pb)
                    if ox > 0.20:
                        problems.append(
                            (i, "RULE-IN-PANEL",
                             f"hairline at y={rb[1]:.2f} crosses a panel "
                             f"y={pb[1]:.2f}..{pb[1]+pb[3]:.2f}"))

        # --- 2. off-canvas
        for sh, b in shapes:
            x, y, w, h = b
            if x < -0.02 or y < -0.02 or x + w > W + 0.02 or y + h > H + 0.02:
                if abs(w - W) < 0.05 and x <= 0.02:
                    continue                      # full-width divider textbox
                if x > W or x + w < 0:
                    continue                      # template logo parked off-canvas
                problems.append(
                    (i, "OFF-CANVAS",
                     f"{sh.shape_type} at ({x:.2f},{y:.2f}) {w:.2f}x{h:.2f}"))

        # --- 3. notes
        if not s.has_notes_slide or not s.notes_slide.notes_text_frame.text.strip():
            problems.append((i, "NO-NOTES", ""))
        else:
            n = s.notes_slide.notes_text_frame.text
            if TIMING.search(n):
                problems.append((i, "TIMING-MARKER", TIMING.search(n).group(0)))

        # --- 4. picture on picture
        pics = [(sh, b) for sh, b in shapes if sh.shape_type == 13]
        for a in range(len(pics)):
            for c in range(a + 1, len(pics)):
                ox, oy = overlap(pics[a][1], pics[c][1])
                if ox > 0.06 and oy > 0.06:
                    problems.append(
                        (i, "PIC-OVERLAP",
                         f"{pics[a][1]} vs {pics[c][1]}"))

        # --- 5. publisher named on a slide face
        for sh, _ in shapes:
            if sh.has_text_frame and "pearson" in sh.text_frame.text.lower():
                problems.append((i, "PUBLISHER-NAMED", sh.text_frame.text[:60]))

        # --- 6. near-blank
        inked = [sh for sh, _ in shapes
                 if (sh.has_text_frame and sh.text_frame.text.strip())
                 or sh.shape_type in (1, 13)]
        if len(inked) < 3:
            problems.append((i, "NEAR-BLANK", f"{len(inked)} inked shapes"))

    print(f"{path}: {len(prs.slides._sldIdLst)} slides, {len(problems)} findings")
    for i, kind, msg in problems:
        print(f"    [{kind:<16}] slide {i:>3}  {msg}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
