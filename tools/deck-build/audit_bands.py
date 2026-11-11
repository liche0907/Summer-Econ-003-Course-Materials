#!/usr/bin/env python3
"""Purpose-built audit for the Ch10/Ch12 decks - the checks fitcheck and collide cannot do.

1. every BAND (y 1.05-4.30, width > 8.0) and KICKER (y 4.45-5.10, width > 8.0) must
   contain a run of >= 3 capitals  (slide-writing-rules S6)
2. no welded words: scan every rendered run for [a-z][A-Z] outside a whitelist
3. no backslash-escaped dollar signs leaked from matplotlib strings
4. no exhibit number in any slide TITLE
5. no slide-number reference on a face or in the notes
6. notes present on every slide
7. the word "Pearson" on no slide face
"""
import re, sys
from pptx import Presentation
from pptx.util import Emu

CAPS = re.compile(r"\b[A-Z]{3,}(?:[ /-][A-Z]{2,})*\b")
WELD = re.compile(r"[a-z][A-Z]")
WELD_OK = re.compile(r"(kWh|MyLab|MC|ATC|MR|PowerPoint|McDonald)")
EXH = re.compile(r"\bExhibit\s+\d", re.I)
SLIDENUM = re.compile(r"\bslides?\s+\d+\b", re.I)

def inches(v):
    return None if v is None else Emu(v).inches

for path in sys.argv[1:]:
    prs = Presentation(path)
    print("=" * 70); print(path)
    bands = kicks = 0
    bad_band = bad_kick = []
    bad_band, bad_kick, weld, esc, exh, sn, nonotes, pears = [], [], [], [], [], [], [], []
    for i, s in enumerate(prs.slides, 1):
        title = None
        for sh in s.shapes:
            if not sh.has_text_frame:
                continue
            t = sh.text_frame.text.strip()
            if not t:
                continue
            y, w, x = inches(sh.top), inches(sh.width), inches(sh.left)
            if y is not None and 0.40 <= y <= 0.60 and w and w > 8.0 and title is None:
                title = t
            if "pearson" in t.lower():
                pears.append((i, t[:50]))
            if "\\$" in t:
                esc.append((i, t[:60]))
            for m in WELD.finditer(t):
                frag = t[max(0, m.start() - 6):m.end() + 8]
                if not WELD_OK.search(frag):
                    weld.append((i, frag))
            if y is None or w is None:
                continue
            if x is None or x < 0.30 or w > 9.20:
                continue        # dividers and the takeaways field span the slide
            if 1.05 <= y <= 4.30 and w > 8.0 and len(t) > 30:
                bands += 1
                if not CAPS.search(t):
                    bad_band.append((i, t[:70]))
            if 4.45 <= y <= 5.10 and w > 8.0 and len(t) > 30:
                kicks += 1
                if not CAPS.search(t):
                    bad_kick.append((i, t[:70]))
        if title and EXH.search(title):
            exh.append((i, title))
        notes = s.notes_slide.notes_text_frame.text.strip() if s.has_notes_slide else ""
        if not notes:
            nonotes.append(i)
        if SLIDENUM.search(notes):
            sn.append((i, SLIDENUM.search(notes).group(0)))
    print(f"  bands checked {bands}, kickers checked {kicks}")
    for label, rows in (("BAND WITHOUT A TERM", bad_band), ("KICKER WITHOUT A TERM", bad_kick),
                        ("WELDED WORD", weld), ("BACKSLASH-DOLLAR", esc),
                        ("EXHIBIT NUMBER IN TITLE", exh), ("SLIDE-NUMBER REFERENCE", sn),
                        ("PEARSON ON A FACE", pears)):
        for r in rows:
            print(f"    [{label}] slide {r[0]}: {r[1]}")
    if nonotes:
        print("    [NO NOTES] slides", nonotes)
    total = sum(map(len, (bad_band, bad_kick, weld, esc, exh, sn, pears))) + len(nonotes)
    print(f"  findings: {total}")
