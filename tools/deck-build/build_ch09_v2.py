#!/usr/bin/env python3
"""Build ECON003_Ch09_..._UCR_v2.pptx - 43 slides, static.

v2 OF THE CHAPTER 9 DECK, and the change is a WRITING RULE, not a structural one.
Every figure, table, photograph, speaker note and slide order is v1's. What changed is
the band-and-kicker layer: about thirty sentences.

WHY. He rewrote the same layer of Chapter 8 by hand across eighteen slides, and the
pattern was consistent: where v1 described the idea in plain English, he named the
economic term in CAPS and stated the operative number. His reason, in his words - the
terminology "helps me stick to professional economic language rather than wind off to
simple language."

THAT IS THE POINT AND IT IS WORTH RESTATING: THE SLIDE FACE IS THE LECTURER'S DISCIPLINE
DEVICE, not only a student reminder. The speaker notes are not in his eyeline while he
teaches; the slide is. So a term on the slide that is ALSO in the notes is not redundant
- the redundancy is the mechanism. Do not "tidy" it away.

WHAT v2 CHANGES, concretely:

  1. Every band and kicker names its term in CAPS - MARGINAL SOCIAL COST, MARGINAL
     EXTERNAL COST, PIGOUVIAN TAX, TAX INCIDENCE, DEADWEIGHT LOSS, COASE THEOREM,
     PROPERTY RIGHTS, TRANSACTION COSTS, FREE RIDING, NONEXCLUDABILITY, PROCYCLICAL,
     MARGINAL ABATEMENT COST, TRAGEDY OF THE COMMONS, OPEN ACCESS.
  2. Lines that described the slide's own furniture are gone. v1's "the gap between the
     second card and the first", "the market handles the top-left box" and "the wedge
     decides which direction" were captions for captions; they now carry the term.
  3. Two terms the deck taught without ever naming are now named: MARKET FAILURE (the
     roadmap kicker) and TAX INCIDENCE (the Pigouvian tax page). MARKET FAILURE is the
     umbrella for all five sections and the publisher's deck never states it.
  4. The five takeaway bullets each open with their term.
  5. EVERY SLIDE-NUMBER REFERENCE IS GONE, from the slide faces and from the notes -
     34 of them. Notes now point at slide TITLES, which survive his renumbering. Four
     references had already gone stale from his deleting one slide. References to the
     Mateer & Coppock deck's own slide numbers stay, because that file does not change.
  6. Exam Check 3 is deleted, per his edit of v1. Exam Checks 1 and 2 stay - he kept
     them. His cut was precise rather than categorical: Exam Check 3 sat directly after
     the four-types table and asked questions that table already answered.

WHAT v2 DOES NOT CHANGE. No figure is redrawn, no table is retouched, no photograph
moves, no note is rewritten except to drop a slide number, and the slide order is his.
The one page I would still question is the charity figures - the giving series is
selected years only and the publisher calls its own values approximate - but it is his
call, so it stays, and its band now names PRIVATE PROVISION OF A PUBLIC GOOD.

SOURCE DECKS, unchanged from v1.

  1. `Slides/Pearson/Acemoglu_Micro_3e_Ch09 (1).pptx` - the publisher's own deck. All 16
     exhibits accounted for, six publisher photographs at feature size, and four defects
     in their material found and taught corrected - one of them in the answer key, where
     their end-of-chapter problem states a net gain of $1 million and 1.1bn - 1.0bn is
     $100 MILLION. Section 9 of the ground rules, building with no publisher deck, is NOT
     in force for this chapter.

  2. `Slides/Pearson/PRINECOMI4_lecppt_ch07.pptx` - Mateer & Coppock, *Principles of
     Microeconomics*, Chapter 7. Supplied on instruction as a reference for material that
     helps students with EXAM questions. Eight imports, each flagged in the notes of the
     page that uses it: the cold open; the internal / external / social cost ladder; Exam
     Check 1; THE COASE 2x2 run under BOTH assignments of the property right - the most
     valuable of the eight, because the publisher runs the bargain one way only and the
     invariance IS the theorem; cap and trade; Exam Check 2; the richer example set in the
     four-types table; the grazing commons with numbers; and the property-rights incentive
     contrast. Nothing on any slide face names either publisher.

NO TITLE IMAGE, by instruction. Slide 1 has no picture shape at all, so adding art later
needs `insert_title_art.py`, not a blob swap - and `collide.py` reports slide 1 as
NEAR-BLANK, which is expected.

NO EXHIBIT NUMBER IN ANY TITLE. He deleted "Exhibit 8.1 - " from a Chapter 8 title by
hand; provenance belongs in the 7 pt credit line, which is where every one of these sits.

STATIC, by rule. Run the animation pass only after his edits settle, from
`ch07_animate.py`.

Figures: `ch09_charts.py`, 13 built and 13 placed, every headline number asserted at
import.
"""
import os

from pptx import Presentation

import deckkit as D
from deckkit import (BLUE, GOLD, DGOLD, GREEN, RED, INK, INK2, GREY, RULE, WHITE,
                     TINT_BLUE, TINT_NEUTRAL, TINT_RED, TINT_GREEN, TINT_GOLD)

SRC = "/mnt/user-data/uploads/ECON003_26S/Slides/ECON003_Ch08_Trade_UCR_v2.pptx"
OUT = "ECON003_Ch09_Externalities_and_Public_Goods_UCR_v2.pptx"
F = "figs/ch09_fig_%s.png"
P = "photos/ch09_photo_%s.png"
IC = "icons/%s.png"

LIMIT = 4.40          # the kicker rule's y on a card page
FIG_FLOOR = 4.42      # figure pages carry no card row

prs = Presentation(SRC)
D.drop_slides_after(prs, 1)
s1 = prs.slides[0]
for _sh in list(s1.shapes):
    if _sh.shape_type == 13:                      # no cover image, by instruction
        _sh._element.getparent().remove(_sh._element)
D.retitle_title_slide(s1, ["Chapter 9", "Externalities and Public Goods"],
                      ["ECON 003", "UC Riverside · Summer 2026"])
D.notes(s1, """Title.

Chapter 9, Externalities and Public Goods. The chapter that takes the invisible hand
apart.

Open with the debt this chapter is collecting. Chapter 7 proved that a competitive market
maximises total surplus. Chapter 8 assumed every cost of a transaction lands on the two
people making it. Today that assumption fails, and when it fails the price stops carrying
all the information - so the market still clears, and it clears at the wrong quantity.

Say out loud that this is the first chapter in which the market is wrong and the
government can help. Students have spent seven chapters learning the opposite, and some
of them will hear this as a contradiction rather than a boundary condition.

No cover image on this slide, by instruction.""")


def S():
    return D.blank_slide(prs)


def figpage(title, lead, fig, kick, credit=None, lead_kind="formula", lead_size=13.5):
    """Title, a ONE-LINE lead band, the figure, a kicker.

    A lead band that wraps to a second line costs the figure 0.28 in of height on a
    height-bound page, so every lead here is written to fit one line at 13.5 pt.
    """
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
    """Wrap a multi-paragraph string, keeping blank lines between paragraphs."""
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
    """Half-slide feature photograph, the posed question set large beside it, body under.

    The question is its OWN text box at 15 pt and the body its own at 11.5 pt. Keeping
    them apart matters twice over: `fitcheck` measures a mixed-size box at its largest
    size and over-reports wildly, and the animation pass in ground-rules S5 identifies a
    posed-question-beside-a-photograph BY POINT SIZE.

    The portrait picture gets a narrow full-height column. Its source is only 492 x 695,
    so it lands just under the usual quarter-of-the-slide floor - placed as large as it
    goes rather than cropped, which is what the ground rules ask for in that case.
    """
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
    """A worked multiple-choice item: the stem, the options, the answer, the reason.

    These are NOT pause-and-think prompts - the Chapter 8 checkpoints were cut by hand
    and stay cut.  The answer and the reasoning are ON the slide, which makes the page a
    worked table and earns it its place under the density rule.
    """
    h = (LIMIT - y - 0.18 * (len(items) - 1)) / len(items)
    for stem, options, answer, why in items:
        D.rect(s, D.M, y, D.CONTENT_W, h, fill=WHITE, line=RULE)
        D.rect(s, D.M, y, 0.06, h, fill=BLUE)
        # every inner box is sized from its own WRAPPED height, never a guessed constant
        slines = D.wrap(stem, 5.30, 12, bold=True)
        sh = D.text_h(len(slines), 12, 1.15)
        D.textbox(s, D.M + 0.20, y + 0.09, 5.30, sh, "\n".join(slines),
                  size=12, bold=True, color=BLUE, line_pct=1.15)
        oy = y + 0.09 + sh + 0.10
        osize, olines = D.fit_size(options, 5.30, (y + h - 0.12) - oy, 11, 8.5, 1.22)
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


# ============================================================ 2. the cold open
s = S()
D.title(s, "A Question to Start With")
yb = D.defbox(s, 1.12, "What is the optimal level of pollution?")
yb = D.band(s, yb + 0.16, "Zero? If your answer is zero — why do we still have any?",
            kind="note", size=15)
D.cards3(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (RED, "THE CASE FOR ZERO", "Pollution harms people who never agreed to it. Any amount "
     "of it is somebody bearing a cost they did not choose."),
    (BLUE, "THE CATCH", "Cleaning up is not free. Every tonne removed costs real "
     "resources — people, equipment, energy — that had another use."),
    (GREEN, "THE SOCIAL OPTIMUM", "Set MARGINAL SOCIAL BENEFIT against MARGINAL SOCIAL COST and solve. "
     "Part 1 does exactly that, and the answer is not zero."),
], body_size=11.5)
D.kicker(s, "The answer is a QUANTITY, set where MARGINAL SOCIAL BENEFIT equals "
            "MARGINAL SOCIAL COST — and it is not zero.")
D.notes(s, """Cold open. Do not answer it yet.

This question is imported from the Mateer & Coppock deck (their Chapter 7, the internal/external/social page), not
from Acemoglu. It is here because it is the best available way into the chapter: almost
every student's instinct is "zero", and the whole apparatus of the chapter exists to
explain why that instinct is wrong without being callous.

Ask it and let it sit. If you are recording rather than teaching live, say "your first
answer is probably zero" and move on — do not leave a silence.

The trap to name explicitly: "optimal" does not mean "desirable". It means the point where
one more unit of cleanup costs more than it is worth. Students who have only ever thought
about the health costs of pollution have never priced the abatement side at all.

THE PAYOFF IS SLIDE 8, and you should say so here so they wait for it. Exhibit 9.2 solves
for a socially optimal quantity of electricity of 300 billion kWh. Not 400, which is what
the market picks. And not zero. That number is the answer to this slide, and it comes out
of a diagram rather than out of a value judgement, which is the thing worth showing.""")

