#!/usr/bin/env python3
"""Build ECON003_Ch08_Trade_UCR_v5.pptx — 41 slides.

v5 = v4 with EVERY lead band and kicker rewritten to the instructor's rule:
  * the top band carries the DEFINITION, or the concrete economic content, of the
    slide's key term — not a description of what the slide is about;
  * the kicker names an ECONOMIC CONCEPT and, wherever the chapter allows it,
    points back at something the students already own (scarcity, the budget
    constraint, surplus, deadweight loss, division of labour).
Removed throughout: procedural instructions, meta-commentary about the deck itself,
encouragement and promises. Recorded as S0c of the ground rules.

REMADE FROM SCRATCH AGAINST THE PUBLISHER'S DECK, which arrived after v1 and v2 were
built.  `Slides/Pearson/Acemoglu_Micro_3e_Ch08 (1).pptx` — 107 slides — is now the source
for structure, examples, exhibit numbers and one photograph.

What that changed, relative to v2:

  * The invented Maya/Owen food-cart example is GONE.  The chapter now runs the book's own
    example throughout: YOU and OLIVIA, websites and computer programs, in an eight-hour
    day.  Students revising from the book see the same names and the same numbers.
  * The cold open is the book's: Babe Ruth, and why the Yankees moved him to the outfield.
    It is posed on slide 4 and answered on slide 16, which is exactly where §8.2 answers it.
  * Every figure carries its EXHIBIT NUMBER.  v2's recap table pointed at sections because
    no exhibit number could be verified; v3 cites 8.1 through 8.15 directly.
  * The absolute-advantage case is the book's, not mine: you take a web-design course, can
    then out-produce Olivia at BOTH goods, and she should still make the websites.
  * §8.3 runs California and Florida on apricots and bananas — the book's pairing.
  * §8.4 and §8.5 run Denmark and tennis shoes, with the book's $50 / $75 / $25 / $15
    tariff sequence and its lettered areas.
  * The chapter's one usable photograph — a WTO protest — is placed at feature size in
    Part 5, with the 7 pt credit line the ground rules permit.
  * The two boxes v2 could only POSE are now answered from the publisher's own notes, so
    no slide carries a PLEASE READ BEFORE DELIVERY flag any more.
  * The Evidence-Based Economics practice problem (New England textiles) is included, with
    its answer, because it is the chapter's own assessment of the EBE question.
  * THE OPENER IS NOT THE BOOK'S, BY INSTRUCTION.  The book opens by asking students to
    wonder whether free trade will cost them their job.  That was replaced with a
    structural portrait of American trade - four facets chosen by the instructor: the
    import share of consumption, the deficit against GDP, what has happened to the
    price of tradable goods, and what the US actually specialises in selling.  A KPI
    row of stat tiles, one headline number each.  The book's question is untouched
    where it belongs, in section 8.5.

Density follows his v2 instruction and has not been relaxed: a figure or a worked table
earns a page; narrative and examples are merged and live in the notes.

ONE PUBLISHER ERROR, FLAGGED ON SLIDE 28 WITHOUT NAMING THEM.  Their slide 76 heads
Exhibit 8.14 "When world price is above domestic price: Import".  It is BELOW; their own
notes on that slide use a world price of $25 against a domestic $50, and their export
slide states the rule correctly.
"""
import os

from pptx import Presentation

import deckkit as D
from deckkit import (BLUE, GOLD, DGOLD, GREEN, RED, INK, INK2, GREY, RULE, WHITE,
                     TINT_BLUE, TINT_NEUTRAL, TINT_RED, TINT_GREEN, TINT_GOLD)

SRC = "/mnt/user-data/uploads/ECON003_26S/Slides/ECON003_Ch08_Trade_UCR.pptx"
OUT = "ECON003_Ch08_Trade_UCR_v5.pptx"
F = "figs3/ch08v3_fig_%s.png"
IC = "icons/%s.png"
PH = "photos/%s_flat.png"

LIMIT = 4.40
FIG_FLOOR = 4.42

prs = Presentation(SRC)
D.drop_slides_after(prs, 1)
s1 = prs.slides[0]
for _sh in list(s1.shapes):
    if _sh.shape_type == 13:                      # no cover image, by instruction
        _sh._element.getparent().remove(_sh._element)
D.retitle_title_slide(s1, ["Chapter 8", "Trade"],
                      ["ECON 003", "UC Riverside · Summer 2026"])
D.notes(s1, """Title.

Chapter 8, Trade. The chapter is a ladder — one idea proved at three scales: two people,
two states, two countries. Nothing changes as you climb it but the size of the units.

Open with the book's own framing: trade just means giving up one thing to get another, so
before we trade with anyone else we have to understand trading with ourselves.""")


def S():
    return D.blank_slide(prs)


def figpage(title, lead, fig, kick, credit=None, lead_kind="formula", lead_size=13.5):
    """Title, a ONE-LINE lead band, the figure, a kicker. Leads must fit one line."""
    s = S()
    D.title(s, title)
    yb = D.band(s, 1.12, lead, kind=lead_kind, size=lead_size) if lead else 1.02
    top = yb + 0.10
    D.picture_fit(s, F % fig, D.M, top, D.CONTENT_W, FIG_FLOOR - top)
    D.kicker(s, kick, y=4.52)
    if credit:
        D.credit(s, credit)
    return s


# ==================================================== 2. where we left off
s = S()
D.title(s, "Where We Left Off")
y = D.defbox(s, 1.15,
             "Chapter 7 asked what one market does when nobody is in charge.\n"
             "Today we let people trade across two markets — and two countries.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "What we proved", "A competitive market maximises social surplus. Nobody "
     "designs that; the price does it.", IC % "balance-scale"),
    (RED, "What we assumed", "One market, one price, everyone inside the same border.",
     IC % "factory"),
    (GREEN, "What we drop today", "That border. Once two producers can trade, a good can "
     "be made wherever it is cheapest.", IC % "shipping-container"),
])
D.kicker(s, "The gains from trade come from differences in OPPORTUNITY COST, not "
            "from differences in skill.", y=4.52)
D.notes(s, """Recap and framing. Thirty seconds.

Only the third card matters. Everything in Chapters 4 to 7 happened inside one market with
one price. Today a second producer exists, with different costs.

Pose the question at the bottom as a paradox: if I am faster than you at everything, what
could you possibly do for me? Most people say "nothing", and that is provably wrong. It
gets answered in Part 2 — do not answer it now.""")

# ========================================================== 3. roadmap
s = S()
D.title(s, "Today's Roadmap")
D.strip5(s, 1.24, [
    ("8.1 The production\npossibilities curve", IC % "up-down"),
    ("8.2 Comparative\nadvantage", IC % "balance-scale"),
    ("8.3 Trade between\nstates", IC % "truck"),
    ("8.4 Trade between\ncountries", IC % "shipping-container"),
    ("8.5 Arguments\nagainst free trade", IC % "ballot-box"),
])
D.rect(s, 0.60, 2.88, 8.80, 0.06, fill=RULE)
D.cards3(s, 3.06, LIMIT - 3.06, [
    (BLUE, "Two people", "You and Olivia, websites and programs. One of you is faster at "
     "everything. Both still gain."),
    (DGOLD, "Two states", "California and Florida, apricots and bananas. Nobody proposes "
     "a tariff at the state line."),
    (RED, "Two countries", "Denmark and tennis shoes — same arithmetic, but a border can "
     "be taxed."),
], body_size=11)
D.kicker(s, "Comparative advantage → specialization → terms of trade → "
            "winners and losers. One chain, three scales.", y=4.52)
D.notes(s, """Roadmap, straight off the book's own section list, so students can follow in
the text.

Say the shape out loud: the entire argument is built in 8.1 and 8.2 with two people and an
eight-hour day. Sections 8.3 and 8.4 introduce one new idea between them — the bowed
economy-wide curve — and otherwise re-run the same arithmetic with bigger units.

The three examples on the cards are the book's, not substitutes. Students will meet the
same names and numbers when they read.

Part 5 is the counterweight and it is not a formality: the book's own question for this
chapter is "Will free trade cause you to lose your job?", not "isn't trade wonderful".""")

