#!/usr/bin/env python3
"""Surgical edits to the instructor's OWN Ch06 deck — the McDonald's pass.

    cp <his ECON003_Ch06_...pptx> work.pptx
    python3 edit_ch06_mcdonalds.py

Five slides inserted, two existing slides gain one card each. Nothing else is touched;
no slide is regenerated.

Every figure on these slides is sourced on the slide face. Sources, once:
  * McDonald's 2025 Franchise Disclosure Document, Items 5, 6, 7 and 19
    (financial data as of 31 Dec 2024) — fees, investment range, average unit volume.
  * mcdonalds.com/us/en-us/us-franchising — cash requirement, site ownership, training.
  * McDonald's USA, "McD US Pricing Myths vs Facts", 29 May 2024 — 2019 vs 2024 prices.
  * McDonald's Q2 2026 earnings release, 4 Aug 2026 — comps and guest counts.
  * McDonald's FY2025 Form 10-K — US restaurant counts.
  * BLS OEWS, May 2025 — crew and food-service-manager pay.
  * California DIR — fast-food minimum wage.
  * US Treasury daily yield curve, 7 Aug 2026 — 10-year yield.
  * Andreyeva, Long & Brownell, AJPH 100(2), 2010 — food-away-from-home elasticity.
"""
from pptx import Presentation

import deckkit as D
from deckkit import (BLUE, GOLD, DGOLD, GREEN, RED, INK, GREY,
                     TINT_NEUTRAL, TINT_GREEN, TINT_GOLD)

SRC, OUT = "work.pptx", "ECON003_Ch06_Sellers_and_Incentives_UCR.pptx"
F, IC = "figs/ch06_fig_%s.png", "icons/%s.png"

prs = Presentation(SRC)
sl = list(prs.slides)
before = len(sl)
lst = prs.slides._sldIdLst
ids = list(lst)


def find(starts):
    for i, s in enumerate(sl):
        for sh in s.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip().startswith(starts):
                return i, s
    raise SystemExit("NOT FOUND: " + starts)


# every anchor resolved BEFORE anything moves, so later inserts cannot shift them
# NB: the Part 1 divider's subtitle also starts with "Seller", so match the whole title.
# The deck uses a curly apostrophe.
i_sp, s_sp = find("Seller’s Problem")
i_ct, _ = find("The Cost Table")
i_bend, s_bend = find("Why the Average Curves Bend")
i_ae, _ = find("Accounting Profit vs Economic Profit")
i_see, _ = find("Seeing the Profit")
i_elas, _ = find("What Makes Supply Elastic?")
i_shut, s_shut = find("Stay Open or Shut Down")
print(f"anchors  seller={i_sp+1} cost-table={i_ct+1} bend={i_bend+1} "
      f"acct/econ={i_ae+1} seeing={i_see+1} elastic={i_elas+1} shutdown={i_shut+1}")

n_new = 0


def S():
    s = D.blank_slide(prs)
    return s


def place(after_el):
    """Move the just-added slide into position IMMEDIATELY.

    Deferring the insert is a trap: while a new slide's sldId sits outside sldIdLst,
    python-pptx cannot see its part, so the NEXT add_slide() hands out the same
    partname. Five deferred inserts produced five slides all called slide62.xml.
    """
    global n_new
    el = list(lst)[-1]
    lst.remove(el)
    lst.insert(list(lst).index(after_el) + 1, el)
    n_new += 1


# ============================================ 1. the business decision, after "Seller's Problem"
s = S()
D.title(s, "So Let's Open One")
y = D.defbox(s, 1.15, "Suppose you want to open a McDonald's. Here is what it takes before "
                      "you serve a single meal.")
