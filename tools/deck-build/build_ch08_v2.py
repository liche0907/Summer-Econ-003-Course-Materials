#!/usr/bin/env python3
"""Build ECON003_Ch08_Trade_UCR_v2.pptx — 41 slides.

Built from HIS 63-slide edit of v1 (mtime 1786929510556), which was slide DELETIONS ONLY:
the four checkpoints and the comparative-advantage experiment box. Verified shape-for-shape
and note-for-note against my v1 before rebuilding, so nothing hand-edited is overwritten.

WHAT v2 CHANGES, on instruction:

1. **Narrative and examples do not get their own page.** Where v1 broke one concept across
   several pages, v2 puts it on one and moves the walk-through into the notes. The five
   arguments against free trade were five pages; they are now one page and five paragraphs
   of notes. Same for: the three kinds of PPC point (folded into the figure's lead band),
   why the economy's curve bows (folded into its figure), the LeBron box and the states
   example (one page, two cards), and the import/export surplus ledgers (the figures
   already print the numbers, so the card rows went).

2. **Nothing outside the textbook.** v1 carried five live-2026 slides — the sugar
   tariff-rate quota, the US-vs-world sugar price, the average tariff rate, the Section 338
   Canada tariff, and tariff pass-through. All five are gone, and with them every re-check
   obligation. `ch08_fig_quota`, `_sugar_prices`, `_tariff_rate`, `_who_pays` and
   `_household` are now orphaned in Resources/CoverArt; the chart script still builds them,
   so re-adding any of it is a one-line change to this file.

3. **Less text per slide.** Card bodies cut to roughly two-thirds. Speaker notes cut to
   about half — what survives is the numbers to read aloud, the errors to pre-empt, and the
   material that came off the merged slides.

The chapter's five sections and its boxed features are unchanged. Two boxes are still posed
rather than answered because their text could not be sourced; those notes carry a
PLEASE READ BEFORE DELIVERY flag.
"""
import os

from pptx import Presentation

import deckkit as D
from deckkit import (BLUE, GOLD, DGOLD, GREEN, RED, INK, INK2, GREY, RULE, WHITE,
                     TINT_BLUE, TINT_NEUTRAL, TINT_RED, TINT_GREEN, TINT_GOLD)

SRC = "/mnt/user-data/uploads/ECON003_26S/Slides/ECON003_Ch08_Trade_UCR.pptx"
OUT = "ECON003_Ch08_Trade_UCR_v2.pptx"
F = "figs/ch08_fig_%s.png"
IC = "icons/%s.png"

LIMIT = 4.40
FIG_FLOOR = 4.42      # figure pages carry no card row

prs = Presentation(SRC)
D.drop_slides_after(prs, 1)
s1 = prs.slides[0]
for _sh in list(s1.shapes):
    if _sh.shape_type == 13:                      # no cover image, by instruction
        _sh._element.getparent().remove(_sh._element)
D.retitle_title_slide(s1, ["Chapter 8", "Trade"],
                      ["ECON 003", "UC Riverside · Summer 2026"])
D.notes(s1, """Title.

Chapter 8, Trade. The chapter is a ladder: one idea proved at three scales — two people,
two states, two countries. Nothing changes as you climb it but the size of the units.

Open with: for seven chapters people have made themselves better off inside one market.
Today they trade across markets, and two people working the same hours with the same
skills end up with more of everything.""")


def S():
    return D.blank_slide(prs)


def figpage(title, lead, fig, kick, credit=None, lead_kind="formula", lead_size=13.5):
    """Title, a ONE-LINE lead band, the figure, a kicker.

    The lead band is where a merged concept goes: a second line costs the figure 0.28 in
    of height on a height-bound page, so keep every lead to one line at 13.5 pt.
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
     "be made where it is cheapest.", IC % "shipping-container"),
])
D.kicker(s, "Today's question: why does anyone gain from trading with someone who is "
            "worse at everything?", y=4.52)
D.notes(s, """Recap and framing. Thirty seconds.

Only the third card matters. Everything in Chapters 4 to 7 happened inside one market with
one price. Today a second producer exists, with different costs.

Pose the question at the bottom as a paradox: if I am faster than you at everything, what
could you possibly do for me? Most people's instinct is "nothing", and the instinct is
provably wrong. Do not answer it — it gets answered on the slide called "Nobody Worked
Harder".""")

# ========================================================== 3. roadmap
s = S()
D.title(s, "Today's Roadmap")
D.strip5(s, 1.24, [
    ("1. What one\nperson can make", IC % "cook"),
    ("2. Who should\ndo what", IC % "balance-scale"),
    ("3. Trade between\nstates", IC % "truck"),
    ("4. Trade between\ncountries", IC % "shipping-container"),
    ("5. The case\nagainst", IC % "ballot-box"),
])
D.rect(s, 0.60, 2.88, 8.80, 0.06, fill=RULE)
D.cards3(s, 3.06, LIMIT - 3.06, [
    (BLUE, "Two people", "Maya and Owen and a food cart. One is faster at everything. "
     "Both still gain."),
    (DGOLD, "Two states", "California almonds, Iowa corn. Nobody proposes a tariff at "
     "the state line."),
    (RED, "Two countries", "The same arithmetic — but a border can be taxed, and that is "
     "Part 4."),
], body_size=11)
D.kicker(s, "Parts 1 and 2 build the whole argument. Parts 3 and 4 change nothing but the "
            "size of the units.", y=4.52)
D.notes(s, """Roadmap, and the three cards are the shape of the hour.

Say it out loud because it is the reason this chapter is easy if you follow it: the entire
argument is built in Parts 1 and 2, using two people and a food cart. Parts 3 and 4
introduce exactly one new idea between them — the bowed economy-wide curve — and otherwise
re-run the same arithmetic with bigger units.

A student who understands the "Nobody Worked Harder" slide understands the chapter.

The state-line card does the rhetorical work later, so plant it now: nobody campaigns for
a tariff on Iowa corn.

Part 5 is the counterweight and it is not a formality — the book's own question for this
chapter is "Will free trade cause you to lose your job?", not "isn't trade wonderful".""")

# ============================================ 4. the carried question
s = S()
D.title(s, "A Question to Carry Through the Hour")
y = D.band(s, 1.15, "Will free trade cause you to lose your job?", kind="note", size=19)
D.cards3(s, y + 0.30, LIMIT - (y + 0.30), [
    (RED, "The answer most people give", "Yes. Cheap imports arrive, the factory that "
     "made the same thing here closes, and those jobs are gone. This happens, and it is "
     "documented."),
    (BLUE, "The answer the model gives", "Trade changes WHICH jobs exist, not how many. "
     "The number of jobs is set by other things — mostly by how many people want to "
     "work."),
    (GREEN, "Why both can be true", "A country can gain overall while specific people "
     "lose badly. The gain is spread thin; the loss is concentrated."),
])
D.kicker(s, "Hold your answer. We come back to it at the end, with the model behind us.",
         y=4.52)
D.notes(s, """The book's Evidence-Based Economics question for Chapter 8. It sits at the
end of the chapter; we pose it at the front because it is the honest frame for the hour.

If you are recording, say "pause and decide your answer now".

Do not soften the first card. The literature on trade shocks and local labour markets is
real and it is not kind to the naive free-trade argument. Students who have seen a plant
close are right about something the simple model does not describe.

The third card is the reconciliation: economists claim something about the SIZE of a
total; critics claim something about its DISTRIBUTION. Different claims, both can be true.

Say plainly that nothing in the next forty minutes settles this. The model says how big
the pie gets, not who eats.""")

# ============================================================ 5. DIVIDER 1
s = S()
D.divider(s, "PART 1", "What One Producer Can Do")
D.notes(s, """Part 1 divider — section 8.1. Students meet the production possibilities
curve and learn that its slope is an opportunity cost.

Worth flagging: most textbooks put the PPC in an early scarcity chapter. This book holds
it back to the trade chapter, where it earns its keep. If your students have seen a PPC
elsewhere, this is four minutes of revision. Let it be.""")

