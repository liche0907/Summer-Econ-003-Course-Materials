#!/usr/bin/env python3
"""Build ECON003_Ch06_Sellers_and_Incentives_UCR.pptx  —  49 slides.

Built from the Ch05 deck to claude/slide-ground-rules.md.  Static — no animations, by rule.

Three things distinguish this deck from the first Ch06 build:
  * the running firm is a McDonald's franchise, not the publisher's Wisconsin Cheeseman;
  * two clip pairs — Zootopia opens the seller's problem, Mr. Plow closes the chapter;
  * the title triangle is the Chapter 4 market art reframed onto the SELLER.
"""
from pptx import Presentation

import deckkit as D
from deckkit import (BLUE, GOLD, DGOLD, GREEN, RED, INK, GREY, RULE,
                     TINT_NEUTRAL, TINT_GREEN, TINT_GOLD)

SRC = "/mnt/user-data/uploads/ECON003_26S/Slides/ECON003_Ch05_Consumers_and_Incentives_UCR_v2.pptx"
OUT = "ECON003_Ch06_Sellers_and_Incentives_UCR.pptx"
F = "figs/ch06_fig_%s.png"
IC = "icons/%s.png"
PH = "photos/%s_flat.png"
TITLE_ART = "title/ch06_title_triangle_seller.png"

ZOOTOPIA = "https://youtu.be/D7Z2GWMvjpU"
MRPLOW = "Video/Clips/[Peferct Competition]Mr Plow.mp4"

prs = Presentation(SRC)
D.drop_slides_after(prs, 1)
s1 = prs.slides[0]
D.retitle_title_slide(s1, ["Chapter 6", "Sellers and Incentives"],
                      ["ECON 003", "UC Riverside · Summer 2026"])

# The title picture keeps its inherited rtTriangle + flipH geometry; only the image
# behind it changes.  PowerPoint does the cutting, so feed it the framed 4:3 art.
for sh in list(s1.shapes):
    if sh.shape_type == 13 and abs(D.Emu(sh.left).inches - 6.70) < 0.05:
        part = sh.part.related_part(sh._element.blip_rId)
        part._blob = open(TITLE_ART, "rb").read()

D.notes(s1, """Title.

Chapter 6, Sellers and Incentives. This is Chapter 5 seen from the other side of the
counter, and the picture says so: it is the same market stall from the Chapter 4 title
slide, reframed onto the SELLER. Same transaction, other side of it.

Say at the top: everything in Chapter 5 built the demand curve from a buyer's problem.
Today we build the supply curve from a seller's problem, and by the end of the hour we
will have both halves of the diagram we have been drawing since Chapter 4 derived from
scratch.

One firm runs through the whole hour — a McDonald's franchise. The textbook runs the same
argument on a cheese factory with different numbers; the logic is identical, and the
bridging figures are in these notes wherever they matter.""")


def S():
    return D.blank_slide(prs)


# ============================================================== 2. where we left off
s = S()
D.title(s, "Where We Left Off")
y = D.defbox(s, 1.15, "In Chapter 5 you built the demand curve out of one buyer's problem.\n"
                      "Today you build the supply curve out of one seller's problem.")
D.cards3(s, y + 0.30, 1.80, [
    (BLUE, "The buyer's problem", "A budget line, a bang-per-buck rule, and a quantity "
     "for every price. Stack those up and you have a demand curve.", IC % "shopping-cart"),
    (RED, "The seller's problem", "A production function, a cost curve, and a quantity "
     "for every price. Stack those up and you get a supply curve.", IC % "factory"),
    (GREEN, "Same machinery", "Optimise at the margin. Keep going while the next unit "
     "adds more than it costs. Stop when they are equal.", IC % "balance-scale"),
])
D.kicker(s, "Chapter 4 asked you to trust the supply curve. Today you build it.", y=4.20)
D.notes(s, """Recap and framing.

One sentence of recap, no more: in Chapter 5 the demand curve stopped being an assertion
and became a result. Today the supply curve gets the same treatment.

Point at the middle card. The parallel is exact and worth naming out loud, because
students who see Chapter 6 as a fresh pile of definitions will drown in the vocabulary.
It is the same optimisation problem with the signs flipped.""")

# ===================================================================== 3. roadmap
s = S()
D.title(s, "Today's Roadmap")
D.strip5(s, 1.35, [
    ("1. Perfect\ncompetition", IC % "exchange"),
    ("2. The seller's\nproblem", IC % "factory"),
    ("3. To the\nsupply curve", IC % "up-down"),
    ("4. Producer\nsurplus", IC % "coin-stack"),
    ("5. Short run to\nlong run", IC % "clock"),
])
D.rect(s, 0.60, 3.15, 8.80, 0.06, fill=RULE)
D.cards2(s, 3.45, 1.30, [
    (BLUE, "Part 6 — entry and exit",
     "What happens to a profitable business when nothing stops anyone else copying it."),
    (GOLD, "And the question we open with",
     "An ethanol subsidy arrives. Who is better off a year later? Come back to it at the "
     "end and see whether your first answer survived."),
])
D.notes(s, """Roadmap.

Six sections, and they are not six separate topics. Parts 2, 3 and 4 are one continuous
argument — production, then costs, then the quantity the firm picks at each price, which
IS the supply curve, and then what the firm gains from trading at the market price.

Parts 5 and 6 change the time horizon and let the number of firms move. That is where the
chapter's punchline lives.

Announce the carried question here as well as on the next slide, so it is heard twice.""")

# ============================================ 4. the carried question (photograph)
s = S()
D.title(s, "A Question to Carry Through the Hour")
D.photo(s, PH % "corn_nozzle", 0.60, 1.12, 1.60, 3.85)
D.textbox(s, 2.55, 1.25, 6.85, 0.80,
          "Washington decides to subsidise ethanol — a payment to producers for every "
          "gallon they make.", size=15, bold=True, color=BLUE, line_pct=1.2)
D.rect(s, 2.55, 2.20, 6.85, 0.06, fill=GOLD)
D.textbox(s, 2.55, 2.42, 6.85, 0.60,
          "A year later, are ethanol producers better off?", size=15, bold=True,
          color=INK, line_pct=1.2)
D.cards2(s, 3.15, 1.35, [
    (GREEN, "The obvious answer",
     "Of course. The government is handing them money for every gallon. Costs fall, "
     "margins widen, profits rise."),
    (RED, "The reason to doubt it",
     "Nothing in this industry stops a new plant being built. Ask what that does to the "
     "price — and to the margin the subsidy just created."),
], width=3.35, xs=(2.55, 6.10))
D.image_credit(s)
D.notes(s, """The carried question. Pose it, do NOT answer it.

This is the chapter's cliffhanger, the same device as Chapter 4's eggs and Chapter 5's
smoker. It comes back at the end of the hour with real data.

Pause here. Take a show of hands on "better off / not better off" and write the split on
the board so you can come back to it. The room will split heavily toward "better off",
which is exactly what makes the ending land.

Do not explain the second card yet. Just plant it.

Say: hold that thought. To answer it properly we need to know how a firm decides what to
make, what it costs, and when it is worth being in the business at all — which is the
whole of today.""")

# ==================================================== PART 1 ======================
s = S()
D.divider(s, "PART 1", "Sellers in a Perfectly\nCompetitive Market")
D.notes(s, """Section divider — Part 1, Pearson section 6.1.

Short section, and it is scaffolding rather than content: it defines the market structure
every diagram today assumes. Tell them that explicitly, so they know it is a set of
assumptions and not a description of the world.""")

s = S()
D.title(s, "Three Conditions, One Benchmark")
y = D.defbox(s, 1.15, "A perfectly competitive market: many small buyers and sellers, "
                      "an identical product, and free entry and exit.")
D.cards3(s, y + 0.28, 1.90, [
    (BLUE, "Nobody is big enough",
     "So many buyers and sellers that no single one of them can move the market price by "
     "anything they do.", IC % "exchange"),
    (RED, "The product is identical",
     "One seller's unit is a perfect substitute for another's. Nobody can charge more by "
     "being different.", IC % "shipping-container"),
    (GREEN, "Anyone can come and go",
     "No licence, no patent, no barrier. Firms enter when there is money in it and leave "
     "when there is not.", IC % "up-down"),
])
D.kicker(s, "This is a benchmark, not a description. Very few real markets satisfy all three.",
         y=4.30)
D.notes(s, """The three conditions.

Get the honesty in early: this is a benchmark. Almost nothing satisfies all three
perfectly. It earns its place because it is the case where the answer is cleanest, and
because the further a real market sits from it, the more of Chapters 12 to 14 you need.

Closest real examples worth naming: commodity grain, foreign exchange at the retail level,
and a lot of online resale of identical goods.

A fair objection a student may raise, and you should welcome it: McDonald's is a BRAND, so
is it really in a perfectly competitive market? No — not perfectly. But the market for a
fast, hot, cheap lunch near campus is close enough that no single restaurant sets the going
price, and that is the assumption doing the work today. Say so rather than pretend.

The third condition is doing the heavy lifting. Conditions one and two set up Parts 2 to 4;
condition three is the whole of Part 6.""")

s = S()
D.title(s, "Price Takers — Quantity Is Your Only Lever")
y = D.defbox(s, 1.15, "A price taker treats the market price as given. It is a fact about "
                      "the world, not a decision the firm gets to make.")
D.cards2(s, y + 0.28, 1.85, [
    (BLUE, "What the firm decides", "Only ONE thing: how much to produce. Price is handed "
     "to it by the market and it takes that number as given.", IC % "factory"),
    (RED, "What happens if it tries", "Charge a bit more and you sell nothing — every "
     "buyer goes to an identical seller. Charge a bit less and you have thrown money away "
     "for no reason, because you could have sold everything at the market price.",
     IC % "price-tag"),
])
D.kicker(s, "Quantity is the firm's only lever. Everything today is about pulling it correctly.",
         y=4.35)
D.notes(s, """Price taking.

This is the single most load-bearing assumption in the chapter, and the one students
quietly stop believing by week ten. Say it plainly: for the next four weeks the firm
chooses a QUANTITY and nothing else.

The asymmetry in the second card is worth spelling out at the board. Raising the price
loses you every customer; cutting it is simply pointless. So there is exactly one price you
would ever post.

Chapter 4's Breaking Bad clip, if they saw it, is the counterexample — a seller who can
move the price. That is a price maker, and it is Chapter 12.""")

s = S()
D.title(s, "Identical Goods — and Why That Matters")
y = D.defbox(s, 1.15, "If nobody can tell one seller's unit from another's, nobody can "
                      "charge more than anybody else.")
D.cards3(s, y + 0.30, 1.90, [
    (RED, "Identical means no room on price",
     "Charge above the going rate and every buyer takes the identical thing from the "
     "seller next door. There is no loyalty to lose.", IC % "shipping-container"),
    (BLUE, "So price is the only competition left",
     "And price competition in this model runs all the way down to the cost curve. That "
     "is the whole result of the chapter.", IC % "price-tag"),
    (GREEN, "Which is why sellers try to escape it",
     "A product buyers believe is different buys a little room on price — and takes the "
     "firm out of this chapter entirely.", IC % "lightbulb"),
])
D.kicker(s, "Almost every marketing budget in the world exists to get a firm out of this "
            "chapter.", y=4.35)
D.notes(s, """Identical goods.

Ask the room for a product where they genuinely cannot tell the brands apart. Petrol, table
salt, unbranded flour, generic paracetamol, a kilowatt-hour. Then ask for one where they
obviously can, and notice how hard the seller worked to make that true.

The economics: if two firms really sell the same thing, the only competition left is price,
and price competition in this model runs all the way down to the cost curve. That is not a
side observation — it IS the result of the chapter, arriving early.

Line worth landing, and it is the kicker: almost every marketing budget in the world exists
to get a firm out of this chapter. Which tells you the chapter's conclusion is not one firms
enjoy.""")

s = S()
D.title(s, "Why Do Corn Farmers Build Grain Bins?")
y = D.defbox(s, 1.15, "A price taker cannot change the price it gets. It can sometimes "
                      "change WHEN it sells.", tint=TINT_GOLD, border=DGOLD, color=DGOLD)
D.cards3(s, y + 0.30, 1.85, [
    (RED, "Harvest is the worst moment",
     "Everyone's crop arrives at once, so supply spikes and the local price is at its "
     "lowest exactly when the farmer has grain to sell.", IC % "wheat"),
    (BLUE, "Storage buys an option",
     "Hold the grain and sell into a later, thinner market. The farmer still takes the "
     "price — just a different one.", IC % "shipping-container"),
    (GREEN, "It is not free",
     "Bins cost money, grain shrinks and spoils, and the later price might be worse. This "
     "is a bet, not an arbitrage.", IC % "coin-stack"),
])
D.kicker(s, "Being a price taker constrains what you can do. It does not make you passive.",
         y=4.30)
