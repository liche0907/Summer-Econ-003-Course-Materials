#!/usr/bin/env python3
"""fix_slide5.py — bring the Adam Smith slide back to house formatting.

He pasted three things onto slide 5 straight out of the publisher deck:

  * two MathType WMF objects — "Self-interested ≠ selfish" and
    "Maximum well-being ≠ fairness"
  * a text box reading "We are examining how efficient markets lead to the maximum
    level of well-being"

All three arrived in the publisher's formatting: the text box is 18 pt in the theme
font with no colour set (the only run in the whole deck that is not Arial apart from
the inherited title card), it sits at x=0.52 w=9.28 against the house 0.60 / 8.80,
and it runs to y=5.38 — into the 7 pt image credit at 5.40. The two WMFs render at
roughly 28 pt, are horizontally misaligned with each other and with everything else,
and the right-hand one ends at x=9.57, past the 9.40 margin.

The content is his and all of it stays. Only the presentation changes:

  * the two inequalities become one blue formula band — the house pattern for a
    stated relation — at 14.5 pt bold blue, centred, full width
  * the sentence becomes the bottom kicker: hairline rule plus one 13 pt bold
    centred line, which is what every other closing sentence in the deck is
  * both are placed off measured geometry so nothing touches the credit line

Nothing else on the slide is moved: the title, the globe photograph and its frame,
the quotation, the attribution and the gold note band are untouched.

Run:  python3 fix_slide5.py <in.pptx> <out.pptx>
"""
import sys

from pptx import Presentation
from pptx.util import Emu

import deckkit as D
from deckkit import BLUE, INK

SRC = sys.argv[1] if len(sys.argv) > 1 else "v2now.pptx"
OUT = sys.argv[2] if len(sys.argv) > 2 else "v2_slide5fixed.pptx"

BAND_Y = 4.18          # clears the gold note band, which ends at 4.08
KICKER_Y = 4.86        # rule; text lands at 5.04 and ends by 5.26, clear of 5.40

prs = Presentation(SRC)
assert len(prs.slides._sldIdLst) == 44, "expected his 44-slide v2"
s = prs.slides[4]
assert D.Emu(s.shapes[1].top).inches < 0.6 and \
    s.shapes[1].text_frame.text.startswith("One Sentence"), "slide 5 is not the Smith slide"

# ---- what came in from the publisher deck, identified by geometry not by index
doomed = []
for sh in s.shapes:
    x, y = D.Emu(sh.left).inches, D.Emu(sh.top).inches
    w, h = D.Emu(sh.width).inches, D.Emu(sh.height).inches
    if str(sh.shape_type).startswith("PICTURE") and 4.20 < y < 4.60 and h < 0.55:
        doomed.append(sh)                                   # the two WMF equations
    elif sh.has_text_frame and "We are examining how" in sh.text_frame.text:
        doomed.append(sh)                                   # the pasted 18 pt line
assert len(doomed) == 3, f"expected 3 pasted shapes, found {len(doomed)}"
for sh in doomed:
    sh._element.getparent().remove(sh._element)

# ---- the same content, in the house patterns
D.band(s, BAND_Y,
       "Self-interested  ≠  selfish        ·        Maximum well-being  ≠  fairness",
       kind="formula", size=14.5)
D.kicker(s, "We are examining how efficient markets lead to the maximum level of "
            "well-being.", y=KICKER_Y)

D.notes(s, """Adam Smith, and the two distinctions the rest of the hour depends on.

Read the quotation out loud. It is short and it is the most quoted sentence in
economics for a reason.

Two things worth saying about it:

First, the phrase "invisible hand" appears exactly once in The Wealth of Nations, in
Book IV, and Smith used it far more cautiously than the modern slogan does. If a
student asks, that is the honest answer — he was making a narrower argument than the
phrase now carries.

Second, and this is the one to labour: Smith is not describing a moral system. He is
describing an information and incentive system. The butcher does not need to know
you, or care about you, or even know your name. The price does the communicating.

THE BAND — take both halves slowly, because both are places students go wrong.

"Self-interested is not selfish." Students arrive believing economics assumes people
are selfish and they resist the whole chapter because of it. The model needs one
thing: that people act on their own preferences consistently. It says nothing about
what those preferences contain. Someone whose utility rises when their neighbour eats
is self-interested and not selfish, and every result today goes through unchanged.
Good line: "The assumption is not that you are a bad person. The assumption is that
you are a person."

"Maximum well-being is not fairness." This is the promissory note for the last part
of the hour. What we are about to maximise is social surplus, which counts a dollar
of willingness to pay identically whoever holds it. That is a real measure and it is
not a measure of fairness. Say now that we will come back to it, so that when Part 4
says efficiency cannot settle a distributional question, it lands as something
promised rather than something conceded.

The kicker is the frame for Part 1: efficient markets, maximum well-being — and we
are about to make both of those phrases mean something you can compute.

Ask, if there is time: what would it take for a central planner to feed a city as
well as the butchers, brewers and bakers do? Hold the answer until Part 3 — it is the
coordination problem.""")

prs.save(OUT)
print(f"{OUT}: removed 3 pasted shapes, added the formula band and the kicker")