# ================================================== 6. the two producers
s = S()
D.title(s, "Two People, Two Things to Make")
D.band(s, 1.12, "Maya and Owen each work an eight-hour shift on a campus food cart.",
       kind="neutral", size=14)
D.table(s, 1.30, 1.86, 7.40, 1.62, [
    ["", "Burritos per hour", "Smoothies per hour", "In a whole shift"],
    ["Maya", "12", "12", "96 burritos, or 96 smoothies"],
    ["Owen", "4", "8", "32 burritos, or 64 smoothies"],
], col_w=[1.30, 2.00, 2.00, 2.10], first_col_fill=BLUE, header_size=10.5,
    body_size=11, align=["l", "ctr", "ctr", "ctr"])
D.band(s, 3.66, "Read every number as a rate: this is what one hour of that person's time "
                "produces.", kind="formula", size=13.5)
D.kicker(s, "Two people, two goods, and one thing that is genuinely scarce: hours.",
         y=4.52)
D.notes(s, """The setup. Every number in Parts 1 to 3 comes off this table, so read it
aloud slowly.

Maya: twelve burritos an hour, or twelve smoothies. Owen: four burritos, or eight
smoothies. Eight-hour shift each.

Two things to make explicit, because they cause every later misunderstanding. These are
rates per hour, not totals — the last column is a whole shift on one good. And Maya is
faster than Owen at BOTH jobs: twelve beats four, twelve beats eight. Students should be
sitting there thinking Owen has nothing to offer. Good.

The scarce thing is hours. Not skill, not money.

Bridge for anyone reading ahead: the book runs its own example here with different names
and goods. The logic is identical; only the arithmetic is ours.""")

# =========================================================== 7. Maya's PPC
figpage("Everything Maya Could Make in a Day",
        "On the curve — every hour used. Inside — an hour wasted. Outside — impossible.",
        "ppc_one",
        "The curve is not a prediction. It is the edge of the possible.")
D.notes(prs.slides[-1], """The production possibilities curve, first appearance. Build it
rather than presenting it, and walk the three lettered points — the lead band names them
so the slide does not need a card row.

All eight hours on burritos: 96 burritos, no smoothies. All eight the other way: 96
smoothies. Four and four: 48 and 48, halfway along.

C is ON the curve — every hour used and used well. Economists call that efficient, and
remember from Chapter 7 that it is a narrow word: nothing is wasted, not that it is best
or fairest.

D is INSIDE. She could have more of both. An idle hour, a broken blender, a badly run
kitchen. Note it is attainable — just poor. Say clearly that a point inside is not "a
choice to work less"; it is a failure, and there is no trade-off to think about, only a
mistake to fix.

U is OUTSIDE. Not enough hours. Wanting it does not help.

If asked what moves the curve outward: more hours, better equipment, another pair of
hands. That is economic growth in one sentence.""")

# ============================================== 8. the slope
figpage("The Slope of the Curve Is an Opportunity Cost",
        "Move along the curve and ask what the extra burritos cost.",
        "ppc_slope",
        "That is what the curve is FOR: it prices your own time, in the other good.")
D.notes(prs.slides[-1], """The most important idea in Part 1.

Walk the arrows. Maya starts at 48 and 48 and wants twelve more burritos. Twelve burritos
is one hour, and that hour has to come out of smoothies, where it was making twelve. So
twelve more burritos cost twelve smoothies: one burrito costs one smoothie.

Then the general version: the slope of the PPC IS the opportunity cost. Not "shows", not
"relates to" — is. The steepness of the line is the exchange rate between the two goods
inside her own day.

Reinforce the Chapter 3 link: opportunity cost is not money. Nobody paid anything. The
cost of the burritos is the smoothies that did not get made.

They will be asked this in both directions, and Maya's one-to-one numbers hide the
difficulty. Drill it on Owen on the next slide, where the answer is a half.""")

# ================================================= 9. reading a cost off
s = S()
D.title(s, "Reading an Opportunity Cost Off the Numbers")
y = D.band(s, 1.15,
           "Opportunity cost of one burrito  =  smoothies given up  ÷  burritos gained",
           kind="formula", size=15)
y = D.band(s, y + 0.14,
           "Maya:  12 smoothies ÷ 12 burritos  =  1 smoothie per burrito", kind="answer",
           size=14.5)
y = D.band(s, y + 0.12,
           "Owen:  8 smoothies ÷ 4 burritos  =  2 smoothies per burrito", kind="answer",
           size=14.5)
D.cards2(s, y + 0.18, LIMIT - (y + 0.18), [
    (BLUE, "And the other way round",
     "Invert it. A burrito costs Maya 1 smoothie, so a smoothie costs her 1 burrito. A "
     "burrito costs Owen 2 smoothies, so a smoothie costs him half a burrito."),
    (RED, "Where marks get lost",
     "Answering in the wrong good. “Opportunity cost of a burrito” must be "
     "answered IN SMOOTHIES. If your answer is in burritos, you have inverted it."),
])
D.kicker(s, "Same one hour, two different exchange rates. That difference is the entire "
            "reason to trade.", y=4.52)
D.notes(s, """The mechanics, and this is examinable every term.

Maya gives up twelve smoothies to gain twelve burritos: one burrito costs one smoothie.
Owen gives up eight to gain four: one burrito costs TWO smoothies. Owen's burritos are
expensive, in smoothies.

Now the inversion, which is where marks go. The opportunity cost of a burrito is measured
in smoothies; of a smoothie, in burritos. They are reciprocals. Maya's are both 1, which
is convenient for seeing the idea and useless for testing it — so use Owen.

If you set one live question in this lecture, make it "what is Owen's opportunity cost of
one smoothie?" Fifteen seconds. The answer is half a burrito, and a good fraction of the
room will say two.

Last line is the hinge of the chapter: whenever two people value the same thing
differently, there is a trade that makes both better off.""")

# ============================================== 10. two curves
figpage("Owen's Curve, Same Axes",
        "One person, one skill, constant opportunity cost — so both curves are straight.",
        "ppc_two",
        "Maya's curve is further out everywhere. Watch the STEEPNESS instead: that is "
        "where the story is.")
D.notes(prs.slides[-1], """Two curves, and the point is the comparison. Also the place to
answer a question students are quietly holding.

First the obvious thing: Maya's curve is outside Owen's at every point. She makes more
burritos AND more smoothies. That is absolute advantage, drawn, and it is what makes
students think Owen is useless.

Now the thing that matters, and pause before it: the two curves have different SLOPES.
Maya's runs 96 to 96, falling one-for-one. Owen's runs 32 to 64, falling two-for-one —
twice as steep. Different slopes mean different opportunity costs, and that means there is
something to trade no matter who is faster.

The sentence that sets up Part 2: the HEIGHT of the curve tells you who is more
productive; the SLOPE tells you who should do what. Students conflate those for the whole
chapter unless you separate them here.

Why straight? Because one person with one skill has a constant opportunity cost — her
eighth hour is as good as her first. Aggregate across millions of people with different
costs and the curve bends, which is Part 3. Plant it, do not draw it.

If a sharp student asks whether one person's curve could bow: yes, if she tires or the
equipment suits one task. We are assuming that away; say so rather than let it pass.""")

# ============================================= 11. what a PPC does not say
s = S()
D.title(s, "What the Curve Does Not Tell You")
y = D.band(s, 1.12, "A production possibilities curve is a menu, not a decision.",
           kind="formula", size=15)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (RED, "It does not pick a point", "Every point on the curve is efficient. Which one "
     "you want depends on what you like — Chapter 5's problem, not this one's."),
    (RED, "It does not price anything", "There is no money on these axes. The only cost "
     "here is the other good."),
    (RED, "It does not say who is better off", "Two people can both be on their own curve "
     "and one still be far poorer. This is capacity, not welfare."),
])
D.kicker(s, "The curve tells you what is possible. It never tells you what to want.",
         y=4.52)