D.notes(s, """Grain storage — the publisher's live-classroom question.

Pause and take answers before revealing the cards. The good student answer is "to sell later
at a higher price", and the follow-up that earns the point is "and that still does not make
him a price setter."

The distinction to draw: choosing WHICH market to sell into is not the same as choosing the
price in a market. He is a price taker in September and a price taker in March.

Do not oversell the profitability of storage. The costs in the third card are real, and in
some years the later price is worse. If a student asks whether storage reliably pays, the
honest answer is that it depends on the shape of the futures curve, which is Chapter 12
material and beyond today.""")

s = S()
D.title(s, "Free Entry and Free Exit")
D.photo(s, PH % "serious_competition", 0.55, 1.15, 3.30, 2.80)
D.textbox(s, 4.25, 1.15, 5.15, 0.62,
          "Nothing legal or technical stops a new firm setting up — or stops one leaving.",
          size=14, bold=True, color=BLUE, line_pct=1.2)
D.cards2(s, 1.95, 1.30, [
    (GREEN, "Entry follows profit",
     "Profit is a signal, and in this model everybody can see it and anybody can act on "
     "it.", IC % "up-down"),
], width=5.15, xs=(4.25,))
D.cards2(s, 3.38, 1.28, [
    (RED, "Exit follows loss",
     "Firms losing money leave. Both movements push the market back toward the same place "
     "— which is what Part 6 is about.", IC % "exchange"),
], width=5.15, xs=(4.25,))
D.textbox(s, 4.25, 4.72, 5.15, 0.52,
          "Remember this one. It decides the ethanol question — and Homer's.",
          size=12, bold=True, color=INK, line_pct=1.15)
D.image_credit(s)
D.notes(s, """Free entry and exit. Flag this one hard.

This is the condition that answers the question posed on slide 4, and it is the one
students forget when they try to answer it. Everything in Part 6 comes from here — and so
does the Simpsons clip at the end of the hour.

The cartoon: a rival has opened directly across the street selling the same thing under a
slightly shinier name. That is entry, and nothing stopped it. Play it lightly and move on.

Counterexamples worth naming for contrast, because they are what the rest of the course is
about: a taxi medallion, a pharmaceutical patent, a banking licence, a broadcast spectrum
allocation. Each is a barrier to entry, and each is why the industry behind it does not
behave the way today's model says it should.

Do not develop the mechanism now. One sentence and move on — the payoff is forty minutes
away and it is better if they have to wait for it.""")

# ==================================================== PART 2 ======================
s = S()
D.divider(s, "PART 2", "The Seller's Problem")
D.notes(s, """Section divider — Part 2, Pearson section 6.2.

The long one, and it is worth saying so. Three questions, answered in order, and the third
cannot be answered until the first two are.

We open it with a film clip rather than a definition, because the clip contains the whole
section in ninety seconds and students will have the shape of it before the vocabulary
arrives.

Warn them the vocabulary comes thick and fast — six kinds of cost in about fifteen minutes.
Tell them the cost table is the slide to photograph.""")

# ---------------------------------------------------------- clip pair 1: Zootopia
s = S()
D.title(s, "How Do You Actually Start a Business?")
D.clip_page(
    s, "Zootopia",
    "Nick and Finnick buy one large popsicle, melt it down, refreeze it into dozens of "
    "small \"Pawpsicles\", and sell them to a queue of hot animals outside the bank.",
    ZOOTOPIA, url_label="youtu.be/D7Z2GWMvjpU",
    watch_for="Watch for three things: what they turn INTO what, what each Pawpsicle "
              "actually costs them, and why nobody in that queue walks away.")
D.notes(s, """Clip page 1 of 2. Play it, do not talk over it.

Why this clip is here: it is the entire seller's problem in ninety seconds, before a single
definition. Nick has to decide what to make, what it costs, and what he can get for it —
the three questions this section answers, in order.

Two sentences of setup before you press play: "Everything in this section is about a firm
deciding what to make and how much of it. Watch two foxes work that out from scratch, and
see if you can name the three decisions they make."

Keep the register analytical afterwards. The point is not that the scheme is clever; it is
that the scheme is a cost structure.

What NOT to claim: the film gives no prices and no costs. Do not quote a figure from it.
The numbers on the next slide are the deck's own round numbers, chosen to make the
arithmetic visible, and you should say so out loud.

One thing worth flagging for the sharp student who raises it: in the film the pair are
arguably not price takers — they are the only Pawpsicle seller outside that bank. True. That
is precisely why the margin is so wide, and precisely why Part 6 matters. Park it; the Mr.
Plow clip at the end pays it off.""")

s = S()
D.title(s, "What Nick Actually Built")
D.textbox(s, 0.60, 1.10, 8.80, 0.34,
          "Three decisions — and they are the three this whole section is about.",
          size=13, bold=True, color=BLUE, align="ctr")
D.cards3(s, 1.52, 1.42, [
    (BLUE, "1. Production", "One big popsicle in, dozens of small ones out. Melt, "
     "re-freeze, add a stick. That is a production function.", IC % "factory"),
    (RED, "2. Costs", "The stick and the melted syrup, and almost nothing else. The cost "
     "of ONE more Pawpsicle is tiny.", IC % "price-tag"),
    (GREEN, "3. Revenue", "A queue of overheated animals outside a bank. They are not "
     "walking to the next stall — because there isn't one.", IC % "coin-stack"),
])
D.picture_fit(s, F % "margin", 0.60, 3.04, 8.80, 1.72)
D.credit(s, "Illustrative round numbers — the film quotes no prices or costs.", y=4.80)
D.notes(s, """Clip page 2 of 2. This is the page students photograph.

Ask FIRST, before you show the bar: "why is that a good business?" Pause. Take answers. The
one you are steering toward is not "because he's clever" but "because the price is far above
what it costs him to make one more."

Then the diagram. Read the numbers as illustrative and say so — the film gives no figures.
Top bar: it costs about 20 cents to make one more Pawpsicle and he sells it for around two
dollars. That gap is the margin, and it is enormous.

Two forces make it wide, and both are on the slide:
  - COSTS are low, because the production step is trivial once you own the big popsicle.
  - DEMAND is high and unresponsive, because the customers are hot, they are already
    queuing, and there is no second stall. A buyer with no alternative does not haggle.

Now the sentence that sets up the whole hour: a wide margin is not a permanent fact about
Pawpsicles. It is a fact about how many people are selling them. Nothing in that scene stops
anyone else buying a big popsicle and standing on the next corner — which is the bottom bar.

Do NOT use this clip for supply elasticity. What the scene shows is inelastic DEMAND — a
captive queue — and the two elasticities are exactly what students confuse. Using it here
would make that worse.

Leave the bottom bar hanging. It is answered by the Simpsons clip in Part 6, and the
callback is the best moment in the lecture.""")

s = S()
D.title(s, "One Goal, Three Questions")
y = D.defbox(s, 1.15, "The seller's goal is to maximise profit. Getting there means "
                      "answering three questions, in order.")
D.picture_fit(s, F % "sellers_problem", 0.60, y + 0.18, 8.80, 2.10)
D.kicker(s, "You cannot answer \"how much should I make?\" until all three are answered.",
         y=4.35)
D.notes(s, """The structure of the whole section — the Pawpsicle scene, formalised.

Production, costs, revenues. Say the order matters: costs are derived from the production
function, and the profit-maximising quantity is derived from costs and revenue together. A
student who memorises the cost definitions without the production function behind them will
not be able to explain why ATC is U-shaped.

The fourth box — how much to make — is deliberately not on the diagram. It is the OUTPUT of
the other three, and it arrives on the profit-maximisation slide.

Point back at the clip: Nick answered all three in ninety seconds without naming any of
them.""")

s = S()
D.title(s, "Question 1: How Do You Make It?")
y = D.defbox(s, 1.15, "Production is the process that turns inputs into outputs. "
                      "Physical capital is any good — machine, building, fryer — used to "
                      "do it.")
D.cards3(s, y + 0.30, 1.85, [
    (BLUE, "Inputs", "Labour, capital, land, raw materials. The things that go in.",
     IC % "hard-hat"),
    (GREEN, "The technology", "The recipe: how much output a given bundle of inputs "
     "yields. Fixed for today.", IC % "research"),
    (RED, "Output", "What comes out and gets sold. Meals served, for the next forty "
     "minutes.", IC % "shipping-container"),
])
D.kicker(s, "How do you make a burger? Beef, a bun, a grill, and somebody who knows how.",
         y=4.30)
D.notes(s, """Production, and the vocabulary of inputs.

Physical capital is worth defining carefully, because students hear "capital" and think
money. In this chapter capital means the grill, not the loan that bought it.

Everything today holds the technology fixed. If the recipe improves — a faster fryer, a
better rota — the whole cost structure moves, and that is a different question.

Keep this brisk. It is a naming slide, and the table two slides on is where the work
happens.""")

s = S()
D.title(s, "Short Run and Long Run")
y = D.defbox(s, 1.15, "The short run is any period in which at least one input cannot be "
                      "changed. The long run is the period in which all of them can.")
D.cards2(s, y + 0.28, 1.85, [
    (RED, "Short run — the kitchen is fixed",
     "Serving lunch today, you are stuck with the grills and the floor space you already "
     "have. The only lever is how many people you roster.", IC % "clock"),
    (GREEN, "Long run — nothing is fixed",
     "Given enough time you can add a second drive-through lane, take the unit next door, "
     "or close the restaurant entirely.", IC % "house"),
])
D.kicker(s, "These are not clock times. They are defined by what you can still change.",
         y=4.35)
D.notes(s, """Short run and long run — and the definition students get wrong.

The single most common error in this chapter: treating the short run as "a few months" and
the long run as "a few years". They are not calendar periods. The short run is whatever
stretch of time leaves something fixed.

Concrete contrast worth saying: for a food truck the long run might be six weeks. For a
nuclear power station it is a decade. Same definition, wildly different clock times.

Standard exam trap: "is rent a fixed cost?" On a signed lease in the short run, yes. Over a
horizon long enough not to renew, no. The answer is always "over what period?"

Parts 2 to 4 are entirely short run. Part 5 switches. Say so now, because when the cost
curves change shape in Part 5 students will think they have been contradicted.

Setting up the next slide: because the kitchen is fixed, the only way to serve more meals
today is to put more people in the same kitchen. Hold that thought — it is the whole reason
marginal product eventually falls.""")

s = S()
D.title(s, "Fixed and Variable Factors")
D.cards2(s, 1.20, 1.55, [
    (RED, "Fixed factor of production",
     "An input that cannot be changed in the short run, and that stays the same no matter "
     "how much you produce. The building. The fryers.", IC % "house"),
    (GREEN, "Variable factor of production",
     "An input you can change within the period, and that moves with the level of output. "
     "Crew hours, beef, buns, power.", IC % "hard-hat"),
])
D.band(s, 3.00, "Every input is one or the other — and which one it is depends entirely on "
                "the length of the run.", kind="formula", size=13)
D.cards2(s, 3.75, 0.95, [
    (BLUE, "In the short run", "Kitchen fixed, crew variable."),
    (BLUE, "In the long run", "Everything variable, including whether you exist."),
])
D.notes(s, """Fixed and variable factors. A naming slide — the one idea worth dwelling on is
in the band.

The SAME input is fixed or variable depending on the run. That is what the band is doing
there.

Standard exam trap: "is rent a fixed cost?" On a signed lease in the short run, yes. Over a
horizon long enough not to renew, no. The answer is always "over what period?"

Setting up the next slide: because the kitchen is fixed, the only way to serve more meals
today is to put more people in the same kitchen. Hold that thought — it is the whole reason
marginal product eventually falls.""")

# ------------------------------------------------------------- production, McDonald's
s = S()
D.title(s, "Production at McDonald's")
rows = [["Workers", "Meals per hour", "Marginal product"]]
prod = [(0, 0, "—"), (1, 5, "+5"), (2, 15, "+10"), (3, 30, "+15"), (4, 42, "+12"),
        (5, 52, "+10"), (6, 60, "+8"), (7, 65, "+5"), (8, 67, "+2"), (9, 63, "−4"),
        (10, 55, "−8")]
for n, q, mp in prod:
    rows.append([str(n), str(q), str(mp)])
D.table(s, 0.60, 1.12, 3.55, 3.16, rows, col_w=[1.05, 1.40, 1.10],
        header_size=9, body_size=9.5, align=["ctr"] * 3)
D.picture_fit(s, F % "production", 4.40, 1.12, 5.00, 3.16)
D.kicker(s, "One kitchen, one set of grills, and workers added one at a time.", y=4.42)
D.notes(s, """The production table and the production function. Same data, two views.

READ THESE OUT: the 3rd worker adds 15 meals, the most of any worker. Output peaks at 67
meals an hour with 8 workers. The 9th worker takes output DOWN by 4, and the 10th by 8.

Everything is held constant except the number of workers — same kitchen, same grills. That
is what makes this the SHORT run.

The link to make explicit: the SLOPE of the curve on the right is marginal product. Steep
slope means a big marginal product; flattening means it is falling; the peak is where
marginal product hits zero; past the peak it is negative.

Say that sentence carefully, because the same relationship appears twice more today — total
cost and marginal cost, total revenue and marginal revenue. Marginal is always the slope of
total.

Ask: how many workers would this restaurant ever hire? Never more than 8, at any wage above
zero. Get that from the room rather than telling them.

BRIDGE TO THE TEXTBOOK: Acemoglu runs this identical argument on a cheese factory. Their
table peaks at 1,934 boxes a day with 38 workers and the 39th takes it down by 100. Same
shape, same three lessons, bigger numbers. If a student is revising from the book, tell them
to map worker 3 here onto worker 4 there — the peak of marginal product.""")

