#!/usr/bin/env python3
"""ECON003_Ch10_..._UCR_v2.pptx - a SURGICAL edit of HIS 20-slide cut, not a rebuild.

WHY v2 IS A NEW FILE.  `~$ECON003_Ch10_Taxation_and_Regulation_UCR.pptx` exists on his
machine, so the deck is open in PowerPoint and anything written underneath it would be
lost.  Ground rules S8.2: when he is editing by hand, write a NEW version number and
leave his file alone.  He asked for v2 explicitly.

WHAT HE CHANGED, and all of it is preserved.  23 slides -> 20:
  * both Exam Check pages deleted
  * one PART divider deleted; the remaining three are correctly renumbered PART 1/2/3
    and reheaded (his PART 2 is now "What Decides the Split", merging my parts 2 and 3)
  * "Intervention Has Costs the Diagram Does Not Show" retitled "Government Failures"
  * every figure resized smaller than the builder placed it - his boxes are kept EXACTLY
    (L/T/W/H read off his file, not recomputed)

WHAT THIS SCRIPT CHANGES, and nothing else:

  1. HIS ACTUAL REQUEST.  "On graph b in page 12 also show the respective prices for
     sellers and buyers.  It is just not clear what prices they are paying.  Check for
     all such instances."

     His page 12 is "Make Demand More Elastic and Sellers Pay More", and he is right:
     panel (b)'s post-tax prices are $7.00 and $5.00 and NEITHER WAS A TICK VALUE, so the
     only numbers on the panel were the shaded bands' "$0.50" and "$1.50" - which are the
     SHARES, and read as prices.  The audit of every figure in both decks found the same
     fault in exactly three places, all in Chapter 10:

       page 11  elast_supply    panel (b): $6.00 not a tick, bands read "$1.50"/"$0.50"
       page 12  elast_demand    panel (b): NEITHER $7.00 nor $5.00 a tick   <- his page
       page 13  dwl_elasticity  both panels: no price shown at all, only the DWL

     Fixed in `ch10_charts.py`, three ways at once so the answer is unmissable:
       - each panel now carries ITS OWN y-axis ticks, and the tick labels are COLOURED -
         what buyers pay in blue, what sellers keep in red, the pre-tax price in grey
       - a two-line block states the outcome in words: "buyers pay $7.00 - bear $0.50",
         "sellers keep $5.00 - bear $1.50".  PRICE FIRST, share second
       - the panel title carries the quantity: "Q falls to 1,750"

  2. THE SAME AMBIGUITY, ONE PAGE EARLIER.  "Where the $2 Goes" labelled its two bands
     "BUYERS $1.00" and "SELLERS $1.00" - the identical trap, and only readable there
     because $7.50/$6.50/$5.50 happened to be tick values.  Now reads
     "BUYERS BEAR $1.00 ($6.50 -> $7.50)".

  3. ONE STALE SPEAKER NOTE.  Deleting both Exam Checks left the TAX INCIDENCE page's
     notes saying the payroll tax "comes back as the first Exam Check".  It does not any
     more.  Rewritten to keep the payroll-tax example, which is worth saying, without
     the forward reference.  Ground rules S10: when a section is deleted, grep the notes
     of every surviving slide.

EVERYTHING ELSE IS UNTOUCHED - no other slide, no other note, no geometry, no order.
Verified by a content diff against his file afterwards (a python-pptx save rewrites every
part, so a byte diff would prove nothing).

CHECKED AND CLEAN, so nothing is done to them: the four Chapter 10 figures that already
name both prices explicitly (the two tax-shift pages annotate "buyers pay $7.50" and
"sellers keep $5.50" on the figure; the ceiling/floor and rent-shift pages put every
control price and equilibrium price on a tick), and all seven Chapter 12 figures, whose
prices - $1.00, $3.50, $2, $4, $6 - are tick values on their own axes.
"""
import copy
import shutil

from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Inches

HIS = "/mnt/user-data/uploads/ECON003_26S/Slides/ECON003_Ch10_Taxation_and_Regulation_UCR.pptx"
OUT = "ECON003_Ch10_Taxation_and_Regulation_UCR_v2.pptx"
F = "figs/ch10_fig_%s.png"

# his slide number -> the figure whose blob belongs there
SWAP = {
    7:  "tax_prod_split",
    11: "elast_supply",
    12: "elast_demand",
    13: "dwl_elasticity",
}

prs = Presentation(HIS)
sl = list(prs.slides)
assert len(sl) == 20, "expected his 20-slide cut, got %d" % len(sl)

for n, fig in SWAP.items():
    s = sl[n - 1]
    pics = [sh for sh in s.shapes if sh.shape_type == 13]
    assert len(pics) == 1, "slide %d has %d pictures" % (n, len(pics))
    pic = pics[0]
    path = F % fig

    # keep HIS box.  Only correct the height if the new figure's aspect drifted, and
    # keep the picture centred on the same line so nothing else on the page moves.
    L, T, W, H = (Emu(pic.left).inches, Emu(pic.top).inches,
                  Emu(pic.width).inches, Emu(pic.height).inches)
    with Image.open(path) as im:
        new_aspect = im.width / im.height
    new_H = W / new_aspect
    cy = T + H / 2
    drift = abs(new_H - H)

    blob = open(path, "rb").read()
    pic.part.related_part(pic._element.blip_rId)._blob = blob
    if drift > 0.005:
        pic.top = Inches(cy - new_H / 2)
        pic.height = Inches(new_H)
    print("  slide %2d  %-16s  aspect %.3f -> %.3f  height %.3f -> %.3f%s"
          % (n, fig, W / H, new_aspect, H, new_H, "  (adjusted)" if drift > 0.005 else ""))

# ---- the one stale forward reference left by his deletion of the Exam Check pages
s5 = sl[4]
notes = s5.notes_slide.notes_text_frame
old = ("Payroll tax is the best one and it comes back as the\nfirst Exam Check: the law "
       "splits it half and half between employer and employee, and\nessentially no "
       "economist thinks the burden splits half and half.")
new = ("Payroll tax is the best one: the law splits it half and half\nbetween employer "
       "and employee, and essentially no economist thinks the burden\nsplits half and "
       "half. Labour supply is famously inelastic, so workers carry most\nof it - which "
       "is Part 2's rule, arriving early.")
assert old in notes.text, "the stale Exam Check reference is not where it was"
notes.text = notes.text.replace(old, new)
print("  slide  5  stale 'first Exam Check' reference rewritten")

prs.save(OUT)
print("wrote", OUT, len(prs.slides._sldIdLst), "slides")
