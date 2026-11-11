#!/usr/bin/env python3
"""Build ECON003_Ch12_Monopoly_UCR.pptx - 25 slides, static.

SCOPE, his call, recorded in `claude/lecture-scope-ch10-ch12.md`:

    COVERED   12.1  Introducing a New Market Structure
              12.2  Sources of Market Power
              12.3  The Monopolist's Problem
              12.4  Choosing the Optimal Quantity and Price
              12.5  The "Broken" Invisible Hand: The Cost of Monopoly
              12.7  Government Policy toward Monopoly   -- two pages, restored on request

    NOT COVERED   12.6  Restoring Efficiency (PRICE DISCRIMINATION), by instruction
                  Exhibit 12.7 (price, MR and total revenue together) - redundant with
                        the quantity-effect / price-effect page
                  the five-slide end-of-chapter EBE problem

PRICE DISCRIMINATION IS THE ONE CUT WITH A REAL COST, and it is recorded here so nobody
has to rediscover it.  The PREVIOUS offering of this course gave price discrimination an
entire chapter, and its final examined it by name: perfect price discrimination captures
all consumer surplus, CS = 0 but DEADWEIGHT LOSS = 0 too, output equals the competitive
quantity, plus a four-way CS/PS/SW comparison across competition, monopoly, imperfect and
perfect discrimination.  It is also half of this book's own Key Idea 5.  TWO THINGS MUST
FOLLOW: the final's Chapter 12 draw has to exclude price-discrimination items (the Pearson
bank is full of them), and the recap page names 12.6 as in the book and not lectured.

Section 12.7 stays precisely because the previous final examined it too - "antitrust,
remove trade barriers, price regulation (fair-return at ATC, MC for allocative
efficiency)" and the graph task "natural monopoly graph: LRATC downward sloping, MC below
ATC, tell profits/losses under socially efficient prices, regulated prices, and
monopolistic price".  Without it the deck would end on "the invisible hand is broken" with
no remedy, in the LAST LECTURE OF THE COURSE.

THE PUBLISHER'S OWN PRICE-REGULATION SLIDE CANNOT BE USED.  It re-uses Exhibit 12.11,
where their notes and description both put MC = ATC = $1 - so the fair-return price
(P = ATC) and the efficient price (P = MC) are the SAME NUMBER and the whole point is
invisible.  Their notes hedge it in the subjunctive.  So that page is drawn on a natural
monopoly with genuine economies of scale, stated as primitives in `ch12_charts.py` and
labelled in the notes as our own worked example.

SOURCES.  `Slides/Pearson/Acemoglu_Micro_3e_Ch12 (1).pptx`, 64 slides, 38 media parts.
ONE usable photograph (the pill bottle spilling money, their EBE opener); the Daraprim
"price hike" graphic is a CHART, so it is redrawn as house cards rather than lifted.
Exhibit 12.1 and Exhibit 12.5 are real PowerPoint tables and were read cell by cell.
Every curve is recovered exactly from Exhibit 12.4's two endpoints and Exhibit 12.5's cost
columns, and every headline number is asserted at import in `ch12_charts.py`.

THREE PUBLISHER DEFECTS, all in the accessibility descriptions, taught corrected:
  1. Exhibit 12.11's description puts MR = MC at "about 560 million pills".  It is 500 -
     their own notes say so twice and their own $3.50 price requires it.  A student who
     takes 560 mis-draws the profit rectangle AND the deadweight-loss triangle.
  2. Exhibit 12.8's description plots Q_H at "(560, $0.50)".  MR = $0.50 at Q = 550.
  3. Exhibit 12.7's description ends total revenue at "about $100 million" where P = $0,
     so TR = $0.  (That exhibit is not drawn here.)
And a fourth thing that is a TRAP rather than an error: Exhibit 12.5's marginal-revenue
column is the derivative evaluated at each row, NOT the difference of the total-revenue
column.  Differencing the table gives the midpoint value.  Said out loud on the table page.

NO COVER IMAGE, by instruction - so `collide.py` reports slide 1 as NEAR-BLANK and that is
EXPECTED.  NO EXHIBIT NUMBER IN ANY TITLE.  NO SLIDE-NUMBER REFERENCE anywhere.
STATIC, by rule.
"""
import os

from pptx import Presentation

import deckkit as D
from deckkit import (BLUE, GOLD, DGOLD, GREEN, RED, INK, INK2, GREY, RULE, WHITE,
                     TINT_BLUE, TINT_NEUTRAL, TINT_RED, TINT_GREEN, TINT_GOLD)

SRC = "/mnt/user-data/uploads/ECON003_26S/Slides/ECON003_Ch08_Trade_UCR_v2.pptx"
OUT = "ECON003_Ch12_Monopoly_UCR.pptx"
F = "figs/ch12_fig_%s.png"
P = "photos/ch12_photo_%s.png"
IC = "icons/%s.png"

LIMIT = 4.40
FIG_FLOOR = 4.42

prs = Presentation(SRC)
D.drop_slides_after(prs, 1)
s1 = prs.slides[0]
for _sh in list(s1.shapes):
    if _sh.shape_type == 13:
        _sh._element.getparent().remove(_sh._element)
D.retitle_title_slide(s1, ["Chapter 12", "Monopoly"],
                      ["ECON 003", "UC Riverside · Summer 2026"])
D.notes(s1, """Title.

Chapter 12, Monopoly. The last lecture of the course, and it is worth telling them that,
because the chapter closes an argument that started in Chapter 7.

Frame it as the removal of one assumption. Perfect competition needed many small sellers,
none big enough to move the price. Take away exactly that one condition - leave everything
else in place, including rational firms and voluntary exchange - and the invisible-hand
result breaks. Not because anybody cheats. Because a seller who can move the price has a
reason to sell less.

Say what is NOT in this lecture, once, at the start: price discrimination, section 12.6,
is in the reading and is not lectured. The recap page repeats it. Students reading along
will notice.

The running example is the book's: Claritin, an allergy drug under patent. Keep it - every
number in the deck is theirs, so a student revising from the textbook sees the same market.

No cover image on this slide, by instruction.""")


def S():
    return D.blank_slide(prs)


def figpage(title, lead, fig, kick, credit=None, lead_kind="formula", lead_size=13.5):
    s = S()
    D.title(s, title)
    yb = D.band(s, 1.12, lead, kind=lead_kind, size=lead_size) if lead else 1.02
    top = yb + 0.10
    D.picture_fit(s, F % fig, D.M, top, D.CONTENT_W, FIG_FLOOR - top)
    D.kicker(s, kick, y=4.52)
    if credit:
        D.credit(s, credit)
    return s


