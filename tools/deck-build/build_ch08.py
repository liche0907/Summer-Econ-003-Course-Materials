#!/usr/bin/env python3
"""Build ECON003_Ch08_Trade_UCR.pptx.

Built from the Ch07 deck to claude/slide-ground-rules.md.  Static - no animations, by
rule.  The title slide keeps the UCR card and its text and carries NO bottom-right
picture, by instruction.

THIS CHAPTER HAS NO PUBLISHER DECK ON DISK.  Slides/Pearson/ runs Ch01-Ch07 only, so
there are no publisher photographs to place and no publisher exhibit numbers to cite.
Every figure here is ours, from ch08_charts.py.  The chapter's SECTION structure is the
book's (8.1 The Production Possibilities Curve, 8.2 The Basis for Trade: Comparative
Advantage, 8.3 Trade Between States, 8.4 Trade Between Countries, 8.5 Arguments Against
Free Trade), as are its four boxed features and its Evidence-Based Economics question.
The worked NUMBERS are ours, because the book's could not be recovered - so the recap
table points at sections, never at exhibit numbers, and the notes say so.
"""
import os

from pptx import Presentation

import deckkit as D
from deckkit import (BLUE, GOLD, DGOLD, GREEN, RED, INK, INK2, GREY, RULE, WHITE,
                     TINT_BLUE, TINT_NEUTRAL, TINT_RED, TINT_GREEN, TINT_GOLD)

SRC = ("/mnt/user-data/uploads/ECON003_26S/Slides/"
       "ECON003_Ch07_Perfect_Competition_and_the_Invisible_Hand_UCR_v3.pptx")
OUT = "ECON003_Ch08_Trade_UCR.pptx"
F = "figs/ch08_fig_%s.png"
IC = "icons/%s.png"

LIMIT = 4.40          # nothing but the kicker below this
# Figure pages carry no card row. A lead band that wraps to a SECOND line costs the
# figure 0.28 in of height, and figures here are height-bound - so every figpage lead
# is written to fit one line at 13.5 pt.
FIG_FLOOR = 4.42

prs = Presentation(SRC)
D.drop_slides_after(prs, 1)
s1 = prs.slides[0]
# The Ch07 deck's NYSE title triangle comes across with the card. No cover image on this
# chapter for now, by instruction - so drop the picture and leave the shape tree alone.
for _sh in list(s1.shapes):
    if _sh.shape_type == 13:
        _sh._element.getparent().remove(_sh._element)
D.retitle_title_slide(s1, ["Chapter 8", "Trade"],
                      ["ECON 003", "UC Riverside · Summer 2026"])
D.notes(s1, """Title.

Chapter 8. Trade — and the chapter is built as a ladder. The same single idea is proved
three times at three scales: between two people, between two states, between two
countries. Nothing changes as you climb it except the size of the units.

No theme image on the title card, by instruction.

The sentence to open with: for seven chapters we have watched people and firms make
themselves better off inside one market. Today we let them trade ACROSS markets, and the
result is the closest thing economics has to a free lunch — two people, working exactly
the same hours with exactly the same skills, ending up with more.""")


def S():
    return D.blank_slide(prs)


def figpage(title, lead, fig, kick, credit=None, lead_kind="formula", lead_size=13.5):
    """Title, one-line lead band, the figure, a kicker. The workhorse of this deck.

    The figure box is driven off the band's RETURNED bottom and off the kicker, never
    off a hard-coded offset - see ground rules S3.
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
     "designs that outcome; the price produces it.", IC % "balance-scale"),
    (RED, "What we assumed", "One market, one good, one price. Everyone inside the same "
     "border, facing the same conditions.", IC % "factory"),
    (GREEN, "What we drop today", "That border. Once two producers can trade, the good "
     "can be made where it is cheapest to make.", IC % "shipping-container"),
])
D.kicker(s, "Today's question: why does anyone gain from trading with someone who is "
            "worse at everything?", y=4.52)
D.notes(s, """Recap and framing. Keep it to thirty seconds.

The only card that matters is the third. Everything in Chapters 4 through 7 happened
inside one market with one price. Today we let a second producer exist, with different
costs, and ask where things should get made.

The question at the bottom is the one the whole hour turns on, and it is worth posing it
as a paradox out loud: if I am faster than you at literally everything, what could you
possibly do for me? Most people's instinct is "nothing". The answer is that the instinct
is wrong, and provably so — and the proof is arithmetic a first-year student can do.

Do not answer it yet. It gets answered on the slide called "Nobody Worked Harder".""")

# ========================================================== 3. roadmap
s = S()
D.title(s, "Today's Roadmap")
D.strip5(s, 1.30, [
    ("1. What one\nperson can make", IC % "cook"),
    ("2. Who should\ndo what", IC % "balance-scale"),
    ("3. Trade between\nstates", IC % "truck"),
    ("4. Trade between\ncountries", IC % "shipping-container"),
    ("5. The case\nagainst", IC % "ballot-box"),
])
D.rect(s, 0.60, 3.05, 8.80, 0.06, fill=RULE)
D.cards2(s, 3.32, 1.42, [
    (BLUE, "One idea, three scales",
     "Parts 1 and 2 build the whole argument using two people and a food cart. Parts 3 "
     "and 4 change nothing but the size of the units — states, then countries."),
    (GOLD, "And the question we close on",
     "Will free trade cause you to lose your job? That is the book's own question for "
     "this chapter, and it is the honest one. We answer it in Part 5."),
])
D.notes(s, """Roadmap.

Say the shape out loud, because it is unusual and it is the reason this chapter is easy
if you follow it and impossible if you don't: the entire argument is built in Parts 1 and
2, at the smallest possible scale — two people making burritos and smoothies. Parts 3 and
4 do not introduce a new idea. They re-run the same arithmetic with bigger units.

So a student who understands slide 27 understands the chapter. Tell them that.

Part 5 is the counterweight and it is not a formality. The book's own Evidence-Based
Economics question for this chapter is "Will free trade cause you to lose your job?" —
not "isn't trade wonderful". Flag now that we will take that seriously.""")

# ============================================ 4. the carried question
s = S()
D.title(s, "A Question to Carry Through the Hour")
y = D.band(s, 1.15, "Will free trade cause you to lose your job?", kind="note", size=19)
D.cards3(s, y + 0.30, LIMIT - (y + 0.30), [
    (RED, "The answer most people give", "Yes. Cheaper imports arrive, the factory that "
     "made the same thing here closes, and those jobs are gone. This happens, it is "
     "documented, and pretending otherwise is not economics."),
    (BLUE, "The answer the model gives", "Trade changes WHICH jobs exist, not how many. "
     "The number of jobs is set by other things entirely — mostly by how many people "
     "want to work."),
    (GREEN, "Why both can be true", "A country can gain overall while specific people "
     "lose badly. The gain is spread thin; the loss is concentrated. Part 5 is about "
     "exactly that gap."),
])
D.kicker(s, "Hold your answer. We come back to this at the end, with the model behind "
            "us.", y=4.52)
D.notes(s, """The carried question. This is the book's Evidence-Based Economics question
for Chapter 8, and it is worth putting up front even though the book puts it at the end.

Pause here and let them think, or if you are recording, say "pause the video and decide
your answer now" — it works better than asking rhetorically.

Do not soften the first card. The empirical literature on trade shocks and local labour
markets is real and it is not kind to the naive version of the free-trade argument.
Students who have heard about closed factories are not confused; they are right about
something the simple model does not describe.

The reconciliation on the third card is the actual intellectual content of the chapter's
ending, and it is worth previewing: economists are making a claim about the SIZE of a
total, and critics are making a claim about its DISTRIBUTION. Those are different claims
and both can be correct at once.

Say plainly: nothing in the next forty minutes settles this question. The model tells us
how big the pie gets. It says nothing about who eats.""")

# ========================================================== 5. three scales
s = S()
D.title(s, "One Idea, Three Scales")
y = D.defbox(s, 1.15,
             "Trade happens because people have different opportunity costs.\n"
             "That is the whole chapter. Everything else is a change of units.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "Two people", "Maya and Owen run a food cart. One of them is faster at "
     "everything. They still both gain by splitting the work.", IC % "cook"),
    (DGOLD, "Two states", "California grows almonds, Iowa grows corn. Nobody thinks "
     "this is a problem, and nobody proposes a tariff at the state line.", IC % "wheat"),
    (RED, "Two countries", "Exactly the same arithmetic. Different politics — because "
     "now there is a border, and a border can be taxed.", IC % "shipping-container"),
])
D.kicker(s, "If you accept the first card, you have already accepted the third. The "
            "argument does not change.", y=4.52)
D.notes(s, """The ladder. This slide is the map of the hour and it is worth thirty
seconds of care.

The rhetorical move in the middle card is the one that does real work. Nobody in
California campaigns for a tariff on Iowa corn. Nobody proposes protecting Riverside's
domestic almond industry from Fresno. And yet the economics of a state line and a
national border are identical — the difference is entirely political and legal.

That is not a trick, and you should not present it as one. There ARE real differences at
a national border: different labour laws, different environmental rules, different
currencies, and no shared system for compensating the losers. Part 5 takes those
seriously. But the CORE arithmetic is the same, and starting from the state line makes
that impossible to miss.

The last line is the one to say twice.""")

# ============================================================ 6. DIVIDER 1
s = S()
D.divider(s, "PART 1", "What One Producer Can Do")
D.notes(s, """Part 1 divider.

Section 8.1 of the book. Two things happen here: students meet the production
possibilities curve, and they learn that its slope is an opportunity cost.

Worth flagging: most textbooks put the PPC in an early chapter about scarcity. This book
holds it back until the trade chapter, and that is a deliberate and good choice — the
curve is introduced exactly where it earns its keep. If your students have seen a PPC in
another course, this will feel like revision for four minutes. Let it.""")

# ================================================== 7. the two producers
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
D.band(s, 3.66, "Read every number as a rate: this is what one hour of that person's "
                "time produces.", kind="formula", size=13.5)
D.kicker(s, "Two people, two goods, and one thing that is genuinely scarce: hours.",
         y=4.52)
D.notes(s, """The setup. Every number in Parts 1, 2 and 3 comes off this table, so it is
worth reading out loud slowly.

Maya: twelve burritos an hour, or twelve smoothies an hour.
Owen: four burritos an hour, or eight smoothies an hour.
Eight-hour shift each.

Two things to make explicit now, because they cause every misunderstanding later:

First, these are rates of production per hour, not totals. The totals in the last column
are what you get if someone spends the WHOLE shift on one good.

Second, and say this out loud: Maya is faster than Owen at both jobs. Twelve beats four,
and twelve beats eight. She is not slightly better; she is comfortably better at
everything. Students should be sitting there thinking Owen has nothing to offer. Good.
That is the position we are going to dismantle.

The scarce thing is hours. Not skill, not money — hours. If hours were free there would
be no opportunity cost and no economics.

Bridge for anyone reading ahead: the book runs its own numerical example here with
different names and different goods. The logic is identical; only the arithmetic is
ours.""")

# =========================================================== 8. Maya's PPC
figpage("Everything Maya Could Make in a Day",
        "Eight hours on burritos, eight on smoothies, or any split in between.",
        "ppc_one",
        "The curve is not a prediction. It is the edge of the possible.")
D.notes(prs.slides[-1], """The production possibilities curve. First appearance, so build
it rather than presenting it.

Walk it: all eight hours on burritos gives 96 burritos and no smoothies — that is the
point on the horizontal axis. All eight hours the other way gives 96 smoothies — the
vertical axis. Four and four gives 48 and 48, halfway along. Join them up and you have
every combination she could produce.

The three lettered points are the examinable part:

C is ON the curve. Every hour is used and used well. Economists call this efficient, and
remember from Chapter 7 that "efficient" is a narrow technical word — it means nothing is
being wasted, not that this is the best or fairest point.

D is INSIDE. She could have more of both. Something is being wasted: an idle hour, a
broken blender, a badly organised kitchen. Note that D is attainable — it is just poor.

U is OUTSIDE. Not enough hours in the shift. Wanting it does not help.

The one thing students get wrong: a point inside the curve is not "a choice to work
less". It is a failure. Sitting down for two hours moves you to a point inside — and the
whole point of the picture is that this is strictly worse, not a trade-off.""")

# ========================================================= 9. three points
s = S()
D.title(s, "Three Kinds of Point, and Only One of Them Is Interesting")
y = D.defbox(s, 1.15,
             "A point on the curve is efficient: every hour is used, and you cannot get "
             "more of one good without giving up some of the other.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "On the curve", "Attainable and efficient. To get more burritos you must "
     "accept fewer smoothies. There is a genuine trade-off here, and that is what makes "
     "it interesting."),
    (GREY, "Inside the curve", "Attainable and wasteful. You could have MORE of both. "
     "There is no trade-off to think about — just a mistake to fix."),
    (RED, "Outside the curve", "Not attainable. Not this shift, not with these skills. "
     "New equipment or a longer day would move the whole curve out."),
])
D.kicker(s, "Economics is about the first case. The other two need a manager, not an "
            "economist.", y=4.52)
D.notes(s, """The vocabulary slide. Short.