s = S()
D.title(s, "Marginal Product: Rise, Fall, Negative")
yb = D.band(s, 1.12, "Marginal product = the change in total output from adding one more "
                     "worker.", kind="formula", size=13)
D.picture_fit(s, F % "marginal_product", 0.60, yb + 0.10, 8.80, 1.98)
D.cards3(s, 3.78, 1.52, [
    (GREEN, "Rises — specialisation", "Switching between jobs wastes time. Split the work "
     "and each person gets good at half of it."),
    (BLUE, "Falls — diminishing returns", "Not because later workers are worse. Because "
     "the kitchen they share is fixed."),
    (RED, "Turns negative", "Enough people in one kitchen and they start getting in each "
     "other's way."),
], body_size=10)
D.notes(s, """Marginal product — the conceptual heart of the production section.

THE NUMBERS: +5, +10, +15, then +12, +10, +8, +5, +2, then −4 and −8.

Walk the three colours, but get the WHY from the room before you reveal the cards. Ask why
the 4th worker adds less than the 3rd. The answer is on the tip of most tongues and it lands
better if a student says it.

The phrase to protect them from is "workers get worse". They do not. Every worker is
identical by assumption. What falls is the amount of kitchen each of them has to work with.

The word EVENTUALLY in the law of diminishing returns matters. It does not say the first
worker is the most productive — here the third is. It says the fall must come at some point.

Head off the confusion now and again in Part 5: diminishing returns is a SHORT-RUN idea and
needs a fixed input. Diseconomies of scale, later, is a LONG-RUN idea where nothing is
fixed. Different concepts, different diagrams.

OPTIONAL 60-SECOND CLIP, if the room wants intuition rather than arithmetic: the Witcher
scene where Geralt calls off Ciri's training — more hours today will yield smaller and
smaller gains, so rest is worth more than the next repetition. Two caveats if you use it:
her skill is not a fixed factor in the way a kitchen is, and the scene is closer to fatigue
than to diminishing returns proper. Play it as an analogy, then come straight back to the
table, which is the examinable version.""")

s = S()
D.title(s, "Three Things This Table Says")
D.cards3(s, 1.20, 2.05, [
    (GREEN, "1. It rises at first — specialisation",
     "One person doing everything wastes time switching tasks. Two can split the work and "
     "each get good at half of it. That is why workers 2 and 3 each add more than the one "
     "before.", IC % "cook"),
    (BLUE, "2. Then it falls — diminishing returns",
     "At some point each extra worker adds less than the one before. Not because he is "
     "worse, but because the kitchen he works in is fixed and there is less of it to go "
     "round.", IC % "up-down"),
    (RED, "3. It can go negative",
     "Keep adding people to the same kitchen and eventually they get in each other's way. "
     "The 9th worker takes output DOWN by 4 meals.", IC % "factory"),
])
D.band(s, 3.50, "The law of diminishing returns: with at least one input fixed, each "
                "additional unit of a variable input eventually adds less than the one "
                "before it.", kind="formula", size=13)
D.notes(s, """The three lessons, stated as a law.

Diminishing returns is the one to get right, and the phrase to protect them from is "workers
get worse". They do not. The workers are identical by assumption. What falls is the kitchen
available per worker.

The word EVENTUALLY in the law matters. It does not say the first worker is the most
productive — here the third is. It says the fall must come at some point.

The negative stretch is not a curiosity. It is why no restaurant would ever roster the 9th
worker even if labour were free, and it is why the production function turns over.

Common exam confusion to head off now: diminishing returns is a SHORT-RUN idea and needs a
fixed input. Diseconomies of scale, in Part 5, is a LONG-RUN idea where nothing is fixed.
Different concepts, different diagrams. Say it now and again in Part 5.""")

# ----------------------------------------------------------------------- costs
s = S()
D.title(s, "What Does It Cost?")
y = D.defbox(s, 1.15, "Total cost = variable cost + fixed cost.\n"
                      "Which is which depends on the length of the run.")
D.cards2(s, y + 0.28, 1.80, [
    (RED, "Fixed cost (FC)",
     "The cost of the fixed factors. The same at zero meals as at a hundred — the rent, "
     "the fryers, the insurance, the loan. Also called overhead. Here: $100 an hour.",
     IC % "house"),
    (GREEN, "Variable cost (VC)",
     "The cost of the variable factors. Moves with output — the crew on shift, the beef, "
     "the buns, the power for the grills.", IC % "hard-hat"),
])
D.kicker(s, "$100 an hour of overhead, paid whether or not a single customer walks in.",
         y=4.35)
D.notes(s, """Costs — the two primitives.

Say the fixed cost clearly: one hundred dollars an hour, and it is paid at zero output. That
is not a technicality; it is the entire shutdown argument in Part 3, and saying it now stops
the result being a surprise later.

Ask the room to sort a few items live. Beef patties — variable. The rent — fixed. The crew
on shift tonight — variable. The manager's salary — fixed, in the short run. The electricity
— mostly variable, some fixed. That last one is a good answer to accept, because real costs
are not always tidy.

BRIDGE: the textbook's cheese factory uses $200 a day of fixed cost and $72 per worker. Same
structure, different figures.""")

s = S()
D.title(s, "Four Averages and a Margin")
D.cards4(s, 1.18, 1.72, [
    (GREEN, "Average total cost (ATC)", "Total cost ÷ output.\nWhat the average meal "
     "costs, all in.", IC % "ledger"),
    (DGOLD, "Average variable cost (AVC)", "Variable cost ÷ output.\nWhat the average "
     "meal costs to actually make.", IC % "hard-hat"),
    (BLUE, "Average fixed cost (AFC)", "Fixed cost ÷ output.\nOverhead spread over the "
     "meals. Always falls.", IC % "house"),
    (RED, "Marginal cost (MC)", "Change in total cost ÷ change in output.\nWhat the NEXT "
     "meal costs.", IC % "price-tag"),
])
D.band(s, 3.08, "ATC = AVC + AFC        and        MC = ΔTC / ΔQ", kind="formula", size=15)
D.kicker(s, "Averages tell you how you have done. The margin tells you what to do next.",
         y=4.18)
D.notes(s, """The cost vocabulary. Six terms in one slide — go slowly and use the band.

The line at the bottom is the one to make them write down. Averages are backward looking;
they describe what has already happened. Marginal cost is the only one that answers a
decision, and every decision in this chapter is made with it.

ATC = AVC + AFC is worth deriving out loud rather than asserting: divide TC = VC + FC through
by Q. Ten seconds, and it stops the identity looking arbitrary.

AFC always falls, because a fixed number divided by a rising one falls. That is "spreading
the overhead", and students already have the intuition from anything they have organised — a
group order, a shared flat, a party with a fixed room hire.""")

s = S()
D.title(s, "The Cost Table")
rows = [["Meals\nper hour", "VC", "FC", "TC", "AVC", "AFC", "ATC", "MC"]]
cost = [(0, 0, 100), (10, 30, 130), (20, 50, 150), (30, 65, 165), (40, 77, 177),
        (50, 87, 187), (60, 100, 200), (70, 120, 220), (80, 160, 260),
        (90, 220, 320), (100, 300, 400)]
prev_vc = 0
for q, vc, tc in cost:
    if q == 0:
        rows.append(["0", "$0", "$100", "$100", "—", "—", "—", "—"])
    else:
        rows.append([str(q), f"${vc}", "$100", f"${tc}", f"${vc/q:.2f}",
                     f"${100/q:.2f}", f"${tc/q:.2f}", f"${(vc-prev_vc)/10:.2f}"])
    prev_vc = vc
D.table(s, 0.45, 1.10, 9.10, 3.10, rows,
        col_w=[1.20, 1.05, 1.05, 1.15, 1.15, 1.15, 1.15, 1.20],
        header_size=9, body_size=9.5, align=["ctr"] * 8)
D.band(s, 4.32, "Every column after the fourth is computed from the first four. Nothing "
                "here is assumed.", kind="answer", size=12)
D.notes(s, """The cost table. Tell them to photograph this slide.

READ THESE OUT: fixed cost is $100 at every level including zero meals. At 80 meals: VC $160,
TC $260, ATC $3.25, AVC $2.00, MC $4.00.

Walk ONE row by hand — doing one live is worth more than describing all eleven. Take 70
meals: variable cost $120, plus fixed $100, gives total cost $220. Divide by 70 meals and the
average is $3.14. The last $20 of variable cost bought the last 10 meals, so marginal cost is
$2.00 a meal.

Three numbers from this table run the rest of the hour, so point at them now:
  - MINIMUM AVC is $1.67, at 60 meals. That will be the shutdown price.
  - MINIMUM ATC is $3.14, at 70 meals. That will be the long-run price.
  - MC is at its lowest, $1.00, at 50 meals.

One honest note if a sharp student checks: because the table steps in tens, MC does not cross
AVC and ATC exactly at a tabulated row — the crossing falls between rows. With a continuous
curve it lands exactly on the minimum, which is what the next slide draws. Say it if asked;
do not volunteer it.

BRIDGE: the textbook's cheese factory has min AVC $0.65 at 558 boxes and min ATC $0.90 at
1,019 boxes, where MC is exactly $0.90 too.""")

s = S()
D.title(s, "Marginal Cost")
y = D.defbox(s, 1.15, "Marginal cost is the change in total cost from producing one more "
                      "unit of output.")
yb = D.band(s, y + 0.20, "MC  =  ΔTC / ΔQ        —        what the NEXT meal costs, not "
                         "what the average one cost", kind="formula", size=15)
D.cards3(s, yb + 0.18, 4.44 - (yb + 0.18), [
    (GREEN, "MC falls while MP rises", "Early on each worker adds more meals for the same "
     "wage, so each meal costs less.", IC % "coin-stack"),
    (RED, "MC rises while MP falls", "Later each worker adds fewer meals for the same wage, "
     "so each meal costs more.", IC % "up-down"),
    (BLUE, "MC is a mirror of MP", "Marginal cost is upside-down marginal product: same "
     "story, different units.", IC % "exchange"),
], body_size=11)
D.kicker(s, "MC bottoms out at $1.00 — and then climbs to $8.00 by 100 meals.", y=4.54)
D.notes(s, """Marginal cost, and the identity that makes its shape obvious.

THE NUMBERS: MC bottoms at $1.00, at 50 meals. By 100 meals it is $8.00 — an eightfold climb
over the second half of the table.

The identity worth holding: marginal cost is the wage divided by marginal product. When the
denominator is at its biggest, the fraction is at its smallest. Students who hold that never
have to memorise the shape of the MC curve, because they already know the shape of marginal
product.

It works cleanly here because labour is the only variable input. Say that caveat — with two
variable inputs the relationship is messier.

Read one step off the table live: going from 70 meals to 80 adds $40 of variable cost for 10
more meals, so the marginal cost over that stretch is $4.00 a meal. That is the number the
profit-maximisation slide uses.""")

s = S()
D.title(s, "The Cost Curves")
D.picture_fit(s, F % "cost_curves", 0.60, 1.10, 8.80, 3.05)
D.kicker(s, "Marginal cost passes through the lowest point of each average curve. Always.",
         y=4.30)
D.notes(s, """The cost curves. The picture students will see for the next three chapters.

NUMBERS: AVC bottoms at $1.67 at 60 meals. ATC bottoms at $3.14 at 70 meals. MC bottoms at
$1.00 at 50 meals and then climbs steeply.

The result to state and then justify: MC passes through the minimum of each average curve.

The justification that works, and the next slide is built on it: if the next meal costs LESS
than the current average, it pulls the average down. If it costs MORE, it pushes the average
up. So the average is falling exactly while MC is below it and rising exactly while MC is
above it — and it must be flat where they cross.

Note the gap between ATC and AVC narrows as output rises. That gap IS average fixed cost, and
it shrinks because the overhead spreads over more meals.

Hold on to $1.67 and $3.14. They come back as the shutdown price and the long-run price, and
by the end of the hour students should be able to say what each one means without looking.""")

s = S()
D.title(s, "The Average Follows the Margin")
y = D.defbox(s, 1.15, "You already know this rule. You have just never called it that.",
             tint=TINT_GOLD, border=DGOLD, color=DGOLD, size=16)
D.cards2(s, y + 0.28, 1.85, [
    (BLUE, "The class average is 85%",
     "Somebody joins and scores 100. What happens to the average?\n\nIt rises — the new "
     "score was above it. Somebody joins and scores 34, and it falls.", IC % "research"),
    (GREEN, "A player averages 30 points a game",
     "He scores 45 tonight and the average rises. He scores 12 and it falls. He scores "
     "exactly 30 and it does not move.\n\nThat last case is where MC crosses ATC.",
     IC % "balance-scale"),
])
D.kicker(s, "A margin above the average pulls it up; below, it pulls it down; equal, it is "
            "flat.", y=4.35)
