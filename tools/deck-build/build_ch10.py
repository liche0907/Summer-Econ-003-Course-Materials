#!/usr/bin/env python3
"""Build ECON003_Ch10_Taxation_and_Regulation_UCR.pptx - 23 slides, static.

SCOPE IS DELIBERATE AND NARROW, and it is his call, recorded in
`claude/lecture-scope-ch10-ch12.md`:

    COVERED   10.1.3  Taxation: Tax Incidence and Deadweight Losses   (pp. 250-256)
              10.2    Regulation                                      (pp. 256-259)
              10.3    Government Failures                             (pp. 259-262)

    NOT COVERED   10.1.1 (levels of government, who pays what) - descriptive statistics
                  10.1.2 (why government taxes and spends; progressive / proportional /
                          regressive; average vs marginal tax rate) - see the risk note
                  10.4   (equity versus efficiency) - Chapter 7 taught this already, on
                         "Equity" and "Efficient Is Not the Same as Fair"
                  10.5   (consumer sovereignty and paternalism)
                  the six-slide end-of-chapter EBE problem

This SUSPENDS ground-rules S0.3 ("include everything the book covers").  The brief is
30-40 minutes of lecture, which meant dropping 30-50% of the publisher's 70 content
slides.  Everything cut is listed in the plan doc so restoring any of it is a
re-insertion, not a rebuild.  The recap table names every section that was not lectured,
so the deck does not pretend the rest of the chapter is not in the book they are reading.

HIS CORRECTION, AND IT GOVERNS THIS WHOLE DECK:

    "They never see tax incidence before, ch9 is a wrong placement for the word."

Chapter 9 v2 printed TAX INCIDENCE as a band term on its Pigouvian tax page, and that was
a misplacement - the slide's subject was setting a tax equal to the marginal external
cost, not who bears it.  So:

  * section 10.1.3 is built as ENTIRELY NEW material, from the pre-tax equilibrium up;
  * NOTHING here says "as you saw in Chapter 9" about incidence, on a face or in a note;
  * Chapter 7 is the only safe callback.  It taught consumer surplus, producer surplus,
    deadweight loss and the price-control wedge, so DWL and the price ceiling may be
    recalled by name.

RISK CARRIED KNOWINGLY.  Section 10.1.2 holds the only computable material in the rest of
the chapter - progressive / proportional / regressive, and average versus marginal tax
rate worked at $100,000.  Bracket arithmetic is a stock multiple-choice item and the
Pearson Chapter 10 bank will be full of it.  Either exclude those items from the final's
draw, or add one slide back.  Flagged on the recap page's notes as well as here.

SOURCES.  `Slides/Pearson/Acemoglu_Micro_3e_Ch10 (1).pptx`, 75 slides, 37 media parts.
Exactly ONE usable photograph in it (the dollar bill in an Uncle Sam hat, their EBE
opener) - the count across chapters now runs 10, 4, 2, 6, 1, 6, 1.  Every figure is
redrawn in `ch10_charts.py` from the exhibits' own numbers, with each headline figure
asserted at import.

TWO PUBLISHER DEFECTS, taught corrected and flagged in the notes without naming them:
  1. Exhibits 10.13 and 10.14 both claim the other curve is "kept the same" between
     panels.  It is not - panel (b) redraws it 12.5% steeper.  Holding it genuinely
     constant reproduces every price they print and moves only the quantity, 2,000 ->
     1,750.  Teach 1,750.
  2. The price-floor slide carries no exhibit number (10.18 by sequence - INFERRED), and
     its accessibility description calls the floor a "price ceiling" and measures sugar in
     "apartments".

NO COVER IMAGE on the title slide, by instruction - as with Chapters 6, 7 and 9.  So
slide 1 has no picture shape at all, adding art later needs `insert_title_art.py` rather
than a blob swap, and `collide.py` reports slide 1 as NEAR-BLANK, which is EXPECTED.

NO EXHIBIT NUMBER IN ANY TITLE (ground rules S5 of the writing rules); provenance lives in
the 7 pt credit line.  NO SLIDE-NUMBER REFERENCE anywhere, faces or notes - notes cite
slide TITLES, which survive his renumbering.

STATIC, by rule.  Run the animation pass only after his edits settle.
"""
import os

from pptx import Presentation

import deckkit as D
from deckkit import (BLUE, GOLD, DGOLD, GREEN, RED, INK, INK2, GREY, RULE, WHITE,
                     TINT_BLUE, TINT_NEUTRAL, TINT_RED, TINT_GREEN, TINT_GOLD)

SRC = "/mnt/user-data/uploads/ECON003_26S/Slides/ECON003_Ch08_Trade_UCR_v2.pptx"
OUT = "ECON003_Ch10_Taxation_and_Regulation_UCR.pptx"
F = "figs/ch10_fig_%s.png"
P = "photos/ch10_photo_%s.png"
IC = "icons/%s.png"

LIMIT = 4.40          # the kicker rule's y on a card page
FIG_FLOOR = 4.42      # figure pages carry no card row

prs = Presentation(SRC)
D.drop_slides_after(prs, 1)
s1 = prs.slides[0]
for _sh in list(s1.shapes):
    if _sh.shape_type == 13:                      # no cover image, by instruction
        _sh._element.getparent().remove(_sh._element)
D.retitle_title_slide(s1, ["Chapter 10", "Taxation and Regulation"],
                      ["ECON 003", "UC Riverside · Summer 2026"])
