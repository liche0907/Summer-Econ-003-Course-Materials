#!/usr/bin/env python3
"""Build ECON003_Ch07_Perfect_Competition_and_the_Invisible_Hand_UCR.pptx.

Built from the Ch06 deck to claude/slide-ground-rules.md.  Static - no animations, by
rule.  The title slide keeps the UCR card and its text and carries NO bottom-right
picture, by instruction.

Every figure comes from Resources/ArtScripts/ch07_charts.py, which derives all of them
from four stated primitives.  Publisher errors are flagged on the slide face without
naming the publisher; the naming happens in the speaker notes.
"""
import os

from pptx import Presentation

import deckkit as D
from deckkit import (BLUE, GOLD, DGOLD, GREEN, RED, INK, GREY, RULE, WHITE,
                     TINT_BLUE, TINT_NEUTRAL, TINT_RED, TINT_GREEN, TINT_GOLD)

SRC = "/mnt/user-data/uploads/ECON003_26S/Slides/ECON003_Ch06_Sellers_and_Incentives_UCR.pptx"
OUT = "ECON003_Ch07_Perfect_Competition_and_the_Invisible_Hand_UCR.pptx"
F = "figs/ch07_fig_%s.png"
IC = "icons/%s.png"
PH = "photos/%s_flat.png"

LIMIT = 4.40          # nothing but the kicker below this

prs = Presentation(SRC)
D.drop_slides_after(prs, 1)
s1 = prs.slides[0]
D.retitle_title_slide(s1, ["Chapter 7", "Perfect Competition and the Invisible Hand"],
                      ["ECON 003", "UC Riverside · Summer 2026"])
D.notes(s1, """Title.

Chapter 7. Chapters 5 and 6 built one buyer's problem and one seller's problem. Today
those two problems meet in a market, and the question is what comes out when nobody is
in charge.

No theme image on the title card yet, by instruction.

The sentence to open with: for two chapters we have watched individuals do the best they
can for themselves. Today we ask whether the result of everyone doing that is chaos or
something better than chaos - and we get to measure the answer, not just assert it.""")


def S():
    return D.blank_slide(prs)


# ============================================================ 2. where we left off
s = S()
D.title(s, "Where We Left Off")
y = D.defbox(s, 1.15,
             "Chapter 5 built the demand curve out of one buyer's problem.\n"
             "Chapter 6 built the supply curve out of one seller's problem.\n"
             "Today we put them in the same room.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "What buyers do", "Spend the next dollar where it buys the most utility. "
     "Stack those choices and you have demand.", IC % "shopping-cart"),
    (RED, "What sellers do", "Produce where price equals marginal cost. Stack those "
     "choices and you have supply.", IC % "factory"),
    (GREEN, "What nobody does", "Coordinate any of it. No one adds the two sides up. "
     "And yet the market clears.", IC % "exchange"),
])
D.kicker(s, "Today's question: when self-interested people trade, what does society end "
            "up with?", y=4.52)
D.notes(s, """Recap and framing.

Keep the recap to twenty seconds. The only thing that matters is the third card: nobody
in either of the last two chapters was trying to make the market work. Every actor was
selfish in the technical sense - maximising their own objective.

The claim of Chapter 7 is that the outcome of all that private optimisation is, under
strict conditions, the best outcome available to society as a whole. That claim is
testable, and we test it three times today: within a market, within a firm, and across
industries.

Do not oversell it. Say now, once, that the conditions are strict and that Chapter 8
onwards is largely about what happens when they fail.""")

# =================================================================== 3. roadmap
s = S()
D.title(s, "Today's Roadmap")
D.strip5(s, 1.30, [
    ("1. Efficiency,\nmeasured", IC % "balance-scale"),
    ("2. Inside\none firm", IC % "factory"),
    ("3. Across\nindustries", IC % "truck"),
    ("4. Prices as\nsignals", IC % "price-tag"),
    ("5. Equity vs\nefficiency", IC % "ballot-box"),
])
D.rect(s, 0.60, 3.05, 8.80, 0.06, fill=RULE)
D.cards2(s, 3.32, 1.42, [
    (BLUE, "One idea, three scales",
     "The same mechanism runs the whole hour: prices carry information, and self-interest "
     "acting on that information lands resources where they are worth most."),
    (GOLD, "And the question we open with",
     "Your ride home costs three times the usual price. Is that the market working, or "
     "the market failing? Answer it now and see whether your answer survives the hour."),
])
D.notes(s, """Roadmap.

Five parts and they escalate in scope: one market, then one firm with two plants, then a
whole economy of industries, then the price system itself, then the one thing the model
cannot settle for us.

Announce the carried question here and again on the next slide. It is deliberately the
one students already have an opinion about, and most rooms start out against surge
pricing. That is exactly what makes the ending land.""")

# ============================================ 4. the carried question (photograph)
s = S()
D.title(s, "A Question to Carry Through the Hour")
px, py, pw, ph = D.photo(s, PH % "uber_phone", 5.05, 1.15, 4.35, 2.60)
D.textbox(s, 0.60, 1.20, 4.20, 0.90,
          "It is raining, the game has just ended, and the app says your ride home "
          "costs $32 instead of $15.", size=15, bold=True, color=BLUE, line_pct=1.22)
D.rect(s, 0.60, 2.22, 4.20, 0.06, fill=GOLD)
D.textbox(s, 0.60, 2.44, 4.20, 0.90,
          "Is that price doing something useful, or just taking advantage of you?",
          size=15, bold=True, color=INK, line_pct=1.22)
D.cards2(s, 3.92, 1.26, [
    (RED, "Most people say",
     "Gouging. Same road, same car, same driver — only the moment has changed."),
    (GREEN, "Hold that thought",
     "By the end of the hour you will be able to put a number on it."),
])
D.image_credit(s)
D.notes(s, """The carried question. Pose it, do NOT answer it.

Take a show of hands: who thinks surge pricing makes riders worse off overall? Write the
split on the board. Rooms usually run three to one against surge, and coming back to that
number at the end is the single most effective thing on this slide.

The photograph and the framing are the publisher's evidence-based-economics question for
this chapter. Do not say so on the slide.

Two things NOT to claim yet: that surge pricing is good, and that it is bad. The whole
point is that we will have a measurement by slide 62, not an opinion.

The $32 figure is illustrative — it is a plausible multiplier, not a quoted fare. Do not
attribute it to any company.""")

# ============================================================= 5. PART 1 divider
s = S()
D.divider(s, "PART 1", "Perfect Competition\nand Efficiency")
D.notes(s, """Section divider - Part 1, Pearson section 7.1.

The job of this part is to make "efficient" a measurable word rather than a compliment.
By the end of it students should be able to compute social surplus for a small market and
say exactly how much a restriction costs.""")

# ====================================================== 6. Adam Smith (photograph)
s = S()
D.title(s, "One Sentence, from 1776")
px, py, pw, ph = D.photo(s, PH % "globe", 0.60, 1.15, 3.90, 2.85)
D.textbox(s, 4.85, 1.20, 4.55, 1.50,
          "“It is not from the benevolence of the butcher, the brewer, or the baker, "
          "that we expect our dinner, but from their regard to their own interest.”",
          size=14.5, bold=True, color=BLUE, italic=True, line_pct=1.24)
D.textbox(s, 4.85, 2.80, 4.55, 0.40, "Adam Smith, The Wealth of Nations, 1776",
          size=11, color=GREY)
D.band(s, 3.30, "Smith's claim is not that people are nice. It is that they do not have "
                "to be.", kind="note", size=13.5, x=4.85, width=4.55)
D.kicker(s, "The butcher feeds you because it pays him to. That is the whole mechanism.",
         y=4.42)
D.image_credit(s)
D.notes(s, """Adam Smith, and the sentence the chapter is built on.

Read the quotation out loud. It is short and it is the most quoted sentence in economics
for a reason.

Two things worth saying:

First, the phrase "invisible hand" appears exactly once in The Wealth of Nations, in Book
IV, and Smith used it far more cautiously than the modern slogan does. If a student asks,
that is the honest answer — Smith was making a narrower argument than the phrase now
carries.

Second, and this is the one to labour: Smith is not describing a moral system. He is
describing an information and incentive system. The butcher does not need to know you, or
care about you, or even know your name. The price does the communicating.

Ask: what would it take for a central planner to feed a city as well as the butchers,
brewers and bakers do? Hold the answer until Part 4 — it is the coordination problem.""")

# ============================================== 7. selfish vs self-interested
s = S()
D.title(s, "Selfish and Self-Interested Are Not the Same Word")
y = D.defbox(s, 1.15,
             "Self-interested means acting on your own preferences.\n"
             "Selfish means being indifferent to everyone else's.")
D.cards2(s, y + 0.28, LIMIT - (y + 0.28), [
    (BLUE, "Self-interested", "You buy the cheaper flight, take the better-paid job, and "
     "give to a charity you care about. All three are self-interested — your preferences "
     "include other people.", IC % "owner"),
    (RED, "Selfish", "Your preferences stop at your own skin. Economics does not need "
     "this assumption, and the model in this chapter does not use it.",
     IC % "coin-stack"),
])
D.kicker(s, "The invisible hand needs self-interest. It does not need selfishness.",
         y=4.50)
D.notes(s, """A distinction the publisher flags and students routinely miss.

Students arrive believing economics assumes people are selfish, and they resist the whole
chapter because of it. Kill that in ninety seconds here.

The model needs one thing: that people act on their own preferences consistently. It says
nothing about what those preferences contain. A person whose utility rises when their
neighbour eats is self-interested and not selfish, and every result today goes through
unchanged.

Good line: "The assumption is not that you are a bad person. The assumption is that you
are a person."

If someone pushes on altruism and market outcomes, the honest answer is that altruistic
preferences change what is demanded, not whether the market clears efficiently given what
is demanded.""")

# ================================================================ 8. reservation values
s = S()
D.title(s, "Two Numbers That Do All the Work")
y = D.defbox(s, 1.15,
             "Reservation value — the most a buyer will pay, or the least a seller will "
             "accept, for one unit.")
y2 = D.band(s, y + 0.22,
            "Buyer's surplus = reservation value − price      ·      "
            "Seller's surplus = price − reservation value", kind="formula", size=14)
D.cards2(s, y2 + 0.22, LIMIT - (y2 + 0.22), [
    (BLUE, "For a buyer", "It is the value of the thing to you. Above it you walk away; "
     "below it you buy and pocket the difference.", IC % "shopping-cart"),
    (RED, "For a seller", "It is what the thing costs you to give up. Below it you keep "
     "it; above it you sell and pocket the difference.", IC % "register"),
])
D.notes(s, """Reservation values.

This is the vocabulary slide for the whole of Part 1, and it is worth being pedantic.

A reservation value is a *number in a person's head*, and it is the source of every
surplus figure we compute today. Notice that it is exactly willingness to pay from
Chapter 5 and willingness to accept from Chapter 6 — new word, old idea, and say that
explicitly so students do not think they have to learn something new.

The two formulae on the blue band are the only arithmetic in this section. Everything
else is addition.

One caution to flag: reservation values are unobservable in the real world. In the toy
market on the next slide we are handed them. In an actual market we infer them from
behaviour, which is what makes empirical demand estimation hard. Do not let students walk
away thinking these numbers are lying around.""")

# =========================================================== 9. Exhibit 7.1 table
s = S()
D.title(s, "Exhibit 7.1 — Seven Buyers, Seven Sellers")
rows = [["Buyer", "Will pay", "Cum. Q", "Seller", "Will accept", "Cum. Q"],
        ["Madeline", "$70", "1", "Tom", "$10", "1"],
        ["Katie", "$60", "2", "Mary", "$20", "2"],
        ["Sean", "$50", "3", "Jeff", "$30", "3"],
        ["Dave", "$40", "4", "Phil", "$40", "4"],
        ["Ian", "$30", "5", "Adam", "$50", "5"],
        ["Kim", "$20", "6", "Matt", "$60", "6"],
        ["Ty", "$10", "7", "Fiona", "$70", "7"]]