def _paras(text, width_in, size, line_pct=1.28):
    out = []
    for i, para in enumerate(text.split("\n\n")):
        if i:
            out.append("")
        out.extend(D.wrap(para, width_in, size) or [""])
    return out


def _fit_paras(text, width_in, height_in, start_pt, min_pt=9.0, line_pct=1.28):
    size = start_pt
    while size >= min_pt:
        lines = _paras(text, width_in, size)
        if D.text_h(len(lines), size, line_pct) <= height_in:
            return size, lines
        size -= 0.5
    return min_pt, _paras(text, width_in, min_pt)


def photopage(title, photo, question, body, kick, lead=None, portrait=False):
    s = S()
    D.title(s, title)
    y0 = 1.12
    if lead:
        y0 = D.band(s, y0, lead, kind="note", size=13) + 0.12
    if portrait:
        pw, px, qx, qw = 2.60, 0.60, 3.50, 5.90
    else:
        pw, px, qx, qw = 4.30, 0.60, 5.15, 4.25
    D.photo(s, P % photo, px, y0, pw, LIMIT - y0 - 0.02)
    qlines = D.wrap(question, qw, 15, bold=True)
    qh = D.text_h(len(qlines), 15, 1.15)
    D.textbox(s, qx, y0, qw, qh, "\n".join(qlines), size=15, bold=True,
              color=DGOLD, line_pct=1.15)
    by = y0 + qh + 0.16
    bh = LIMIT - by - 0.02
    bsize, blines = _fit_paras(body, qw, bh, 11.5)
    D.textbox(s, qx, by, qw, bh, "\n".join(blines), size=bsize, color=INK2, line_pct=1.28)
    D.kicker(s, kick, y=4.52)
    D.image_credit(s)
    return s


def examcheck(s, y, items):
    h = (LIMIT - y - 0.18 * (len(items) - 1)) / len(items)
    for stem, options, answer, why in items:
        D.rect(s, D.M, y, D.CONTENT_W, h, fill=WHITE, line=RULE)
        D.rect(s, D.M, y, 0.06, h, fill=BLUE)
        slines = D.wrap(stem, 5.30, 12, bold=True)
        sh = D.text_h(len(slines), 12, 1.15)
        D.textbox(s, D.M + 0.20, y + 0.09, 5.30, sh, "\n".join(slines),
                  size=12, bold=True, color=BLUE, line_pct=1.15)
        oy = y + 0.09 + sh + 0.10
        osize, _ = D.fit_size(options, 5.30, (y + h - 0.12) - oy, 11, 8.5, 1.22)
        olines = []
        for ln in options.split("\n"):
            olines.extend(D.wrap(ln, 5.30, osize) or [""])
        D.textbox(s, D.M + 0.20, oy, 5.30, (y + h - 0.12) - oy, "\n".join(olines),
                  size=osize, color=INK2, line_pct=1.22)
        D.rect(s, 6.20, y + 0.10, 3.10, h - 0.20, fill=TINT_GREEN, line=GREEN)
        alines = D.wrap(answer, 2.82, 11.5, bold=True)
        ah = D.text_h(len(alines), 11.5, 1.15)
        D.textbox(s, 6.34, y + 0.18, 2.82, ah, "\n".join(alines),
                  size=11.5, bold=True, color=GREEN, line_pct=1.15)
        wy = y + 0.18 + ah + 0.10
        wsize, wlines = D.fit_size(why, 2.82, (y + h - 0.14) - wy, 10, 8.0, 1.2)
        D.textbox(s, 6.34, wy, 2.82, (y + h - 0.14) - wy, "\n".join(wlines),
                  size=wsize, color=INK2, line_pct=1.2)
        y += h + 0.18


# ================================================================ 2. where we left off
s = S()
D.title(s, "Where We Left Off")
yb = D.band(s, 1.12, "Chapter 7 assumed every seller was a PRICE TAKER. Today we remove "
                     "that one condition and nothing else.", kind="formula", size=13.5)
D.cards3(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (GREEN, "WHAT CHAPTER 7 PROVED", "In PERFECT COMPETITION, P = MR = MC, firms earn "
     "ZERO ECONOMIC PROFIT in the long run, and SOCIAL SURPLUS is maximised. The "
     "INVISIBLE HAND, in one line.", IC % "shopping-cart"),
    (BLUE, "THE ASSUMPTION WE DROP", "Many sellers, none big enough to move the price. "
     "A MONOPOLY is one seller of a good with no close substitutes — and it is therefore "
     "a PRICE MAKER.", IC % "factory"),
    (RED, "WHAT BREAKS", "Not honesty and not effort. The monopolist maximises profit "
     "exactly as the competitive firm did — and produces LESS at a HIGHER price, with "
     "DEADWEIGHT LOSS.", IC % "price-tag"),
], body_size=11.5)
D.kicker(s, "MARKET POWER — the ability to set the price. It is the only thing that "
            "changes today, and it is enough to break the result.")
D.notes(s, """Opening. Two minutes.

The framing that makes this chapter land is that it is a controlled experiment. Chapter 7
needed a list of conditions: many sellers, identical products, free entry, perfect
information, price takers. Today we remove ONE of them. Everything else stays - the firm
still maximises profit, exchange is still voluntary, nobody is behaving badly.

Say that last part explicitly, because students moralise about monopoly and the economics
is more interesting than the moralising. The monopolist does not restrict output out of
greed in some sense competitive firms lack. It restricts output because, facing a
downward-sloping demand curve, selling one more unit forces the price down on every unit -
and that is a cost the competitive firm simply does not have.

Name the term MARKET POWER now and use it all hour. Monopoly is the extreme case of it;
almost every real firm has some.

If someone asks for real monopolies: local water and electricity distribution, a patented
drug during its patent, and older cases like Alcoa in bauxite and De Beers in diamonds.
Most famous "monopolies" people name are not - they are firms with a lot of market power
and some competitors, which the next chapter's material would handle.""")

# ============================================================================ 3. roadmap
s = S()
D.title(s, "One Seller, Six Moves")
yb = D.band(s, 1.12, "A MONOPOLIST picks a QUANTITY and lets DEMAND pick the price. "
                     "Everything today follows from that.", kind="formula", size=13.5)