# ================================================================= 3. roadmap
s = S()
D.title(s, "Chapter 9 in Five Moves")
yb = D.band(s, 1.12, "One idea, five times over: PRIVATE cost and benefit are not "
                     "SOCIAL cost and benefit.", kind="formula", size=13.5)
D.strip5(s, yb + 0.30, [
    ("What an externality\nis, and what it costs", IC % "factory"),
    ("Whether people can\nfix it themselves", IC % "exchange"),
    ("What government\ncan do about it", IC % "ballot-box"),
    ("Goods the market\nwill not supply", IC % "apartment"),
    ("Goods the market\nuses up", IC % "wheat"),
], label_size=10.5)
D.band(s, 3.30, "Sections 9.1 → 9.5:   EXTERNALITIES · PRIVATE SOLUTIONS · "
                "GOVERNMENT SOLUTIONS · PUBLIC GOODS · COMMON POOL RESOURCES",
       kind="neutral", size=12.5)
D.kicker(s, "MARKET FAILURE — an inefficient allocation of resources. All five "
            "sections of this chapter are cases of it.")
D.notes(s, """Roadmap. Read the top band — it is the whole chapter in one line.

The shape is worth naming out loud because it is not obvious from the section titles.
Sections 9.1 to 9.3 are ONE market, examined three times: what goes wrong (9.1), whether
the parties can fix it privately (9.2), and what government can do if they cannot (9.3).
Sections 9.4 and 9.5 are a different problem — not a market that misprices, but goods
that markets will not or cannot supply properly at all.

The link between the two halves, which the book makes and students miss: a common pool
resource is a negative externality with the property right missing. Section 9.5 is
section 9.1 wearing different clothes. Say that at the Part 5 divider too.

If you are short of time, Part 5 compresses well; Parts 1 and 4 do not.""")

# ============================================================= 4. PART 1 divider
s = S()
D.divider(s, "PART 1", "When the Price Stops\nTelling the Truth")
D.notes(s, """Divider. Section 9.1, Externalities.

One sentence over it: for seven chapters the price has carried every cost of making the
thing and every benefit of having it. Now some of the cost gets left out of the price,
and the market clears anyway — at the wrong quantity.""")

# ====================================================== 5. what an externality is
s = S()
D.title(s, "Somebody Outside the Deal Pays Part of the Bill")
yb = D.defbox(s, 1.12, "An EXTERNALITY occurs when an economic activity has either a spillover COST to, or a "
                       "spillover BENEFIT for, a bystander.")
D.cards3(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (BLUE, "INTERNAL COST", "What the people in the market actually pay. Coal, turbines, "
     "wages, the loan. This is the firm's supply curve.", IC % "factory"),
    (RED, "EXTERNAL COST", "What the activity costs everybody else. Sulphur dioxide, "
     "mercury, a warmer planet. Nobody in the market is billed for it.", IC % "house"),
    (DGOLD, "SOCIAL COST", "The two added together. What the activity really costs the "
     "world. This is the curve the market never sees.", IC % "balance-scale"),
], body_size=11.5)
D.kicker(s, "MARGINAL EXTERNAL COST — social cost minus private cost, per unit. "
            "It has a size, and you can draw it.")
D.notes(s, """The definition and the vocabulary. Read the definition off the slide; it is
the book's own wording.

THE THREE-CARD LADDER IS IMPORTED from the Mateer & Coppock deck (their Chapter 7, slides
7 and 8). Acemoglu's deck draws MC, MEC and MSC on the diagram but never names the
decomposition, and a lot of exam questions are phrased in the internal / external / social
vocabulary rather than the marginal one. Give students both and say they are the same
thing: internal = private = what the supply curve shows; external = the spillover; social
= the sum.

The same three words work on the benefit side, and you should say so now rather than in
ten minutes: internal benefit, external benefit, social benefit. Section 9.1's second half
is exactly that.

Two examples that land, both from the book's own notes. Negative: a power plant's
emissions — sulphur dioxide and nitrogen oxides, linked to bronchitis and pneumonia,
mercury from coal linked to birth defects. Positive: a vaccination, or a year of somebody
else's schooling.

The word "bystander" is doing the work. Test any candidate example against it: is the
person bearing the cost a PARTY to the transaction? If they are, it is not an externality.
That test is what the pecuniary-externality page is about, and it is worth planting here.""")

# ============================================================ 6. Exhibit 9.1
figpage("The Market for Electricity, As Chapter 4 Would Draw It",
        "MARKET EQUILIBRIUM — 400 billion kWh at $0.20, where supply is "
        "MARGINAL PRIVATE COST only.",
        "elec_market",
        "The supply curve is MARGINAL PRIVATE COST — what the plant pays. It is not "
        "MARGINAL SOCIAL COST.",
        credit="Redrawn from Exhibit 9.1.")
D.notes(prs.slides[-1], """Exhibit 9.1. The starting picture, and it should look completely
familiar — that is the point.

Numbers to say exactly: equilibrium quantity 400 billion kilowatt-hours, equilibrium price
​$0.20 per kilowatt-hour. Demand is P = 0.40 minus 0.0005Q; supply is P = 0.0005Q. Both
recovered from the drawn exhibit.

Say plainly that everything students know so far says this outcome is efficient. Chapter 7
proved it: at the intersection, total surplus is maximised. Nobody has made a mistake.
Every buyer who values a kilowatt-hour above its cost gets one.

Then set up the turn: the supply curve is the firm's marginal COST curve, and the question
for the next slide is whose costs are in it.

The book's own way in is a warm-up worth borrowing if you have the time: imagine a factory
that could get all its yarn free — what happens to supply? It shifts out, and it produces
more. Now: were the resources that made the yarn actually free, or was somebody else just
paying for them? That is the entire chapter in one question.""")

# ==================================================== 7. what the picture leaves out
photopage("What That Diagram Does Not Show",
          "plant",
          "Where does the smoke go on this graph?",
          "Nowhere. Burning coal to make electricity releases sulphur dioxide and nitrogen "
          "oxides — lung irritation, bronchitis, pneumonia. At high doses the mercury "
          "from coal plants has been linked to birth defects. Emissions from power "
          "generation are part of the warming record.\n\n "
          "None of it appears on the supply curve, because the plant is not billed for "
          "any of it. The curve is an honest picture of the plant's costs. It is a "
          "dishonest picture of the electricity's costs.",
          "NEGATIVE EXTERNALITY — a spillover COST borne by a bystander, and no price "
          "anywhere reflects it.")
D.notes(prs.slides[-1], """The turn. This is the slide where the chapter starts.

Deliver it slowly. The argument is not "firms are bad" — it is that the firm's supply
curve is a correct answer to the wrong question. It records what the plant pays. It was
never designed to record what the electricity costs.

The health list is the book's own, from section 9.1: sulphur dioxide and nitrogen oxides
causing lung irritation, bronchitis and pneumonia; mercury from coal-burning plants linked
at high dosage to birth defects; global warming linked to power-plant emissions. Say the
list rather than gesturing at "pollution" — the specificity is what makes the size of the
external cost plausible when we put a number on it two slides from now.

Watch the framing when you say who pays. The people breathing it are not buying the
electricity and not selling it. That is what makes them bystanders and this an externality
rather than just an unpleasant cost.

If a student asks whether the plant "should have known" — that is section 9.2's question,
not this one. Park it, and say Part 2 answers it.""")

# ============================================================ 8. Exhibit 9.2
figpage("Adding the Cost Nobody Bills",
        "MARGINAL SOCIAL COST = MARGINAL PRIVATE COST + MARGINAL EXTERNAL COST, "
        "and MEC = $0.10 throughout.",
        "elec_msc",
        "SOCIALLY OPTIMAL QUANTITY = 300 billion kWh, where demand meets MSC. "
        "Not 400, and not zero.",
        credit="Redrawn from Exhibit 9.2.")
D.notes(prs.slides[-1], """Exhibit 9.2. THIS SLIDE ANSWERS THE COLD OPEN. Say so.

Numbers to read, not recall. The marginal external cost is ​$0.10 per kilowatt-hour and it
is CONSTANT, which is why MSC runs exactly parallel to supply. Market quantity 400 at
​$0.20. Socially optimal quantity 300 at ​$0.25. MSC at the market quantity is ​$0.30.

Walk it in this order and no other:
  1. The firm decides using the costs it actually pays. That is S. It picks 400.
  2. The costs it avoids do not stop existing. Add them: that is MSC.
  3. Society's right quantity is where demand meets MSC, because MSC is the whole cost.
     That is 300.

Now go back to the cold open explicitly. The optimal amount of this polluting activity is 300
billion kilowatt-hours a year. It is a positive number, and it is smaller than the market
picks. Zero would mean giving up 300 billion kilowatt-hours whose value to buyers exceeds
their full social cost. The reason we do not eliminate pollution is the same reason we do
not eliminate anything else: at some point the next unit of cleanup costs more than it is
worth.

THE ERROR THAT COSTS MARKS EVERY TERM: reading the socially optimal PRICE off the wrong
curve. At Q = 300 the price is ​$0.25, which is on the demand curve. Students routinely
read ​$0.15 off the supply curve instead. Say it once here and once more on the Pigouvian tax page.""")

# ============================================================ 9. Exhibit 9.3
figpage("Putting a Number on the Damage",
        "Between 300 and 400, MARGINAL SOCIAL COST exceeds MARGINAL BENEFIT on "
        "every unit produced.",
        "elec_dwl",
        "DEADWEIGHT LOSS = ½ × $0.10 × 100 = $5 billion — value that no one "
        "receives.",
        credit="Redrawn from Exhibit 9.3.")
D.notes(prs.slides[-1], """Exhibit 9.3. The deadweight loss, and this one is examinable as
a drawing.

The arithmetic, out loud: the triangle has vertices at (300, ​$0.25), (400, ​$0.20) and
(400, ​$0.30). Its vertical side is the ​$0.10 external cost; its horizontal side is the
100 billion kWh of over-production. Half of 0.10 times 100 is 5. Five billion dollars.

The unit-by-unit argument is the one that convinces. Take the 301st unit. The buyer values
it at just under ​$0.25 — that is the demand curve. It costs society just over ​$0.25 —
that is MSC. So making it destroys a little value. Do that for every unit from 300 to 400
and the little slivers add to the triangle.

Say what the triangle is NOT. It is not the total damage from pollution — the total damage
is the whole area between S and MSC out to 400, which is much larger, and most of it is
attached to units we would want produced anyway. The triangle is the AVOIDABLE part: the
loss from producing the wrong quantity, over and above the unavoidable cost of producing
the right one. Students conflate these two constantly and the distinction is worth thirty
seconds.

Same shape as the tariff triangles in Chapter 8, and worth saying so: a deadweight loss is
always value that nobody receives, as opposed to a transfer, which somebody does.""")

