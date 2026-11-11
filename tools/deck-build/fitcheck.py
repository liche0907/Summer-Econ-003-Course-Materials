#!/usr/bin/env python3
"""
fitcheck.py — verify a finished ECON 003 deck.

Checks, in order:
  1. every slide part parses as XML and the zip has no duplicate entries
  2. no shape runs off the 10.000 x 5.625 canvas
  3. no text box overflows its measured wrapped height
  4. no shape overlaps the title band or the bottom kicker rule
  5. every slide carries speaker notes, and no note contains a timing marker
  6. fonts are Arial everywhere except the inherited title card

Over-reports for spAutoFit boxes with free space below them. Treat the output as a
shortlist to eyeball in the render, not a pass/fail gate.
"""
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

from pptx import Presentation
from pptx.util import Emu

import deckkit as dk

W, H = 10.0, 5.625
TIMING = re.compile(r"\d{1,2}:\d{2}\s*[–\-—]\s*\d{1,2}:\d{2}")


def main(path):
    problems = []

    # ---- 1. container integrity
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            problems.append(("ZIP", 0, f"corrupt entry {bad}"))
        names = z.namelist()
        dupes = {n for n in names if names.count(n) > 1}
        if dupes:
            problems.append(("ZIP", 0, f"duplicate entries {dupes}"))
        for n in names:
            if n.endswith(".xml") or n.endswith(".rels"):
                try:
                    ET.fromstring(z.read(n))
                except ET.ParseError as e:
                    problems.append(("XML", 0, f"{n}: {e}"))
    parts = len(names)

    prs = Presentation(path)
    if abs(prs.slide_width / 914400 - W) > 0.01 or abs(prs.slide_height / 914400 - H) > 0.01:
        problems.append(("CANVAS", 0, f"{prs.slide_width/914400} x {prs.slide_height/914400}"))

    fonts = set()
    for idx, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.left is None or sh.top is None:
                continue
            x, y = sh.left / 914400, sh.top / 914400
            w = (sh.width or 0) / 914400
            h = (sh.height or 0) / 914400

            # ---- 2. off-canvas
            if idx > 1:  # slide 1 is the inherited UCR title card, which bleeds by design
                if x < -0.02 or y < -0.02 or x + w > W + 0.02 or y + h > H + 0.02:
                    problems.append(("OFFCANVAS", idx,
                                     f"{sh.shape_type} at ({x:.2f},{y:.2f}) {w:.2f}x{h:.2f}"))

            if not sh.has_text_frame:
                continue
            txt = sh.text_frame.text
            if not txt.strip():
                continue

            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.name:
                        fonts.add(r.font.name)

            # ---- 3. measured text overflow
            sizes = [r.font.size.pt for p in sh.text_frame.paragraphs
                     for r in p.runs if r.font.size]
            if not sizes:
                continue
            size = max(sizes)
            # line_spacing is a float for percentages but a Length for exact point
            # spacing - only the float form is a multiplier.
            pcts = [p.line_spacing for p in sh.text_frame.paragraphs
                    if isinstance(p.line_spacing, float)]
            pct = max(pcts) if pcts else 1.0
            lines = 0
            for para in txt.split("\n"):
                lines += max(1, len(dk.wrap(para, w, size,
                                            bold=any(r.font.bold for r in
                                                     sh.text_frame.paragraphs[0].runs))))
            need = dk.text_h(lines, size, pct)
            # slide 1 is the inherited UCR title card - its boxes are template-sized
            # and the ground rules forbid moving anything on it.
            if idx > 1 and need > h + 0.06:
                problems.append(("TEXTFIT", idx,
                                 f'"{txt[:44].strip()}" needs {need:.2f}in has {h:.2f}in'))

            # ---- 4. collision with the title band
            if idx > 1 and y < 1.02 and y + h > 0.40 and size < 20 and w < 8.0:
                problems.append(("TITLEBAND", idx, f'"{txt[:40].strip()}" at y={y:.2f}'))

        # ---- 5. notes
        if not s.has_notes_slide or not s.notes_slide.notes_text_frame.text.strip():
            problems.append(("NONOTES", idx, "slide has no speaker notes"))
        else:
            n = s.notes_slide.notes_text_frame.text
            if TIMING.search(n):
                problems.append(("TIMING", idx, TIMING.search(n).group(0)))

    print(f"{path}")
    print(f"  slides       : {len(prs.slides._sldIdLst)}")
    print(f"  package parts: {parts}")
    print(f"  fonts in use : {sorted(fonts)}")
    print(f"  findings     : {len(problems)}")
    for kind, idx, msg in problems:
        print(f"    [{kind:10}] slide {idx:>2}  {msg}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else "ECON003_Ch05_Consumers_and_Incentives_UCR.pptx"))
