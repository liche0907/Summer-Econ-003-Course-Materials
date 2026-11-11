#!/usr/bin/env python3
"""Ch06 v2 — the instructor's fifth round of changes. Surgical; nothing is regenerated.

    cp <his ECON003_Ch06_...pptx> work.pptx
    python3 edit_ch06_v2.py

What it does:
  1. Swaps nine figures in place (by slide, since PowerPoint has re-encoded every blob
     and SHA matching no longer works). Each new PNG is fitted to the pixel size already
     embedded, so no picture shape is resized and nothing on any slide moves.
  2. Rebuilds the card row on "Profits Are a Signal" on a McDonald's-versus-Treasury
     comparison instead of corn versus soybeans.
  3. Adds the efficient-scale point to "Why Long-Run Supply Is Flat".
  4. Inserts one new slide after it: what long-run equilibrium looks like as a count of
     restaurants.

Figures changed and why:
  34 profit_max, 37 three_prices, 43 loss_but_open, 52 ps_price_rise
        quantity numbers restored — a specific quantity is read off each of these
  46 shutdown, 47 supply_curve
        MC redrawn through the block midpoints, so it cuts AVC at its minimum
  58 entry, 60 exit
        market panels solved rather than eyeballed; every dashed price line now meets
        the curves where it says it does. Panel (b) gets the same MC treatment, because
        "entry stops at minimum ATC" is a tangency claim too.
  61 lr_supply — unchanged content, re-rendered for consistency
"""
import io
import json

from PIL import Image
from pptx import Presentation
from pptx.util import Inches

import deckkit as D
from deckkit import BLUE, GREEN, RED, DGOLD, GOLD, INK, GREY

SRC, OUT = "work.pptx", "_full.pptx"
F, IC = "figs/ch06_fig_%s.png", "icons/%s.png"

prs = Presentation(SRC)
sl = list(prs.slides)
before = len(sl)
TOUCHED = set()          # every part this script actually changes, for the splice


def find(starts):
    for i, s in enumerate(sl):
        for sh in s.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip().startswith(starts):
                return i, s
    raise SystemExit("NOT FOUND: " + starts)