# ==================================================== 10. Exhibits 9.4 and 9.5
figpage("The Same Argument, Upside Down",
        "MARGINAL SOCIAL BENEFIT = MARGINAL PRIVATE BENEFIT + MARGINAL EXTERNAL "
        "BENEFIT, and MEB = $20 thousand.",
        "educ_dwl",
        "POSITIVE EXTERNALITY — a spillover BENEFIT. The market UNDER-produces: "
        "40, not the optimal 50.",
        credit="Redrawn from Exhibits 9.4 and 9.5.")
D.notes(prs.slides[-1], """Exhibits 9.4 and 9.5, merged onto one page. The positive case.

Numbers: demand P = 80 minus Q, supply P = Q, both in thousands of dollars against
millions of years of schooling. The market lands at 40 million years at ​$40 thousand. The
marginal external benefit is ​$20 thousand and constant, so MSB is P = 100 minus Q, and the
social optimum is 50 million years at ​$50 thousand. Deadweight loss is a half times 20
times 10 = 100 in the figure's units.

The book's list of the external benefits of education, from section 9.1, and it is worth
reading: higher wages mean more tax revenue; less reliance on social programmes; less
crime; more innovation; a better-functioning society. Vaccination is the book's other
example and it is the cleaner one — the benefit to the people you do not infect is
completely outside your decision.

THE STRUCTURAL POINT, and it is the one that gets examined: for a negative externality the
wedge is added to the COST side, so the extra curve sits above SUPPLY and the optimum moves
LEFT. For a positive externality the wedge is added to the BENEFIT side, so the extra curve
sits above DEMAND and the optimum moves RIGHT. In both cases the new curve is above the old
one. What differs is which curve it is above. Next slide puts the two side by side.

Careful with the units — they are stylised. Do not quote a total subsidy bill from this
diagram.""")

# ================================================================= 11. the contrast
figpage("Two Failures, One Diagnosis",
        "Both markets clear, and both clear at the wrong quantity — the "
        "EXTERNALITY decides the direction.",
        "neg_pos",
        "NEGATIVE EXTERNALITY → OVER-PRODUCTION.   POSITIVE EXTERNALITY → "
        "UNDER-PRODUCTION.")
D.notes(prs.slides[-1], """The contrast page. If a student remembers one slide from Part 1,
this is the one to make it.

The book's own summary, from the end of section 9.1: when externalities are present the
free-market outcome is inefficient; with negative externalities markets produce and consume
too much; with positive externalities they produce and consume too little.

How to say it so it sticks: the market counts only what shows up in someone's own ledger.
When a cost is missing from the ledger the thing looks cheaper than it is, so we buy too
much. When a benefit is missing the thing looks less valuable than it is, so we buy too
little. That is the whole of section 9.1.

Drill the direction with a fast oral round — secondhand smoke, a vaccination, littering,
a restored historic building, a neighbour's 2 a.m. drum kit, a beehive next to an orchard.
For each: which kind, and does the market give us too much or too little?

The failure mode to pre-empt: students memorise "externality means too much" because the
pollution case is taught first and taught longest. Half of exam questions on this section
are positive-externality questions precisely because that asymmetry is so common.""")

# ============================================== 12. pecuniary externalities
s = S()
D.title(s, "Not Every Spillover Is an Externality")
yb = D.defbox(s, 1.12, "PECUNIARY EXTERNALITY — when a market exchange affects other people through market prices.")
yb = D.band(s, yb + 0.14,
            "A PECUNIARY EXTERNALITY is a TRANSFER through prices — not a MARKET "
            "FAILURE, and it creates no DEADWEIGHT LOSS.", kind="formula", size=13)
_top = yb + 0.18
D.cards2(s, _top, LIMIT - _top, [
    (RED, "NOT AN EXTERNALITY", "A phone becomes the thing to own, demand rises and you "
     "pay more. You are IN this market. The higher price is the signal doing its job — "
     "and it is somebody else's higher income.", IC % "price-tag"),
    (GREEN, "AN EXTERNALITY", "The plant upwind sells you nothing and buys nothing from "
     "you, and you breathe its output anyway. No price connects you to it, so no price "
     "adjusts.", IC % "factory"),
], body_size=11)
D.kicker(s, "The test is not “was I made worse off?” It is “was I a party to the "
            "transaction?”")
D.notes(prs.slides[-1], """Pecuniary externalities. Section 9.1's last idea, and the one
students most often get backwards.

The book's own example: a good becomes fashionable, lots of people buy it, demand rises and
so does the price. You now pay more. That is bad for you — and it is not an externality.
You are a participant in that market. The price rise is the market reallocating a scarce
good toward the people who value it most, which is the mechanism working exactly as
Chapters 4 and 7 described.

The reason it matters, beyond definitions: pecuniary effects do not create deadweight loss
and do not justify intervention. Real externalities do. A student who cannot tell them
apart will argue for a tax on anything whose price went up.

The other half of it, which the book does not spell out but is worth one sentence: your
higher price is somebody's higher revenue. The loss to you is a TRANSFER, not a
destruction. Compare with the deadweight-loss page, where the ​$5 billion goes to nobody at all. That is the
same transfer-versus-deadweight-loss distinction from the tariff diagram in Chapter 8, and
naming the parallel helps.

Test to give them, and it is on the kicker: not "am I worse off" but "was I a party to the
transaction". If you were, it is a price effect. If you were not, it is an externality.""")

# ============================================================ 13. Exam Check 1
s = S()
D.title(s, "Exam Check: Is It an Externality, and Which Kind?")
examcheck(s, 1.12, [
    ("Which of these most likely creates a NEGATIVE externality?",
     "A  Eating a slice of pizza\n "
     "B  Smoking a cigarette\n "
     "C  Taking a nap\n "
     "D  Getting a college degree",
     "B — smoking a cigarette",
     "Secondhand smoke lands on people who are not party to the sale. A and C affect only "
     "you; D is the standard POSITIVE case."),
    ("Your neighbourhood becomes fashionable and your rent goes up. Is that an "
     "externality?",
     "A  Yes — negative, you are worse off\n "
     "B  Yes — positive, for the landlord\n "
     "C  No — it is a pecuniary effect\n "
     "D  No — rent is not a market price",
     "C — a pecuniary effect",
     "You are a party to the rental market. The price moved against you, which is the "
     "market working, not a cost bypassing it."),
])
D.notes(prs.slides[-1], """Exam Check 1. The answers are on the slide deliberately — this
is a worked page, not a pause-and-think prompt.

BOTH ITEMS ARE ADAPTED FROM THE MATEER & COPPOCK DECK (their Chapter 7, slides 10 and 11).
Their originals ask for the negative case and the positive case as two separate questions;
the second one here has been rewritten to test the pecuniary distinction instead, because
that is where this cohort actually loses marks and because the pecuniary-externality page has just set it up.

Deliver these by reading the stem, giving a beat, then reading the answer and the reason.
Do not skip the reason — the reason is the transferable part.

On item 1, the distractor that matters is D. A college degree is the book's flagship
POSITIVE externality, so a student who has half-learned "externality = bad" picks it.
Say that out loud.

On item 2, if you want one more: a student who picks A has correctly noticed they are worse
off and incorrectly concluded that being worse off is what defines an externality. Point at
the kicker on the previous slide.""")

# ============================================================= 14. PART 2 divider
s = S()
D.divider(s, "PART 2", "Can They Just Sort It Out\nBetween Themselves?")
D.notes(s, """Divider. Section 9.2, Private Solutions to Externalities.

One line over it: before we call the government, ask whether the people involved have any
reason to fix this on their own. Sometimes they do, and the answer is more interesting than
it sounds.""")

# ================================================== 15. the bargaining table
s = S()
D.title(s, "Fred's Filter: A Bargain Worth Making")
yb = D.band(s, 1.12, "Fred's sweater plant discharges upstream. Anne's brewery draws the "
                     "water downstream. Profits per day:", kind="neutral", size=13)
D.table(s, 0.60, yb + 0.16, 8.80, 1.44, [
    ["", "Without the filter", "With the filter", "Change"],
    ["Fred (sweater plant)", "$130", "$100", "−$30"],
    ["Anne (brewery)", "$90", "$140", "+$50"],
    ["Both together", "$220", "$240", "+$20"],
], col_w=[2.60, 2.20, 2.10, 1.90], first_col_fill=BLUE, body_size=11, row_h=0.34)
D.band(s, 3.42, "The filter is worth $50 to Anne and costs Fred $30, so any payment "
                "strictly between them works.\n "
                "At $35: Fred ends at $135 (+$5), Anne at $105 (+$15). The $20 gain "
                "is split, not created twice.", kind="answer", size=13)
D.kicker(s, "PRIVATE BARGAINING: the filter creates the $20 SOCIAL GAIN. The payment only "
            "splits it — $5 to Fred, $15 to Anne.")
D.notes(prs.slides[-1], """The bargaining table, from section 9.2. This is the book's own
example and its own numbers — use them.

Read the table across. Without the filter Fred makes ​$130 a day and Anne ​$90. With it Fred
makes ​$100 and Anne ​$140. So the filter costs Fred ​$30 and is worth ​$50 to Anne.

Why Fred will never fit it unprompted: it lowers HIS profit. There is no confusion and no
villainy here — he is responding correctly to the costs he faces, which is exactly the
diagnosis from Part 1.

The bargain. Anne gains ​$50; Fred loses ​$30. Total surplus rises by ​$20. Any payment
strictly above ​$30 and strictly below ​$50 makes both of them better off. The book works
​$35: Fred gets ​$100 plus ​$35 = ​$135, up ​$5. Anne gets ​$140 minus ​$35 = ​$105, up ​$15.

THE POINT STUDENTS MISS, and it is worth being explicit: the payment does not create the
​$20. The FILTER creates the ​$20. The payment only decides how it is divided — ​$5 to Fred
and ​$15 to Anne at a price of ​$35. Move the price and you move the split, not the total.
Check it on the slide: 5 plus 15 is 20.

The bounds are examinable and the strict inequality matters. At exactly ​$30 Fred is
indifferent; at exactly ​$50 Anne is. Neither is a bargain either party has a reason to
strike.""")

# ==================================================== 16. Coase, both directions
s = S()
D.title(s, "Coase: Change Who Is Liable, and Watch What Does Not Change")
yb = D.defbox(s, 1.12, "COASE THEOREM — with clear PROPERTY RIGHTS and low TRANSACTION COSTS, private "
                       "bargaining reaches an EFFICIENT allocation, whoever holds the right.", size=14)