D.strip5(s, yb + 0.34, [
    ("Price taker vs\nprice maker", IC % "price-tag"),
    ("Where market\npower comes from", IC % "factory"),
    ("Why MR is\nbelow price", IC % "coin-stack"),
    ("Choosing Q,\nthen reading P", IC % "research"),
    ("What it costs,\nand what policy can do", IC % "ballot-box"),
], label_size=10.5)
D.band(s, 3.34, "Sections 12.1 → 12.5 and 12.7:   MARKET POWER · BARRIERS TO ENTRY · "
                "MARGINAL REVENUE · MR = MC · DEADWEIGHT LOSS · REGULATION",
       kind="neutral", size=12)
D.kicker(s, "The competitive firm chose only a QUANTITY. So does the monopolist — the "
            "difference is that its choice moves the PRICE.")
D.notes(s, """Roadmap. Read the top band; it is the chapter's one sentence.

The observation worth making early, because it removes a persistent confusion: the
monopolist does not "choose a price" in the sense of choosing any price it likes. It
chooses a quantity, and the demand curve then tells it the highest price at which that
quantity will sell. Choosing the price and choosing the quantity are the same decision made
from opposite ends - it cannot choose both.

Section 12.6, price discrimination, is not in this lecture. Say so here, not at the end.

If you are short of time the compressible section is the last one, policy. The three that
are not: why marginal revenue lies below price, the MR = MC rule with the price read off
demand, and the surplus comparison. Those three are the chapter.""")

# =================================================================== 4. PART 1 divider
s = S()
D.divider(s, "PART 1", "One Seller")
D.notes(s, """Divider. Section 12.1.

Short section - one table. Its job is to set up the contrast the rest of the hour keeps
returning to, and to give them the vocabulary: price taker, price maker, market power,
monopoly.""")

# ============================================================= 5. Exhibit 12.1 as a table
s = S()
D.title(s, "Two Market Structures, Side by Side")
yb = D.band(s, 1.10, "MONOPOLY — one seller of a good or service with NO CLOSE "
                     "SUBSTITUTES.", kind="formula", size=14)
D.table(s, 0.60, yb + 0.14, 8.80, 4.38 - (yb + 0.14), [
    ["", "Perfect competition", "Monopoly"],
    ["Number of sellers", "Many", "One"],
    ["The product", "Identical across sellers", "No close substitutes"],
    ["Barriers to entry", "None — free entry and exit", "High"],
    ["Price", "PRICE TAKER: P = MR = MC", "PRICE MAKER: P > MR = MC"],
    ["Demand facing the firm", "Horizontal — perfectly elastic", "The whole market curve, "
                                                                "downward-sloping"],
    ["Long-run profit", "Zero economic profit", "Can stay positive indefinitely"],
    ["Social surplus", "Maximised", "Not maximised"],
], col_w=[2.20, 3.30, 3.30], first_col_fill=BLUE, header_size=10.5, body_size=10,
    align=["l", "l", "l"])
D.kicker(s, "Read the PRICE row: the competitive firm is HANDED P = MR = MC. The "
            "monopolist SETS P above MR = MC. Every other row follows.")
D.notes(s, """The comparison table. Do not read all eight rows aloud - read three.

READ THESE THREE:
  demand facing the firm - horizontal versus the whole market curve. This is the cause of
      everything else, and the next section draws it.
  price - P = MR = MC against P > MR = MC. That inequality is the single most examined
      line in the chapter. Say it as a sentence: the monopolist's price is ABOVE its
      marginal revenue, and its marginal revenue is what equals marginal cost.
  long-run profit - zero versus potentially positive forever. Students carry "profits get
      competed away" from Chapter 7 as if it were a law of nature. It is a consequence of
      FREE ENTRY, and free entry is exactly what a barrier to entry removes.

The one row worth a caveat rather than a claim: social surplus. The book adds that society
sometimes benefits from the research and development that the prospect of monopoly profit
funds. That is the chapter's own closing question - can a monopoly ever be good for
society - and the honest answer is that the patent system deliberately trades a period of
deadweight loss for an incentive to invent. Do not resolve it here; it comes back at the
end.

The point to leave them with is the kicker: the competitive firm is handed its price, the
monopolist chooses. That is the whole difference.""")

# =================================================================== 6. PART 2 divider
s = S()
D.divider(s, "PART 2", "Where Market Power\nComes From")
D.notes(s, """Divider. Section 12.2.

The question this section answers: if a monopolist earns positive profit forever, why does
nobody enter and compete it away? Something must be stopping them, and that something has
a name.

Make the link back explicitly: in Chapter 7, positive profit was a SIGNAL that pulled
firms in. Here the signal is just as loud and nobody can act on it.""")

# ======================================================== 7. barriers to entry
s = S()
D.title(s, "Four Reasons Nobody Else Can Enter")
yb = D.band(s, 1.12, "BARRIERS TO ENTRY — circumstances that prevent potential "
                     "competitors from entering the market.", kind="formula", size=14)
D.cards4(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (BLUE, "LEGAL", "The state grants exclusivity. A PATENT for an invention, a COPYRIGHT "
     "for a work, a licence for a route or a frequency.", IC % "balance-scale"),
    (RED, "KEY RESOURCE", "Own the input and you own the output. Alcoa and bauxite; De "
     "Beers and rough diamonds.", IC % "factory"),
    (GREEN, "ECONOMIES OF SCALE", "ATC still falling at the size of the whole market. A "
     "NATURAL MONOPOLY — the next page.", IC % "house"),
    (DGOLD, "NETWORK EXTERNALITIES", "The product is worth more because others use it. "
     "A rival with a better product still starts with nobody on it.", IC % "phone"
     if os.path.exists(IC % "phone") else IC % "coin-stack"),
], body_size=10.5)
D.kicker(s, "Chapter 7's ENTRY drove economic profit to zero. A BARRIER TO ENTRY is "
            "precisely what stops that mechanism running.")
D.notes(s, """The taxonomy. Four cards, four kinds of barrier, and the kicker ties them to
Chapter 7.

LEGAL. Patents and copyrights are the interesting ones because they are a monopoly created
ON PURPOSE. Say the trade-off out loud - a patent is society buying an invention with a
period of monopoly pricing - because it is the honest version and it sets up the closing
question of the chapter.

KEY RESOURCE. Alcoa and De Beers are the book's examples and they are historical rather
than current, which is worth admitting. Both have eroded, which is itself the useful
lesson: resource monopolies are less durable than they look.

ECONOMIES OF SCALE. Do not spend time here - it gets its own figure on the next page.

NETWORK EXTERNALITIES. The one students find most familiar and the one most often stated
badly. It is not that the product is better; it is that its VALUE to each user rises with
the number of other users, so a superior entrant still faces an empty network. Note the
connection back to Chapter 9 if you like: this is a positive externality between users of
the same product.

The kicker matters. Students remember "profits attract entry" as an iron law. It is not -
it is a consequence of free entry, and this whole section is a list of ways free entry
fails.""")