D.notes(s1, """Title.

Chapter 10, Taxation and Regulation. Say at the top what this hour is and is not.

It is one question, asked properly for the first time in this course: WHEN THE GOVERNMENT
PUTS A TAX ON SOMETHING, WHO ACTUALLY PAYS IT? Then two shorter movements - what price
controls do, and the ways government intervention goes wrong on its own terms.

It is not the whole chapter. The book's sections on the size and structure of US
government, on progressive versus regressive tax systems, on equity versus efficiency and
on paternalism are in their reading and are not in this lecture. Tell them that once, at
the start, plainly - the recap page at the end lists them again. Students who are reading
along will notice, and it is better coming from you.

Do NOT say "you already know tax incidence from Chapter 9." They do not. Chapter 9 used a
tax as an instrument for fixing an externality and never asked who hands over the money.
Everything today is new.

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
    """Half-slide feature photograph, the posed question set large beside it.

    The question is its OWN text box at 15 pt and the body its own at 11.5 pt - ground
    rules S1: never two point sizes in one box.
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
    """A worked multiple-choice item: stem, options, answer, reason - answer ON the slide.

    These are worked tables, not pause-and-think prompts.  An exam-practice page must test
    something the previous page does not already answer.
    """
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


# ==================================================================== 2. where we left off
s = S()
D.title(s, "Where We Left Off")
yb = D.band(s, 1.12, "Chapter 9 used a tax as an INSTRUMENT. It never asked who "
                     "hands over the money.", kind="formula", size=14)
D.cards3(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (GREEN, "CHAPTER 7 GAVE US THE TOOLS", "CONSUMER SURPLUS, PRODUCER SURPLUS and "
     "DEADWEIGHT LOSS. Every area on today's diagrams is one of those three.",
     IC % "balance-scale"),
    (BLUE, "CHAPTER 9 SET A TAX EQUAL TO HARM", "A PIGOUVIAN TAX of exactly the MARGINAL "
     "EXTERNAL COST moves the market to the social optimum. That was the tax's SIZE.",
     IC % "factory"),
    (RED, "TODAY: WHO BEARS IT", "TAX INCIDENCE is a different question from the tax "
     "rate. The law names who writes the cheque. It does not decide who is poorer.",
     IC % "receipt"),
], body_size=11.5)
D.kicker(s, "STATUTORY INCIDENCE is who remits the tax. ECONOMIC INCIDENCE is whose "
            "income falls. They are almost never the same people.")
D.notes(s, """Opening. Two minutes, no more.

Say the debt this chapter collects. Chapter 7 built the surplus apparatus and showed what
a price control destroys. Chapter 9 reached for taxes and subsidies as if they were free
instruments - a tax of exactly the marginal external cost, and the market lands on the
optimum. Neither chapter asked the question this one is about.

BE EXPLICIT THAT INCIDENCE IS NEW. Do not say "you saw this in Chapter 9". You did not
teach it there; the word appeared on a slide about the SIZE of a Pigouvian tax, and the
students have no working picture of a tax wedge. Build it from scratch today.

The distinction on the kicker is the spine of the first half and it is worth saying twice
in different words: the law can say the SELLER remits the money, and the seller can still
end up bearing almost none of it. Whether that happens is not a legal question at all - it
is a question about elasticity, and the second half of Part 1 answers it.

Name today's scope out loud. Three sections: who pays a tax, what price controls do, and
what goes wrong when government intervenes. The rest of Chapter 10 is reading.""")

# ============================================================================ 3. roadmap
s = S()
D.title(s, "Three Questions, One Hour")
yb = D.band(s, 1.12, "A TAX and a PRICE CONTROL are both WEDGES: they stop trades that "
                     "both sides wanted to make.", kind="formula", size=13.5)
D.strip5(s, yb + 0.34, [
    ("Who bears the\nburden of a tax", IC % "receipt"),
    ("Does it matter who\nthe law taxes?", IC % "balance-scale"),
    ("What decides\nthe split", IC % "up-down"),
    ("What price\ncontrols do", IC % "house"),
    ("Where government\nitself goes wrong", IC % "ballot-box"),
], label_size=10.5)
D.band(s, 3.34, "Sections 10.1.3 → 10.2 → 10.3:   TAX INCIDENCE and DEADWEIGHT LOSS · "
                "REGULATION · GOVERNMENT FAILURE", kind="neutral", size=12.5)
D.kicker(s, "Every diagram today has the same shape: a WEDGE between what buyers pay and "
            "what sellers keep, and a quantity that falls.")
D.notes(s, """Roadmap. Read the top band aloud - it is the whole hour in one sentence.

The unifying idea is worth naming before any diagram appears, because it is what makes
the second half feel like the same lecture as the first. A per-unit tax puts a wedge
between the price a buyer pays and the price a seller receives. A price ceiling or floor
does something related: it stops the price from clearing the market, so quantity falls
and trades that both sides wanted do not happen. In both cases the quantity traded falls
below the efficient one, and the loss is a triangle.

The five markers are the beats, not five sections. The first three are all section 10.1.3
and they are where most of the hour goes.

If you are running long, the section that compresses is the last one - government failure
is three named ideas with no arithmetic. Parts 1 and 2 do not compress; the wedge diagram
has to be built slowly the first time.""")

# ================================================================== 4. PART 1 divider
s = S()
D.divider(s, "PART 1", "Who Actually Pays\na Tax")
D.notes(s, """Divider. Section 10.1.3, tax incidence.

Set the question before the diagram. A restaurant tax of two dollars a plate: the
restaurant remits it, so the restaurant pays it - true or false? Almost every student says
true, and almost every student is wrong, and the diagram is how you show it rather than
assert it.

The running example is the book's own: jambalaya, two dollars a plate. Keep it - the
numbers on every figure in this part are the book's, so a student revising from the
textbook sees the same market.""")