The line to land is the kicker. A point inside the curve poses no economic problem — it
poses an operational one. If you can have more of everything, take it; nothing to decide.
A point outside poses no problem either, because it isn't available.

Only points on the curve involve a choice, because only there does more of one thing
require less of another. That is why the curve is drawn at all.

If a student asks what moves the curve outward: more hours, better equipment, better
technique, another pair of hands. Anything that changes what an hour is worth. That is
economic growth in one sentence, and it is worth saying because they will meet it again.

Careful with the word "efficient" — you spent time in Chapter 7 narrowing it, so keep it
narrow here. On the curve means nothing is wasted. It does not mean good.""")

# ================================================== 10. the slope
figpage("The Slope of the Curve Is an Opportunity Cost",
        "Move along the curve and ask what the extra burritos cost.",
        "ppc_slope",
        "That is what the curve is FOR: it puts a price on your own time, in the "
        "other good.")
D.notes(prs.slides[-1], """The single most important idea in Part 1, and the one that
carries the whole chapter.

Walk the arrows. Maya starts at 48 and 48. She decides she wants twelve more burritos.
Twelve burritos is one hour of her time. That hour has to come from somewhere, and the
only place it can come from is smoothies — where it was producing twelve smoothies.

So twelve more burritos cost twelve smoothies. One burrito costs one smoothie.

Now say the general version: the slope of the PPC IS the opportunity cost. Not "shows",
not "relates to" — is. The steepness of that line is literally the exchange rate between
the two goods inside Maya's own day.

Reinforce the Chapter 3 link out loud: opportunity cost is not money. Nobody paid
anything here. The cost of the burritos is the smoothies that did not get made.

Examinable, and they will be asked it in both directions: if one burrito costs one
smoothie, then one smoothie costs one burrito. Students routinely fail to invert
correctly when the numbers are not one-to-one, so drill it on Owen in two slides' time,
where the answer is a half.""")

# =================================================== 11. reading a cost off
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
     "Invert it. A burrito costs Maya 1 smoothie, so a smoothie costs her 1 burrito. "
     "A burrito costs Owen 2 smoothies, so a smoothie costs him half a burrito."),
    (RED, "Where marks get lost",
     "Answering the wrong question. “Opportunity cost of a burrito” must be "
     "answered IN SMOOTHIES. If your answer is in burritos, you have inverted it."),
])
D.kicker(s, "Same one hour, two different exchange rates. That difference is the entire "
            "reason to trade.", y=4.52)
D.notes(s, """The mechanics, and this is examinable in every version of this exam.

Read the formula out and then do both lines slowly.

Maya gives up twelve smoothies to gain twelve burritos, so one burrito costs one
smoothie. Owen gives up eight smoothies to gain four burritos, so one burrito costs TWO
smoothies. Owen's burritos are expensive — in smoothies.

Now the inversion, which is where students lose marks. Say it explicitly: the opportunity
cost of a burrito is measured in smoothies, and the opportunity cost of a smoothie is
measured in burritos. They are reciprocals. Maya's are both 1, which is convenient for
seeing the idea and dangerous for testing it — so use Owen. A burrito costs him 2
smoothies; a smoothie costs him half a burrito.

If you set one live question in this lecture, make it "what is Owen's opportunity cost of
one smoothie?" and give them fifteen seconds. The answer is half a burrito, and a good
fraction of the room will say two.

Last line, and it is the hinge of the chapter: Maya and Owen face different exchange
rates between the same two goods. Whenever two people value something differently, there
is a trade that makes them both better off. That is not special to economics — it is why
anyone swaps anything.""")

# ================================================ 12. why a straight line
s = S()
D.title(s, "Why This Curve Is a Straight Line")
y = D.defbox(s, 1.15,
             "Maya's opportunity cost never changes: every hour she shifts buys the "
             "same 12 burritos. Constant opportunity cost draws a straight line.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "One person, one skill", "Maya's tenth hour is as good as her first. Nothing "
     "about her gets better or worse as she switches, so the rate is constant."),
    (DGOLD, "But add people", "Different people have different costs. Shift the "
     "cheapest ones first and the rate rises as you go. That bends the line."),
    (GREEN, "Which is Part 3", "A whole economy's curve is bowed outward, and it is "
     "bowed for exactly that reason. We draw it in Part 3.", IC % "up-down"),
])
D.kicker(s, "Straight means constant cost. Bowed means rising cost. The shape is telling "
            "you something.", y=4.52)
D.notes(s, """Short slide, but it prevents a genuine confusion later.

Students who have seen a PPC before have almost certainly seen a bowed one, and they will
be quietly wondering why ours is straight. Answer it before they ask.

A straight PPC says the opportunity cost is the same everywhere along it. That is
realistic for ONE person with ONE skill: Maya's eighth hour is as productive as her
first, so switching an hour always costs the same.

It stops being realistic the moment you aggregate. An economy has millions of people with
millions of different opportunity costs. If you want more burritos you move the
cheapest-to-switch people first, then the next cheapest, and the cost of each additional
burrito rises. That is what bows the curve outward.

Do not draw it yet. Just plant it, and point at Part 3.

A sharp student may ask whether ONE person's curve could bow — yes, if she gets tired, or
if the equipment only suits one task. We are assuming that away, and it is worth saying
that we are assuming it rather than letting it pass.""")

# ============================================== 13. two curves
figpage("Owen's Curve, Same Axes",
        "Owen is slower at both jobs — and his curve is a different SHAPE.",
        "ppc_two",
        "Maya's curve is further out everywhere. Watch the STEEPNESS instead: that is "
        "where the story is.")
D.notes(prs.slides[-1], """Two curves, and the point is the comparison.

First the obvious thing: Maya's curve is outside Owen's at every point. She can make more
burritos AND more smoothies. That is what absolute advantage looks like on a picture, and
it is what makes students think Owen is useless.

Now the thing that actually matters, and it takes a deliberate pause: the two curves have
different SLOPES. Maya's runs from 96 to 96, so it falls at one-for-one. Owen's runs from
32 to 64, so it falls at two-for-one — twice as steep.

Different slopes mean different opportunity costs. And different opportunity costs mean
there is something to trade, no matter who is faster.

Say the sentence that sets up Part 2: the height of the curve tells you who is more
productive; the slope of the curve tells you who should do what. Students conflate those
two facts for the entire chapter unless you separate them here, deliberately, with the
picture in front of them.

Both panels are drawn on the same axis scale, so the comparison of position is fair as
well as the comparison of slope.""")

# ============================================= 14. what a PPC does not say
s = S()
D.title(s, "What the Curve Does Not Tell You")
y = D.band(s, 1.12, "A production possibilities curve is a menu, not a decision.",
           kind="formula", size=15)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (RED, "It does not pick a point", "Every point on the curve is efficient. Which one "
     "you want depends on what you like — and that is Chapter 5's problem, not this "
     "chapter's."),
    (RED, "It does not price anything", "There is no money on these axes. The only cost "
     "here is the other good, which is what makes it an opportunity cost."),
    (RED, "It does not say who is better off", "Two people can both be on their own "
     "curve and one of them can still be far poorer. The curve is about capacity, not "
     "welfare."),
])
D.kicker(s, "The curve tells you what is possible. It never tells you what to want.",
         y=4.52)
D.notes(s, """The honesty slide for Part 1. Every part of this deck has one — the place
where the model stops and we say so.

The first card is the one worth dwelling on, because it is a habit of mind rather than a
fact. A model that narrows the options is doing its job. A model that picks for you is
usually smuggling in a value judgement.

The second card kills a common error before it starts: students want to put dollars on
these axes. There are no dollars. The cost of a burrito is a smoothie. Money enters in
Part 4 and not before.

The third card is a forward reference to Part 5. A country can be on its production
possibilities curve, trading efficiently, and still contain people who are much worse off
than they were. Efficiency does not distribute.

Keep this to forty seconds and move.""")

# =============================================== 15. checkpoint 1
s = S()
D.title(s, "Checkpoint: What You Should Be Able to Do")
y = D.band(s, 1.12, "Before we go on, three things from Part 1.", kind="neutral",
           size=14)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "Draw it", "Given output per hour and a number of hours, draw the curve. Both "
     "intercepts are just rate × hours."),
    (BLUE, "Read the slope", "State the opportunity cost of one unit of EACH good, in "
     "units of the other. Two answers, and they are reciprocals."),
    (BLUE, "Classify a point", "On, inside or outside — and say what each one means "
     "about how the hours are being used."),
])
D.kicker(s, "All three appear on the problem set, and all three appear on the final.",
         y=4.52)
D.notes(s, """Checkpoint. Twenty seconds, and it exists so students can self-assess
before the harder material.

If you are recording, this is a good place to suggest a pause and a scratch pad.

The one to emphasise is the middle card: two answers, and they are reciprocals. Every
term, a substantial number of students give the opportunity cost of a burrito in
burritos.""")

# ============================================================ 16. DIVIDER 2
s = S()
D.divider(s, "PART 2", "Who Should Do What")
D.notes(prs.slides[-1], """Part 2 divider. Section 8.2 of the book — the heart of the
chapter and, honestly, the heart of the course's claim to be non-obvious.

Everything after this is application. If they get Part 2, Parts 3, 4 and 5 are
bookkeeping.""")

# =================================================== 17. absolute advantage
figpage("The Obvious Answer: Who Is Better?",
        "Absolute advantage: producing more of a good with the same resources.",
        "advantage",
        "Maya wins both bars. On the obvious answer, Owen should not be employed at all.")
D.notes(prs.slides[-1], """Absolute advantage. Define it, then show why it is the wrong
tool.

Definition to give them, and it is a key term: a producer has an ABSOLUTE ADVANTAGE in a
good if they can make more of it with the same resources. It is a comparison of
productivity, straight up.

Read the bars. Maya makes twelve burritos an hour to Owen's four — absolute advantage in
burritos. Twelve smoothies an hour to Owen's eight — absolute advantage in smoothies too.
She has both.

Now say the conclusion that the picture appears to support, and say it in a voice that
makes clear you are about to demolish it: on this evidence, Maya should do everything and
Owen should go home.

That conclusion is wrong. Not "incomplete" — wrong. And the next four slides prove it
with arithmetic they can check.

This is the single best moment in the chapter for a live question if you use them: "Maya
is faster at both jobs. Should she hire Owen?" Most rooms say no.""")

# ============================================== 18. why it is the wrong question
s = S()
D.title(s, "And Why That Is the Wrong Question")
y = D.defbox(s, 1.15,
             "Maya cannot do both jobs at once. Every hour she spends on smoothies is "
             "an hour not spent on burritos — where she is spectacular.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (RED, "The question that fails", "“Who is faster at this job?” It ignores "
     "what the faster person gives up by doing it.", IC % "clock"),
    (GREEN, "The question that works", "“Who gives up the least by doing this "
     "job?” That is an opportunity cost question, and it has a different answer."),
    (BLUE, "Why they differ", "Being good at everything means everything you do costs "
     "you something else you were good at. Skill does not remove the trade-off."),
])
D.kicker(s, "Being the best at a job is not a reason to do it. Being the cheapest at it "
            "is.", y=4.52)
D.notes(s, """The pivot of the chapter. Slow down here — this is thirty seconds of
material that deserves ninety.

The trap in absolute advantage is that it compares people at a job and forgets that time
is finite. Maya's hour of smoothie-making does not appear from nowhere. It comes out of
burrito-making, where she is producing twelve an hour. Owen's hour of smoothie-making
comes out of burrito-making too, where he only produces four.

So the same hour of smoothies costs Maya a great deal and costs Owen very little.

The kicker is the sentence to repeat. Being the best at something is not a reason to do
it. Being the CHEAPEST at it is. And "cheapest" here means lowest opportunity cost — it
has nothing to do with wages.

A useful analogy if the room is quiet: a surgeon who types faster than her assistant
still does not do her own typing. Not because she can't. Because the hour costs her an
operation. Students find that instantly obvious, and it is exactly the same argument.""")

# ================================================= 19. opportunity cost table
s = S()
D.title(s, "Opportunity Cost, Side by Side")
D.band(s, 1.12, "The same two people, priced in each other's goods rather than in "
                "output per hour.", kind="neutral", size=14)
D.table(s, 1.00, 1.86, 8.00, 1.68, [
    ["", "Cost of ONE burrito", "Cost of ONE smoothie", "Cheapest at"],
    ["Maya", "1 smoothie", "1 burrito", "burritos"],
    ["Owen", "2 smoothies", "½ burrito", "smoothies"],
], col_w=[1.30, 2.40, 2.40, 1.90], first_col_fill=BLUE, header_size=10.5,
    body_size=11.5, align=["l", "ctr", "ctr", "ctr"])
D.band(s, 3.72, "Maya's burritos are cheap. Owen's smoothies are cheap. Nobody is "
                "cheapest at both — and nobody ever can be.", kind="answer", size=13.5)
D.kicker(s, "Read the columns, not the rows: in each column, someone is cheaper.",
         y=4.52)