# ============================================================= 8. the Daraprim page
photopage(
    "A Barrier With a Price Tag On It",
    "pills",
    "One firm bought one old drug and raised the price from $13.50 a tablet to $750. "
    "Why could it?",
    "Nothing about the drug changed. Daraprim came off patent decades ago, so anyone may "
    "make it.\n\n"
    "The BARRIER TO ENTRY was regulatory delay: a new manufacturer must take a generic "
    "through FDA approval first, and that can take more than two years.\n\n"
    "For those two years the buyer had no close substitute — which is the definition of "
    "a MONOPOLY, arrived at without a patent, a key resource or a network.",
    "A barrier does not have to be permanent to confer MARKET POWER. It only has to last "
    "longer than the buyer can wait.")
D.notes(prs.slides[-1], """The vivid page, and it earns its place: $13.50 to $750 is the
number students remember from this chapter.

The facts, and stay inside them: Turing Pharmaceuticals acquired Daraprim - pyrimethamine,
used against toxoplasmosis - and raised the list price from about $13.50 to about $750 a
tablet. The drug had been off patent for decades. The company's market power came entirely
from the LAG before a generic competitor could clear FDA approval, which the book puts at
more than two years.

THE ECONOMICS, which is the reason it is here rather than the outrage. Every other barrier
on the previous page is structural: a patent, a resource, a cost curve, a network. This one
is pure timing. It shows that "barrier to entry" means anything that keeps a competitor out
LONG ENOUGH, and that the relevant length is measured against how long the buyer can wait -
which for a patient on this drug is not long at all.

Connect it to the previous page rather than telling it as a scandal story. Ask the room
which of the four categories it belongs to. The honest answer is that it is a fifth kind,
and that is precisely what makes it worth thirty seconds.

The photograph is the publisher's own; the 7 pt credit is the only attribution, by rule.
Their own "price hike" graphic is a chart, so it is not reproduced - the two numbers are on
the slide instead.""")

# ============================================================= 9. Exhibit 12.2
figpage("When One Firm Really Is Cheaper Than Two",
        "A NATURAL MONOPOLY has ECONOMIES OF SCALE over the whole market: ATC is still "
        "falling when one firm has served everybody.",
        "nat_mono",
        "Split the market and ATC rises $3.50 → $5.00. The BARRIER TO ENTRY here is the "
        "COST CURVE itself — no rule is needed.",
        credit="Worked example. Fixed cost $1.2m a month, marginal cost $2 a household")
D.notes(prs.slides[-1], """The natural monopoly figure. Two minutes, and it comes back in
the last section, so build it properly now.

The setup, and say the numbers: a regional water utility. The pipes, the treatment plant
and the reservoirs cost $1.2 million a month whether one household is connected or a
million. The marginal cost of serving one more household is about $2. So average total cost
is the fixed cost spread thinner and thinner - it falls all the way out.

Read the two points off the figure:
  one firm serving 800,000 households   ATC $3.50
  two firms serving 400,000 each        ATC $5.00 - the same water, more expensive

THE POINT TO MAKE EXPLICITLY: this is a barrier to entry that no legislature created. An
entrant would have to lay its own pipes down the same streets, start small, and therefore
have HIGHER average costs than the incumbent from day one. It would lose money. Nothing is
stopping it except arithmetic.

That is why utilities are usually either publicly owned or privately owned and
price-regulated - competition is not available, so something has to substitute for it. Flag
that we come back to it in the last section, because the same figure is where the
regulation page is drawn.

These numbers are ours, not the book's: their Exhibit 12.2 is drawn without a scale. Say
"a worked example" if anyone asks, and the credit line on the slide says so.""")

# ================================================================== 10. PART 3 divider
s = S()
D.divider(s, "PART 3", "Why Marginal Revenue\nFalls Below Price")
D.notes(s, """Divider. Section 12.3, and this is the analytical heart of the chapter.

Everything students find hard about monopoly is on the next three pages. If they leave
understanding only one thing today, it should be why marginal revenue is less than price
for a firm facing a downward-sloping demand curve.

Slow down here. This is not a section to compress.""")

# ============================================================= 11. Exhibit 12.3
figpage("The Curve the Firm Faces Is the Whole Market",
        "A PRICE TAKER faces a horizontal demand curve, so D = MR. A MONOPOLIST faces the "
        "MARKET demand curve, so it slopes DOWN.",
        "demand_pc_mono",
        "The MONOPOLIST IS THE INDUSTRY — it cannot sell more without cutting the price, "
        "and it cannot cut the price for only the last buyer.")
D.notes(prs.slides[-1], """The cause of everything. Say it as a sentence before you explain
the panels: THE MONOPOLIST IS THE INDUSTRY, so the curve facing the firm is the curve
facing the market.

Panel (a). A competitive wheat farmer can sell one more bushel, or a thousand more, at the
going price. Their output is a rounding error in the market, so demand facing THEM is flat,
and price equals marginal revenue - the extra bushel brings in exactly the price.

Panel (b). The monopolist selling 200 million pills at $5 can sell 400 million, but only by
dropping the price to $4. Not for the extra buyers. For everyone.

THE SENTENCE THAT DOES THE WORK, and it is on the kicker: it cannot cut the price for only
the last buyer. That single constraint is what makes marginal revenue fall below price, and
the next page turns it into a number.

The constraint worth naming while the panel is up: the monopolist is still LIMITED by
demand. It cannot charge any price it likes, because exchange is voluntary and buyers walk
away. Students often think a monopolist can name any number. It can name any point ON THE
DEMAND CURVE, which is a very different freedom.""")

# ============================================================= 12. Exhibit 12.5 table
s = S()
D.title(s, "Revenue and Cost at Every Output")
yb = D.band(s, 1.08, "MARGINAL REVENUE is the change in TOTAL REVENUE from one more "
                     "unit — and it is NOT the price.", kind="formula", size=13.5)