D.notes(s, """Why the average curves are U-shaped, in language nobody has to memorise.

This slide exists because "MC cuts ATC at its minimum" gets learned as a fact about a picture
rather than as arithmetic. Do the two examples out loud and let the room answer.

Then make the transfer explicit: marginal cost is the "next score". Average total cost is the
"average so far". While the next meal costs less than the average, the average falls. The
moment the next meal costs more, the average starts rising. So the lowest point of ATC is
exactly where the two are equal.

That is a complete proof and it takes thirty seconds. Once they have it, they never need to
memorise the shape of the cost curves again.

Push it one step if you have the room: this also tells you the U-shape of ATC is NOT caused
by fixed costs alone. AFC falls forever. What turns ATC back up is rising MC — which is
diminishing returns arriving from the production table.""")

s = S()
D.title(s, "Why the Average Curves Bend")
D.picture_fit(s, F % "cost_anatomy", 0.60, 1.10, 8.80, 2.62)
D.cards2(s, 3.86, 1.30, [
    (BLUE, "AFC falls forever", "$100 spread over more and more meals. It never turns up — "
     "it just flattens toward zero."),
    (GREEN, "ATC is the race", "Falling AFC pulls ATC down; rising AVC pushes it up. AVC "
     "wins in the end, and that is the U."),
], body_size=11)
D.notes(s, """Why the U-shape happens — the mechanism behind the picture.

This exists because "ATC is U-shaped" gets memorised without a cause, and then students
cannot say why the LONG-run curve in Part 5 is U-shaped for a completely different reason.

The story: two forces. Spreading the overhead pushes average cost down and never stops.
Diminishing returns pushes it up and gets stronger. At low output the first wins, at high
output the second does, and the turning point is the minimum — $3.14 at 70 meals.

Say clearly: AFC has no U in it. It falls forever. Anybody who draws a U-shaped AFC has
misunderstood.

The vertical gap between ATC and AVC is average fixed cost, and it narrows as output rises
for exactly that reason. The arrow on the figure marks it at 70 meals, where the gap is
$3.14 − $1.71 = $1.43, which is 100 ÷ 70.""")

s = S()
D.title(s, "Test Yourself: The $70 Room")
y = D.defbox(s, 1.15, "A friend's hotel costs $75 a night per room on average. In the "
                      "off-season somebody offers her $70 for a room. She refuses — it is "
                      "below her average cost. Was that right?",
             tint=TINT_GOLD, border=DGOLD, color=DGOLD, size=15)
D.cards2(s, y + 0.26, 4.26 - (y + 0.26), [
    (RED, "Her reasoning", "\"$70 is less than $75. Every room I let at $70 loses me $5. "
     "So I say no.\"", IC % "receipt"),
    (GREEN, "What is wrong with it", "Most of that $75 is the building, the front desk and "
     "the loan — costs she pays whether or not that room is occupied tonight. The MARGINAL "
     "cost of one more guest is the cleaning and the laundry. If that is under $70, she "
     "just refused free money.", IC % "lightbulb"),
])
D.kicker(s, "Decisions are made at the margin. Averages do not make decisions.", y=4.36)
D.notes(s, """The publisher's Test Your Understanding. Pause and take answers before
revealing the second card — this one usually splits the room, which is what makes it useful.

She was wrong. The right comparison is $70 against MARGINAL cost, not against average total
cost. If the marginal cost of one more occupied room is, say, $25 of cleaning and laundry,
she has turned down $45.

This is the first appearance of the argument that runs the whole of Part 3. The shutdown rule
is exactly this question asked about the whole business rather than one room.

Push it one step if the room is with you: is there ANY price at which she should refuse? Yes
— anything below the marginal cost of servicing the room. That is the AVC line, and it is
coming.

Do not let "ignore fixed costs" become the takeaway. Fixed costs matter enormously for
whether to be in the hotel business at all. They just do not matter for tonight's room.""")

# --------------------------------------------------------------------- revenue
s = S()
D.title(s, "Question 3: What Can You Sell It For?")
y = D.defbox(s, 1.15, "Revenue is the money the firm brings in from selling its product. "
                      "Total revenue = price × quantity.")
D.cards3(s, y + 0.30, 1.85, [
    (RED, "The firm does not set the price",
     "It is a price taker. The market hands it $4 a meal and that is the end of the "
     "negotiation.", IC % "price-tag"),
    (BLUE, "So revenue has one lever",
     "Total revenue = $4 × however many meals it chooses to serve.", IC % "register"),
    (GREEN, "And the next meal always adds $4",
     "Sell one more, get one more $4. Marginal revenue equals the price.",
     IC % "coin-stack"),
])
D.kicker(s, "For a price taker, and only for a price taker: MR = P.", y=4.30)
D.notes(s, """Revenue, and the two-panel picture.

Say the axis point before anything else, because it is where students get lost: the LEFT
panel measures the whole market, in thousands of meals. The RIGHT panel measures one
restaurant, in meals. One restaurant is a rounding error in its own market, which is exactly
why it cannot move the price.

Do the arithmetic out loud. Price $4. Sell one meal: $4. Two: $8. Three: $12. How much more
revenue from the third than the second? $4. Every time. So marginal revenue equals the price.

The horizontal line in panel (b) is simultaneously the demand curve facing this firm, its
marginal revenue curve, its average revenue curve, and the price. Four labels, one line. Say
that, because exam questions exploit it.

Flag the qualifier hard, because it is the most common error carried into Chapter 12: MR = P
is true FOR A PRICE TAKER. A firm that has to cut its price to sell more has marginal revenue
BELOW price. That is the whole of monopoly.""")

s = S()
D.title(s, "The Market and the Firm")
D.picture_fit(s, F % "market_and_firm", 0.60, 1.10, 8.80, 2.95)
D.kicker(s, "Two diagrams, two different x-axes. The market is in thousands of meals; the "
            "firm is in meals.", y=4.22)
D.notes(s, """The two-panel picture, and the axis warning.

Say the axis point before anything else, because it is where students get lost: the LEFT
panel measures the whole market, in thousands of meals. The RIGHT panel measures one
restaurant, in meals. One restaurant is a rounding error in its own market, which is exactly
why it cannot move the price.

Left panel: ordinary supply and demand, crossing at $4.

Right panel: the demand curve FACING THIS FIRM is horizontal at $4. That is what price taking
looks like drawn. Sell as many as you like at $4; try $4.01 and sell none.

The horizontal line is simultaneously the firm's demand curve, its marginal revenue curve,
its average revenue curve and the price. Four labels, one line. Say that, because exam
questions exploit it.

Do the arithmetic out loud if you did not on the previous slide: one meal $4, two $8, three
$12 — the third adds exactly $4, same as the second. MR = P.""")

s = S()
D.title(s, "Accounting Profit vs Economic Profit")
rows = [["An hour at the restaurant", "Cost type", "Amount"],
        ["Revenues", "", "$8,000"],
        ["Workers' wages", "Explicit", "$4,000"],
        ["Insurance and rent", "Explicit", "$2,500"],
        ["Food ingredients", "Explicit", "$1,000"],
        ["ACCOUNTING PROFIT", "", "$500"],
        ["Opportunity cost of the owner's time", "Implicit", "$300"],
        ["Opportunity cost of the owner's capital", "Implicit", "$400"],
        ["ECONOMIC PROFIT", "", "−$200"]]
D.table(s, 0.60, 1.10, 8.80, 2.75, rows, col_w=[4.60, 1.90, 2.30],
        header_size=10, body_size=10, align=["l", "ctr", "r"])
D.band(s, 4.00, "Economic profit = accounting profit − implicit costs.   The books say she "
                "made $500. The economics says she lost $200.", kind="flag", size=12.5)
D.notes(s, """The most important table in the chapter for conceptual understanding. Walk it
line by line.

THE NUMBERS: revenue $8,000. Explicit costs $4,000 + $2,500 + $1,000 = $7,500. Accounting
profit = $8,000 − $7,500 = $500. Then add the implicit costs: the owner's time $300 and her
capital $400, so total costs are $8,200. Economic profit = $8,000 − $8,200 = −$200.

Land the punchline slowly: the accountant says she made $500. The economist says she lost
$200. Both are right — they are answering different questions.

What the implicit costs ARE: the salary she gave up to run this place instead of taking a
job, and the return her money would have earned invested elsewhere. Real costs of choosing
this, even though no cheque is written.

The reading to give them for economic profit — and this is the sentence that makes Part 6
survivable: it is not "how much did I make", it is "how much better off am I than my next
best option". Positive means you chose well. Zero means you did exactly as well as the
alternative. Negative means you should have done the other thing, even though the cheques
cleared.

Every diagram from here on uses ECONOMIC profit. Say so now.""")

s = S()
D.title(s, "Corn or Soybeans?")
y = D.defbox(s, 1.15, "1,000 acres. Corn returns $50 an acre; soybeans would have returned "
                      "$40. The farmer plants corn.", tint=TINT_NEUTRAL, border=GREY,
             color=INK, size=15)
D.cards3(s, y + 0.26, 1.75, [
    (BLUE, "The accountant says $50,000",
     "$50 an acre × 1,000 acres. Money in, money out, and that is the number on the tax "
     "return.", IC % "ledger"),
    (GREEN, "The economist says $10,000",
     "Planting corn meant NOT planting soybeans, which would have returned $40,000. That "
     "forgone $40,000 is a real cost of the decision.", IC % "wheat"),
    (RED, "Both are right",
     "They are answering different questions. The accountant asks what happened; the "
     "economist asks whether it was the best available choice.", IC % "balance-scale"),
])
D.kicker(s, "Positive economic profit means: this was better than anything else you could "
            "have done.", y=4.30)
D.notes(s, """The textbook's corn-and-soybeans example. It runs through the rest of the
chapter, so get it clean now.

Numbers: $50 an acre for corn, $40 for soybeans, 1,000 acres. Accounting profit $50,000.
Economic profit $50,000 − $40,000 = $10,000.

Both accountants are right, and the third card matters — do not let this become "the
accountant is wrong". Different question, different answer.

The reading to give them for economic profit, and it is the same one the restaurant table
just gave: it is not "how much did I make", it is "how much better off am I than my next best
option".

This is the stylised version. The next slide is what the same decision actually looks like
this year — and it runs the other way.""")

s = S()
D.title(s, "Same Question, Real Numbers: Corn or Soybeans?")
D.picture_fit(s, F % "corn_soy", 0.60, 1.08, 8.80, 2.60)
D.band(s, 3.80, "Corn's accounting profit is positive. Its ECONOMIC return, once you count "
                "the soybeans you did not plant, is not.", kind="answer", size=12.5)
D.credit(s, "Returns: farmdoc daily 16:88, spring revision to the 2026 Illinois crop "
            "budgets, 19 May 2026, at $4.50 corn and $11.50 soybeans. Acreage: USDA NASS "
            "Acreage, 30 June 2026. Both figures live — re-check before delivery.",
         y=4.62)
D.notes(s, """Live slide. The same implicit-cost idea, on a decision somebody made this year.

READ THESE OUT. Central Illinois high-productivity soils, projected 2026: corn returns MINUS
$45 an acre, soybeans PLUS $67. Southern Illinois: corn minus $91, soybeans plus $30. Planted
acreage 2026: corn 95.3 million acres, down 3%; soybeans 85.4 million, up 5%.

The link to the previous slide: a farmer choosing corn gives up the soybean return. That
forgone return is an implicit cost of planting corn, exactly like the restaurant owner's
forgone salary. Right now it is a big one — about $112 an acre in central Illinois.

Then the payoff: farmers responded the way the model says they should. Corn acres down,
soybean acres up. That is the model predicting behaviour, not just labelling a table.

TWO THINGS A SHARP STUDENT WILL CATCH, and you should say both first:
1. "Operator and land return" is measured BEFORE land cost — cash rent or property tax. So a
   negative corn return does not mean farms are losing money outright. It means corn is not
   covering what the land could earn.
2. These are projections made in May 2026 at assumed prices of $4.50 corn and $11.50
   soybeans, not realised results. Front-month corn was $4.39 on 7 August 2026.

RE-CHECK BEFORE YOU TEACH THIS. The August WASDE lands 12 August 2026 with the first
survey-based corn yield of the season.""")

s = S()
D.title(s, "Walking Toward the Optimum")
y = D.defbox(s, 1.15, "Keep producing while the next unit brings in more than it costs. "
                      "Stop when they are equal.")
D.cards3(s, y + 0.28, 1.85, [
    (GREEN, "If MR > MC", "The next meal earns more than it costs. Make it. You are leaving "
     "money on the table if you stop.", IC % "up-down"),
    (RED, "If MR < MC", "The next meal costs more than it earns. Do not make it — and if "
     "you already did, make one fewer.", IC % "receipt"),
    (BLUE, "If MR = MC", "Nothing left to gain in either direction. That is the "
     "profit-maximising quantity.", IC % "balance-scale"),
])
D.kicker(s, "This is Chapter 3's marginal reasoning, and Chapter 5's bang per buck, again.",
         y=4.30)
