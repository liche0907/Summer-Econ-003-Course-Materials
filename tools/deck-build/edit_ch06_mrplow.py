#!/usr/bin/env python3
"""Surgical edits to the instructor's OWN Ch06 deck. Nothing is regenerated.

Run against a fresh copy of his file, never against a build output:

    cp <his ECON003_Ch06_...pptx> work.pptx
    python3 edit_ch06_mrplow.py

What it does, and nothing else:
  1. Rebuilds the Mr. Plow analysis page on a MARKET-ONLY diagram, so it can run in
     Part 1 with nothing but Chapter 4 behind it.
  2. Moves the Mr. Plow clip pair to Part 1, immediately after "Free Entry and Free Exit".
  3. Adds one new Part 6 slide carrying the firm-level entry diagram the move displaced.
  4. Rewords the ethanol slide's kicker, which still referred to an opening show of hands
     on a slide the instructor had deleted.

Every other slide is left byte-identical.
"""
from pptx import Presentation
import deckkit as D

SRC = "work.pptx"
OUT = "ECON003_Ch06_Sellers_and_Incentives_UCR.pptx"

prs = Presentation(SRC)
sl = list(prs.slides)
before = len(sl)


def find(title_starts):
    for i, s in enumerate(sl):
        for sh in s.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip().startswith(title_starts):
                return i, s
    raise SystemExit("NOT FOUND: " + title_starts)


def set_single_line(shape, text):
    """Replace a multi-run, multi-paragraph textbox with one line, keeping its formatting."""
    paras = shape.text_frame.paragraphs
    runs = [r for p in paras for r in p.runs]
    assert runs, "no runs to write into"
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""


i_clip, s_clip = find("What Happens to a Good Business?")
i_ana, s_ana = find("Why Homer's Profit Vanished")
i_free, _ = find("Free Entry and Free Exit")
i_sig, _ = find("Profits Are a Signal")
i_eth, s_eth = find("So: How Does an Ethanol Subsidy")
print(f"located  clip={i_clip+1}  analysis={i_ana+1}  free-entry={i_free+1}  "
      f"signal={i_sig+1}  ethanol={i_eth+1}")

# ---- 1. the analysis page, rebuilt for Part 1 -------------------------------------
for sh in list(s_ana.shapes):
    if sh.shape_type == 13:                       # drop the old market+firm figure
        sh._element.getparent().remove(sh._element)
D.picture_fit(s_ana, "figs/ch06_fig_entry_market.png", 0.60, 1.05, 8.80, 2.90)
for sh in s_ana.shapes:
    if sh.has_text_frame and "minimum ATC" in sh.text_frame.text:
        set_single_line(sh, "Free entry is not a detail. It is the condition that decides "
                            "what happens to every profit in this chapter.")
D.notes(s_ana, """Clip page 2 of 2. The analysis — and it needs nothing but Chapter 4.

Ask FIRST: what exactly went wrong for Homer? Take answers. The right one is "nothing". He
was not outcompeted on quality, he made no bad decision, and the snow kept falling. Somebody
simply saw that he was doing well and bought a plough.

The diagram is the whole of it, and every piece is Chapter 4: one more seller means market
supply shifts right, and a supply curve shifting right means the price comes down. Here from
$4 to $3.

The sentence to land, and it is the chapter's thesis arriving in the first ten minutes: the
profit is not destroyed by bad luck. It is destroyed by the RESPONSE to it. The profit
existed, it was visible, and nothing stopped anyone acting on it.

What we CANNOT say yet, and do not try: where the price stops falling. That needs the firm's
average cost curve, which is forty minutes away. Tell them so explicitly — "we will find out
exactly where this stops in Part 6" — and the gap becomes a promise instead.

Callback to set up now: the Pawpsicle clip is next. Nick's margin is wide for the same reason
Homer's was, and it will die the same way.""")
print("~ analysis page rebuilt on the market-only diagram")

# ---- 2. move the pair into Part 1 --------------------------------------------------
lst = prs.slides._sldIdLst
ids = list(lst)
clip_el, ana_el = ids[i_clip], ids[i_ana]
lst.remove(clip_el)
lst.remove(ana_el)
pos = list(lst).index(ids[i_free]) + 1
lst.insert(pos, clip_el)
lst.insert(pos + 1, ana_el)
print(f"~ clip pair moved to slides {pos + 1}-{pos + 2}")

# ---- 3. Part 6 keeps the firm-level entry diagram ----------------------------------
s_new = D.blank_slide(prs)
D.title(s_new, "Entry Competes the Profit Away")
D.picture_fit(s_new, "figs/ch06_fig_entry.png", 0.60, 1.05, 8.80, 2.90)
D.band(s_new, 4.06, "Entry stops when P = minimum ATC = $3.14, because at that price there "
                    "is nothing left to attract anybody.", kind="answer", size=12.5)
D.notes(s_new, """Homer's clip, finished — the answer to the question left open in Part 1.

In Part 1 we watched entry drive a price down and said we could not yet say where it stops.
This is where.

NUMBERS: price starts at $4 with the restaurant making $60 an hour. Entry shifts market supply
right. Price falls to $3.14 — the MINIMUM of ATC — at 70 meals per restaurant. Economic profit
is then zero.

Why exactly minimum ATC, and not some other price? Because entry continues while profit is
positive, and profit is positive whenever price exceeds ATC at the chosen quantity. The only
price at which the firm can just break even is the one that touches ATC at a single point —
its minimum.

Two consequences worth saying:
  - Firms end up producing at the lowest possible average cost. Nobody planned that.
  - This is the strongest efficiency claim in the chapter, and Chapter 10 asks what it is
    worth.

Then close the loop out loud, all three at once: Nick's margin was wide because he was the
only seller outside that bank. Homer's was wide because he was the only plough in Springfield.
Neither is a fact about popsicles or snow. Both are facts about how many people are selling —
and the ethanol subsidy is about to be the third.""")
new_el = list(lst)[-1]
lst.remove(new_el)
lst.insert(list(lst).index(ids[i_sig]) + 1, new_el)
print("+ Part 6: 'Entry Competes the Profit Away' added after 'Profits Are a Signal'")

# ---- 4. the ethanol kicker no longer points at a deleted slide ---------------------
OLD = "Take the show of hands again. Then ask who actually captured the subsidy."
NEW = "So who actually captured the subsidy? Not the producers who came later."
hit = False
for sh in s_eth.shapes:
    if sh.has_text_frame and OLD in sh.text_frame.text:
        for pa in sh.text_frame.paragraphs:
            for r in pa.runs:
                if OLD in r.text:
                    r.text = r.text.replace(OLD, NEW)
                    hit = True
assert hit, "ethanol kicker not found"
nf = s_eth.notes_slide.notes_text_frame
nf.text = nf.text.replace(
    "Go back to the board and read out the show of hands from slide 4. Most of the room said\n"
    "producers end up better off. The model says: only the ones who were already there when it was\n"
    "announced, and only until entry catches up.",
    "Put the question to the room now, if you have not already: are ethanol producers better off\n"
    "a year after the subsidy arrives? Most will say yes. The model says: only the ones who were\n"
    "already there when it was announced, and only until entry catches up.")
print("~ ethanol kicker and notes reworded")

prs.save(OUT)
print(f"\nsaved {OUT}: {before} → {len(Presentation(OUT).slides._sldIdLst)} slides")