D.cards3(s, y + 0.28, 1.92, [
    (BLUE, "The cheque you write",
     "A $45,000 franchise fee, and $1.47 to $2.73 million for equipment, seating, signage "
     "and opening stock. At least $750,000 of it has to be your own money, not borrowed.",
     IC % "coin-stack"),
    (RED, "What you do NOT buy",
     "Not the land, and not the building. McDonald's picks the site, buys it and builds "
     "the restaurant — then leases it to you. Hold that thought; it shapes every cost in "
     "this chapter.", IC % "house"),
    (GREEN, "And the clock",
     "Six to twelve months of training before you are even considered for a restaurant, "
     "and an agreement that usually runs twenty years.", IC % "clock"),
])
D.kicker(s, "Every number in the next forty minutes belongs to this restaurant.", y=4.42)
D.credit(s, "McDonald's 2025 Franchise Disclosure Document, Items 5 and 7; "
            "mcdonalds.com/us/en-us/us-franchising (costs, process and FAQ pages), "
            "retrieved 9 August 2026.", y=4.96)
D.notes(s, """The decision that carries the rest of the hour. Spend two minutes here.

READ THESE OUT: a $45,000 franchise fee. A total initial investment of $1.47 to $2.73
million. At least $750,000 of it in non-borrowed personal funds. Six to twelve months of
training. A twenty-year agreement.

THE SECOND CARD IS THE IMPORTANT ONE and it is easy to skip. The franchisee does NOT buy
the land or the building. McDonald's acquires the site, builds the restaurant, and issues
the operator a lease. That is why the initial investment looks small for a restaurant — the
real capital is on McDonald's balance sheet, and it comes back as rent. We meet that rent in
twenty minutes.

If a student says "$2.7 million seems cheap for a restaurant" — they are right, and that is
the answer. Say so; it is a good catch.

One sourcing note worth making out loud if you like, because it teaches something: McDonald's
own franchising-costs page says $750,000 of non-borrowed funds, while its consumer FAQ page
still says $500,000. Both were live in August 2026. Use $750,000 — the dedicated page — and
tell them that checking two pages of the same company's site is normal work.

From here on, "the firm" means this restaurant. Every table, every curve, every decision.""")
place(ids[i_sp])

# ============================================ 2. the running cost, after "The Cost Table"
s = S()
D.title(s, "What It Actually Costs to Run One")
D.picture_fit(s, F % "mcd_costs", 0.60, 1.05, 8.80, 2.06)
D.cards2(s, 3.26, 1.52, [
    (RED, "Shares of SALES, not of profit",
     "The royalty and the ad fund come off the top line. They are owed whether or not the "
     "restaurant makes anything."),
    (BLUE, "So which of them is fixed?",
     "Rent has a minimum base you owe whatever you sell. The royalty and ad fund move with "
     "sales. All three feel like overhead — only one behaves like it."),
], body_size=11)
D.credit(s, "Average annual sales and all three fees: McDonald's 2025 Franchise Disclosure "
            "Document, Items 5, 6 and 19 — 2024 sales across about 12,023 US franchised "
            "restaurants open at least a year; median $3.80m, range $914,000 to $19.7m. "
            "Rent is shown at 10% for illustration; the FDD discloses effective rents from "
            "0.00% to 33.33% of gross sales.", y=4.90)