D.notes(s, """The optimisation walk. Do this as a walk, not as a formula.

Start at a low quantity and ask: should you serve one more? At 30 meals, marginal cost is
$1.50 and the meal sells for $4. Obviously yes. Keep walking. At 80 meals the next one costs
$4.00 and earns $4.00 — and the question stops being obvious. That is the answer.

Name the callback: this is the same move as Chapter 5's "buy in order of bang per buck until
the budget runs out", and the same move as Chapter 3's optimisation in differences. Third
time they have seen it. Say so — the repetition is the point of the course.

The rule on the next slide is not a new idea. It is this walk written down.""")

s = S()
D.title(s, "The Profit-Maximising Rule")
D.band(s, 1.18, "MR  =  MC        and, because the firm is a price taker,        P  =  MC",
       kind="formula", size=17)
D.cards3(s, 2.08, 1.80, [
    (BLUE, "Step 1 — find the quantity",
     "Go along until MR meets MC. At $4 a meal, that is 80 meals an hour.", IC % "research"),
    (GREEN, "Step 2 — read off ATC there",
     "At 80 meals, average total cost is $3.25. That is what each meal cost, all in.",
     IC % "ledger"),
    (RED, "Step 3 — compare P with ATC",
     "P > ATC → profit. P < ATC → loss. P = ATC → break even, and no reason to be anywhere "
     "else.", IC % "balance-scale"),
])
D.kicker(s, "Three steps. Every profit question in this course is one of them.", y=4.18)
D.notes(s, """The rule and the three steps. The most examinable slide in the deck — tell them
to copy it verbatim.

NUMBERS: at P = $4 the optimal quantity is 80 meals, because MC at 80 is exactly $4.00. ATC
there is $260 ÷ 80 = $3.25.

Build it as a walk before you state it as a rule. Start low and ask: should you serve one
more? At 30 meals, MC is $1.50 and the meal sells for $4. Obviously yes. Keep walking. The
question stops being obvious exactly where the two are equal.

Emphasise the ORDER. Quantity first, from MR = MC. Only THEN look at ATC. Students who go
looking for the minimum of ATC and produce there are answering a question nobody asked —
that is the long-run outcome, not the short-run decision.

Warn about P = MC: it holds only because MR = P for a price taker. The general rule is
MR = MC.

Name the callback: this is the same move as Chapter 5's "buy in order of bang per buck", and
the same move as Chapter 3's optimisation in differences. Third time. The repetition is the
point of the course.""")

s = S()
D.title(s, "Seeing the Profit")
D.picture_fit(s, F % "profit_max", 0.60, 1.08, 6.35, 3.05)
D.cards2(s, 1.20, 1.50, [
    (GREEN, "The rectangle", "Height is P − ATC = $4.00 − $3.25 = $0.75.\nWidth is 80 "
     "meals.\nArea is the profit."),
], width=2.60, xs=(6.80,))
D.cards2(s, 2.85, 1.42, [
    (BLUE, "The arithmetic", "TR = 80 × $4 = $320.\nTC = $260.\nProfit = $60 an hour."),
], width=2.60, xs=(6.80,))
D.notes(s, """Profit as a rectangle.

NUMBERS TO READ OUT, not recall: P = $4.00. Q = 80 meals. ATC = $3.25. Total revenue
80 × $4 = $320. Total cost $260. Profit = $60 an hour.

Both routes give the same number and it is worth showing that: the rectangle is
(4.00 − 3.25) × 80 = $60, and revenue minus total cost is 320 − 260 = $60.

The habit to build: profit is ALWAYS this rectangle. Height is the vertical gap between price
and ATC AT THE CHOSEN QUANTITY; width is the quantity. It works for losses too, and in
fifteen minutes we use it for exactly that.

Common error to head off: reading the rectangle's height at the minimum of ATC rather than at
Q*. The height must be measured at 80 meals, where ATC is $3.25, not at 70 where it is $3.14.

BRIDGE: the textbook's cheese factory makes $248.25 a day at a price of $1.13 — same
rectangle, different numbers. (You may see $245 printed; that comes from rounding average
cost to $0.93 first. A student who answers $245 has done nothing wrong.)""")

# ==================================================== PART 3 ======================
s = S()
D.divider(s, "PART 3", "From the Seller's Problem\nto the Supply Curve")
D.notes(s, """Section divider — Part 3, Pearson section 6.3.

The payoff section. Everything so far has been machinery; here it becomes the supply curve
students have been drawing since Chapter 4.

Say the sentence when you reach the supply-curve slide: "In Chapter 4 I drew this curve and
asked you to trust it. You have just built it." Same beat as Chapter 5's demand curve.""")

s = S()
D.title(s, "Change the Price, Redo the Problem")
D.picture_fit(s, F % "three_prices", 0.60, 1.08, 8.80, 2.95)
D.band(s, 4.18, "$2 → 70 meals.    $4 → 80 meals.    $6 → 90 meals.    Three prices, three "
                "quantities — and every one of them is a point on MC.",
       kind="answer", size=12.5)
D.notes(s, """The moment the supply curve appears.

READ THE PAIRS: at $2 the restaurant serves 70 meals an hour. At $4, 80. At $6, 90. Each
comes from MR = MC, so each is a point ON the marginal cost curve.

The move to make explicit: we did not derive a new rule. We applied the same rule three times
at three prices. Price-quantity pairs are exactly what a supply curve IS.

So the marginal cost curve is the supply curve. Let that land — and then immediately undercut
it, because it is not true at every price, and the next fifteen minutes are about the
exception.

Ask the room directly before moving on: is there a price so low that you would serve nobody
at all? Most will say yes, and most will guess the threshold is where you start losing money.
That guess is wrong, and the fact that it is wrong is the best thing in this chapter.""")

s = S()
D.title(s, "So Marginal Cost Is the Supply Curve — Isn't It?")
y = D.defbox(s, 1.15, "At every price, the firm produces where P = MC. So the MC curve "
                      "gives quantity supplied at every price.", tint=TINT_GREEN,
             border=GREEN, color=GREEN)
D.cards2(s, y + 0.30, 1.85, [
    (GREEN, "True at the prices we tried", "$2, $4 and $6 all land on the MC curve, and all "
     "of them are quantities the restaurant would genuinely choose."),
    (RED, "But is it true at ALL prices?", "Is there a price so low that the restaurant "
     "would rather serve nobody at all than produce where P = MC? Hold that question — it "
     "is the shutdown decision, and we come back to it."),
])
D.kicker(s, "Park this. First: how much MORE do sellers make when the price rises?", y=4.35)
D.notes(s, """The setup for the shutdown decision — deliberately unresolved.

The publisher poses this question here and answers it much later, and the gap is doing work.
Leave it open.

Ask the room directly: is there a price so low you would serve nobody? Most will say yes, and
most will guess the threshold is where you start losing money. That guess is wrong, and the
fact that it is wrong is the best thing in this chapter.

Then park it and do elasticity, which is a short self-contained detour. Tell them it is a
detour so nobody thinks the thread has been dropped.""")

s = S()
D.title(s, "Price Elasticity of Supply")
y = D.defbox(s, 1.15, "The price elasticity of supply measures how responsive quantity "
                      "supplied is to a change in the market price.")
yb = D.band(s, y + 0.20, "ε_S  =  % change in quantity supplied  ÷  % change in price",
            kind="formula", size=15)
D.cards3(s, yb + 0.18, 4.26 - (yb + 0.18), [
    (GREEN, "Elastic:  ε_S > 1", "Quantity is very responsive. A 10% price rise brings out "
     "more than 10% extra."),
    (RED, "Inelastic:  ε_S < 1", "Quantity barely moves. A 10% price rise brings out less "
     "than 10% extra."),
    (BLUE, "Unit-elastic:  ε_S = 1", "They move together. A 10% price rise brings out "
     "exactly 10% extra."),
])
D.kicker(s, "Supply elasticity is normally POSITIVE — up with price, unlike demand.",
         y=4.36)
D.notes(s, """Elasticity of supply. Same machinery as Chapter 5, different curve — keep it
brisk.

The sign is the thing to flag. Demand elasticity is negative and we took absolute values.
Supply elasticity is naturally positive because the supply curve slopes up. A NEGATIVE supply
elasticity should make a student suspicious of their own arithmetic.

Middle panel arithmetic: price $5 to $6 is +20%, quantity 100 to 120 is +20%, so elasticity is
exactly 1. Worth knowing: ANY straight line through the origin is unit-elastic everywhere,
whatever its slope. That surprises people and it is a nice one-line result.

Use the midpoint formula from Chapter 5 for anything examinable — divide each change by the
AVERAGE of the two values, so you get the same answer in both directions.

WHAT MAKES SUPPLY ELASTIC — three determinants, worth saying even without a slide:
  1. Inventory on hand. A firm sitting on stock can push it out the moment price rises.
  2. How easily it can hire. If workers are available at the going wage, output scales.
  3. TIME, and this is the big one. Over a day almost nothing can change; over a year you can
     build a second kitchen. Supply is more elastic the longer the horizon.
That third one connects straight to Part 5 and to the oil slide at the end of this part.

Real approximations for the three extremes: perfectly inelastic is close to right for seats at
tonight's concert; perfectly elastic is close to right for one small farmer's wheat.""")

s = S()
D.title(s, "Three Extreme Cases")
D.picture_fit(s, F % "supply_elasticity", 0.60, 1.15, 8.80, 2.40)
D.cards3(s, 3.75, 1.15, [
    (GREEN, "Perfectly elastic", "Any amount at $5, nothing at $4.99. Horizontal."),
    (BLUE, "Unit-elastic", "+20% price, +20% quantity. A straight line through the origin."),
    (RED, "Perfectly inelastic", "100 units whatever the price. Vertical — a fixed stock, "
     "already produced."),
], body_size=10.5)
D.notes(s, """Three limiting cases.

Middle panel arithmetic: price $5 to $6 is +20%, quantity 100 to 120 is +20%, so elasticity
is exactly 1. Worth knowing: ANY straight line through the origin is unit-elastic everywhere,
whatever its slope. That surprises people and it is a nice one-line result.

Use the midpoint formula from Chapter 5 for anything examinable — divide each change by the
AVERAGE of the two values, so you get the same answer in both directions.

Real approximations, since the extremes never happen exactly: perfectly inelastic is close to
right for seats at tonight's concert, or a Picasso. Perfectly elastic is close to right for
one small farmer's wheat at the market price.

Contrast with Chapter 5's three extreme cases for demand if they saw them — same geometry,
opposite slope.""")

s = S()
D.title(s, "What Makes Supply Elastic?")
D.cards3(s, 1.20, 2.10, [
    (BLUE, "Inventory on hand", "A firm sitting on stock can push it out the moment the "
     "price rises. A firm with empty shelves has to make it first.",
     IC % "shipping-container"),
    (GREEN, "How easily it can hire", "If workers are available at the going wage, output "
     "scales quickly. If the skill is scarce, it does not.", IC % "hard-hat"),
    (RED, "Time — and this is the big one", "Over a day, almost nothing can change. Over a "
     "year, you can build a second kitchen. Supply is more elastic the longer the horizon.",
     IC % "clock"),
])
D.kicker(s, "The same market has a different supply elasticity depending on the window you "
            "ask about.", y=4.35)
D.notes(s, """Determinants of supply elasticity.

Time is the one that matters and the one that connects forward. Short-run supply is steep
because capital is fixed. Long-run supply is flatter because it is not. Same market, two
elasticities, and the only difference is how long you gave it.

Concrete: an oil price spike. Within a week, output barely moves. Within two years, rigs are
drilling. Within five, whole fields come online. Three elasticities for one commodity.

This card also previews the oil-patch slide at the end of this part, and Part 5's switch to
the long run.""")

s = S()
D.title(s, "Should You Harvest the Corn?")
y = D.defbox(s, 1.15, "The crop is grown. The seed, the fertiliser and the land are paid "
                      "for. The only question left is whether to run the combine.",
             tint=TINT_GOLD, border=DGOLD, color=DGOLD, size=15)
D.cards3(s, y + 0.28, 1.75, [
    (GREEN, "Corn at $4?", "Comfortably worth it. Harvest.", IC % "wheat"),
    (BLUE, "At $3?", "Still probably. What matters is whether it covers the diesel and the "
     "labour.", IC % "gas-pump"),
    (RED, "At $2?", "At some price the fuel to run the combine costs more than the corn in "
     "the tank. Then you leave it standing.", IC % "truck"),
])
D.kicker(s, "Notice what is NOT in the answer: everything you already spent getting here.",
         y=4.30)
D.notes(s, """The publisher's shutdown question. Pause and take answers.

The intuition arrives faster with corn than with a restaurant, which is why it goes first.
Every student can see that the seed money is gone regardless, and that the only live question
is diesel against grain.

Get them to say the comparison themselves: harvest if the corn is worth more than the cost of
harvesting it. That is P against average VARIABLE cost, and they have just derived the
shutdown rule without the vocabulary.

Do NOT give the rule yet. Three more slides.

The kicker is the point. What is absent from the decision is everything already spent — which
is the sunk cost idea, arriving shortly.""")