D.table(s, 0.60, 1.15, 8.80, 2.55, rows,
        col_w=[1.70, 1.30, 1.10, 1.70, 1.40, 1.60],
        first_col_fill=BLUE, header_size=10, body_size=10,
        align=["l", "ctr", "ctr", "l", "ctr", "ctr"])
D.kicker(s, "One market for one used phone each. Nobody trades more than once.", y=3.92)
D.notes(s, """Exhibit 7.1. Tell them to photograph it — every number in the next eight
slides comes from this table.

Set it up carefully. Seven people each want to buy one phone; seven people each own one
and would sell it. Madeline values a phone at $70; Tom would part with his for $10.

Then walk the logic of the two "cumulative quantity" columns, because that is what turns
a list of people into a curve: at any price, the number of buyers willing to trade is the
number whose reservation value is at least that price, reading down; the number of
sellers is the number whose reservation value is at most that price, reading down the
other side.

One honest note: the numbers are symmetric on purpose, so the arithmetic stays clean. Real
markets are not, and nothing in the argument depends on the symmetry.

A student will notice this is not the market as they experience it — one phone each, no
haggling. Agree, and say that Chapter 4's smooth curves are what you get when you do this
with a million people instead of seven.""")

# ============================================== 10. what happens at $10 and $60
s = S()
D.title(s, "Try a Price. Any Price.")
D.cards2(s, 1.15, 1.55, [
    (RED, "At a price of $10",
     "Every one of the seven buyers wants a phone — $10 is below what all of them will "
     "pay. Only Tom will sell. Seven wanted, one available."),
    (RED, "At a price of $60",
     "Only Madeline and Katie still want one. But Tom, Mary, Jeff, Phil, Adam and Matt "
     "all want to sell. Two wanted, six available."),
])
y = D.band(s, 2.90, "At $40 — and only at $40 — four buyers want a phone and four "
                    "sellers want to sell one.", kind="answer", size=14.5)
D.cards2(s, y + 0.22, 5.00 - (y + 0.22), [
    (BLUE, "The price is not chosen", "Nobody sets it. It is the only number at which the "
     "two sides of the table agree."),
    (GREEN, "This is Chapter 4's equilibrium", "The same idea, small enough to count on "
     "your fingers."),
])
D.notes(s, """Trying prices. Do this live at the board rather than reading the slide.

Pick $10 first, because the imbalance is dramatic and everyone can see it: seven buyers,
one seller. Then $60 the other way. Then ask the room for the price that balances before
you reveal $40.

The pedagogical point is that equilibrium is not a compromise or a fair price or a price
anyone negotiated. It is an arithmetic fact about the table.

Worth pausing on: at $40, Dave and Phil are both exactly indifferent. Dave pays what the
phone is worth to him; Phil accepts exactly what it costs him. Neither gains anything.
That is why the fourth trade adds nothing to social surplus, and it is the detail that
makes the next few slides make sense.

A sharp student may ask whether the equilibrium quantity is 3 or 4. Both give total
surplus of $120, because the fourth trade creates zero surplus. Say so — it is a good
question, not a gotcha.""")

# =============================================== 11. Exhibit 7.2 staircase figure
s = S()
D.title(s, "Exhibit 7.2 — The Same Table, Drawn")
D.picture_fit(s, F % "staircase", 0.60, 1.12, 8.80, 3.20)
D.kicker(s, "Every step is one person. Where the staircases cross is where the table "
            "balanced.", y=4.46)
D.notes(s, """Exhibit 7.2 - the staircase market.

Walk it slowly the first time. The blue staircase is the demand curve: it starts high at
Madeline's $70 and drops one step per buyer. The red staircase is supply, starting at
Tom's $10 and climbing.

The steps are the point. In Chapter 4 the curves were smooth lines and students took them
on trust. Here you can see what a demand curve IS — a queue of people sorted by how much
they value the thing. Say that out loud: a demand curve is a queue.

The curves cross at $40 and four units, exactly as the table said. Nothing new has
happened; we have just changed representation.

If you have time, the one extra sentence worth adding: add a few million more people and
the steps get small enough that the staircase looks like a line. That is all the smooth
curves in Chapter 4 ever were.""")

# ============================================= 12. consumer surplus rebuilt
s = S()
D.title(s, "Consumer Surplus, at a Price of $40")
rows = [["Buyer", "Will pay", "Pays", "Consumer surplus"],
        ["Madeline", "$70", "$40", "$30"],
        ["Katie", "$60", "$40", "$20"],
        ["Sean", "$50", "$40", "$10"],
        ["Dave", "$40", "$40", "$0"],
        ["Ian, Kim, Ty", "$30 and below", "—  no trade", "$0"],
        ["Total", "", "", "$60"]]
D.table(s, 1.10, 1.15, 7.80, 2.35, rows, col_w=[2.10, 1.90, 1.80, 2.00],
        first_col_fill=BLUE, header_size=10, body_size=10.5,
        align=["l", "ctr", "ctr", "ctr"])
D.band(s, 3.68, "Consumer surplus is what buyers got for free: the gap between what a "
                "phone was worth to them and what they paid.", kind="formula", size=13.5)
D.notes(s, """Consumer surplus, rebuilt from the table.

Do the first row out loud. Madeline would have paid $70 and paid $40, so she walks away
$30 better off than if she had not traded. That $30 is real — it is not accounting profit,
it is the value she captured.

Then Katie $20, Sean $10, Dave $0.

Two things to be explicit about:

Ian, Kim and Ty get nothing, and that is not a failure. Their reservation values are below
$40, so a trade at $40 would have made them worse off. The market correctly excluded
them.

Dave gets nothing either, but for the opposite reason — he traded, and it was exactly a
wash. Marginal buyer, zero surplus. That is what "marginal" means.

Total: $60. Write it on the board and leave it there; you need it in two slides.""")

# ============================================= 13. producer surplus rebuilt
s = S()
D.title(s, "Producer Surplus, at the Same Price")
rows = [["Seller", "Will accept", "Receives", "Producer surplus"],
        ["Tom", "$10", "$40", "$30"],
        ["Mary", "$20", "$40", "$20"],
        ["Jeff", "$30", "$40", "$10"],
        ["Phil", "$40", "$40", "$0"],
        ["Adam, Matt, Fiona", "$50 and above", "—  no trade", "$0"],
        ["Total", "", "", "$60"]]
D.table(s, 1.10, 1.15, 7.80, 2.35, rows, col_w=[2.30, 1.90, 1.70, 1.90],
        first_col_fill=RED, header_size=10, body_size=10.5,
        align=["l", "ctr", "ctr", "ctr"])
D.band(s, 3.68, "Producer surplus is the mirror image: the gap between what a seller "
                "received and the least they would have accepted.", kind="formula",
       size=13.5)
D.notes(s, """Producer surplus - the mirror of the last slide.

Run it fast. The structure is identical and students will see it coming, which is the
point: the two sides of a market are the same problem viewed from opposite ends.

Tom's $30 is the biggest gain because Tom was the most eager seller. Fiona, who wanted
$70, sells nothing and loses nothing.

Total again $60, which is a coincidence of the symmetric numbers, not a law. Say that
explicitly — a student who leaves thinking consumer and producer surplus are always equal
has learned something false. In Chapter 4's tax and price-control diagrams they were very
much not equal.

Now you have $60 and $60 on the board.""")

# ==================================================== 14. social surplus figure
s = S()
D.title(s, "Social Surplus")
y = D.defbox(s, 1.08, "Social surplus = consumer surplus + producer surplus")
D.picture_fit(s, F % "surplus", 0.60, y + 0.08, 8.80, 4.52 - (y + 0.08))
D.kicker(s, "$60 + $60 = $120. That is the whole value this market created — now try to "
            "beat it.", y=4.58)
D.notes(s, """Social surplus, and the number the rest of Part 1 is measured against.

Definition first: social surplus is the total value the market created, counting everyone
in it. It does not care who got what — a dollar of surplus to Fiona counts the same as a
dollar to Madeline. Flag that now, because it is exactly the assumption Part 5 comes back
and questions.

On the figure: the blue blocks above the price line are consumer surplus, the red blocks
below it are producer surplus, and the whole shaded region is social surplus. The area
between the two staircases, up to where they cross.

Then set up the next two slides as a challenge. We have a candidate answer — $120, from
leaving the market alone. Anyone who thinks a rule would do better has to beat $120. We
will try two rules: a cap and a floor.

Numbers to have to hand: $60, $60, $120.""")

# ===================================================== 15. cap it at two
s = S()
D.title(s, "Now Cap the Market at Two Phones")
y = D.defbox(s, 1.12,
             "Only two phones may be traded, at $40. Madeline and Katie buy; Tom and "
             "Mary sell.", tint=TINT_GOLD, border=DGOLD, color=DGOLD)
D.cards3(s, y + 0.24, 1.30, [
    (BLUE, "Consumer surplus", "$30 + $20 = $50", IC % "shopping-cart"),
    (RED, "Producer surplus", "$30 + $20 = $50", IC % "register"),
    (DGOLD, "Social surplus", "$50 + $50 = $100 — down $20", IC % "balance-scale"),
])
y2 = D.band(s, y + 1.78,
            "The missing $20 is one trade: Sean would have paid $50 for a phone Jeff "
            "would have sold for $30.", kind="flag", size=13.5)
D.credit(s, "Worth checking against the textbook's table: the consumer- and "
            "producer-surplus columns there are each totalled at $100, but each column "
            "sums to $50. The $100 is the social surplus, and it is the only figure of "
            "the three that is right.", y=4.92)
D.notes(s, """The cap, and the first arithmetic slip in the publisher's deck.

Work it live. With only two trades allowed, Madeline and Katie buy at $40 and Tom and
Mary sell. Consumer surplus is 30 + 20 = $50. Producer surplus is 30 + 20 = $50. Social
surplus $100, down from $120.

THE ERROR TO KNOW ABOUT: the Pearson slides for this section print "$100" as the total of
the consumer-surplus column AND as the total of the producer-surplus column. Each of those
columns sums to $50. Their next slide then says social surplus is $100, which is right —
so the two table totals are each double what they should be. Students revising from the
publisher deck will hit this, which is why the correction is on the slide face. Do not say
"Pearson got it wrong" on camera; say "if you see $100 in a surplus column, check the
column."

The lost $20 is worth naming and re-naming: it is not money that went somewhere else. It
is value that never came into existence, because a trade that would have made two people
better off was not allowed to happen. Sean would have paid $50; Jeff would have sold at
$30; the $20 between them is gone.

That is the first deadweight loss of the course, though we do not use the term until Part
4.""")

# ============================================ 16. Exhibit 7.3 three panels
s = S()
D.title(s, "Exhibit 7.3 — Cap It, Leave It, or Force It")
D.picture_fit(s, F % "three_panels", 0.60, 1.12, 8.80, 3.12)
D.kicker(s, "Too few trades wastes $20. Too many wastes $20. Left alone, the market "
            "finds the top.", y=4.40)
D.notes(s, """Exhibit 7.3, and the punchline of Part 1.

Three panels, and the middle one wins.

Panel (a) - the cap. Two trades, surplus $100. The market is stopped before it has
finished creating value.

Panel (b) - left alone. Four trades, surplus $120. The maximum.

Panel (c) - a floor: five trades required. Now Ian, who values a phone at $30, has to buy
one from Adam, who would only part with his for $50. That trade destroys $20 of value.
Surplus back down to $100.

The symmetry is the thing to point at. Interfering in either direction costs the same $20,
for opposite reasons: the cap blocked a trade worth making, the floor forced a trade not
worth making.

State the result plainly: the competitive equilibrium maximises social surplus. Not
"tends to", not "usually" — in this market, exactly, and you can check it by adding up
seven numbers.

Then immediately add the caveat, because it is the honest half: this result assumes the
conditions of perfect competition hold. When they do not — and Chapter 8 onwards is
mostly about when they do not — the result can fail.""")

