#!/usr/bin/env python3
"""addback_ch07.py — restore nine slides to the instructor's cut of the Ch07 deck,
and repair the references his cuts left dangling.

This is an INSERTION pass, not a rebuild (ground rules S8.4). It opens his edited file,
edits only the shapes that now point at deleted material, appends the new slides, and
reorders the slide-id list so they land in the right places. Every slide he kept keeps
its own content.

He cut 65 slides to 38, removing all of Part 2 (the two-plant CEO), the practice problem,
and every live 2026 example. The brief was to add back what makes the hour run more
smoothly and argue harder, NOT the long worked examples — so Part 2 and the practice
problem stay out. What comes back is framing, one recall slide, one counter-argument and
two live laws.

WHAT HIS CUTS BROKE, and what this fixes:
  * the roadmap still promises a carried question that no longer exists   -> N1
  * the roadmap says "three scales" but only two survive                  -> text edit
  * the Part 2 divider still reads "PART 3", so there are two of them     -> text edit
  * Exhibit 7.9 and 7.11's notes say "the three steps" - now nowhere      -> N3
  * "Where It Stops" asserts zero economic profit with no gloss           -> N4
  * SFpark answers a question the deck never asks                         -> N5
  * Exhibit 7.16's "$147" comes from nothing, and its notes point forward  -> N6
  * five slides of price-control argument with no counterweight            -> N7
  * Part 5 has no contemporary anchor                                      -> N8
  * Exhibit 7.17 is an orphan diagram in the equity section                -> N9
  * "Two Ways to Answer Them" and "The Central Planner" notes call back to
    the deleted CEO                                                        -> notes rewrite
  * the recap table still has an "Inside a firm" row citing Exhibits 7.4-7.7 -> row dropped
  * takeaway 2 is the deleted Part 2's result                              -> replaced

Run:  python3 addback_ch07.py <in.pptx> <out.pptx>
"""
import sys

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Inches

import deckkit as D
from deckkit import (BLUE, GOLD, DGOLD, GREEN, RED, INK, GREY, RULE, WHITE,
                     TINT_BLUE, TINT_NEUTRAL, TINT_RED, TINT_GREEN, TINT_GOLD)

SRC = sys.argv[1] if len(sys.argv) > 1 else "cur.pptx"
OUT = sys.argv[2] if len(sys.argv) > 2 else "ECON003_Ch07_..._UCR_v2.pptx"
F = "figs/ch07_fig_%s.png"
IC = "icons/%s.png"
PH = "photos/%s_flat.png"
LIMIT = 4.40

prs = Presentation(SRC)
N_KEPT = len(prs.slides._sldIdLst)
assert N_KEPT == 38, f"expected his 38-slide cut, got {N_KEPT}"


# --------------------------------------------------------------- helpers
def slide(n):
    """1-indexed slide from the ORIGINAL 38."""
    return prs.slides[n - 1]


def find(s, startswith):
    for sh in s.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip().startswith(startswith):
            return sh
    raise LookupError(startswith)


def set_text(shape, new):
    """Replace a single-run textbox's words, keeping every formatting attribute."""
    runs = [r for p in shape.text_frame.paragraphs for r in p.runs]
    runs[0].text = new
    for r in runs[1:]:
        r.text = ""


def drop(shape):
    shape._element.getparent().remove(shape._element)


# ================================================ repairs to his kept slides
# --- roadmap: two scales survive, not three
set_text(find(slide(3), "ONE IDEA"), "ONE IDEA, TWO SCALES")
D.notes(slide(3), """Roadmap.

Four parts. They escalate in scope: one market you can count on your fingers, then a whole
economy of industries, then the price system itself, then the one question the model
cannot settle for us.

Announce the carried question here and again on the next slide. It is deliberately the one
students already have an opinion about, and most rooms start out against surge pricing.
That is exactly what makes the ending land.""")

# --- the Part 2 divider still reads PART 3
set_text(find(slide(15), "PART"), "PART 2")

# --- Exhibit 7.3 carries the publisher's arithmetic slip, since the slide that
#     worked the cap by hand is gone
D.credit(slide(12),
         "Worth checking against the textbook's own table for the capped case: it totals "
         "the consumer- and producer-surplus columns at $100 each, but each column sums to "
         "$50. The $100 is the social surplus — the only one of the three figures that is "
         "right.", y=4.95)