D.notes(s, """The table that decides the chapter. Give it time.

Column one: a burrito costs Maya one smoothie and costs Owen two. Maya is the
cheap producer of burritos.

Column two: a smoothie costs Maya a whole burrito and costs Owen only half a burrito.
Owen is the cheap producer of smoothies.

Now the striking claim on the green band, and it is worth stating as a theorem rather
than an observation: it is arithmetically impossible for one person to have the lower
opportunity cost in both goods. The costs are reciprocals of each other. If your burritos
are cheaper than mine, your smoothies must be dearer. There is no escape from this — it
is not an empirical regularity, it is division.

That is why there is always a basis for trade. Always. However unequal two producers are
in skill, each of them is the cheap producer of something.

The instruction on the kicker is practical and worth repeating at revision time: to find
comparative advantage, compare DOWN a column, never across a row.""")

# =============================================== 20. comparative advantage
s = S()
D.title(s, "Comparative Advantage")
y = D.defbox(s, 1.15,
             "A producer has a COMPARATIVE ADVANTAGE in a good if they can make it at a "
             "lower opportunity cost than anyone else.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "Absolute advantage", "Compares OUTPUT. Who makes more per hour? Maya, at "
     "both. Tells you who is more productive, and nothing else."),
    (GREEN, "Comparative advantage", "Compares COST. Who gives up least? Maya for "
     "burritos, Owen for smoothies. Tells you who should do what."),
    (DGOLD, "The rule", "Specialise where you have the comparative advantage. Trade for "
     "the rest. It is the answer to the whole chapter.", IC % "exchange"),
])
D.kicker(s, "Absolute advantage is about how good you are. Comparative advantage is "
            "about what you give up.", y=4.52)
D.notes(s, """The definition slide. Both terms are key terms in the book's glossary and
both come up on the exam, usually in the same question, usually designed so that the two
answers differ.

Read the definition off the panel word for word — "lower opportunity cost" is doing all
the work and students who paraphrase it as "better at" have lost the idea entirely.

The contrast on the first two cards is the examinable distinction. A clean way to say it:
absolute advantage is measured in units of output, comparative advantage is measured in
units of the other good.

Then the rule, which is short enough to memorise: specialise where your opportunity cost
is lowest, and trade for everything else.

Worth naming the intellectual history in one sentence, because it is genuinely one of the
oldest results in the subject: this is David Ricardo's argument from 1817, and it is
still the single most counter-intuitive true thing in introductory economics. Two hundred
years and it still surprises people every year.""")

# ================================================ 21. two rules agree
s = S()
D.title(s, "Two Ways to Find It, and They Never Disagree")
y = D.band(s, 1.12, "Method 1 — compare opportunity costs directly. Lower cost wins the "
                    "good.", kind="formula", size=14)
y = D.band(s, y + 0.18, "Method 2 — compare the ratios. Maya makes 12/4 = 3× Owen's "
                        "burritos, but only 12/8 = 1.5× his smoothies.", kind="formula",
           size=14)
D.cards2(s, y + 0.24, LIMIT - (y + 0.24), [
    (GREEN, "What method 2 is saying",
     "Maya's edge is BIGGER in burritos (3×) than in smoothies (1.5×). So burritos are "
     "where her advantage really lies, and that is her comparative advantage."),
    (BLUE, "Use whichever you trust",
     "They give the same answer every time, because they are the same arithmetic written "
     "two ways. In an exam, use the one you make fewer mistakes with."),
])
D.kicker(s, "Even when someone is better at everything, they are relatively better at "
            "something.", y=4.52)
D.notes(s, """A second route to the same answer, offered because students split roughly
evenly on which one they find natural.

Method one is the opportunity cost table from two slides ago. Method two asks by HOW MUCH
each person is better. Maya makes three times as many burritos per hour as Owen, but only
one and a half times as many smoothies. Her advantage is concentrated in burritos, so
burritos are where she should be.

Say clearly that these are not two competing tests that might disagree. They are the same
division performed in a different order, and they cannot give different answers. Students
worry about this.

Tell them to pick one and stick to it. Mixing the two mid-question is where errors come
from.

The kicker is the sentence that generalises: relative advantage always exists, because
"relative" is a comparison and comparisons always have a direction.""")

# ============================================= 22. specialise
s = S()
D.title(s, "Step 1: Specialise")
D.band(s, 1.12, "Each of them does only the job they are cheapest at. Same people, same "
                "hours, same skills.", kind="neutral", size=14)
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
D.notes(s, """The payoff, and the number to say slowly is the green band.

Top row: they each divide their shift. Maya spends six hours on burritos and two on
smoothies, giving 72 and 24. Owen spends four and four, giving 16 and 32. Together: 88
burritos and 56 smoothies.

Bottom row: each does only what they are cheapest at. Maya, all burritos, 96. Owen, all
smoothies, 64.

Compare the last column. Burritos rise from 88 to 96. Smoothies rise from 56 to 64. Eight
more of each.

Now the sentence that matters, and it deserves a pause: no new equipment appeared, nobody
learned a new skill, and nobody stayed late. Sixteen hours went in before and sixteen
hours went in after. The extra output came from nothing except pointing the hours at the
right jobs.

That is what "gains from trade" means, and it is worth saying that it feels like a
conjuring trick the first time and stops feeling like one once you see where it comes
from — the wasted hours were Maya's, spent making smoothies she was bad at relative to
her burritos.

One honest caveat if a sharp student raises it: this comparison depends on the starting
split. With a different starting point the totals move. What NEVER changes is that
specialisation puts them on the outer edge of what the two of them can jointly do — which
is exactly the joint curve we draw in three slides.""")

# ============================================ 23. terms of trade
s = S()
D.title(s, "Step 2: Agree a Price")
y = D.defbox(s, 1.15,
             "The TERMS OF TRADE are the rate at which the two goods actually swap.")
y = D.band(s, y + 0.20, "They settle on:   1 burrito  =  1.5 smoothies", kind="answer",
           size=17)
D.cards2(s, y + 0.24, LIMIT - (y + 0.24), [
    (BLUE, "Why Maya accepts it",
     "After specialising she has 96 burritos and no smoothies at all. Making a smoothie "
     "herself costs her one whole burrito. Buying one from Owen costs her two-thirds of "
     "a burrito. Trading is cheaper than making."),
    (DGOLD, "Why Owen accepts it",
     "After specialising he has 64 smoothies and no burritos at all. Making a burrito "
     "himself costs him two smoothies. Buying one from Maya costs him one and a half. "
     "Trading is cheaper than making."),
])
D.kicker(s, "Both of them are buying the other's good for less than it would cost to "
            "make it themselves.", y=4.52)
D.notes(s, """Terms of trade — a key term, and the piece students most often skip.

The setup is the important bit. After specialising, Maya has 96 burritos and no
smoothies. Owen has 64 smoothies and no burritos. Neither of them can eat a balanced
lunch. They have to swap, and swapping requires a rate.

We pick one-and-a-half smoothies per burrito. Where that number comes from in the real
world is bargaining, or a market price — the model does not determine it, and you should
say so rather than let students think it was derived.

Then walk both cards, because the symmetry is the argument.

Maya: to get a smoothie by making it herself, she gives up a burrito. To get one by
trading, she gives up two-thirds of a burrito. Cheaper.

Owen: to get a burrito by making it, he gives up two smoothies. By trading, one and a
half. Cheaper.

Both are better off at the same rate, at the same time, without anyone being fooled. This
is the moment to say that voluntary trade is not zero-sum — a phrase students have heard
and rarely had demonstrated.""")

# ============================================ 24. which prices work
s = S()
D.title(s, "Which Prices Work, and Which Do Not")
y = D.band(s, 1.12,
           "For both to gain, the price must sit BETWEEN the two opportunity costs:\n"
           "1 smoothie  <  price of a burrito  <  2 smoothies", kind="formula", size=15)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (RED, "Below 1 smoothie", "Maya refuses. She can make a smoothie herself for one "
     "burrito; she will not sell a burrito for less than that."),
    (GREEN, "Between 1 and 2", "Both gain. The closer to 1, the more of the gain goes to "
     "Owen; the closer to 2, the more goes to Maya."),
    (RED, "Above 2 smoothies", "Owen refuses. He can make a burrito himself for two "
     "smoothies; he will not pay more than that."),
])
D.kicker(s, "The two opportunity costs are the bargaining range. The price inside it "
            "decides who gets more of the gain.", y=4.52)
D.notes(s, """The range, and it is examinable — expect a question of the form "which of
these terms of trade would both parties accept?"

The logic is a no-arbitrage argument and it is worth naming as one, because they met the
idea in Chapter 7: nobody buys something for more than it costs them to make, and nobody
sells for less. Those two refusals bracket the price.

Below one smoothie per burrito, Maya is better off staying home and making her own
smoothies. Above two, Owen is better off making his own burritos. Anywhere strictly
between, both are better off than not trading.

Then the distributional point, which is the honest one and which sets up Part 5: WHERE in
the range the price lands decides how the gains are split. At a price near one, Owen
captures most of the gain. Near two, Maya does. The model says both gain; it does not say
they gain equally, and it has nothing to say about which split is fair.

That distinction — trade creates a surplus, bargaining divides it — is the same structure
as the whole free-trade debate at national scale. Point that out here, once, cheaply.""")

# ============================================= 25. the gains
s = S()
D.title(s, "Step 3: Trade — and Count What Changed")
D.band(s, 1.12, "Maya ships 18 burritos. Owen ships back 27 smoothies. That is the "
                "agreed rate, applied.", kind="neutral", size=14)
D.table(s, 0.80, 1.82, 8.40, 1.76, [
    ["", "Alone", "After trading", "Change"],
    ["Maya eats", "72 burritos, 24 smoothies", "78 burritos, 27 smoothies",
     "+6 and +3"],
    ["Owen eats", "16 burritos, 32 smoothies", "18 burritos, 37 smoothies",
     "+2 and +5"],
], col_w=[1.60, 2.45, 2.45, 1.90], first_col_fill=BLUE, header_size=10.5,
    body_size=10, align=["l", "ctr", "ctr", "ctr"])
D.band(s, 3.80, "Both of them have more of BOTH goods. Neither gave anything up.",
       kind="answer", size=14.5)
D.kicker(s, "This is the result the chapter exists to prove — and every number on it is "
            "checkable.", y=4.52)
D.notes(s, """The result. Read the table across, one row at a time, and then stop talking
for a moment.

Maya alone: 72 burritos, 24 smoothies. After trading: 78 and 27. Six more burritos, three
more smoothies.

Owen alone: 16 and 32. After trading: 18 and 37. Two more burritos, five more smoothies.

The green band is the sentence to say twice, because it is the one students will be asked
to reproduce: BOTH parties have MORE of BOTH goods. Not a trade-off. Not a compromise.
More of everything, for both, out of the same sixteen hours.

Two checks worth doing on the board, because they make it feel like arithmetic instead of
magic:

Does it add up? 78 plus 18 is 96 burritos — exactly what Maya produced. 27 plus 37 is 64
smoothies — exactly what Owen produced. Nothing was created in the trade itself. All the
gain came from the specialisation.

Does the exchange rate hold? Eighteen burritos at one and a half smoothies each is
twenty-seven smoothies. It does.

Note also that the gains are NOT split evenly — Maya gains more burritos, Owen gains more
smoothies. That is the price sitting where it sits, and it is worth one sentence.""")

# =========================================== 26. outside your own curve
figpage("Both of Them End Up Outside Their Own Curve",
        "Solid line: what they can MAKE. Dashed line: what they can CONSUME.",
        "trade_line",
        "Trade does not move your production curve. It lets you consume past it.")
D.notes(prs.slides[-1], """The picture of the result, and the single most useful diagram
in the chapter for an exam.

Point at Maya's panel. The solid blue line is her production possibilities curve — it has
not moved and it never moves. She is exactly as fast as she was. The dashed green line is
her CONSUMPTION possibilities: what she can end up with once she can trade at one and a
half smoothies per burrito.

The dashed line lies outside the solid one. Her consumption point, 78 and 27, is a point
she could not possibly produce — 78 plus 27 is 105 and her limit is 96.

Same story in Owen's panel.

The sentence that makes it stick: trade does not make you more productive. It breaks the
link between what you make and what you consume. Before trade those had to be the same
bundle. After trade they are two different bundles and only the first is constrained by
your own skill.

One honest housekeeping point, and say it rather than hoping nobody notices: the two
panels are drawn to DIFFERENT scales, because Owen's numbers are so much smaller that a
shared axis makes his panel unreadable. Both axes shrink by the same factor between the
panels, so the slopes are still comparable — but do not invite students to compare the
two curves' positions across panels.""")

# ============================================ 27. joint PPC
figpage("The Two of Them, Counted Together",
        "Add both producers into one curve. It kinks where the cheap one runs out.",
        "ppc_joint",
        "Specialisation lands them exactly on the corner — the best the two of them can "
        "jointly do.")