# the fence cost lives in the table's corner cell rather than in a band of its own:
# a band here grew through the kicker rule, which is the documented Ch08 failure.
_ty = yb + 0.16
_th = 1.20
D.table(s, 0.60, _ty, 8.80, _th, [
    ["Cattle stray onto\na wheat farm.\nA fence costs $25,000.",
     "If the RANCHER is liable", "If the FARMER bears it"],
    ["Damage is $30,000", "Rancher builds the fence — $25,000",
     "Farmer builds the fence — $25,000"],
    ["Damage is $20,000", "Rancher pays $20,000 in damages",
     "Farmer absorbs $20,000"],
], col_w=[2.20, 3.30, 3.30], first_col_fill=BLUE, body_size=10.5, row_h=0.52)
_by = D.band(s, _ty + _th + 0.16,
             "Read DOWN the columns: they are identical. The law decides who pays. "
             "It does not decide what gets done.", kind="answer", size=13.5)
D.kicker(s, "The EFFICIENT OUTCOME is invariant to the assignment of PROPERTY RIGHTS. "
            "Only the DISTRIBUTION changes.", y=max(4.45, _by + 0.14))
D.notes(prs.slides[-1], """The Coase theorem, and THIS IS THE MOST IMPORTANT SLIDE IN PART
2. Give it time.

THE 2x2 IS IMPORTED FROM THE MATEER & COPPOCK DECK (their Chapter 7, slides 20 to 22).
This matters and is worth knowing why. Acemoglu's Fred-and-Anne table runs the bargain in
ONE direction only — Anne pays Fred — which shows that bargaining can reach efficiency but
never shows the invariance. The invariance is the actual content of the Coase theorem and
it is the thing exams ask about. Their rancher-and-farmer case runs the same bargain under
BOTH assignments of the property right, with numbers, and the two columns come out
identical. That is why it is here.

Work the table cell by cell, out loud.
  Rancher liable, damage ​$30,000: he can build a ​$25,000 fence or pay ​$30,000. He builds.
  Rancher liable, damage ​$20,000: fence ​$25,000 or pay ​$20,000. He pays.
  Farmer bears it, damage ​$30,000: he can build a ​$25,000 fence or eat ​$30,000 of losses.
    He builds.
  Farmer bears it, damage ​$20,000: fence ​$25,000 or eat ​$20,000. He absorbs it.

Then say the sentence the whole slide exists for: the fence goes up in exactly the same
circumstances either way. Assigning the right changes who is out of pocket. It does not
change what happens to the land.

The second-best example if they are not convinced, also theirs, and it is the one that
lands with a room full of people who fly: reclining an airline seat. If the person in front
has the right to recline and the person behind values the space at ​$50 while the recliner
values reclining at ​$40, the person behind pays them not to recline. Reverse the right and
the recliner pays for permission when they value it at ​$70 against ​$50. Efficient outcome
either way; different person out of pocket.

DO NOT OVERSELL THIS. The conditions are doing enormous work and the next slide is about
how often they fail. Coase's own point was closer to "look at the transaction costs" than
"the government is unnecessary".""")

# ==================================================== 17. when bargaining fails
s = S()
D.title(s, "Why We Cannot Just Leave It to Bargaining")
yb = D.band(s, 1.12, "Three conditions on the COASE THEOREM — and real externalities break all three.",
            kind="flag", size=14)
D.cards3(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (RED, "TRANSACTION COSTS", "Negotiating takes lawyers, time and information. If that "
     "costs more than the $20 on the table, the efficient deal does not get struck.",
     IC % "receipt"),
    (RED, "UNCLEAR PROPERTY RIGHTS", "Bargaining needs somebody to hold the right. Who "
     "owns the air above a city, or an aquifer, or the ocean? Often the law does not say.",
     IC % "balance-scale"),
    (RED, "TOO MANY PARTIES", "Fred and Anne is two people. A power plant and 100,000 "
     "downwind households cannot get into a room, and each has a reason to stay out.",
     IC % "apartment"),
], body_size=11)
D.kicker(s, "TRANSACTION COSTS, ill-defined PROPERTY RIGHTS and FREE RIDING are why private "
            "bargaining usually fails.")
D.notes(prs.slides[-1], """The limits, from section 9.2. The book lists exactly these three
and you should attribute the shape of the argument to it.

Card 1, transaction costs. The condition is not "bargaining is free" — it is that
bargaining costs less than the surplus at stake. Fred and Anne have ​$20 a day to divide;
if a lawyer costs ​$300 an hour there is no deal, and the filter does not get fitted even
though fitting it would make the world better off.

Card 2, property rights. This is the one worth dwelling on because it connects forward. If
nobody owns the resource, there is nobody to buy the right from and nobody to sell it. Hold
that thought — it is the whole of Part 5. The tragedy of the commons is this card.

Card 3, numbers. The book's own illustration is a power plant against 100,000 fishermen.
Beyond the logistics there is a free-riding problem: if the other 99,999 fund the
settlement, my share of the benefit arrives anyway. Everyone reasons that way and the
coalition never forms. That is Part 4's free-rider problem showing up early, and naming it
here makes Part 4 easier.

The book's third private solution, which does not get its own page: doing the right thing.
People recycle without being paid to and mostly without being forced to. Social norms move
behaviour toward the social optimum. It is real and it is not sufficient — which is the
bridge to Part 3.""")

# ============================================================= 18. PART 3 divider
s = S()
D.divider(s, "PART 3", "What Government Can Do\nAbout It")
D.notes(s, """Divider. Section 9.3, Government Solutions to Externalities.

One line: if the parties cannot internalise the externality themselves, the question is
whether a third party can make them. Two families of answer, and the second one is where
the economics is.""")

# ============================================ 19. two families of policy
s = S()
D.title(s, "Two Ways In, and They Are Not Equivalent")
yb = D.band(s, 1.12, "INTERNALISING THE EXTERNALITY — making the decision-maker face the full social cost.", kind="formula", size=14)
D.cards2(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (BLUE, "COMMAND AND CONTROL", "Government regulates the allocation directly. Produce "
     "300, not 400. Fit this scrubber. Cap injection at 8,000 barrels a day. Simple, fast "
     "and effective — but it fixes the technology in place, because nothing rewards a "
     "firm for beating the standard.", IC % "ballot-box"),
    (GREEN, "MARKET-BASED", "Government changes the prices and lets firms choose: a tax "
     "per unit of harm, a subsidy per unit of benefit, a tradable permit. Slower to "
     "design — but it puts the abatement where it is cheapest, because the firm that "
     "can cut cheaply now has a reason to cut more.", IC % "coin-stack"),
], body_size=13)
D.kicker(s, "COMMAND-AND-CONTROL sets the QUANTITY. MARKET-BASED POLICY sets the PRICE and "
            "lets firms choose the quantity.")
D.notes(prs.slides[-1], """The two families, from the top of section 9.3.

The book's framing: command-and-control policies directly regulate the allocation of
resources; market-based policies give private parties an incentive to internalise the
externality themselves.

The catalytic converter is the book's argument FOR command-and-control and it is a good
one. Ask: if a catalytic converter were optional, like a sunroof, would you buy one? Almost
nobody would — there is no private benefit and a real private cost. Even the
environmentally committed would mostly not, because one car's emissions change nothing.
Required since 1975, and mandating it imposes the same cost on everyone at once. Some
externalities have no realistic market fix.

The argument AGAINST it, also the book's: the regulator has to pick the technology, and
firms then aim at the standard rather than past it. A firm that could cut emissions far
more cheaply has no reason to.

The efficiency case for market-based tools, which the book makes and which you should say
plainly: a tax equalises MARGINAL abatement cost across firms. Firms that can cut cheaply
cut a lot, firms that cannot cut little, and any given total reduction is achieved at the
lowest possible cost. A uniform mandate cannot do that — it forces the same action on a
firm for which it is cheap and a firm for which it is ruinous.

Do not let this become ideological. Both tools are in the book, both are used, and the EBE
in this chapter is a case where command-and-control demonstrably worked.""")

# ============================================================ 20. Exhibit 9.8
figpage("A Tax That Is Exactly the Right Size",
        "PIGOUVIAN TAX = MARGINAL EXTERNAL COST = $0.10 per kWh, which lifts supply onto MSC.",
        "elec_tax",
        "TAX INCIDENCE: buyers pay $0.25, sellers keep $0.15. Revenue of $30 billion is a "
        "TRANSFER, not the efficiency gain.",
        credit="Redrawn from Exhibit 9.8.")
D.notes(prs.slides[-1], """Exhibit 9.8. The Pigouvian tax, and the mechanism is prettier
than students expect.

Definition to read: a Pigouvian tax is the tax necessary to make a firm produce the
socially optimal level of output. It addresses a negative externality by charging the
producer of it.

The numbers. Tax of ​$0.10 per kilowatt-hour. It shifts the firm's supply curve up by
exactly ​$0.10 — which lands it precisely on MSC, because the marginal external cost is
constant at ​$0.10. The firm now maximises profit at 300 billion kWh. Consumers pay ​$0.25.
Producers keep ​$0.15. Tax revenue is ​$0.10 times 300 = ​$30 billion.

The elegance worth naming: nobody told the firm to produce 300. The firm still does exactly
what it did before — sets its own marginal cost against price — and lands on the social
optimum, because its own cost curve now tells the truth. That is what "internalising the
externality" means, in one diagram.

SAY THE CONDITION OUT LOUD or students will over-generalise: the tax equals MSC only
because the external cost is constant per unit here. If the marginal damage rose with
output, the right instrument would be a tax equal to the marginal external cost AT THE
OPTIMAL QUANTITY, and it would not reproduce the whole MSC curve.

Two errors to pre-empt, both worth marks. First: the price consumers pay rises by ​$0.05,
not by the full ​$0.10 — the incidence splits, exactly as in Chapter 4. Second, the one
from the Exhibit 9.2 page again: the optimal price is read off DEMAND at Q = 300, which is ​$0.25.
Producers receiving ​$0.15 is a different number and both appear on the diagram.

Real examples if you want them: the federal gasoline tax, state gasoline taxes, and taxes
on tobacco and alcohol are all defended on these grounds.""")

# ============================================================ 21. Exhibit 9.9
figpage("And a Subsidy That Is Exactly the Right Size",
        "PIGOUVIAN SUBSIDY = MARGINAL EXTERNAL BENEFIT = $20 thousand, which lifts demand "
        "onto MSB.",
        "educ_subsidy",
        "Quantity rises from 40 to the SOCIALLY OPTIMAL 50, and the DEADWEIGHT LOSS "
        "is eliminated.",
        credit="Redrawn from Exhibit 9.9.")