# =================================================================== 5. tax incidence
photopage(
    "The Law Names a Payer. It Does Not Choose One.",
    "dollar",
    "A $2 tax on every plate of jambalaya. The restaurant remits it. So the restaurant "
    "pays it — yes?",
    "TAX INCIDENCE — who actually bears the burden of a tax, measured by whose income "
    "falls, not by whose name is on the payment.\n\n"
    "STATUTORY INCIDENCE is a legal fact: the statute names a remitter. ECONOMIC "
    "INCIDENCE is an economic outcome, and the market settles it.\n\n"
    "The restaurant will try to pass the tax on by raising the menu price. Whether it "
    "can, and by how much, is what the next four pages work out — and the answer turns "
    "out to have nothing to do with the wording of the law.",
    "The question is not WHO REMITS. The question is WHOSE PRICE CHANGES — and both "
    "prices change.")
D.notes(prs.slides[-1], """Tax incidence, defined.

Put the two terms up and keep them up: STATUTORY INCIDENCE and ECONOMIC INCIDENCE. They
are the vocabulary for the whole part and exam questions use both.

Read the definition off the slide, then make it concrete with something outside the
textbook so they hear it twice. Payroll tax is the best one and it comes back as the
first Exam Check: the law splits it half and half between employer and employee, and
essentially no economist thinks the burden splits half and half.

Ask the posed question and let them answer before you draw anything. Most rooms say the
restaurant pays. Some say the customer. The honest answer is BOTH, in proportions the law
has no say over, and that is a more interesting result than either guess.

The photograph is the publisher's own. The 7 pt credit line at the bottom right is the
only attribution on the page, by rule.""")

# ============================================================= 6. Exhibit 10.11 (a)(b)
figpage("A Tax on Sellers Shifts Supply Up by Exactly the Tax",
        "The market clears at 4,000 plates and $6.50. A $2 TAX raises every seller's "
        "required price by $2.",
        "tax_prod_shift",
        "Quantity falls 4,000 → 2,500. Buyers pay $7.50 and sellers keep $5.50 — the "
        "TAX WEDGE is $2 and both prices move.",
        credit="Market drawn to Acemoglu, Laibson & List, Microeconomics 3e, ch. 10")
D.notes(prs.slides[-1], """The first tax diagram. Build it slowly - this is the page the
rest of the hour stands on.

Numbers to say exactly, and they are all the book's:
  pre-tax    4,000 plates a day at $6.50
  after      2,500 plates; buyers pay $7.50, sellers keep $5.50
  the tax    $2, and 7.50 minus 5.50 is exactly 2

WHY THE CURVE MOVES UP BY EXACTLY THE TAX. A supply curve says what price a seller needs
to be willing to supply a given quantity. If the seller must now hand $2 of that price to
the government, the price they need goes up by $2, at every quantity. So the shift is
vertical and it is the size of the tax, not more and not less. Students who have only ever
been told "taxes shift supply left" cannot tell you HOW FAR, and the how-far is the whole
calculation.

THEN THE PART THEY WILL GET WRONG. The price rose by ONE dollar, not two. Ask why out loud
before you answer it. The reason is that the higher price chokes off quantity, and at the
lower quantity sellers are willing to accept less - so they absorb the other dollar. If
the seller could pass the whole $2 on, they would have to sell to buyers who are no longer
there.

Panel (a) also re-labels consumer and producer surplus. That is a Chapter 7 callback and
it is safe to make - they built those triangles there.

Point at the two hollow markers and say what they are: buyers' price and sellers' price at
the SAME quantity. A tax makes one market have two prices. That is the wedge.""")

# ============================================================= 7. Exhibit 10.11 (c)
figpage("Where the $2 Goes, and the Part Nobody Gets",
        "TAX REVENUE = tax × post-tax quantity. DEADWEIGHT LOSS = the trades the wedge "
        "prevented.",
        "tax_prod_split",
        "TAX REVENUE $5,000 a day. DEADWEIGHT LOSS $1,500 a day — value destroyed, not "
        "transferred, and nobody collects it.",
        credit="Market drawn to Acemoglu, Laibson & List, Microeconomics 3e, ch. 10")
D.notes(prs.slides[-1], """The welfare page. Three areas, and the difference between two of
them is the examinable idea.

The arithmetic, all of it worth saying aloud:
  tax revenue      $2 x 2,500 = $5,000 a day, split $2,500 from buyers and $2,500 from
                   sellers because each price moved by $1
  deadweight loss  one half x $2 x 1,500 = $1,500 a day
  the base of that triangle is the quantity that DISAPPEARED, 4,000 minus 2,500

THE DISTINCTION TO HAMMER. Tax revenue is a TRANSFER - somebody lost it and the government
got it, and every dollar is still in the economy. Deadweight loss is DESTROYED. There are
1,500 plates a day that a buyer valued above what a seller would have accepted, and they
are simply not made. No one is holding that value. This is the same distinction Chapter 7
made about price controls, and it is worth saying that explicitly - it is one of the very
few things they can carry across from that chapter today.

The error students make here, by name: computing deadweight loss on the PRE-tax quantity,
or using the whole price change rather than the tax. The triangle's height is the tax and
its base is the CHANGE in quantity. Say the formula in the form the exam asks for: one
half times the tax times the fall in quantity.

If someone asks whether the deadweight loss means taxes are bad - the honest answer is
that it means taxes are costly, which is not the same thing, and that the chapter's own
closing question is exactly how to weigh that cost against what the revenue buys.""")

# ================================================================== 8. PART 2 divider
s = S()
D.divider(s, "PART 2", "Does It Matter Who\nthe Law Taxes?")
D.notes(s, """Divider. Still section 10.1.3, and this is the chapter's cleanest result.

Pose it as a policy question, because that is how it arrives in the world. A legislature
that wants to spare consumers writes the tax onto sellers. Does that work?

Answer it with the diagram rather than with an assertion. The next two pages run the SAME
$2 tax the other way round and every number comes out identical.""")