# ============================================================ 17. Pareto efficiency
s = S()
D.title(s, "Pareto Efficiency")
y = D.defbox(s, 1.15,
             "An allocation is Pareto efficient when nobody can be made better off "
             "without making somebody else worse off.")
D.cards2(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "At $40 and four phones",
     "Try it. Move a phone to Ian and you must take it from someone who values it more. "
     "Change the price and one side gains exactly what the other loses. There is no free "
     "move left.", IC % "balance-scale"),
    (RED, "At $20, say",
     "Buyers do better and sellers do worse. That is not a Pareto improvement — it is a "
     "transfer. And with fewer sellers willing, fewer phones trade at all.",
     IC % "exchange"),
])
D.kicker(s, "“No free moves left” is a much weaker claim than “this "
            "outcome is fair”.", y=4.50)
D.notes(s, """Pareto efficiency - and the sentence that stops it being mistaken for a
moral endorsement.

Definition first, then test it on the market they already know.

The important and slightly deflating fact: Pareto efficiency is a very low bar. An
allocation in which one person owns everything and everyone else owns nothing is Pareto
efficient, because you cannot improve anyone without hurting the owner. Say that example
out loud — it is the single most useful thing on this slide, and it inoculates students
against reading "efficient" as "good".

Relation to social surplus: maximising social surplus implies Pareto efficiency here, but
the reverse does not hold in general. Do not go deeper than that in an intro course; just
be sure nobody leaves thinking the two words are synonyms.

Set up Part 5 now with one sentence: efficiency is about the size of the pie, equity is
about the slices, and this chapter's model has nothing to say about the slices.""")

# ================================================ 18. what efficient does not mean
s = S()
D.title(s, "What “Efficient” Does and Does Not License")
D.cards2(s, 1.15, 1.65, [
    (GREEN, "It does say", "If the market is perfectly competitive and you intervene, "
     "you will end up with less total surplus than you started with. That is a real "
     "result and it has teeth."),
    (RED, "It does not say", "That the outcome is fair, that everyone can afford the "
     "product, or that we should never intervene. Surplus counts dollars, not people."),
])
y = D.band(s, 3.02,
           "So intervention cannot be justified on efficiency grounds here — but it may "
           "still be justified on other grounds.", kind="note", size=14)
D.kicker(s, "Efficiency is one argument. It was never meant to be the only one.", y=4.46)
D.notes(s, """The boundary of the result. This slide is where students most often
over-learn the chapter, so it is worth a full minute.

The publisher states this carefully and we should too: because the competitive equilibrium
is Pareto efficient, government intervention in THIS market cannot be defended by saying
it will make the pie bigger. It will not.

But three things remain wide open, and name all three:

One — the conditions. Perfect competition needs many buyers, many sellers, identical
goods, free entry, and good information. Remove any of them and the efficiency result can
break. Chapter 8 onwards.

Two — external effects. If production pollutes, private surplus and social surplus are
different numbers, and the market maximises the wrong one.

Three — distribution. Efficiency is silent on it, by construction, and Part 5 comes back
to this.

The line to say: "Efficient is a technical word with a narrow meaning. If you use it as a
compliment you will lose arguments to people who know what it means." """)

# ============================================================= 19. PART 2 divider
s = S()
D.divider(s, "PART 2", "Inside the Firm")
D.notes(s, """Section divider - Part 2, Pearson section 7.2.

The scale changes. Part 1 was a market of individuals; this is one firm with two factories
and a manager who thinks he can do better than the market.

Tell them at the top that this section has a twist and that it is worth staying with the
arithmetic, because the answer is not the one the setup points at.""")

# ================================================================= 20. the new CEO
s = S()
D.title(s, "You Are the New CEO")
y = D.defbox(s, 1.15,
             "Your company makes microchips in a perfectly competitive market. The price "
             "is $10 a chip and you cannot move it. You own two plants.")
D.cards2(s, y + 0.26, LIMIT - (y + 0.26), [
    (RED, "The old plant", "Fifty years old. Old machinery, higher marginal cost at every "
     "level of output. Currently makes 20,000 chips a day and earns exactly nothing.",
     IC % "factory"),
    (GREEN, "The new plant", "Four years old. Better technology, lower cost. Makes 50,000 "
     "chips a day and earns $125,000 a day.", IC % "hard-hat"),
])
D.kicker(s, "Each plant has been run by its own manager, each told to maximise their own "
            "plant's profit.", y=4.50)
D.notes(s, """The setup. Read it as a management problem, not an economics problem — that
is what makes the twist work.

The facts to establish clearly, because everything turns on them:

- The firm is a price taker. $10 a chip, take it or leave it. Chapter 6's rule applies:
  produce where P = MC.
- The two plants have different technology. The old plant's marginal cost is higher at
  every quantity.
- Each plant manager has been optimising independently, and neither has been told anything
  about the other.

Ask the room to predict, before the numbers arrive, what a good CEO should do. Most will
say consolidate into the modern plant. That is the trap, and it is a genuinely reasonable
first instinct — this is not a stupid mistake, it is what most managers would say.

Do not tip the answer.""")

# ==================================================== 21. Exhibit 7.4 two MC curves
s = S()
D.title(s, "Exhibit 7.4 — Two Plants, Two Marginal Cost Curves")
D.picture_fit(s, F % "two_plants_mc", 0.60, 1.12, 8.80, 3.14)
D.kicker(s, "The old plant is worse at every single level of output. Remember that — it "
            "is not enough to settle the question.", y=4.42)
D.notes(s, """Exhibit 7.4.

Read the picture: the old plant's marginal cost curve lies above the new plant's
everywhere. At any quantity you care to name, the old plant costs more to run than the
new one.

That fact is true and it is also the fact that misleads the CEO, so mark it now. Being
worse at every quantity does not mean you should not be used at all — because the two
plants do not have to produce the same quantity.

A note on the drawing, if a student compares it with the textbook: our marginal cost
curves are straight lines because both plants' costs come from an explicit quadratic cost
function, which is what lets every number in this section be exact rather than
approximate. The textbook draws them freehand with a dip. Nothing in the argument depends
on the shape — only on the old plant's curve being above the new one's.

Numbers behind the drawing, if asked: old plant total cost is 100,000 + 0.00025Q²; new
plant is 125,000 + 0.0001Q².""")

# ================================================= 22. each manager's own problem
s = S()
D.title(s, "Each Manager Solves the Chapter 6 Problem")
y = D.band(s, 1.15, "Step 1: find where MR = MC      ·      Step 2: read ATC at that "
                    "quantity      ·      Step 3: compare P with ATC",
           kind="formula", size=14)
D.cards3(s, y + 0.24, LIMIT - (y + 0.24), [
    (BLUE, "Price is marginal revenue", "A price taker sells every extra chip for $10, so "
     "MR = P = $10 no matter how many it makes.", IC % "price-tag"),
    (RED, "So each plant sets MC = $10", "Not the same quantity in each plant — the same "
     "marginal cost. The old plant hits $10 at 20,000; the new one at 50,000.",
     IC % "factory"),
    (GREEN, "Then check profit", "Compare $10 with average total cost at the chosen "
     "quantity. That comparison, not marginal cost, is what says whether money is being "
     "made.", IC % "ledger"),
])
D.kicker(s, "Nobody is coordinating. Each manager is looking only at their own plant.",
         y=4.42)
D.notes(s, """The recall slide. Keep it brisk — this is Chapter 6's three steps, unchanged.

The one sentence that matters, and it is easy to say too fast: the two managers choose
DIFFERENT quantities but the SAME marginal cost. Both stop where the next chip costs $10
to make, because both face a price of $10.

That is the whole mechanism of this section, arriving quietly. Say it, then say it again
in different words: independent profit maximisation makes marginal cost equal across
plants without anybody arranging it.

If a student asks why they do not both make the same amount: because the plants have
different cost curves, so $10 of marginal cost buys different quantities in each.""")

# ============================================================ 23. Exhibit 7.5 old
s = S()
D.title(s, "Exhibit 7.5 — The Old Plant's Answer")
D.picture_fit(s, F % "old_plant", 0.60, 1.10, 8.80, 3.02)
y = D.band(s, 4.22, "20,000 chips · revenue $200,000 · cost $200,000 · economic profit $0",
           kind="neutral", size=13.5)
D.notes(s, """Exhibit 7.5.

The old plant's manager sets MC = $10 and lands on 20,000 chips a day.

Read the rectangle: 20,000 chips at an average total cost of $10 is $200,000 of cost, and
20,000 chips at a price of $10 is $200,000 of revenue. Economic profit exactly zero.

Two things to say about that zero:

First, it is a coincidence of where this plant's cost curve sits — the price happens to
equal the minimum of its average total cost. Nothing forced it.

Second, and this is the Chapter 6 point students keep forgetting: zero ECONOMIC profit is
not zero profit. The owners are earning exactly the return they could get elsewhere. The
plant is not in trouble.

Have the numbers ready to say, not recall: 20,000 chips, $10 each, $200,000 of revenue,
$200,000 of cost, $0 profit.""")

# ============================================================ 24. Exhibit 7.6 new
s = S()
D.title(s, "Exhibit 7.6 — The New Plant's Answer")
D.picture_fit(s, F % "new_plant", 0.60, 1.10, 8.80, 3.02)
y = D.band(s, 4.22, "50,000 chips · revenue $500,000 · cost $375,000 · economic profit "
                    "$125,000", kind="answer", size=13.5)
D.notes(s, """Exhibit 7.6.

Same rule, different plant, different answer: MC = $10 at 50,000 chips.

Read the two rectangles. The lower one is cost: 50,000 chips at an average total cost of
$7.50 is $375,000. The upper one is profit: 50,000 chips at $2.50 of margin each is
$125,000 a day.

Emphasise that the profit rectangle is the price-minus-ATC gap times quantity — the same
picture as Chapter 6, and the same picture that will come back in Part 3.

Firm totals so far, and put them on the board: 70,000 chips a day, revenue $700,000, cost
$575,000, profit $125,000.

Every one of these figures comes out exactly from the two cost functions; none of them is
rounded.""")

# ================================================= 25. should you close the old plant
s = S()
D.title(s, "So Should You Close the Old Plant?")
y = D.defbox(s, 1.15,
             "The new plant is newer, cheaper, and earns all the money. The old plant "
             "earns nothing. Move all 70,000 chips to the new plant?",
             tint=TINT_GOLD, border=DGOLD, color=DGOLD)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "The case for closing", "Lower costs, better technology, and $100,000 a day "
     "of the old plant's fixed costs disappear with it.", IC % "coin-stack"),
    (BLUE, "The case for waiting", "The old plant is earning zero economic profit, which "
     "means it is covering its opportunity cost exactly. It is not losing money.",
     IC % "clock"),
    (RED, "The question to ask", "Not “which plant is better?” but “what "
     "does the 70,000th chip cost in each place?”", IC % "lightbulb"),
])
D.kicker(s, "Decide before you turn the page.", y=4.44)
D.notes(s, """The decision point. Pause here.

Take a vote: close the old plant, or leave both open? Most rooms close it, and so do most
executives, which is what makes this example good.

The third card is the whole lesson, and it is worth saying before the reveal even though
it gives away the method: the comparison that matters is not between plants, it is between
the marginal cost of the next chip in each plant. "Which factory is better" is the wrong
question; "where should the next chip be made" is the right one.

Note the honest strengthening of the publisher's version: we are crediting the closure
with saving the old plant's entire $100,000 a day of fixed costs. That makes closing look
as good as it can possibly look — and it still loses. Say that, because a student will
otherwise ask whether the fixed cost was double counted.""")

# ================================================================ 26. one year later
s = S()
D.title(s, "One Year Later")
D.cards2(s, 1.15, 1.45, [
    (GREY, "Old plant", "Output 0.  Profit $0.  Closed, as ordered."),
    (RED, "New plant", "Output 70,000 a day.  Profit $85,000 — down from $125,000."),
])
y = D.band(s, 2.82, "Your order cost the firm $40,000 a day. About $14 million a year.",
           kind="flag", size=16)