# ============================================ 4. the opener: four numbers
figpage("Where the United States Sits in World Trade",
        "Four facts about American trade, before any theory.",
        "opener",
        "America sells the world energy and aeroplanes — and rents it ideas, expertise "
        "and a balance sheet.",
        "Consumer import share: Federal Reserve Bank of San Francisco, Economic Letters "
        "2019-01 and 2025-12. Trade balance and exports: Census / BEA annual revision, "
        "June 2026, 2025 data. Prices: BLS CPI-U, January 2000 to July 2026.",
        lead_kind="neutral")
D.notes(prs.slides[-1], """The opener. Two or three minutes, no diagrams and no vocabulary.
Take the four in order.

MADE ABROAD. Ask the room to guess first — what share of a dollar of American spending
goes to something made outside the United States? Most guess somewhere between a third
and a half. It is about a tenth. The San Francisco Fed traces personal consumption
spending back through the supply chain to where the value was actually added.

Two details that make it land. Even for clothing and footwear, one of the most
import-heavy categories, about 70% of what you pay stays in the United States. And
roughly half of what you spend on an imported item goes to Americans anyway — the
retailer's margin, the trucking, the shelf-stacking. The sticker says made in Vietnam;
half the money does not go there.

Say "roughly a tenth", not a precise figure. The 2019 letter says 11% counting goods and
services; the 2025 letter says 9% counting goods only. Those measure different things and
it would be wrong to present it as a fall.

THE TRADE DEFICIT. Three per cent of GDP in 2025 — $932 billion against an economy of
about $30.8 trillion. This is a macro number in a micro course and it is here for scale,
not for analysis.

The interesting part is the split. The goods deficit is $1.26 trillion, but services run a
SURPLUS of $328 billion, which cancels about a quarter of it. So "the trade deficit" is
really a goods story. Hold that thought for the fourth panel.

If a student asks about 2026: the deficit is running about a third lower so far this year.
That is tariff front-running in early 2025 and some very large gold movements, not a
trend. Do not build anything on it.

PRICES SINCE 2000. Toys down 73%, clothing up 6%, everything on average up 98%, college
and childcare up 188%. The pattern is not goods-versus-services in general — it is
tradable versus non-tradable. Things you can put in a shipping container got cheaper.
Things you cannot got much more expensive.

Two honest caveats, both worth ten seconds. Part of the toy collapse is the statisticians
adjusting for the fact that a toy today is a better product, not just a cheaper one. And
college and healthcare are not expensive BECAUSE of trade — that is mostly Baumol's cost
disease, insurance, and subsidised lending. The claim is about what trade exposure does to
prices, not that trade caused tuition.

WHAT AMERICA SELLS. Rank US export earnings by sector and the answer surprises people in
both directions.

Four of the top six are services, and they are the ones students never think of:
business and professional services — consulting, engineering, R&D, advertising — at $284
billion; travel and education, which is largely foreign students and tourists spending
money here, at $214 billion; financial services at $214 billion; and $195 billion a year
in patent, software and brand licensing. Each of those individually earns more than cars,
or drugs, or medical instruments.

But do not let it become a pure "finance and software" story, because that is wrong in an
important way. The largest single US export sector is ENERGY — crude, refined fuel and
gas, $309 billion. The largest manufactured one is aircraft and spacecraft, $164 billion.
America is the world's biggest oil and gas exporter and its dominant aerospace exporter,
and both belong on the list.

One nuance if a student asks where software is: direct exports of computer and information
services are only about $102 billion. The software money mostly arrives as licensing —
which is why it sits inside that $195 billion patents-and-software bar.

The sentence to leave them with: America sells the world energy and aeroplanes, and rents
it ideas, expertise and a balance sheet. Why any country ends up specialising in
particular things is the rest of the chapter.""")

# ============================================ 5. the Babe Ruth puzzle
s = S()
D.title(s, "And a Puzzle to Carry With It")
y = D.band(s, 1.12, "Why did the Yankees put Babe Ruth in the outfield?", kind="formula",
           size=17)
D.cards2(s, y + 0.28, LIMIT - (y + 0.28), [
    (DGOLD, "The puzzle",
     "He was a dominant left-handed pitcher — two World Series with the Red Sox, and a "
     "scoreless-innings record that stood until 1961. Traded to New York, he pitched 17 "
     "games in 1919 and then almost never again."),
    (BLUE, "Why an economist cares",
     "He was the best pitcher AND the best hitter available. Being the best at something "
     "turns out not to be a reason to do it — and that is the whole of Part 2."),
])
D.kicker(s, "Opportunity cost, not ability, decides who does what.", y=4.52)
D.notes(s, """The book's own cold open for this chapter, and it works best delivered as a
trivia question.

The Red Sox had a left-handed pitcher who helped win the World Series in 1916 and 1918
and set a consecutive-scoreless-innings record that stood until 1961. After 1918 he was
traded, and in 1919 he pitched only 17 games for his new team — he played the outfield
instead. Who was he?

Let them answer, then ask the real question: why would you move the best pitcher in
baseball off the mound?

Do not give it away. It is answered in Part 2, on the slide that says so, and the answer
is the single idea the chapter exists to teach.""")

# ============================================================ 5. DIVIDER 1
s = S()
D.divider(s, "PART 1", "The Production\nPossibilities Curve")
D.notes(s, """Part 1 divider — section 8.1.

The book's framing is worth using: to understand trade between individuals, states or
countries, you must first understand trade with YOURSELF. Any time you do more of one
thing and less of another, you have traded — just with yourself.

Note for anyone who has seen a PPC elsewhere: most textbooks put it in an early scarcity
chapter. This book holds it back to the trade chapter, where it earns its keep.""")

# ================================================== 6. Exhibit 8.1
s = S()
D.title(s, "Exhibit 8.1 — First, Trade With Yourself")
D.band(s, 1.12, "You have an eight-hour day. You can build websites, or write computer "
                "programs, or split the time.", kind="neutral", size=14)
D.table(s, 1.55, 1.86, 6.90, 1.62, [
    ["Hours on websites", "Websites", "Hours on programs", "Programs"],
    ["8", "8", "0", "0"],
    ["6", "6", "2", "4"],
    ["4", "4", "4", "8"],
    ["0", "0", "8", "16"],
], col_w=[1.90, 1.50, 1.90, 1.60], header_size=10.5, body_size=11,
    align=["ctr", "ctr", "ctr", "ctr"])
D.band(s, 3.66, "One website an hour. Two programs an hour. Every row uses all eight "
                "hours.", kind="formula", size=13.5)
D.kicker(s, "The trade-off IS scarcity — Chapter 1's first idea, now measured in "
            "websites and programs.", y=4.52)
D.notes(s, """The book's Exhibit 8.1, abridged to four rows — the full nine-row table is in
the text and there is no need to read it out.

The rates: one website per hour, two programs per hour. So a full day is either 8 websites
or 16 programs, or anything in between that uses eight hours.

Two things to make explicit now, because they cause every later misunderstanding. These
are rates, not totals. And we are assuming whole units and a full eight hours, exactly as
Chapter 5 did with jeans and sweaters — connect it back, students remember that one.

The book's framing for this section is the useful one: this is trade with yourself. If you
shift an hour from programs to websites you have exchanged one good for another. Everything
that follows is the same act with a second person in it.""")

# =================================== 7. Exhibit 8.2, with the three regions and the slope
# The figure page and the old "Reading the Curve" card page are ONE slide: the cards
# were explaining a picture that was on the previous slide, which is exactly the split
# the density rule forbids.  Figure height gives way to the card row deliberately.
s = S()
D.title(s, "Exhibit 8.2 — The Production Possibilities Curve")
D.picture_fit(s, F % "ex82_ppc", D.M, 1.10, D.CONTENT_W, 1.75)
D.cards3(s, 2.97, LIMIT - 2.97, [
    (GREEN, "Where a point sits", "ON it (B, D): every hour used. INSIDE (A): possible "
     "but wasteful. OUTSIDE (C): not possible today."),
    (RED, "The slope is the cost", "D to B: give up 4 programs, get 2 websites. So one "
     "website costs two programs — everywhere on the line."),
    (BLUE, "The definition", "The maximum of one good for a given level of the other. "
     "Also called the production possibilities FRONTIER."),
], body_size=10.5)
D.kicker(s, "Same shape as Chapter 5's budget constraint — but this line is what you can "
            "PRODUCE, not what you can afford.", y=4.52)