# ============================================================= 9. Exhibit 10.12
figpage("The Same $2, Collected From Buyers Instead",
        "A tax on buyers shifts DEMAND down by the tax — what sellers may charge falls "
        "by $2 at every quantity.",
        "tax_cons",
        "2,500 plates. Buyers pay $7.50. Sellers keep $5.50 — identical. The TAX WEDGE "
        "does not care which side of it the law stands on.",
        credit="Market drawn to Acemoglu, Laibson & List, Microeconomics 3e, ch. 10")
D.notes(prs.slides[-1], """The equivalence, drawn.

Say what shifts and why. A demand curve says the most a buyer will pay. If the buyer must
hand $2 to the government on top of the menu price, the most they will pay the RESTAURANT
falls by $2, at every quantity. So demand shifts DOWN by exactly the tax - the mirror of
what supply did.

Then read the numbers off and let the repetition do the work:
  quantity        2,500. The same.
  buyers pay      $5.50 to the restaurant plus $2 to the government, so $7.50. The same.
  sellers keep    $5.50. The same.
  revenue         $5,000. Deadweight loss $1,500. The same.

The line to say slowly: the market does not read the statute. It responds to the wedge,
and a $2 wedge is a $2 wedge.

A student will ask whether this means it genuinely does not matter who is taxed. In this
model, correct - it does not. In practice it can matter for collection costs, evasion and
who NOTICES the tax, and it is worth naming those as reasons outside the model rather than
pretending the model settles everything. That is a good place to stop, not a place to go
into detail.""")

# ================================================================ 10. the two together
s = S()
D.title(s, "Two Taxes, One Outcome")
yb = D.band(s, 1.10, "STATUTORY INCIDENCE is a legal fact. ECONOMIC INCIDENCE is a "
                     "market outcome.", kind="formula", size=13.5)
# height driven off the band's own bottom - a band that wraps must not push the table
# through the kicker rule (ground rules S3)
D.table(s, 0.60, yb + 0.16, 8.80, 4.38 - (yb + 0.16), [
    ["", "Tax collected from SELLERS", "Tax collected from BUYERS"],
    ["Which curve moves", "Supply, UP by $2", "Demand, DOWN by $2"],
    ["Quantity traded", "2,500 plates", "2,500 plates"],
    ["Buyers pay", "$7.50", "$7.50"],
    ["Sellers keep", "$5.50", "$5.50"],
    ["Tax revenue", "$5,000 a day", "$5,000 a day"],
    ["Deadweight loss", "$1,500 a day", "$1,500 a day"],
], col_w=[2.30, 3.25, 3.25], first_col_fill=BLUE, header_size=10.5, body_size=10.5,
    align=["l", "ctr", "ctr"])
D.kicker(s, "Read DOWN either column and the answer is the same. A $2 WEDGE is a $2 "
            "WEDGE, whoever the statute names.")
D.notes(s, """The equivalence as a table, because this is the form an exam question takes.

Do not read every cell. Read the two outer columns for ONE row - buyers pay - and then say
that every remaining row is the same story.

WHY THIS TABLE EXISTS RATHER THAN A THIRD DIAGRAM. Multiple-choice items on this material
almost always give you a scenario and four candidate outcomes, and the winning strategy is
to know that the statutory side is irrelevant. A student who has this table can answer
without redrawing anything.

The one row that is NOT identical, and it is worth pre-empting because a sharp student
will raise it: the posted price differs. Under a seller-side tax the menu says $7.50 and
the customer hands over $7.50. Under a buyer-side tax the menu says $5.50 and the customer
hands over $5.50 plus $2 at the till. The economics is identical; what the customer SEES
is not. That is a real difference and it is a behavioural one, outside this model. Sales
tax in the United States works the second way, which is why the number on the shelf is
never the number you pay.

Say the kicker as the takeaway line and move on - the next part is where the split comes
from.""")

# ============================================================== 11. Exam Check 1
s = S()
D.title(s, "Exam Check: Who Really Pays the Payroll Tax?")
examcheck(s, 1.12, [
    ("A payroll tax is levied half on employers, half on employees. Labour SUPPLY is "
     "the less elastic side. Who bears most of it?",
     "A.  Employers — the law names them for half\n"
     "B.  Exactly 50/50, because the statute says so\n"
     "C.  Workers — labour SUPPLY is the inelastic side\n"
     "D.  Neither; a tax on a factor has no incidence",
     "C",
     "STATUTORY INCIDENCE is 50/50. ECONOMIC INCIDENCE follows ELASTICITY, and the "
     "inelastic side bears more. Workers change hours far less than firms change hiring."),
    ("A $3 per-unit tax cuts quantity from 900 to 700. The buyer's price rises from $20 "
     "to $22. What is the DEADWEIGHT LOSS?",
     "A.  $2,100                 B.  $600\n"
     "C.  $300                    D.  $400",
     "C",
     "Half x tax x the FALL in quantity: 0.5 x 3 x 200 = $300. Tax revenue is the other "
     "figure — 3 x 700 = $2,100 — and it is a TRANSFER, not a loss."),
])
D.notes(s, """Two worked items. Both answers are on the slide - read the stem, pause a
beat, then read the answer panel. Do not leave silence on a recording.

ITEM 1 is the payroll tax, and it is the single most examined application of incidence
there is. The point to make out loud: the statute is a fact about paperwork. Labour supply
is famously inelastic - most people cannot much vary how many hours they work in response
to a small change in take-home pay - so workers carry the great majority of the burden,
and the empirical literature is fairly settled on that. Distractor D is the one worth
naming as wrong: every tax has an incidence, including a tax on a factor.

ITEM 2 is pure arithmetic and it is where marks are actually lost. Two traps, both worth
naming:
  - using the PRE-tax quantity, 900, as the base of the triangle. The base is the FALL,
    200.
  - using the price change, $2, as the height. The height is the TAX, $3. The $2 is only
    the buyers' share of it.
Distractor A is the tax revenue, which is what a student computes if they answer the wrong
question, and it is the most attractive wrong answer on the page.

If you want one line to leave them with: revenue uses the quantity that SURVIVES, the
triangle uses the quantity that DIED.""")

