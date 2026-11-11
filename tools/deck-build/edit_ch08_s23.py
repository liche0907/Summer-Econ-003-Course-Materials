#!/usr/bin/env python3
"""Rebuild slide 23, "What the United States Actually Trades", around the book's own
three exhibits instead of describing them in words.

On instruction: "include the actual pictures of aggregate, crude oil and manufactured
goods". Ch08 was built without redrawing Exhibits 8.9, 8.10 and 8.11 because their
long-descriptions give only about ten approximate readings each and redrawing sixty
years of data from approximations would be inventing a figure (ground rules S6). The
honest way to put them on the slide is therefore to LIFT the publisher's own rendered
exhibits rather than to reconstruct them — which is a deliberate exception to "charts:
redraw, never lift", and is why this slide now carries image_credit().

The three card bodies that described the exhibits move into the notes: with the figures
on the page they were describing something the students could not see.

Sources: Acemoglu_Micro_3e_Ch08 (1).pptx slides 63, 64, 65. 8.11 ships as two panels;
panel (a), U.S. exports and imports of manufactured goods, is the one the card text was
about, and panel (b) is left in the book.
"""
import copy
import sys

from pptx import Presentation
from pptx.util import Inches

import deckkit as D
from deckkit import BLUE, GREY, RULE

SRC = sys.argv[1] if len(sys.argv) > 1 else "his_v5.pptx"
DST = sys.argv[2] if len(sys.argv) > 2 else "v7_pre.pptx"
N = 23

FIGS = [("exflat/ch08_exhibit_89.png",   "8.9 — The aggregate"),
        ("exflat/ch08_exhibit_810.png",  "8.10 — Crude oil"),
        ("exflat/ch08_exhibit_811a.png", "8.11(a) — Manufactured goods")]

# three columns across the content width, 0.15 in apart
COL_W = (D.CONTENT_W - 0.30) / 3.0
COL_X = [D.M, D.M + COL_W + 0.15, D.M + 2 * (COL_W + 0.15)]
FIG_TOP, FIG_BOT = 1.86, 4.14          # the band above ends at 1.80, captions below
CAP_Y = 4.18

prs = Presentation(SRC)
s = prs.slides[N - 1]

# --- 1. strip the card row (panels, accent bars, labels, bodies, spot icons) -------
KEEP = {2, 3, 4, 5, 21, 22}            # tab, title, lead band + its text, kicker rule + line
for sh in list(s.shapes):
    if sh.shape_id not in KEEP:
        sh._element.getparent().remove(sh._element)

# --- 2. the lead band has to come down to ONE line to pay for the figure height ---
for sh in s.shapes:
    if sh.shape_id == 5:
        tf = sh.text_frame
        # The band was HARD-WRAPPED into two paragraphs when it was built two lines
        # tall. Rewriting only paragraphs[0] leaves the orphan "imports." behind on a
        # second line, which is what `fitcheck` reported as needing 0.56 in in a 0.30 in
        # box. Drop every paragraph after the first, and every run after the first
        # inside it, so the run's bold/colour survives and nothing else does.
        for extra in list(tf.paragraphs)[1:]:
            extra._p.getparent().remove(extra._p)
        p0 = tf.paragraphs[0]
        for extra in list(p0.runs)[1:]:
            extra._r.getparent().remove(extra._r)
        p0.runs[0].text = (
            "TRADE DEFICIT — imports exceed exports.    "
            "TRADE SURPLUS — exports exceed imports.")
        for p in tf.paragraphs:
            for r in p.runs:
                r.font.size = D.Pt(13.5)
        sh.top, sh.height = Inches(1.22), Inches(0.30)
    if sh.shape_id == 4:               # the tinted panel behind it
        sh.top, sh.height = Inches(1.12), Inches(0.58)

# --- 3. the three exhibits, centred in equal boxes so the row reads level ---------
for (path, cap), x in zip(FIGS, COL_X):
    from PIL import Image
    with Image.open(path) as im:
        pw, ph = im.size
    box_h = FIG_BOT - FIG_TOP
    scale = min(COL_W / pw, box_h / ph)
    w, h = pw * scale, ph * scale
    px = x + (COL_W - w) / 2
    py = FIG_TOP + (box_h - h) / 2
    s.shapes.add_picture(path, Inches(px), Inches(py), Inches(w), Inches(h))
    size = D.fit_one_line(cap, COL_W, 10.5, 8, bold=True)
    D.textbox(s, x, CAP_Y, COL_W, 0.24, cap, size=size, bold=True,
              color=BLUE, align="ctr")

# --- 4. the one piece of on-slide attribution the ground rules permit -------------
D.image_credit(s)

D.notes(s, """What the United States actually trades — the book's three data exhibits,
8.9, 8.10 and 8.11, on the page rather than described.

These are the publisher's own figures, lifted rather than redrawn. Their underlying
series are not in the deck — only approximate readings — so redrawing them would have
meant inventing sixty years of data. Say nothing about their provenance in class; the
credit line is bottom-right.

Take them left to right, and the point of the slide is the CONTRAST between them, not
any one series.

8.9, THE AGGREGATE. Exports and imports both grew enormously since 1960 — from almost
nothing on this scale to roughly $2.5 trillion of exports against $3.1 trillion of
imports. The shape to point at: the two lines track each other closely until the
mid-1970s and then imports pull away and stay ahead. That gap IS the trade deficit, and
it is the only place in the chapter where they see it drawn.

Note the 2008-09 notch in both lines. Worth ten seconds: trade collapses faster than
output in a recession, and it recovers faster too.

8.10, CRUDE OIL. A completely different shape, and this is why the slide exists. Imports
climb to about 22 quadrillion BTU by 2005, then fall hard; exports sit on the floor for
fifty years and only lift after 2014, when the export ban went. One good, running
against the aggregate.

8.11(a), MANUFACTURED GOODS. The two lines are almost identical until about 2000 and
then imports separate decisively. This is the bulk of the reason the US is a net
importer overall. Meanwhile it is a major exporter of food, services and films — which
is the fourth panel of the opener, so call back to it.

Then the kicker, and make them say it back: "net importer" is a statement about a
TOTAL. Three goods, three different stories, one aggregate. A student who leaves
thinking "the US imports things and exports nothing" has read the total and none of the
detail.

The book carries a panel (b) on 8.11 as well — exports of manufactured goods by
destination. It is not needed for this argument and it is in the text.""")

prs.save(DST)
print(f"{DST}: slide {N} rebuilt, {len(s.shapes)} shapes")