D.notes(prs.slides[-1], """The joint curve. This is the most sophisticated diagram in Part
2 and it rewards a slow walk.

Build it from the left. Starting at the top left, everyone is making smoothies: 96 from
Maya plus 64 from Owen is 160. To get burritos, you take them from whoever gives up least
— that is Maya, at one smoothie per burrito. So the first stretch falls at one-for-one.

At 96 burritos, Maya has run out of hours. She is making nothing but burritos. To get any
more you must move Owen, and Owen costs two smoothies per burrito. The line gets steeper.
That is the kink.

Now the punchline, and it is worth its own beat: the kink is exactly the point where each
person does only the job they are cheapest at. Specialisation is not one option among
many — it is the corner of the joint curve, the single point where the two of them,
together, are doing the best they possibly can.

The grey point inside is where they were when they each split their time. The arrow to
the corner is the gain: eight burritos and eight smoothies, from reorganising alone.

Connect it back to Part 1 with one sentence: this curve is bent, and it is bent for
exactly the reason we flagged then — two producers with two different opportunity costs.
Add a third producer and you get a third segment. Add millions and you get the smooth
bowed curve of Part 3.""")

# ============================================ 28. nobody worked harder
s = S()
D.title(s, "Nobody Worked Harder")
y = D.defbox(s, 1.15,
             "Sixteen hours went in before. Sixteen hours went in after. There is more "
             "food. That is the entire argument for trade, at every scale.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "Where the gain came from", "Hours that were producing at a bad exchange "
     "rate are now producing at a good one. Nothing else changed.", IC % "clock"),
    (BLUE, "Why it works with unequal partners", "Because opportunity costs are "
     "reciprocals. Whoever you are, you are the cheap producer of something."),
    (DGOLD, "And the answer to the opening question", "Owen is worse at everything and "
     "Maya still wants to trade with him. Her alternative is making smoothies herself, "
     "at one burrito each.", IC % "exchange"),
])
D.kicker(s, "You do not trade with someone because they are good. You trade with them "
            "because your own time is expensive.", y=4.52)
D.notes(s, """The close of Part 2, and the answer to the paradox posed at the start.

Say the first line as a challenge: sixteen hours before, sixteen hours after, more food
out the other end. If a student cannot say where the extra food came from, they have not
got the chapter. The answer is on the first card — the hours were reallocated to where
they were worth more.

The third card is the direct answer to the opening question and it deserves to be
delivered as an answer, not as a summary. Maya trades with Owen not out of charity and
not because Owen is any good. She trades with him because her own alternative is bad:
every smoothie she makes herself costs her a burrito, and burritos are what she is
extraordinary at. Owen's smoothies are cheap for her precisely because her own are
expensive.

The kicker generalises it to something students can carry out of the room: you outsource
what your own time is too valuable to spend on. That is the same reason a country imports
T-shirts and the same reason a surgeon does not do her own typing.

If you cut anything from this deck, do not cut this slide.""")

# ============================================ 29. the experiment box
s = S()
D.title(s, "Does It Actually Happen? An Experiment")
y = D.band(s, 1.12,
           "Put people in a room, give them different production rates, and let them "
           "trade. Do they find the pattern?", kind="note", size=14.5)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "What the theory predicts", "Each person should end up doing the job with "
     "their own lowest opportunity cost — without being told the rule."),
    (DGOLD, "Why it is worth testing", "Comparative advantage is counter-intuitive. A "
     "result that has to be taught might not be a result people act on.", IC % "research"),
    (GREEN, "Why the answer matters", "If specialisation only emerges when an economist "
     "explains it, it is a classroom curiosity. If it emerges on its own, it is a "
     "description of the world."),
])
D.kicker(s, "The textbook devotes a box to this precisely because the result is too "
            "strange to take on trust.", y=4.52)
D.notes(s, """This corresponds to the book's Choice and Consequence box in section 8.2,
"An Experiment on Comparative Advantage". One of the book's authors runs field and
laboratory experiments for a living, which is why an experimental box appears here rather
than a worked example.

IMPORTANT AND PLEASE READ BEFORE DELIVERY: I could not obtain the text of that box, so
this slide frames the QUESTION the experiment asks rather than reporting its result. Do
not state a finding from this slide. Open the book to section 8.2 before you record, read
the box, and either add the result to the notes or deliver this as posed here.

Delivered as it stands, the slide still earns its place — the middle card is a genuinely
good methodological point for a first-year class. A theory that only works when someone
explains it is a weaker theory than one people follow without being told.

If you would rather cut a slide from Part 2, this is the one to cut.""")

# ============================================ 30. checkpoint 2
s = S()
D.title(s, "Checkpoint: The Examinable Core")
y = D.band(s, 1.12, "If you learn four things from this lecture, learn these.",
           kind="neutral", size=14)
D.cards4(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "1. The two advantages", "Absolute compares output. Comparative compares "
     "opportunity cost. Say which the question is asking for."),
    (BLUE, "2. Finding it", "Build the opportunity cost table. Compare DOWN the columns. "
     "Lower cost takes the good."),
    (BLUE, "3. The range", "Both gain only if the terms of trade sit strictly between "
     "the two opportunity costs."),
    (BLUE, "4. The result", "After specialising and trading, both consume outside their "
     "own production curve."),
])
D.kicker(s, "Everything in Parts 3, 4 and 5 is these four ideas with bigger numbers.",
         y=4.52)
D.notes(s, """Checkpoint. This is the slide to tell them to photograph.

All four appear on the problem set and at least two will appear on the final. Number
three is the one most often missed, because it requires an inequality rather than a
calculation.

Say the kicker and mean it: from here on, nothing new is being claimed. Parts 3 and 4
substitute states and countries for Maya and Owen. Part 5 asks whether the gains are
distributed in a way anyone should be happy about.""")

# ============================================================ 31. DIVIDER 3
s = S()
D.divider(s, "PART 3", "The Same Logic,\nBigger Units")
D.notes(prs.slides[-1], """Part 3 divider. Section 8.3 of the book, "Trade Between
States".

Worth knowing why this section exists at all: most textbooks go straight from two people
to two countries. This book deliberately puts a rung in between, and the rung is
rhetorically powerful — nobody has strong feelings about interstate trade, so the
economics can be seen without the politics attached.""")

# ============================================ 32. economy PPC
figpage("From One Person to a Whole Economy",
        "Every producer has their own opportunity cost. Switch the cheapest ones first.",
        "ppc_economy",
        "Four producers give you a staircase. Millions of them give you a smooth curve.")
D.notes(prs.slides[-1], """The economy-wide production possibilities curve. This is the
promise made back in Part 1, now paid.

Left panel: four producers instead of two. Start with everyone making good Y. To get some
X, move the producer with the lowest opportunity cost of X. Then the next lowest. Each
segment is one producer, and each is steeper than the last, because you are working
through them from cheapest to dearest.

Right panel: do that with millions of producers and the steps become invisible. What is
left is a smooth curve, bowed outward from the origin.

The reason for the bow is the whole content of the picture, so state it as a sentence
students can write down: the curve bows out because opportunity cost RISES as you produce
more of a good. And it rises because the economy runs out of the people and land and
machinery that are cheap at that job, and starts using the ones that are expensive.

A concrete version, and it lands better than the abstract one: the first acre of
California converted to almonds is an acre that was terrible for anything else. The
millionth is an acre you had to take from something valuable.

This is a named concept in the book — the economy-wide PPC — and it appears on exams as
"why is the PPC bowed outward?" The answer is one sentence: increasing opportunity
cost.""")

# ============================================ 33. why bowed
s = S()
D.title(s, "Why the Economy's Curve Bends and Maya's Did Not")
y = D.band(s, 1.12,
           "One person, one skill  →  constant opportunity cost  →  a straight line\n"
           "Many producers, many skills  →  rising opportunity cost  →  a bowed curve",
           kind="formula", size=14.5)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "The cheap ones go first", "Nobody moves the best corn land into almonds "
     "first. You move the land that was bad at corn anyway."),
    (DGOLD, "Then it gets expensive", "Keep going and you are converting good corn land. "
     "Each extra tonne of almonds costs more corn than the last.", IC % "wheat"),
    (RED, "Which is what the bow IS", "The curve gets steeper as you move right. That "
     "steepening is rising opportunity cost, drawn."),
])
D.kicker(s, "Resources are not interchangeable. That single fact is the shape of the "
            "curve.", y=4.52)
D.notes(s, """A slide that exists because "the PPC is bowed outward due to increasing
opportunity cost" is a sentence students memorise without understanding.

Make them see the mechanism. Land, people and machines are specialised. Some land is good
for corn and useless for almonds. Some people are good at one job and hopeless at the
other. When a country shifts from one good to another it moves the least suitable
resources first, because those are the cheapest to move.

As you keep going you run out of unsuitable resources and start moving the suitable ones.
The cost per unit rises. Drawn, that is a curve that gets steeper as you go right.

The counterfactual is the fastest way to check understanding: if every resource were
equally good at both jobs, the curve would be a straight line, exactly like Maya's. It is
the DIVERSITY of resources that bends it.

Watch out for a common student error: they say the curve bows because of "diminishing
returns" or "scarcity". Scarcity is why there is a curve at all. Diversity of opportunity
cost is why it bends.""")

# ============================================ 34. LeBron box
s = S()
D.title(s, "Should LeBron James Paint His Own House?")
y = D.defbox(s, 1.15,
             "Suppose he is genuinely a faster painter than any professional he could "
             "hire. Should he pick up the brush?")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (RED, "The absolute advantage answer", "Yes. He paints faster than the painter, so "
     "he should do it himself and save the fee.", IC % "house"),
    (GREEN, "The comparative advantage answer", "No. The hours cost him training, "
     "filming and playing. The painter's hours cost far less."),
    (BLUE, "The general form", "The higher your best alternative, the more of your life "
     "you should be buying from other people.", IC % "clock"),
])
D.kicker(s, "He does not hire a painter because he is bad at painting. He hires one "
            "because his afternoons are expensive.", y=4.52)
D.notes(s, """The book's Choice and Consequence box in section 8.3. Students remember this
one, so use it as the anchor for the whole idea.

Set it up carefully: the interesting version of the question assumes he really IS a
better painter. If he were worse, there would be nothing to discuss. Absolute advantage
in painting, and he should still hire someone.

Why? Because the cost of his afternoon is not measured in paint. It is measured in what
else that afternoon could have produced — training, endorsements, a game. The painter's
afternoon has a much lower alternative value. So the painter is the CHEAP producer of
painting even though he is the SLOW producer of painting.

This is the exact structure of Maya and Owen, in a form students already believe. Say that
out loud — it is the same argument and they should notice.

Then generalise with the third card, because it is the version that will outlive the
course: the more valuable your time, the more of your life you should buy from others.
And it runs both ways — the reason someone else is happy to sell you that hour is that
their alternative was worth less. Both sides gain. Again.

Keep it to a minute. It is an illustration, not a proof.""")

# ============================================ 35. states specialise
s = S()
D.title(s, "States Specialise, and Nobody Files a Complaint")
y = D.band(s, 1.12,
           "Fifty states, one currency, no tariffs, no paperwork — and extreme "
           "specialisation everywhere you look.", kind="neutral", size=14)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (DGOLD, "California", "Almonds, avocados, wine, strawberries. Not because Californians "
     "cannot make other things — because the land is worth more doing this.", IC % "wheat"),
    (GREEN, "Iowa", "Corn and soybeans, at a scale that has nothing to do with what "
     "Iowans eat. It is sold to everyone else.", IC % "truck"),
    (BLUE, "And the point", "California imports nearly all its corn and Iowa imports "
     "nearly all its almonds. No one calls this a crisis.", IC % "shipping-container"),
])
D.kicker(s, "Riverside runs an enormous trade deficit with Iowa, and you have never once "
            "worried about it.", y=4.52)
D.notes(s, """The rhetorical centre of Part 3, and the kicker is the line to deliver
properly — pause before it and pause after it.

The observation is simple. States specialise ferociously. California grows almonds and
wine grapes; Iowa grows corn and soybeans. Each buys from the other the things it does not
make. That is trade, at enormous volume, entirely uncontroversial.

Nobody in Riverside worries about our trade deficit with Iowa. Nobody proposes a tariff on
Iowa corn to protect Californian corn growers. Nobody describes Iowa as taking advantage
of us.

Then the question that opens Part 4: what changes when the line on the map is a national
border instead of a state border? Economically, nothing at all — the arithmetic is
identical. Politically and legally, a great deal, because a national border can be taxed
and a state border cannot.

Be careful not to overplay it. There ARE real differences: within the United States,
workers can move freely, there is a common set of labour and environmental rules, and
there are federal transfers that partially compensate places that lose out. Those
differences are genuinely relevant, and Part 5 comes back to them. Say that here so the
argument does not sound like a debating trick.

One factual note: the specialisation claims on this slide are well known and safe to say
qualitatively. There are no production figures on the slide face on purpose — do not add
any from memory.""")