# ================================================================= 12. PART 3 divider
s = S()
D.divider(s, "PART 3", "What Decides\nthe Split")
D.notes(s, """Divider. The end of section 10.1.3, and the part that generalises.

Frame it as the question the last two parts left open. The law does not decide the split.
Something does. It is ELASTICITY, and the rule is one sentence long.

Warn them that the two figures coming up look almost the same and are not - one flattens
supply, the other flattens demand, and the burden moves in opposite directions.""")

# ============================================================= 13. Exhibit 10.13
figpage("Make Supply More Elastic and Buyers Pay More",
        "Sellers who can walk away easily do. The side that can ESCAPE the tax escapes "
        "it, and the other side absorbs it.",
        "elast_supply",
        "ELASTIC SUPPLY → burden on BUYERS: $1.50 of the $2, against $0.50 for sellers.",
        credit="Panel (b) drawn holding DEMAND genuinely constant — see speaker notes")
D.notes(prs.slides[-1], """First elasticity figure. Say the mechanism, not just the result.

Panel (a) is the market you already know: both sides equally elastic, the tax splits
evenly at a dollar each.

Panel (b) makes SUPPLY flatter - three times as elastic. A flat supply curve means sellers
are very willing to leave this market: at a slightly lower net price, a lot of them stop
producing. So they refuse to absorb much of the tax. The quantity falls further, and
buyers end up paying $8.00 while sellers keep $6.00 - a $1.50 / $0.50 split.

THE INTUITION TO SAY IN PLAIN WORDS: elasticity is a measure of having somewhere else to
go. Whoever has somewhere else to go pays less of the tax. Whoever is stuck pays more.
That single sentence answers most exam questions on this topic.

A NUMBER THAT DIFFERS FROM THE BOOK, and say it if anyone is reading along. Their panel
(b) prints a post-tax quantity of 2,000. Their own figure quietly redraws the demand curve
about 12% steeper between the two panels, so the comparison is not holding demand
constant. Holding demand genuinely constant - which is what the exhibit is FOR - gives
1,750. Every price on our figure is theirs: $6.50, $8.00, $6.00, and the $1.50 / $0.50
split. Only the quantity moves. If a homework item uses 2,000, it is using their drawing;
the prices and the split are what matter and those agree.

Do not name the publisher out loud. "The textbook figure" is enough.""")

# ============================================================= 14. Exhibit 10.14
figpage("Make Demand More Elastic and Sellers Pay More",
        "Now BUYERS are the side with somewhere else to go — and the ELASTICITY of "
        "demand turns the burden right round.",
        "elast_demand",
        "THE RULE: the burden falls on the LESS ELASTIC side. Elastic demand → sellers "
        "bear $1.50 of the $2.",
        credit="Panel (b) drawn holding SUPPLY genuinely constant — see speaker notes")
D.notes(prs.slides[-1], """Second elasticity figure, and the general rule.

Same construction, other side. Demand is flattened threefold; buyers now abandon the
market at the smallest price rise, so sellers cannot pass the tax on. Buyers pay $7.00,
sellers keep $5.00 - the mirror image of the previous page, $0.50 / $1.50.

STATE THE RULE IN THE FORM THE EXAM USES, and it is the kicker: the tax burden falls more
heavily on the side of the market that is LESS elastic - less responsive to price. Say the
contrapositive too, because half the questions are worded that way: the burden falls LESS
heavily on the more elastic side.

Two applications that make it stick, both worth thirty seconds:
  - cigarettes. Demand is highly inelastic, supply is not. Tobacco taxes are borne
    overwhelmingly by smokers, which is precisely why they raise so much revenue and
    reduce quantity so little.
  - a tax on land. Supply is perfectly inelastic, so landowners bear all of it and the
    deadweight loss is zero. That is a famous result and it is the limiting case of this
    page.

Same correction as the previous figure applies here: their panel (b) redraws supply
slightly steeper, and holding it constant gives 1,750 rather than 2,000. Every price is
theirs.""")

# ================================================================= 15. DWL and elasticity
figpage("The More Elastic the Market, the More the Tax Destroys",
        "Elasticity does two things at once: it moves the BURDEN, and it enlarges the "
        "DEADWEIGHT LOSS.",
        "dwl_elasticity",
        "Same $2 tax, same revenue per plate — DEADWEIGHT LOSS rises $1,500 → $2,250 "
        "because more trades disappear.")
D.notes(prs.slides[-1], """The page that ties incidence to efficiency. Short, and it is the
one that gets used in policy arguments.

The comparison: the same $2 tax in two markets. In the flexible market quantity falls from
4,000 to 1,750 rather than to 2,500, and the deadweight loss grows from $1,500 to $2,250 -
half again as large.

THE MECHANISM, said plainly: deadweight loss is made of trades that did not happen. The
more easily either side can walk away, the more trades the wedge prevents, and the bigger
the triangle. Elasticity IS the willingness to walk away.

THE POLICY COROLLARY, and it is the reason this matters beyond the exam: if a government
wants revenue with the least damage, it taxes inelastic things. That is a genuine
principle - the Ramsey rule, though you need not name it - and it explains why real tax
systems lean on tobacco, alcohol, fuel, and property. Then say the uncomfortable half out
loud, because a student will think it: the same logic says tax necessities rather than
luxuries, which is efficient and regressive at the same time. The book handles that
trade-off in the section on equity versus efficiency, which is in their reading. Name it
and leave it there - do not open it.

One honest caveat if it comes up: this is all partial equilibrium and it assumes the tax
is small enough that the curves are locally linear. Fine at this level; say so if asked
rather than overclaiming.""")