s = S()
D.title(s, "Stay Open or Shut Down: What Do You Still Pay?")
D.cards2(s, 1.20, 2.20, [
    (GREEN, "Stay open", "You pay your VARIABLE costs — the crew, the beef, the power — "
     "and you pay your FIXED costs.\n\nBut you also take in revenue.", IC % "factory"),
    (RED, "Shut down", "You pay no variable costs. Nobody is rostered, nothing is "
     "bought.\n\nYou still pay every penny of your FIXED costs. And you take in nothing.",
     IC % "house"),
])
D.band(s, 3.60, "Fixed costs are paid in BOTH columns. So they cannot decide between them.",
       kind="flag", size=14)
D.notes(s, """The two columns. This slide is the hinge of the whole argument — do not rush it.

Build it on the board rather than just showing it. Two columns, "stay open" and "shut down",
and fill in what you pay under each.

The moment to land: fixed costs appear in BOTH columns, identically. $100 either way. A cost
that is the same under both options cannot possibly tell you which to choose. It falls out of
the comparison entirely.

What is left is variable cost against revenue. That is the whole shutdown rule, and it is now
almost trivial.

Ask: so what WOULD make you close for the night? Answer: if the takings do not even cover
what you spend to open. Producing would then lose you MORE than the $100 you were going to
lose anyway.

A concrete version that always works: a restaurant open on a dead Tuesday night. Why bother?
Because the rent is owed either way, and if the tables that do come in more than cover the
food and the crew, the evening reduces the loss.""")

s = S()
D.title(s, "Losing Money and Still Opening the Doors")
D.picture_fit(s, F % "loss_but_open", 0.60, 1.08, 6.20, 3.05)
D.cards2(s, 1.15, 1.45, [
    (RED, "Shut down", "Revenue $0.\nVariable cost $0.\nFixed cost $100.\n"
     "Lose the whole $100."),
], width=2.75, xs=(6.65,))
D.cards2(s, 2.75, 1.60, [
    (GREEN, "Stay open at $2", "Revenue $140.\nVariable cost $120.\nFixed cost $100.\n"
     "Lose $80 — which is $20 better."),
], width=2.75, xs=(6.65,))
D.notes(s, """The resolution, and the counterintuitive result of the chapter.

READ THE ARITHMETIC OUT, slowly. Price $2, so the restaurant serves 70 meals.
  Revenue    70 × $2 = $140
  Variable   $120
  Fixed      $100
  Total cost $220, so a LOSS of $80.
Shut down instead: no revenue, no variable cost, but still $100 of fixed cost — a loss of
$100.

$80 is better than $100. The restaurant opens, loses money, and is right to.

Say the sentence: the $140 of takings covers all $120 of variable cost and leaves $20 to put
toward the overhead. Twenty dollars of the hundred gets covered. Close, and you cover none of
it.

This is the answer to the question posed at the top of the section. Pause on it. Students find
it genuinely surprising that "I am losing money" is not by itself a reason to close.

BRIDGE: the textbook runs the same case at $0.78 a box, where the cheese factory loses $110
rather than the $200 of fixed cost it would lose shut.""")

s = S()
D.title(s, "Sunk Costs")
y = D.defbox(s, 1.15, "A sunk cost has already been committed and can never be recovered. "
                      "It should not affect any decision you make from now on.")
D.cards3(s, y + 0.30, 1.80, [
    (RED, "In the short run, fixed costs are sunk",
     "The lease is signed, the fryers are bought. That money is gone whatever you decide "
     "tonight.", IC % "house"),
    (BLUE, "So they drop out of the decision",
     "Not because they do not matter — they matter enormously — but because they are the "
     "same under every option.", IC % "balance-scale"),
    (GREEN, "This is not just a firm problem",
     "The ticket you already bought. The two years already spent on the degree. The meal "
     "already paid for. Same logic, same error.", IC % "lightbulb"),
])
D.kicker(s, "\"But I've already spent so much on it\" is never, by itself, a reason to "
            "continue.", y=4.30)
D.notes(s, """Sunk costs.

Careful with the framing. Sunk costs do not "not matter". They matter for whether you should
have got into this in the first place, and for the long-run decision to stay in the industry.
They are irrelevant to THIS period's produce-or-not question, because they are identical under
both options.

The everyday examples in the third card are worth doing — the sunk cost fallacy is the one
piece of economics students take home and use.

Best version to say out loud: you paid $60 for a concert ticket, it is pouring with rain, and
you do not want to go. The $60 is gone either way. The only live question is whether going
tonight beats staying home tonight.

If someone raises "escapable" fixed costs — a lease you could sublet, equipment you could
resell — that is a good objection, and the honest answer is that those are not fully sunk. The
pure textbook case assumes they are.""")

s = S()
D.title(s, "The Shutdown Rule")
D.band(s, 1.15, "Shut down if  P  <  AVC.        Keep producing if  P  >  AVC.",
       kind="formula", size=17)
D.picture_fit(s, F % "shutdown", 0.60, 1.90, 6.10, 2.55)
D.cards2(s, 2.00, 1.20, [
    (RED, "Below $1.67", "Every meal loses money on its ingredients alone. Serving makes "
     "things worse. Serve nobody."),
], width=2.85, xs=(6.55,))
D.cards2(s, 3.35, 1.10, [
    (GREEN, "Above $1.67", "Every meal contributes something toward the overhead. Open, "
     "even at a loss."),
], width=2.85, xs=(6.55,))
D.notes(s, """The shutdown rule, stated.

THE NUMBER: minimum average variable cost is $1.67, at 60 meals an hour. That is the shutdown
price. Below it, serve nobody.

Say why the threshold is MINIMUM AVC and not just AVC: the firm gets to pick its quantity, so
it shuts down only if there is NO quantity at which price covers average variable cost. The
best chance is at AVC's lowest point. If price is below even that, no quantity works.

The two mistakes to name explicitly, because both are common in exams:
  - Shutting down whenever there is a loss. Wrong. Losses are survivable down to AVC.
  - Comparing P with ATC to decide. Wrong curve. ATC decides whether you are PROFITABLE; AVC
    decides whether you should be OPEN.

Shutdown is a SHORT-RUN decision to produce nothing this period. It is not exit. The firm
still exists, still owes its fixed costs, and reopens the moment the price recovers. Exit is
Part 6.

BRIDGE: the cheese factory's shutdown price is $0.65.""")

s = S()
D.title(s, "The Firm's Supply Curve")
D.picture_fit(s, F % "supply_curve", 0.60, 1.08, 8.80, 2.95)
D.band(s, 4.18, "The short-run supply curve is the portion of the marginal cost curve that "
                "lies above average variable cost.", kind="answer", size=13)
D.notes(s, """The answer to the question left open, and the moment the chapter pays off.

SAY THE SENTENCE: "In Chapter 4 I drew this curve and asked you to trust it. You have just
built it yourself." Same beat as the demand curve in Chapter 5.

What is on the picture: below $1.67 the quantity supplied is zero and the supply curve runs
down the vertical axis. At and above $1.67 it is the marginal cost curve. The kink is at
minimum AVC.

The market supply curve of Chapter 4 is the horizontal sum of these across all firms. One
sentence; it does not need a slide.

Worth flagging: this is the SHORT-RUN supply curve. The long-run one looks completely
different and arrives in fifteen minutes. Students who miss that will think Part 6 contradicts
this slide.""")

s = S()
D.title(s, "The Shutdown Rule in the Oil Patch")
D.picture_fit(s, F % "dallas_fed", 0.60, 1.05, 8.80, 2.80)
D.band(s, 3.95, "Existing wells keep running down to $26–$45. A NEW well needs $61–$70. "
                "The gap between them is AVC against ATC.", kind="answer", size=12.5)
D.credit(s, "Dallas Fed Energy Survey special questions, fielded 12–20 March 2025, "
            "published 26 March 2025 (n = 83 and 81). The March 2026 round moved the "
            "all-respondent averages to $43 and $66. WTI spot $78.18 on 7 August 2026.",
         y=4.68)
D.notes(s, """Live slide. The best evidence in the chapter — worth the time.

READ THESE OUT. The Dallas Fed asks oil producers two separate questions, and they are
literally AVC and ATC:
  - the WTI price needed to COVER OPERATING COSTS on existing wells: $26 in the Eagle Ford,
    $33 and $35 in the two Permian sub-basins, up to $45. Average $41.
  - the WTI price needed to PROFITABLY DRILL A NEW WELL: $61 to $70. Average $65.

Now run the shutdown rule across three episodes:
  - April–May 2020. WTI $17 to $29, BELOW the operating line. North Dakota production fell
    from 1.5 to 0.9 million barrels a day, of which about 0.4 million was voluntarily shut in
    beyond natural decline. Producing wells fell from about 16,000 to 12,800. (EIA, 20 August
    2020.)
  - 2025. WTI around $60 — BETWEEN the two lines. Nothing shut down, but new drilling stalled,
    and US output still hit a record near 13.8 million barrels a day because existing wells
    kept running.
  - Today, 7 August 2026. WTI $78, above both. Everything runs and new wells get drilled.

Same firms, same rule, three different outcomes, decided entirely by which side of which line
the price sat on.

THREE THINGS TO SAY BEFORE A STUDENT SAYS THEM:
1. The chart is the March 2025 round, because that is the most recent round publishing BOTH
   questions broken out by region. The 2026 round moved the averages to $43 and $66 — the
   shape is the same.
2. Shutting in a real well is not the frictionless switch of the model. Reservoir damage and
   re-entry costs mean the true trigger sits below the naive AVC number.
3. These are survey responses — what firms say they need, not audited accounts.""")

# ==================================================== PART 4 ======================
s = S()
D.divider(s, "PART 4", "Producer Surplus")
D.notes(s, """Section divider — Part 4, Pearson section 6.4.

Short section and the exact mirror of Chapter 5's consumer surplus. Lead with that: same
diagram, same triangle, other side of the price line.

If they remember consumer surplus, this takes eight minutes.""")

s = S()
D.title(s, "Producer Surplus")
y = D.defbox(s, 1.15, "Producer surplus is the difference between the price a seller "
                      "actually receives and the lowest price it would have accepted.")
D.cards2(s, y + 0.30, 1.90, [
    (BLUE, "The mirror of Chapter 5",
     "Consumer surplus was the gap between what a buyer WOULD have paid and what she did "
     "pay — the area under demand, above price.", IC % "shopping-cart"),
    (RED, "Producer surplus",
     "The gap between what a seller receives and what it would have accepted — the area "
     "above supply, below price.", IC % "coin-stack"),
])
D.kicker(s, "The supply curve is a marginal cost curve, so \"lowest acceptable price\" "
            "means marginal cost.", y=4.35)
D.notes(s, """Producer surplus, defined.

Lead with the symmetry. Consumer surplus was under the demand curve and above the price;
producer surplus is above the supply curve and below the price. Same picture, split by the
price line.

The kicker earns its place. Students accept "willingness to accept" as a phrase without
connecting it to anything. It is marginal cost — the supply curve already tells you the
lowest price at which each meal would be offered.

Flag now what the next slide proves: producer surplus is NOT profit. They differ by the fixed
cost. If nobody asks, say it anyway — it is a favourite exam question.""")

s = S()
D.title(s, "Measuring Producer Surplus")
D.picture_fit(s, F % "producer_surplus", 0.60, 1.08, 6.20, 3.05)
D.cards2(s, 1.12, 1.66, [
    (BLUE, "Meal by meal", "The 10th meal would have been served for $3 and earns $4. The "
     "80th costs exactly $4 and earns $4 — no surplus at all."),
], width=2.75, xs=(6.65,))
D.cards2(s, 2.92, 1.62, [
    (RED, "Not the same as profit", "Producer surplus $160.\nProfit $60.\nThe gap is "
     "exactly the $100 of fixed cost."),
], width=2.75, xs=(6.65,))
D.notes(s, """Producer surplus, and the distinction that gets examined.

NUMBERS: at a price of $4 the restaurant serves 80 meals. Revenue $320, variable cost $160, so
producer surplus is $160. Profit is $60. The gap between them is $100 — exactly the fixed
cost.

Lead with the symmetry. Consumer surplus sat under the demand curve and above the price;
producer surplus sits above the supply curve and below the price. Same picture, split by the
price line.

Why the supply curve is the right lower boundary: the supply curve IS marginal cost, so it
already tells you the lowest price at which each meal would be offered. Producer surplus is
the sum, over every meal, of the gap between what it fetched and what it cost to make.

THE EXAM POINT, and it is on the slide: producer surplus is revenue minus VARIABLE cost.
Profit is revenue minus TOTAL cost. In the short run they differ by exactly the fixed cost.
Students conflate them constantly. Make them write the $160 / $60 / $100 line down.

The marginal meal carries no surplus at all — the 80th meal costs exactly $4 and sells for
exactly $4. That is true on both sides of the market and worth saying once.""")

s = S()
D.title(s, "What a Price Rise Adds")
D.picture_fit(s, F % "ps_price_rise", 0.60, 1.10, 8.80, 2.75)
D.band(s, 4.05, "$4 → $6 takes producer surplus from $160 to $320. Sellers gain $160 — and "
                "buyers lose.", kind="answer", size=13)