D.cards2(s, y + 0.22, LIMIT - (y + 0.22) + 0.28, [
    (BLUE, "Revenue did not change", "Still 70,000 chips at $10. Still $700,000 a day."),
    (RED, "Cost did", "$575,000 across two plants became $615,000 in one."),
])
D.notes(s, """The reveal. Let it land before explaining it.

Revenue is identical — 70,000 chips at $10 either way. So the entire difference is cost:
$575,000 when the two plants split the work, $615,000 when the new plant does all of it.
$40,000 a day, roughly $14 million over a working year.

And remember that this is AFTER the firm stopped paying the old plant's $100,000 a day of
fixed costs. Closing the plant saved real money and the decision still destroyed value.

Do not explain why yet. Ask the room why first — someone will get close, and the sentence
you are fishing for is "the new plant had to be pushed past the point where it was
efficient."

A number worth saying exactly: $40,000 a day. Not "about forty thousand".""")

# =============================================== 27. Exhibit 7.7 enforced schedule
s = S()
D.title(s, "Exhibit 7.7 — The Same Plant, Two Orders")
D.picture_fit(s, F % "enforced", 0.60, 1.10, 8.80, 3.20)
D.kicker(s, "Push a plant past MC = P and every extra chip costs more than it sells for.",
         y=4.46)
D.notes(s, """Exhibit 7.7, redrawn.

Both panels are the same plant and the same cost curves. Only the quantity changes.

Panel (a): the manager's own choice, 50,000 chips, where marginal cost equals the $10
price. Average total cost $7.50, so costs $375,000 and profit $125,000.

Panel (b): 70,000 chips, as ordered. Average total cost rises to $8.79, so cost is
$615,000. Profit falls to $85,000. And look at the marginal cost point: the 70,000th chip
costs $14 to make and sells for $10.

That last chip is the argument in miniature. Every chip between 50,000 and 70,000 was made
at a marginal cost above $10 in a plant that had run out of cheap capacity, when the old
plant could have made those same chips at $10.

An honesty note for you, not for the slide. The textbook's version of this exhibit puts
average total cost at 70,000 at $22.50 and the loss at $875,000. Those numbers cannot come
from the marginal cost curve drawn beside them — if marginal cost is $10 at 50,000 and
about $30 at 70,000, the extra 20,000 chips cannot cost more than $600,000, so average
total cost cannot exceed about $14. Our figures come from an explicit cost function and
close exactly. If a student is revising from the publisher's deck and asks why the numbers
differ, tell them the direction of the result is identical and ours is the one that
adds up.""")

# ================================================================ 28. the 70,000th chip
s = S()
D.title(s, "The 70,000th Chip")
y = D.band(s, 1.15, "In the new plant it costs $14 to make.   In the old plant it costs "
                    "$10.   It sells for $10.", kind="formula", size=15)
D.cards3(s, y + 0.24, LIMIT - (y + 0.24), [
    (RED, "Made in the new plant", "Costs $14, sells for $10. Every chip like it destroys "
     "$4 of value.", IC % "factory"),
    (GREEN, "Made in the old plant", "Costs $10, sells for $10. Breaks even — which is "
     "exactly what a marginal unit should do.", IC % "hard-hat"),
    (BLUE, "The rule underneath", "Cost is minimised when marginal cost is the same "
     "everywhere. Not average cost. Marginal cost.", IC % "balance-scale"),
])
D.kicker(s, "“Which plant is better?” is the wrong question. “Where should "
            "the next chip be made?” is the right one.", y=4.44)
D.notes(s, """The explanation. This is the slide students should photograph.

Walk it one sentence at a time.

The new plant is better on average. It is not better at the margin once you push it to
70,000, because its marginal cost curve slopes up and by 70,000 it has climbed to $14.

Meanwhile the old plant, sitting idle, could have made that chip for $10.

So the firm paid $14 for something it could have had for $10. Do that twenty thousand
times and you have your $40,000.

The general principle, and say it as a rule they can use anywhere: to produce any given
total at least cost, allocate output so that marginal cost is equal across every source.
Not equal average cost. Equal marginal cost. Students confuse these constantly.

Sanity check to offer: if marginal costs were unequal, you could always move one unit from
the high-MC source to the low-MC one and save the difference. The only place with no such
move left is where they are equal. That is an argument, not an assertion, and it takes ten
seconds.""")

# ================================================== 29. every possible split priced
s = S()
D.title(s, "Every Possible Split, Priced")
D.picture_fit(s, F % "split_cost", 0.60, 1.12, 8.80, 3.10)
D.kicker(s, "The cheapest way to make 70,000 chips is the one the two managers found on "
            "their own.", y=4.44)
D.notes(s, """An extension figure - not in the publisher's deck, and worth the minute it
costs.

The horizontal axis is how many of the 70,000 chips are made at the old plant; the rest go
to the new one. The vertical axis is what the whole 70,000 then costs.

The curve has one minimum, at 20,000 chips in the old plant, and it costs $575,000. That
is exactly the split the two independent managers arrived at, each looking only at their
own plant and neither knowing the other existed.

The red dot on the left is the CEO's order — nothing in the old plant, everything in the
new one — at $615,000, already crediting the closure with the old plant's saved fixed
cost.

The point to land: the invisible hand is not only a story about markets between firms. It
runs inside a firm too, whenever independent units respond to the same price. Head office
did not have more information than the managers; it had less, because it was not looking
at marginal costs.

If someone asks whether real firms should therefore never centralise: no — this result
depends on both plants facing the same true price and having no reason to misreport. That
is a genuinely open question in organisational economics and it is a good thing to say
you cannot settle in an intro course.""")

# ====================================================== 30. the hand inside the firm
s = S()
D.title(s, "The Invisible Hand Inside the Firm")
y = D.defbox(s, 1.15,
             "Two managers, each maximising their own plant's profit, minimised the "
             "firm's total cost — without being asked to, and without talking to "
             "each other.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "What coordinated them", "The price. Both faced $10, both set marginal cost to "
     "$10, so marginal costs matched.", IC % "price-tag"),
    (RED, "What broke it", "An instruction that overrode the price signal with something "
     "that felt sensible.", IC % "manager"),
    (GREEN, "The general form", "Whenever independent units face the same price, "
     "self-interest equalises marginal cost — which is the condition for least-cost "
     "production.", IC % "exchange"),
])
D.kicker(s, "Same result as Part 1, one scale up.", y=4.52)
D.notes(s, """The Part 2 summary.

Draw the parallel with Part 1 explicitly, because it is the architecture of the whole
chapter: in Part 1 individual buyers and sellers, each acting alone, maximised social
surplus. In Part 2 individual plant managers, each acting alone, minimised the firm's
costs. Same mechanism, one level up.

The middle card is the one to dwell on. The CEO's instruction was not stupid and it was
not malicious. It was a reasonable-sounding rule that replaced a price signal with a
judgement. That is what central direction does, and it is the bridge to Part 4.

Close with the question for Part 3: we have coordinated people inside a market, and plants
inside a firm. Can the same mechanism decide how much of the economy's resources go to
paper delivery and how much to trucking? Nobody is in charge of that either.""")

# ============================================================= 31. PART 3 divider
s = S()
D.divider(s, "PART 3", "Across Industries")
D.notes(s, """Section divider - Part 3, Pearson section 7.3.

Scale changes again. Now the question is not who produces within a market or within a
firm, but how many firms an industry should have at all — and how that gets decided when
nobody decides it.

The mechanism is entry and exit, which they met at the end of Chapter 6. This section
turns it into the resource-allocation story.""")

# ============================================================ 32. the three steps
s = S()
D.title(s, "The Three Steps, One More Time")
y = D.band(s, 1.15, "1. Find q where MR = MC   ·   2. Read ATC at that q   ·   "
                    "3. Compare P with ATC", kind="formula", size=15)
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (GREEN, "P > ATC", "Economic profit. The industry is paying better than the "
     "alternatives, and outsiders can see it.", IC % "coin-stack"),
    (RED, "P < ATC", "Economic loss. Resources here are earning less than they would "
     "elsewhere.", IC % "receipt"),
    (BLUE, "P = ATC", "Break-even. Nothing pulls anyone in and nothing pushes anyone out.",
     IC % "balance-scale"),
])
D.kicker(s, "Economic profit is not a reward. It is a signal, and everyone can read it.",
         y=4.42)
D.notes(s, """Recall from Chapter 6, one slide, no more.

The only new emphasis is the kicker. In Chapter 6 economic profit was an outcome — the
answer to "am I making money?". In Chapter 7 it is an input — a message to everyone
outside the industry saying "resources are underemployed here, come and get some."

That reframing is the whole of Part 3. Say it before the diagrams arrive, so the diagrams
confirm something they have already heard rather than introducing it.

Reminder to state: economic profit is measured after opportunity cost, so P = ATC means
the owners are doing exactly as well as their next best option. That is why zero economic
profit is a stable resting point rather than a crisis.""")

# ================================================= 33. Exhibit 7.9 profit
s = S()
D.title(s, "Exhibit 7.9 — Economic Profit in Paper Delivery")
D.picture_fit(s, F % "paper_profit", 0.60, 1.10, 8.80, 3.04)
y = D.band(s, 4.20, "q = 60 tons a day · price $18 · ATC $13 · profit $300 a day, "
                    "per firm", kind="answer", size=13.5)
D.notes(s, """Exhibit 7.9, redrawn as a firm in a profitable industry.

Walk the three steps on the picture so the method becomes muscle memory.

Step 1: MC crosses the $18 price line at 60 tons a day. That is the quantity.
Step 2: read up to the ATC curve at 60 — average total cost is $13.
Step 3: $18 is above $13, so there is profit: $5 a ton on 60 tons, $300 a day.

Every one of those numbers is exact. The firm's total cost is 240 + 0.15q², which gives a
minimum average total cost of $12 at 40 tons, and $13 at 60 tons.

Now the question that opens the next slide: this firm is making $300 a day. Who else can
see that, and what will they do about it?

A student may notice the profit rectangle is not at the minimum of ATC. Correct, and
important: firms maximise profit, not minimise average cost. Producing at minimum ATC
would mean giving up profitable units.""")

# ============================================== 34. Exhibit 7.10 entry
s = S()
D.title(s, "Exhibit 7.10 — Entry, and What It Does to the Price")
D.picture_fit(s, F % "entry", 0.60, 1.10, 8.80, 3.06)
D.credit(s, "Note for anyone comparing with the textbook figure: entry adds firms, so "
            "market supply shifts RIGHT and the price falls. Some printings of this "
            "exhibit draw the shift the other way.", y=4.28)
D.kicker(s, "Entry does not stop when the newcomers arrive. It stops when the profit "
            "does.", y=4.62)
D.notes(s, """Exhibit 7.10, redrawn - and one of the flags of this chapter.

Panel (a), the market: more firms means more supply at every price, so the supply curve
shifts RIGHT, from S1 to S2, and the price falls from $18 to $12.

Panel (b), the firm: as the price falls the profit rectangle shrinks. At $12 it has
vanished — price equals minimum average total cost, and the firm produces 40 tons instead
of 60.

THE ERROR: the version of Exhibit 7.10 in the publisher's slide deck draws S2 to the LEFT
of S1 on a slide titled "Firm Entry and Its Effect on the Market" — a leftward shift is
exit. The deck actually ships a corrected duplicate of the same exhibit a slide later,
with a note from its own author saying so. Teach the right one; if a student's copy shows
the arrow pointing left, that is the reason.

Numbers, if wanted: the industry goes from 14,000 firms at $18 to 24,000 firms at $12, and
market output rises from 840 to 960 thousand tons a day. Each firm shrinks while the
industry grows — that is worth one sentence, because it surprises people.""")

# ============================================== 35. Exhibit 7.11 loss
s = S()
D.title(s, "Exhibit 7.11 — And an Industry Losing Money")
D.picture_fit(s, F % "trucking_loss", 0.60, 1.10, 8.80, 3.04)
y = D.band(s, 4.20, "q = 30 ton-miles a day · price $9 · ATC $12.50 · loss $105 a day, "
                    "per firm", kind="flag", size=13.5)