# ============================================================== 16. Exam Check 2
s = S()
D.title(s, "Exam Check: Read the Split Off the Numbers")
examcheck(s, 1.12, [
    ("A market clears at $10. After a per-unit tax buyers pay $13 and sellers keep $9. "
     "What is the tax, and how does it split?",
     "A.  Tax $3; buyers $3, sellers $0\n"
     "B.  Tax $4; buyers $3, sellers $1\n"
     "C.  Tax $4; buyers $1, sellers $3\n"
     "D.  Tax $13; buyers $13, sellers $9",
     "B",
     "The TAX WEDGE is the gap between the two prices: 13 − 9 = $4. Each side's share is "
     "measured from the ORIGINAL price of $10, so buyers $3 and sellers $1."),
    ("In that same market, which MUST be true?",
     "A.  Demand is more elastic than supply\n"
     "B.  Supply is more elastic than demand\n"
     "C.  Both sides are perfectly inelastic\n"
     "D.  The tax was collected from sellers",
     "B",
     "Buyers bear the larger share, so buyers are the LESS elastic side and SUPPLY is the "
     "more elastic one. D is unknowable — and irrelevant, which is the point."),
])
D.notes(s, """Two items, and together they are the whole of Part 1 in exam form.

ITEM 1 tests the mechanics. Two things to say:
  - the tax is the GAP between the two post-tax prices, not either price on its own. If
    they can find $13 minus $9 they have the tax.
  - each side's share is measured from the ORIGINAL equilibrium price. Buyers went from
    $10 to $13, so $3. Sellers went from $10 to $9, so $1. And $3 plus $1 is $4, which is
    the check.
Distractor A is what you get if you forget the seller's price moved at all - the single
most common error on this material.

ITEM 2 runs the rule backwards, which is the harder direction and the one that separates
grades. Buyers bore three quarters of it, so buyers are the stuck side, so demand is the
inelastic one and supply is the elastic one. Students reliably invert this. Give them the
sentence to hold: THE SIDE THAT PAYS MORE IS THE SIDE THAT COULD NOT LEAVE.

Distractor D is there on purpose and deserves a comment: the question of who the statute
named is not answerable from the numbers, because it makes no difference to any of them.
That is the equivalence result from Part 2, tested by omission.""")

# ================================================================= 17. PART 4 divider
s = S()
D.divider(s, "PART 4", "Regulation, and Where\nIt Goes Wrong")
D.notes(s, """Divider. Sections 10.2 and 10.3 together - the shorter half of the hour.

Two moves. First, the other instrument: government can regulate the amount of an activity
directly, or control its price. Second, the honest accounting - intervention has costs of
its own that are not on any diagram.

Tell them the price-control material is a return visit. Chapter 7 built the price-ceiling
diagram in detail; today it is one page of recall plus one thing that chapter did not
show. That is deliberate and it is why this part is short.""")

# ============================================================ 18. two kinds of regulation
s = S()
D.title(s, "Two Ways to Intervene Without Taxing")
yb = D.band(s, 1.12, "REGULATION — government action aimed at the quantity, price, "
                     "quality or safety of what is traded.", kind="formula", size=14)
D.cards2(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (BLUE, "DIRECT REGULATION", "Also called COMMAND-AND-CONTROL: the government sets the "
     "AMOUNT of an activity rather than its price. Emissions caps, drug approval, vehicle "
     "standards, licensing. Chapter 9's Oklahoma injection-volume order was exactly this. "
     "The FDA is the standing example — roughly 9,000 staff and about $2 billion a year, "
     "and the complaint against it is slowness, which is itself a cost.",
     IC % "ballot-box"),
    (RED, "PRICE CONTROLS", "The government sets the PRICE instead. A PRICE CEILING is a "
     "legal maximum and it bites only BELOW the market price. A PRICE FLOOR is a legal "
     "minimum and it bites only ABOVE it. A control set on the wrong side of the market "
     "price does nothing at all — which sounds trivial and is the single most examined "
     "point in the section.",
     IC % "price-tag"),
], body_size=11.5)
D.kicker(s, "A tax changes the PRICE and lets the market pick the quantity. DIRECT "
            "REGULATION picks the quantity. A PRICE CONTROL picks the price and lets "
            "neither clear.")
D.notes(s, """The taxonomy page. Two named instruments, and one comparison worth making.

DIRECT REGULATION is genuinely new vocabulary even though they have seen an instance of
it: Chapter 9's Kansas and Oklahoma injection-volume orders were command-and-control, and
you can say so - that callback is safe, it was taught. The FDA figures are the book's own
and are fine to quote: about 9,000 employees, about $2 billion a year. The interesting
part is that the standard criticism of the FDA is that it is SLOW, and slowness is a real
economic cost that never appears on a supply-and-demand diagram. That sets up section 10.3
directly, so make the link.

PRICE CONTROLS is mostly recall. What is worth spending time on is the "which side" point
on the card, because it is where marks go: a ceiling above the market price and a floor
below it are both completely inert. Students memorise "ceilings cause shortages" and then
answer that a ceiling of $50 in a market clearing at $30 causes a shortage. It causes
nothing.

The kicker is the comparison that makes the three instruments one family, and it is worth
saying slowly. A tax moves the price and lets quantity adjust. Direct regulation fixes the
quantity. A price control fixes the price and prevents the market from clearing at all -
which is why it, uniquely, produces a shortage or a surplus rather than just a smaller
market.""")