# ============================================ 36. the interstate experiment
s = S()
D.title(s, "The Experiment That Has Already Been Run")
y = D.defbox(s, 1.15,
             "The United States is the largest free-trade area ever created: fifty "
             "economies, no internal tariffs, for over two centuries.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "What the model predicts", "Deep specialisation by region, heavy trade "
     "between regions, and a much larger total output than fifty self-sufficient states."),
    (BLUE, "What we observe", "Exactly that. No state tries to make everything, and no "
     "state would be richer if it did."),
    (RED, "What it does not settle", "Whether every PLACE gained. Some regions "
     "specialised in things that later collapsed, and they have not recovered.",
     IC % "factory"),
])
D.kicker(s, "The gains are real and so are the losers. Both halves of that sentence are "
            "in the evidence.", y=4.52)
D.notes(s, """The honesty slide for Part 3.

The first two cards are the straightforward case, and it is strong: the US internal market
is about as clean a demonstration of gains from specialisation as economics has, and it
has been running for two hundred years.

The third card is the one that keeps the lecture honest, and do not skip it to save time.
Regional specialisation means regional exposure. When the thing your region specialised in
declines, the specialisation that made you rich makes you vulnerable. Parts of the
American manufacturing belt are the standing example, and students from those places know
it better than the model does.

Say the kicker slowly. It is the sentence that lets you argue for trade in Part 4 without
sounding like you are ignoring the room.

Deliberately no numbers on this slide. Regional employment and income series are easy to
quote badly and hard to quote well — if you want a figure here, look one up and put it in
these notes before you record rather than reaching for one live.""")

# ============================================ 37. checkpoint 3
s = S()
D.title(s, "Checkpoint: What Changed Between Parts 2 and 3")
y = D.band(s, 1.12, "Nothing changed except the size of the units. That is the point.",
           kind="answer", size=15)
D.cards2(s, y + 0.28, LIMIT - (y + 0.28), [
    (BLUE, "What stayed exactly the same",
     "Opportunity cost decides who does what. Specialisation raises total output. Trade "
     "at a rate between the two costs makes both sides better off. Every word of Part 2 "
     "survives at state scale."),
    (DGOLD, "The one genuinely new idea",
     "The economy-wide curve bows outward, because an economy contains many different "
     "opportunity costs and uses the cheapest first. Maya's straight line was a "
     "one-person special case."),
])
D.kicker(s, "Next we change the units one more time — and this time somebody can put a "
            "tax on the boundary.", y=4.52)
D.notes(s, """Checkpoint, thirty seconds, and it does real work: students think each part
of a chapter is new material, and here it genuinely is not.

The only new idea in Part 3 is the bowed curve, and the only reason it bows is the
diversity of producers inside an economy.

The kicker sets up Part 4 in one clause. Everything that follows about tariffs and quotas
exists because a national border is a place where a government can stand and collect
money. The economics of trade does not change at the border; the LAW does.""")

# ============================================================ 38. DIVIDER 4
s = S()
D.divider(s, "PART 4", "Now Draw the Border")
D.notes(prs.slides[-1], """Part 4 divider. Section 8.4 of the book, "Trade Between
Countries".

Structural note for delivery: Part 4 changes the tool. Parts 1 to 3 used production
possibilities curves; Part 4 uses the supply and demand diagram from Chapter 4 and the
surplus areas from Chapter 7. Tell students that explicitly, because a student who is
still thinking in PPCs will be lost within two slides.

This is the longest part of the deck and it is where the exam questions cluster.""")

# ============================================ 39. the world price
s = S()
D.title(s, "One New Number: The World Price")
y = D.defbox(s, 1.15,
             "The WORLD PRICE is the price a good sells for on the international market.\n"
             "A country that opens its border can buy or sell all it likes at that price.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "Compare it with your own", "Work out what the price would be with no trade. "
     "Then look at the world price. Only the comparison matters."),
    (GREEN, "World price lower", "Foreigners make it more cheaply than you do. You "
     "import, and your domestic price falls to theirs.", IC % "shipping-container"),
    (RED, "World price higher", "You make it more cheaply than the rest of the world. "
     "You export, and your domestic price rises to theirs.", IC % "truck"),
])
D.kicker(s, "The world price is comparative advantage arriving as a number you can look "
            "up.", y=4.52)
D.notes(s, """The bridge from Parts 1 to 3 into the diagrams, and the sentence on the
kicker is the bridge itself — say it deliberately.

In Part 2, comparative advantage was something you worked out by comparing opportunity
costs. In a real economy nobody does that calculation. The world price does it for you:
if the world can supply a good more cheaply than you can, the world price is below your
domestic price, and that IS the statement that they have the comparative advantage.

We are assuming the country is small enough that it can trade as much as it likes without
moving the world price. Say that assumption out loud — it is what makes the world price a
horizontal line on every diagram that follows, and it is doing real work. For sugar and
for the United States it is not literally true, and a sharp student may say so. The answer
is that relaxing it changes the size of the effects, not their direction.

Also worth one sentence: the choice to import or export is not a policy decision on this
slide. It falls out of the comparison. Policy enters when we start taxing the flow.""")

# ============================================ 40. autarky
figpage("Start With the Border Closed",
        "The US market for raw sugar, with no imports and no exports allowed.",
        "market_autarky",
        "Sixty cents a pound, forty million pounds a week — and every pound of it grown "
        "here.",
        "Illustrative schedules, scaled to the real price range. The statutory numbers "
        "are on a later slide.")
D.notes(prs.slides[-1], """The baseline diagram. Everything in Part 4 is measured against
this picture, so make sure it is solid before moving.

This is Chapter 4's diagram with Chapter 7's shading. Demand slopes down in blue, supply
slopes up in red, and they cross at sixty cents and forty million pounds a week. With the
border closed, that is the price and that is the quantity.

Consumer surplus is the blue triangle above the price and below demand: 800. Producer
surplus is the red triangle below the price and above supply: 800. Total 1,600. Those
units are arbitrary — what matters is how they change.

Say clearly what these schedules are: illustrative straight lines, not measured ones. I
have scaled them so the closed-border price lands in the real range for US sugar, which
makes the story concrete, but the numbers on the axes are a model, and the credit line
says so. The genuinely real numbers arrive four slides from now, and they are worth
waiting for.

Remind them what surplus means, briefly — Chapter 7 did the work: consumer surplus is
what buyers got above what they were willing to pay; producer surplus is what sellers got
above what they would have accepted.""")

# ============================================ 41. imports
figpage("Open the Border: the World Price Is Lower",
        "The world will sell sugar at 40¢. Nobody in America will now pay 60¢ for it.",
        "market_import",
        "The price falls to 40¢, American growers supply 20 instead of 40, and 40 "
        "million pounds arrive from abroad.",
        "Illustrative schedules. Surplus figures are in the same arbitrary units "
        "throughout Part 4.")
D.notes(prs.slides[-1], """The importing case. Walk the mechanics before the welfare.

At sixty cents, American buyers can now get sugar abroad for forty. So nobody pays sixty,
and the domestic price falls to forty — the world price.

At forty cents, look at each curve separately, because this is where students go wrong.
Read across to the RED supply curve: American growers are willing to supply only 20
million pounds at that price, down from 40. Read across to the BLUE demand curve:
Americans want to buy 60 million pounds, up from 40.

The gap between them — 60 wanted, 20 grown here — is imports. Forty million pounds.

Now the welfare, and the green area is the whole of it. Consumers gain 1,000. Producers
lose 600. The country nets a gain of 400.

Two things to say plainly.

First, that 400 is the gains from trade from Part 2, in a different diagram. Same result,
new tool.

Second, and this is the honest part: the 600 that producers lose is not a rounding error
and it does not go to Americans. Sugar growers are genuinely worse off, and they know
exactly who they are, which is why they lobby. Consumers gain more in total but each one
gains a little, spread across everybody, and most of them have no idea. Concentrated
losses and diffuse gains is the political economy of trade in six words, and it explains
almost everything in Part 5.""")

# ============================================ 42. importing winners/losers
s = S()
D.title(s, "Importing: Who Wins, Who Loses")
y = D.band(s, 1.12,
           "Consumers  +1,000        Producers  −600        Country  +400",
           kind="answer", size=16)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "Buyers win", "A lower price and more of it. Every household that eats "
     "anything with sugar in it gains a small amount.", IC % "shopping-cart"),
    (RED, "Domestic producers lose", "A lower price and less of it. Some farms that were "
     "viable at 60¢ are not viable at 40¢.", IC % "wheat"),
    (BLUE, "The country gains on net", "The winners' gain exceeds the losers' loss by "
     "400. That is a statement about the TOTAL and nothing else."),
])
D.kicker(s, "Winners could in principle compensate losers and still come out ahead. "
            "Whether they do is a different question.", y=4.52)
D.notes(s, """The ledger for the importing case. Keep it tight — the diagram did the work.

The kicker is the compensation principle and it is worth naming as such, because the book
raises it at the end of the chapter and it is the intellectual bridge to Part 5.

The logic: if the gain is 1,000 and the loss is 600, then in principle the winners could
hand 600 to the losers, everyone would be at least as well off as before, and 400 would
be left over. That is what "the country gains" means.

Then the hard question, and put it to them directly rather than answering it: does that
compensation actually happen? Mostly it does not, or not fully. The gains show up as
slightly cheaper groceries for a hundred million households. The losses show up as
specific farms and specific towns. Nobody writes the cheque.

An economist saying "the country gains" is making a precise and limited claim about a
total. It is not a claim that everyone gains, and students should not hear it as one. Say
that sentence — it is the difference between teaching this well and teaching it as
propaganda.""")

# ============================================ 43. exports
figpage("Same Country, Higher World Price",
        "Now the world will PAY 80¢. No American grower sells at home for 60¢.",
        "market_export",
        "The price rises to 80¢, growers produce 60, Americans buy 20, and 40 million "
        "pounds go abroad.")
D.notes(prs.slides[-1], """The exporting case, and it is the mirror image. Go faster than
you did on the import slide — the students have the machinery now.

If the world will pay eighty cents, no American grower sells at home for sixty. The
domestic price rises to the world price.

At eighty: growers supply 60, Americans buy only 20. The excess of 40 is exported.

The welfare is the import case with the roles swapped. Producers gain 1,000, consumers
lose 600, the country gains 400.

The symmetry is worth pointing at explicitly, because it prevents a real misconception:
trade is not good for consumers and bad for producers. It is good for whichever side was
being constrained by the closed border. Exporting hurts domestic consumers — American
sugar buyers are worse off in this scenario, and they are exactly the people who gained
in the previous one.

Note also that the net gain is 400 in both directions. That is not a coincidence of my
numbers — the schedules and the price gap are symmetric here on purpose, and if a student
notices, that is a good student.

The general result to state: trade makes a country better off in total whichever
direction it flows, and in both directions it creates a domestic group that loses.""")

# ============================================ 44. exporting winners/losers
s = S()
D.title(s, "Exporting: Who Wins, Who Loses")
y = D.band(s, 1.12,
           "Producers  +1,000        Consumers  −600        Country  +400",
           kind="answer", size=16)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "Domestic producers win", "A higher price and a bigger market. This is what "
     "an export industry lobbying for market access is asking for.", IC % "factory"),
    (RED, "Domestic consumers lose", "They now compete with the whole world for the same "
     "good, and they pay the world's price for it.", IC % "shopping-cart"),
    (BLUE, "The country gains on net", "Same arithmetic, opposite direction. And the "
     "same unanswered question about who compensates whom."),
])
D.kicker(s, "Trade always creates domestic losers. Which group loses depends only on "
            "which way the goods move.", y=4.52)
D.notes(s, """The mirror ledger. Sixty seconds.

The kicker is the generalisation and it is the one worth carrying into Part 5: there is no
version of opening a border in which everybody at home gains. Somebody was benefiting from
the closed border, and opening it takes that benefit away.

A useful real-world hook, delivered carefully because it is a general observation rather
than a sourced claim: when a food exporting country has a bad harvest and world prices
spike, its own citizens face higher food prices and governments sometimes restrict exports
to protect them. That is precisely this diagram, and it shows the export case is not
hypothetical.

Do not attach a specific country, year or number to that unless you have looked it up.""")

# ============================================ 45. the rule
s = S()
D.title(s, "The Rule That Decides Everything in Part 4")
y = D.band(s, 1.12,
           "world price  <  your no-trade price   →   you IMPORT\n"
           "world price  >  your no-trade price   →   you EXPORT",
           kind="formula", size=16)
D.cards2(s, y + 0.28, LIMIT - (y + 0.28), [
    (BLUE, "It is comparative advantage, restated",
     "A world price below yours means the rest of the world gives up less to make this "
     "than you do. That is the definition from Part 2, arriving as a market price instead "
     "of a table of opportunity costs."),
    (GREEN, "And it is how exam questions are set",
     "You will be given supply and demand schedules and a world price. Find the no-trade "
     "equilibrium first, compare, then read the two quantities off the two curves at the "
     "world price. The gap is the trade."),
])
D.kicker(s, "Find the closed-border price first. Every question in this part starts "
            "there.", y=4.52)