D.table(s, 0.60, yb + 0.12, 8.80, 4.38 - (yb + 0.12), [
    ["Q (m pills)", "Price", "Total revenue", "Marginal revenue", "Total cost",
     "Marginal cost", "ATC"],
    ["100", "$5.50", "$550", "$5.00", "$110", "$1.00", "$1.100"],
    ["200", "$5.00", "$1,000", "$4.00", "$210", "$1.00", "$1.050"],
    ["300", "$4.50", "$1,350", "$3.00", "$310", "$1.00", "$1.033"],
    ["400", "$4.00", "$1,600", "$2.00", "$410", "$1.00", "$1.025"],
    ["500", "$3.50", "$1,750", "$1.00", "$510", "$1.00", "$1.020"],
    ["600", "$3.00", "$1,800", "$0.00", "$610", "$1.00", "$1.017"],
    ["700", "$2.50", "$1,750", "−$1.00", "$710", "$1.00", "$1.014"],
], col_w=[1.24, 1.02, 1.42, 1.62, 1.14, 1.30, 1.06], first_col_fill=BLUE,
    header_size=9.5, body_size=9.5,
    align=["ctr", "ctr", "r", "r", "r", "ctr", "r"])
D.kicker(s, "At every row MARGINAL REVENUE is BELOW price, and by Q = 600 it is zero: "
            "selling more would REDUCE total revenue.")
D.notes(s, """The book's own table. Do not read it across - read it down, one column at a
time, and stop on three things.

FIRST, the marginal revenue column against the price column. At 200 million pills the price
is $5.00 and marginal revenue is $4.00. At 500 it is $3.50 against $1.00. MR is below P at
every single row, and the gap widens. That is the previous page, in numbers.

SECOND, total revenue. It rises to $1,800 million at 600 and then FALLS. The reason is on
the same row: marginal revenue hits zero at 600. Past that point the price effect swamps the
quantity effect and selling more brings in less money. So no monopolist ever operates
where MR is negative - the bottom rows of this table are choices no firm would make.

THIRD, marginal cost is a constant $1.00 and the fixed cost is $10 million. That is realistic
for a drug: the research is spent, and the next pill costs pennies. It is also why ATC falls
steadily down the column and ends up very close to $1.

A TRAP WORTH NAMING OUT LOUD, because it is exactly the skill an exam asks for. The marginal
revenue column here is calculated AT each quantity, not by differencing the total-revenue
column across the 100-unit steps. If you difference - (1,000 minus 550) over 100 - you get
$4.50, and the table's row for 200 says $4.00. Both are correct; the difference gives you the
value at the MIDPOINT of the step, 150. Tell them which one the question wants: if a table has
gaps of 100 units and asks for marginal revenue "between" two rows, difference it. If it asks
for marginal revenue AT a quantity, read the column.

Flag the row for 500 - it is where the next two pages land.""")

# ============================================================= 13. Exhibit 12.6
figpage("Cut the Price and Two Things Happen at Once",
        "QUANTITY EFFECT: more units sold. PRICE EFFECT: every unit you were already "
        "selling now earns less.",
        "qty_price_effect",
        "MARGINAL REVENUE = ($800 − $200) ÷ 200 = $3 a pill — below the $4 price, because "
        "the PRICE EFFECT is subtracted from it.",
        credit="Worked on the book's own $5 → $4 example, Acemoglu, Laibson & List, ch. 12")
D.notes(prs.slides[-1], """The mechanism page. This is the one to do slowly and the one
students quote back.

The story, in the book's own numbers. The firm is selling 200 million pills at $5. It wants
to sell more, so it cuts the price to $4 and sales rise to 400 million.

  THE GOOD NEWS - the QUANTITY EFFECT. 200 million extra pills at $4 each: revenue up $800
  million. That is the green box.

  THE BAD NEWS - the PRICE EFFECT. The 200 million pills it was ALREADY selling now go for
  $4 instead of $5. Revenue down $200 million. That is the pink box.

  NET: up $600 million, for 200 million extra pills. So marginal revenue is $600 divided by
  200, which is $3 a pill - and the price is $4.

SAY THE CONCLUSION IN THE FORM THE EXAM USES: for any firm facing a downward-sloping demand
curve, marginal revenue is less than price, because the price effect is subtracted from the
quantity effect. For a price taker there is no price effect, which is why P = MR there.

The follow-up worth asking aloud: what happens if the price effect is BIGGER than the
quantity effect? Then marginal revenue is negative and the price cut loses money. That is
the bottom of the table on the previous page, and it is why total revenue turns down at 600
million pills.

If you want one line for them to write down, it is: MR = price minus what you gave up on
the units you were already selling.""")

# ================================================================== 14. PART 4 divider
s = S()
D.divider(s, "PART 4", "Choosing the Quantity,\nThen Reading the Price")
D.notes(s, """Divider. Section 12.4 - the rule, and the graph task.

Tell them this is the most examined page-pair in the chapter. Reading a monopoly diagram is
a skill with a fixed procedure, and the procedure is three steps in a fixed order.""")

# ================================================== 15. Exhibits 12.8 and 12.9
figpage("Three Steps, and the Order Matters",
        "STEP 1 find Q where MR = MC. STEP 2 go UP to the DEMAND curve. STEP 3 read the "
        "PRICE off the vertical axis.",
        "mr_mc",
        "MR = MC at 500 million pills, and DEMAND sets the price at $3.50. The rule is "
        "P > MR = MC.",
        credit="Market drawn to Acemoglu, Laibson & List, Microeconomics 3e, ch. 12")
D.notes(prs.slides[-1], """The procedure. Say the three steps in order, then say the error.

STEP 1. Marginal revenue equals marginal cost at 500 million pills. The logic is identical
to Chapter 7's: while MR exceeds MC the next unit adds more than it costs, so make it; once
MC exceeds MR, stop. Nothing about profit maximisation changed. What changed is that MR is
no longer the price.

STEP 2. Go straight UP from 500 to the DEMAND curve, not to the MR curve. Demand is the
schedule of what buyers will actually pay.

STEP 3. Read across to the axis: $3.50.

THE ERROR, and it costs marks every single term: reading the price off the MR curve, or off
the MC curve, giving $1.00. The $1 is a COST, not a price. The figure flags it. Say it out
loud as well - "the price is never read off marginal revenue" - and then say why: MR is
bookkeeping about the firm's revenue, demand is what a buyer will hand over.

The rule to leave on the board is the kicker: P > MR = MC. Contrast it with the competitive
firm's P = MR = MC and note that the only thing that changed is the first equals sign
becoming a greater-than.

One number that differs from the textbook's own alt text, if anyone is reading it: their
description of this figure puts the marginal-revenue reading of $0.50 at 560 million pills.
It is 550. The intersection they matter about, MR = MC, is at 500 - which their instructor
notes and their own $3.50 price both confirm.""")