D.notes(s, """Exhibit 7.11 - the mirror of Exhibit 7.9.

Same three steps, opposite answer. Marginal cost meets the $9 price at 30 ton-miles;
average total cost there is $12.50; price is below cost, so the firm loses $3.50 a
ton-mile, $105 a day.

Two questions to head off:

"Why is it operating at all?" Because this is a short-run picture and, as long as price
covers average VARIABLE cost, shutting down would lose more. That is Chapter 6's shutdown
rule, and it is worth ten seconds of recall.

"Why doesn't it just produce less?" Because 30 is the loss-MINIMISING quantity. Producing
less would forgo units whose revenue exceeds their marginal cost. Students find this
counterintuitive every year.

The long-run answer is on the next slide: it does not produce less, it leaves.""")

# ============================================== 36. Exhibit 7.12 exit
s = S()
D.title(s, "Exhibit 7.12 — Exit, and the Same Mechanism Backwards")
D.picture_fit(s, F % "exit", 0.60, 1.10, 8.80, 3.06)
D.kicker(s, "Firms leaving is not the market breaking. It is the market moving resources "
            "somewhere they are worth more.", y=4.44)
D.notes(s, """Exhibit 7.12.

Panel (a): firms leave, so supply shifts LEFT from S1 to S2 and the price RISES, from $9
to $12. Panel (b): the loss rectangle shrinks and disappears at $12.

The exit industry runs from 34,000 firms down to 24,000. Note that it lands on the same
$12 and the same 40-ton firm as the entry industry did, because both are using the same
cost technology. That is deliberate — it makes the point that the resting place is a
property of the technology, not of where you started.

The sentence that makes this Part 3 rather than Chapter 6 revision: the trucks, the
drivers and the capital that left this industry did not evaporate. They went to industries
where the return was higher — perhaps to paper delivery, where profits were attracting
entry. That is the cross-industry reallocation, and nobody organised it.

Ask: who decided that the economy needed fewer trucking firms and more paper delivery
firms? Nobody did. The prices did.""")

# ============================================================= 37. where it stops
s = S()
D.title(s, "Where It Stops")
D.picture_fit(s, F % "longrun", 0.60, 1.10, 8.80, 2.98)
y = D.band(s, 4.14, "Long-run equilibrium: P = MC = minimum ATC, and economic profit is "
                    "zero in every industry at once.", kind="formula", size=14)
D.notes(s, """The resting point.

Entry stops when profit reaches zero. Exit stops when losses reach zero. Both roads lead
to the same place: price equal to the minimum of average total cost.

Three consequences to state, because each is examinable:

One - the price ends up at the lowest average cost the technology allows. Consumers get
the good at the cheapest sustainable price. Nobody arranged that.

Two - each firm produces at the bottom of its ATC curve, which is the most cost-effective
scale. Nobody arranged that either.

Three - economic profit is zero everywhere, which means no industry is offering a better
return than any other. That is what "resources are allocated to their highest-value use"
actually means, stated as a condition you can check.

The picture is worth one more sentence: notice this is where MC crosses ATC, which
Chapter 6 established is always the minimum of ATC. Nothing new is being assumed.""")

# ================================================== 38. zero economic profit again
s = S()
D.title(s, "Zero Economic Profit Is Not Zero Profit")
y = D.defbox(s, 1.15,
             "Economic profit is measured after subtracting what the owners' money and "
             "time could have earned somewhere else.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (RED, "What it does not mean", "That the firm is failing, or that the owners take "
     "nothing home. Accounting profit can be large while economic profit is zero.",
     IC % "receipt"),
    (GREEN, "What it does mean", "That this industry pays exactly what the next-best use "
     "of the same resources pays. No reason to move.", IC % "balance-scale"),
    (BLUE, "Why it is the resting point", "Anything above it pulls firms in until it is "
     "gone; anything below it pushes firms out until it is gone.", IC % "exchange"),
])
D.kicker(s, "The single most misread result in the whole course. Say it back to yourself "
            "before the exam.", y=4.50)
D.notes(s, """The most misread result in the chapter, and it comes up every year.

Make it concrete with a number. Suppose you put $500,000 into a paper delivery firm and it
returns $40,000 a year, while the same money in an index fund would have returned $40,000.
Accounting profit: $40,000. Economic profit: zero. You are doing fine. You have no reason
to move your money, and no reason to move it out.

That is what long-run equilibrium looks like from the inside. It is not an industry on
life support; it is an industry that has stopped being unusual.

Give them the exam warning explicitly: a question that says "in long-run competitive
equilibrium, firms earn zero economic profit" is not saying firms earn nothing. Students
lose marks on this every term.""")

# ============================================= 39. entry and exit are the market working
s = S()
D.title(s, "Entry and Exit Are the Market Working")
D.cards2(s, 1.15, 1.60, [
    (GREEN, "Profits attract",
     "A profitable industry is one where resources are earning more than they could "
     "elsewhere. Entry is the economy noticing and responding."),
    (RED, "Losses repel",
     "A loss-making industry is one where resources are earning less than they could "
     "elsewhere. Exit is the same mechanism running the other way."),
])
y = D.band(s, 2.98, "Free entry and free exit are what make the reallocation possible. "
                    "Block either one and the mechanism stops.", kind="note", size=14)
D.kicker(s, "Firms closing is uncomfortable. It is also how the economy stops wasting "
            "things.", y=4.48)
D.notes(s, """The Part 3 summary, and a place to be honest.

The economics is clean: entry and exit move capital and labour toward their highest-value
uses, and free entry and exit are the necessary condition. Say the condition out loud —
licensing, patents, capital requirements and network effects all restrict entry, and all
of them break this result to some degree. Chapter 8 onwards.

Then the honest part, and do not skip it: "resources reallocate" is a phrase that hides
people losing jobs, towns losing employers, and skills becoming worthless. The model is
about the size of the pie. It says nothing about who bears the cost of the transition, and
the answer is usually not the people who captured the gains.

That is not a criticism of the model — it is the boundary of it, and it is the second time
today we have hit that boundary. Part 5 is where we stop working around it.""")

# ============================================================= 40. PART 4 divider
s = S()
D.divider(s, "PART 4", "Prices Guide\nthe Invisible Hand")
D.notes(s, """Section divider - Part 4, Pearson section 7.4.

Everything so far has run on prices without saying much about them. This part makes the
price itself the object of study: what information it carries, what happens when it is
allowed to move, and what happens when it is not.

This is also the part with the live material in it.""")

# ============================================================ 41. a price is a message
s = S()
D.title(s, "A Price Is a Message")
y = D.defbox(s, 1.15,
             "A price is the shortest possible summary of everything anyone knows about "
             "how scarce something is and how badly it is wanted.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "To buyers it says", "Here is what this costs society to give you. Take it "
     "only if it is worth that much to you.", IC % "shopping-cart"),
    (RED, "To sellers it says", "Here is what people will give up for this. Make it only "
     "if you can do so for less.", IC % "factory"),
    (GREEN, "To everyone else it says", "There is money to be made here, or there is not. "
     "Come, or go.", IC % "exchange"),
])
D.kicker(s, "Nobody has to understand the message. They only have to respond to it.",
         y=4.50)
D.notes(s, """The conceptual heart of Part 4.

The idea to convey: a price is an extraordinary act of compression. When the price of
copper rises, every user of copper economises on it, and not one of them needs to know
whether a mine flooded in Chile or a new use was found in China. The number is enough.

That is Hayek's argument, and it is worth naming him even in an intro course, because it
is the strongest version of the case for markets and it is not the same as the efficiency
argument we proved in Part 1. Part 1 said the outcome is good given the information. This
says the price system economises on the information anyone needs to have.

The three cards are the three audiences. Point at each and read it.

Then the transition: if the price is the message, what happens when we stop it from
changing? That is the rest of Part 4.""")

# =========================================================== 42. the parking meter
s = S()
D.title(s, "What Is a Parking Meter For?")
y = D.defbox(s, 1.15, "Take thirty seconds. Why does a city put a price on kerb space?",
             tint=TINT_GOLD, border=DGOLD, color=DGOLD)
D.cards3(s, y + 0.28, LIMIT - (y + 0.28), [
    (GREY, "“To raise money”", "Meter and fine revenue is a small share of a "
     "city budget, and a good deal of it goes on enforcement.", IC % "coin-stack"),
    (GREY, "“To stop people parking”", "But a city wants its kerb used. Empty "
     "spaces on a busy street are a waste, not a success.", IC % "house"),
    (BLUE, "The economic answer", "To allocate a scarce thing to whoever values it most "
     "right now — and to make sure a space is free when someone needs one.",
     IC % "price-tag"),
])
D.kicker(s, "The meter is not a tax on parking. It is a price for parking.", y=4.44)
D.notes(s, """Pearson's live-classroom question, adapted for a recorded lecture.

Pause the recording here. Ask the question, wait, then take the two wrong-ish answers
before revealing the third.

The revenue answer is the one most students give and it is empirically weak — parking
revenue is a minor line in a city budget and enforcement eats into it.

The real function is allocation. Kerb space in a busy district is genuinely scarce, and
without a price it is rationed by who is willing to drive around the longest looking. That
is rationing by waiting, and the waiting is pure waste — nobody receives it. The driver
burns fuel and time and hands the value to no one.

With a price, the space goes to whoever values it most at that moment, and the money at
least goes somewhere.

Then the natural objection, which you should raise yourself: does this actually work, or
is it just a story? Next slide.""")

# =========================================================== 43. SFpark
s = S()
D.title(s, "San Francisco Priced Its Kerb, and Measured What Happened")
D.picture_fit(s, F % "sfpark", 0.60, 1.10, 8.80, 2.96)
D.credit(s, "SFpark pilot, launched April 2011; SFMTA evaluation published 19 June 2014. "
            "Meter prices adjusted periodically by block and time of day to hold "
            "occupancy between 60% and 80%.", y=4.14)
D.kicker(s, "Prices went down, availability went up. Rationing by price beat rationing "
            "by circling.", y=4.42)
D.notes(s, """The evidence, and it is unusually clean.

San Francisco ran a demand-responsive pricing pilot: instead of one meter rate everywhere,
rates moved up on blocks that were always full and down on blocks that were always empty,
aiming to keep roughly one space free per block.

The results from the SFMTA's own evaluation: the time drivers spent searching for a space
fell 43%; the driving-around-looking and its emissions fell 30%; citations fell 23%. And
here is the part that surprises people — the average meter rate FELL 4% and the average
garage rate fell 12%. Prices went down on average because most blocks were over-priced
relative to demand; only the busiest ones went up.

The lesson to land: "letting the price move" is not a synonym for "raising the price". It
means letting the number carry information. Where demand was low the information was that
the price was too high.

One honest caveat, and say it: this was a pilot with an evaluation run by the agency that
implemented it, and later academic work has questioned how much of the gain came from the
pricing rule versus better real-time information for drivers. The direction of the result
is not seriously disputed; the exact magnitudes are.""")

# ================================================= 44. Exhibit 7.14 demand shift
s = S()
D.title(s, "Exhibit 7.14 — A Storm Is Coming")
D.picture_fit(s, F % "water_shift", 0.60, 1.10, 8.80, 3.00)
y = D.band(s, 4.16, "Demand shifts right · the price rises from $30 to $40 · quantity "
                    "traded rises from 60 to 80 cases", kind="formula", size=13.5)
D.notes(s, """Exhibit 7.14. Bottled water before a storm.

This is Chapter 4 machinery and it should take ninety seconds. A hurricane warning goes
out; demand for bottled water, plywood, ice and generators jumps; the demand curve shifts
right; the price rises.

What to point at, because it is the bit students skip: quantity traded ALSO rises, from 60
to 80. The higher price is not just a transfer from buyers to sellers. It is the
instruction that brings the extra 20 cases into the market — someone drove a truck through
the night because $40 made it worth doing.

Numbers, exact: supply is Qs = 2P, demand shifts from Qd = 90 − P to Qd = 120 − P.
Equilibrium moves from ($30, 60) to ($40, 80).

Hold the moral judgement for two slides. Right now this is a description, not a defence.""")