D.notes(s, """The examinable procedure, and it is worth dictating as a procedure.

Step one, and students skip it: find the equilibrium price with no trade. Set quantity
demanded equal to quantity supplied and solve. Everything is a comparison against that
number and you cannot make the comparison without it.

Step two: compare the world price with it. Below means import, above means export.

Step three: at the world price, read quantity supplied off the supply curve and quantity
demanded off the demand curve, SEPARATELY. Do not set them equal — they are not equal, and
their difference is the whole point.

Step four: the gap is imports or exports.

The most common error by a distance is setting supply equal to demand at the world price.
Say so explicitly. Once the border is open the domestic market does not clear on its own —
it clears with the help of the rest of the world, and that help is the gap.

The first card is worth thirty seconds even though it is not examinable, because it is the
sentence that stitches the two halves of the chapter together.""")

# ============================================ 46. fair trade box
s = S()
D.title(s, "Letting the Data Speak: Fair Trade Products")
y = D.defbox(s, 1.15,
             "A fair trade label promises that the grower was paid above the market "
             "price. Consumers pay more, deliberately.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "What it is trying to do", "Move some of the gains from trade towards the "
     "producer, using the buyer's willingness to pay rather than a law.",
     IC % "coffee-cup"),
    (DGOLD, "Why an economist looks twice", "A price floor above the market price is a "
     "familiar object from Chapter 7. It attracts more supply than it can absorb."),
    (GREEN, "And why it is a data question", "Whether growers are actually better off is "
     "measurable, and the answer depends on how much of the premium reaches them.",
     IC % "research"),
])
D.kicker(s, "A good intention and a good outcome are different claims, and only one of "
            "them can be tested.", y=4.52)
D.notes(s, """This corresponds to the book's Letting the Data Speak box in section 8.4.

PLEASE READ BEFORE DELIVERY: as with the experiment box in Part 2, I could not obtain the
text, so this slide poses the question the box asks rather than reporting its finding.
Open the book to section 8.4 and check what it concludes before you record. Do not state a
result from this slide as it stands.

Delivered as posed, it still works, and the middle card is the genuinely economic content:
a guaranteed above-market price is a price floor, and students met price floors in Chapter
7. The predictable consequences are excess supply and a rationing problem — who gets to
sell at the premium price?

Handle the topic with care. Students have strong and mostly good instincts about fair
trade, and the aim is not to debunk it. The aim is the kicker: intending to help and
succeeding in helping are different claims, and the second one is empirical. That is a
transferable habit of mind and it is worth more than any conclusion about coffee.

Keep it to a minute unless the room engages, in which case it is a good discussion.""")

# ============================================ 47. a tariff
figpage("A Tariff",
        "A TARIFF is a tax on an imported good. Here: 10¢ a pound.",
        "market_tariff",
        "The domestic price rises to 50¢, imports halve, and two triangles of value "
        "disappear entirely.",
        "Illustrative schedules. Real statutory tariff and quota figures follow.")
D.notes(prs.slides[-1], """The central diagram of Part 4. This is the one that appears on
the exam, and it is the one the book's own end-of-chapter question asks about by name.

Mechanics first. A ten cent tariff means an importer paying forty cents abroad must hand
ten cents to the government at the border. They will not sell for less than fifty. So the
domestic price rises from forty to fifty.

At fifty cents, four things move, and go through them one at a time:

Domestic supply rises from 20 to 30 — the higher price makes more American farms viable.
Domestic demand falls from 60 to 50 — some buyers drop out. Imports therefore fall from 40
to 20, halved. And the government collects ten cents on each of the 20 million pounds
still imported: revenue of 200, the gold rectangle.

Now the two red triangles, and they are the point of the slide.

Triangle A, on the left, is the PRODUCTION distortion. Those extra 10 million pounds are
now grown in America at a cost above forty cents, when the world would have sold them for
forty. Real resources are being burned to make something we could have bought more
cheaply.

Triangle B, on the right, is the CONSUMPTION distortion. Those 10 million pounds are no
longer bought at all, by people who valued them at more than the world price. That value
simply does not happen.

Together A and B are 100, and nobody receives them. Not consumers, not producers, not the
government. That is deadweight loss, exactly as in Chapter 7.

The book asks students to explain areas A and B in its end-of-chapter questions, which is
why they are lettered that way here.""")

# ============================================ 48. areas A and B
s = S()
D.title(s, "The Two Triangles, in Words")
y = D.band(s, 1.12, "A tariff destroys value in two separate ways, and they are worth "
                    "naming separately.", kind="neutral", size=14)
D.cards2(s, y + 0.28, LIMIT - (y + 0.28), [
    (RED, "A — the production distortion",
     "American farms grow 10 million more pounds. Every one of them costs MORE to grow "
     "here than the 40¢ it would have cost to buy. The difference is real resources "
     "burned — land, water, labour spent making something we could have had for less."),
    (RED, "B — the consumption distortion",
     "Americans buy 10 million fewer pounds. Every one of them was worth MORE than 40¢ to "
     "the person who wanted it. That value is not transferred anywhere; it simply never "
     "happens."),
])
D.kicker(s, "The transfer is arguable. The two triangles are not — they are value that "
            "stops existing.", y=4.52)
D.notes(s, """The interpretation slide. This is where a student moves from being able to
draw the diagram to being able to explain it, and the book asks for the explanation
directly.

Make the distinction sharp, because students blur the transfer and the loss.

The money consumers hand to producers is a TRANSFER. Americans pay it, other Americans
receive it. You might think that is fine or you might think it is unfair, but it is a
distributional question and economics does not settle it.

The two triangles are different in kind. Nobody gets that value. It is not moved from one
American to another — it stops existing.

Triangle A: growing sugar in America at fifty cents when the world sells it at forty
wastes ten cents of real resources on every pound. Those are acres and hours that could
have made something else.

Triangle B: someone who would happily have paid forty-five cents for a pound of sugar now
does not buy it. The value they would have got is gone, and no one else has it.

The kicker is the sentence to end on and it is the honest framing of the whole tariff
debate: you can argue about who should get the transfer. The triangles are pure loss and
there is no argument to have about them.""")

# ============================================ 49. the ledger
figpage("Who Pays for a Tariff",
        "Add up every group. The four numbers must, and do, account for each other.",
        "tariff_ledger",
        "Consumers lose 550. Producers and government together gain 450. The missing "
        "100 is gone.")
D.notes(prs.slides[-1], """The tariff ledger. Read the four bars in order, and let the
arithmetic do the persuading.

Consumers lose 550 — they pay ten cents more on every pound they still buy, and some stop
buying.

Producers gain 250 — a higher price on a larger domestic output.

The government collects 200 — ten cents on twenty million imported pounds.

Add the gains: 250 plus 200 is 450. The loss was 550. The difference, 100, is the
deadweight loss. It is exactly the two triangles from the previous slide.

The sentence worth repeating: a tariff is mostly a transfer from consumers to producers
and the government, plus a genuine loss. If you want to defend a tariff, you have to
either defend the transfer or argue that something outside this diagram makes the loss
worth paying. Part 5 is about arguments of the second kind.

An observation students find striking: the government's revenue is NOT the main effect. It
is 200 out of 550 taken from consumers. Most of what consumers lose goes to domestic
producers, not to the Treasury. So a tariff is a much better tool for helping a specific
industry than it is for raising money — which is exactly what its political history looks
like.""")

# ============================================ 50. quotas
s = S()
D.title(s, "A Quota Does the Same Job, Differently")
y = D.defbox(s, 1.15,
             "A QUOTA is a limit on how much of a good may be imported. Instead of "
             "taxing the flow, it caps it.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "Same direction of effect", "Fewer imports, a higher domestic price, domestic "
     "producers protected, consumers paying more. The diagram looks familiar."),
    (RED, "One important difference", "There is no tariff revenue. The gap between the "
     "world price and the domestic price is collected by whoever holds the right to "
     "import.", IC % "price-tag"),
    (DGOLD, "Which is why they are fought over", "That gap is called a quota rent, and "
     "governments decide who gets it. In the US the answer is published, by country.",
     IC % "ledger"),
])
D.kicker(s, "A tariff sends the money to the Treasury. A quota sends it to whoever holds "
            "the licence.", y=4.52)
D.notes(s, """Quotas. The book lists them among the methods of protectionism, and the
comparison with tariffs is a standard exam question.

Lead with the similarity: a quota that cuts imports to twenty million pounds produces the
same domestic price as a tariff that cuts them to twenty million pounds. Price up, imports
down, domestic producers gain, consumers lose, and the same two deadweight loss triangles
appear. Students should see that the direction of every effect is identical.

Then the difference, which is where the marks are. Under a tariff, the wedge between the
world price and the domestic price is collected by the government at the border. Under a
quota, that wedge still exists — someone buys at forty and sells at fifty — but it goes to
whoever has permission to import. That is a QUOTA RENT.

Say why that is politically consequential rather than a technicality: quota rents are
worth a great deal to specific, identifiable firms and countries, and governments allocate
them. That creates a permanent constituency for keeping the quota, which is one reason
quotas outlive their justifications.

The next slide shows a real one where the allocation is published country by country in
the Federal Register, which makes the abstraction concrete in a way students remember.""")

# ============================================ 51. the real quota
figpage("The Real Thing: American Sugar",
        "Not an illustration. These are the rates in the US tariff schedule.",
        "quota",
        "Two rates, one line in the schedule: 0.66¢ a pound up to 1,117,195 tonnes, "
        "15.36¢ a pound after it.",
        "Rates: US Harmonized Tariff Schedule, heading 1701.14 (1.4606¢/kg in-quota, "
        "33.87¢/kg over-quota). Quota quantity: Federal Register, 24 July 2026, FY2027 "
        "tariff-rate quota allocations, effective 1 October 2026.")
D.notes(prs.slides[-1], """The live example, and the best slide in Part 4. Every number on
it comes out of a legal document, not out of me.

The structure is called a tariff-rate quota and it is the most common form of protection in
US agriculture. Read it off the picture:

Up to 1,117,195 metric tons of raw cane sugar a year, the tariff is 1.4606 cents per
kilogram — about two-thirds of a cent a pound. Essentially free trade.

Past that line, the rate jumps to 33.87 cents per kilogram — 15.36 cents a pound. That is
roughly a twenty-three-fold increase, and it is high enough that in practice very little
sugar comes in over the quota.

Say the exact figures once, from these notes rather than from memory: 0.66 cents a pound
in-quota, 15.36 cents a pound over-quota, quota of 1,117,195 tonnes.

Two things that make this worth the time.

First, the quota is not one number handed to the world. It is divided among 39 named
countries in the Federal Register — the Dominican Republic, the Philippines and Brazil hold
the largest shares. Those allocations are the quota rents from the previous slide, made
concrete and published with names attached.

Second, for scale: that quota is roughly a tenth of all the sugar Americans consume. One
line in one schedule, set for a year at a time.

RE-CHECK BEFORE DELIVERY: this is live material. The rates are stable, but confirm the
FY2027 allocation has not been amended before you record.""")

# ============================================ 52. the price gap
figpage("What That Costs at the Checkout",
        "World raw sugar and American raw sugar, same months, same units.",
        "sugar_prices",
        "Americans paid about two and a half times the world price for raw sugar "
        "through the first half of 2026.",
        "ICE No. 11 (world) and No. 16 (US) raw sugar, monthly averages, IMF via FRED "
        "series PSUGAISAUSDM and PSUGAUSAUSDM, both updated 13 July 2026.")
D.notes(prs.slides[-1], """The consequence, in real prices. This is the payoff for the two
previous slides.

The two contracts are the standard world and US raw sugar benchmarks, and the US
Department of Agriculture uses these same two series as its own official benchmarks — so
this is not a comparison I have assembled, it is the one the government uses.

June 2026: the world price was 13.91 cents a pound. The American price was 35.50. A gap of
21.59 cents, and the American price is about two and a half times the world price. The
earlier months on the chart show it is not a one-month fluke.

Now be careful, and this is important, because there is a trap here that a sharp student
could walk into and so could you.

The observed gap of 21.59 cents is LARGER than the over-quota tariff of 15.36 cents. Under
a simple tariff model that should not be possible — if the domestic price exceeded the
world price plus the duty, someone would import over the quota and pocket the difference.

Two things are going on and you should say both. First, the quota rather than the tariff is
the binding constraint: over-quota imports are close to zero, so the wedge is quota rent,
not tariff. Second, the two contracts are not perfectly comparable — the US contract is
delivered duty-paid on a US basis and the world contract is free-on-board, so freight,
insurance and delivery terms account for part of the residual.

So the defensible sentence, and use this wording: American sugar costs about two and a half
times world sugar, and a 15.36 cent over-quota tariff plus a 1.1 million tonne quota is
why. Do NOT claim the full 21.59 cents is policy-created rent. You cannot defend that
precisely and you do not need to.""")

# ============================================ 53. where tariffs are
figpage("Where American Tariffs Actually Are",
        "Duties actually collected, as a share of the value of everything imported.",
        "tariff_rate",
        "From about 2% to about 7% in two years. The last time it was this high, most "
        "of your parents were not born.",
        "2024 and 2025: US Census trade data via USAFacts, page updated 16 April 2026. "
        "June 2026: Penn Wharton Budget Model, published 10 August 2026. Statutory "
        "average: Yale Budget Lab, 11 August 2026.")