# ============================================================= 16. Exhibit 12.10
figpage("Profit Is a Rectangle, and Nothing Erodes It",
        "PROFIT = (P − ATC) × Q, exactly as in Chapter 7. What is new is that no ENTRY "
        "arrives to compete it away.",
        "profit_rect",
        "(3.50 − 1.02) × 500 = $1,240 million a year — and it can persist, because the "
        "BARRIER TO ENTRY holds.",
        credit="Cost data from Acemoglu, Laibson & List, Microeconomics 3e, ch. 12")
D.notes(prs.slides[-1], """The profit page. The formula is old; the conclusion is new.

The arithmetic, and it is all off the table two pages back:
  price at 500 million pills   $3.50
  average total cost there     $1.02  (total cost $510m over 500m pills)
  profit                       (3.50 minus 1.02) times 500 = $1,240 million

SAY THE FORMULA IN THE FORM THEY LEARNED IT IN CHAPTER 7: profit equals price minus average
total cost, times quantity. Nothing about that changed. Students expect monopoly to need new
machinery and it does not - only the demand curve changed.

WHY ATC IS SO CLOSE TO MC HERE, because the figure makes it look like a drawing error. The
fixed cost is $10 million and it is spread over 500 million pills, which is two cents each.
That is the economics of pharmaceuticals: the research is enormous and sunk, and the
marginal pill is nearly free. Say it - otherwise the flat green curve looks like a mistake.

THE CONCLUSION THAT IS ACTUALLY NEW, and it is the reason this page exists at all: ask them
what happens next. In Chapter 7, $1,240 million of economic profit would pull in entrants,
supply would rise, price would fall, and profit would go to zero. Here nothing happens.
Claritin is under patent. The barrier holds, so the rectangle stays.

That is the sentence to leave them with: in perfect competition, profit is a signal. In
monopoly, it is a destination.""")

# ============================================================== 17. Exam Check
s = S()
D.title(s, "Exam Check: Read the Monopoly Diagram")
examcheck(s, 1.12, [
    ("A monopolist's MR = MC at Q = 40. Demand at Q = 40 is $18; MC is $6 and ATC is "
     "$11. What price does it charge, and what is profit?",
     "A.  P = $6, profit = $200\n"
     "B.  P = $11, profit = $0\n"
     "C.  P = $18, profit = $280\n"
     "D.  P = $18, profit = $480",
     "C",
     "Price is read off DEMAND at the MR = MC quantity: $18. Profit is (P − ATC) × Q = "
     "(18 − 11) × 40 = $280. Answer D uses MC instead of ATC."),
    ("Compared with a competitive industry facing the same costs and demand, a monopolist "
     "produces ___ and charges ___ .",
     "A.  more; less\n"
     "B.  less; more\n"
     "C.  the same; more\n"
     "D.  less; the same",
     "B",
     "Less output at a higher price — because it sets P above MR = MC, while competition "
     "drives P down to MC. That gap is the DEADWEIGHT LOSS on the next page."),
])
D.notes(s, """Two worked items. Read the stem, pause a beat, read the answer panel - do not
leave silence on a recording.

ITEM 1 is the graph task in words, and it is the single most common monopoly question there
is. Two traps live in it:
  - reading the price off MC, giving $6. That is answer A and it is the same error the
    previous figure flagged.
  - computing profit with MC rather than ATC, giving (18 − 6) × 40 = $480. That is answer
    D, and it is the more sophisticated mistake - the student has the right formula shape
    and the wrong cost concept. Say the rule: profit uses AVERAGE cost, because you need
    the cost of ALL the units, not the last one.
Answer B is what you get by pricing at ATC, which is the regulated outcome, not the
monopolist's choice - and it comes back in the last section.

ITEM 2 is the qualitative version and it is worth doing because students who can compute
sometimes cannot state. Less output, higher price, every time, for the same costs and the
same demand. If they can say that sentence they can eliminate three options on any
comparison question.""")

# ================================================================== 18. PART 5 divider
s = S()
D.divider(s, "PART 5", "What Monopoly Costs\nSociety")
D.notes(s, """Divider. Section 12.5, the payoff of the whole course.

Frame it against Chapter 7 explicitly. That chapter's result was that a competitive market
maximises social surplus. This section runs the same market as a monopoly and measures what
is lost - using the same triangles they have used since Chapter 7.

Two slides, and the second one is the exam-facing comparison.""")

# ============================================================= 19. Exhibit 12.11
figpage("The Same Market, Run Twice",
        "Identical demand, identical costs. Only the number of sellers changes — and "
        "SOCIAL SURPLUS falls.",
        "pc_vs_mono",
        "CS falls $2,500m → $625m. $1,250m is TRANSFERRED to the monopolist; $625m is "
        "DEADWEIGHT LOSS and nobody receives it.",
        credit="Market drawn to Acemoglu, Laibson & List, Microeconomics 3e, ch. 12")
D.notes(prs.slides[-1], """The chapter's payoff figure. Give it time.

Panel (a): competition. Price is driven to marginal cost, $1, and 1,000 million pills are
sold. Consumer surplus is the whole triangle under demand and above $1: $2,500 million.
Producer surplus is zero, because price equals marginal cost.

Panel (b): monopoly. 500 million pills at $3.50. Consumer surplus shrinks to $625 million.
The monopolist takes $1,250 million as producer surplus. And a triangle of $625 million
belongs to nobody.

THE ARITHMETIC THAT MAKES IT CLICK, and it is worth doing on camera: consumers lost $2,500
minus $625, which is $1,875 million. The monopolist gained $1,250 million. Those do not
match, and the difference is $625 million - exactly the deadweight loss. EVERY DOLLAR
CONSUMERS LOSE IS EITHER TRANSFERRED OR DESTROYED, and the triangle is the destroyed part.
Say that sentence; it is the whole of welfare analysis in one line.

WHAT THE TRIANGLE IS MADE OF, concretely: the pills between 500 and 1,000 million. Take the
600 millionth pill. A patient values it at about $3, it costs $1 to make, and it is not
made. Nobody is better off for that. Those are the trades the monopolist's price prevents.

Note out loud that the mechanism is identical to the tax wedge in Chapter 10 - a gap between
what buyers pay and what the last unit costs, and a triangle where the trades used to be.
Here nothing is being collected; the gap is the monopolist's markup.

One correction if a student is reading the textbook's own figure description: it places the
MR = MC intersection at "about 560 million pills". It is 500 - the $3.50 price on their own
figure requires it. At 560 the price would be $3.20.""")