D.notes(s, """The honesty slide for Part 1. Forty seconds — every part of this deck has
one and they are the slides that keep the lecture from sounding like advocacy.

The first card is a habit of mind: a model that narrows the options is doing its job; one
that picks for you is usually smuggling in a value judgement.

The second kills a common error before it starts — students want dollars on these axes.
There are none. Money enters in Part 4 and not before.

The third is a forward reference to Part 5: a country can sit on its curve, trading
efficiently, and contain people much worse off than before. Efficiency does not
distribute.""")

# ============================================================ 12. DIVIDER 2
s = S()
D.divider(s, "PART 2", "Who Should Do What")
D.notes(prs.slides[-1], """Part 2 divider — section 8.2. The heart of the chapter and of
the course's claim to be non-obvious. Everything after this is application: if they get
Part 2, Parts 3, 4 and 5 are bookkeeping.""")

# =================================================== 13. absolute advantage
figpage("The Obvious Answer: Who Is Better?",
        "ABSOLUTE ADVANTAGE: producing more of a good with the same resources.",
        "advantage",
        "Maya wins both bars. On the obvious answer, Owen should not be employed at all.")
D.notes(prs.slides[-1], """Absolute advantage. Define it, then show why it is the wrong
tool. Key term, and it will be on the exam next to comparative advantage.

Read the bars: twelve burritos an hour to Owen's four, twelve smoothies to his eight. She
has both absolute advantages.

Now say the conclusion the picture appears to support, in a voice that makes clear you are
about to demolish it: Maya should do everything and Owen should go home. That conclusion
is wrong — not incomplete, wrong — and the next three slides prove it with arithmetic they
can check.

Best moment in the chapter for a live question: "Maya is faster at both jobs. Should she
hire Owen?" Most rooms say no.

Then set up the pivot verbally, because it no longer has its own slide: the trap in
absolute advantage is that it compares people at a job and forgets time is finite. Maya's
hour of smoothie-making does not appear from nowhere — it comes out of burritos, where she
makes twelve. Owen's comes out of burritos too, where he makes four. The same hour of
smoothies costs her a great deal and costs him very little. Being the BEST at a job is not
a reason to do it; being the CHEAPEST at it is.

The surgeon analogy lands well and is the same argument: a surgeon who types faster than
her assistant still does not do her own typing. Not because she can't — because the hour
costs her an operation.""")

# ================================================= 14. comparative advantage
s = S()
D.title(s, "Comparative Advantage")
y = D.defbox(s, 1.15,
             "A lower OPPORTUNITY COST of making a good than anyone else has.")
D.table(s, 1.00, y + 0.20, 8.00, 1.60, [
    ["", "Cost of ONE burrito", "Cost of ONE smoothie", "Cheapest at"],
    ["Maya", "1 smoothie", "1 burrito", "burritos"],
    ["Owen", "2 smoothies", "½ burrito", "smoothies"],
], col_w=[1.30, 2.40, 2.40, 1.90], first_col_fill=BLUE, header_size=10.5,
    body_size=11.5, align=["l", "ctr", "ctr", "ctr"])
D.band(s, y + 1.94, "Nobody is cheapest at both — and nobody ever can be. The two costs "
                    "are reciprocals of each other.", kind="answer", size=14)
D.kicker(s, "Read the columns, not the rows: in each column, someone is cheaper.",
         y=4.52)
D.notes(s, """The table that decides the chapter. Give it time.

Column one: a burrito costs Maya one smoothie and Owen two. Maya is the cheap producer of
burritos. Column two: a smoothie costs Maya a whole burrito and Owen only half. Owen is
the cheap producer of smoothies.

Now state the green band as a theorem, not an observation: it is arithmetically impossible
for one person to have the lower opportunity cost in both goods, because the two costs are
reciprocals. If your burritos are cheaper than mine, your smoothies must be dearer. That
is not an empirical regularity — it is division.

So there is ALWAYS a basis for trade. However unequal two producers are, each is the cheap
producer of something.

The kicker is the practical instruction and it is worth repeating at revision: to find
comparative advantage, compare DOWN a column, never across a row.

Name the history in one sentence — this is David Ricardo, 1817, and it is still the most
counter-intuitive true thing in introductory economics.""")

# ================================================ 15. the contrast and the rule
s = S()
D.title(s, "Absolute, Comparative, and the Rule")
D.cards3(s, 1.15, 2.42, [
    (BLUE, "Absolute advantage", "Compares OUTPUT. Who makes more per hour? Maya, at "
     "both. Tells you who is more productive, and nothing else."),
    (GREEN, "Comparative advantage", "Compares COST. Who gives up least? Maya for "
     "burritos, Owen for smoothies. Tells you who should do what."),
    (DGOLD, "The rule", "Specialise where your opportunity cost is lowest. Trade for the "
     "rest.", IC % "exchange"),
])
D.band(s, 3.72, "Absolute advantage is about how good you are. Comparative advantage is "
                "about what you give up.", kind="formula", size=14)
D.kicker(s, "Even when someone is better at everything, they are relatively better at "
            "something.", y=4.52)
D.notes(s, """The examinable distinction. Both terms are in the book's glossary and they
turn up in the same question, usually designed so the two answers differ.

Cleanest way to say it: absolute advantage is measured in units of output; comparative
advantage is measured in units of the other good.

Then the rule, short enough to memorise: specialise where your opportunity cost is lowest,
trade for everything else.

If you want a second route for students who find the table awkward, give it verbally
rather than on a slide: compare the ratios. Maya makes three times Owen's burritos but
only one and a half times his smoothies, so her advantage is concentrated in burritos.
Same answer, always — it is the same division in a different order. Tell them to pick one
method and stick to it; mixing them mid-question is where errors come from.""")

# ============================================= 16. specialise
s = S()
D.title(s, "Step 1: Specialise")
D.band(s, 1.12, "Each does only the job they are cheapest at. Same people, same hours, "
                "same skills.", kind="neutral", size=14)
D.table(s, 0.80, 1.86, 8.40, 1.72, [
    ["", "Maya makes", "Owen makes", "Between them"],
    ["Splitting their time", "72 burritos, 24 smoothies", "16 burritos, 32 smoothies",
     "88 burritos, 56 smoothies"],
    ["Each doing one job", "96 burritos, 0 smoothies", "0 burritos, 64 smoothies",
     "96 burritos, 64 smoothies"],
], col_w=[1.90, 2.20, 2.20, 2.10], first_col_fill=BLUE, header_size=10.5,
    body_size=10, align=["l", "ctr", "ctr", "ctr"])
D.band(s, 3.76, "Eight more burritos AND eight more smoothies, out of the same sixteen "
                "hours.", kind="answer", size=14.5)
D.kicker(s, "Nothing was invented and nobody worked harder. The hours were just pointed "
            "somewhere better.", y=4.52)
D.notes(s, """The payoff. Say the green band slowly.

Top row: they split their shifts. Maya six hours on burritos and two on smoothies, giving
72 and 24. Owen four and four, giving 16 and 32. Together 88 burritos and 56 smoothies.

Bottom row: each does only what they are cheapest at. Maya 96 burritos, Owen 64 smoothies.

Compare the last column: burritos 88 to 96, smoothies 56 to 64. Eight more of each.

Then pause and say it: no new equipment, no new skill, nobody stayed late. Sixteen hours
went in before and sixteen after. The extra output came from nothing but pointing the
hours at the right jobs.

One honest caveat if a sharp student raises it: the comparison depends on the starting
split. What never changes is that specialisation puts them on the outer edge of what the
two of them can jointly do — which is the curve two slides from now.""")