D.notes(prs.slides[-1], """Exhibit 9.9. The Pigouvian subsidy. Deliver it as the mirror of
the last slide and it costs you two minutes instead of five.

Definition: a Pigouvian subsidy is the subsidy necessary to make an agent increase
consumption to the socially optimal level. It addresses a positive externality by
encouraging buyers to demand more.

Numbers: subsidy of ​$20 thousand per year of schooling, equal to the marginal external
benefit. Demand shifts up by ​$20 thousand, which lands it exactly on MSB. Quantity rises
from 40 to 50 million years. Producers receive ​$50 thousand; buyers pay ​$50 thousand minus
the ​$20 thousand subsidy.

Real examples, from the book: states subsidise college tuition; tax credits for electric
vehicles and for home insulation and heat pumps. And the non-price version — laws
REQUIRING consumption. Vaccination before school enrolment, compulsory schooling between
about 6 and 16. Those are command-and-control answers to a positive externality, which is
a combination students rarely think of.

A FLAG ON THE PUBLISHER'S OWN MATERIAL, and it only affects screen-reader users. The
accessibility description attached to this exhibit says the top of the subsidy arrow is at
"(40, 60) on the supply curve". Supply passes through (40, 40). The point (40, 60) is on
MSB. The drawn figure is right and the description is wrong. If a student quotes the
description back at you, that is why. Do not name the publisher when you say it.""")

# ================================================================ 22. cap and trade
s = S()
D.title(s, "Selling the Right to Pollute")
yb = D.defbox(s, 1.12, "CAP AND TRADE — government fixes the total QUANTITY of emissions and issues "
                       "permits for it, then lets firms buy and sell them.",
              size=15)
D.cards3(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (GREEN, "WHO SELLS", "A firm that can cut emissions cheaply cuts more than it has to "
     "and sells the permits it no longer needs. The cut costs it less than the permit "
     "fetches.", IC % "factory"),
    (BLUE, "WHO BUYS", "A firm facing high abatement costs buys permits instead. Paying "
     "for the right is cheaper than retooling.", IC % "coin-stack"),
    (DGOLD, "WHAT IT CREATES", "A property right in something that never had one. The cap "
     "fixes the total; the market decides who does the cutting, and it picks the cheapest "
     "cutters.", IC % "balance-scale"),
], body_size=12.5)
D.kicker(s, "A permit price equalises MARGINAL ABATEMENT COST across firms — least-cost for "
            "any given CAP.")
D.notes(prs.slides[-1], """Cap and trade.

THIS SLIDE IS IMPORTED FROM THE MATEER & COPPOCK DECK (their Chapter 7, the tragedy-of-the-commons page). Section
9.3 of our own book covers "market-based approaches", but the publisher's slides stop at
corrective taxes and subsidies and never reach tradable permits. Since cap and trade is the
main real-world market-based instrument and appears in every exam bank for this topic, it
is worth the page. If you would rather stay strictly inside the Acemoglu text, this is the
one slide in Part 3 to cut.

The mechanism, said carefully. Government does not set a price; it sets a QUANTITY, and the
market discovers the price. That is the exact opposite of a Pigouvian tax, which sets a
price and lets the market discover the quantity. Under certainty the two are equivalent;
that equivalence is a graduate-level result and you do not need it here, but the
price-versus-quantity contrast is a good sentence.

Why the total cost falls: every firm faces the same permit price, so every firm cuts until
its own marginal abatement cost equals that price. Marginal abatement costs end up equal
across firms, which is the condition for achieving any given total reduction at least cost.
A uniform mandate cannot equalise anything.

The honest difficulties, and say them. Setting the cap requires knowing the right total.
Enforcement needs measurement. And an emissions market bounded by one country puts its own
firms at a cost disadvantage, so the pressure is toward international schemes, which are
correspondingly hard to negotiate. Critics call it "cap and tax" for the reason you would
expect.

Tie it back to the three-conditions page: this works by MANUFACTURING the property right that card 2 said
was missing.""")

# =========================================================== 23. pay as you throw
photopage("You Are a Producer of Externalities Too",
          "trash",
          "Should you be charged by the bag?",
          "Under a flat annual fee for rubbish collection, your marginal cost of throwing "
          "one more bag away is zero. So the landfill fills faster than anyone would "
          "choose.\n\n "
          "Pay-as-you-throw charges by volume instead. The cost of the next bag stops "
          "being zero, and households throw less and recycle more — the same mechanism as "
          "the tax on the plant, pointed at a consumer.",
          "A flat fee sets your MARGINAL COST of the next bag to zero. Consumers create "
          "NEGATIVE EXTERNALITIES too.")
D.notes(prs.slides[-1], """Pay as you throw. The book's Letting the Data Speak box in
section 9.3.

The mechanism is the one from the Pigouvian tax page, so keep it short. A flat fee means the marginal
cost of the next bag is zero, so the quantity chosen is far above the social optimum.
Charging by volume makes the marginal cost positive, and quantity falls.

Why the slide is here at all: every example so far has had a firm as the villain, and
students leave the chapter believing externalities are something corporations do. This one
puts them on the other side of the diagram, and the arithmetic is identical.

The book's other consumer-side examples, if you want them: littering, playing music loudly,
driving in rush hour, secondhand smoke. Congestion pricing on the congestion-charge results is the same idea at
city scale, so this slide is also the setup for the closing EBE.

Worth one honest sentence: pay-as-you-throw creates its own problem, which is that illegal
dumping now has a positive payoff. Schemes have to be designed around that. Naming a policy
side-effect keeps the chapter from reading as advocacy.""")

# ================================================================ 24. EBE, posed
photopage("How Did Oklahoma Get Earthquakes?",
          "quake",
          "How can the government lower the number of earthquakes in Oklahoma?",
          "Oklahoma was a seismically quiet state. Then it was not — by 2015 it was "
          "recording hundreds of earthquakes a year.\n\n "
          "The cause is not the drilling. Fracturing produces saltwater as a by-product, "
          "too contaminated to purify, so it is injected deep underground. That raises "
          "pressure in the rock and triggers faults that were already there.",
          "Damage borne by bystanders — MARGINAL SOCIAL COST far above the MARGINAL "
          "PRIVATE COST the drillers face.",
          lead="Evidence-Based Economics · Section 9.3")
D.notes(prs.slides[-1], """The Evidence-Based Economics box for section 9.3. Pose it here;
the data answers it on the next two slides.

The chain of causation, from the book, and it is worth getting right because students
assume "fracking causes earthquakes" full stop: fracking produces saltwater as a by-product
→ the water is too chemically contaminated to purify → it is disposed of by deep injection
into the Arbuckle formation → that raises pore pressure in the rock → pressure triggers
faults that were already there. The earthquakes come from the DISPOSAL, not from the
fracturing. That distinction is what makes a targeted policy possible: you can cap
injection rates without banning extraction.

The externality, named in the book's own terms: loss of property, loss of financial
stability, even loss of life, with total costs running into the billions — which makes
marginal social cost far higher than the marginal cost the firms face. Exactly the Exhibit 9.2 page's
diagram, with a real number attached.

Note this chapter carries TWO Evidence-Based Economics boxes rather than the usual one —
this and the congestion-charge question on the congestion-charge results. If you are compressing, this is the
one to shorten, because the cost-benefit page already works its arithmetic.""")

# ================================================== 25. Exhibits 9.6 and 9.7
figpage("The Data, and a State That Tried Something",
        "Oklahoma's count and Kansas's response, on the same page and to different "
        "scales.",
        "quakes",
        "COMMAND-AND-CONTROL: Kansas capped injection in March 2015, and activity fell "
        "across every magnitude band.",
        credit="Redrawn from Exhibits 9.6 and 9.7.")
D.notes(prs.slides[-1], """Exhibits 9.6 and 9.7, one page. THE TWO PANELS ARE ON DIFFERENT
SCALES — left is earthquakes per YEAR in Oklahoma, right is per MONTH in Kansas. Say it
out loud; the subtitle says it too but nobody reads subtitles.

Left panel, numbers worth reading: essentially nothing until 2008 — single digits a year.
Then 20 in 2009, 103 in 2013, 585 in 2014, 887 in 2015. The book's line is that 2015 ran at
more than 300 times the annual average for 1973 to 2008. Quote it as the book's figure
rather than computing it from this chart, which starts in 2000.

Right panel. Kansas faced the same problem and in March 2015 ordered saltwater injection
rates cut: a cap of 16,000 barrels a day falling to 8,000 within 100 days, with penalties
up to ​$10,000 per day of continuing violation. The dashed line marks the order. Activity
falls across magnitude 2, 3 and 4 alike, and by December 2015 it is well below the 2014-15
peak.

BE HONEST ABOUT WHAT THIS SHOWS. It is a before-and-after comparison in one state, not a
controlled experiment. There is no control group, and other things changed — notably oil
prices, which fell hard over exactly this window and reduced drilling activity everywhere.
The book presents it as suggestive and so should you. A sharp student will raise this and
they will be right; having said it first is much better than conceding it.

Note the direction this cuts: the chapter's own showcase for command-and-control is
evidence the instructor should hedge. Say that too — it is what separates teaching
evidence from citing it.""")

# ============================================== 26. the EBE cost-benefit problem
s = S()
D.title(s, "Was It Worth Doing? Run the Numbers")
yb = D.band(s, 1.12, "Cutting injection enough to stop the earthquakes costs the industry "
                     "$1 billion a year. Oklahoma has 4 million residents.",
            kind="neutral", size=13)
D.table(s, 0.60, yb + 0.14, 8.80, 1.30, [
    ["What residents would pay", "Total willingness to pay", "Cost", "Go ahead?"],
    ["$100 each, every resident", "$100 × 4m = $400 million", "$1,000m",
     "No — net loss $600m"],
    ["Half at $500, half at $50", "$275 × 4m = $1,100 million", "$1,000m",
     "Yes — net gain $100m"],
], col_w=[2.50, 2.70, 1.40, 2.20], first_col_fill=BLUE, body_size=10.5, row_h=0.36)
D.band(s, 3.30, "Same policy, same cost, opposite answer. Everything turns on a number "
                "nobody can observe: what avoiding the risk is worth.", kind="flag",
       size=13)
D.kicker(s, "COST-BENEFIT ANALYSIS: costs are observable, WILLINGNESS TO PAY is not. That is "
            "where it breaks.")
D.notes(prs.slides[-1], """The chapter's end-of-chapter Evidence-Based Economics problem,
worked. This is the most exam-shaped slide in the deck — spend time on it.

Part (a). Every resident values avoiding the extra earthquakes at ​$100 a year. Four million
residents, so total willingness to pay is ​$400 million. Abatement costs ​$1 billion. Do not
do it: the loss is ​$600 million.

Part (b). Instead, half value it at ​$500 and half at ​$50. The average is ​$275, so total
willingness to pay is ​$1.1 billion against the same ​$1 billion cost. Now do it. The net
gain is ​$100 MILLION.

READ THAT NUMBER OFF THE SLIDE. The publisher's own answer key for this problem states the
net gain as "​$1 million". It is ​$100 million — 1.1 billion minus 1.0 billion — and their
figure is out by a factor of a hundred. Their wording also calls it a net gain "for
industry", which is wrong in a second way: industry is the party paying the ​$1 billion. It
is a net gain to SOCIETY. Teach the corrected version, and flag it without naming them,
because students revise from the publisher's slides too and will hit the error.

The lesson underneath the arithmetic, and it is the transferable one: costs are usually
observable — you can price scrubbers and equipment and lost output. Benefits usually are
not, because nobody is billed for clean air, so there is no market price to read. Everything
here turns on a survey number, and survey numbers of this kind are notoriously soft: people
answer differently when the money is hypothetical.

Note the distributional point hiding in part (b). The mean rises from ​$100 to ​$275 with no
change in the policy, purely because valuations are spread out. Cost-benefit analysis adds
willingness to pay across people, which quietly weights the answer toward those with more
to pay with. Worth one sentence — it is the standard objection to the method and students
should know it exists.""")