D.notes(s, """The price rise.

NUMBERS: at $4 the restaurant serves 80 meals; revenue $320, variable cost $160, so producer
surplus is $160. At $6 it serves 90; revenue $540, variable cost $220, so producer surplus is
$320. The gain is $160.

Break the gain into its two pieces, because the decomposition is the examinable part:
  - most of it is extra money on meals it was already serving — 80 meals × $2 = $160 of extra
    revenue on the old quantity;
  - and the 10 extra meals bring in $60 while costing $60 of extra variable cost, so they add
    nothing net at the margin. The marginal unit never carries surplus.

Then the honest note: this is not a free gain to the world. Buyers are paying more. Chapter
5 showed the same price rise destroying consumer surplus. Put the two together and you have
Chapter 10, where we ask whether the total went up or down.

Say explicitly: producer surplus rising is not the same as society being better off.""")

# ==================================================== PART 5 ======================
s = S()
D.divider(s, "PART 5", "From the Short Run\nto the Long Run")
D.notes(s, """Section divider — Part 5, Pearson section 6.5.

The time horizon changes here and everything that was fixed becomes variable. Warn them before
the diagrams change shape.

In the short run you ask "how much should I make?" In the long run you ask "how big should I
be?" Two different questions, two different diagrams.""")

s = S()
D.title(s, "In the Long Run, Everything Is Variable")
D.cards2(s, 1.18, 2.05, [
    (RED, "Short run", "Some factors fixed. The only way to change output is to change "
     "LABOUR — more people in the same kitchen.\n\nThat is why diminishing returns bites, "
     "and why MC eventually rises steeply.", IC % "clock"),
    (GREEN, "Long run", "Nothing fixed. To change output you can change ANYTHING — take the "
     "unit next door, add a second line, move.\n\nThe long run is a planning period: what "
     "is the right SIZE of restaurant?", IC % "house"),
])
D.band(s, 3.45, "In the short run you ask \"how much should I make?\" In the long run you "
                "ask \"how big should I be?\"", kind="formula", size=14)
D.notes(s, """Short run to long run.

The band is the sentence to make them write down. Two different questions, and they get two
different diagrams.

Emphasise the planning framing: the long run is not a date in the future. It is the decision
problem you face when nothing is yet committed. A firm choosing its restaurant size is "in
the long run" even though it is choosing today.

Once the kitchen is built, the firm is back in the short run with that kitchen's cost curves.
Every firm lives in the short run and plans in the long run. That is exactly what the next
diagram shows.""")

s = S()
D.title(s, "The Long-Run Average Cost Curve")
D.picture_fit(s, F % "lrac", 0.60, 1.10, 8.80, 3.00)
D.band(s, 4.28, "Each grey curve is one possible restaurant size. The blue curve is the "
                "cheapest you can do at each output, once you can choose the size.",
       kind="answer", size=12.5)
D.notes(s, """The envelope, and the three regions.

How to walk it: each grey U is the short-run ATC of one possible restaurant size. Pick a level
of output, look down the grey curves, take the lowest. Do that at every output and you trace
the blue curve. Hence "envelope" — the long-run curve is never above any short-run curve,
because in the long run you could always have chosen that size.

THE CRITICAL DISTINCTION, and say it twice because it is the most confused pair in the
chapter:
  - Short-run ATC is U-shaped because of DIMINISHING RETURNS — a fixed input.
  - Long-run ATC is U-shaped because of ECONOMIES then DISECONOMIES OF SCALE — and there is
    nothing fixed at all. Everything scales up together and it still eventually gets worse.
Same shape, completely different cause. Exam questions live in that gap.

Concrete examples worth naming:
  - Economies: a semiconductor fab. Billions before a single chip is sold, so cost per chip
    falls steeply with volume. (Trade press puts a 2nm-class fab module at $25–35 billion; the
    WTO put a bleeding-edge fab at "well over $20 billion" in 2023. These are estimates, not
    company disclosures — attribute loosely.)
  - And the one we come back to in twenty minutes: the average US ethanol plant grew from
    about 34 million gallons a year in 2000 to about 96 million by 2023, while the number of
    plants stopped rising.
  - Diseconomies: any organisation where a decision now needs six approvals.

Note the blue curve is flat in the middle. That is constant returns, and it is why the
long-run supply curve turns out horizontal in Part 6.""")

s = S()
D.title(s, "Economies, Constant Returns, Diseconomies")
D.cards3(s, 1.18, 2.20, [
    (GREEN, "Economies of scale", "ATC FALLS as output rises. Double the inputs, more than "
     "double the output.\n\nWhy: large set-up costs get spread, and bigger operations "
     "specialise further.", IC % "factory"),
    (BLUE, "Constant returns to scale", "ATC is FLAT. Double the inputs, double the "
     "output.\n\nWhy: the gains from specialising have all been taken, and nothing has "
     "started going wrong yet.", IC % "exchange"),
    (RED, "Diseconomies of scale", "ATC RISES. Double the inputs, less than double the "
     "output.\n\nWhy: coordination. Too many layers of management, too far between the "
     "decision and the work.", IC % "manager"),
])
D.kicker(s, "Nothing is fixed here. This is NOT diminishing returns — that needs a fixed "
            "input.", y=4.42)
D.notes(s, """The three regions, named.

THE KICKER IS THE POINT, and it is the most confused pair in the chapter. Diminishing returns
needs a fixed factor and is short run. Diseconomies of scale has NO fixed factor and is long
run — everything scales up together and it still gets worse. Students merge these constantly.

Concrete examples worth naming:
  - Economies: a semiconductor fab. Billions before a single chip is sold, so cost per chip
    falls steeply with volume. (Trade press puts a 2nm-class fab module at $25–35 billion; the
    WTO put a bleeding-edge fab at "well over $20 billion" in 2023. These are estimates, not
    company disclosures — attribute loosely.)
  - The one we come back to in twenty minutes: the average US ethanol plant grew from about 34
    million gallons a year in 2000 to about 96 million by 2023, while the number of plants
    stopped rising. Economies of scale visible in an industry we are already discussing.
  - Diseconomies: any organisation where a decision now needs six approvals.

And say why the long-run supply curve in Part 6 comes out flat: the middle region. Where ATC
is flat, adding firms does not change anyone's costs.""")

# ==================================================== PART 6 ======================
s = S()
D.divider(s, "PART 6", "From the Firm to the Market:\nLong-Run Equilibrium")
D.notes(s, """Section divider — Part 6, Pearson section 6.6.

The last section, and it answers the question from slide 4. Everything here follows from the
third condition of perfect competition, which we set up forty minutes ago and have not used
since: free entry and exit.

Tell them that. And tell them the Pawpsicle question from Part 2 is about to be answered.""")

# ------------------------------------------------------------- clip pair 2: Mr. Plow
s = S()
D.title(s, "What Happens to a Good Business?")
D.clip_page(
    s, "The Simpsons — Mr. Plow",
    "Homer buys a snow plough and does very well out of it. Then somebody notices how well "
    "he is doing, and buys a snow plough.",
    MRPLOW, url_label="Video · Clips · Mr Plow.mp4",
    watch_for="Watch for the moment the business stops working — and note that nothing goes "
              "wrong. Homer does not make a mistake, and the snow keeps falling.")
D.notes(s, """Clip page 1 of 2. Play it, do not talk over it.

The file sits in Slides/Video/Clips/. The link on the slide is relative to the deck, so it
resolves if the deck is opened from the Slides folder; if it does not, open it from the
folder directly.

Why this clip is here, and why HERE rather than in Part 1: it is the free-entry condition
doing its work, and it is only worth watching once students have the machinery to say what
happened.

Two sentences of setup: "Forty minutes ago we said anyone can enter this kind of market. Watch
what that does to a business that is working beautifully. Notice that Homer does not do
anything wrong."

The callback to make BEFORE you press play, and it is the best moment in the lecture: remember
Nick's Pawpsicle margin. Same question, different animal. Watch what happens when the second
seller shows up.

Keep the register analytical. The joke is the vehicle; the mechanism is the subject.

What NOT to claim: no figures from the episode. Everything numerical on the next page is the
deck's own restaurant, carried through the whole hour.""")

s = S()
D.title(s, "Why Homer's Profit Vanished")
D.picture_fit(s, F % "entry", 0.60, 1.05, 8.80, 2.90)
D.band(s, 4.06, "Entry stops when P = minimum ATC = $3.14, because at that price there is "
                "nothing left to attract anybody.", kind="answer", size=12.5)
D.notes(s, """Clip page 2 of 2. The analysis, on our own restaurant.

Ask FIRST: what exactly went wrong for Homer? Take answers. The right one is "nothing". He was
not outcompeted on quality, he did not make a bad decision, and demand did not fall. Somebody
simply noticed the profit and copied him.

NUMBERS: price starts at $4 with the restaurant making $60 an hour. Entry shifts market supply
right. Price falls to $3.14, which is the MINIMUM of ATC, at 70 meals per restaurant. Economic
profit is then zero.

Why exactly minimum ATC, and not some other price? Because entry continues while profit is
positive, and profit is positive whenever price exceeds ATC at the chosen quantity. The only
price at which the firm can just break even is the one that touches ATC at a single point —
its minimum.

The sentence to land, and it is the chapter's thesis: the profit is not destroyed by bad luck.
It is destroyed by the RESPONSE to it. The profit existed, it was visible, and nothing stopped
anyone acting on it.

Two consequences worth saying:
  - Firms end up producing at the lowest possible average cost. Nobody planned that.
  - This is the strongest efficiency claim in the chapter, and Chapter 10 asks what it is
    worth.

Then close the Pawpsicle loop out loud: Nick's margin was wide because he was the only seller
outside that bank. Homer's margin was wide because he was the only plough in Springfield.
Neither is a fact about popsicles or snow. Both are facts about how many people are selling.""")

s = S()
D.title(s, "Profits Are a Signal — and Everybody Can See Them")
y = D.defbox(s, 1.15, "In the long run, firms can enter an industry or leave it. Nothing "
                      "legal or technical stands in the way.")
D.cards3(s, y + 0.28, 1.85, [
    (GREEN, "Corn returns $50, soybeans $40",
     "Economic profit of $10 an acre. Our farmer plants corn — and so does everybody else "
     "who can see the same numbers.", IC % "wheat"),
    (BLUE, "More corn gets planted",
     "Market supply of corn shifts right. And a supply curve shifting right means the price "
     "comes down.", IC % "up-down"),
    (RED, "Which shrinks the very profit that attracted them",
     "Entry continues while there is still an advantage to be had. It stops when there is "
     "not.", IC % "exchange"),
])
D.kicker(s, "The profit is not destroyed by bad luck. It is destroyed by the response to it.",
         y=4.30)
D.notes(s, """Entry generalised, on the example they already have.

Homer's plough was one firm. Run the same mechanism on the corn-and-soybeans numbers from
Part 2 so they see it is not a joke about snow: $50 corn against $40 soybeans is a $10 an acre
economic profit. Anyone can switch. Everyone switches. Corn supply rises, corn price falls,
and the $10 shrinks.

The kicker is the sentence to land, and it is the same one the clip page made. Nothing goes
wrong. Nobody is unlucky. The profit disappears precisely BECAUSE it existed, was visible,
and nothing stopped anyone acting on it.

Ask: when does the switching stop? When corn and soybeans return the same thing — because
then there is nothing to gain by moving. That is the equilibrium, and it is the next
slide.""")

s = S()
D.title(s, "Zero Economic Profit Is Not Zero Profit")
y = D.defbox(s, 1.15, "In long-run equilibrium, price equals minimum average total cost "
                      "and economic profit is zero.", tint=TINT_NEUTRAL, border=GREY,
             color=INK, size=16)
D.cards2(s, y + 0.28, 1.85, [
    (RED, "What it does NOT mean", "It does not mean the owner is broke, working for free, "
     "or should quit. She is being paid, and her capital is earning its normal return.",
     IC % "ledger"),
    (GREEN, "What it DOES mean", "There is nothing better available. Every alternative use "
     "of the same time, money and space returns exactly the same. She has no reason to "
     "move — and neither does anyone outside.", IC % "balance-scale"),
])
D.kicker(s, "\"Zero economic profit\" means \"doing exactly as well as the next best "
            "thing\" — which is fine.", y=4.35)
D.notes(s, """The single most misread result in the chapter.

Say it before they can misread it: zero economic profit does NOT mean zero income, and it does
not mean the business is failing. The owner is being paid. The capital is earning its normal
return. Those are COSTS in the economic accounting, and they have been paid in full.

What is zero is the EXCESS over the next best alternative.

Point back at the accounting-versus-economic-profit table. The restaurant owner there had $500
of accounting profit and MINUS $200 of economic profit. Zero economic profit sits between
those — a healthy accounting profit, exactly matching what she could earn elsewhere.

If a student asks why anybody bothers running a business for zero economic profit: because the
alternative also returns zero economic profit, by construction. The zero is a statement about
the comparison, not about the bank balance.""")