D.notes(s, """The book's Exhibit 8.2, with its four lettered points, and the three things
students have to take from it.

Build the line first. All eight hours on programs gives 16 — the vertical intercept. All
eight on websites gives 8. Join them.

WHERE A POINT SITS. B and D are ON the curve: attainable and efficient, every hour used.
A is INSIDE: attainable but inefficient — you could have more of both, so something is
being wasted. C is OUTSIDE: not attainable in an eight-hour day. Worth saying explicitly
that a point inside is not "choosing to work less" — it is a failure, and there is no
trade-off to think about, only a mistake to fix.

THE SLOPE. Moving from D to B you give up 4 programs and get 2 websites, so one website
costs two programs — and because the line is straight it costs two programs everywhere
along it. Then drill the inversion, because it is where marks go: if a website costs 2
programs, a program costs half a website. Ask for that second one out loud.

Why is the slope negative? Because the hours are fixed. That is the whole content of the
minus sign.

THE DEFINITION, in the book's own words: the production possibilities curve shows the
relationship between the maximum production of one good for a given level of production
of another good. It is also called the production possibilities FRONTIER, and students
will meet both names.

THE KICKER IS THE ONE TO DWELL ON. The book makes this link twice in its own notes, and
it is the fastest way in for anyone who found Chapter 5 easier than this one: the PPC is
the budget constraint, moved from consumption to production. Same downward-sloping line,
same "the slope is what you give up", same three regions.

The difference is what limits you. In Chapter 5 the constraint was money and prices — what
you could AFFORD. Here it is hours and skill — what you can MAKE. If you drew the jeans
and sweaters budget line in Chapter 5, you have already drawn this.

One honest note if a student pushes: the book gives no separate name for the region under
the curve. There is no "production set" to match Chapter 5's budget set — only the curve
itself is a defined term.""")

# =========================================================== 9. Exhibit 8.3
figpage("Exhibit 8.3 — Two Production Possibilities Curves",
        "Olivia has the same eight hours and the opposite strengths.",
        "ex83_two",
        "Her curve is not smaller than yours, it is the other way up — and the slope IS "
        "the opportunity cost.")
D.notes(prs.slides[-1], """Olivia enters. The book's Exhibit 8.3.

She can make 16 websites or 8 programs in her day — the mirror image of you. Note that
neither of you is better at both: you out-produce her on programs, she out-produces you on
websites. That is the easy case, and the book starts here deliberately before making it
hard.

The thing to point at is the SLOPES. Yours falls two programs for every website. Hers
falls half a program for every website. Different slopes mean different opportunity costs.

Say the sentence that sets up Part 2: the height of a curve tells you who is more
productive; the slope tells you who should do what. Students conflate those two facts for
the whole chapter unless you separate them here, with the picture up.""")

# ============================================ 10. calculating opportunity cost
s = S()
D.title(s, "Calculating Opportunity Cost")
D.band(s, 1.12, "OPPORTUNITY COST — the units of the other good you give up to "
                "produce one unit of this one.", kind="neutral", size=14)
D.table(s, 1.00, 1.86, 8.00, 1.68, [
    ["", "One website costs", "One program costs"],
    ["You", "2 programs", "½ a website"],
    ["Olivia", "½ a program", "2 websites"],
], col_w=[1.60, 3.20, 3.20], first_col_fill=BLUE, header_size=10.5, body_size=11.5,
    align=["l", "ctr", "ctr"])
D.band(s, 3.72, "Websites are cheap for Olivia. Programs are cheap for you. Nobody is "
                "cheapest at both.", kind="answer", size=13.5)
D.kicker(s, "Different people have different specialties — this is where the "
            "DIVISION OF LABOUR arises.", y=4.52)
D.notes(s, """The table that decides the chapter. Read it slowly.

A website costs you 2 programs and costs Olivia half a program — so websites are cheap for
her. A program costs you half a website and costs Olivia 2 websites — so programs are cheap
for you.

The green band is worth stating as a theorem rather than an observation: the two costs in a
row are reciprocals of each other, so it is arithmetically impossible for one person to be
the cheap producer of both. If your websites are cheaper than mine, your programs must be
dearer. That is division, not an empirical regularity — which is why there is ALWAYS a
basis for trade.

The kicker is the practical instruction and it is worth repeating at revision time.

Common error to name now: answering in the wrong good. The cost of a website is measured in
programs; the cost of a program is measured in websites.""")

# ============================================================ 11. DIVIDER 2
s = S()
D.divider(s, "PART 2", "The Basis for Trade:\nComparative Advantage")
D.notes(prs.slides[-1], """Part 2 divider — section 8.2. The heart of the chapter.
Everything after this is application: if they get Part 2, Parts 3, 4 and 5 are
bookkeeping.""")

# =================================================== 12. comparative advantage
s = S()
D.title(s, "Comparative Advantage")
y = D.defbox(s, 1.15,
             "COMPARATIVE ADVANTAGE — the ability of one economic agent to produce at a "
             "lower opportunity cost than another.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "You", "Lower cost of producing PROGRAMS: half a website each, against "
     "Olivia's two.", IC % "research"),
    (DGOLD, "Olivia", "Lower cost of producing WEBSITES: half a program each, against "
     "your two.", IC % "phone"),
    (GREEN, "So specialise", "Each of you does only the good you are cheapest at, and "
     "then you trade. More gets produced out of the same sixteen hours.", IC % "exchange"),
])
D.kicker(s, "The person with the lowest opportunity cost should be the one who produces.",
         y=4.52)
D.notes(s, """The definition, read off the panel word for word — "lower opportunity cost"
is doing all the work, and students who paraphrase it as "better at" have lost the idea.

This is the book's rule, stated on its own slide: the person with the lowest opportunity
cost should produce. That is the sentence to memorise.

Worth naming the intellectual history in one line, because it is one of the oldest results
in the subject: this is David Ricardo's argument from 1817, and it is still the most
counter-intuitive true thing in introductory economics.

The next exhibit shows what specialising actually buys.""")

# =========================================================== 13. Exhibit 8.4
figpage("Exhibit 8.4 — The Gains from Specialization",
        "Add the two curves together. You make only programs, Olivia makes only websites.",
        "ex84_gains",
        "Point T — 16 websites and 16 programs — is outside BOTH curves. Specialization "
        "puts you beyond your own curve.")
D.notes(prs.slides[-1], """The payoff exhibit, and it rewards a slow walk.

The green line is the two PPCs added together. Build it from the left: starting with
everyone making programs, you get 24 — 16 from you and 8 from Olivia. To get websites you
move whoever gives up least, which is Olivia at half a program per website, so the first
stretch has HER slope. When she runs out of hours you are at point T. Past that you have
to move yourself, at two programs per website, so the line gets steeper. That is why it
kinks, and it is why the book says specialisation makes the joint curve bow out.

At T you make 16 programs and Olivia makes 16 websites.

Now the sentence that matters: T is above both individual curves. Neither of you has the
resources to produce it alone. Trade is a way of breaking the constraint that scarce
resources put on you — that is the book's own phrasing and it is worth quoting.

Nobody worked longer. Sixteen hours went in before and sixteen after.""")

# =========================================================== 14. Exhibit 8.5
figpage("Exhibit 8.5 — What If You Were Better at Both?",
        "You take a course in web design. You can now make 24 websites a day, or 16 "
        "programs.",
        "ex85_absolute",
        "You now out-produce Olivia at BOTH goods. Should you just do everything "
        "yourself?")
D.notes(prs.slides[-1], """The twist, and it is the book's, not mine. Deliver the question
on the kicker as a genuine one and let it sit.

After the course you can produce 24 websites in a day rather than 8. Your program
production is unchanged at 16. Olivia's curve has not moved at all.

So you can now make more websites than Olivia (24 against 16) AND more programs (16
against 8). Your curve is outside hers everywhere.

Students find it very hard to see why you should not simply produce both goods yourself —
the book says so explicitly in its notes, so expect it. Do not resolve it on this slide.
The next slide does, with the arithmetic.""")