# ============================================================ 27. Exam Check 2
s = S()
D.title(s, "Exam Check: Picking the Right Instrument")
examcheck(s, 1.12, [
    ("Good X creates a negative externality. Which would NOT correct it?",
     "A  Subsidise the production of X\n "
     "B  Tax the production of X\n "
     "C  Limit how much X may be produced\n "
     "D  Make producers pay the external costs",
     "A — subsidise production",
     "A subsidy raises output. With a negative externality output is already too high, so "
     "this moves the market further from the optimum."),
    ("The marginal external cost is $0.10 per unit. The correct Pigouvian tax is:",
     "A  $0.05 — half, since incidence is shared\n "
     "B  $0.10 — the marginal external cost\n "
     "C  $0.30 — the marginal social cost at Qₘ\n "
     "D  Whatever raises the most revenue",
     "B — $0.10 per unit",
     "Set the tax equal to the external cost and supply becomes MSC. A confuses the tax "
     "with its incidence; revenue is a by-product, never the target."),
])
D.notes(prs.slides[-1], """Exam Check 2. Answers on the slide; work the reasons.

ITEM 1 IS FROM THE MATEER & COPPOCK DECK (their Chapter 7, Fred's filter). Item 2 is written for
this deck to catch the two errors the Pigouvian tax page's notes flag.

Item 1 is nearly free marks and students still lose them, because "subsidy" reads as
"government doing something" rather than as "government making the thing cheaper". Say the
direction out loud: a subsidy increases quantity; a negative externality means quantity is
already too high.

Item 2 is the one that separates. Distractor A is the incidence confusion — buyers do bear
only half the tax here, since the price rises from ​$0.20 to ​$0.25 while the tax is ​$0.10,
but that is a consequence of the tax, not its size. Distractor C picks the height of MSC at
the market quantity, ​$0.30, which is a number that appears on the diagram and is not the
tax. Distractor D is the policy-goal confusion; revenue is a side-effect.

If you want a third item orally: at the optimum, is the tax revenue equal to the deadweight
loss it eliminated? No — revenue is ​$30 billion and the deadweight loss removed was ​$5
billion. Revenue is a transfer; the ​$5 billion is the efficiency gain. Same distinction as
the pecuniary-externality page and Chapter 8's tariff.""")

# ============================================================= 28. PART 4 divider
s = S()
D.divider(s, "PART 4", "Goods the Market\nWill Not Supply")
D.notes(s, """Divider. Section 9.4, Public Goods.

One line: so far the market has produced the wrong QUANTITY. Now we meet goods it will
barely produce at all — and the reason is not a missing cost, it is a missing ability to
charge.""")

# =========================================== 29. rival and excludable
s = S()
D.title(s, "Two Questions That Sort Every Good")
yb = D.band(s, 1.12, "Ask them in this order. The answers are independent, which is why "
                     "there are four kinds of good and not two.", kind="formula", size=13.5)
D.cards2(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (BLUE, "IS IT RIVAL?", "If I consume it, can you still consume it? "
     "RIVAL — I eat the apple, you cannot; one trout, one person. "
     "NONRIVAL — we both stream the same film. The army defending me defends you at no "
     "extra cost.", IC % "shopping-cart"),
    (GREEN, "IS IT EXCLUDABLE?", "Can somebody who has not paid be kept out? "
     "EXCLUDABLE — no payment, no apple; no subscription, no stream. "
     "NONEXCLUDABLE — the army cannot defend the houses that paid and skip the one that "
     "did not.", IC % "house"),
], body_size=13)
D.kicker(s, "RIVALRY is a fact about the good. EXCLUDABILITY is a fact about whether you can "
            "charge for it.")
D.notes(prs.slides[-1], """The two characteristics, section 9.4. Get these exactly right —
everything in Parts 4 and 5 is built on them and this is where classification questions are
won or lost.

Run the book's own two questions live. "If I eat this apple, can you eat it too?" No —
rival. "Can you eat an apple without paying for it?" No — excludable. Then the same two
questions about national defence, and both answers flip.

THE CRITICAL POINT, and it is the single most common error in this topic: the two
properties are INDEPENDENT. A good can be nonrival and excludable (a streaming service). It
can be rival and nonexcludable (ocean fish). Students who collapse the two into one
spectrum — "private at one end, public at the other" — get the two off-diagonal boxes
wrong every time, and those two boxes are where the exam questions live.

The second most common error, and the book warns about it too: "provided by the government"
does not mean "public good". Public education is excludable (private schools charge) and
rival (a seat and a teacher's attention are used up). The postal service charges. Neither is
a public good in the technical sense. Say this twice; students reach for the everyday
meaning of "public" and it is not the same word.

The Mateer deck runs the same two questions with a hamburger and a satellite dish; the
substance is identical and the book's apple works fine.""")

# ============================================================ 30. Exhibit 9.10
s = S()
D.title(s, "Four Kinds of Good")
yb = D.band(s, 1.12, "PRIVATE GOODS · CLUB GOODS · COMMON POOL RESOURCES · PUBLIC GOODS — "
                "rivalry down the side, excludability across the top.",
            kind="neutral", size=13)
D.table(s, 0.60, yb + 0.16, 8.80, 2.10, [
    ["", "EXCLUDABLE — you can charge",
     "NONEXCLUDABLE — you cannot"],
    ["RIVAL\nused up", "PRIVATE GOODS\nclothes, food, furniture, a hamburger, a car\n "
     "The market supplies these well.",
     "COMMON POOL RESOURCES\nocean fish, groundwater, natural forest, a congested road\n "
     "Overused — all of Part 5."],
    ["NONRIVAL\nshared freely", "CLUB GOODS\nstreaming, satellite TV, campus Wi‑Fi, a "
     "country club\nSupplied privately, rarely competitively.",
     "PUBLIC GOODS\nnational defence, an early-warning system, mosquito abatement\n "
     "Barely supplied at all."],
], col_w=[1.70, 3.55, 3.55], first_col_fill=BLUE, body_size=9.5, row_h=0.42)
D.kicker(s, "The market supplies EXCLUDABLE goods. NONEXCLUDABILITY is what defeats it — "
            "and it defeats it twice over.")
D.notes(prs.slides[-1], """Exhibit 9.10, with a fuller example set. THE EXAMPLES ARE POOLED
from our own book and from the Mateer & Coppock deck (their Chapter 7, the rival/excludable page), because
between them the two decks cover the corners better than either does alone. The structure
of the grid is the book's.

Take the boxes in this order — easy diagonal first, then the corners.

PRIVATE GOODS. Rival and excludable. The market supplies these and Chapters 4 to 7 were
entirely about them. If you do not pay you do not get one, so a firm has every reason to
produce them.

CLUB GOODS. Nonrival but excludable. The market WILL supply these, because it can charge —
but note the shape: high fixed cost, near-zero marginal cost. Pricing at marginal cost, as
perfect competition would, means never covering the fixed cost. So these markets are
naturally concentrated. That is a forward reference to Chapter 12 and worth planting.

COMMON POOL RESOURCES. Rival but nonexcludable — the worst combination. One person's use
genuinely subtracts from what is left, and nobody can be kept out. Part 5.

PUBLIC GOODS. Nonrival and nonexcludable. Nobody can be charged and nobody needs to be
excluded. The market has no mechanism here at all.

Ask for their own examples for each box rather than supplying more. The classification
skill is the thing being examined, and a student who can generate examples can classify
them.

Congested roads are worth flagging as the interesting case: an empty road is nonrival, a
congested one is rival. Rivalry can depend on how many people show up.""")

# =========================================================== 32. the free rider
s = S()
D.title(s, "Why Nobody Will Sell You National Defence")
yb = D.defbox(s, 1.12, "FREE-RIDER PROBLEM — an individual does not pay for a good because it is "
                       "NONEXCLUDABLE, and consumes it anyway.")
D.cards3(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (BLUE, "NOBODY KNOWS THEIR SHARE", "Ask people to post a cheque to Washington for "
     "national defence. Even the willing cannot work out what their share is — the good "
     "is nonrival, so there is no quantity to divide.", IC % "ballot-box"),
    (RED, "NOBODY CAN BE MADE TO", "If you send nothing, will the army leave your street "
     "undefended? It cannot. Not paying costs you nothing at all.", IC % "house"),
    (GREEN, "SO IT IS TAXED", "Government supplies the good and makes paying compulsory. "
     "That is what taxation is for — not a moral claim, a solution to this exact "
     "problem.", IC % "coin-stack"),
], body_size=11)
D.kicker(s, "FREE RIDING is individually rational and collectively ruinous — hence "
            "COMPULSORY TAXATION.")
D.notes(prs.slides[-1], """The free-rider problem, section 9.4. The book's own thought
experiment and it is a good one — run it as a question, not a statement.

Ask: could the United States fund its military by asking people to send in what they think
it is worth? Students say no immediately. Push on WHY, because there are two distinct
reasons and they map onto the first two cards.

First, nonrivalry makes the share unknowable. With a private good your share is the unit you
buy. With a nonrival good everyone consumes the whole thing at once, so there is no natural
unit and no obvious contribution.

Second, nonexcludability removes any consequence. The book's version: if you do not
contribute, does the government tell the enemy to bomb your house first? Obviously not. The
army cannot defend the people who paid and skip the one who did not — not as a matter of
policy but as a matter of physics.

Then the conclusion, and put it gently but plainly: the market is not interested in
supplying a good it cannot charge for. So government provides it and makes paying
mandatory. That is what taxes ARE, structurally. Students who have only ever heard taxation
argued about morally find this framing clarifying.

Emphasise that free riding is not cheating. Every individual is reasoning correctly given
what everyone else does. The failure is collective, not moral. That framing is also what
makes Part 5 make sense — the herders are not villains either.""")

# ============================================== 33. Exhibits 9.11 and 9.12
figpage("Adding Up Demand — Sideways, Then Upwards",
        "Two identical buyers, one individual demand curve, two completely different "
        "MARKET DEMAND curves.",
        "summation",
        "PRIVATE GOOD — sum QUANTITIES horizontally.   PUBLIC GOOD — sum PRICES "
        "vertically.",
        credit="Redrawn from Exhibits 9.11 and 9.12.")