# --- "Two Ways to Answer Them": the CEO callback it leaned on is gone
D.notes(slide(31), """The comparison.

Keep it analytical rather than ideological. The difference between the two columns is not
about motives; it is about where information sits and how much of it has to move.

The point to press is the last line of the command-economy card: a planner has to COLLECT
the information that a price would have summarised for free, and collect it faster than it
goes stale. Nobody has ever managed the second part.

Make it concrete before the kicker. Ask what a central agency would need to know to set the
price of one thing — say, copper. Every mine's cost, every user's alternative, every
substitute's price, and all of it changing daily. Then the kicker: now do that for every
product at once, where each answer depends on all the others.

Fair-minded note if a student raises it: real economies are all mixtures, and some
functions — defence, public health, basic research — are directed centrally in every
country, for reasons the next section starts to explain.""")

# --- "The Central Planner": same callback
D.notes(slide(32), """The publisher's illustration of central direction, handled carefully.

The story as they tell it: the blue light special began in 1965 as a store-level tool — a
manager with too many of something switched on the light and cleared it. Later the
corporate office took the decision over, running the same promotion on the same item at the
same time nationwide, and the results were worse.

What I can source and what I cannot, and this matters. The 1965 start, the loudspeaker
announcement, the discontinuation in the early 1990s and the revivals in 2001 and 2015 are
all well documented. The claim that centralising the decision CAUSED lower profits is not
something I can find a source for. So tell it as an illustration of the mechanism, not as
evidence for it, and do not put a figure on the damage.

The mechanism is the one from the last slide, shrunk to a size students can hold: the local
manager could see which shelves were full and head office could not. Substituting a uniform
rule for local information throws away the only thing the manager had that head office
lacked.

Good question to leave hanging: what would head office have needed to know to do this
well? The answer is "everything every store manager knew", which is the coordination
problem in one sentence.""")

# --- recap table: drop the row for the section he deleted, and re-word the evidence row
tbl = next(sh for sh in slide(37).shapes if sh.has_table).table
for r, row in enumerate(tbl.rows):
    if row.cells[0].text.strip() == "Inside a firm":
        tbl._tbl.remove(row._tr)
        break
for row in tbl.rows:
    if row.cells[0].text.strip() == "The evidence":
        set_text(row.cells[1], "Kerb pricing, a real 10% price cap and surge pricing "
                               "all show the mechanism.")
        set_text(row.cells[2], "SFpark, anti-gouging rules, surge pricing")
# five body rows now share the height the six had
hdr_h = 0.38
body_h = (3.31 - hdr_h) / (len(tbl.rows) - 1)
tbl.rows[0].height = Inches(hdr_h)
for r in range(1, len(tbl.rows)):
    tbl.rows[r].height = Inches(body_h)

# --- takeaway 2 was Part 2's result; replace it with one the deck still proves
old = find(slide(38), "Self-interest equalises")
x, y, w = old.left, old.top, old.width
drop(old)
NEW_BULLET = ("Pareto efficient is a low bar. It only means no free moves are left — "
              "one person owning everything clears it.")
lines = D.wrap(NEW_BULLET, 7.60, 13.5)
D.textbox(slide(38), D.Emu(x).inches, D.Emu(y).inches, 7.60,
          D.text_h(len(lines), 13.5, 1.2), "\n".join(lines),
          size=13.5, color=WHITE, line_pct=1.2, anchor="ctr")
D.notes(slide(38), """Key takeaways. Five, and the first and last are the ones that matter
beyond this course.

If they remember one thing, make it the last: they now know what an economist means by
"efficient", and they know it is a narrower word than it sounds. That is worth more than
any diagram in the deck.

The second and third are the examinable core. The Pareto line is the one students most
often over-read — say the "one person owns everything" example out loud, because it is what
stops "efficient" being heard as "good".

Set up what comes next: everything today assumed many buyers, many sellers, an identical
good, free entry and good information. Chapter 8 starts taking those away, beginning with
what happens when one seller is big enough to move the price. Every result from today
weakens or reverses.

Last line to say out loud: the invisible hand is not magic and it is not a moral claim. It
is a claim about what prices do with information — and like every claim in this course, it
comes with conditions attached.""")


# ============================================================ the new slides
def S():
    return D.blank_slide(prs)


new_order = []   # (insert_after_original_slide_number, appended_index)


def add(after):
    new_order.append(after)
    return S()


# ---------------------------------------- N1. the carried question (after roadmap)
s = add(3)
D.title(s, "A Question to Carry Through the Hour")
D.photo(s, PH % "uber_phone", 5.05, 1.15, 4.35, 2.60)
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
point is that the last exhibit of the hour gives us a measurement rather than an opinion.