# ============================================ 15. absolute advantage
s = S()
D.title(s, "Absolute Advantage — and Why It Does Not Decide")
y = D.defbox(s, 1.15,
             "ABSOLUTE ADVANTAGE — the ability to produce MORE output than another agent "
             "with the same resources.")
D.table(s, 1.00, y + 0.20, 8.00, 1.40, [
    ["", "One website costs", "One program costs"],
    ["You (after the course)", "⅔ of a program  (0.67)", "1½ websites  (1.50)"],
    ["Olivia", "½ a program  (0.50)", "2 websites  (2.00)"],
], col_w=[2.40, 2.80, 2.80], first_col_fill=BLUE, header_size=10.5, body_size=11,
    align=["l", "ctr", "ctr"])
D.band(s, y + 1.74, "0.50 beats 0.67, so websites are STILL Olivia's. 1.50 beats 2.00, so "
                    "programs are still yours.", kind="answer", size=13.5)
D.kicker(s, "You have both absolute advantages and neither of you has both comparative "
            "advantages.", y=4.52)
D.notes(s, """The resolution, and it is the most important slide in Part 2.

Read the definition off the panel — absolute advantage compares OUTPUT, comparative
advantage compares COST. That distinction is examinable and the exam question is usually
built so the two answers differ.

Now the arithmetic. After the course a website costs you two-thirds of a program, because
in the time it takes to build one you could have written two-thirds of a program. It costs
Olivia half a program. Half is less than two-thirds, so she is still the cheap producer of
websites.

A program costs you one and a half websites; it costs Olivia two. So programs are still
cheaper for you.

Then the general result, which the book states and which is worth giving them: with
straight-line curves, unless two people have exactly the same opportunity cost, one will
always have the comparative advantage in one good and the other in the other. Being better
at everything does not and cannot give you both.

Say it plainly: you can be better at everything and still gain by letting someone else do
some of it.""")

# ============================================ 16. Babe Ruth answered
s = S()
D.title(s, "So Why Didn't Babe Ruth Pitch Again?")
y = D.band(s, 1.12, "Because being the best at a job is not a reason to do it.",
           kind="answer", size=16)
D.cards3(s, y + 0.28, LIMIT - (y + 0.28), [
    (BLUE, "He had both absolute advantages", "One of the best pitchers in baseball, and "
     "the best hitter. On output alone he should have done both.", IC % "clock"),
    (RED, "But pitching cost him more", "A pitcher plays roughly every fourth day. An "
     "outfielder bats every day. Pitching meant giving up most of his hitting."),
    (GREEN, "So the Yankees specialised him", "His opportunity cost was lower in hitting. "
     "They moved him where he gave up least — and he rewrote the record book."),
])
D.kicker(s, "The same logic as Olivia's websites, in pinstripes — comparative advantage, "
            "in a batting order.", y=4.52)
D.notes(s, """The payoff to the cold open, and the book answers it in exactly this place.

Their note is the whole answer in one line: Ruth was both a dominant pitcher and a dominant
hitter, but his opportunity cost was lower with hitting.

Make the mechanism concrete, because it is what makes it stick. A starting pitcher works
roughly one game in four. An everyday outfielder bats in all of them. So every game Ruth
spent pitching was three or four games of his bat that the Yankees did not get. He was
excellent at both; he was CHEAP at only one.

Then generalise, and this is the version students carry out of the room: you give the job
to whoever gives up least by doing it. It is why a surgeon who types quickly still does not
do her own typing, and it is why you should let Olivia build the websites.

Careful with one thing if a baseball-literate student pushes back: the Yankees' decision
was not purely economic and the historical record is more tangled than the textbook
version. Teach it as the textbook's illustration, which is what it is.""")

# ============================================ 17. would you take this trade
s = S()
D.title(s, "Would You Take This Trade?")
D.band(s, 1.12, "You can always \"trade with yourself\" at your own opportunity cost. Any "
                "offer has to beat that.", kind="formula", size=14)
D.cards3(s, 1.86, 1.62, [
    (RED, "1 website for 1 program?", "NO. Give up a program yourself and you get 1½ "
     "websites. Olivia's offer is worse than doing it alone."),
    (GREEN, "2 websites for 1 program?", "YES. Two beats the 1½ you could get on your "
     "own. You are better off trading."),
    (RED, "3 websites for 1 program?", "Olivia says no. She can get 2 websites per "
     "program by herself, so 3 is above her limit."),
])
D.band(s, 3.62, "Your minimum is 1½ websites. Her maximum is 2 websites. Any price "
                "strictly between them works.", kind="answer", size=14)
D.kicker(s, "Nobody trades below their own opportunity cost — the voluntary exchange "
            "behind Chapter 7's surplus.", y=4.62)
D.notes(s, """The book's three questions, on one page instead of three. This is the
examinable mechanic — expect "which of these terms of trade would both parties accept?"

Work them in order.

One website for one program: you say no. If you simply stop making one program yourself
you free up enough time to build one and a half websites. Olivia is offering less than you
can do alone.

Two websites for one program: yes. Two beats one and a half.

Three websites for one program: now check HER side. Olivia can turn one program's worth of
her own time into two websites, so she will never pay three. Her maximum is two.

That is the whole logic, and it is a no-arbitrage argument — the same shape as Chapter 7.
Nobody buys for more than it costs them to make, nobody sells for less. Those two refusals
bracket the price.

The book's own worked example, worth giving: at one and three-quarter websites per program,
each of you gains a quarter of a website and a quarter of a program. Both better off, at
the same price, at the same time.""")

# ============================================ 18. terms of trade
s = S()
D.title(s, "Terms of Trade")
y = D.defbox(s, 1.15,
             "TERMS OF TRADE — the \"price\" of one good in terms of the other; the "
             "exchange rate between goods.")
D.cards2(s, y + 0.24, LIMIT - (y + 0.24), [
    (BLUE, "The model fixes the range",
     "Between the two opportunity costs — here, 1½ to 2 websites for a program. Outside "
     "that range one side is better off not trading at all, so no deal happens."),
    (DGOLD, "But not the price inside it",
     "Where it lands depends on bargaining, or on a market. Near 1½ Olivia captures most "
     "of the gain; near 2 you do. Both gain either way — but not equally."),
])
D.kicker(s, "Trade creates surplus; the terms of trade split it — as the price split "
            "surplus in Chapter 7.", y=4.52)
D.notes(s, """The definition and the honest limit of the model. This is a short slide but
the second card sets up Part 5, so do not rush it.

The range is determined: between the two opportunity costs, and the book says so
explicitly.

The price INSIDE the range is not determined by anything in this chapter. It comes out of
bargaining, or out of a world market once we get to Section 8.4. Say that rather than let
students think it was derived.

Then the distributional point, which is the same structure as the entire free-trade debate
at national scale: trade creates a surplus, and bargaining divides it. The model says both
sides gain. It says nothing about whether the split is fair, and it has no way to.""")

# ============================================================ 19. DIVIDER 3
s = S()
D.divider(s, "PART 3", "Trade Between States")
D.notes(prs.slides[-1], """Part 3 divider — section 8.3.

Why this section exists: most textbooks go straight from two people to two countries. This
book puts a rung in between, and it is rhetorically powerful — nobody has strong feelings
about interstate trade, so the economics can be seen without the politics attached.""")

# ============================================ 20. exports and imports
s = S()
D.title(s, "Exports and Imports")
y = D.defbox(s, 1.15,
             "EXPORT — produced here, shipped to another state or country.\n"
             "IMPORT — produced in another state or country, sold here.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "Notice what is missing", "Neither definition mentions a national border. The "
     "book defines both for STATES as well as countries, on purpose."),
    (DGOLD, "What gives a state its edge", "Natural resources, proximity to rivers, ports "
     "and transport hubs, and concentrations of expertise.", IC % "truck"),
    (GREEN, "And the consequence", "States specialise hard and trade the results. No one "
     "regards that as a problem, and no one proposes a tariff at the state line."),
])
D.kicker(s, "Economically a state line and a national border are the same thing. Legally "
            "they are not.", y=4.52)