D.notes(prs.slides[-1], """Exhibits 9.11 and 9.12 side by side. THE MOST EXAMINABLE FIGURE
IN PART 4. If Part 4 gets one slow slide, make it this one.

Numbers. Each individual demand is P = 80 minus 10Q. For the PRIVATE good, at a common
price of ​$50 you buy 3 pairs and Jim buys 3, so the market buys 6 — add the quantities
sideways, and market demand is P = 80 minus 5Q, reaching zero at Q = 16. For the PUBLIC
good, at a common quantity of 3 missions the third is worth ​$50 to you and ​$50 to Jim, so
society values it at ​$100 — add the prices upwards, and market demand is P = 160 minus 20Q,
reaching zero at Q = 8.

WHY the rule differs, and this is the sentence that makes it stick rather than something to
memorise. For a private good, the question is "how many units will people buy at this
price?" — because each of you consumes a DIFFERENT unit. For a public good, the question is
"how much is this unit worth to everyone together?" — because you both consume the SAME
unit. The physical fact of nonrivalry is what turns the addition ninety degrees.

A FLAG ON THE PUBLISHER'S OWN MATERIAL, and this one has consequences. The accessibility
description attached to Exhibit 9.12 describes the summed public-good curve as running from
(0, 160) to (16, 0). That is a horizontal-sum axis attached to a vertical-sum figure. The
description's own sample point, (3, 100), requires the curve to reach zero at Q = 8, and the
drawn panel does run 0 to 8. The drawn figure is right. It matters because a student who
takes 16 will get the wrong optimal quantity on the very next slide. Flag it without naming
the publisher.

Both panels are drawn on the same axes on purpose, so the doubling of the vertical
intercept is visible. Say so — students otherwise read the empty right half of the second
panel as an error.""")

# ============================================================ 34. Exhibit 9.13
figpage("How Much Should We Provide?",
        "Provide until MARGINAL SOCIAL BENEFIT = MARGINAL SOCIAL COST — the same rule as ever.",
        "public_eq",
        "Q* = 4 missions at $80, where MSB = MSC. Only the DEMAND curve was built "
        "differently.",
        credit="Redrawn from Exhibit 9.13.")
D.notes(prs.slides[-1], """Exhibit 9.13. The payoff, and it is deliberately anticlimactic.

Numbers: the vertically summed demand P = 160 minus 20Q meets supply P = 20Q at 4 missions
and ​$80.

The reassurance to give: the decision rule has not changed since Chapter 3. Provide the good
up to the point where the marginal benefit of the last unit equals its marginal cost. That
is the same rule that governs how many burritos to make and how many hours to work. The ONLY
thing that changed in Part 4 is how the benefit curve was constructed — vertically rather
than horizontally — and that change came from a physical fact about the good.

Then the practical difficulty, which sets up nothing less than the whole business of
government: to apply the rule you have to know what everyone's willingness to pay actually
is. For a private good the market reveals it — people buy or they do not. For a public good
nobody is ever asked to pay, so nobody's valuation is revealed, and if you ask them directly
they have a reason to misstate it. Understate if you fear being billed; overstate if you
want the good and somebody else pays.

Which is why the cost-benefit page mattered: cost-benefit analysis with survey numbers is the practical
substitute, and it is a weak one. Say the loop out loud — it ties the two halves of the
chapter together.

Environmental economists call the survey method contingent valuation. Worth naming; not
worth ten minutes.""")

# ======================================= 35. Exhibits 9.14 and 9.15
figpage("Some of It Does Get Paid For Voluntarily",
        "PRIVATE PROVISION OF A PUBLIC GOOD — voluntary contributions toward a good "
        "nobody can be charged for.",
        "giving",
        "Hundreds of billions a year — and PROCYCLICAL: it fell into the 2008 recession, "
        "when the need was greatest.",
        credit="Redrawn from Exhibits 9.14 and 9.15. Left panel: selected years, as "
               "reported.")
D.notes(prs.slides[-1], """Exhibits 9.14 and 9.15. Private provision of public goods,
section 9.4.

The definition first: private provision of a public good happens when private citizens
contribute to producing or maintaining it. Free riding predicts this should barely happen.
It happens a great deal, and that is genuinely interesting.

The book's way in is the best one available: how many of you watched Sesame Street? How many
of your parents sent money to PBS? Far more watched than paid — free riding, visible in one
show — and yet the programme got made, because enough people did pay.

Left panel: total US giving rising from roughly ​$150 billion in the late 1970s to around
​$440 billion by 2018, in inflation-adjusted dollars. THE MARKERS ARE THE ONLY YEARS THE
EXHIBIT REPORTS and the publisher describes its own values as approximate; the connecting
line is a guide, not data. Do not quote a precise figure for a year that is not marked.

The teaching point is the red segment. Giving fell from roughly ​$400 billion in 2005 to
​$350 billion in 2008 — into the recession, which is exactly when the needs it funds are
greatest. That is charity's structural weakness: it is procyclical, and it is most reliable
when it is least needed.

Right panel: the share saying they donated money in the past month, 2018, by world region.
Australia and New Zealand highest at 70 per cent, North America 59, down to southern Africa
at 10. Handle this carefully — the differences reflect income, tax treatment of donations,
and how much is done through the state rather than any claim about generosity. Say so.""")

# ============================================== 36. what charity cannot do
photopage("What Charity Cannot Fix",
          "species",
          "Which of these would you rather save?",
          "Most people say the panda. Ochre sea stars are a keystone species — remove them "
          "and the whole intertidal community collapses. Pandas are charismatic. Sea stars "
          "are load-bearing.\n\n "
          "Voluntary giving allocates by what moves donors, which is not the same as "
          "allocating by where the need is greatest. Add the two problems from the last "
          "slide — the total is variable, and it falls in downturns — and private "
          "provision cannot be the whole answer.",
          "FREE RIDING under-supplies the good; donor preference MISALLOCATES what is "
          "supplied. Two separate failures.")
D.notes(prs.slides[-1], """The limits of private provision. The book's own closing move for
section 9.4.

The book's point about the images: donors support charismatic species — pandas — rather
than keystone species such as the ochre sea star, which do far more ecological work and
have no visual appeal. Ask the question before you give the answer; the room will say panda
and then be slightly embarrassed, which is the effect you want.

The three problems with relying on charity, together:
  1. The money does not go where need is greatest — it goes where attention is.
  2. The total is variable, so you cannot plan around it.
  3. It falls in downturns, precisely when the need rises. That is the red segment on the
     previous slide.

Be fair about it. None of this says charity is bad or that donors are foolish. It says
voluntary contribution has a predictable ALLOCATION problem, and that is a different claim.
Private provision is a genuine supplement. It is not a mechanism you can build a public
good on.

Connect it back once: the free-rider problem said the good would be undersupplied. This
slide says that even the part that does get supplied is supplied in the wrong proportions.
Two separate failures, stacked.""")

# ============================================================= 37. PART 5 divider
s = S()
D.divider(s, "PART 5", "Goods the Market\nUses Up")
D.notes(s, """Divider. Section 9.5, Common Pool Resource Goods.

One line, and make it the link rather than a new topic: a common pool resource is a negative
externality with the property right missing. Everything in Part 1 applies. What is new is
that there is nobody to bargain with, because nobody owns the thing.""")

# ==================================================== 38. common pool resources
photopage("Rival, and Nobody Can Be Kept Out",
          "fish",
          "Why would people who fish for a living vote for limits on their own catch?",
          "A common pool resource is rival — the fish you land is not there for anyone "
          "else — and nonexcludable, so nobody can be stopped from fishing.\n\n "
          "That combination means every boat's catch imposes a cost on every other boat, "
          "and no boat is billed for it. It is the negative externality from Part 1, with "
          "the property right missing.",
          "TRAGEDY OF THE COMMONS — OPEN ACCESS plus DEPLETION THROUGH USE. A negative "
          "externality with no owner to bargain with.",
          lead="Section 9.5 · the externality with nobody to bargain with")
D.notes(prs.slides[-1], """Common pool resources, section 9.5. Open with the question on the
slide — it looks paradoxical and it is not.

Why fishermen support catch limits: with no excludability, each boat has every incentive to
take as much as it can, because the fish it leaves will simply be taken by someone else. But
each fish taken is one that cannot breed, so the stock falls and everyone's future catch
falls with it. A binding limit that everyone must obey makes every one of them better off.
They are voting to be protected from each other, not from the government.

The book's definition to read: the externality involved with a common pool resource arises
from the combination of OPEN ACCESS and DEPLETION THROUGH USE. Both halves are needed. A
nonexcludable good that is not depleted — a lighthouse — is a public good and causes no
tragedy at all.

Say the structural link explicitly, because it is what makes Part 5 short: this is Part 1's
negative externality. One person's use imposes a cost on others who are not party to the
transaction. The reason it cannot be bargained away is card 2 from the three-conditions page — there is no
property right, so there is nobody to negotiate with and nothing to buy.

The book's Choice & Consequence boxes here are the Tragedy of the Commons and the Race to
Fish. The race-to-fish dynamic is worth a sentence: when the season is open to all, boats
compete to catch first, which drives investment into ever bigger boats and ever shorter
seasons — a pure waste of capital on top of the depletion.""")

# ================================================================ 39. the commons
figpage("A Hundred Farmers, a Hundred Cows, and One Extra Each",
        "The commons carries 100 cows. One hundred farmers with one cow each is exactly "
        "sustainable.",
        "commons",
        "Each farmer captures the whole MARGINAL PRIVATE BENEFIT and bears one hundredth "
        "of the MARGINAL SOCIAL COST.")
D.notes(prs.slides[-1], """The grazing commons, with numbers.

THIS EXAMPLE IS IMPORTED FROM THE MATEER & COPPOCK DECK (their Chapter 7, the public-good equilibrium page). Our own
book states the tragedy of the commons and names the original grazing example but never
works it with numbers. Numbers make the asymmetry visible instead of merely asserted, and
the asymmetry is the whole mechanism.

Walk it as a story, in the first person.
  The commons sustains 100 cows indefinitely. There are 100 farmers with one cow each. This
  is exactly sustainable — nothing is wrong yet.
  Now I think: what if I bring a second cow? 100 cows or 101 — the grass will not notice.
  I am right. One extra cow does no meaningful damage, and I get a whole extra cow's worth
  of milk.
  But every one of the other 99 is reasoning identically, and each of them is also right.
  Two hundred cows on land that carries one hundred. The commons is destroyed.

THE ARITHMETIC IS THE POINT AND IT IS ON THE FIGURE: I keep 100 per cent of the benefit of
my extra cow and bear 1 per cent of the cost, because the damage is spread across all 100 of
us. At that ratio adding the cow is correct for me at every level of grazing, right up to
the collapse. Compare the Coase bargain on the Coase table: there, two parties internalised the
whole gain between them. Here there are a hundred, and each internalises a hundredth.

Say the line the figure is titled with: nobody wanted this outcome and everybody chose it.
No villain, no error, no failure of information — just a structure in which individual
rationality and collective outcome come apart.

The book's own version is bison against cattle, on the next slide. Other real cases: aquifer
depletion, deforestation, traffic congestion, antibiotic resistance.""")