def fit_to(path, target):
    """New PNG bytes at exactly `target` px, content pinned top-left.

    savefig.bbox='tight' means adding or dropping a row of tick labels changes the
    image height, and a changed aspect inside a picture shape whose size must not move
    comes out stretched. Fit into the embedded box instead and pad the remainder white.
    """
    im = Image.open(path).convert("RGB")
    tw, th = target
    if im.width > tw or im.height > th:
        s = min(tw / im.width, th / im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    canvas = Image.new("RGB", target, "white")
    canvas.paste(im, (0, 0))
    buf = io.BytesIO()
    canvas.save(buf, "PNG", optimize=True)
    return buf.getvalue()


# ============================================================ 1. the nine figure swaps
SWAPS = [("Seeing the Profit", "profit_max"),
         ("Change the Price, Redo the Problem", "three_prices"),
         ("Losing Money and Still Opening the Doors", "loss_but_open"),
         ("The Shutdown Rule", "shutdown"),
         ("The Firm's Supply Curve", "supply_curve"),
         ("What a Price Rise Adds", "ps_price_rise"),
         ("Entry Competes the Profit Away", "entry"),
         ("And Exit Works the Same Way", "exit"),
         ("Why Long-Run Supply Is Flat", "lr_supply")]

for title, fig in SWAPS:
    i, s = find(title)
    pics = [sh for sh in s.shapes if sh.shape_type == 13]
    assert len(pics) == 1, f"slide {i+1} {title!r}: expected 1 picture, found {len(pics)}"
    pic = pics[0]
    part = pic.part.related_part(pic._element.blip_rId)
    target = Image.open(io.BytesIO(part._blob)).size
    part._blob = fit_to(F % fig, target)
    TOUCHED.add(str(part.partname).lstrip("/"))
    print(f"~ slide {i+1:>2}  {fig:<16} refitted into {target[0]}x{target[1]}")


# ================================= 2. "Profits Are a Signal" — McDonald's vs Treasuries
i_sig, s_sig = find("Profits Are a Signal")
for sh in list(s_sig.shapes):                      # the card row only: 2.36 .. 4.21 in
    y = (sh.top or 0) / 914400
    if 2.20 < y < 4.25:
        sh._element.getparent().remove(sh._element)
D.cards3(s_sig, 2.36, 1.85, [
    (BLUE, "The franchise beats the Treasury",
     "Put the $2.1 million a restaurant costs into 10-year Treasuries at 4.65% and it "
     "returns about $98,000 a year, risk-free. Clear more than that and the difference "
     "is economic profit.", IC % "balance-scale"),
    (GREEN, "So more McDonald's open",
     "Anybody who can read the disclosure document can see the same numbers. "
     "Restaurants get built, market supply shifts right — and a supply curve shifting "
     "right means the price comes down.", IC % "house"),
    (RED, "Which shrinks the very profit that attracted them",
     "Entry continues while there is still an advantage over the Treasury. It stops "
     "when there is not.", IC % "up-down"),
], body_size=11)
D.notes(s_sig, """Entry generalised — on the restaurant they have been running all hour.

THE COMPARISON IS THE POINT, and it is the economic-profit slide arriving again with real
money in it. A restaurant costs $1.47 to $2.73 million. Take the midpoint, $2.1 million. The
10-year Treasury paid 4.65% on 7 August 2026, so that same money parked in Treasuries returns
about $98,000 a year and you never get out of bed. Anything the restaurant clears ABOVE that
is economic profit — and the franchise disclosure document is a public filing, so anybody
who wants to run the comparison can.

Then the mechanism, and it is one sentence: everyone who can see the same numbers wants one.
Restaurants get built. Market supply shifts right. A supply curve shifting right means the
price comes down. And the $98,000 gap narrows.

Ask: when does the building stop? When the restaurant returns the same as the Treasury — no
better, no worse — because at that point there is nothing to move money for. That is zero
ECONOMIC profit, and it is the next slide.

ONE HONEST CAVEAT, and say it before a student does. Entry into McDonald's specifically is
not free: the franchisor picks the operators, picks the sites, and decides how many
restaurants a market gets. What IS free is entry into fast food — anybody can open a burger
restaurant, and Chick-fil-A, In-N-Out and everyone else did. The model needs free entry into
the INDUSTRY, not into one company's brand. If anything, McDonald's controlling its own
entry is why its US store count is as stable as the next-but-one slide shows.""")
TOUCHED.add(str(s_sig.part.partname).lstrip("/"))
TOUCHED.add(str(s_sig.notes_slide.part.partname).lstrip("/"))
print(f"~ slide {i_sig+1}  card row rebuilt on McDonald's vs Treasuries")


# =========================== 3. "Why Long-Run Supply Is Flat" — the efficient-scale point
i_lrs, s_lrs = find("Why Long-Run Supply Is Flat")
ANCHOR = list(prs.slides._sldIdLst)[i_lrs]         # captured before anything is added
D.band(s_lrs, 4.90, "And $3.14 is the BOTTOM of the ATC curve — so entry pushes every "
                    "restaurant to its efficient scale. Nobody planned that.",
       kind="answer", size=12)
nf = s_lrs.notes_slide.notes_text_frame
nf.text = nf.text.replace(
    "This is also the ethanol answer arriving a slide early. Let them notice before you say it.",
    """AND THE EFFICIENCY POINT, which is the green band and the strongest claim in the chapter.

$3.14 is not just the price entry settles at. It is the MINIMUM of the average total cost
curve — the one output at which this restaurant makes meals as cheaply as it is capable of
making them. Economists call it the efficient scale.

So in long-run equilibrium every surviving restaurant is producing at the lowest average cost
available to it, and it is selling at exactly that cost. Nobody chose this. No regulator set
the output, no manager was told to minimise average cost for the public's benefit. Each
operator was trying to make money, and entry did the rest.

Say plainly what it does NOT mean, because students over-read it: it does not mean the
outcome is fair, and it does not mean the right number of restaurants exist from society's
point of view. Chapter 10 asks that question. This is a claim about cost, not about welfare.""")
TOUCHED.add(str(s_lrs.part.partname).lstrip("/"))
TOUCHED.add(str(s_lrs.notes_slide.part.partname).lstrip("/"))
print(f"~ slide {i_lrs+1}  efficient-scale band added")


# ============================ 4. the new slide: equilibrium as a count of restaurants
s = D.blank_slide(prs)
D.title(s, "So How Many McDonald's Does America End Up With?")
D.picture_fit(s, F % "mcd_equilibrium", 0.60, 1.02, 8.80, 1.98)
D.cards2(s, 3.12, 1.46, [
    (BLUE, "Twenty years, net minus twenty-one",
     "13,727 US restaurants in 2005. 13,706 in 2025. It peaked at 14,350 in 2014 and "
     "bottomed at 13,438 in 2021 — seven straight years of net closures."),
    (GREEN, "Entry went somewhere else",
     "Of ~2,600 restaurants planned worldwide for 2026, about 750 are in the US and all "
     "International Operated Markets. Over 1,800 are in licensed markets."),
], body_size=10.5)
D.kicker(s, "Nobody chose 13,706. Entry chose it — and then it stopped.", y=4.66)
D.credit(s, "US counts: McDonald's Corp — Q4 2005 earnings release, Q4 releases 2015–2018, "
            "and Forms 10-K FY2020/FY2022/FY2024/FY2025. 2026 plan: FY2025 10-K, MD&A. "
            "Country counts: “Restaurants by Market 2025”. Populations: national "
            "statistical offices; US Census Bureau Vintage 2025 (340,003,797 at 1 Jul 2025).",
         y=5.22)
D.notes(s, """Long-run equilibrium, as a number you can look up. This is the payoff slide for
Part 5 and it is worth three minutes.

THE HEADLINE, and read it out: 13,727 US McDonald's in 2005. 13,706 in 2025. Net change over
twenty years: minus twenty-one restaurants. Out of nearly fourteen thousand.

That is what "the number of firms adjusts until economic profit is zero" looks like when you
go and count. The model does not predict a growing industry or a shrinking one. It predicts a
number that stops moving.

THE PATH MATTERS AS MUCH AS THE ENDPOINT. Point at the hump. The peak was 14,350 in 2014 —
entry overshot. Then SEVEN consecutive years of net closures, 2015 through 2021, bottoming at
13,438. Then back up to 13,706. Exit and entry, both visible, both doing what Part 5 says.
About 200 of the 2020 closures were low-volume restaurants inside Walmart stores; McDonald's
says so in its own 10-K.

PANEL (b) IS THE SECOND LESSON: the equilibrium number is not a law of nature. Same company,
same product, and the US settles at 40 restaurants per million people while Germany settles
at 17 and South Korea at 8. Ask the room why. Good answers: how often people eat out, how
cities are laid out, what the competition is, what land costs. All of those move the cost
curves or the demand curve, and the equilibrium number moves with them. Australia at 39 and
Canada at 37 are within 10% of the US, so the split is not "America is different" — it is
Anglosphere against Europe and East Asia.

THE THIRD POINT, on the second card: entry has not stopped worldwide, it has MOVED. Of about
2,600 openings planned for 2026, at most 750 are in the US and all International Operated
Markets combined; over 1,800 are in developmental licensed markets. Capital goes where the
economic profit still is. That is the chapter's mechanism operating at the level of countries.

SAY THIS OUT LOUD, because it is the difference between teaching evidence and citing it:
McDonald's has never said the US market is saturated. The words "saturation" and
"cannibalization" appear in none of its SEC filings — I checked. The plateau is a measurement;
"the industry reached long-run equilibrium" is OUR interpretation of it. The company describes
the same fact in the language of unit economics and restaurant quality. Students should see
where the data stops and the model starts.

If someone asks about other chains: Subway has about 18,800 US locations and Starbucks about
16,900, both more than McDonald's — and Subway closed 729 US stores in 2025 alone. Biggest is
not the same as settled.""")

lst = prs.slides._sldIdLst
el = list(lst)[-1]
lst.remove(el)
lst.insert(list(lst).index(ANCHOR) + 1, el)
print(f"+ new slide inserted at {i_lrs+2}: 'So How Many McDonald's Does America End Up With?'")

prs.save(OUT)
TOUCHED.add(str(s.part.partname).lstrip("/"))
TOUCHED.add(str(s.notes_slide.part.partname).lstrip("/"))
json.dump(sorted(TOUCHED), open("_manifest.json", "w"), indent=1)
print("manifest:", sorted(TOUCHED))
print(f"\nsaved {OUT}: {before} → {len(Presentation(OUT).slides._sldIdLst)} slides")