D.notes(s, """Two key terms, and the book defines them for states as well as countries —
which is the point.

An export is produced here and shipped elsewhere; an import is produced elsewhere and sold
here. Neither definition needs a border.

Ask the book's question before giving the second card: what gives a state a comparative
advantage? Natural resources, proximity to transportation hubs — rivers and sea coasts —
and concentrations of expertise. Ask for examples of goods particular to one or two states
and you will get oranges, cotton, pineapples.

The kicker is the setup for Part 4 and it is worth saying twice. The arithmetic at a state
line and a national border is identical. What differs is that a national border is a place
where a government can stand and collect money.""")

# =========================================================== 20. Exhibit 8.6
figpage("Exhibit 8.6 — How Much States Trade With Each Other",
        "EXPORT: made here, sold elsewhere. IMPORT: made elsewhere, sold here.",
        "ex86_states",
        "The average state ships about eleven times as much value to other states as it "
        "does abroad.",
        "Exhibit 8.6, redrawn. The publisher states these ratios are approximate.")
D.notes(prs.slides[-1], """Exports and imports get defined here, and the book defines them
for STATES as well as countries — a good and slightly unusual choice, so use it.

An export is a good produced domestically and shipped to another state or country. An
import is produced elsewhere and sold here. Note the definitions do not mention borders.

The chart is the ratio of interstate exports to international exports, state by state.
Almost every bar is well above one, and several are enormous — South Dakota near 37,
Hawaii near 30, Oklahoma near 25.

The District of Columbia is the only one below one, at about a quarter. Ask why, and let
them work it out: it is tiny, it borders two states it is economically continuous with, and
what it "exports" is largely services.

Two things to say. First, states specialise ferociously and trade the results, and nobody
regards that as a problem — nobody proposes a tariff on Iowa corn. Second, and this is the
setup for Part 4: economically, a state line and a national border are the same thing. The
difference is legal and political, because a national border can be taxed.

Ask the book's question — what gives a state a comparative advantage? Natural resources,
proximity to ports and rivers, and concentrations of expertise.

Say once that the ratios are approximate; the credit line says so too.""")

# =========================================================== 21. Exhibit 8.7
figpage("Exhibit 8.7 — A Whole Economy's Curve Bends",
        "INCREASING OPPORTUNITY COST — each extra unit costs more of the other than "
        "the last.",
        "ex87_increasing",
        "Resources are not equally suited to every use, so an economy's curve bows "
        "outward.")
D.notes(prs.slides[-1], """The economy-wide PPC, and the one genuinely new idea in Part 3.

Your curve and Olivia's were straight because one person with one skill has a constant
opportunity cost — the eighth hour is as good as the first.

An economy is not like that. Take the book's apples and oranges. Start with everything in
apples. To grow the first orange you move the land that was worst at apples anyway, so it
costs you very little. Keep going and you run out of bad apple land and start converting
good apple land, so each additional orange costs more than the last. Going from 0 to 1
orange costs a fraction of an apple; going from 6 to 7 costs more than two.

Drawn, rising cost is a curve that steepens as you move right. That is the bow.

Same three regions as before — B on the curve, A inside, C outside.

Watch for the standard wrong answer: students say the curve bows because of "scarcity" or
"diminishing returns". Scarcity is why there is a curve at all. It is the DIVERSITY of
resources — some land good for apples, some for oranges — that bends it. If every resource
were equally good at both, the curve would be straight.""")

# =========================================================== 22. Exhibit 8.8
figpage("Exhibit 8.8 — How Improved Technology Shifts the Curve",
        "Point C was impossible. What would it take to make it possible?",
        "ex88_shift",
        "ECONOMIC GROWTH is the production possibilities curve shifting outward.")
D.notes(prs.slides[-1], """Short slide, thirty seconds, and it answers the question left
hanging on Exhibit 8.7.

Point C was outside the curve. To reach it the curve itself has to move, and there are
three ways: more resources, higher-quality resources, or an improvement in technology.

That is economic growth in one sentence, and it is worth saying that this is the same
picture macroeconomics uses for it.

Note what does NOT move the curve: wanting more, or working the same resources harder in
the same way. And note that a shift outward means more of BOTH goods becomes possible —
this is not a trade-off, which is exactly what makes growth different from every other
choice in this chapter.""")

# ============================================ 23. California and Florida
s = S()
D.title(s, "Who Should Produce What? California and Florida")
D.band(s, 1.12, "The same opportunity-cost table, for two states instead of two people.",
       kind="neutral", size=14)
D.table(s, 1.00, 1.80, 8.00, 1.44, [
    ["", "One apricot costs", "One banana costs"],
    ["California", "⅕ of a banana", "5 apricots"],
    ["Florida", "8 bananas", "⅛ of an apricot"],
], col_w=[1.90, 3.05, 3.05], first_col_fill=BLUE, header_size=10.5, body_size=11.5,
    align=["l", "ctr", "ctr"])
D.band(s, 3.38, "Apricots are cheap in California (⅕ against 8). Bananas are cheap in "
                "Florida (⅛ against 5).\nSo the terms of trade for a banana lie between "
                "⅛ and 5 apricots.", kind="answer", size=13.5)
D.kicker(s, "Comparative advantage does not depend on the size of the trading unit: person, state or country.", y=4.62)
D.notes(s, """The book's state-level example, and the point of it is that nothing new is
happening.

Read down the columns. An apricot costs California a fifth of a banana and costs Florida
eight bananas — so California is the cheap apricot producer, by a wide margin. A banana
costs California five apricots and Florida an eighth of an apricot — so Florida is the
cheap banana producer.

Same rule, same table shape, same conclusion. Only the units changed.

The terms of trade work exactly as before: Florida will not accept less than an eighth of
an apricot for a banana, because it can get that by producing apricots itself. California
will not pay more than five apricots for the same reason. So the price sits between an
eighth and five.

Notice how wide that range is compared with the one and a half to two we had for you and
Olivia. Worth one sentence: the more different two producers' opportunity costs are, the
bigger the potential gain from trading and the wider the range of prices that works.

And the observation that carries into Part 4: this trade happens constantly, at enormous
volume, and nobody objects to it.""")

# ============================================================ 24. DIVIDER 4
s = S()
D.divider(s, "PART 4", "Trade Between Countries")
D.notes(prs.slides[-1], """Part 4 divider — section 8.4.

Tell students explicitly that the tool changes here. Parts 1 to 3 used production
possibilities curves. Part 4 uses the supply and demand diagram from Chapter 4 and the
surplus areas from Chapter 7. A student still thinking in PPCs will be lost within two
slides.

This is where the exam questions cluster.""")

# ============================================ 25. what the US trades
s = S()
D.title(s, "What the United States Actually Trades")
y = D.band(s, 1.12, "TRADE DEFICIT — imports exceed exports.   TRADE SURPLUS — "
                    "exports exceed imports.", kind="neutral", size=14)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "8.9 — the aggregate", "Exports and imports both grew enormously since 1960. "
     "They tracked each other until the mid-1970s, then imports pulled ahead.",
     IC % "shipping-container"),
    (DGOLD, "8.10 — crude oil", "A very different shape. Looking only at totals hides "
     "how much trade behaviour varies good by good.", IC % "gas-pump"),
    (GREEN, "8.11 — manufactured goods", "The bulk of the reason the US is a net "
     "importer. Meanwhile it is a major exporter of food, services and films.",
     IC % "factory"),
])
D.kicker(s, "\"Net importer\" is a statement about a total. It says almost nothing about "
            "any particular good.", y=4.52)