# ============================================================== 20. the comparison table
s = S()
D.title(s, "Competition and Monopoly, Number by Number")
yb = D.band(s, 1.10, "One change causes every row: the seller SETS P > MR = MC instead "
                     "of being handed it.", kind="formula", size=13.5)
D.table(s, 0.60, yb + 0.16, 8.80, 4.38 - (yb + 0.16), [
    ["", "Perfect competition", "Monopoly", "Change"],
    ["Quantity", "1,000m pills", "500m pills", "Halved"],
    ["Price", "$1.00", "$3.50", "3.5× higher"],
    ["Consumer surplus", "$2,500m", "$625m", "Falls $1,875m"],
    ["Producer surplus", "$0", "$1,250m", "Rises $1,250m"],
    ["Social surplus", "$2,500m", "$1,875m", "Falls $625m"],
    ["Deadweight loss", "$0", "$625m", "The whole fall"],
], col_w=[2.30, 2.30, 2.10, 2.10], first_col_fill=BLUE, header_size=10.5, body_size=10,
    align=["l", "ctr", "ctr", "ctr"])
D.kicker(s, "And a MONOPOLIST HAS NO SUPPLY CURVE: a supply curve answers “at price "
            "P, how much?” — but a PRICE MAKER is never handed a price.")
D.notes(s, """The comparison as a table, because this is the form the exam takes.

Do not read every cell. Read the last column, which is where the argument is, and stop on
two rows.

CONSUMER SURPLUS falls by $1,875 million; PRODUCER SURPLUS rises by $1,250 million. The
difference is the deadweight loss. Students who can do that subtraction can answer almost
any welfare-comparison question, including the ones that give them different numbers.

The row that catches people out is producer surplus. It RISES - monopoly is good for the
monopolist, which is not a paradox and is exactly why firms seek market power. What falls is
the TOTAL. If a question asks who is worse off, the answer is consumers and society, not
the firm.

THE KICKER IS A REAL RESULT and it deserves its ten seconds. Chapter 7 spent pages building
a firm's supply curve out of its marginal cost curve. A monopolist has no supply curve at
all. A supply curve answers the question "if the price were P, how much would you produce?"
- and that question cannot be asked of a firm that chooses the price. Given a demand curve
the monopolist picks one point; change the demand curve and it picks a different one, with
no stable relationship between price and quantity supplied. Students find this genuinely
surprising and it is a good check on whether they understand what a price maker is.

If a student asks whether monopoly is therefore always bad: the honest answer is that this
diagram measures one period with the product already invented, and that the patent case
deliberately accepts this loss to buy the invention in the first place. That is the
chapter's own closing question, and the next section is what policy does about the part
that is not a patent.""")

# ================================================================== 21. PART 6 divider
s = S()
D.divider(s, "PART 6", "What Policy Can Do\nAbout It")
D.notes(s, """Divider. Section 12.7, and the last two content pages of the course.

The question: we have a market that produces too little at too high a price and no
mechanism inside the market that fixes it. What can be done from outside?

Two answers. Where competition is possible, restore it - antitrust, and opening the border.
Where competition is impossible because the industry is a natural monopoly, regulate the
price instead. The second one gets the figure, because it is the one with a graph task
attached.""")

# ============================================================= 22. regulating a natural monopoly
figpage("Regulating a Natural Monopoly: Two Prices the Law Can Set",
        "P = MC is EFFICIENT but loses money, because ATC lies ABOVE MC. P = ATC is the "
        "FAIR-RETURN price: zero economic profit.",
        "nat_mono_reg",
        "Unregulated $6 × 400. FAIR RETURN $4 × 600, zero profit. EFFICIENT $2 × 800 — "
        "and a $1,200 loss the taxpayer would have to cover.",
        credit="Worked example — the natural monopoly of the earlier figure, with demand added")
D.notes(prs.slides[-1], """The regulation figure, and it is the graph task the previous
final examined. Give it two minutes.

The same water utility as earlier, with demand added. Three prices, and the table to read
off:

  UNREGULATED   MR = MC gives 400 thousand households at $6. ATC is $5, so profit is
                $400 thousand a month. The monopoly outcome.
  FAIR RETURN   force P = ATC: 600 thousand households at $4. Price equals average cost,
                so economic profit is exactly zero. The firm survives without a subsidy.
  EFFICIENT     force P = MC: 800 thousand households at $2. This is the socially optimal
                quantity - the last household values water at what it costs to serve them.
                But ATC there is $3.50, so the firm loses $1.50 on every household, which
                is $1,200 thousand a month - exactly its fixed cost.

THE POINT OF THE WHOLE PAGE, and say it plainly: for a natural monopoly, the efficient
price is not sustainable. ATC lies above MC at every quantity because average cost is still
carrying the fixed cost. So a regulator who insists on P = MC must also write a cheque, and
the money for that cheque comes from taxes, which have their own deadweight loss - which is
Chapter 10, and worth naming as a callback.

Fair-return pricing is the compromise actually used: the firm covers its costs, earns a
normal return and nothing more, and society gets 600 rather than 400. Deadweight loss falls
from $800 thousand to $200 thousand a month. It does not reach zero. Regulation improves
this market; it does not perfect it, and that is the honest version.

A NOTE ON WHY WE DRAW OUR OWN FIGURE HERE. The textbook illustrates price regulation on the
Claritin diagram, where marginal cost and average total cost are both $1. On that figure the
fair-return price and the efficient price are the same number, so the distinction the
section is about cannot be seen. Their own notes say "if ATC is greater than $1..." - which
is the case this figure actually draws. Use ours; do not name them.""")

# ============================================================== 23. antitrust
s = S()
D.title(s, "Where Competition Is Possible, Restore It")
yb = D.band(s, 1.12, "ANTITRUST POLICY — government action against anti-competitive "
                     "pricing, restricted output and the deadweight loss they cause.",
            kind="formula", size=13.5)
D.cards3(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (BLUE, "THE SHERMAN ACT, 1890", "Prohibits agreements and actions in RESTRAINT OF "
     "TRADE, and monopolising a market. Violations are felonies — fines, and prison "
     "sentences.", IC % "balance-scale"),
    (DGOLD, "WHAT A REMEDY LOOKS LIKE", "Microsoft was found to have monopolised by "
     "bundling its browser with Windows. It was NOT broken up: it had to change its "
     "marketing and let rival browsers work with Windows.", IC % "research"),
    (GREEN, "OPEN THE BORDER", "A domestic monopolist with no domestic rivals may have "
     "plenty of foreign ones. Removing a TRADE BARRIER is competition policy by another "
     "name — Chapter 8's argument, applied.", IC % "shopping-cart"),
], body_size=11)
D.kicker(s, "Antitrust attacks the BARRIER TO ENTRY. Price regulation accepts the "
            "monopoly and attacks the PRICE. Which one fits depends on whether "
            "competition is possible at all.")