# ============================================ 17. terms of trade
s = S()
D.title(s, "Step 2: Agree a Price")
y = D.defbox(s, 1.15,
             "TERMS OF TRADE — the rate at which the two goods actually swap.")
y = D.band(s, y + 0.20,
           "They settle on:   1 burrito  =  1.5 smoothies\n"
           "Any rate between 1 and 2 smoothies works.", kind="answer", size=15)
D.cards2(s, y + 0.22, LIMIT - (y + 0.22), [
    (BLUE, "Why Maya accepts",
     "Making a smoothie herself costs her a whole burrito. Buying one from Owen costs her "
     "two-thirds of a burrito."),
    (DGOLD, "Why Owen accepts",
     "Making a burrito himself costs him two smoothies. Buying one from Maya costs him "
     "one and a half."),
])
D.kicker(s, "Below 1 Maya refuses, above 2 Owen does. In between, both are buying for "
            "less than it would cost to make.", y=4.52)
D.notes(s, """Terms of trade — a key term, and the piece students skip.

The setup matters: after specialising, Maya has 96 burritos and no smoothies, Owen has 64
smoothies and no burritos. Neither can eat a balanced lunch. They have to swap, and
swapping needs a rate. Where that rate comes from in the real world is bargaining or a
market price — the model does not determine it, and say so rather than let students think
it was derived.

Walk both cards; the symmetry is the argument. Maya: a smoothie made costs a burrito, a
smoothie bought costs two-thirds. Owen: a burrito made costs two smoothies, bought costs
one and a half. Both better off at the same rate at the same time, nobody fooled. This is
where "voluntary trade is not zero-sum" stops being a slogan.

The range on the second line is examinable — expect "which of these terms of trade would
both accept?". The logic is no-arbitrage: nobody buys for more than it costs to make, and
nobody sells for less. Those two refusals bracket the price.

Then the distributional point, which sets up Part 5: WHERE in the range the price lands
decides how the gains split. Near 1, Owen captures most; near 2, Maya does. The model says
both gain. It does not say they gain equally, and it has nothing to say about fair. Trade
creates a surplus; bargaining divides it — same structure as the whole free-trade debate
at national scale.""")

# ============================================= 18. the gains
s = S()
D.title(s, "Step 3: Trade — and Count What Changed")
D.band(s, 1.12, "Maya ships 18 burritos. Owen ships back 27 smoothies. The agreed rate, "
                "applied.", kind="neutral", size=14)
D.table(s, 0.80, 1.82, 8.40, 1.76, [
    ["", "Alone", "After trading", "Change"],
    ["Maya eats", "72 burritos, 24 smoothies", "78 burritos, 27 smoothies", "+6 and +3"],
    ["Owen eats", "16 burritos, 32 smoothies", "18 burritos, 37 smoothies", "+2 and +5"],
], col_w=[1.60, 2.45, 2.45, 1.90], first_col_fill=BLUE, header_size=10.5,
    body_size=10, align=["l", "ctr", "ctr", "ctr"])
D.band(s, 3.80, "Both of them have more of BOTH goods. Neither gave anything up.",
       kind="answer", size=14.5)
D.kicker(s, "This is the result the chapter exists to prove — and every number on it is "
            "checkable.", y=4.52)
D.notes(s, """The result. Read the table across one row at a time, then stop talking for a
moment.

Maya alone 72 and 24, after trading 78 and 27. Owen alone 16 and 32, after 18 and 37.

The green band is the sentence to say twice: BOTH parties have MORE of BOTH goods. Not a
trade-off, not a compromise. More of everything, for both, out of the same sixteen hours.

Two checks on the board, because they turn magic into arithmetic. Does it add up? 78 plus
18 is 96 burritos, exactly what Maya produced; 27 plus 37 is 64 smoothies, exactly what
Owen produced. Nothing was created in the trade itself — all the gain came from the
specialisation. Does the rate hold? Eighteen burritos at one and a half is twenty-seven
smoothies. It does.

Note the gains are not split evenly. That is the price sitting where it sits.""")

# =========================================== 19. outside your own curve
figpage("Both of Them End Up Outside Their Own Curve",
        "Solid line: what they can MAKE. Dashed line: what they can CONSUME.",
        "trade_line",
        "Trade does not move your production curve. It lets you consume past it.")
D.notes(prs.slides[-1], """The picture of the result, and the most useful diagram in the
chapter for an exam.

Maya's panel: the solid blue line is her production curve and it has not moved — she is
exactly as fast as she was. The dashed green line is what she can CONSUME once she can
trade at one and a half smoothies per burrito. It lies outside. Her consumption point, 78
and 27, is one she could not possibly produce: 78 plus 27 is 105 and her limit is 96. Same
story in Owen's panel.

The sentence that makes it stick: trade does not make you more productive. It breaks the
link between what you make and what you consume. Before trade those had to be the same
bundle; after, they are two bundles and only the first is limited by your own skill.

Housekeeping, and say it rather than hope nobody notices: the two panels are drawn to
DIFFERENT scales, because Owen's numbers are small enough that a shared axis makes his
panel unreadable. Both axes shrink by the same factor so the slopes stay comparable — but
do not invite students to compare positions across panels.""")

# ============================================ 20. joint PPC
figpage("The Two of Them, Counted Together",
        "Add both producers into one curve. It kinks where the cheap one runs out.",
        "ppc_joint",
        "Specialisation lands them exactly on the corner — the best the two of them can "
        "jointly do.")
D.notes(prs.slides[-1], """The joint curve. Most sophisticated diagram in Part 2 and it
rewards a slow walk.

Build it from the left. At the top left everyone makes smoothies: 96 from Maya plus 64
from Owen is 160. To get burritos you take them from whoever gives up least — Maya, at one
smoothie each — so the first stretch falls one-for-one. At 96 burritos Maya has run out of
hours. Any more must come from Owen, at two smoothies each, so the line steepens. That is
the kink.

The punchline deserves its own beat: the kink is exactly the point where each person does
only the job they are cheapest at. Specialisation is not one option among many — it is the
corner, the single point where the two of them together are doing the best they possibly
can.

The grey point inside is where they were splitting their time. The arrow is the gain:
eight burritos and eight smoothies from reorganising alone.

One sentence back to Part 1: this curve is bent because two producers have two different
opportunity costs. Add a third and you get a third segment. Add millions and you get the
smooth bowed curve of Part 3.""")

# ============================================ 21. nobody worked harder
s = S()
D.title(s, "Nobody Worked Harder")
y = D.defbox(s, 1.15,
             "Sixteen hours went in before. Sixteen hours went in after. There is more "
             "food. That is the entire argument for trade, at every scale.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "Where the gain came from", "Hours that were producing at a bad exchange rate "
     "are now producing at a good one.", IC % "clock"),
    (BLUE, "Why it works with unequal partners", "Opportunity costs are reciprocals. "
     "Whoever you are, you are the cheap producer of something."),
    (DGOLD, "And the opening question, answered", "Maya trades with Owen because her own "
     "alternative is bad: every smoothie she makes costs her a burrito.", IC % "exchange"),
])
D.kicker(s, "You do not trade with someone because they are good. You trade with them "
            "because your own time is expensive.", y=4.52)
D.notes(s, """The close of Part 2 and the answer to the paradox from the start. If you cut
anything from this deck, do not cut this slide.

Say the first line as a challenge: sixteen hours before, sixteen after, more food out. A
student who cannot say where the extra food came from has not got the chapter. The answer
is the first card — the hours were reallocated to where they were worth more.

Deliver the third card as an answer, not a summary. Maya trades with Owen not out of
charity and not because Owen is any good. She trades because her own alternative is bad:
every smoothie she makes herself costs her a burrito, and burritos are what she is
extraordinary at. Owen's smoothies are cheap for her precisely because hers are expensive.

The kicker is the version students carry out of the room: you outsource what your own time
is too valuable to spend on.""")