D.notes(s, """The book carries three data exhibits here — 8.9, 8.10 and 8.11. They are in
the text and I have deliberately NOT redrawn them: the underlying series are not in the
deck, only approximate readings, and redrawing sixty years of data from approximations
would be inventing a figure. Point students at the exhibits in the book and teach the three
conclusions, which is all they are examined on.

8.9: both exports and imports have grown by orders of magnitude since 1960. They were close
together until the mid-1970s; since then imports have grown faster, which is the trade
deficit.

8.10: crude oil looks nothing like the aggregate. Use this to make the methodological point
on the kicker — an aggregate hides enormous variation.

8.11: manufactured goods are most of the gap. And say the other half out loud, because
students rarely hear it: the United States is a large net EXPORTER of agricultural
commodities and processed food, of management and business services, and of films.

The kicker is the transferable idea. Being a net importer overall is compatible with
dominating world exports in several industries.""")

# ============================================ 26. where world prices come from
s = S()
D.title(s, "Where Do World Prices Come From?")
y = D.band(s, 1.12, "WORLD PRICE — where world supply of a good meets world demand.",
           kind="formula", size=15)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "What a country starts with", "Natural resources, the capital it has already "
     "built, and its technology.", IC % "factory"),
    (DGOLD, "Who does the work", "Education, work habits and experience of the labour "
     "force — and how abundant labour is against physical capital.", IC % "hard-hat"),
    (GREEN, "And the accidents", "Climate. Denmark does not grow bananas, and no amount "
     "of policy will change that.", IC % "wheat"),
])
D.kicker(s, "Differences in resources, capital and technology are what make one "
            "country's costs differ from another's.", y=4.52)
D.notes(s, """The book asks this directly and it is worth a page, because otherwise the
world price looks like a number that fell out of the sky.

In the diagrams that follow we FIX the world price to make a point about winners and
losers. But it is not exogenous in reality. As countries open their borders and act on
their comparative advantages, you can add up all those actions into a world supply curve
and a world demand curve. Where they cross is the world price. Same framework as Chapter 4,
bigger units — which is the whole theme of the chapter.

The list on the cards is the book's own answer to why one country's costs differ from
another's: natural resources, stocks of human-made resources, technology, the education and
work habits and experience of labour, the relative abundance of labour against physical
capital, and climate.

Keep it to a minute. It is context, not mechanics.""")

# =========================================================== 26. Exhibit 8.12
figpage("Exhibit 8.12 — Start With the Border Closed",
        "The market for tennis shoes in Denmark, with no imports and no exports.",
        "ex812_denmark",
        "Fifty dollars a pair, two million pairs — and every pair made in Denmark.")
D.notes(prs.slides[-1], """The baseline. Everything in Part 4 is measured against this
picture.

Chapter 4's diagram with Chapter 7's shading. Supply and demand cross at $50 and 2 million
pairs. With the border closed that is the price and the quantity, consumer surplus is the
blue triangle and producer surplus the red one.

Now the new idea: FREE TRADE means trade with no government involvement, and it produces a
WORLD PRICE — the price of the good on the world market. Denmark is small enough to buy or
sell as much as it likes at that price, which is why it will be a horizontal line on the
next two diagrams.

The question that drives the rest of Part 4, and put it to them before you answer it: will
Denmark import tennis shoes, or export them? The answer is that it depends entirely on how
the world price compares with this $50.""")

# =========================================================== 27. Exhibit 8.13
figpage("Exhibit 8.13 — Winners and Losers in an Exporting Nation",
        "Suppose the world price is $75. No Danish producer will sell at home for $50.",
        "ex813_export",
        "Producers gain B + C, consumers lose B, and the country nets area C — 31¼ "
        "million dollars.")
D.notes(prs.slides[-1], """The exporting case. Mechanics first, then the welfare.

If the world will pay $75, Danish producers would rather sell abroad, so the domestic price
rises to $75. Read the two curves separately at that price — and this is where students go
wrong. Demand: Danes now want only 0.75 million pairs. Supply: Danish firms want to make
3.25 million. The difference, 2.5 million pairs, is exported.

Now the areas, which is what the exhibit is for. Consumer surplus was B + D and is now just
D, so consumers lose B. Producer surplus was A and is now A + B + C, so producers gain
B + C. Area B moved from consumers to producers — a transfer. Area C belonged to nobody
before: it exists only because trade is possible.

Net gain to Denmark: area C, which works out to $31.25 million.

Then the honest part. Danish consumers are worse off — less product at a higher price. Ask
whether they will be pleased that the country gained area C, and let the room say no. The
book's own suggestion is that the government could transfer some of the producers' gains to
offset the consumers' losses. Note "could".""")

# =========================================================== 28. Exhibit 8.14
figpage("Exhibit 8.14 — Winners and Losers in an Importing Nation",
        "Now the world price is $25 — BELOW the domestic $50. Denmark imports.",
        "ex814_import",
        "Consumers gain C + D, producers lose C, and the country nets area D — again "
        "31¼ million dollars.",
        "The rule is: a world price BELOW the domestic price means you import. Some "
        "printed versions of this exhibit state it the wrong way round.")
D.notes(prs.slides[-1], """The importing case, and the mirror image.

At a world price of $25, Danish consumers want 3.25 million pairs and Danish producers want
to make only 0.75 million. The missing 2.5 million pairs are imported.

Consumer surplus rises by C + D. Producer surplus falls by C. C is a transfer from
producers to consumers; D exists only because of trade. Net gain: area D, $31.25 million —
the same figure as the export case, because these schedules are symmetric.

FLAG ON THE SLIDE, AND SAY IT OUT LOUD. The credit line notes that some printed versions of
this exhibit head it "when world price is ABOVE domestic price: import". That is backwards,
and their own worked numbers on the same page use $25 against $50. Tell students to trust
the arithmetic, not the heading — and do not name the publisher on camera; the slide does
not name them either.

The rule, and dictate it: world price below your no-trade price means you import; above it
means you export. Find the no-trade price FIRST — every question in this part starts there.

And the commonest error, worth stating explicitly: at the world price, quantity supplied and
quantity demanded are NOT equal. Read them off the two curves separately. Their difference
is the trade.

Ask whether Danish producers are pleased about area D. They are not, and they are the ones
who will lobby.""")

# ============================================ 29. both ways
s = S()
D.title(s, "Either Direction, the Country Gains")
y = D.band(s, 1.12, "Exporting: producers gain more than consumers lose.   Importing: "
                    "consumers gain more than producers lose.", kind="formula", size=14)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "The result", "In both cases Denmark is better off overall. The specific "
     "winners and losers swap; the total goes up either way."),
    (RED, "The catch", "There is no version of opening a border where everyone at home "
     "gains. Somebody was benefiting from it being shut."),
    (DGOLD, "The book's answer", "Winners COULD be required to compensate losers — and "
     "still come out ahead. Whether they are is a political choice.", IC % "ballot-box"),
])
D.kicker(s, "\"The country gains\" is a claim about a total. It never was a claim that "
            "each person gains.", y=4.52)
D.notes(s, """The summary of Section 8.4 and the bridge into Part 5.

The result is symmetric and worth stating as such: trade raises Denmark's total surplus
whichever way the shoes flow. What changes is who wins.

The second card is the one to say slowly. Opening a border always creates a domestic loser,
because someone was protected by it being closed. In the export case it is consumers; in the
import case it is producers.

The third card is the compensation principle, and the book raises it directly. The
arithmetic is clean: gains exceed losses, so the winners could hand over enough to leave
everyone at least as well off and still be ahead. That is what "the country gains" means,
formally.

The gap between "could" and "does" is the whole of Part 5, so leave it open here.

Finally, the book's own question — where do world prices come from? Answer: the same supply
and demand framework, at world scale. As countries open up and act on their comparative
advantages, world supply and world demand intersect, and that intersection is the world
price. Differences in natural resources, capital, technology, education, labour and climate
are what make one country's costs differ from another's.""")

# ============================================================ 30. DIVIDER 5
s = S()
D.divider(s, "PART 5", "Arguments Against\nFree Trade")
D.notes(prs.slides[-1], """Part 5 divider — section 8.5.

Set the tone. Everything so far has pointed one way and a student paying attention should
be slightly suspicious of how tidy it has been.

Deliver this part straight. Do not set the arguments up in order to knock them down. Some
are weak, one is strong, and students should be able to tell which from the reasoning
rather than from your tone of voice.""")

