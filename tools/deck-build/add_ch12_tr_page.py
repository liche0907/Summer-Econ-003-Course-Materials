#!/usr/bin/env python3
"""add_ch12_tr_page.py - insert the TOTAL REVENUE page after his slide 15.

HIS INSTRUCTION: "add a graph of Total Revenue of the firm after slide 15, and segregate
it into different regions that correspond to the table in the previous pages", then:
"the region descriptions should be comparing MR, MC, and price effect/quantity effects".

THIS REVERSES A CUT, and the reversal is right.  `build_ch12.py` dropped Exhibit 12.7
(price, MR and total revenue on one figure) as redundant with the quantity-effect /
price-effect page.  What that judgement missed is that the TURN in total revenue is
already sitting in the Exhibit 12.5 table two pages earlier - $1,750 at Q = 500, $1,800
at 600, $1,750 AGAIN at 700 - and almost nobody reads a table well enough to see it.
Drawn, it is unmissable.  The figure is `tr_regions` in `ch12_charts.py`, total revenue
ALONE; the publisher's version stacks price and MR on the same axes and is unreadable at
lecture size.

THE THREE REGIONS ARE NAMED IN THE PREVIOUS PAGE'S OWN TERMS, which is his second
instruction and the reason the page belongs HERE rather than anywhere else:

    Q < 500      QUANTITY EFFECT > PRICE EFFECT.  MR runs $5 down to $2 and stays ABOVE
                 MC = $1.  Revenue rises and profit rises with it.
    500 - 600    QUANTITY EFFECT STILL WINS - MR is positive, so revenue is STILL RISING
                 - but MR has fallen BELOW MC.  Profit is already falling.
    Q > 600      PRICE EFFECT > QUANTITY EFFECT.  MR turns NEGATIVE and revenue FALLS.

The y-axis ticks are the table's own total-revenue column, so a student can put a finger
on a row and find it on the curve.

RUN ON HIS FILE, NOT ON MINE.  He has edited the delivered v2 - slide 2's kicker lost a
line break, and slide 7's "licence" became "license".  Both survive because this script
opens his file and adds one slide to it.

python-pptx can only APPEND a slide, so the new slide is created at the end and its
sldId element is then moved to index 15.  Everything after it shifts by one, which is why
`ch12_animate.py`'s RECAP and OWNER constants move with it.
"""
import sys

from pptx import Presentation

import deckkit as D

SRC = sys.argv[1] if len(sys.argv) > 1 else "his_c12v2.pptx"
DST = sys.argv[2] if len(sys.argv) > 2 else "c12_tr_added.pptx"
AFTER = 15                       # his "Why MR Falls Twice as Fast as the Price"
FIG = "figs/ch12_fig_tr_regions.png"
FIG_FLOOR = 4.42

prs = Presentation(SRC)
sl = list(prs.slides)
assert len(sl) == 25, "expected his 25-slide cut, got %d" % len(sl)
head = next((sh.text_frame.text for sh in sl[AFTER - 1].shapes
             if sh.has_text_frame and sh.text_frame.text.strip()), "")
assert "Twice as Fast" in head, \
    "slide %d is not the page this one goes after; it reads %r" % (AFTER, head[:60])

s = D.blank_slide(prs)
D.title(s, "Where Total Revenue Rises, Peaks, and Falls")
yb = D.band(s, 1.12,
            "TOTAL REVENUE = P × Q. It RISES while the QUANTITY EFFECT beats the PRICE "
            "EFFECT, PEAKS where MR = $0, and FALLS once the PRICE EFFECT wins.",
            kind="formula", size=13.5)
top = yb + 0.10
D.picture_fit(s, FIG, D.M, top, D.CONTENT_W, FIG_FLOOR - top)
D.kicker(s, "The monopolist stops at 500 — SHORT of the revenue peak at 600. "
            "MAXIMISING REVENUE IS NOT MAXIMISING PROFIT.", y=4.52)
D.credit(s, "Drawn from the Exhibit 12.5 table on the revenue-and-cost page — "
            "Acemoglu, Laibson & List, ch. 12")

D.notes(s, """The table two pages back already contained this page. Almost nobody reads a
table well enough to see it, so draw it.

START ON THE TABLE, not on the curve. Ask them to read the TOTAL REVENUE column down:
$1,750 at 500 — $1,800 at 600 — and $1,750 AGAIN at 700. It goes up and then it comes
back down, and it passes through the same number twice. That is the whole page, and it
was on a slide they have already seen.

THE THREE REGIONS, and name them in the language of the price-effect page, because that
is where marginal revenue came from:

  GREEN, up to 500. The QUANTITY EFFECT beats the PRICE EFFECT comfortably. Marginal
  revenue runs from $5 down to $2 and stays ABOVE marginal cost of $1. Every extra pill
  brings in more than it costs. Revenue rises, profit rises.

  GOLD, 500 to 600, and this is the region worth the page. The quantity effect STILL
  wins — marginal revenue is still positive, so TOTAL REVENUE IS STILL RISING. But
  marginal revenue has dropped BELOW marginal cost. Revenue is going up and PROFIT IS
  ALREADY GOING DOWN. So the firm stops at 500 and leaves $50 million of revenue on the
  table on purpose.

  RED, past 600. The PRICE EFFECT now beats the quantity effect. Marginal revenue is
  NEGATIVE — at 700 it is minus a dollar — and selling more brings in LESS money. No firm
  ever operates here, which is why the bottom rows of the table are choices nobody makes.

THE SENTENCE TO PUT ON THE BOARD: a monopolist does NOT maximise revenue. It maximises
profit, and profit stops rising before revenue does. Anyone who answers "the monopolist
produces where total revenue is highest" has just written Q = 600 instead of Q = 500, and
that is a whole question gone.

THE GEOMETRY WORTH POINTING AT: the peak of total revenue sits exactly under the point
where MR crosses zero. Same quantity, 600, on both figures. If they can see that, they
understand that MR is the SLOPE of total revenue — which is the calculus, without the
calculus.

AND THE PUBLISHER'S OWN SLIP, if anyone is reading the e-text description: it ends this
curve at "about $100 million" at Q = 1,200. Price is $0 there, so total revenue is $0.
Ours ends at zero.""")

xml = prs.slides._sldIdLst
ids = list(xml)
xml.remove(ids[-1])
xml.insert(AFTER, ids[-1])

prs.save(DST)
print("inserted a slide at position %d; wrote %s (%d slides)"
      % (AFTER + 1, DST, len(prs.slides._sldIdLst)))
for i, sd in enumerate(Presentation(DST).slides, 1):
    if i in (AFTER, AFTER + 1, AFTER + 2):
        t = next((sh.text_frame.text for sh in sd.shapes
                  if sh.has_text_frame and sh.text_frame.text.strip()), "")
        print("   %2d  %s" % (i, t.split("\n")[0][:64]))