# ============================================================ 22. DIVIDER 3
s = S()
D.divider(s, "PART 3", "The Same Logic,\nBigger Units")
D.notes(prs.slides[-1], """Part 3 divider — section 8.3, "Trade Between States".

Why the section exists: most textbooks go straight from two people to two countries. This
book puts a rung in between, and it is rhetorically powerful — nobody has strong feelings
about interstate trade, so the economics can be seen without the politics attached.

Only one genuinely new idea in this part: the economy-wide curve bows outward.""")

# ============================================ 23. economy PPC
figpage("From One Person to a Whole Economy",
        "Switch the cheapest producers first, and each extra unit costs more than the "
        "last.",
        "ppc_economy",
        "Straight means constant cost. Bowed means rising cost. The shape is telling you "
        "something.")
D.notes(prs.slides[-1], """The economy-wide production possibilities curve — the promise
made in Part 1, now paid. This slide also absorbs the "why is Maya's straight" question.

Left panel: four producers. Start with everyone on good Y. To get X, move the producer
with the lowest opportunity cost of X, then the next lowest. Each segment is one producer,
each steeper than the last.

Right panel: do that with millions and the steps become invisible. What is left is a
smooth curve, bowed outward.

State the reason as a sentence they can write down: the curve bows out because opportunity
cost RISES as you make more of a good — and it rises because the economy runs out of the
people and land that are cheap at that job and starts using the ones that are expensive.

The concrete version lands better: the first acre of California converted to almonds was
terrible for anything else. The millionth had to be taken from something valuable.

Counterfactual, and it is the fastest check of understanding: if every resource were
equally good at both jobs the curve would be a straight line, exactly like Maya's. It is
the DIVERSITY of resources that bends it.

Watch for the standard wrong answer. Students say the curve bows because of "scarcity" or
"diminishing returns". Scarcity is why there is a curve at all. Diversity of opportunity
cost is why it bends.""")

# ============================================ 24. LeBron + states
s = S()
D.title(s, "The Same Logic, Two Illustrations")
D.cards2(s, 1.15, 2.42, [
    (BLUE, "Should LeBron James paint his own house?",
     "Suppose he really is the faster painter. He should still hire someone — the "
     "afternoon costs him training, filming and playing, and it costs the painter far "
     "less. He hires a painter not because he is bad at painting, but because his "
     "afternoons are expensive."),
    (DGOLD, "Should California grow its own corn?",
     "California grows almonds and wine; Iowa grows corn and soybeans; each buys the "
     "rest from the other. Fifty states, no tariffs, extreme specialisation — and no one "
     "calls it a crisis. Riverside runs an enormous trade deficit with Iowa."),
])
D.band(s, 3.72, "One is a person, one is a state. Neither argument has changed since "
                "Maya and Owen.", kind="formula", size=14)
D.kicker(s, "And you have never once worried about the trade deficit with Iowa.", y=4.52)
D.notes(s, """The book's Choice and Consequence box from section 8.3, merged with the
states example. Both are illustrations of one idea, so they share a page.

LeBron first. Set it up carefully: the interesting version assumes he really IS the better
painter — if he were worse there would be nothing to discuss. Absolute advantage in
painting, and he should still hire someone, because the cost of his afternoon is not
measured in paint but in what else it could have produced. The painter's afternoon has a
much lower alternative value, so the painter is the CHEAP producer of painting even though
he is the SLOW one. Say out loud that this is exactly Maya and Owen in a form students
already believe. It runs both ways too: the painter sells the hour because his alternative
was worth less. Both gain.

Then the states. Nobody in Riverside worries about our trade deficit with Iowa, nobody
proposes a tariff on Iowa corn, nobody describes Iowa as taking advantage of us.

That sets up Part 4 with a question: what changes when the line on the map is a national
border? Economically nothing — politically and legally a great deal, because a national
border can be taxed and a state border cannot.

Do not overplay it. There ARE real differences: workers move freely within the US, there
is a common set of labour and environmental rules, and federal transfers partly compensate
places that lose out. Say that here so the argument does not sound like a debating trick —
Part 5 comes back to it.

And the honest half, which used to have its own slide: regional specialisation means
regional exposure. When the thing your region specialised in declines, the specialisation
that made you rich makes you vulnerable. Parts of the American manufacturing belt are the
standing example, and students from those places know it better than the model does. The
gains are real and so are the losers.

No production figures on the slide on purpose — do not add any from memory.""")

# ============================================================ 25. DIVIDER 4
s = S()
D.divider(s, "PART 4", "Now Draw the Border")
D.notes(prs.slides[-1], """Part 4 divider — section 8.4.

Tell students explicitly that the tool changes here. Parts 1 to 3 used production
possibilities curves; Part 4 uses the supply and demand diagram from Chapter 4 and the
surplus areas from Chapter 7. A student still thinking in PPCs will be lost within two
slides.

This is the longest part and it is where the exam questions cluster.""")

# ============================================ 26. the world price
s = S()
D.title(s, "One New Number: The World Price")
y = D.defbox(s, 1.15,
             "The WORLD PRICE is what a good sells for internationally. Open your border "
             "and you can buy or sell all you like at that price.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "Compare it with your own", "Work out the price with no trade. Then look at "
     "the world price. Only the comparison matters."),
    (GREEN, "World price lower", "They make it more cheaply than you. You import, and "
     "your price falls to theirs.", IC % "shipping-container"),
    (RED, "World price higher", "You make it more cheaply than they do. You export, and "
     "your price rises to theirs.", IC % "truck"),
])
D.kicker(s, "The world price is comparative advantage arriving as a number you can look "
            "up.", y=4.52)
D.notes(s, """The bridge from Parts 1 to 3 into the diagrams, and the kicker is the bridge
— say it deliberately.

In Part 2, comparative advantage was something you worked out by comparing opportunity
costs. In a real economy nobody does that calculation. The world price does it for you: a
world price below yours IS the statement that the rest of the world gives up less to make
this than you do.

State the assumption out loud: the country is small enough to trade as much as it likes
without moving the world price. That is what makes it a horizontal line on every diagram
that follows, and it is doing real work. For a large country it is not literally true, and
a sharp student may say so — relaxing it changes the size of the effects, not their
direction.

Note also that importing or exporting is not a policy decision here. It falls out of the
comparison. Policy enters when we tax the flow.""")

# ============================================ 27. autarky
figpage("Start With the Border Closed",
        "The US market for raw sugar, with no imports and no exports allowed.",
        "market_autarky",
        "Sixty cents a pound, forty million pounds a week — and every pound grown here.",
        "Illustrative linear schedules; surplus figures are in the same arbitrary units "
        "throughout Part 4.")
D.notes(prs.slides[-1], """The baseline. Everything in Part 4 is measured against this
picture, so make it solid before moving.

Chapter 4's diagram with Chapter 7's shading. Demand down in blue, supply up in red,
crossing at sixty cents and forty million pounds. With the border closed, that is the price
and the quantity.

Consumer surplus is the blue triangle above the price and below demand: 800. Producer
surplus is the red triangle below the price and above supply: 800. The units are arbitrary
— what matters is how they change.

Say what these schedules are: illustrative straight lines, not measured ones, scaled so the
closed-border price sits in a plausible range for sugar. The credit line says so.

Remind them briefly what surplus means — Chapter 7 did the work.""")

# ============================================ 28. imports
figpage("Open the Border: the World Price Is Lower",
        "The world will sell sugar at 40¢. Nobody in America will now pay 60¢ for it.",
        "market_import",
        "Consumers gain 1,000, producers lose 600, the country gains 400 — and the losers "
        "know exactly who they are.")