# ============================================ 31. the photograph
s = S()
D.title(s, "Not Everybody Is Convinced")
D.photo(s, PH % "wto_protest", 0.60, 1.15, 2.30, 3.25)
D.textbox(s, 3.25, 1.20, 6.15, 0.90,
          "Every result so far said trade makes a country better off.\n"
          "So why do people protest against it?",
          size=15, bold=True, color=DGOLD, line_pct=1.22)
D.rect(s, 3.25, 2.22, 6.15, 0.06, fill=GOLD)
D.textbox(s, 3.25, 2.44, 6.15, 1.90,
          "Because \u201cbetter off\u201d has been a statement about a TOTAL, all hour. "
          "The diagrams have been showing you the losers in red since Exhibit 8.13 — "
          "Danish shoemakers when the price fell, Danish shoe buyers when it rose.\n\n"
          "Those people are real, they know exactly who they are, and the compensation "
          "the model says is affordable is rarely actually paid.",
          size=12.5, color=INK2, line_pct=1.26)
D.image_credit(s)
D.notes(s, """The chapter's one photograph, at feature size.

Use it as a pivot rather than a decoration. Ask the question on the slide and let it sit for
a moment. Students who have followed the last twenty minutes have been told repeatedly that
trade makes a country better off, and they are about to be told that serious people disagree.

The resolution is the one you have been building all hour: every result has been about a
total. The diagrams showed the losers explicitly — area B taken from Danish consumers when
the price rose, area C taken from Danish producers when it fell. Nothing in Part 4 was
hidden.

What the model does not deliver is the compensation. It says the transfer is affordable. It
does not make anyone vote for it.

That is the honest way into the five arguments, and it means you can take them seriously
rather than treating them as errors.""")

# ============================================ 32. five arguments
s = S()
D.title(s, "Arguments Against Free Trade")
y = D.band(s, 1.12, "Every one of them accepts the diagram and argues that something "
                    "outside it matters more.", kind="formula", size=14.5)
D.strip5(s, y + 0.24, [
    ("National\nsecurity", IC % "hard-hat"),
    ("Culture and\nglobalization", IC % "ballot-box"),
    ("Environment\nand resources", IC % "wheat"),
    ("Infant\nindustries", IC % "lightbulb"),
    ("Local wages\nand jobs", IC % "factory"),
])
y = D.band(s, 3.34, "PROTECTIONISM — the view that governments should control trade "
                    "because of the harmful effects of free trade.\nIts most popular "
                    "instrument is the TARIFF.", kind="note",
           size=13.5)
D.kicker(s, "The test for any of them: is a tariff the cheapest way to buy the thing you "
            "actually want?", y=4.62)
D.notes(s, """All five arguments on one page — the detail lives here, not in five slides.
Budget three or four minutes and take them in order.

The top band is the analytical key and it is worth saying twice. None of these five claims
the diagram is wrong. They all concede that a tariff costs consumers more than it gains
producers. What they claim is that the diagram leaves out something worth more than the
loss. That tells students how to evaluate a protection argument they have never met before.

NATIONAL SECURITY. Over-reliance on other countries for goods and services you might
urgently need. The strong version is correct — no economist argues a country should buy its
munitions from whoever is cheapest this year. The problem is that it has no natural
boundary: it is a claim about a hypothetical future, so it is very hard to test, and
historically it has been attached to a remarkable range of products. And even a real
security concern can be met by stockpiles or diversified suppliers rather than a permanent
tax on consumers.

CULTURE AND GLOBALIZATION. Globalization is the shift toward interdependent economies. The
fear is dilution of a national culture or an infringement of its values. This is a claim
about values, not efficiency, and economics has no special authority over it. Say that
plainly rather than dismissing it.

ENVIRONMENT AND RESOURCES. Countries differ in how stringent their environmental rules are,
so free trade can raise demand in exactly the places with the laxest standards, increasing
pollution and resource depletion. Flag this as a forward reference: a cost falling on people
outside the transaction is an externality, and that is the whole of Chapter 9 — next lecture.

INFANT INDUSTRIES. The most intellectually respectable of the five. Young firms are
vulnerable against established rivals; protection might let them reach scale, learn by
doing, and generate technological spillovers to a whole cluster. The book asks the right
follow-up question, so put it to the room: is a government well suited to pick which
technologies and firms will succeed, or are profit-seeking venture capitalists better at it?
The practical test for any real case: was an end date set, and did it hold?

LOCAL WAGES AND JOBS. The serious one, and the chapter's own question is about it. It gets
its own treatment three slides from now.

For the middle three the answer is the same general principle, worth stating once at full
strength: aim the policy at the problem. If pollution is the problem, tax the pollution —
including at home. A tariff addresses these clumsily, hits unrelated goods, and burns real
value on the way.""")

# =========================================================== 33. Exhibit 8.15
figpage("Exhibit 8.15 — The Effect of a Tariff",
        "A TARIFF is a tax added to the price of an imported product.",
        "ex815_tariff",
        "A $15 tariff lifts the Danish price from $25 to $40, and imports fall from 2.5 "
        "million pairs to 1 million.")
D.notes(prs.slides[-1], """The central diagram of Part 5, and the one that will be examined
as a drawing.

Same Danish market, importing at a world price of $25. The government adds a $15 tariff, so
the effective market price becomes $40.

At $40, read the curves separately. Danish supply rises from 0.75 to 1.5 million pairs — the
higher price makes more domestic production viable. Danish demand falls from 3.25 to 2.5
million. Imports therefore fall from 2.5 million pairs to 1 million.

Four things happen to the surplus, and the figure letters the ones that move.

E goes to Danish producers — a higher price on a larger domestic output.

I goes to the government: $15 a pair on the 1 million pairs still imported, which is $15
million. That is the number printed in the book.

G and J go to nobody. G is the production distortion: those extra pairs are now made in
Denmark at a cost above the $25 the world would have charged, so real resources are being
burned. J is the consumption distortion: pairs that Danes valued above $25 are simply not
bought. Together they are $11.25 million of deadweight loss.

The full letter algebra is in the book if you want it on the board: consumer surplus falls
from B + F + E + G + H + I + J to B + F + H, so consumers lose E + G + I + J. Producers gain
E. Government gains I. What is left over — G + J — is the loss.

Make the distinction sharp, because students blur it: E and I are TRANSFERS from Danish
consumers to other Danes. G and J are not transferred anywhere. They stop existing. You can
argue about who should get a transfer; there is no argument to have about G and J.

One observation students find striking: the government's revenue is not the main effect.
Most of what consumers lose goes to domestic producers, not the treasury — which is why a
tariff is a much better tool for protecting an industry than for raising money.

The book also carries Exhibit 8.16, the history of US import tariffs from 1891, with the
Smoot-Hawley Act of 1930 marked. Point students at it: tariffs were above 40% for much of
the nineteenth century and have been in single digits since the 1970s.""")

# ============================================ 34. the tariff ledger
s = S()
D.title(s, "Who Gets What When a Tariff Goes On")
D.cards4(s, 1.15, 2.32, [
    (GREEN, "E → producers", "A higher price on a larger domestic output. Danish "
     "shoemakers gain, and they are easy to identify."),
    (DGOLD, "I → government", "$15 a pair on the 1 million pairs still imported. Exactly "
     "$15 million."),
    (RED, "G → nobody", "The production distortion. Pairs now made in Denmark above the "
     "$25 the world would have charged."),
    (RED, "J → nobody", "The consumption distortion. Pairs Danes valued above $25 that "
     "are simply never bought."),
])
D.band(s, 3.62, "E and I are TRANSFERS between Danes. G + J = $11.25 million is not "
                "transferred anywhere — it stops existing.", kind="answer", size=14)
D.kicker(s, "G + J is DEADWEIGHT LOSS — surplus that no one receives, exactly as "
            "under a price control.", y=4.62)