# ======================================= 40. property rights and the fix
s = S()
D.title(s, "Why Cattle Are Not Extinct and Bison Nearly Were")
yb = D.band(s, 1.12, "Same animal, same uses, opposite outcomes — and the only difference "
                     "was who owned them.", kind="formula", size=14)
yb = D.band(s, yb + 0.12,
            "Owned privately: maintain, protect, conserve, trade. Held in common: "
            "neglect it, and take yours first.", kind="neutral", size=12.5)
_top = yb + 0.18
D.cards3(s, _top, LIMIT - _top, [
    (GREEN, "PRIVATE OWNERSHIP", "Assign the right and the owner bears the whole cost of "
     "depletion. Ranching, fishing quotas, land titles.", IC % "house"),
    (BLUE, "REGULATION", "Cap the take. Catch limits, closed seasons, size rules — with "
     "enforcement and real penalties.", IC % "ballot-box"),
    (DGOLD, "A CHARGE FOR USE", "Price the access. A congestion charge, a grazing fee — "
     "Part 3's tax, pointed at a resource.", IC % "coin-stack"),
], body_size=10.5)
D.kicker(s, "PROPERTY RIGHTS, REGULATION or a PIGOUVIAN CHARGE — all three INTERNALISE the "
            "externality.")
D.notes(prs.slides[-1], """The book's bison-and-cattle question, and the three solutions from
the end of section 9.5.

Ask it as the book does before answering: bison and cattle were hunted for the same things —
meat and hides. Bison went to the brink of extinction and cattle never came close. Why?

The answer is not that people liked cows better. Cattle were private property: every animal
had an owner who bore the entire cost of killing it and captured the entire benefit of
keeping it alive to breed. Bison were a common pool resource: any animal you did not shoot
was one somebody else would, so the cost of taking it fell on everyone and the benefit fell
on you. The commons arithmetic, with a real species attached.

THE INCENTIVE CONTRAST IN THE SECOND BAND IS IMPORTED FROM THE MATEER & COPPOCK DECK (their
Chapter 7, slides 19 and 35). Our book states the solutions but does not lay the two
incentive sets against each other, and the contrast is what makes the mechanism memorable.
Their own test question for it is good and takes ten seconds: which do you take better care
of — your own bathroom or a public one? Your own car or the bus?

The three cards are the book's three solutions. Note what they share: each one puts the cost
of depletion back onto the person deciding. Private ownership does it by assignment,
regulation by prohibition, a charge by price. Card 3 is explicitly Part 3's Pigouvian tax
reappearing, and saying so is worth doing — the chapter has one idea in it.

The book's Alaskan king crab case is the best evidence that regulation works: stocks
stabilised under a limited season, harvest caps and male-only rules — with enforcement and
stated penalties, which is the part that is easy to leave out.

One honesty note: privatisation is not always available or acceptable. You cannot easily
assign property rights in the atmosphere, and there are resources where doing so would be
politically or ethically fraught. Do not present card 1 as the general answer.""")

# ================================================================ 41. EBE, posed
photopage("Evidence-Based Economics: The Chapter's Closing Question",
          "congestion",
          "How can the Queen of England lower her commute time to Wembley Stadium?",
          "London's traffic had become a textbook negative externality. Every driver who "
          "joined a queue slowed every other driver, and no driver was billed for it.\n\n "
          "The answer is the one Part 3 gave: if a cost is missing from a price, put it "
          "there. From 2003 London charged drivers to enter the central zone during "
          "working hours.",
          "CONGESTION is a negative externality, and the CONGESTION CHARGE is a PIGOUVIAN "
          "TAX on road use.",
          portrait=True)
D.notes(prs.slides[-1], """The chapter's headline Evidence-Based Economics question, and the
one it opens with. Pose it, then answer it on the next slide.

The question is deliberately silly and the mechanism is not. Congestion is a negative
externality of exactly the Part 1 kind: when you drive into a crowded zone you slow everyone
already in it, and nothing in the price of your journey reflects that. So too many people
drive, exactly as too much electricity was generated.

The policy: a congestion charge on vehicles entering central London during charging hours,
introduced in February 2003. It is a Pigouvian tax with a road for a tax base.

Say the connection out loud, because it is the chapter closing its own loop: this is slide
20. Same diagram, same logic, same instrument. The chapter opened with a professor lighting a
cigar in a classroom to introduce spillover costs and it ends with a city charging for one.

The photograph is the actual Central Zone signage, so students recognise it if they have
been. Portrait format, so it gets the full-height column rather than the usual half-slide
box.""")

# ============================================================ 42. Exhibit 9.16
figpage("What Happened When London Charged for the Road",
        "First full year of the charge against the last year without it, by vehicle type.",
        "congestion",
        "Car use fell about a third, with SUBSTITUTION toward taxis, buses and bicycles. "
        "A price changes behaviour.",
        credit="Redrawn from Exhibit 9.16. Category totals are approximate.")
D.notes(prs.slides[-1], """Exhibit 9.16. The answer, and a good last figure.

The headline number: car use in the charging zone fell by roughly a third between 2002, the
last year without the charge, and 2003, the first year with it.

The pattern matters more than any single bar. Cars fell. Taxis, buses, motorcycles and
bicycles all rose. That is not people giving up travel — it is people substituting toward
modes that were exempt or cheaper. Which is exactly what a price is supposed to do, and it
is the same substitution logic from Chapter 5. A tax does not simply reduce activity; it
redirects it.

QUOTE THE PATTERN AND THE CARS FIGURE, NOT THE INDIVIDUAL CATEGORY TOTALS. The publisher's
own accessibility description of this exhibit gives higher numbers for the smaller
categories than its own drawn bars do — motorcycles at 170 against roughly 125 drawn, buses
at 70 against roughly 45. The direction of every change is the same either way, and the cars
number agrees to within two points on either reading, so the teaching content is unaffected.
But do not put a precise figure on vans or buses. Flag it without naming the publisher if a
student asks.

If you want one honest caveat: this is a before-and-after in a single city, and 2003 differed
from 2002 in other ways too. The effect is large and consistent across categories, which is
about as convincing as a natural experiment of this kind gets, but it is not a randomised
trial. Same standard you applied to Kansas on the earthquake data page.""")

# ================================================================== 43. recap
s = S()
D.recap_table(s, "Chapter 9: The Full Picture", [
    ["Externalities", "A cost or benefit lands on somebody outside the deal, so the price "
     "is wrong.", "externality, MSC, MSB, deadweight loss", "Section 9.1 · Exhibits 9.1–9.5"],
    ["Which way it fails", "Negative → the market makes too much. Positive → too little.",
     "negative and positive externality", "Section 9.1 · Exhibits 9.3, 9.5"],
    ["Private fixes", "Bargaining works if rights are clear, costs are low and parties are "
     "few.", "Coase theorem, transaction costs", "Section 9.2"],
    ["Government fixes", "Mandate the quantity, or price the harm and let firms choose.",
     "command-and-control, Pigouvian tax and subsidy", "Section 9.3 · Exhibits 9.8, 9.9"],
    ["Public goods", "Nonrival and nonexcludable, so nobody can be charged. Add demand "
     "upwards.", "free rider, nonrival, nonexcludable", "Section 9.4 · Exhibits 9.10–9.13"],
    ["Common pool", "Rival and nonexcludable, so it gets used up. Assign, regulate or "
     "charge.", "common pool resource, tragedy of the commons",
     "Section 9.5 · Exhibit 9.16"],
], "Every row is one sentence: when PRIVATE cost and benefit differ from SOCIAL cost and benefit, the price misinforms.")
D.notes(s, """Recap. Nothing new on it — the hour re-indexed so students can find things.

Read the closing line. It is the honest summary of the chapter and it is the sentence to
revise from.

Unlike Chapter 8, the right-hand column cites EXHIBIT NUMBERS as well as sections, because
this chapter was built with the publisher's own deck in hand. All sixteen exhibits are
accounted for and every number in this deck traces to one of them.

If you cut material today, leave this slide up while you say what got cut and where to read
it. The two rows most often compressed are public goods and common pool resources; both are
examinable and neither should be skipped entirely.

Point forward: this chapter showed that government CAN improve on the market outcome when
private and social costs diverge. Chapter 10 asks what happens when government acts — what
taxes actually do to a market, who really bears them, and what regulation costs. The tool
you would reach for after today is the subject of the next chapter.""")

# =============================================================== 44. takeaways
s = S()
D.takeaways_page(s, "Chapter 9: Externalities and Public Goods", [
    "EXTERNALITY — a cost or benefit falling on somebody who is not party to the "
    "transaction. The market still clears, at the wrong quantity.",
    "NEGATIVE EXTERNALITY → over-production; POSITIVE EXTERNALITY → under-production. "
    "The extra curve is always above the old one; what differs is which curve.",
    "COASE THEOREM — with clear PROPERTY RIGHTS and low TRANSACTION COSTS, the "
    "efficient action does not depend on who is liable. Only the distribution does.",
    "PIGOUVIAN TAX = MARGINAL EXTERNAL COST. It lifts the firm's private cost curve "
    "onto MARGINAL SOCIAL COST, so the firm picks the social optimum unprompted.",
    "NONEXCLUDABILITY is the deep problem: FREE RIDING when the good is NONRIVAL, "
    "TRAGEDY OF THE COMMONS when it is RIVAL.",
])
D.notes(s, """Key takeaways. The second and fourth are the examinable core.

If they remember one thing, make it the fifth. Nonexcludability is the single property
underneath both halves of the chapter: when you cannot charge people, either the good does
not get made — public goods — or it gets used up — common pool resources. Which of the two
depends only on whether the good is rival. That is the whole taxonomy in one sentence and
it is far more durable than four memorised boxes.

The third is the one students most often state wrongly. The Coase theorem is not "the
government is unnecessary". It is that the EFFICIENT ACTION does not depend on who holds
the right — only who pays does. And the conditions under which it holds are restrictive
enough that most real externalities fail them.

Close on the honest note rather than the triumphant one. This chapter showed markets
failing and government helping, after seven chapters of the opposite. Both are conditional
results, and today's version is conditional on the government knowing the size of the
external cost — which the cost-benefit page showed is exactly the thing nobody can observe.

Next: today we reached for taxes and subsidies as if they were free instruments. Chapter 10
asks what a tax actually does to a market — who bears it, what it costs beyond the revenue
it raises, and what regulation costs on top. That is The Government in the Economy:
Taxation and Regulation.""")

prs.save(OUT)
print(f"{OUT}: {len(prs.slides._sldIdLst)} slides")