s = S()
D.title(s, "And Exit Works the Same Way")
D.picture_fit(s, F % "exit", 0.60, 1.05, 8.80, 2.90)
D.band(s, 4.06, "Demand falls, price drops to $2, restaurants lose money, some close — and "
                "the price climbs back to $3.14.", kind="answer", size=12.5)
D.notes(s, """Exit — the same mechanism running backwards.

NUMBERS: start in long-run equilibrium at $3.14. Demand shifts left; price falls to $2. At $2
each restaurant serves 70 meals and loses $80 an hour — the same arithmetic as the
staying-open slide. Note it does NOT close: $2 is above minimum AVC of $1.67. It stays open
and bleeds.

Then, over the long run, some restaurants close. Market supply shifts left. Price rises back
to $3.14 and the survivors break even again.

THE TWO DISTINCTIONS, which finally separate here:
  - SHUTDOWN is short run. Serve nobody this period, keep existing, keep owing the fixed
    costs, reopen when price recovers. Trigger: P < AVC.
  - EXIT is long run. Leave the industry, sell the fryers, owe nothing. Trigger: P < ATC
    persistently.
At $2 this restaurant does neither in the short run — it serves meals at a loss. But if $2 is
the new normal, in the long run it or somebody like it closes for good.

The symmetry with entry is the point. Same signal, same response, opposite sign.""")

s = S()
D.title(s, "Why Long-Run Supply Is Flat")
D.picture_fit(s, F % "lr_supply", 0.60, 1.05, 8.80, 2.90)
D.band(s, 4.06, "In the long run the price returns to minimum ATC whatever demand does. "
                "What changes is the NUMBER of firms.", kind="answer", size=12.5)
D.notes(s, """The horizontal long-run supply curve.

The result: demand can shift wherever it likes and the long-run price comes back to $3.14
every time. What absorbs the change is not the price — it is how many restaurants there are.

Why: any price above $3.14 attracts entry until it is competed back down; any price below
$3.14 drives exit until it is pushed back up. $3.14 is the only price that can persist.

This is the sharpest contrast in the chapter. Put the two sentences side by side:
  - SHORT-run supply slopes UP. The firm moves along its own marginal cost curve.
  - LONG-run supply is FLAT. The industry adds and removes firms instead.

The assumption underneath, and name it so it is not smuggled: every firm has the same cost
curves, and input prices do not change as the industry grows. Relax either and the long-run
supply curve slopes up somewhat. The flat case is what is examinable.

This is also the ethanol answer arriving a slide early. Let them notice before you say it.""")

# ============================================== the answer to the opening question
s = S()
D.title(s, "So: How Does an Ethanol Subsidy Affect Producers?")
y = D.defbox(s, 1.15, "A subsidy arrives. In the SHORT run, producers profit. In the LONG "
                      "run, entry competes it away — and the price falls by roughly the "
                      "subsidy.", tint=TINT_GREEN, border=GREEN, color=GREEN, size=15)
D.cards3(s, y + 0.28, 1.90, [
    (GREEN, "Short run — yes, they gain",
     "Cost per gallon falls by the subsidy. Existing plants are suddenly profitable and "
     "earn real economic profit.", IC % "coin-stack"),
    (BLUE, "Then entry happens",
     "Nothing stops a new plant being built. Profit is visible, so plants get built and "
     "supply rises.", IC % "factory"),
    (RED, "Long run — back to zero",
     "Price falls until economic profit is gone again. The producers who were there at the "
     "start captured the gain; the ones who came later did not.", IC % "up-down"),
])
D.kicker(s, "Take the show of hands again. Then ask who actually captured the subsidy.",
         y=4.38)
D.notes(s, """The answer to the question posed at the start of the hour.

Go back to the board and read out the show of hands from slide 4. Most of the room said
producers end up better off. The model says: only the ones who were already there when it was
announced, and only until entry catches up.

This is the third time today the same mechanism has run — Nick's Pawpsicles, Homer's plough,
and now a federal subsidy. Say that. One mechanism, three costumes.

The best discussion question in the chapter: if the subsidy does not end up with producers in
the long run, where does it go? Some to consumers through a lower price, and some capitalised
into whatever input is genuinely scarce — which in this industry is corn, and land. That is
why farmland values are part of the ethanol policy story.

Do not overclaim. This is the model's answer and it assumes free entry, identical firms and
constant input prices. Real ethanol has scale economies and rising corn prices, both of which
complicate it. The next slide is what actually happened.""")

s = S()
D.title(s, "What Actually Happened")
D.picture_fit(s, F % "ethanol_plants", 0.60, 1.05, 8.80, 2.85)
D.band(s, 4.02, "Plants: 54 in 2000 → 201 in 2019 → 187 by 2023. Entry, then a stop, then "
                "exit — with average plant size tripling throughout.",
       kind="answer", size=12)
D.credit(s, "Plants and capacity: DOE Alternative Fuels Data Center, 1999–2023, sourced to "
            "the Renewable Fuels Association and EIA. EIA counted 191 plants and 18,477 "
            "million gal/yr of capacity as of 1 January 2025.", y=4.86)
D.notes(s, """The evidence, redrawn and extended.

NUMBERS TO READ OUT: 54 plants in 2000. 201 in 2019, the peak. 187 by 2023. Average plant size
went from about 34 million gallons a year to about 96 million over the same period.

The two dashed lines are the policy events. January 2006: the "addicted to oil" State of the
Union. December 2011: the blender's credit expires.

BE PRECISE ABOUT THE 2006 SPEECH, because it is easy to overstate. Bush announced RESEARCH
FUNDING — a 22% increase in clean energy research and a cellulosic ethanol initiative. He did
not create the subsidy. The blender's credit came from the American Jobs Creation Act of 2004
at 51 cents a gallon, dropped to 45 cents in 2009, and expired at the end of 2011. The mandate
came from the Energy Policy Act of 2005 and was expanded in 2007. Say "Bush created the
ethanol subsidy" and a well-read student can correct you.

What the picture shows: a decade of entry, exactly as the model predicts. Then entry stops and
reverses. But note what does NOT stop — capacity keeps rising. The industry consolidated into
bigger plants. That is Part 5's economies of scale, visible in the same chart as Part 6's
entry and exit.

Honest caveat: the credit expiring at the end of 2011 and the plant count peaking in 2019 are
eight years apart. Do not draw a causal arrow. The mandate survived the credit and is still
setting volumes — EPA finalised 2026 and 2027 volumes in April 2026.

If asked whether ethanol is still subsidised: the blender's credit is gone. Since January 2025
there is a different instrument, the 45Z clean fuel production credit, which pays the PRODUCER
on a sliding scale by carbon intensity rather than a flat rate to the blender, and currently
runs to the end of 2029. Do not describe it as "the old credit at a dollar a gallon" — most
corn ethanol earns far less than the headline rate.""")

s = S()
D.title(s, "Practice: The Subsidy Is Cut")
y = D.defbox(s, 1.15, "Ethanol costs $1.25 a gallon to make, for every seller. Each plant "
                      "produces 2 million gallons. The subsidy is cut from 25¢ to 20¢ a "
                      "gallon.", size=15)
rows = [["Price", "Gallons (m)", "Price", "Gallons (m)", "Price", "Gallons (m)"]]
sched = [(1.40, 2), (1.35, 4), (1.30, 6), (1.25, 8), (1.20, 10), (1.15, 12),
         (1.10, 14), (1.05, 16), (1.00, 18), (0.95, 20), (0.90, 22), (0.85, 24)]
for i in range(4):
    r = []
    for j in range(3):
        p, q = sched[i + 4 * j]
        r += [f"${p:.2f}", str(q)]
    rows.append(r)
D.table(s, 0.60, y + 0.22, 8.80, 1.55, rows,
        col_w=[1.50, 1.45, 1.50, 1.45, 1.50, 1.40], header_size=9.5, body_size=10,
        align=["ctr"] * 6)
D.cards2(s, 4.00, 1.05, [
    (BLUE, "Work out", "(a) the new ATC   (b) profit at $1.00   (c) enter or leave?"),
    (BLUE, "Then", "(d) how many sellers in equilibrium   (e) economic profit there"),
])
D.notes(s, """Practice setup. Put it up, give them three or four minutes in pairs, then take
answers before the next slide.

What they need: ATC without any subsidy is $1.25. Each plant makes 2 million gallons. Old
subsidy 25 cents, new subsidy 20 cents. The market schedule is on the slide.

Nudge if they stall: a subsidy per gallon lowers the effective cost per gallon by exactly that
amount. So what does cutting it do to ATC?""")

s = S()
D.title(s, "The Answers")
D.picture_fit(s, F % "ethanol_subsidy", 0.60, 1.05, 5.70, 3.05)
D.cards2(s, 1.12, 1.55, [
    (GREEN, "(a)  New ATC = $1.05", "$1.25 − $0.20. The old 25¢ subsidy made it $1.00."),
], width=3.10, xs=(6.30,))
D.cards2(s, 2.78, 1.32, [
    (GREEN, "(b)  Loss of $100,000", "($1.00 − $1.05) × 2 million gallons. So (c) sellers "
     "LEAVE."),
], width=3.10, xs=(6.30,))
D.band(s, 4.22, "(d)  In equilibrium P = ATC = $1.05, so 16 million gallons ÷ 2 million per "
                "plant = 8 sellers.        (e)  Economic profit = 0.",
       kind="answer", size=12.5)
D.notes(s, """The answers. Walk each one.

(a) The subsidy falls 5 cents, so effective ATC rises 5 cents: $1.25 − $0.20 = $1.05. Under
    the old 25-cent subsidy it was $1.00.
(b) At the old price of $1.00 each seller now loses 5 cents a gallon on 2 million gallons = a
    loss of $100,000.
(c) Losses mean sellers leave.
(d) Exit continues until price equals ATC. P = $1.05. Read across the schedule: at $1.05 the
    market takes 16 million gallons. Divide by 2 million per plant: 8 sellers.
(e) Zero, by construction. That is what "long-run equilibrium" means.

Point out the shape of the answer: cutting the subsidy did not just shrink profits, it shrank
the INDUSTRY. That is the entry-and-exit margin doing the work, and it is exactly what the real
ethanol plant count did after 2019.

Sanity check to offer: at $1.05 with 8 sellers each making 2 million gallons, total output is
16 million — which matches the schedule. The answer closes.""")

# ==================================================== closing pair =================
s = S()
D.recap_table(s, "Chapter 6: The Full Picture", [
    ["Production", "Output rises with labour, then more slowly, then falls. The kitchen is "
     "fixed in the short run.", "marginal product, diminishing returns, specialisation",
     "The 3rd worker adds 15"],
    ["Costs", "TC = VC + FC. The average follows the margin, so MC passes through the low "
     "point of each average curve.", "FC, VC, ATC, AVC, AFC, MC",
     "min AVC $1.67, min ATC $3.14"],
    ["The rule", "Produce where MR = MC, and MR = P for a price taker. Then compare P with "
     "ATC.", "price taker, economic profit, implicit cost", "$4 → 80 meals → $60"],
    ["Supply", "Short-run supply is MC above AVC. Below minimum AVC, produce nothing.",
     "shutdown rule, sunk cost, ε_S", "$2 → lose $80, not $100"],
    ["Surplus", "The area above supply and below price — it exceeds profit by the fixed "
     "cost.", "producer surplus, willingness to accept", "$160 surplus, $60 profit"],
    ["The long run", "Entry and exit drive price to minimum ATC, so long-run supply is flat "
     "and profit is zero.", "economies of scale, free entry, long-run equilibrium",
     "Nick, Homer, and ethanol"],
], "Chapter 5 built the demand curve. Chapter 6 built the supply curve. "
   "Chapter 4's diagram is now derived from both sides.")
D.notes(s, """Recap. Nothing new — the hour re-indexed so students can find things.

Read the last line out. It is the real close: we have now built both curves of the supply and
demand diagram from individual optimisation problems, and neither is an assertion any more.

The right-hand column is deliberately numbers rather than exhibit references, because this
deck runs one firm the whole way through and those five figures are the spine of it.""")

s = S()
D.takeaways_page(s, "Chapter 6: Sellers and Incentives", [
    "The average follows the margin — which is why MC passes through the bottom of ATC.",
    "Produce where MR = MC. For a price taker MR = P, so produce where P = MC.",
    "Compare P with ATC for profit; compare P with AVC for whether to open at all.",
    "Fixed costs are sunk in the short run. They cannot decide anything.",
    "Free entry drives price to minimum ATC — and economic profit to zero.",
])
D.notes(s, """Key takeaways. Five, and the middle three are the examinable core.

If they remember only one thing, make it the third: two different curves answer two different
questions. ATC answers "am I making money?" AVC answers "should I be open?" Mixing them up is
the most costly single error in this chapter.

The last one sets up Chapter 7, which asks what happens when the conditions for perfect
competition fail.

Close on the thread: Nick's Pawpsicles, Homer's plough, and a federal ethanol subsidy are the
same story told three times. A wide margin is never a fact about the product. It is a fact
about how many people are selling it.""")

prs.save(OUT)
print(f"{OUT}: {len(prs.slides._sldIdLst)} slides")