# ================================================ 45. Exhibit 7.15 shortage
s = S()
D.title(s, "Exhibit 7.15 — Hold the Price Instead")
D.picture_fit(s, F % "water_shortage", 0.60, 1.10, 8.80, 3.00)
y = D.band(s, 4.16, "At $30: 60 cases arrive, 90 are wanted. The 30-case gap is not "
                    "filled by anything.", kind="flag", size=13.5)
D.notes(s, """Exhibit 7.15. The same storm, with the price held at $30.

Demand still shifts. Supply still slopes up. But the price is not allowed to move, so the
quantity supplied stays at 60 while quantity demanded goes to 90.

Thirty cases of shortage. And the crucial question to ask the room: who gets the 60 cases
that do exist?

Not the people who need them most — the price is no longer sorting anyone. They go to
whoever arrives first, whoever lives nearest, whoever can queue longest, whoever knows the
shop owner. Those are real allocation rules and none of them is "whoever values water
most".

Say the phrase that makes this stick: the shortage does not eliminate rationing. It
changes who does the rationing, from the price to the queue — and unlike a price, the
queue's cost is paid and received by nobody.

Do not moralise yet. The equity argument is coming in four slides and it deserves a fair
hearing.""")

# ======================================= 46. price controls restrict efficiency (photo)
s = S()
D.title(s, "Price Controls Restrict Efficiency")
px, py, pw, ph = D.photo(s, PH % "efficiency_bars", 0.60, 1.15, 3.55, 2.90)
D.textbox(s, 4.55, 1.20, 4.85, 1.00,
          "If the price cannot move, it cannot carry information — and everything the "
          "invisible hand does, it does through the price.",
          size=14.5, bold=True, color=BLUE, line_pct=1.24)
D.rect(s, 4.55, 2.32, 4.85, 0.06, fill=GOLD)
D.cards2(s, 2.52, 1.90, [
    (RED, "What is blocked", "Sellers do not learn that supply is short. Buyers do not "
     "learn to economise. Nobody outside learns to come and help."),
    (RED, "What appears instead", "A shortage, a queue, and an allocation nobody chose "
     "and nobody can defend on efficiency grounds."),
], xs=(4.55, 7.05), width=2.35)
D.image_credit(s)
D.notes(s, """The conceptual bridge between the shortage diagram and the deadweight-loss
measurement.

One idea: a price control does not just move money around. It disables the signalling
system. Everything in Parts 1, 2 and 3 ran through the price, so if the price is frozen,
all three mechanisms stop at once.

Worth making concrete with the three levels we have already done:
- Within the market, high-value buyers no longer outbid low-value ones.
- Within a firm, plants no longer know where to put the next unit.
- Across industries, nobody learns that this is where resources are needed.

Then set up the measurement: we have said "less efficient" three times now. On the next
two slides we put a number on it.""")

# ============================================================ 47. deadweight loss
s = S()
D.title(s, "Deadweight Loss")
y = D.defbox(s, 1.15,
             "Deadweight loss — the social surplus that a market intervention destroys. "
             "Not transferred to anyone. Destroyed.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "A transfer", "A price cap moves money from sellers to the buyers who still "
     "get the good. Somebody loses, somebody gains, and the total is unchanged.",
     IC % "exchange"),
    (RED, "A deadweight loss", "The trades that no longer happen at all. The buyer's gain "
     "and the seller's gain both vanish. Nobody picks them up.", IC % "receipt"),
    (GREEN, "You already met one", "The $20 in the capped phone market. Sean's trade with "
     "Jeff. Same idea, now with a name.", IC % "lightbulb"),
])
D.kicker(s, "Ask of any policy: how much is a transfer, and how much simply disappears?",
         y=4.50)
D.notes(s, """The definition, and the distinction students most need.

Transfers and deadweight losses are completely different animals and they get conflated
constantly, including in public debate.

A transfer is a distributional question: sellers lose $X, buyers gain $X, and reasonable
people can disagree about whether that is good. Economics has no special authority there.

A deadweight loss is not a distributional question. It is value that nobody has. There is
no one to argue on its behalf because nobody received it.

Point back at the third card. They computed a deadweight loss on slide 15 without knowing
the word, which is the right order to learn it in.

Then set up the arithmetic: the next slide puts letters on the areas; the one after puts
a real statutory number on it.""")

# ============================================= 48. Exhibit 7.16 lettered
s = S()
D.title(s, "Exhibit 7.16 — Where the Surplus Goes")
D.picture_fit(s, F % "dwl_letters", 0.60, 1.10, 8.80, 3.10)
D.kicker(s, "A + B = $4,800.  C + E = $4,653.  D = $147, and it belongs to nobody.",
         y=4.42)
D.notes(s, """Exhibit 7.16, redrawn with the publisher's lettering so students can match
it to the textbook.

Panel (a), free market: consumer surplus is A, producer surplus is B, and A + B is the
whole social surplus — $4,800 an hour in this market.

Panel (b), with a ceiling: consumer surplus is C, producer surplus is E. C is not simply
smaller than A — part of it is the rectangle taken from sellers and handed to the buyers
who still get water. That part is a transfer.

D is the triangle, and D is the deadweight loss: $147. It is the surplus from the 14 cases
that would have been traded and now are not. Nobody has it.

Two things students get wrong here:

Consumer surplus can RISE under a price ceiling. Buyers who still get the good pay less.
That is why price controls are popular, and it is a real gain to real people — do not
pretend otherwise.

Producer surplus falls unambiguously. Sellers lose the transfer and the lost trades.

The next slide says where the $147 and the ceiling price came from, and the answer is not
hypothetical.""")

# ==================================================== 49. Texas, live
s = S()
D.title(s, "The Statute Switches On: Texas, July 2026")
y = D.defbox(s, 1.15,
             "A price ceiling is not usually a permanent law. It is a rule that activates "
             "the moment a disaster is declared — exactly when demand jumps.",
             tint=TINT_GOLD, border=DGOLD, color=DGOLD)
D.cards3(s, y + 0.26, 4.30 - (y + 0.26), [
    (RED, "The trigger", "Floods hit the Texas Hill Country again in July 2026, a year "
     "after the 2025 disaster. A state of disaster was declared.", IC % "house"),
    (BLUE, "The rule", "Texas law makes it illegal to charge an exorbitant or excessive "
     "price for necessities during a declared disaster. The Attorney General enforces it.",
     IC % "ballot-box"),
    (DGOLD, "The goods", "Water, food, fuel, lodging, repairs — the same list as our "
     "diagram, and the same moment the demand curve jumps right.", IC % "gas-pump"),
])
D.credit(s, "Texas Attorney General consumer alert on flood-related scams and price "
            "gouging, 17 July 2026. Figures and enforcement status are live — re-check "
            "before delivery.", y=4.38)
D.kicker(s, "This is Exhibit 7.15, in a statute, in force right now.", y=4.62)
D.notes(s, """A live example. Re-check it the morning you record.

The point of this slide is not to take a side. It is to show that the diagram two slides
back is not a classroom abstraction — anti-gouging statutes exist in most US states and
they bind precisely when the demand curve shifts right, which is the only time they could
possibly bite.

Say what the statute does and does not do. Texas's rule prohibits an "exorbitant or
excessive" price during a declared disaster; it does not name a number, which makes it
vaguer than New York's rule on the next slide and correspondingly harder to model.

Handling note: floods in the Hill Country killed people in 2025 and again in 2026. Keep
the register analytical and brief. Do not use the death toll as a rhetorical device in
either direction, and do not editorialise about the law. Present the mechanism, then the
evidence, then let students argue.

Re-check before recording: whether any enforcement actions have been announced, and
whether the disaster declaration is still active.""")

# ==================================================== 50. New York's 10 per cent
s = S()
D.title(s, "New York Wrote Down a Number: 10%")
D.picture_fit(s, F % "ten_percent", 0.60, 1.06, 5.55, 3.20)
D.textbox(s, 6.35, 1.12, 3.05, 1.30,
          "New York adopted price-gouging rules on 28 January 2026. A rise of more than "
          "10% during an abnormal market disruption is presumed to be an unconscionably "
          "excessive price.", size=11.5, bold=True, color=BLUE, line_pct=1.26)
D.rect(s, 6.35, 2.56, 3.05, 0.06, fill=GOLD)
D.textbox(s, 6.35, 2.74, 3.05, 1.50,
          "Put that on our storm: $30 × 1.10 = $33. The market wanted $40. Result — "
          "66 cases traded instead of 80, 21 buyers left short, and $147 an hour of "
          "surplus destroyed.", size=11.5, color=INK, line_pct=1.26)
D.credit(s, "New York State Attorney General, final price-gouging rules adopted 28 "
            "January 2026, including the 10% gross-disparity threshold. The threshold "
            "creates a rebuttable presumption, not an absolute cap: a seller can rebut it "
            "by showing its own costs rose. Live — re-check before delivery.", y=4.56)
D.notes(s, """The best slide in Part 4, because the number is real and the arithmetic
closes.

Numbers to read, not recall: pre-storm price $30. Statutory threshold 10%, so $33. The
market-clearing price after the demand shift is $40. At $33 the quantity supplied is 66
cases; quantity demanded is 87; so 21 cases short. Trades fall from 80 to 66, and the
deadweight loss triangle is one half times 14 cases times $21, which is exactly $147 an
hour.

Now the honesty, and this matters more than the arithmetic:

The 10% figure creates a rebuttable PRESUMPTION, not a hard ceiling. A seller whose own
wholesale costs rose can charge more and defend it. So the true constraint is looser than
the one we have drawn, and our $147 is an upper bound on what this particular rule would
cost in this particular market. Say that on camera.

Also worth saying: the rule was adopted with a package of others — definitions of unfair
leverage, a 30% market-share presumption, a concentration threshold — so it is aimed
mainly at sellers with market power, not at the corner shop. That is a more sophisticated
piece of drafting than the classroom price-ceiling story usually allows for.

If a student asks whether the rule is a good idea: that is the next slide, and the answer
is that it depends on something the model cannot measure.""")

# =========================================================== 51. the case on the other side
s = S()
D.title(s, "The Case on the Other Side")
D.cards2(s, 1.15, 1.72, [
    (BLUE, "The argument for the ceiling",
     "In a disaster, willingness to pay tracks ability to pay. Letting the price clear the "
     "market allocates water to the richest, not the thirstiest. A queue is a worse "
     "allocator than a price in normal times and arguably a better one here."),
    (RED, "The argument against",
     "The high price is what brings the extra water in. Cap it and the trucks do not come, "
     "so the shortage is deeper and lasts longer — and the people who lose most are the "
     "ones without the time to queue."),
])
y = D.band(s, 3.08,
           "One study of US state anti-gouging rules during 2020 found they were "
           "associated with more shopping trips and more in-store contact — consistent "
           "with shortages sending people from shop to shop.",
           kind="note", size=12.5)
D.credit(s, "Chakraborti & Roberts, “How price-gouging regulation undermined "
            "COVID-19 mitigation”, Public Choice 196 (2023). One study, one episode "
            "— not a settled literature.", y=4.62)
D.notes(s, """Give both sides properly. This is the slide where you are most likely to be
accused of having an agenda, so be visibly even-handed.

The equity argument is not weak and should not be presented as a naive objection. Social
surplus counts a dollar of willingness to pay identically whoever holds it, and in an
emergency that is a genuinely contestable way to count. A person who cannot afford $40
water is not revealing that they value it less.

The efficiency argument is also not weak. The supply response is the entire mechanism, and
suppressing it makes the shortage worse for everyone including the poor.

On the study: one paper, one episode, an indirect outcome measure — contacts inferred from
phone location data rather than shortages measured directly. Cite it as evidence, not as
proof, and say so. If a student wants the other side of the literature, there is work
finding anti-gouging rules speed recovery in some settings; the honest summary is that the
empirical question is not settled.

Land it here: the model tells you the size of the efficiency cost. It cannot tell you
whether that cost is worth paying. That is a value judgement, and Part 5 is about
admitting it.""")