# ========================================================== 19. ceiling and floor
figpage("A Ceiling Makes a Shortage. A Floor Makes a Surplus.",
        "A PRICE CEILING bites BELOW the market price; a PRICE FLOOR bites ABOVE it. "
        "Either way the SHORT SIDE decides what trades.",
        "ceiling_floor",
        "Rent capped at $750: 5,500 wanted, 2,500 offered, SHORTAGE 3,000. Sugar floored "
        "at $16: 150 offered, 60 wanted, SURPLUS 90.",
        credit="Markets drawn to Acemoglu, Laibson & List, Microeconomics 3e, ch. 10")
D.notes(prs.slides[-1], """The price-control page. This is recall, so move at pace - Chapter
7 built this diagram from scratch and they have seen the deadweight-loss triangle before.

The numbers, both the book's:
  apartments   clears at 4,000 units and $1,200. Ceiling at $750: 2,500 supplied, 5,500
               demanded, shortage 3,000.
  sugar        clears at 100 tons and $9. Floor at $16: 150 supplied, 60 demanded,
               surplus 90 tons.

THE SHORT-SIDE RULE is the one idea to state explicitly, because it explains both panels
with one sentence: exchange is voluntary, so the quantity actually traded is the SMALLER
of what is offered and what is wanted. Under the ceiling that is supply, 2,500. Under the
floor it is demand, 60. Nobody can be forced to trade.

Two things worth saying that the diagram does not:
  - Under rent control, consumer surplus can RISE. The 2,500 tenants who get an apartment
    pay $750 for something they valued at up to $1,650. The people who lose are landlords
    and the 3,000 households with no apartment, and the second group is invisible on the
    diagram. If the tenants who keep apartments are the households the policy meant to
    help, the policy can be defended - that is the book's own argument and it is a fair
    one. Say it; do not sneer at rent control.
  - Under a floor, somebody has to deal with the surplus. Governments typically buy it -
    for foreign aid, storage, or destruction - which is a further cost on top of the
    triangle.

The shading on the left panel is the deadweight loss; name it and move on, they know it.""")

# ============================================================== 20. Exhibit 10.17
figpage("A Ceiling Only Bites If the Market Is Above It",
        "The regulation did not change. The MARKET moved under it — and the CEILING "
        "stopped doing anything.",
        "rent_shift",
        "Demand falls, rent would clear at $600, and a $750 ceiling is now ABOVE the "
        "market price: NO SHORTAGE, no DEADWEIGHT LOSS, no effect at all.",
        credit="Market drawn to Acemoglu, Laibson & List, Microeconomics 3e, ch. 10")
D.notes(prs.slides[-1], """The one genuinely new thing in this section, and the reason the
section is here at all. Chapter 7 never drew this.

The story: the rent ceiling stays at $750. Demand for apartments falls - a factory closes,
the population shrinks, a university cuts enrolment. The market would now clear at 2,000
apartments and $600. The ceiling is at $750, which is ABOVE $600, so it is not binding. No
shortage. No queue. No deadweight loss. The law is still on the books and it does nothing.

TWO TERMS TO USE: a control is BINDING or NON-BINDING. Exam questions use those words and
students who have only met "ceiling causes shortage" have no way to answer them.

The general statement, which is what to leave them with: a price ceiling has an effect
only when it is set BELOW the equilibrium price, and a price floor only when it is set
ABOVE it. Whether a given control binds is not a property of the law - it is a property of
the law AND the market together, and markets move.

Worth thirty seconds of real-world context, and it is honest rather than rhetorical: this
is why price-control laws that were controversial when passed sometimes become invisible
without ever being repealed, and why a minimum wage set in nominal terms stops binding as
wages drift up around it. Same diagram, other direction.

Do not extend this into a discussion of the minimum wage's empirical literature - it is
not in the chapter and the evidence is genuinely contested.""")

# ================================================================= 21. section 10.3
s = S()
D.title(s, "Intervention Has Costs the Diagram Does Not Show")
yb = D.band(s, 1.12, "GOVERNMENT FAILURE — inefficiency caused by the government's own "
                     "intervention.", kind="formula", size=14)
D.cards3(s, yb + 0.20, LIMIT - (yb + 0.20), [
    (BLUE, "BUREAUCRATIC COST", "More rules need more people to enforce them, and those "
     "people had another use. That is an OPPORTUNITY COST, not an accounting entry — and "
     "it is a reason to weigh a regulation, not a reason against having one.",
     IC % "ledger"),
    (DGOLD, "CORRUPTION", "Public funds diverted to private use. Not confined to "
     "government: rent control produces landlords demanding payments under the table, "
     "which is corruption generated in the PRIVATE sector by a public rule.",
     IC % "coin-stack"),
    (RED, "THE UNDERGROUND ECONOMY", "Where a control creates a shortage or a tax makes "
     "an activity expensive, trade moves off the books. BLACK MARKETS grow exactly where "
     "the wedge is biggest — the shortage from the previous page has to go somewhere.",
     IC % "up-down"),
], body_size=11)
D.kicker(s, "DEADWEIGHT LOSS is the cost the diagram shows. GOVERNMENT FAILURE is the "
            "cost it does not — and both belong on the same side of the ledger.")
