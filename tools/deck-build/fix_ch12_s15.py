#!/usr/bin/env python3
"""fix_ch12_s15.py - rebuild HIS slide 15 to house format, and nothing else.

HIS INSTRUCTION: "Fix page 15 to maintain same format across the deck."

WHAT WAS WRONG WITH IT.  He drew the page by hand in PowerPoint, so none of it sat on
the deck's grid:

    title  TEXT_BOX  at y = 0.26, 0.93 in tall   house is y = 0.48, one line, autofit
                                                 -- it wrapped to two lines and ran
                                                 straight through the gold accent tab
    left picture     at x = 0.04                 house left margin is 0.60
    right GROUP      running to x = 9.96         house right margin is 9.40
    body   TEXT_BOX  0.28, 3.82, 11.48 x 1.46    1.76 in of it hangs off the right edge
                                                 of a 10 in slide; the last line is cut
    body type        red 20 pt PowerPoint bullets with a 14 pt sub-bullet -- no other
                                                 page in either deck uses bullets at all
    no band, no kicker rule, no source line, and no speaker notes.

WHAT IS KEPT, all of it.  The argument is his and it is a good one, so every element of
it survives: both comic strips, the corrected $15 sign he layered onto the second
strip's first panel, the two second-order effects, and the "(Not Required)" marker that
tells the room this is intuition rather than examinable material.

  * THE TWO STRIPS ARE NOW TWO PICTURES, not a picture plus a two-image GROUP.  His
    group held the whole round-2 strip at 6.24 x 3.48 with a redrawn panel-1 pasted on
    top at 1.97 x 3.31, cropped down to a 5.31 x 2.61 window on the slide.  That is
    impossible to animate and impossible to move.  The overlay is composited into the
    strip once, here, at exactly the offsets his group used
    (0.11/6.24, 0.08/3.48, 1.97/6.24, 3.31/3.48), and the result written to
    figs/ch12_fig_mr_round2.png.  What renders is pixel-for-pixel what he built.

  * HIS TWO EFFECTS BECOME THE BAND, in the deck's own voice.  "The guy in plaid is
    contributing $5 less than the girl in white" is the OUTPUT effect; "there was one
    more person in queue asking for $5 refund" is the PRICE effect.

  * THE KICKER SAYS THE RESULT HIS TITLE ASKS FOR.  Each further $5 cut loses $5 more
    in refunds AND takes in $5 less at the gate, so marginal revenue falls $10 for every
    $5 the price falls - which IS "twice as steep", and the page never actually said it.

  * SOURCE LINE.  The strips are his own AI-made art, not the publisher's, and the
    ground rules require any non-publisher figure to say so.

TWO PICTURES RATHER THAN ONE COMPOSITE, deliberately: it gives the page a round-1 click
and a round-2 click, which is the order he tells it in.  See ch12_animate.py, FORCED.

The existing <p:timing> on this slide dies with the shapes it referenced; the animation
pass writes a new one.
"""
import sys

from pptx import Presentation
from pptx.util import Inches

import deckkit as D

SRC = sys.argv[1] if len(sys.argv) > 1 else "his_c12.pptx"
DST = sys.argv[2] if len(sys.argv) > 2 else "c12_s15fixed.pptx"
N = 15

prs = Presentation(SRC)
s = list(prs.slides)[N - 1]

before = [(str(sh.shape_type).split()[0], sh.shape_id) for sh in s.shapes]
assert [k for k, _ in before] == ["PICTURE", "GROUP", "AUTO_SHAPE", "TEXT_BOX", "TEXT_BOX"], \
    "slide %d is not the hand-drawn page this script was written for: %r" % (N, before)
assert "twice as steep" in s.shapes[4].text_frame.text.lower() or \
       "twice as steep" in s.shapes[3].text_frame.text.lower()

for sh in list(s.shapes):
    sh._element.getparent().remove(sh._element)

D.title(s, "Why MR Falls Twice as Fast as the Price (Not Required)")
yb = D.band(s, 1.12,
            "SECOND-ROUND OUTPUT EFFECT: the new buyer pays $5 LESS than the last one "
            "did.   SECOND-ROUND PRICE EFFECT: the refund now goes to ONE MORE earlier "
            "buyer.", kind="formula", size=13.5)
top = yb + 0.08
FLOOR = 4.42
D.picture_fit(s, "figs/ch12_fig_mr_round1.png", 0.60, top, 4.35, FLOOR - top)
D.picture_fit(s, "figs/ch12_fig_mr_round2.png", 5.05, top, 4.35, FLOOR - top)
D.kicker(s, "Every $5 cut costs $5 MORE in refunds and brings in $5 LESS at the gate — "
            "so MARGINAL REVENUE falls $10 each time the PRICE falls $5.", y=4.52)
D.credit(s, "Our own illustration — the book states the result and does not derive it")

D.notes(s, """NOT REQUIRED, and say so out loud before you start. Nobody is examined on
why the MR line is exactly twice as steep. This page is here because every year somebody
asks, and because the answer makes the previous page stick.

THE SET-UP, in one sentence: the gate is the monopolist, and each price cut has to be
given to everybody already through it.

ROUND 1, the left strip - this is the previous page again, in pictures. $20 posted, the
girl with the backpack walks away. Drop the sign to $15 and she pays. And then the family
already inside comes back to the window, because they paid $20 for the same ticket. One
new customer at $15, one refund of $5.

ROUND 2, the right strip - this is the new part. $15 posted, the boy in plaid says no.
Drop the sign to $10 and he pays. Both things have got worse, and by the same $5:

   THE OUTPUT EFFECT. He hands over $10. The girl last round handed over $15. The new
   customer is worth $5 LESS than the last new customer was.

   THE PRICE EFFECT. Now TWO people are at the window wanting $5 back - the family AND
   the girl in white, who is herself only inside because of round 1. The refund bill is
   $5 BIGGER than last round.

ADD THEM. The price fell $5. Marginal revenue fell $5 + $5 = $10. Do it again and it
falls another $10. Twice the slope, and that is the whole proof - no calculus on the
board, and no algebra they have to reproduce.

IF SOMEONE WANTS THE ALGEBRA, it is one line and it belongs in office hours, not here:
with P = a - bQ, total revenue is aQ - bQ², so MR = a - 2bQ. Same intercept, double the
slope.

WHERE IT PAYS OFF: on the graph task. If they ever have to sketch MR themselves, the
trick is that MR starts at the SAME point on the vertical axis as demand and hits the
horizontal axis at HALF the quantity demand does. That is the one usable consequence of
this page.""")

# Deleting a picture's shape does not delete the RELATIONSHIP that pointed at its image
# part, and an orphaned r:id keeps a dead image alive in the package (it cost 2.2 MB
# here). Drop every image rel this slide no longer names.
xml = s._element.xml
for rId, rel in list(s.part.rels.items()):
    if rel.reltype.endswith("/image") and ('r:embed="%s"' % rId) not in xml \
            and ('r:link="%s"' % rId) not in xml:
        s.part.drop_rel(rId)
        print("   dropped dead image rel", rId)

prs.save(DST)
print("rebuilt slide %d; wrote %s" % (N, DST))
for sh in s.shapes:
    print("   %-10s id%-4d %.2f,%.2f %.2fx%.2f  %s"
          % (str(sh.shape_type).split()[0], sh.shape_id,
             sh.left / 914400, sh.top / 914400, sh.width / 914400, sh.height / 914400,
             (sh.text_frame.text.split("\n")[0][:48] if sh.has_text_frame else "")))