D.notes(s, """The running cost, on the real restaurant. This is the slide the cost table was
building toward.

READ THESE OUT: an average US franchised McDonald's sold $3,966,000 in 2024. The service fee
— the royalty — is 5% of gross sales for a new franchisee. The advertising contribution is
not less than 4% of gross sales. Rent to McDonald's is a percentage of gross sales too.

At $3.97 million, the royalty alone is about $198,000 a year and the ad fund about $159,000.
Rent at 10% would be another $397,000. That is roughly $754,000 gone before a single burger,
a single hour of crew, or a single kilowatt is paid for.

THE DENOMINATOR IS THE LESSON. Every one of those percentages is a share of GROSS SALES —
the top line — not of profit and not of what is left. Ask the room what happens to the
royalty in a bad month. It falls with sales, yes; but it never falls to zero while the doors
are open, and it does not care whether the month was profitable.

The second card is the subtle one and worth the time. Rent is structured as the greater of a
minimum base rent or a percentage of sales. So there is a floor you owe regardless. The
royalty has no floor. Two things that both feel like overhead, and only one of them is fixed
in the sense this chapter means.

TWO CAVEATS, and say them before a student does:
1. The 5% royalty applies to NEW franchisees, from 1 January 2024 — the first increase in
   nearly thirty years. Operators who signed earlier are grandfathered at 4%.
2. The $3.97m average is across restaurants open at least a year, and the range runs from
   $914,000 to $19.7 million. It is not what your store would make in year one.

WHAT I HAVE NOT PUT ON THE SLIDE, and why: McDonald's discloses gross sales and fees, but
NOT franchisee profit. Any "a McDonald's owner makes $150,000 a year" figure you find online
is somebody applying an assumed margin. We come back to that on the economic-cost slide.""")
place(ids[i_ct])

# ==================================== 3. economic cost, after "Accounting Profit vs Economic Profit"
s = S()
D.title(s, "The Economic Cost of Running a McDonald's")
y = D.defbox(s, 1.15, "The accountant counts the cheques you write. The economist adds what "
                      "you gave up in order to write them.")
D.cards3(s, y + 0.26, 1.92, [
    (BLUE, "EXPLICIT — the invoices",
     "Food and paper. Crew. Power. Rent. The 5% royalty. The 4% ad fund. Every one of them "
     "is billed, paid, and on the tax return.", IC % "receipt"),
    (GREEN, "IMPLICIT — your time",
     "Somebody has to run the restaurant. A US food-service manager earns about $74,900 a "
     "year. Do the job yourself and you have given that up.", IC % "manager"),
    (RED, "IMPLICIT — your money",
     "$750,000 of your own cash, locked in for twenty years. At the 4.65% Treasury yield "
     "that is $35,000 a year of forgone interest.", IC % "coin-stack"),
])
D.band(s, 4.28, "Roughly $110,000 a year of real cost that never appears on the tax return — "
                "and McDonald's publishes no franchisee profit figure at all.",
       kind="flag", size=12)
D.credit(s, "Food-service manager pay: BLS Occupational Employment and Wage Statistics, "
            "May 2025 (mean annual $74,880). Ten-year Treasury constant maturity yield "
            "4.65%, 7 August 2026, US Treasury. Cash requirement: McDonald's franchising "
            "costs page.", y=5.02)
D.notes(s, """The economic-cost slide, on our own restaurant. This is where the previous
slide's abstraction becomes somebody's actual decision.

READ THESE OUT: a US food-service manager earns a mean of $74,880 a year. The 10-year
Treasury yielded 4.65% on 7 August 2026. On the $750,000 of non-borrowed cash alone that is
about $35,000 a year of forgone interest; on the full $2.1 million midpoint investment it is
closer to $98,000.

Add the manager's salary and the interest on the cash and you have roughly $110,000 a year of
cost that no accountant records. On the full investment it is nearer $170,000.

The argument to make: the owner-operator is not working for free and the money is not sitting
idle by accident. Both have alternatives, and the value of the best alternative is a cost of
choosing this. That is the whole of economic profit.

THE FLAG BAND IS WORTH DWELLING ON. McDonald's Franchise Disclosure Document discloses gross
sales — and stops. It publishes no franchisee profit, no cash flow, no net income. So a
student who goes looking for "what does a McDonald's owner earn" will find only numbers that
somebody built by assuming a margin. Tell them that. Learning that a figure is not published
is a real result, and it protects them from repeating a made-up one.

Directionally, what IS on the record: McDonald's chief executive said in 2024 that franchisee
cash flows were down about 10% from their highs, with California operators under more
pressure than most. No dollar baseline was given, and do not invent one.

Callback: this is the restaurant owner from the previous slide's table, with $500 of
accounting profit and minus $200 of economic profit. Same arithmetic, real business.""")
place(ids[i_ae])