D.notes(prs.slides[-1], """The importing case. Mechanics first, then the welfare — the
figure prints the three numbers so the slide needs no card row.

At sixty cents, buyers can get sugar abroad for forty, so nobody pays sixty and the price
falls to the world price.

At forty cents, read each curve SEPARATELY — this is where students go wrong. Across to
the red supply curve: American growers supply only 20 million pounds, down from 40. Across
to the blue demand curve: Americans want 60, up from 40. The gap — 60 wanted, 20 grown
here — is imports of 40 million pounds.

Welfare: consumers gain 1,000, producers lose 600, the country nets 400. That 400 is the
gains from trade from Part 2 in a different diagram. Same result, new tool.

Then the honest part, and it is the political economy of the whole chapter in six words.
The 600 producers lose is not a rounding error. Sugar growers are genuinely worse off and
they know exactly who they are, which is why they lobby. Consumers gain more in total but
each gains a little, spread across everybody, and most have no idea. Concentrated losses,
diffuse gains.

Name the compensation principle here, because Part 5 needs it: if the gain is 1,000 and
the loss 600, the winners could in principle hand over 600, leave everyone at least as
well off, and keep 400. That is what "the country gains" means. Whether the cheque is
actually written is a different question — mostly it is not.""")

# ============================================ 29. exports
figpage("Same Country, Higher World Price",
        "Now the world will PAY 80¢. No American grower sells at home for 60¢.",
        "market_export",
        "Producers gain 1,000, consumers lose 600, the country gains 400 again. Only the "
        "loser changed.")
D.notes(prs.slides[-1], """The exporting case, and it is the mirror image. Go faster — they
have the machinery now.

If the world pays eighty, no grower sells at home for sixty, so the domestic price rises to
the world price. At eighty: growers supply 60, Americans buy 20, the excess of 40 is
exported.

Producers gain 1,000, consumers lose 600, the country gains 400.

Point at the symmetry explicitly, because it prevents a real misconception: trade is not
good for consumers and bad for producers. It is good for whichever side the closed border
was constraining. American sugar BUYERS are worse off here — exactly the people who gained
on the previous slide.

The general result: a country gains in total whichever way the goods flow, and in both
directions it creates a domestic group that loses. There is no version of opening a border
where everybody at home gains — somebody was benefiting from it being shut.

If a student notices the net gain is 400 both ways, that is not a coincidence of the
numbers; the schedules and the price gap are symmetric on purpose. Good student.""")

# ============================================ 30. the rule
s = S()
D.title(s, "The Rule That Decides Everything in Part 4")
y = D.band(s, 1.12,
           "world price  <  your no-trade price   →   you IMPORT\n"
           "world price  >  your no-trade price   →   you EXPORT",
           kind="formula", size=16)
D.cards2(s, y + 0.28, LIMIT - (y + 0.28), [
    (BLUE, "It is comparative advantage, restated",
     "A world price below yours means the rest of the world gives up less to make this "
     "than you do. Part 2's definition, arriving as a market price instead of a table."),
    (GREEN, "And it is how the question is set",
     "Find the no-trade equilibrium FIRST. Compare. Then read the two quantities off the "
     "two curves separately at the world price. The gap is the trade."),
])
D.kicker(s, "Find the closed-border price first. Every question in this part starts "
            "there.", y=4.52)
D.notes(s, """The examinable procedure. Dictate it as a procedure.

One, and students skip it: find the equilibrium price with no trade. Set quantity demanded
equal to quantity supplied and solve. Everything is a comparison against that number.

Two: compare the world price with it. Below means import, above means export.

Three: at the world price, read quantity supplied off the supply curve and quantity
demanded off the demand curve, SEPARATELY. Do not set them equal — they are not equal, and
their difference is the whole point.

Four: the gap is imports or exports.

The commonest error by a distance is setting supply equal to demand at the world price.
Say so explicitly. Once the border is open the domestic market does not clear on its own —
it clears with help from the rest of the world, and that help is the gap.

Tell them to practise the tariff diagram from a blank page; that is how it will be
asked.""")

# ============================================ 31. a tariff
figpage("A Tariff",
        "A TARIFF is a tax on an imported good. Here: 10¢ a pound, on top of the 40¢ "
        "world price.",
        "market_tariff",
        "The price rises to 50¢, imports halve, and two triangles of value disappear "
        "entirely.")
D.notes(prs.slides[-1], """The central diagram of Part 4. It is on the exam, and the book's
own end-of-chapter question asks about areas A and B by name — which is why they are
lettered that way here.

A ten cent tariff means an importer paying forty abroad hands ten to the government at the
border, so they will not sell below fifty. The domestic price rises from forty to fifty.

At fifty, four things move. Domestic supply rises 20 to 30 — the higher price makes more
American farms viable. Domestic demand falls 60 to 50 — some buyers drop out. Imports halve,
40 to 20. The government collects ten cents on each of the remaining 20 million pounds:
revenue of 200, the gold rectangle.

Now the two triangles, and this is the content the exam wants in words.

A, on the left, is the PRODUCTION distortion. Those extra 10 million pounds are grown in
America at a cost above forty cents when the world would have sold them for forty. Real
resources — land, water, labour — burned to make something we could have bought cheaper.

B, on the right, is the CONSUMPTION distortion. Those 10 million pounds are not bought at
all, by people who valued them above the world price. That value simply does not happen.

Together A and B are 100, and nobody receives them.""")

# ============================================ 32. the ledger
figpage("Who Pays for a Tariff",
        "The transfer is arguable. The two triangles are value that stops existing.",
        "tariff_ledger",
        "Consumers lose 550. Producers and government together gain 450. The missing 100 "
        "is gone.")
D.notes(prs.slides[-1], """The ledger. Read the four bars in order and let the arithmetic
persuade.

Consumers lose 550 — ten cents more on every pound they still buy, and some stop buying.
Producers gain 250 — a higher price on a larger domestic output. Government collects 200.
Gains total 450 against a loss of 550, so 100 is missing. That 100 is the two triangles.

Make the distinction sharp, because students blur the transfer and the loss. The money
consumers hand to producers is a TRANSFER — Americans pay it, other Americans receive it.
You may think that fair or unfair, but it is a distributional question and economics does
not settle it. The triangles are different in kind: nobody gets that value, it is not
moved from one American to another, it stops existing.

One observation students find striking: the government's revenue is NOT the main effect —
200 out of the 550 taken from consumers. Most of what consumers lose goes to domestic
producers, not the Treasury. So a tariff is a much better tool for helping a specific
industry than for raising money, which is exactly what its political history looks like.

If you want to defend a tariff you must either defend the transfer or argue that something
outside this diagram is worth the loss. Part 5 is arguments of the second kind.""")

# ============================================ 33. quotas
s = S()
D.title(s, "A Quota Does the Same Job, Differently")
y = D.defbox(s, 1.15,
             "A QUOTA is a limit on how much may be imported. Instead of taxing the flow, "
             "it caps it.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "Same direction of effect", "Fewer imports, a higher domestic price, producers "
     "protected, consumers paying more. The same two triangles."),
    (RED, "One important difference", "No tariff revenue. The gap between the world price "
     "and the domestic price goes to whoever holds the right to import.", IC % "price-tag"),
    (DGOLD, "Which is why they are fought over", "That gap is a quota rent, and "
     "governments decide who gets it.", IC % "ledger"),
])
D.kicker(s, "A tariff sends the money to the Treasury. A quota sends it to whoever holds "
            "the licence.", y=4.52)
D.notes(s, """Quotas — listed among the methods of protectionism, and the comparison with
tariffs is a standard exam question.

Lead with the similarity: a quota that cuts imports to 20 million pounds produces the same
domestic price as a tariff that cuts them to 20 million pounds. Price up, imports down,
producers gain, consumers lose, same two deadweight loss triangles. Every effect points the
same way.

Then the difference, where the marks are. Under a tariff, the wedge between the world price
and the domestic price is collected by the government at the border. Under a quota the
wedge still exists — someone buys at forty and sells at fifty — but it goes to whoever has
permission to import. That is a quota rent.

Why that matters rather than being a technicality: quota rents are worth a great deal to
specific identifiable firms and countries, and governments allocate them. That creates a
permanent constituency for keeping the quota, which is one reason quotas outlive their
justifications.""")