# ============================================= 52. two problems any economy has to solve
s = S()
D.title(s, "Two Problems Any Economy Has to Solve")
D.cards2(s, 1.15, 1.68, [
    (BLUE, "The coordination problem",
     "Getting millions of self-interested strangers to form markets at all — to find each "
     "other, agree what to trade, and settle on terms. Nobody has a list of who wants "
     "what."),
    (RED, "The incentive problem",
     "Getting them to actually do the thing once the market exists — to show up, produce, "
     "and not shirk, when nobody is watching closely enough to check."),
])
y = D.band(s, 3.06, "Prices solve both at once. That is why they are the answer to two "
                    "questions and not just one.", kind="formula", size=14)
D.kicker(s, "A system that solved only one of these would not work at all.", y=4.48)
D.notes(s, """The framing for the last stretch of Part 4.

Both problems are hard and it is worth making that felt. To coordinate an economy
centrally you would need to know every consumer's preferences, every firm's technology,
and every resource's location, and you would need it faster than any of them change. To
give incentives centrally you would need to monitor effort you cannot observe.

Prices do both simultaneously. The price tells you what to do (coordination) and paying
you the price makes you want to do it (incentive). That double duty is the thing to
underline — it is why the market answer is not simply "one of several ways to organise an
economy".

Then the honest counterweight, one sentence: markets solve these two problems well and
create others, which is what the rest of the course is about.

This slide also pays back the Adam Smith slide from the start of the hour: the butcher
does not need to be told and does not need to be supervised.""")

# ============================================================= 53. market or command
s = S()
D.title(s, "Two Ways to Answer Them")
D.cards2(s, 1.15, 1.75, [
    (GREEN, "Market economy",
     "Prices direct the flow of resources and provide the incentives to follow them. "
     "Information stays where it already is — with the people who have it — and nobody "
     "needs to collect it."),
    (RED, "Command economy",
     "A central agency directs resources and supplies incentives. It must first gather "
     "the information that prices would otherwise have summarised, and it must gather it "
     "faster than it goes stale."),
])
y = D.band(s, 3.12, "The two-plant CEO ran a command economy with two units in it, and "
                    "lost $40,000 a day.", kind="flag", size=14)
D.kicker(s, "Now imagine that problem with a million units.", y=4.48)
D.notes(s, """The comparison, and the callback.

Keep it analytical rather than ideological. The difference between the two columns is not
about motives; it is about where information sits and how much of it has to move.

The callback to Part 2 is the strongest thing on the slide, so make it explicit. The CEO
had exactly two production units, both inside his own company, both reporting to him, both
with their books open. He had better information than any central planner has ever had
about any industry. And he still got it wrong, by $40,000 a day, because he substituted a
sensible-sounding rule for a price.

Then the kicker: scale that to an economy of millions of products and hundreds of millions
of people, and every input's price depending on every other.

Fair-minded note if a student raises it: real economies are all mixtures, and some
functions — defence, public health, basic research — are directed centrally in every
country for reasons the next section starts to explain.""")

# ================================================= 54. the central planner (photograph)
s = S()
D.title(s, "The Central Planner")
px, py, pw, ph = D.photo(s, PH % "blue_light", 5.30, 1.12, 4.10, 2.85)
D.textbox(s, 0.60, 1.18, 4.35, 1.05,
          "Kmart's blue light special: a flashing light, a loudspeaker, and a discount "
          "that lasted fifteen minutes.", size=14.5, bold=True, color=BLUE, line_pct=1.24)
D.rect(s, 0.60, 2.36, 4.35, 0.06, fill=GOLD)
D.cards2(s, 2.56, 1.86, [
    (GREEN, "As designed", "A store manager, looking at their own overstocked shelves, "
     "decided what to discount and when."),
    (RED, "As centralised", "Head office chose the item, the discount and the hour — for "
     "every store in the country at once."),
], xs=(0.60, 2.82), width=2.12)
D.image_credit(s)
D.notes(s, """The publisher's illustration of central direction, handled carefully.

The story as they tell it: the blue light special began in 1965 as a store-level tool — a
manager with too many of something switched on the light and cleared it. Later the
corporate office took the decision over, running the same promotion on the same item at
the same time nationwide, and the results were worse.

What I can source and what I cannot, and this matters. The 1965 start, the loudspeaker
announcement, the discontinuation in the early 1990s and the revivals in 2001 and 2015 are
all well documented. The claim that centralising the decision CAUSED lower profits is not
something I can find a source for. So tell it as an illustration of the mechanism, not as
evidence for it, and do not put a figure on the damage.

The mechanism itself is exactly Part 2's, and that is the reason to tell it at all: the
local manager knew which shelves were full and head office did not. Substituting a
uniform rule for local information throws away the only thing the manager had.

Good question to leave hanging: what would head office have to have known to do this
well?""")

# ============================================================= 55. PART 5 divider
s = S()
D.divider(s, "PART 5", "Equity and Efficiency")
D.notes(s, """Section divider - Part 5, Pearson section 7.5.

Short section, and the most important twelve minutes of the hour for students who will
never take another economics course.

Everything so far has been positive economics — statements that can be checked. This
section is where we say clearly what the model does not decide, and hand that question
back.""")

# ==================================================== 56. equity (photograph)
s = S()
D.title(s, "Equity")
px, py, pw, ph = D.photo(s, PH % "equity_cartoon", 5.15, 1.15, 4.25, 2.80)
D.textbox(s, 0.60, 1.20, 4.25, 0.95,
          "Equity asks whether the distribution of resources across a society is fair.",
          size=15, bold=True, color=BLUE, line_pct=1.24)
D.rect(s, 0.60, 2.28, 4.25, 0.06, fill=GOLD)
D.cards2(s, 2.48, 1.92, [
    (GREEN, "Efficiency is positive", "It asks what IS. Given the curves, social surplus "
     "is $4,800 or it is not. You can check it."),
    (RED, "Equity is normative", "It asks what OUGHT to be. Nothing in the diagram "
     "answers it, and no amount of better data will."),
], xs=(0.60, 2.82), width=2.12)
D.image_credit(s)
D.notes(s, """Equity, and the positive/normative line.

Define equity and then be precise about what kind of question it is. This is the
distinction from Chapter 1 — positive versus normative — arriving where it finally has
teeth.

The sentence to say plainly: markets do not make judgements. A market has no opinion about
whether the person who got the water needed it. It allocates to willingness to pay, and
willingness to pay is partly a statement about preferences and partly a statement about
what is in your account.

Then the thing students most need to hear from an economist, said out loud: economics does
not have a technique for settling equity questions. It can tell you what a redistribution
costs in surplus. It cannot tell you whether to do it. Anyone who tells you the discipline
settles it is selling something.

The cartoon is the publisher's and it is a light touch after a heavy point. Use it, do not
labour it.""")

# ================================================== 57. efficient is not fair
s = S()
D.title(s, "Efficient Is Not the Same as Fair")
y = D.defbox(s, 1.15,
             "Every allocation on the frontier is efficient. The frontier does not tell "
             "you which point on it to want.")
D.cards3(s, y + 0.26, LIMIT - (y + 0.26), [
    (BLUE, "The trade-off is real", "Most ways of redistributing change behaviour, and "
     "changed behaviour costs surplus. Bigger pie, less equal slices — often, not "
     "always.", IC % "balance-scale"),
    (RED, "But not always", "Some inefficiencies fall hardest on the poor, so removing "
     "them raises both. Efficiency and equity are not automatically opposed.",
     IC % "exchange"),
    (GREEN, "What economics contributes", "The price of each option. It tells you what "
     "the choice costs. It does not tell you which to choose.", IC % "ledger"),
])
D.kicker(s, "One of the roles of government is to address efficient outcomes that we do "
            "not consider equitable.", y=4.44)
D.notes(s, """The trade-off, stated fairly in both directions.

The textbook frames this as a trade-off between making the pie as big as possible and
dividing it evenly, and that framing is standard and mostly right. But do not let the
middle card get lost, because a student who leaves thinking equity always costs efficiency
has learned something false.

Examples where both improve together, if you want one: removing a barrier to entry that
protects incumbents; funding education that credit constraints would otherwise ration by
parental wealth. Both raise total surplus AND spread it more evenly.

The third card is the professional position, and it is worth saying you hold it: an
economist's contribution to a distributional argument is the price tag, not the verdict.

Close the section by returning to the question from Part 4: the New York rule costs $147
an hour of surplus in our storm. Whether that is worth paying to keep water at $33 is not
an economics question. It is a question about what kind of society you want, and your vote
counts the same as mine.""")

# ================================================== 58. Maryland drew the line
s = S()
D.title(s, "Where One Legislature Drew the Line")
y = D.defbox(s, 1.12,
             "Maryland, April 2026: the first US state to ban personalised pricing on "
             "groceries — prices set for you, from your own data.",
             tint=TINT_GOLD, border=DGOLD, color=DGOLD)
D.cards3(s, y + 0.24, 4.34 - (y + 0.24), [
    (RED, "What it bans", "Setting a different price for a specific shopper based on that "
     "shopper's personal data, at large food retailers and delivery apps.",
     IC % "phone"),
    (GREEN, "What it protects", "Price changes driven by supply and demand, weather, "
     "energy costs — and ordinary discounts and loyalty offers.", IC % "price-tag"),
    (BLUE, "Why that is interesting", "The line drawn is exactly the line this chapter "
     "draws: a price that carries information about scarcity does work. A price that "
     "only sorts by what you will tolerate does not.", IC % "lightbulb"),
])
D.credit(s, "Maryland HB 895, signed 28 April 2026, effective 1 October 2026. Applies to "
            "large grocery retailers and third-party delivery providers; the "
            "supply-and-demand exemption is written into the statute. Live — re-check "
            "before delivery.", y=4.44)
D.notes(s, """The most sophisticated slide in the deck, and worth the time.

The story: dynamic pricing has become politically contentious, and in April 2026 Maryland
became the first state to legislate against a specific form of it. The law is narrow — it
covers large grocers and delivery apps, and only tax-exempt food.

Here is why it belongs in this chapter. The legislature did not ban prices from moving. It
explicitly carved out changes driven by supply and demand, weather, and energy costs. What
it banned is a price computed from YOUR data, for YOU.

That is a remarkably clean statement of the distinction this whole chapter rests on. A
price that moves with scarcity is a message about the world, and it does allocative work —
it brings the trucks. A price computed from your browsing history carries no information
about scarcity at all; it just moves surplus from you to the seller.

Be careful not to overstate two things:
- The economics of price discrimination is genuinely more complicated than "it just
  transfers surplus". It can expand output and serve customers who would otherwise be
  priced out. Chapter 10 territory; flag it, do not resolve it.
- Whether the law will work as drafted is untested. It takes effect on 1 October 2026,
  after this course ends.

Re-check before delivery: whether the effective date holds and whether other states have
followed.""")

# =========================================== 59. so does Uber use the invisible hand
s = S()
D.title(s, "So: Does Uber Use the Invisible Hand?")
px, py, pw, ph = D.photo(s, PH % "uber_taxi", 0.60, 1.15, 4.15, 2.70)
D.textbox(s, 5.00, 1.20, 4.40, 1.10,
          "The question from the top of the hour. You now have everything you need to "
          "answer it — and to say by how much.",
          size=14.5, bold=True, color=BLUE, line_pct=1.24)