# ============================================ 4. profit maximisation, after "Seeing the Profit"
s = S()
D.title(s, "How a McDonald's Actually Maximises Profit")
y = D.defbox(s, 1.15, "MR = MC is not a burger-by-burger decision. In a real restaurant it "
                      "is an hour-by-hour one.")
D.cards3(s, y + 0.26, 1.86, [
    (BLUE, "The marginal unit is a crew-hour",
     "Roster one more person for one more hour. Does the extra service that hour buys bring "
     "in more than the hour costs?", IC % "hard-hat"),
    (RED, "So what does the hour cost?",
     "Fast-food and counter workers average $15.46 an hour nationally. In California the "
     "fast-food minimum is $20.00 — against a $16.90 general minimum, an 18% premium your "
     "students can see from campus.", IC % "clock"),
    (GREEN, "And the same rule sets the hours",
     "Open at 5am? Staff the second drive-thru lane? Run overnight? Every one of them is "
     "MR = MC asked about a smaller unit.", IC % "register"),
])
D.kicker(s, "Same rule as the diagram. Real units: crew-hours, not burgers.", y=4.40)
D.credit(s, "Wages: BLS Occupational Employment and Wage Statistics, May 2025 — fast food "
            "and counter workers, mean hourly $15.46, median $15.00. California fast-food "
            "minimum wage $20.00 since 1 April 2024 and unchanged in 2026; California "
            "general minimum $16.90 from 1 January 2026 (California DIR).", y=4.94)
D.notes(s, """Profit maximisation, made operational. The previous slide drew the rectangle;
this one says what the manager actually decides.

READ THESE OUT: fast-food and counter workers averaged $15.46 an hour nationally in May 2025,
median $15.00. California's fast-food minimum has been $20.00 since April 2024 and was still
$20.00 in 2026. California's general minimum is $16.90 from January 2026 — so fast food
carries a $3.10, roughly 18%, premium.

The move to make: students picture the firm choosing "how many burgers", which is not a
decision anybody makes. The restaurant serves whoever walks in. What the manager actually
chooses is how much CAPACITY to have on the floor — how many people rostered, which hours to
open, whether the second lane is staffed.

So the marginal unit is a crew-hour, and the rule is unchanged: roster the hour if the extra
service it buys is worth more than the hour costs. In California, at $20, the bar is 18%
higher than the national average — which is a live natural experiment your students can watch
from the parking lot.

Ask: what does the California wage do to the profit-maximising number of crew-hours? Fewer of
them, at any given price. And then the follow-up that makes it interesting — what does it do
to the incentive to install ordering kiosks?

ONE HONEST NOTE if a student asks what McDonald's pays: McDonald's does not set wages at
about 95% of US restaurants, because they are independently owned, and it publishes no
system-wide average. The BLS occupational figure is the defensible number. That the franchisor
does not control its franchisees' largest controllable cost is itself worth a sentence.""")
place(ids[i_see])

# ======================================== 5. elasticity, after "What Makes Supply Elastic?"
s = S()
D.title(s, "How Elastic Is McDonald's?")
D.picture_fit(s, F % "mcd_prices", 0.60, 1.02, 8.80, 2.06)
D.cards2(s, 3.24, 1.56, [
    (RED, "SUPPLY elasticity — this chapter",
     "Within the hour, roster another crew member: very responsive. Within a year, McDonald's "
     "must buy a site and build, and the operator needs 6–12 months of training. The US network "
     "grew by 149 restaurants in 2025, on a base of 13,706."),
    (BLUE, "DEMAND elasticity — Chapter 5",
     "In the second quarter of 2026 US comparable sales rose 0.8% — on a bigger average "
     "check, “partly offset by negative comparable guest counts”. Prices up, visits down."),
], body_size=10.5)
D.credit(s, "Menu prices: McDonald's USA, “McD US Pricing Myths vs Facts”, 29 May 2024, "
            "with its own 29% food-away-from-home benchmark. Comparable sales and guest "
            "counts: McDonald's Q2 2026 earnings release, 4 August 2026. Restaurant counts: "
            "McDonald's FY2025 Form 10-K. Published elasticity for food away from home: "
            "−0.81 (Andreyeva, Long & Brownell, AJPH 100(2), 2010).", y=4.92)