The $32 figure is illustrative — a plausible multiplier, not a quoted fare. Do not
attribute it to any company.""")

# ------------------------------------------- N2. try a price (after Exhibit 7.1)
s = add(7)
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
D.notes(s, """Trying prices. Do this live at the board rather than reading the slide — it is
the one moment in Part 1 where the room works something out instead of being told.

Pick $10 first, because the imbalance is dramatic and everyone can see it: seven buyers,
one seller. Then $60 the other way. Then ask the room for the price that balances, and wait,
before you reveal $40.

The pedagogical point is that equilibrium is not a compromise, or a fair price, or a price
anyone negotiated. It is an arithmetic fact about the table.

Worth pausing on: at $40, Dave and Phil are both exactly indifferent. Dave pays what the
phone is worth to him; Phil accepts exactly what it costs him. Neither gains anything. That
is why the fourth trade adds nothing to social surplus, and it is the detail that makes the
surplus slides make sense.

A sharp student may ask whether equilibrium quantity is 3 or 4. Both give total surplus of
$120, because the fourth trade creates zero surplus. Say so — it is a good question, not a
gotcha.""")

# --------------------------------- N3. the three steps (opening Part 3, before Ex 7.9)
s = add(15)
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
D.notes(s, """Chapter 6's three steps, recalled. Brisk — but do not skip it, because this is
now the only slide in the deck that states the profit-maximising procedure, and the next
four exhibits all run it.

Walk the band once, pointing at each step, and say that every diagram in this section is
the same three moves in a different position.

The new emphasis is the kicker. In Chapter 6 economic profit was an outcome — the answer to
"am I making money?". In Chapter 7 it is an input: a message to everyone OUTSIDE the
industry saying resources here are earning more than they could elsewhere, come and get
some.

That reframing is the whole of this part, so say it before the diagrams arrive rather than
after.

Reminder worth stating: economic profit is measured after opportunity cost, which is why
P = ATC is a resting point rather than a crisis. The slide after the long-run diagram
comes back to this.""")

# ------------------------- N4. zero economic profit (after "Where It Stops")
s = add(20)
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
D.notes(s, """The most misread result in the chapter, and it comes up every year. The
previous slide has just asserted that economic profit is zero in every industry at once,
which sounds alarming if you do not gloss it.

Make it concrete with a number. Put $500,000 into a paper delivery firm and it returns
$40,000 a year, while the same money in an index fund would have returned $40,000.
Accounting profit: $40,000. Economic profit: zero. You are doing fine. You have no reason
to move your money in, and none to move it out.

That is what long-run equilibrium looks like from the inside. It is not an industry on life
support; it is an industry that has stopped being unusual.

Give the exam warning explicitly: a question saying "in long-run competitive equilibrium
firms earn zero economic profit" is not saying firms earn nothing. Students lose marks on
this every term.""")

# ---------------------------- N5. the parking meter question (before SFpark)
s = add(23)
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
D.notes(s, """The publisher's live-classroom question, adapted for a recorded lecture.

Pause the recording here. Ask the question, wait, then take the two wrong-ish answers before
revealing the third. Without this slide the next one answers a question nobody has asked.

The revenue answer is the one most students give and it is empirically weak — parking
revenue is a minor line in a city budget and enforcement eats into it.

The real function is allocation. Kerb space in a busy district is genuinely scarce, and with
no price it gets rationed by who is willing to drive around the longest looking. That is
rationing by waiting, and the waiting is pure waste — nobody receives it. The driver burns
fuel and time and hands the value to no one.

With a price, the space goes to whoever values it most at that moment, and the money at
least goes somewhere.

Then raise the objection yourself: does this actually work, or is it just a story? Next
slide.""")

# ------------------------- N6. New York's 10 per cent (after Exhibit 7.16)
s = add(29)
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
D.notes(s, """The payoff for the whole price-control run, and the reason the $147 on the
previous slide is a real number rather than a classroom one.

Numbers to read, not recall: pre-storm price $30. Statutory threshold 10%, so $33. The
market-clearing price after the demand shift is $40. At $33 the quantity supplied is 66
cases; quantity demanded is 87; so 21 cases short. Trades fall from 80 to 66, and the
deadweight-loss triangle is one half times 14 cases times $21 — exactly $147 an hour.

Now the honesty, and it matters more than the arithmetic:

The 10% figure creates a rebuttable PRESUMPTION, not a hard ceiling. A seller whose own
wholesale costs rose can charge more and defend it. So the true constraint is looser than
the one we have drawn, and our $147 is an upper bound on what this rule costs in this
market. Say that on camera.