# ============================================ 34. fair trade + firms
s = S()
D.title(s, "Two Complications Worth Knowing")
D.cards2(s, 1.15, 2.52, [
    (GREEN, "Fair trade products",
     "The label promises the grower was paid above the market price, and buyers pay more "
     "deliberately. An economist looks twice: a guaranteed above-market price is a price "
     "floor, familiar from Chapter 7, and it attracts more supply than it can absorb. "
     "Whether growers end up better off is measurable."),
    (RED, "Tariffs land on firms",
     "Most of what crosses a border is a part on its way to becoming something else. So a "
     "tariff on imported steel raises costs for every American firm that builds things "
     "out of steel. Protecting one industry means taxing the industries downstream of "
     "it — and both are American."),
])
D.band(s, 3.78, "A good intention is not a good outcome. And which producers, exactly?",
       kind="formula", size=14)
D.kicker(s, "Both are questions you can answer with data rather than with sympathy.",
         y=4.52)
D.notes(s, """The book's two remaining boxes — Letting the Data Speak on fair trade
(section 8.4) and Choice and Consequence on tariffs between firms (section 8.5) — merged,
because both are illustrations rather than mechanisms.

PLEASE READ BEFORE DELIVERY: I could not obtain the text of the fair trade box, so the
left card poses the question rather than reporting its finding. Open the book to section
8.4 and check what it concludes before recording. Do not state a result from this slide as
it stands. The right card is standard economics and needs no check.

Fair trade: handle with care — students have strong and mostly good instincts here and the
aim is not to debunk. The economic content is that a guaranteed above-market price is a
price floor, so the predictable consequences are excess supply and a rationing problem:
who gets to sell at the premium? The transferable point is on the band — intending to help
and succeeding in helping are different claims, and only the second is empirical.

Tariffs on firms: the content students miss is that a large share of trade is intermediate
goods, firms buying inputs from firms, a part sometimes crossing a border several times
before the product is finished. So a tariff on imported steel raises the price of steel
inside the country that imposed it. American steel producers gain; American car makers,
appliance makers, construction firms and machine shops face higher costs. Everyone in that
sentence is American.

The protected industry is typically smaller and more concentrated than the industries
paying for the protection — concentrated benefits, diffuse costs again, and the best single
explanation of why protection is politically durable even when the arithmetic is against
it.""")

# ============================================================ 35. DIVIDER 5
s = S()
D.divider(s, "PART 5", "The Case on\nthe Other Side")
D.notes(prs.slides[-1], """Part 5 divider — section 8.5.

Set the tone before the next slide. Everything so far has pointed one way and a student
paying attention should be slightly suspicious of how tidy it has been.

Deliver this part straight. Do not set the arguments up in order to knock them down. Some
are weak, one is strong, and students should be able to tell which is which from the
reasoning rather than from your tone of voice.""")

# ============================================ 36. five arguments
s = S()
D.title(s, "Five Arguments Against Free Trade")
y = D.band(s, 1.12, "Every one of them accepts the diagram and argues that something "
                    "outside it matters more.", kind="formula", size=14.5)
D.strip5(s, y + 0.24, [
    ("1. National\nsecurity", IC % "hard-hat"),
    ("2. Infant\nindustry", IC % "lightbulb"),
    ("3. Environmental\nstandards", IC % "wheat"),
    ("4. Cultural\nidentity", IC % "ballot-box"),
    ("5. Jobs and\nwages", IC % "factory"),
])
D.band(s, 3.34, "Number 5 has the best evidence behind it and is the book's own chapter "
                "question.\nNumber 1 is the hardest to falsify — which is exactly why it "
                "gets attached to so much.", kind="note", size=13.5)
D.kicker(s, "The test for any of them: is a tariff the cheapest way to buy the thing you "
            "actually want?", y=4.52)
D.notes(s, """All five arguments on one page — the detail lives here, in the notes, not in
five slides. Budget three or four minutes and take them in order.

The top band is the analytical key and it is worth saying twice. None of these five claims
the diagram is wrong. They all concede that a tariff costs consumers more than it gains
producers and burns two triangles on the way. What they claim is that the diagram leaves
out something worth more than the loss. That tells students how to evaluate a protection
argument they have never heard before.

ONE, NATIONAL SECURITY. Take the strong version seriously first, because it is correct:
there are goods where dependence on a potential adversary is a real strategic risk, and no
economist argues a country should buy its munitions from whoever is cheapest this year. The
problem is not that the argument is wrong but that it has no natural boundary — it is a
claim about a hypothetical future, very hard to test, and therefore attractive to any
industry looking for a reason. Historically it has been attached to a remarkable range of
products. The economist's contribution: even a real security concern can be met by
stockpiles, diversified suppliers or a subsidised strategic capacity. The question is not
whether security is valuable but whether a permanent tax on consumers is the cheapest way
to buy it. Do not name specific current cases unless you have checked them.

TWO, INFANT INDUSTRY. The most intellectually respectable of the five. The mechanism is
genuine: if costs fall with experience, a new entrant might be uncompetitive today and
competitive in ten years, and might never get those years if undercut from day one.
Temporary protection could bridge the gap and leave the country permanently better off. It
usually fails for political rather than economic reasons — protection creates people whose
livelihoods depend on it, and they lobby, so the industry acquires a constituency for
permanent protection long before it acquires a cost advantage. The practical test students
can apply to any case they read about: was a date set, and did it hold? Be even-handed —
there are real historical cases, particularly in East Asia, argued on both sides, and the
disagreement turns on what else those governments were doing at the same time.

THREE, ENVIRONMENTAL STANDARDS. The stronger of the middle pair, and a forward reference:
if a foreign producer is cheaper because it is allowed to pollute, the price gap is not a
real cost advantage — it is a cost paid by someone outside the transaction. That is an
externality, and it is the whole of Chapter 9, the next lecture. So this is not really a
complaint about trade at all.

FOUR, CULTURAL IDENTITY. Different in kind. Some countries protect domestic film, music,
publishing or food traditions on the grounds that these are not ordinary goods. That is a
values claim, not an efficiency claim, and economics has no special authority over it. Say
that plainly rather than dismissing it.

For three and four the answer is the same and it is a general principle worth stating once
at full strength: aim the policy at the problem. If pollution is the problem, tax the
pollution — including at home, where you also have polluters. If domestic film matters,
subsidise domestic film. A tariff addresses these clumsily, hits unrelated goods, and burns
the two triangles on the way.

FIVE is the serious one and it gets the next slide.""")

# ============================================ 37. jobs and wages
s = S()
D.title(s, "5. Jobs and Wages — the Serious One")
y = D.defbox(s, 1.15,
             "When imports arrive, specific factories close and specific towns lose their "
             "employer. This is not a theoretical worry. It happens, and it is measured.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (RED, "What is true", "The losses are concentrated, geographic and lasting. People do "
     "not smoothly move to the new jobs — those are elsewhere and need different skills.",
     IC % "factory"),
    (BLUE, "What is also true", "Trade changes which jobs exist, not how many. Total "
     "employment is driven by other things, mostly by how many people want to work."),
    (GREEN, "Why both survive", "“The country gains” is a claim about a total. "
     "It never was a claim that each person gains."),
])
D.kicker(s, "Trade makes the pie bigger and hands out uneven slices. Denying either half "
            "is dishonest.", y=4.52)