D.rect(s, 5.00, 2.42, 4.40, 0.06, fill=GOLD)
D.cards2(s, 2.62, 1.72, [
    (BLUE, "Both sides are price takers", "Riders see a price and decide. Drivers see a "
     "price and decide. Neither can move it."),
    (GREEN, "The price is doing a job", "It rations the rides that exist, and it calls "
     "more drivers onto the road."),
], xs=(5.00, 7.28), width=2.12)
D.image_credit(s)
D.notes(s, """Return to the carried question. Remind the room of the show of hands from
the start of the hour and the number you wrote on the board.

Frame the answer as a mechanism, not a verdict. Surge pricing does two things at once, and
students usually only see the first:

It rations demand — at a higher price, fewer people request a ride, and the ones who drop
out are the ones for whom the trip was worth least. That is the part that feels unfair.

It calls supply — at a higher price, more drivers decide the evening is worth working. Cars
that would have stayed parked come out. That is the part people miss, and it is the reason
the total number of completed rides goes UP.

Do not resolve it yet. Next slide has the diagram, the slide after has the evidence, and
the practice problem has the number.""")

# ============================================ 60. Exhibit 7.17 surge
s = S()
D.title(s, "Exhibit 7.17 — Two Ways to Handle a Demand Surge")
D.picture_fit(s, F % "surge", 0.60, 1.10, 8.80, 3.06)
D.kicker(s, "Without the surge, 15 rides happen and 15 people wait. With it, 20 rides "
            "happen and nobody does.", y=4.44)
D.notes(s, """Exhibit 7.17, drawn on the schedule from the end-of-chapter problem so the
picture and the arithmetic are the same market.

Panel (a): the game ends, demand shifts right, and the price is held at $15. Quantity
supplied stays at 15 rides. Quantity demanded is 30. Fifteen people are left standing in
the rain, and the app shows no cars.

Panel (b): the price is allowed to rise to $20. Drivers respond — this is a MOVEMENT along
the supply curve, not a shift, and it is worth saying that phrase because it is a
Chapter 4 distinction students still get wrong. Twenty rides happen and the market clears.

Compare the two outcomes honestly. In panel (b) the fifteen people who would have got a
ride at $15 now pay $20, and five people who would not have got one at all now do. So
there are winners and losers among riders, and the drivers gain. The total number of rides
is higher.

A note if a student compares with the textbook figure: the book draws this with $10 and
$20 and no schedule. We use $15 and $20 because those come from the schedule in the
end-of-chapter problem, so the picture and the numbers you will work in ten minutes are
the same market.""")

# ================================================ 61. what happened when surge broke
s = S()
D.title(s, "What Happened When the Surge Broke")
y = D.defbox(s, 1.15,
             "On New Year's morning in 2015 a technical fault switched surge pricing off "
             "for 26 minutes. It is as close to a controlled experiment as this question "
             "gets.")
D.cards3(s, y + 0.26, 1.62, [
    (RED, "The price fell", "The multiplier dropped from about 2.7× to 1× and stayed "
     "there for 26 minutes.", IC % "price-tag"),
    (RED, "Waits grew", "Estimated arrival times rose to around eight minutes as the "
     "available cars were taken.", IC % "clock"),
    (RED, "Requests went unfilled", "Roughly a quarter of trip requests were not "
     "completed at all.", IC % "phone"),
])
D.credit(s, "Hall, Kendrick & Nosko, “The Effects of Uber's Surge Pricing: A Case "
            "Study”, 2015. Note that this is the company's own research on its own "
            "product — strong on mechanism, and not independent.", y=4.36)
D.kicker(s, "Turn the price off and the shortage arrives in about a minute.", y=4.58)
D.notes(s, """The evidence, and the caveat that comes with it.

The natural experiment: in the early hours of 1 January 2015 the surge algorithm failed
for 26 minutes. Demand was at its annual peak, the multiplier fell to 1×, and the market
behaved exactly as Exhibit 7.15 says it should — arrival times rose to around eight
minutes and about a quarter of requests went unfilled.

The comparison case in the same study is a concert letting out at Madison Square Garden,
where surge worked normally: app openings quadrupled, driver supply roughly doubled, and
the average wait stayed at 2.6 minutes.

Now the caveat, and say it clearly on camera: this study was written by Uber's own
economists about Uber's own product, and it was published to defend a policy the company
was being criticised for. That does not make it wrong — the mechanism is exactly what
theory predicts, and the outage really was outside anyone's control. But it is not
independent evidence, and a student who cites it in an essay should say whose research it
is.

Good habit to model out loud: ask who ran the study, on whose data, and with what interest
in the answer. Then decide how much weight it carries. That is not cynicism, it is
reading.""")

# ================================================== 62. practice setup
s = S()
D.title(s, "Practice: The Football Game Lets Out")
D.textbox(s, 0.60, 1.10, 8.80, 0.34,
          "Supply is unchanged all evening. Demand doubles when the game ends.",
          size=13, bold=True, color=INK)
rows = [["Price", "Qd before", "Qd after the game", "Qs"],
        ["$5", "25", "50", "5"],
        ["$10", "20", "40", "10"],
        ["$15", "15", "30", "15"],
        ["$20", "10", "20", "20"],
        ["$25", "5", "10", "25"]]
D.table(s, 0.60, 1.52, 4.55, 2.45, rows, col_w=[1.00, 1.15, 1.55, 0.85],
        first_col_fill=BLUE, header_size=9.5, body_size=10,
        align=["ctr", "ctr", "ctr", "ctr"])
D.cards2(s, 1.52, 2.45, [
    (BLUE, "Answer these", "(a) Equilibrium price and quantity before the game.\n"
     "(b) The same, after, if the price is free to move.\n"
     "(c) At a fixed $15: how many rides, and what is the excess demand?\n"
     "(d) What is the deadweight loss from fixing the price?"),
], xs=(5.45,), width=3.95)
D.kicker(s, "Four minutes, in pairs. Then we do it together.", y=4.24)
D.notes(s, """Practice setup. Put it up, give them three or four minutes in pairs, then
take answers before revealing.

Parts (a) to (c) are the publisher's. Part (d) is added, because after Part 4 they can
do it and it is the question the whole hour has been building to.

Hints to give if the room stalls, in this order:
- For (a) and (b), find the row where quantity demanded equals quantity supplied.
- For (c), the price is fixed, so read quantity supplied at $15 and remember that the
  short side of the market always prevails — exchange is voluntary, so nobody can be made
  to sell.
- For (d), the deadweight loss is the triangle between the demand and supply curves,
  spanning the quantities that should have traded and did not.

The schedules, if useful at the board: before the game, quantity demanded is 30 minus the
price; after, it is 60 minus twice the price; supply is quantity equals price throughout.""")

# ================================================== 63. the answers
s = S()
D.title(s, "The Answers")
D.picture_fit(s, F % "practice", 0.60, 1.06, 5.35, 3.14)
lines = [
    ("(a)  Before: $15 and 15 rides.", {"bold": True, "color": BLUE}),
    ("Where 30 − P equals P.", {"size": 10.5, "color": INK}),
    ("", {"size": 6}),
    ("(b)  After: $20 and 20 rides.", {"bold": True, "color": BLUE}),
    ("Where 60 − 2P equals P.", {"size": 10.5, "color": INK}),
    ("", {"size": 6}),
    ("(c)  At a fixed $15: 15 rides happen.", {"bold": True, "color": BLUE}),
    ("30 wanted, 15 supplied — 15 short.", {"size": 10.5, "color": INK}),
    ("", {"size": 6}),
    ("(d)  Deadweight loss $18.75 an hour.", {"bold": True, "color": DGOLD}),
    ("½ × 5 rides × $7.50 of missing value.", {"size": 10.5, "color": INK}),
]
D.textbox(s, 6.20, 1.20, 3.25, 2.90, lines, size=12, line_pct=1.22)
D.kicker(s, "Five rides that should have happened did not — and that is the whole cost of "
            "holding the price.", y=4.34)
D.notes(s, """The answers. Walk each one.

(a) Before the game, quantity demanded equals quantity supplied at $15 and 15 rides.

(b) After the game, demand has doubled. Setting 60 minus twice the price equal to the
price gives $20 and 20 rides. Note that both the price AND the quantity rose — the surge
did not just make rides dearer, it made more of them happen.

(c) With the price nailed at $15, drivers still supply 15 rides. Riders want 30. Fifteen
people do not get home. This is Exhibit 7.15 with a different product.

(d) The deadweight loss. The five rides between 15 and 20 are each worth more to a rider
than they cost a driver, and none of them happens. The gap starts at $7.50 on the
fifteenth ride and closes to zero on the twentieth, so the loss is one half times five
times $7.50 — $18.75 an hour.

Then close the loop on the show of hands from slide 4. Ask whether anyone has changed
their mind, and be scrupulous about what the number does and does not settle: $18.75 is
the efficiency cost. It is not an argument that surge pricing is fair, and the fifteen
riders who now pay $20 instead of $15 have a real complaint. The model prices the
trade-off; it does not make the choice.

Every figure here closes exactly.""")

# ==================================================== closing pair =================
s = S()
D.recap_table(s, "Chapter 7: The Full Picture", [
    ["Efficiency", "Competitive equilibrium maximises social surplus.",
     "consumer and producer surplus, Pareto efficiency", "Exhibits 7.1–7.3"],
    ["Inside a firm", "Independent managers facing one price equalise marginal cost.",
     "marginal cost equalisation", "Exhibits 7.4–7.7"],
    ["Across industries", "Profit attracts entry, loss forces exit; both stop at "
     "P = MC = min ATC.", "free entry and exit, long-run equilibrium", "Exhibits 7.9–7.12"],
    ["Prices", "Freeze a price and you get a shortage, a queue and a deadweight loss.",
     "price signal, price ceiling, deadweight loss", "Exhibits 7.14–7.16"],
    ["Equity", "Efficiency is positive, equity is normative — and the model cannot "
     "settle it.", "equity, positive and normative", "Section 7.5"],
    ["The evidence", "Kerb pricing, storm statutes and a surge outage all show the "
     "mechanism.", "SFpark, anti-gouging rules, surge pricing", "Exhibit 7.17"],
], "Three chapters, one argument: buyers optimise, sellers optimise, and the price makes "
   "the two add up.")
D.notes(s, """Recap. Nothing new on this slide - it is the hour re-indexed so students can
find things.

Read the closing line out. It is the real close of the three-chapter arc: Chapter 5 built
demand from a buyer's problem, Chapter 6 built supply from a seller's problem, and Chapter
7 showed that putting the two together produces an outcome no one designed and no one
could improve on without hurting somebody.

If you cut material today, leave this slide up while you say what got cut and where to
read it.

Point forward: every result today depended on the conditions of perfect competition. From
here on the course removes them one at a time.""")

s = S()
D.takeaways_page(s, "Chapter 7: Perfect Competition and the Invisible Hand", [
    "Social surplus measures what a market creates. The competitive equilibrium "
    "maximises it — restricting trade or forcing it both destroy value.",
    "Self-interest equalises marginal cost across plants, firms and industries. That is "
    "what least-cost production means.",
    "Profit and loss are signals. Free entry and exit act on them until economic profit "
    "is zero and price equals minimum average total cost.",
    "A price is information and an incentive at once. Freeze it and you get a shortage, "
    "a queue, and a deadweight loss nobody receives.",
    "Efficient is not the same as fair. Economics prices the trade-off; it does not "
    "choose for you.",
])
D.notes(s, """Key takeaways. Five, and the first and last are the ones that matter beyond
this course.

If they remember one thing, make it the last: they now know what an economist means by
"efficient", and they know it is a narrower word than it sounds. That is worth more than
any diagram in the deck.

The second and third are the examinable core — marginal cost equalisation and the
zero-economic-profit long run come up every term.

Set up what comes next: everything today assumed many buyers, many sellers, an identical
good, free entry and good information. Chapter 8 starts taking those away, beginning with
what happens when one seller is big enough to move the price. Every result from today
weakens or reverses, and the difference between the two chapters is the difference between
a market that works and a market that needs watching.

Last line to say out loud: the invisible hand is not magic and it is not a moral claim.
It is a claim about what prices do with information — and like every claim in this course,
it comes with conditions attached.""")

prs.save(OUT)
print(f"{OUT}: {len(prs.slides._sldIdLst)} slides")