D.notes(s, """The policy card page, and the last content slide of the course. Two minutes.

THE SHERMAN ACT is the one date worth knowing: 1890. What matters more than the date is
what it prohibits - restraint of trade, and monopolising - and that it carries criminal
penalties, which surprises students who assume this is a matter of fines.

MICROSOFT is the book's worked case and the useful part is the REMEDY, not the verdict. The
company was found to have monopolised, and it was NOT split in two. It had to change
conduct: stop the bundling practices and make it easier for rival browsers to work with
Windows. That is what most antitrust remedies look like - behavioural, not structural. Say
so, because the popular image of antitrust is trust-busting and break-ups, and those are
rare.

OPEN THE BORDER is worth the callback to Chapter 8. A firm can be the only domestic producer
and face fierce competition from imports. Protection creates market power; removing it
removes market power. It is the cheapest competition policy there is and it does not require
a court.

THE KICKER IS THE SUMMARY OF THE SECTION and it is the right note to end the argument on:
antitrust goes after the barrier, price regulation accepts the monopoly and goes after the
price. You choose between them by asking whether competition is even possible. For a water
network it is not, so you regulate. For a software market it is, so you litigate.

If you want to close the chapter's own question - can a monopoly ever be good for society -
this is the moment. The honest answer: the deadweight loss on the earlier figure is real and
measurable, and the case for tolerating it rests on innovation that would not otherwise
happen. Patents are society making that bargain deliberately, with an expiry date attached.
That is a defensible trade, not a free lunch, and saying so is better than either
cheerleading or condemning.""")

# ================================================================== 24. the full picture
s = S()
D.recap_table(s, "Chapter 12: The Full Picture", [
    ["One seller",
     "A price maker faces the whole market demand curve, so it must cut price to sell more.",
     "MONOPOLY, MARKET POWER, PRICE MAKER",
     "§12.1 · the two-structure table"],
    ["Why nobody enters",
     "Legal grant, a key resource, economies of scale, or a network — entry is blocked.",
     "BARRIERS TO ENTRY, NATURAL MONOPOLY",
     "§12.2 · Daraprim, the utility"],
    ["Marginal revenue",
     "Quantity effect minus price effect, so MR is below price at every quantity.",
     "MARGINAL REVENUE, QUANTITY / PRICE EFFECT",
     "§12.3 · the $5 → $4 cut"],
    ["The rule",
     "Find Q where MR = MC, go up to demand, read the price. P > MR = MC.",
     "PROFIT MAXIMISATION",
     "§12.4 · 500m pills at $3.50"],
    ["What it costs",
     "Less output, higher price: surplus transferred to the firm, and a triangle destroyed.",
     "DEADWEIGHT LOSS, TRANSFER",
     "§12.5 · $1,250m moved, $625m lost"],
    ["What policy does",
     "Attack the barrier with antitrust, or accept the monopoly and regulate the price.",
     "ANTITRUST, FAIR-RETURN PRICE",
     "§12.7 · P = ATC vs P = MC"],
], "Not lectured, and in your reading: §12.6, price discrimination — first, second and "
   "third degree, and what perfect price discrimination does to consumer surplus.")
D.notes(s, """Recap. Read the row labels, not the cells.

SAY THE CLOSING LINE AND DO NOT SKIP IT. Section 12.6 is in the reading and was not
lectured. Tell them now rather than letting a homework question tell them.

If you want to give them one sentence about what 12.6 says, so the omission is not a
mystery: a monopolist that can charge different buyers different prices captures more of
the surplus, and in the extreme case of PERFECT price discrimination it captures all of it -
and, counter-intuitively, produces the EFFICIENT quantity, so the deadweight loss disappears
even though consumers get nothing. That is the paradox the section is built around. One
sentence is enough.

A NOTE FOR WHOEVER PREPARES THE FINAL, not for delivery. The Chapter 12 question bank is
full of price-discrimination items and this lecture does not cover the material. Those items
have to be excluded from the draw. This matters more than the Chapter 10 equivalent, because
the previous offering of this course taught price discrimination as a whole chapter and
examined it heavily - anyone reusing that item pool will pull them in by default.

Then close the course. This chapter is the last assumption of Chapter 7 being removed, and
the deadweight-loss triangle they met under a price control in Chapter 7, then under a tax
in Chapter 10, is the same triangle here with no government involved at all. That is the
through-line of the term and it is worth saying out loud on the last recording.""")

# ==================================================================== 25. key takeaways
s = S()
D.takeaways_page(s, "Chapter 12: Monopoly", [
    "MARKET POWER — a monopolist is the industry, so it faces the whole downward-sloping "
    "demand curve and is a PRICE MAKER.",
    "BARRIERS TO ENTRY — legal grant, key resource, economies of scale or network effects "
    "are what stop entry competing profit away.",
    "MARGINAL REVENUE is below price, because the QUANTITY EFFECT is offset by a PRICE "
    "EFFECT on every unit already being sold.",
    "THE RULE IS P > MR = MC — choose Q where MR = MC, then read the price off DEMAND, "
    "never off MR or MC.",
    "DEADWEIGHT LOSS — less output at a higher price: some surplus is TRANSFERRED to the "
    "firm and some is destroyed, and policy targets one or the other.",
])
D.notes(s, """Key takeaways, and the last slide of the course. Five lines, each opening with
its term. Read them; do not paraphrase.

The one-sentence summary if you want to end on it: a monopolist does nothing a competitive
firm does not do — it sets marginal revenue equal to marginal cost — and produces the wrong
quantity anyway, because for a price maker marginal revenue is not the price.

Then say the through-line of the term, because this is the final recording. The
deadweight-loss triangle appeared three times this course: under a price control in Chapter
7, under a tax in Chapter 10, and here under nothing but one seller's market power. Same
triangle, same meaning every time — trades that both sides wanted, that did not happen.

Housekeeping to say at the end rather than in the middle: the final is cumulative, the
question bank is drawn from every chapter, and section 12.6 is reading, not lectured.""")

prs.save(OUT)
print("wrote", OUT, len(prs.slides._sldIdLst), "slides")