D.notes(prs.slides[-1], """The macro context, and it is the slide most likely to attract a
question, so read these notes properly before delivering it.

The three bars are the same measurement: duties actually collected, divided by the value of
imports. 2.3% in 2024. 7.7% in 2025. 7.1% in June 2026. Roughly a tripling.

Say who produced each figure, out loud: the 2024 and 2025 numbers come from Census trade
data compiled by USAFacts; the June 2026 figure is from the Penn Wharton Budget Model.
Both are non-partisan. That matters here more than usual.

The gold dashed line is a DIFFERENT measurement and the slide says so. The Yale Budget Lab
puts the average STATUTORY rate — what the tariff schedule says — at 11.0%. The gap between
11.0% and 7.1% is not a disagreement between two teams. It is exemptions, carve-outs, and
buyers switching away from the most heavily tariffed suppliers. Never quote 2.3% against
11.0%; those are different definitions and the comparison would badly overstate the change.

Two questions you should be ready for.

Why did the rate FALL between 2025 and 2026? Because the Supreme Court struck down the
tariffs imposed under emergency economic powers in February 2026, and the replacement
programme is narrower. That is a genuinely good question and the answer is a real event.

Is it really the highest in generations? On the collected measure, this is the highest
since the late 1960s. On the statutory measure, the highest since the early 1940s. Say
"the highest in at least two generations" rather than picking, because the two measures
give different answers and both are defensible.

RE-CHECK BEFORE DELIVERY. This number moves. Confirm the Penn Wharton and Yale figures
before you record.""")

# ============================================ 54. this week
s = S()
D.title(s, "This Week: A 1930 Statute, Used for the First Time")
y = D.band(s, 1.12,
           "A 50% tariff on about $20 billion of Canadian goods is scheduled to take "
           "effect on Wednesday, 19 August 2026.", kind="note", size=15)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "The legal authority", "Section 338 of the Tariff Act of 1930. Ninety-six "
     "years on the books and, until now, never used by any president.", IC % "ledger"),
    (DGOLD, "What it covers", "Vehicles and manufactured goods, alcohol, wood, paper, "
     "hockey equipment and dairy. Steel and aluminium are already covered elsewhere.",
     IC % "truck"),
    (GREEN, "Why it is on this slide", "Whether or not it lands, it shows what a tariff "
     "is for: a lever, aimed at a negotiation, with the diagram's costs attached."),
])
D.kicker(s, "Run it through today's diagram: American buyers pay, Canadian sellers sell "
            "less, and two triangles disappear.", y=4.52)
D.notes(s, """The live slide, and the most perishable thing in the deck.

RE-CHECK ON THE MORNING YOU RECORD. As of 17 August 2026 the tariffs were still scheduled
for the 19th, negotiations were continuing, no delay had been announced, and Canada had
announced no retaliation. Any of those could change within hours. The slide is worded to
survive either outcome — "scheduled to take effect" is true whether or not it does — but
check before you speak.

Why it is worth a slide at all: it is the diagram from six slides ago, happening this week,
with a rate high enough that students will notice. Fifty per cent is not a subtle number.

The interesting part for a first-year class is the third card. If a deal is struck before
Wednesday and the tariff never lands, that is not a failure of the example — it is the
example. The threat of the tariff was the instrument. That is a genuine and slightly
uncomfortable extension of the model: the diagram prices the cost of a tariff being
imposed, and says nothing about the value of being able to credibly threaten one.

The Section 338 detail is worth thirty seconds because it is genuinely remarkable. A
statute sat unused on the books for ninety-six years and was reached for in 2026. Tariff
authority in the United States belongs to Congress and has been delegated to the president
in pieces across a century of separate statutes — which is why the same policy can be
rebuilt under a new legal authority when a court strikes down the old one, as happened
twice this year.

If you are short of time, this is the slide to cut. It is the most fun and the least
examinable.""")

# ============================================ 55. who pays
figpage("So Who Actually Pays a Tariff?",
        "The diagram says domestic buyers. The evidence agrees, by a wide margin.",
        "who_pays",
        "About 90% of the tariff showed up in US prices. Foreign sellers absorbed almost "
        "none of it.",
        "Pass-through: Fajgelbaum & Khandelwal, Brookings Papers on Economic Activity, "
        "March 2026 (2025 tariffs through December 2025; range 80–100%). Household cost: "
        "Yale Budget Lab and Tax Foundation, both 11 August 2026.")
D.notes(prs.slides[-1], """The empirical check on the diagram, and it is the strongest
evidence slide in the deck.

The left panel answers a question students genuinely have, because they have heard the
opposite claim: when a tariff is imposed, does the foreign seller cut their price to keep
the sale, or does the American buyer pay more? The diagram assumes the American pays.
Fajgelbaum and Khandelwal, in the Brookings Papers on Economic Activity in March 2026,
estimate that roughly ninety per cent of the tariff showed up in tariff-inclusive US
prices. Foreign sellers absorbed almost none of it.

Say who they are and where it was published — this is a peer-reviewed conference paper by
academic economists, not an advocacy estimate, and that is worth stating given how
politically loaded the topic is. The range they report is eighty to a hundred per cent; use
"about ninety" and say it is a range.

The right panel is the household cost, and the honest handling is the point. The Yale
Budget Lab says about 1,100 dollars a household a year. The Tax Foundation says about 900.
Same week, twenty-two per cent apart, and the difference is modelling assumptions about
retaliation and substitution.

Give students the range, not a point estimate. "Roughly nine hundred to eleven hundred
dollars a household" is honest and still lands hard. Quoting one number to the dollar
would be false precision.

One flag worth raising, and it is worth thirty seconds because it teaches something real:
the Tax Foundation is a free-market advocacy organisation. Its methodology is transparent
and widely cited, but it is not a neutral body — and note which direction its estimate
runs, which is the LOWER one. Yale Budget Lab and Penn Wharton are non-partisan academic
units. Naming the interest of a source out loud, even when you use the source, is the habit
this course is trying to build.

RE-CHECK the household figures before delivery.""")

# ============================================ 56. tariffs between firms
s = S()
D.title(s, "Tariffs Land on Firms, Not Just Countries")
y = D.defbox(s, 1.15,
             "Most of what crosses a border is not a finished product. It is a part, on "
             "its way to becoming something else.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "What actually gets traded", "Components, materials and half-built things, "
     "often crossing the same border several times before anyone buys the result.",
     IC % "factory"),
    (RED, "So a tariff hits your own producers", "A tariff on imported steel is a cost "
     "increase for every American firm that builds things out of steel.",
     IC % "hard-hat"),
    (DGOLD, "Which complicates the politics", "Protecting one domestic industry means "
     "taxing the domestic industries downstream of it. Both sides are American."),
])
D.kicker(s, "“Protecting American producers” is ambiguous the moment you ask "
            "WHICH American producers.", y=4.52)
D.notes(s, """This corresponds to the book's Choice and Consequence box in section 8.5,
"Tariffs Affect Trade Between Firms". The framing here is mine — I could not obtain the
box's text — but the economics is standard and safe to teach, so unlike the two earlier
boxes this slide does not need checking before delivery. Check it anyway if you have the
book open.

The content students miss: a large share of international trade is intermediate goods.
Firms buying inputs from firms. A car part may cross a border several times before the car
is finished.

The consequence is the second card, and it is worth stating carefully because it genuinely
changes how the debate reads: a tariff on imported steel raises the price of steel inside
the country that imposed it. American steel producers gain. American car makers,
appliance makers, construction firms and machine shops all face higher costs. Everyone in
that sentence is American.

So the phrase "protecting American producers" contains a hidden choice about WHICH American
producers, and typically the protected industry is smaller and more concentrated than the
industries paying for the protection. That asymmetry — concentrated benefits, diffuse
costs — is the same one from the import slide, and it is the best single explanation of why
protection is politically durable even when the arithmetic is against it.

Connect it back to the current steel and aluminium tariffs if you want a live hook, but do
not put a rate on the slide face without checking it first.""")

# ============================================ 57. checkpoint 4
s = S()
D.title(s, "Checkpoint: The Diagrams You Must Be Able to Draw")
y = D.band(s, 1.12, "Four pictures, and every exam question in Part 4 is one of them.",
           kind="neutral", size=14)
D.cards4(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "1. No trade", "Supply meets demand. Find this price FIRST — everything is "
     "measured against it."),
    (BLUE, "2. Importing", "World price below. Read Qs and Qd separately; the gap is "
     "imports."),
    (BLUE, "3. Exporting", "World price above. Same reading, opposite gap."),
    (BLUE, "4. A tariff", "Price up by the tariff. Revenue rectangle, two deadweight "
     "triangles, A and B."),
])
D.kicker(s, "Practise drawing number four from a blank page. That is how it will be "
            "asked.", y=4.52)
D.notes(s, """Checkpoint for Part 4. This is the second slide to tell them to photograph.

The instruction on the kicker is specific and worth giving: the tariff diagram is examined
by asking students to produce it, label it and explain the two triangles. Recognising it is
not enough.

Repeat the procedural warning once more, because it is the single most common error in this
part of the course: at the world price, quantity supplied and quantity demanded are NOT
equal. Read them off the two curves separately. Their difference is the trade.""")

# ============================================================ 58. DIVIDER 5
s = S()
D.divider(s, "PART 5", "The Case on\nthe Other Side")
D.notes(prs.slides[-1], """Part 5 divider. Section 8.5 of the book, "Arguments Against Free
Trade".

Set the tone before the first slide of this part. Everything so far has pointed one way,
and a student who has been paying attention should be slightly suspicious of how tidy it
has been. Part 5 exists because the tidiness is real but incomplete.

Deliver this part straight. Do not set up the arguments in order to knock them down. Some
of them are weak, one of them is strong, and students should be able to tell which is
which by the end — from the reasoning, not from your tone of voice.""")

# ============================================ 59. five arguments
s = S()
D.title(s, "Five Arguments Against Free Trade")
y = D.band(s, 1.12, "These are the objections the textbook takes seriously enough to "
                    "list. They are not equally strong.", kind="neutral", size=14)
D.strip5(s, y + 0.32, [
    ("1. National\nsecurity", IC % "hard-hat"),
    ("2. Infant\nindustry", IC % "lightbulb"),
    ("3. Environmental\nstandards", IC % "wheat"),
    ("4. Cultural\nidentity", IC % "ballot-box"),
    ("5. Jobs and\nwages", IC % "factory"),
], h=1.30)
D.rect(s, 0.60, 3.20, 8.80, 0.06, fill=RULE)
D.band(s, 3.42, "Number 5 has the best evidence behind it, and it is the book's own "
                "chapter question.\nNumber 1 is the hardest to falsify — which is "
                "exactly why it gets attached to so much.", kind="note", size=13.5)
D.kicker(s, "Every one of them accepts the diagram and argues that something outside it "
            "matters more.", y=4.62)
D.notes(s, """The map of Part 5, and the kicker is the analytical key to the whole part —
say it deliberately and then repeat it at the end.

None of these five arguments claims the tariff diagram is wrong. Not one. They all concede
that a tariff costs consumers more than it gains producers and burns two triangles of value
along the way. What they claim is that the diagram leaves something out that is worth more
than the loss.

That reframing is the most useful thing a student can take from this part, because it tells
them how to evaluate an argument they have not heard before. Every serious argument for
protection has the same shape: name the thing outside the diagram, and then show it is
worth more than the deadweight loss.

That also tells you how to test one. What is being claimed? Is it measurable? Is a tariff
the cheapest way to get it?

Give the honest ranking now so they know where you are going: one is real but narrow, two
is coherent but hard to execute, three and four are genuine values that a tariff is a poor
tool for, and five is the one with the strongest evidence behind it and the one the book's
own chapter question is about.""")

# ============================================ 60. national security
s = S()
D.title(s, "1. National Security")
y = D.defbox(s, 1.15,
             "Some goods you may not want to buy from a country that could stop selling "
             "them to you at the worst possible moment.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "The strong version", "Weapons, and the small number of inputs with no "
     "substitute and no stockpile. Dependence is a genuine strategic risk."),
    (RED, "The weak version", "Almost everything else. The argument is easy to make and "
     "almost impossible to falsify, so it gets attached to industries that merely want "
     "protection."),
    (BLUE, "The test to apply", "Would losing this supply actually be catastrophic, and "
     "is a tariff cheaper than a stockpile or a second supplier?", IC % "balance-scale"),
])
D.kicker(s, "A real argument with a real problem: nothing about it limits how far it can "
            "be stretched.", y=4.52)
D.notes(s, """Argument one. Sixty seconds.

Take the strong version seriously first, because it is correct. There genuinely are goods
where dependence on a potential adversary is a strategic risk, and no economist argues a
country should buy its munitions from whoever is cheapest this year.

Then the problem, which is not that the argument is wrong but that it has no natural
boundary. Because it is a claim about a hypothetical future, it is very hard to test, and
that makes it attractive to any industry looking for a reason. Historically the national
security justification has been attached to a remarkable range of products.

The third card is what to do about it, and it is the economist's contribution: even if the
security concern is real, a tariff is only one way to address it. Stockpiles, diversifying
suppliers, and subsidising a small strategic capacity are alternatives. The question is not
"is security valuable" — obviously it is — but "is a permanent tax on consumers the
cheapest way to buy it".

Do not name specific current cases unless you have checked them. This area moves quickly
and it is politically charged.""")