D.notes(s, """Elasticity on the real firm — and the slide exists partly to stop a confusion.

READ THESE OUT. McDonald's own 2019-to-2024 price comparison: Big Mac $4.39 to $5.29, up 21%.
Ten-piece McNuggets, the same, up 21%. Quarter Pounder with cheese, up 20%. Egg McMuffin, up
23%. Medium fries $2.29 to $3.29 — up 44%. Food-away-from-home inflation over the same years
was 29%, which is McDonald's own benchmark in the same document.

Note what that means and say it: against 29% general inflation, the real price of a Big Mac
FELL. Only the fries rose faster than the category. If you are going to run an elasticity
calculation, decide first whether you are using nominal or real prices — the sign of the
implied response can flip.

THE TWO CARDS ARE TWO DIFFERENT ELASTICITIES AND THAT IS THE POINT OF THE SLIDE.

Supply elasticity — this chapter — asks how quickly the SELLER can produce more when the
price rises. Over an hour, very quickly: roster another person. Over a year, slowly: McDonald's
has to acquire a site and build a restaurant, and the operator needs six to twelve months of
training. The US network went from 13,557 to 13,706 restaurants during 2025 — 149 net
additions, about 1.1%. That is a mature market where entry is slow and expensive.

Demand elasticity — Chapter 5 — asks what buyers do when the price rises. McDonald's own words
for the second quarter of 2026: US comparable sales up 0.8%, driven by positive check growth,
"partly offset by negative comparable guest counts". Bigger baskets, fewer visits.

Sharper still, and worth saying: management reported low-income customer traffic falling at
roughly double-digit rates through 2025 while higher-income traffic rose. Same menu, same
prices, opposite responses — elasticity differs by who is buying.

THINGS NOT TO CLAIM:
- McDonald's does not publish a guest-count percentage, only the direction. If you have seen
  "US traffic fell 4.5%", that is Placer.ai mobile-location data, not McDonald's, and it
  measures store visits rather than transactions. Attribute it or leave it out.
- The −0.81 elasticity is for food away from home in aggregate, from a 2010 review of older
  studies. It is not a fast-food elasticity and not a 2026 one.
- McDonald's said two different things in one week in 2024: core items up 20-23%, and an
  executive saying the average item cost about 40% more than 2019. Both are on the record.
  Menu mix and the fries outlier reconcile them, and it is a good prompt if you want one.""")
place(ids[i_elas])

print(f"+ {n_new} slides inserted")

# ---------------------------------- 6. a quick McDonald's example on "Why the Average Curves Bend"
D.cards2(s_bend, 1.15, 2.45, [
    (DGOLD, "At a McDonald's",
     "Base rent spreads over more meals, so it falls per meal. The 5% royalty and 4% ad "
     "fund are shares of sales — they never spread at all."),
], width=1.92, xs=(7.48,), body_size=9)
print("~ McDonald's card added to 'Why the Average Curves Bend'")

# ---------------------------------- 7. and one on the shutdown comparison
D.cards2(s_shut, 4.20, 1.02, [
    (DGOLD, "At a McDonald's this is an hour, not a year",
     "Open at 6am? Run overnight? The rent is owed either way; the crew, the power and the "
     "food are not."),
], width=8.80, xs=(0.60,), body_size=11)
print("~ McDonald's card added to 'Stay Open or Shut Down'")

prs.save(OUT)
print(f"\nsaved {OUT}: {before} → {len(Presentation(OUT).slides._sldIdLst)} slides")