D.notes(s, """The interpretation slide — this is where a student moves from drawing the
diagram to explaining it, and the explanation is what gets marked.

Take the four in order. E goes to domestic producers. I goes to the government and is
exactly $15 million — $15 a pair on the million pairs still imported. G and J go nowhere.

The distinction to make sharp: E and I are transfers. Danish consumers pay them and other
Danes receive them. You may think that fair or unfair, but it is a distributional question
and economics does not settle it. G and J are different in kind — nobody receives them.

G, concretely: those extra pairs are made in Denmark at a resource cost above what the world
would have charged. Real labour and materials burned to make something that could have been
bought for less. J: pairs that someone wanted at more than the world price and now does not
buy at all. The value never happens.

If you want the full algebra on the board it is in the book: consumer surplus falls from
B + F + E + G + H + I + J to B + F + H.

One observation students find striking: the government's revenue is not the main effect.
Most of what consumers lose goes to domestic producers, not the treasury — which is why a
tariff is a better tool for protecting an industry than for raising money, and why its
political history looks the way it does.""")

# ============================================ 34. EBE answered
s = S()
D.title(s, "Will Free Trade Cause You to Lose Your Job?")
y = D.band(s, 1.12, "Trade destroys jobs in the importing industry and creates them in "
                    "the exporting one.", kind="note", size=15)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (RED, "Some workers do lose", "Fewer shoes are made in Denmark once it imports them. "
     "That can depress wages or put cobblers out of work, and it is not hypothetical."),
    (GREEN, "But there is no broad harm", "There is no systematic evidence that opening "
     "up to trade harms workers as a whole. The wider gains offset much of the loss, so "
     "the net effect on jobs can be quite small."),
    (BLUE, "The catch is compensation", "In theory the winners can more than compensate "
     "the losers. In practice, complete compensation is difficult — and rarely required.",
     IC % "coin-stack"),
])
D.kicker(s, "Compensation is affordable in the model and rare in practice.", y=4.52)
D.notes(s, """The Evidence-Based Economics question, answered from the book.

Their answer, almost verbatim, is the middle card: some workers might lose their jobs, but
there is no systematic evidence that opening up to trade harms workers broadly.

The book anticipates the sharp student's objection and so should you. If the winners can
more than compensate the losers, why does it matter that wages fall and jobs are lost?
Can't we all still be better off? The book calls that a keen insight and theoretically
correct — and then says that in practice complete compensation of the losers is difficult.
That is the honest answer and it is worth giving in those terms.

Do not soften the first card. Someone in the room has watched a plant close.

The asymmetry worth naming: the gains are spread across everyone as slightly cheaper goods
and are largely invisible; the losses are concentrated on identifiable people in
identifiable places. Diffuse beneficiaries do not organise. Concentrated losers do.

Close on the kicker.""")

# ============================================ 35. practice problem
figpage("Practice — New England Textiles",
        "Equilibrium is $15 and 15 million units. Then China enters and the world price "
        "is $5.",
        "textiles",
        "With a $5 tariff the price is $10. Assume 10 workers produce 1 million units a "
        "year.")
D.notes(prs.slides[-1], """The book's Evidence-Based Economics problem, and it is the best
single assessment item in the chapter because it connects the diagram to the EBE question.

Set it up and then pause the recording, or tell students to pause, before the answers on
the next slide.

The questions: what are consumer and producer surplus initially? What are they at the world
price of $5? What are they with a $5 tariff? And how many fewer workers are employed under
free trade than under no trade?

Read the quantities off carefully with them. At $15, supply meets demand at 15 million
units. At the world price of $5, domestic supply is 5 million and demand is 25 million, so
imports are 20 million. With the $5 tariff the price is $10, domestic supply is 10 million
and demand is 20 million, so imports fall to 10 million.

Note that this is the same shape as the Danish tariff diagram with different numbers — say
so, because recognising that is the skill.""")

# ============================================ 36. practice answers
s = S()
D.title(s, "Practice — the Answers")
y = D.band(s, 1.12, "No trade at $15  →  free trade at $5  →  a $5 tariff at $10",
           kind="formula", size=15)
D.cards3(s, y + 0.26, 1.46, [
    (BLUE, "Domestic output", "15 million units with no trade. 5 million at the world "
     "price. 10 million once the tariff is on."),
    (GREEN, "Consumers", "Gain from opening: they buy 25 million units at $5 instead of "
     "15 million at $15. The tariff takes part of that back."),
    (RED, "Producers", "Lose from opening — domestic output falls by two-thirds. The "
     "tariff restores half of the fall."),
], body_size=11)
D.band(s, y + 1.86, "Employment: 150 workers with no trade, 50 under free trade — "
                    "100 fewer jobs in New England textiles.", kind="answer", size=14.5)
D.kicker(s, "Jobs lost in one industry, surplus gained across all consumers — the "
            "trade-off in one problem.", y=4.62)
D.notes(s, """The answers. Work the employment number on the board — it is the one that
matters and it is the one that connects to the EBE question.

Ten workers produce one million units a year. With no trade New England produces 15 million
units, so 150 workers. Under free trade at the world price of $5 it produces 5 million
units, so 50 workers. That is 100 fewer jobs.

Say it plainly: that is a real number, in a real region, and this is the textbook's own
problem — it is not a critic's example. The chapter is not hiding the cost.

And then the other half, with equal weight: consumers went from 15 million units at $15 to
25 million units at $5. The surplus gain is large and it is spread across everybody.

Both are true. That is the chapter, and it is why the answer to "will free trade cost you
your job" is neither yes nor no.

For the surplus algebra, the letters are in the book's answer key: initial CS is A and PS is
B + C + D; at the world price CS becomes A + B + C + E + F + G + H and PS is D; with the
tariff CS is A + B + E and PS is D + C, with G going to the government.""")

# ============================================================ 37. recap
s = S()
D.recap_table(s, "Chapter 8: The Full Picture", [
    ["The curve", "All you can make with the hours you have. Its slope is your cost.",
     "production possibilities curve", "Exhibits 8.1–8.2"],
    ["Who does what", "Do what costs YOU least — not what you are best at.",
     "comparative advantage, absolute advantage", "Exhibits 8.3–8.5"],
    ["The gains", "Specialise, then trade at a price between the two costs.",
     "specialization, terms of trade", "Exhibit 8.4"],
    ["Bigger units", "An economy holds many costs, so its curve bows outward.",
     "increasing opportunity cost", "Exhibits 8.6–8.8"],
    ["Countries", "Compare the world price with your own. Below it you import.",
     "world price, exports, imports", "Exhibits 8.12–8.14"],
    ["Protection", "A transfer to producers and government, plus a loss nobody gets.",
     "tariff, protectionism", "Exhibit 8.15"],
], "One idea, proved three times: people, states and countries all gain by doing what they "
   "give up least to do.")
D.notes(s, """Recap. Nothing new — the hour re-indexed so students can find things, and the
right-hand column now points at the book's exhibit numbers so they can revise straight from
the text.

Read the closing line out.

If you cut material today, leave this slide up while you say what got cut and where to read
it.

Point forward: this chapter assumed every cost of a transaction falls on the two parties
making it. Chapter 9 removes that.""")

# ============================================================ 38. takeaways
s = S()
D.takeaways_page(s, "Chapter 8: Trade", [
    "The production possibilities curve shows what you can make from the resources you "
    "have. Its slope is an opportunity cost.",
    "The basis for trade is comparative advantage — lowest opportunity cost — and never "
    "absolute advantage.",
    "Specialise and trade at a price between the two opportunity costs, and both sides "
    "end up beyond their own curve.",
    "There are winners and losers in every trading state and country, and which group "
    "loses depends only on which way the goods move.",
    "The winners can more than compensate the losers. Whether they do is a political "
    "question, not an economic one.",
])
D.notes(s, """Key takeaways — these are the book's own Key Ideas, in its order, so students
can match them to the text.

If they remember one thing, make it the third: two people, the same hours, the same skills,
and more of everything at the end.

The second is the examinable core and the one most often got wrong. The fifth is the honest
close, and it is the book's own framing.

Close on it rather than on a triumphant note. Everything today was a statement about totals.
The chapter proved the total gets bigger; it never proved everyone gains, and the diagrams
showed the losers from Exhibit 8.13 onwards.

Next: today every cost of a transaction fell on the two people making it. Next time somebody
outside the transaction pays part of the bill and the price stops telling the truth. That is
Chapter 9, externalities and public goods.""")

prs.save(OUT)
print(f"{OUT}: {len(prs.slides._sldIdLst)} slides")