# ============================================ 61. infant industry
s = S()
D.title(s, "2. The Infant Industry")
y = D.defbox(s, 1.15,
             "A new domestic industry might be able to compete eventually — but not yet, "
             "and not while established foreign firms are already cheaper.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "Why it is coherent", "If costs fall with experience, temporary protection "
     "could buy a permanently competitive industry. That is a real economic mechanism.",
     IC % "lightbulb"),
    (RED, "Why it usually fails", "Temporary protection is not temporary. The industry "
     "grows a constituency for keeping it long before it grows a cost advantage."),
    (BLUE, "The test to apply", "Was a date set at the start, and did the protection "
     "actually end on it? That question answers most real cases.", IC % "clock"),
])
D.kicker(s, "The economics is sound. The politics is where it dies.", y=4.52)
D.notes(s, """Argument two, and it is the most intellectually respectable of the five,
which is why it deserves a careful treatment rather than a dismissal.

The mechanism is genuine. If a firm's costs fall as it accumulates experience, then a new
entrant might be uncompetitive today and competitive in ten years — and might never get
those ten years if it is undercut from day one. Temporary protection could in principle
bridge that gap and leave the country permanently better off.

Then the practical problem, and it is a political economy problem rather than an economic
one. Protection creates a group of people whose livelihoods depend on it, and that group
lobbies. The industry acquires a constituency for permanent protection long before it
acquires a cost advantage. So the temporary tariff becomes permanent, and the country pays
the deadweight loss forever in exchange for an industry that never became competitive.

The test on the third card is the practical one and students can apply it to any case they
read about: was there a date, and did it hold?

Be even-handed here. There are real historical cases where targeted protection is argued to
have worked, particularly in East Asia, and there is a serious literature on both sides. Do
not present the case as closed. If a student raises it, "there is real disagreement about
those cases and it turns on what else those governments were doing at the same time" is an
honest answer.""")

# ============================================ 62. environment and culture
s = S()
D.title(s, "3 and 4. Environmental Standards and Cultural Identity")
D.cards2(s, 1.15, 2.30, [
    (GREEN, "Environmental standards",
     "If a foreign producer is cheaper because it is allowed to pollute, the price gap is "
     "not a real cost advantage — it is a cost being paid by someone who is not in the "
     "transaction. That is Chapter 9's problem, arriving early."),
    (DGOLD, "Cultural identity",
     "Some countries protect domestic film, music, publishing or food traditions on the "
     "grounds that they are not ordinary goods. This is a claim about values, and it is "
     "outside what the diagram can price."),
])
D.band(s, 3.52, "In both cases the honest economist's answer is the same: the concern may "
                "be real, and a tariff is probably the wrong instrument.", kind="formula",
       size=14)
D.kicker(s, "Aim the policy at the problem. A tax on the pollution beats a tax on the "
            "trade.", y=4.52)
D.notes(s, """Arguments three and four, taken together because the response to them is the
same.

The environmental argument is the stronger of the two and it is worth flagging as a
forward reference: if production imposes costs on people outside the transaction, the
market price understates the true cost. That is an externality and it is the whole of
Chapter 9, which is the next lecture. So this argument is not a complaint about trade at
all — it is a complaint about unpriced pollution that happens to show up in a trade
context.

The cultural argument is different in kind. It is a claim that some goods carry value
beyond what people will pay for them, and that markets will under-supply them. That is a
values claim, not an efficiency claim, and economics has no special authority over it. Say
that plainly rather than dismissing it.

The response on the band is the general principle and it is worth naming: target the
instrument at the problem. If pollution is the problem, tax the pollution — including at
home, where you also have polluters. If domestic film matters, subsidise domestic film. A
tariff addresses these concerns clumsily, hits unrelated goods, and burns the two triangles
on the way.

That principle recurs throughout economics and is worth stating once at full strength: the
best policy acts as closely as possible to the source of the problem.""")

# ============================================ 63. jobs and wages
s = S()
D.title(s, "5. Jobs and Wages — the Serious One")
y = D.defbox(s, 1.15,
             "When imports arrive, specific factories close and specific towns lose their "
             "employer. This is not a theoretical worry. It happens, and it is measured.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (RED, "What is true", "The losses are concentrated, geographic and lasting. People "
     "do not smoothly move to the new jobs, because the new jobs are somewhere else and "
     "need different skills.", IC % "factory"),
    (BLUE, "What is also true", "Trade changes which jobs exist, not how many. Total "
     "employment is driven by other things — mostly by how many people want to work."),
    (GREEN, "Why both survive", "“The country gains” is a claim about a total. "
     "It was never a claim that each person gains, and it should not be heard as one."),
])
D.kicker(s, "Trade makes the pie bigger and hands out uneven slices. Denying either half "
            "is dishonest.", y=4.52)
D.notes(s, """The most important slide in Part 5. Give it the time.

Take the first card entirely seriously and say it without hedging. The adjustment costs of
trade are real, they are concentrated in particular places, and they last a long time. The
comfortable phrase "workers will move to more productive sectors" describes something that
happens slowly, incompletely, and often not to the same people. A student whose family
lived through a plant closing is not confused about economics — they are describing
something the simple model does not capture.

The second card is what the model actually says, and state its limits precisely. Trade
changes the COMPOSITION of employment, not the LEVEL. If trade destroyed jobs on net, two
centuries of expanding trade would have produced permanent mass unemployment, and it did
not. The level of employment is determined by labour supply, demography, and macroeconomic
policy.

The third card is the reconciliation and it is the intellectual heart of the chapter's
ending. When an economist says a country gains from trade, that is a statement about a
sum. It has never been a statement about every individual, and the diagram makes that
obvious — the producer surplus loss on the import slide was right there, in red, from the
beginning.

The kicker is the sentence to land the part on. Both halves. Trade makes the pie bigger,
and it hands out uneven slices. Anyone who tells you only one of those things is selling
you something.""")

# ============================================ 64. the EBE
s = S()
D.title(s, "So: Will Free Trade Cause You to Lose Your Job?")
y = D.band(s, 1.12, "The chapter's own question, and the honest answer has three parts.",
           kind="note", size=15)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (RED, "Possibly, if you are in the wrong industry", "Some specific jobs disappear "
     "because of imports. That risk is real and it is not evenly spread across people or "
     "places."),
    (GREEN, "But not on net, and not the economy's jobs", "Trade reshuffles employment "
     "between sectors. It does not determine how many jobs a country has."),
    (BLUE, "And your wage depends on something else", "What you earn depends mostly on "
     "what your work produces. Trade changes what is worth producing, which is a slower "
     "and less visible thing than a factory closing."),
])
D.kicker(s, "A truthful answer to this question is uncomfortable, and any answer that is "
            "comfortable is incomplete.", y=4.52)
D.notes(s, """The chapter's Evidence-Based Economics question, answered. This is the close
of Part 5 and the emotional close of the lecture.

Deliver the three cards as one answer rather than three separate points.

Yes, some people lose their jobs to import competition, and the risk is concentrated rather
than random.

No, trade does not reduce the total number of jobs, and the evidence over two centuries is
about as clear as evidence in economics gets.

And in the long run wages track productivity, which trade tends to raise — but that is a
slow, diffuse process that nobody can photograph, whereas a closing plant is on the news.
The asymmetry in visibility is a large part of why this debate is shaped the way it is, and
it is worth naming.

PLEASE NOTE BEFORE DELIVERY: I could not obtain the text of the book's own answer to this
question, so this slide gives the standard economic answer rather than reporting the book's
evidence. Read the Evidence-Based Economics section at the end of section 8.5 before
recording and add its specific evidence to these notes. Students will be examined on the
book's version.

Close with the kicker. The honest answer to this question is uncomfortable, and a
comfortable answer is a sign that something has been left out. That is a good note to end
the argument on.""")

# ============================================ 65. compensation
s = S()
D.title(s, "The Question the Model Leaves Open")
y = D.defbox(s, 1.15,
             "If the winners gain more than the losers lose, the winners COULD compensate "
             "the losers and still come out ahead. The model says nothing about whether "
             "they do.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "In principle", "Trade adjustment assistance, retraining, relocation support, "
     "regional investment. The gains are large enough to fund all of it.",
     IC % "coin-stack"),
    (RED, "In practice", "The compensation is usually small, slow, and hard to get. The "
     "gains stay where they land."),
    (DGOLD, "Which is a political choice", "Not an economic law. Economics can tell you "
     "the transfer is affordable. It cannot make anyone vote for it.", IC % "ballot-box"),
])
D.kicker(s, "“The winners could compensate the losers” is a fact about "
            "arithmetic, not a description of what happens.", y=4.52)
D.notes(s, """The compensation principle, and the book raises it directly in its
end-of-chapter questions — one of them asks why it matters that wages and employment fall
for some workers if the winners could more than compensate them. So this is examinable in
discussion form as well as being the right way to close.

The logic is clean: gains 1,000, losses 600, so a transfer of 600 leaves everyone at least
as well off with 400 left over. That is what "the country gains" means, formally.

The gap between "could" and "does" is the whole of the second card, and it is worth being
concrete about why the gap persists. The gains from trade are spread across everyone as
slightly cheaper goods, largely invisible. The losses are concentrated on identifiable
people in identifiable places. Diffuse beneficiaries do not organise; concentrated losers
do. That asymmetry is not a market failure — it is a feature of how political attention
works.

The third card is the honest boundary of the discipline and it is worth saying carefully.
Economics can establish that the compensation is affordable. It cannot make it happen, and
it has no special authority to say how much of it there should be. That is a question for
voters.

If a student wants to argue that the compensation never materialising is itself a reason to
be sceptical of free-trade arguments, that is a coherent position and you should say so
rather than talk them out of it. It is a claim about political feasibility, not about the
arithmetic.""")

# ============================================ 66. what the model does not settle
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
mirrors the equity-versus-efficiency slide at the end of Chapter 7, and it is worth saying
that out loud — this is the second time the course has drawn this line, and it will not be
the last.

The left box is genuinely settled. There is no serious school of economics that disputes
that specialisation by comparative advantage raises total output. Students should know
which parts of what they have been taught are robust.

The right box is not settled and, more importantly, is not the kind of thing that could be
settled by better economics. How much a town is worth against a national total is not a
measurement problem. It is a values question, and having a model does not give an economist
a vote worth more than anyone else's.

The band is the transferable skill, and it is the most useful sentence in the deck: most
bad arguments about policy come from putting a question in the wrong box — either treating
a values question as if data could settle it, or treating a factual question as if it were
a matter of opinion.

Then hand over to Chapter 9 in one sentence: this chapter assumed that the only people
affected by a transaction are the two people making it. Next time we drop that, and the
first casualty is the assumption that a market price reflects a real cost.""")

# ============================================================ 67. recap
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

Read the closing line out. It is the honest summary of the chapter: one idea, demonstrated
at three scales, and the scale never mattered.

The right-hand column points at SECTIONS rather than exhibit numbers, deliberately. This
deck was built without the publisher's slides for this chapter, so I have not cited exhibit
numbers I could not verify. Students should be told to read by section, and if you want
exhibit numbers on this slide, add them from your copy of the book before recording.

If you cut material today, leave this slide up while you say what got cut and where to read
it.

Point forward: this chapter assumed every cost of a transaction falls on the two parties
doing it. Chapter 9 removes that assumption.""")

# ============================================================ 68. takeaways
s = S()
D.takeaways_page(s, "Chapter 8: Trade", [
    "The slope of a production possibilities curve is an opportunity cost. That single "
    "fact is what the curve is for.",
    "Comparative advantage — lowest opportunity cost — decides who should do what. Being "
    "better at something is not the same as being cheaper at it.",
    "Specialise and trade at a price between the two opportunity costs, and both sides "
    "consume outside their own curve. Nobody worked harder.",
    "Compare the world price with your own no-trade price. Below it you import, above it "
    "you export, and either way the country gains on net.",
    "A tariff is a transfer plus a deadweight loss. The transfer is arguable; the two "
    "triangles are value that stops existing.",
])
D.notes(s, """Key takeaways. Five, and the second and third are the ones that matter beyond
this course.

If they remember one thing, make it the third: two people, the same hours, the same skills,
and more of everything at the end. That result is two hundred years old, it is still
counter-intuitive, and it is the best single advertisement for the subject.

The first, second and fifth are the examinable core. The tariff diagram in particular will
be asked, and it will be asked as a drawing.

Close the lecture on the honest note rather than the triumphant one. Everything today was a
statement about totals. The chapter proved that trade makes the total bigger; it did not
prove that everyone gains, and the diagram showed the losers in red from the first
picture.

Set up what comes next: today every cost of a transaction fell on the people making it.
Next time somebody outside the transaction pays part of the bill, and the price stops
telling the truth. That is Chapter 9 — externalities and public goods — and it is the
chapter where markets start needing help.""")

prs.save(OUT)
print(f"{OUT}: {len(prs.slides._sldIdLst)} slides")