D.notes(s, """Section 10.3, and the close of the lecture's argument. Two or three minutes.

The four costs the book lists are deadweight loss, bureaucratic cost, corruption and the
underground economy. The first one has had two figures already, so spend the time on the
other three.

BUREAUCRATIC COST. Frame it as opportunity cost, which is Chapter 1 vocabulary and worth
reaching back for: the enforcement staff could have been doing something else. Say the
balancing clause out loud - the book does, and it matters. This is not an argument that
regulations are bad. It is an argument that they are not free, and that the comparison is
cost against benefit rather than benefit alone.

CORRUPTION. The example to use is the one that ties back to the previous page: under rent
control, an apartment at $750 is worth $1,650 to somebody, and that $900 gap is an
incentive for a side payment. Note who is doing the corrupting there - private landlords,
responding to a public rule. Corruption is not a government-sector phenomenon; it is a
response to a wedge.

THE UNDERGROUND ECONOMY. Same logic once more, and this is the unifying observation of the
whole hour: WHEREVER THERE IS A WEDGE, SOMETHING GROWS IN IT. A tax makes off-the-books
trade profitable. A ceiling makes a black market profitable. The bigger the wedge, the
bigger the incentive.

If you want a closing line for the lecture, it is the kicker. Then stop - the equity
question the chapter goes on to ask is in their reading and it is not today's material.""")

# ================================================================== 22. the full picture
s = S()
D.recap_table(s, "Chapter 10: The Full Picture", [
    ["Who bears a tax",
     "The law names a remitter; the market decides who is poorer. Both prices move.",
     "TAX INCIDENCE, STATUTORY vs ECONOMIC",
     "§10.1.3 · the $2 jambalaya tax"],
    ["It does not matter who is taxed",
     "Tax the seller or tax the buyer: same quantity, same two prices, same revenue.",
     "TAX WEDGE",
     "§10.1.3 · the two-column table"],
    ["What decides the split",
     "The burden falls on the LESS elastic side — whoever cannot walk away.",
     "ELASTICITY, INCIDENCE",
     "§10.1.3 · the two elasticity figures"],
    ["What a tax costs",
     "Revenue is transferred; the triangle is destroyed. Both grow with elasticity.",
     "DEADWEIGHT LOSS, TRANSFER",
     "§10.1.3 · ½ × tax × fall in Q"],
    ["Regulation",
     "Direct limits, or price controls that bind only on one side of the market.",
     "COMMAND-AND-CONTROL, CEILING, FLOOR, BINDING",
     "§10.2 · rent and sugar"],
    ["Government failure",
     "Bureaucracy, corruption and black markets are costs no supply diagram shows.",
     "GOVERNMENT FAILURE",
     "§10.3"],
], "Not lectured, and in your reading: §10.1.1 and §10.1.2 (what government taxes and "
   "spends, progressive / proportional / regressive, average vs marginal tax rate), "
   "§10.4 (equity vs efficiency) and §10.5 (consumer sovereignty and paternalism).")
D.notes(s, """Recap. Read the row labels, not the cells.

SAY THE CLOSING LINE OUT LOUD AND DO NOT SKIP IT. Four parts of this chapter were not
lectured and they are in the assigned reading. Students find out either from you or from a
homework question, and the first is much better.

Point them specifically at 10.1.2 if they want something concrete to study on their own:
progressive, proportional and regressive tax systems, and the difference between an
AVERAGE and a MARGINAL tax rate worked through the federal brackets. It is the only part
of the unlectured material with arithmetic in it, and arithmetic is what gets examined.

A NOTE FOR WHOEVER PREPARES THE ASSESSMENTS, not for delivery. The MyLab assignment for
this chapter and the Chapter 10 question bank both draw on sections this lecture does not
cover, 10.1.2 above all - bracket arithmetic is a stock multiple-choice item. Either
restrict the item selection to the sections taught, or add the average-versus-marginal
slide back. That decision should be deliberate rather than discovered.

Section 10.4 is worth one sentence if anyone asks why it is missing: Chapter 7 already
made the equity-versus-efficiency argument, on the pages titled "Equity" and "Efficient Is
Not the Same as Fair".""")

# ==================================================================== 23. key takeaways
s = S()
D.takeaways_page(s, "Chapter 10: Taxation and Regulation", [
    "TAX INCIDENCE — the law names who remits a tax; the market decides whose income "
    "falls. They are rarely the same.",
    "THE TAX WEDGE — tax the buyer or tax the seller and every number is identical: same "
    "quantity, same two prices, same revenue.",
    "ELASTICITY DECIDES — the burden falls on the side that cannot walk away, and the "
    "more elastic the market the more trade the tax destroys.",
    "DEADWEIGHT LOSS — revenue is transferred, the triangle is destroyed: ½ × tax × the "
    "FALL in quantity.",
    "BINDING OR NOT — a CEILING acts only below the market price and a FLOOR only above "
    "it, and GOVERNMENT FAILURE is the cost no diagram shows.",
])
D.notes(s, """Key takeaways. Five lines, one per idea, each opening with its term.

Read them. Do not paraphrase - these are the retrieval keys and the exam uses these words.

If you want a single sentence to end the recording on, it is the one that unites the whole
hour: a tax and a price control are both wedges, and a wedge always does three things -
it moves quantity down, it splits the burden according to who cannot leave, and it
destroys the trades in between.

WHAT NEXT LECTURE COLLECTS. Chapter 12 removes the last assumption Chapter 7 made -
that no seller is big enough to move the price. A monopolist chooses quantity and lets
the market pick the price, and the deadweight-loss triangle comes straight back, this
time with no tax and no regulation causing it. Say that; it makes the last lecture of the
course land as the completion of an argument rather than a new topic.""")

prs.save(OUT)
print("wrote", OUT, len(prs.slides._sldIdLst), "slides")