Also worth saying: the rule was adopted with a package of others — definitions of unfair
leverage, a 30% market-share presumption, a concentration threshold — so it is aimed mainly
at sellers with market power, not at the corner shop. That is more careful drafting than the
classroom price-ceiling story usually allows for.

If a student asks whether the rule is a good idea: that is the next slide, and the answer
depends on something the model cannot measure.""")

# ------------------------------ N7. the case on the other side (after N6)
s = add(29)
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
D.notes(s, """Give both sides properly. Five slides in a row have now pointed one way; this
is the one that stops the sequence being a sermon, and a case that answers its strongest
objection is stronger than one that ignores it.

The equity argument is not weak and should not be presented as a naive objection. Social
surplus counts a dollar of willingness to pay identically whoever holds it, and in an
emergency that is a genuinely contestable way to count. A person who cannot afford $40
water is not revealing that they value it less.

The efficiency argument is also not weak. The supply response is the entire mechanism, and
suppressing it makes the shortage worse for everyone, including the poor.

On the study: one paper, one episode, an indirect outcome measure — contacts inferred from
phone location data rather than shortages measured directly. Cite it as evidence, not proof,
and say so. There is other work finding anti-gouging rules speed recovery in some settings;
the honest summary is that the empirical question is not settled.

Land it here: the model tells you the size of the efficiency cost. It cannot tell you whether
that cost is worth paying. That is a value judgement, and the last part of the hour is about
admitting it rather than dressing it up.""")

# ------------------- N8. Maryland (after "Efficient Is Not the Same as Fair")
s = add(35)
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
D.notes(s, """The most sophisticated slide in the deck, and the only contemporary anchor in
this part. Worth the time.

The story: dynamic pricing has become politically contentious, and in April 2026 Maryland
became the first state to legislate against a specific form of it. The law is narrow — large
grocers and delivery apps, tax-exempt food only.

Here is why it belongs in this chapter. The legislature did not ban prices from moving. It
explicitly carved out changes driven by supply and demand, weather and energy costs. What it
banned is a price computed from YOUR data, for YOU.

That is a remarkably clean statement of the distinction the whole hour rests on. A price that
moves with scarcity is a message about the world and does allocative work — it brings the
trucks. A price computed from your browsing history carries no information about scarcity at
all; it just moves surplus from you to the seller.

Two things not to overstate:
- The economics of price discrimination is genuinely more complicated than "it just
  transfers surplus". It can expand output and serve customers who would otherwise be priced
  out. Flag it, do not resolve it.
- Whether the law works as drafted is untested. It takes effect on 1 October 2026, after
  this course ends.

Re-check before delivery: whether the effective date holds and whether other states have
followed.""")

# ------------------- N9. does Uber use the invisible hand (before Exhibit 7.17)
s = add(35)
D.title(s, "So: Does Uber Use the Invisible Hand?")
D.photo(s, PH % "uber_taxi", 0.60, 1.15, 4.15, 2.70)
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
D.notes(s, """Return to the carried question. Remind the room of the show of hands from the
start of the hour and the number you wrote on the board.

Frame the answer as a mechanism, not a verdict. Surge pricing does two things at once, and
students usually only see the first:

It rations demand — at a higher price fewer people request a ride, and the ones who drop out
are the ones for whom the trip was worth least. That is the part that feels unfair.

It calls supply — at a higher price more drivers decide the evening is worth working. Cars
that would have stayed parked come out. That is the part people miss, and it is why the
total number of completed rides goes UP.

Do not resolve it yet. The next slide has the diagram, and the honest close is the one from
two slides ago: the model prices the trade-off, it does not make the choice. Fifteen riders
who now pay $20 instead of $15 have a real complaint, and five riders who get home instead
of standing in the rain have a real gain.""")

# =========================================== put the new slides in their places
sldIdLst = prs.slides._sldIdLst
ids = list(sldIdLst)
kept, added = ids[:N_KEPT], ids[N_KEPT:]
assert len(added) == len(new_order), (len(added), len(new_order))

final = []
for i, sid in enumerate(kept, start=1):
    final.append(sid)
    for j, after in enumerate(new_order):
        if after == i:
            final.append(added[j])

assert len(final) == N_KEPT + len(added), (len(final), N_KEPT, len(added))
for sid in ids:
    sldIdLst.remove(sid)
for sid in final:
    sldIdLst.append(sid)

prs.save(OUT)
print(f"{OUT}: {N_KEPT} + {len(added)} = {len(prs.slides._sldIdLst)} slides")