D.notes(s, """The most important slide in Part 5. Give it the time you saved on the
previous one.

Take the first card entirely seriously and without hedging. The adjustment costs of trade
are real, concentrated in particular places, and long-lasting. "Workers will move to more
productive sectors" describes something that happens slowly, incompletely, and often not to
the same people. A student whose family lived through a plant closing is not confused about
economics — they are describing something the simple model does not capture.

The second card is what the model actually says, and state its limits precisely: trade
changes the COMPOSITION of employment, not the LEVEL. If trade destroyed jobs on net, two
centuries of expanding trade would have produced permanent mass unemployment. It did not.
The level is set by labour supply, demography and macroeconomic policy.

The third card is the reconciliation and the intellectual heart of the chapter's ending.
When an economist says a country gains from trade, that is a statement about a sum. The
diagram made that obvious from the first picture — the producer surplus loss was right
there, in red.

Land the kicker on both halves. Anyone who tells you only one of them is selling you
something.""")

# ============================================ 38. the EBE answered
s = S()
D.title(s, "So: Will Free Trade Cause You to Lose Your Job?")
y = D.band(s, 1.12, "The chapter's own question, and the honest answer has three parts.",
           kind="note", size=14.5)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (RED, "Possibly, if you are in the wrong industry", "Some specific jobs disappear "
     "because of imports, and that risk is not evenly spread across people or places."),
    (GREEN, "But not on net", "Trade reshuffles employment between sectors. It does not "
     "set how many jobs a country has."),
    (BLUE, "And the winners could compensate the losers", "The gains are more than large "
     "enough to fund retraining and relocation. Whether anyone writes the cheque is a "
     "political choice, not an economic law.", IC % "ballot-box"),
])
D.kicker(s, "A truthful answer here is uncomfortable, and any answer that is comfortable "
            "is incomplete.", y=4.52)
D.notes(s, """The chapter's Evidence-Based Economics question, answered, with the
compensation principle folded in as the third card.

PLEASE READ BEFORE DELIVERY: I could not obtain the book's own answer to this question, so
this is the standard economic answer rather than the book's evidence. Read the
Evidence-Based Economics section at the end of 8.5 before recording and add its specifics
to these notes — students are examined on the book's version.

Deliver the three cards as one answer. Yes, some people lose their jobs to import
competition, and the risk is concentrated rather than random. No, trade does not reduce the
total number of jobs. And in the long run wages track productivity, which trade tends to
raise — a slow, diffuse process nobody can photograph, whereas a closing plant is on the
news. That asymmetry in visibility explains much of the shape of this debate.

The third card is the book's own end-of-chapter question, so it is examinable in discussion
form: if the winners can more than compensate the losers, why does it matter that wages and
employment fall for some? The arithmetic is clean — gains 1,000, losses 600, transfer 600,
400 left over. The gap between "could" and "does" is the point. The gains are spread across
everyone as slightly cheaper goods, largely invisible; the losses are concentrated on
identifiable people in identifiable places. Diffuse beneficiaries do not organise;
concentrated losers do.

Economics can establish that the compensation is affordable. It cannot make it happen and
has no special authority on how much there should be. If a student argues that the
compensation never materialising is itself a reason to be sceptical of free-trade
arguments, that is a coherent position — say so rather than talk them out of it.""")

# ============================================ 39. what it settles
s = S()
D.title(s, "What This Chapter Settles, and What It Does Not")
D.cards2(s, 1.15, 2.32, [
    (GREEN, "Settled, and not seriously disputed",
     "Specialisation by comparative advantage raises total output. Voluntary trade at a "
     "price between the two opportunity costs makes both sides better off. A tariff "
     "transfers value and destroys some of it. These are results, not opinions."),
    (RED, "Not settled, and not settleable here",
     "Whether the losers should be compensated, and how much. Whether a particular "
     "industry deserves protection. How to weigh a town against a total. Every one of "
     "these is a question about values."),
])
D.band(s, 3.54, "Knowing which of these two boxes a question belongs in is most of what "
                "an economics education is for.", kind="formula", size=14)
D.kicker(s, "The model is a tool for thinking about trade-offs. It does not do the "
            "choosing.", y=4.52)
D.notes(s, """The honesty slide for the chapter and the last content slide. It deliberately
mirrors the equity-versus-efficiency close of Chapter 7 — say that out loud, because it is
the second time the course has drawn this line and it will not be the last.

The left box is genuinely settled. No serious school of economics disputes that
specialisation by comparative advantage raises total output. Students should know which
parts of what they have been taught are robust.

The right box is not settled and could not be settled by better economics. How much a town
is worth against a national total is not a measurement problem; having a model does not
give an economist a vote worth more than anyone else's.

The band is the transferable skill and the most useful sentence in the deck: most bad
arguments about policy come from putting a question in the wrong box — treating a values
question as if data could settle it, or treating a factual question as a matter of opinion.

Hand over to Chapter 9 in one sentence: this chapter assumed the only people affected by a
transaction are the two making it. Next time we drop that, and the first casualty is the
assumption that a market price reflects a real cost.""")

# ============================================================ 40. recap
s = S()
D.recap_table(s, "Chapter 8: The Full Picture", [
    ["The curve", "Everything you could make with the hours you have. Its slope is your "
     "cost.", "production possibilities curve, opportunity cost", "Section 8.1"],
    ["Who does what", "Do what costs YOU least — not what you are best at.",
     "absolute advantage, comparative advantage", "Section 8.2"],
    ["The gains", "Specialise, then trade at a price between the two costs. Both gain.",
     "specialisation, terms of trade", "Section 8.2"],
    ["Bigger units", "An economy holds many costs, so its curve bows outward.",
     "economy-wide PPC", "Section 8.3"],
    ["Countries", "Compare the world price with your own. Below it you import.",
     "world price, imports, exports", "Section 8.4"],
    ["Protection", "A transfer to producers and government, plus a loss nobody receives.",
     "tariff, quota, deadweight loss", "Sections 8.4–8.5"],
], "One idea, proved three times: people, states and countries all gain by doing what they "
   "give up least to do.")
D.notes(s, """Recap. Nothing new — the hour re-indexed so students can find things.

Read the closing line out; it is the honest summary.

The right-hand column points at SECTIONS rather than exhibit numbers, deliberately: this
deck was built without the publisher's slides for this chapter, so no exhibit number is
cited anywhere. Tell students to read by section. If you want exhibit numbers, add them
from your copy before recording.

If you cut material today, leave this slide up while you say what got cut and where to read
it. Point forward: this chapter assumed every cost of a transaction falls on the two
parties doing it. Chapter 9 removes that.""")

# ============================================================ 41. takeaways
s = S()
D.takeaways_page(s, "Chapter 8: Trade", [
    "The slope of a production possibilities curve is an opportunity cost. That is what "
    "the curve is for.",
    "Comparative advantage — lowest opportunity cost — decides who should do what. Being "
    "better at something is not being cheaper at it.",
    "Specialise and trade at a price between the two opportunity costs, and both sides "
    "consume outside their own curve. Nobody worked harder.",
    "Compare the world price with your own no-trade price. Below it you import, above it "
    "you export, and either way the country gains on net.",
    "A tariff is a transfer plus a deadweight loss. The transfer is arguable; the two "
    "triangles are value that stops existing.",
])
D.notes(s, """Key takeaways. The second and third matter beyond this course.

If they remember one thing, make it the third: two people, the same hours, the same skills,
more of everything at the end. Two hundred years old, still counter-intuitive, and the best
advertisement the subject has.

The first, second and fifth are the examinable core, and the tariff diagram will be asked as
a drawing.

Close on the honest note rather than the triumphant one. Everything today was a statement
about totals — the chapter proved the total gets bigger, not that everyone gains, and the
diagram showed the losers in red from the first picture.

Next: today every cost of a transaction fell on the people making it. Next time somebody
outside the transaction pays part of the bill and the price stops telling the truth. That
is Chapter 9.""")

prs.save(OUT)
print(f"{OUT}: {len(prs.slides._sldIdLst)} slides")
