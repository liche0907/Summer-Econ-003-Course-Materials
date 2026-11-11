#!/usr/bin/env python3
"""ECON 003 - Chapter 9 (Externalities and Public Goods) figures.

matplotlib, UCR palette, Liberation Sans (Arial metrics).  Blue = demand / marginal
benefit, red = supply / marginal cost, everywhere, permanently.  Green marks the social
optimum; gold-brown marks the wedge between private and social.

UNLIKE CHAPTER 8, THIS CHAPTER HAS THE PUBLISHER'S DECK.  Every curve below is recovered
from the drawn exhibits in Acemoglu_Micro_3e_Ch09, not invented, and every headline
number is asserted at import so a later edit that breaks the arithmetic fails loudly.

  RECOVERY METHOD.  The publisher's exhibit images were read directly, and the alt-text
  ("Long Description") in the notes was used as a cross-check.  Where the two disagree
  THE DRAWN FIGURE WINS - see the three defects recorded at the bottom of this header.

  ELECTRICITY (Exhibits 9.1, 9.2, 9.3, 9.8)   P in $/kWh, Q in billions of kWh
        D:    P = 0.40 - 0.0005 Q          (drawn through (100,0.35) and (700,0.05))
        S:    P = 0.0005 Q                 (drawn through (100,0.05) and (700,0.35))
        MSC:  P = 0.0005 Q + 0.10          (drawn parallel to S, MEC constant)
      market      Q = 400, P = 0.20
      optimal     Q = 300, P = 0.25,   MSC(400) = 0.30
      MEC         $0.10 per kWh, constant - which is why the Pigouvian tax is a
                  constant $0.10 and lands the market exactly on Q = 300.
      DWL         1/2 x 0.10 x 100 = $5 billion
      tax revenue 0.10 x 300 = $30 billion; consumers pay 0.25, producers keep 0.15.

  EDUCATION (Exhibits 9.4, 9.5, 9.9)   P in $ thousands, Q in millions of years
        D  (= marginal private benefit):  P = 80 - Q
        S  (= marginal social cost):      P = Q
        MSB (= D + marginal external benefit): P = 100 - Q
      market      Q = 40, P = 40
      optimal     Q = 50, P = 50,   MSB(40) = 60
      MEB         $20 thousand per year, constant -> Pigouvian subsidy = $20 thousand
      DWL         1/2 x 20 x 10 = 100 in the figure's own units

  PUBLIC vs PRIVATE GOODS (Exhibits 9.11, 9.12, 9.13)   two identical consumers
        each individual:  P = 80 - 10 Q
        private good, sum HORIZONTALLY:  P = 80 - 5 Q     (at P=50: 3 + 3 = 6)
        public good,  sum VERTICALLY:    P = 160 - 20 Q   (at Q=3: 50 + 50 = 100)
        supply for the public good:      P = 20 Q
      optimal provision  Q = 4 missions, P = $80.  This is Exhibit 9.13's intersection
      and it is the arithmetic check that fixes the vertical sum (see defect 2).

  REAL DATA ON FOUR FIGURES, and only these four.  All four are the publisher's own
  series, transcribed from the exhibits' accessibility descriptions; none is re-sourced
  and none needs re-checking before delivery, because none of it can go stale.
    quakes_ok    Exhibit 9.6, annual count of earthquakes in Oklahoma 2000-2019.
    quakes_ks    Exhibit 9.7, monthly count in Kansas by magnitude, Jan 2013 - Jul 2016,
                 around the March 2015 injection-rate order.
    giving       Exhibit 9.14, total US giving, selected years only, described by the
                 publisher as approximate - drawn as markers, NOT as a continuous line.
    congestion   Exhibit 9.16, London vehicle-kilometres 2002 vs 2003.

  THREE DEFECTS IN THE PUBLISHER'S OWN MATERIAL, all in the accessibility descriptions
  rather than in the drawn figures.  Recorded because a student using a screen reader
  gets the description, not the picture.

    1. Exhibit 9.9's description places the top of the subsidy brace at "(40, 60) on the
       supply curve".  Supply passes through (40, 40); (40, 60) is on MSB.  The drawn
       figure is right.
    2. Exhibit 9.12's description gives the summed public-good demand as running "(0,160)
       to (16,0)".  That is a horizontal-sum axis pasted onto a vertical-sum figure: the
       description's own sample point (3, 100) and Exhibit 9.13's intersection at (4, 80)
       both require P = 160 - 20Q, which reaches zero at Q = 8, and the drawn panel does
       run 0-8.  The drawn figure is right.  THIS IS THE ONE THAT MATTERS - a student
       who takes 16 gets the wrong optimal quantity in 9.13.
    3. Exhibit 9.16's description over-states the smaller categories relative to the drawn
       bars (it gives motorcycles 170 against roughly 125 drawn, buses 70 against roughly
       45).  The direction of every change is the same either way.  The description's
       numbers are used below because they are the publisher's stated values, but NO
       per-category figure should be quoted aloud - only the pattern, and the cars number,
       which agrees to within two points either way (-36% described, -34% drawn).

Run:  python3 ch09_charts.py [outdir]
"""
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# ----------------------------------------------------------------- house style
BLUE = "#003DA5"      # demand / marginal benefit
RED = "#CC3333"       # supply / marginal cost
GREEN = "#2E7D32"     # the social optimum, the "right" answer
DGOLD = "#B88300"     # the wedge: marginal external cost or benefit
GOLD = "#FFB81D"
INK = "#333333"
GREY = "#666666"
LGREY = "#BBBBBB"
TINT_GREEN = "#E4F0E4"
TINT_RED = "#F7DEDE"
TINT_BLUE = "#DCE6F5"
TINT_GOLD = "#FBEFCF"
TINT_GREY = "#EDEDED"

plt.rcParams.update({
    "font.family": "Liberation Sans",
    "font.size": 11,
    "axes.edgecolor": "#888888",
    "axes.linewidth": 0.9,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": GREY,
    "ytick.color": GREY,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.06,
})

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)

# Any annotation inside the axes gets a white bbox by default.  Ch08 spent three render
# passes moving labels that this would have fixed at once.
BOX = dict(fc="white", ec="none", alpha=0.90, pad=1.6)


def save(fig, name):
    p = os.path.join(OUT, "ch09_fig_%s.png" % name)
    fig.savefig(p, facecolor="white")
    plt.close(fig)
    print("  ", os.path.basename(p))


# ============================================================ PRIMITIVES: ELECTRICITY
# P in dollars per kWh, Q in billions of kWh per year.
E_INT, E_SLOPE = 0.40, 0.0005          # demand
E_SUP = 0.0005                         # supply (= marginal private cost)
MEC = 0.10                             # marginal external cost, constant


def e_d(q):
    return E_INT - E_SLOPE * q


def e_s(q):
    return E_SUP * q


def e_msc(q):
    return e_s(q) + MEC


E_QM = round((E_INT) / (E_SLOPE + E_SUP), 9)          # 400
E_PM = e_d(E_QM)                                      # 0.20
E_QO = round((E_INT - MEC) / (E_SLOPE + E_SUP), 9)    # 300
E_PO = e_d(E_QO)                                      # 0.25
E_DWL = 0.5 * MEC * (E_QM - E_QO)                     # 5.0  ($ billion)
E_TAXREV = MEC * E_QO                                 # 30.0 ($ billion)
E_PPROD = E_PO - MEC                                  # 0.15, what producers keep

assert E_QM == 400 and abs(E_PM - 0.20) < 1e-12, "Exhibit 9.1 equilibrium is (400, 0.20)"
assert E_QO == 300 and abs(E_PO - 0.25) < 1e-12, "Exhibit 9.2 optimum is (300, 0.25)"
assert abs(e_msc(E_QM) - 0.30) < 1e-12, "Exhibit 9.3 puts MSC(400) at 0.30"
assert abs(E_DWL - 5.0) < 1e-9, "Exhibit 9.3 deadweight loss must be $5 billion"
assert abs(E_TAXREV - 30.0) < 1e-9
assert abs(E_PPROD - 0.15) < 1e-12
# the tax works ONLY because MEC is constant: supply + tax must BE the MSC curve
assert all(abs((e_s(q) + MEC) - e_msc(q)) < 1e-12 for q in (0, 100, 300, 400, 800)), \
    "a constant per-unit tax reproduces MSC only when the external cost is constant"
assert E_QO < E_QM, "a negative externality means the market OVER-produces"
# and the optimum is not zero - which is the answer to the cold open
assert E_QO > 0, "the socially optimal quantity of a polluting good is not zero"

# ============================================================ PRIMITIVES: EDUCATION
# P in thousands of dollars, Q in millions of years of schooling.
MEB = 20.0                             # marginal external benefit, constant


def u_d(q):
    return 80.0 - q


def u_s(q):
    return q


def u_msb(q):
    return u_d(q) + MEB


U_QM = 40.0
U_PM = u_d(U_QM)                                      # 40
U_QO = 50.0
U_PO = u_s(U_QO)                                      # 50
U_DWL = 0.5 * MEB * (U_QO - U_QM)                     # 100

assert abs(u_d(U_QM) - u_s(U_QM)) < 1e-12 and U_PM == 40, "Exhibit 9.4 is (40, 40)"
assert abs(u_msb(U_QO) - u_s(U_QO)) < 1e-12 and U_PO == 50, "Exhibit 9.5 optimum is (50, 50)"
assert abs(u_msb(U_QM) - 60.0) < 1e-12, "Exhibit 9.9 brace runs from (40,40) to (40,60)"
assert abs(U_DWL - 100.0) < 1e-9
assert U_QO > U_QM, "a positive externality means the market UNDER-produces"

# ================================================== PRIMITIVES: PRIVATE vs PUBLIC GOODS
N_CONSUMERS = 2
IND_INT, IND_SLOPE = 80.0, 10.0        # each individual: P = 80 - 10Q


def ind_d(q):
    return IND_INT - IND_SLOPE * q


def priv_mkt(q):                       # horizontal sum: P = 80 - 5Q
    return IND_INT - (IND_SLOPE / N_CONSUMERS) * q


def pub_mkt(q):                        # vertical sum: P = 160 - 20Q
    return N_CONSUMERS * ind_d(q)


def pub_s(q):                          # Exhibit 9.13 supply
    return 20.0 * q


# horizontal sum: at a common PRICE, quantities add
assert abs(ind_d(3) - 50.0) < 1e-12 and abs(priv_mkt(6) - 50.0) < 1e-12, \
    "Exhibit 9.11: each buys 3 pairs at $50, the market buys 6"
assert abs(priv_mkt(16)) < 1e-12, "Exhibit 9.11 panel (c) reaches zero at Q = 16"
# vertical sum: at a common QUANTITY, prices add
assert abs(pub_mkt(3) - 100.0) < 1e-12, \
    "Exhibit 9.12: each values the 3rd mission at $50, so society values it at $100"
assert abs(pub_mkt(8)) < 1e-12, "Exhibit 9.12 panel (c) reaches zero at Q = 8, NOT 16"
PUB_QO = round(160.0 / 40.0, 9)                       # 4
assert abs(pub_mkt(PUB_QO) - pub_s(PUB_QO)) < 1e-12 and PUB_QO == 4
assert abs(pub_s(PUB_QO) - 80.0) < 1e-12, "Exhibit 9.13 optimum is (4, $80)"
# and this is the check that condemns the alt-text's Q=16 reading of Exhibit 9.12
assert abs((160.0 - 10.0 * PUB_QO) - pub_s(PUB_QO)) > 1e-6, \
    "if the summed curve reached zero at 16 the optimum would not be 4 missions"

# ============================================================ PRIMITIVES: COASE
# Acemoglu's bargaining table (deck slides 22-23): profits per day, dollars.
FRED_NO, ANNE_NO = 130.0, 90.0         # without the filter
FRED_YES, ANNE_YES = 100.0, 140.0      # with the filter
FRED_LOSS = FRED_NO - FRED_YES         # 30
ANNE_GAIN = ANNE_YES - ANNE_NO         # 50
SOCIAL_GAIN = ANNE_GAIN - FRED_LOSS    # 20
PAYMENT = 35.0                         # the worked example

assert FRED_NO + ANNE_NO == 220.0 and FRED_YES + ANNE_YES == 240.0
assert (FRED_YES + ANNE_YES) - (FRED_NO + ANNE_NO) == SOCIAL_GAIN == 20.0
assert FRED_LOSS < PAYMENT < ANNE_GAIN, "the payment must lie strictly between 30 and 50"
assert (FRED_YES + PAYMENT) > FRED_NO and (ANNE_YES - PAYMENT) > ANNE_NO, \
    "both parties must end up better off than without the filter"
assert (FRED_YES + PAYMENT - FRED_NO) + (ANNE_YES - PAYMENT - ANNE_NO) == SOCIAL_GAIN, \
    "the two private gains must exhaust the social gain - the payment only splits it"

# Mateer & Coppock's rancher / wheat farmer (their Chapter 7 slides 20-22), which runs
# the SAME bargain under BOTH assignments of the property right.  Acemoglu's table runs
# one direction only, so this is what makes the invariance visible.
FENCE = 25000.0
DAMAGE_HIGH, DAMAGE_LOW = 30000.0, 20000.0

# whoever bears the cost picks the cheaper of (build the fence) and (accept the damage)
assert min(FENCE, DAMAGE_HIGH) == FENCE, "with damage of $30,000 the fence is efficient"
assert min(FENCE, DAMAGE_LOW) == DAMAGE_LOW, "with damage of $20,000 no fence is efficient"
# ... and that choice does not depend on WHO bears it.  That is the Coase theorem.
for damage in (DAMAGE_HIGH, DAMAGE_LOW):
    rancher_liable = min(FENCE, damage)
    farmer_bears = min(FENCE, damage)
    assert rancher_liable == farmer_bears, \
        "the efficient action must not depend on who holds the property right"

# ================================== PRIMITIVES: THE OKLAHOMA COST-BENEFIT PROBLEM
# The publisher's own end-of-chapter Evidence-Based Economics problem.  Worked here
# because THEIR ANSWER KEY IS WRONG on part (b) - see the assertion.
OK_POP = 4_000_000
OK_ABATEMENT_COST = 1_000_000_000          # what lower injection rates cost the industry

OK_WTP_FLAT = 100.0                        # part (a): every resident values it at $100
OK_BENEFIT_A = OK_WTP_FLAT * OK_POP        # 400,000,000
OK_NET_A = OK_BENEFIT_A - OK_ABATEMENT_COST

OK_WTP_SPLIT = (500.0 + 50.0) / 2          # part (b): half at $500, half at $50
OK_BENEFIT_B = OK_WTP_SPLIT * OK_POP       # 1,100,000,000
OK_NET_B = OK_BENEFIT_B - OK_ABATEMENT_COST

assert OK_BENEFIT_A == 400_000_000 and OK_NET_A == -600_000_000, \
    "part (a): $400m of benefit against $1bn of cost, so a net loss of $600m"
assert OK_WTP_SPLIT == 275.0
assert OK_BENEFIT_B == 1_100_000_000
# THE PUBLISHER'S KEY SAYS "a net gain of $1 million".  1.1bn - 1.0bn = 100 MILLION.
assert OK_NET_B == 100_000_000, \
    "part (b) nets $100 million, not the $1 million the publisher's answer key states"
assert OK_NET_B == 100 * 1_000_000, "the key is out by a factor of one hundred"
# and it is a gain to SOCIETY, not "to industry" - industry is the party bearing the cost
assert OK_NET_A < 0 < OK_NET_B, "the decision flips between the two valuations"


# ============================================================ PRIMITIVES: THE COMMONS
# Mateer & Coppock's grazing commons (their slide 33).
COMMONS_CAPACITY = 100                 # cows the commons sustains indefinitely
COMMONS_FARMERS = 100
COMMONS_EACH = 1
assert COMMONS_FARMERS * COMMONS_EACH == COMMONS_CAPACITY, "one cow each exactly fills it"
COMMONS_IF_ALL_ADD = COMMONS_FARMERS * (COMMONS_EACH + 1)      # 200
assert COMMONS_IF_ALL_ADD == 2 * COMMONS_CAPACITY
# the asymmetry that drives it: one farmer keeps ALL of the extra cow's benefit but
# bears only 1/100th of the extra damage.
COMMONS_PRIVATE_SHARE = 1.0
COMMONS_COST_SHARE = 1.0 / COMMONS_FARMERS                     # 0.01
assert COMMONS_PRIVATE_SHARE > COMMONS_COST_SHARE * COMMONS_FARMERS - 1e-9

# ============================================================ REAL SERIES (publisher)
# Exhibit 9.6 - annual earthquakes in Oklahoma.
OK_YEARS = list(range(2000, 2020))
OK_COUNT = [0, 0, 3, 0, 2, 1, 3, 1, 2, 20, 41, 63, 34, 103, 585, 887, 639, 272, 166, 57]
assert len(OK_YEARS) == len(OK_COUNT) == 20
assert max(OK_COUNT) == 887 and OK_COUNT[OK_YEARS.index(2015)] == 887

# Exhibit 9.7 - monthly earthquakes in Kansas by magnitude, around the March 2015 order.
# (year, month): (M2, M3, M4).  Months not listed by the publisher are zero.
KS = {
    (2013, 1): (0, 1, 0), (2013, 9): (1, 0, 0), (2013, 10): (1, 0, 0), (2013, 12): (0, 1, 0),
    (2014, 2): (1, 2, 0), (2014, 3): (5, 4, 0), (2014, 4): (3, 2, 0), (2014, 5): (2, 0, 0),
    (2014, 6): (5, 0, 0), (2014, 7): (3, 1, 0), (2014, 8): (4, 4, 0), (2014, 9): (1, 4, 0),
    (2014, 10): (18, 12, 1), (2014, 11): (19, 6, 1), (2014, 12): (17, 4, 0),
    (2015, 1): (21, 5, 0), (2015, 2): (23, 16, 0), (2015, 3): (33, 9, 0),
    (2015, 4): (23, 10, 0), (2015, 5): (17, 7, 0), (2015, 6): (7, 17, 5),
    (2015, 7): (19, 0, 0), (2015, 8): (26, 2, 0), (2015, 9): (56, 9, 0),
    (2015, 10): (23, 9, 0), (2015, 11): (14, 7, 0), (2015, 12): (6, 0, 0),
    (2016, 1): (5, 0, 0), (2016, 2): (2, 1, 0), (2016, 3): (5, 0, 0), (2016, 4): (4, 0, 0),
    (2016, 5): (3, 1, 0), (2016, 6): (3, 4, 0), (2016, 7): (1, 4, 0),
}
KS_ORDER_YM = (2015, 3)                # the March 2015 command-and-control order
assert KS_ORDER_YM in KS
_pre = sum(sum(v) for k, v in KS.items() if (k[0], k[1]) >= (2014, 10) and k < KS_ORDER_YM)
_post = sum(sum(v) for k, v in KS.items() if k >= (2015, 12))
assert _pre > _post, "the point of Exhibit 9.7 is that activity fell after the order"

# Exhibit 9.14 - total US giving, SELECTED years, publisher-described as approximate.
GIVE_YEARS = [1978, 1980, 1985, 1986, 1992, 1995, 1996, 1998, 2000,
              2004, 2005, 2006, 2008, 2012, 2016, 2018]
GIVE_VALUE = [150, 150, 170, 200, 200, 200, 245, 280, 350,
              340, 400, 375, 350, 375, 450, 440]
assert len(GIVE_YEARS) == len(GIVE_VALUE)
assert GIVE_VALUE[GIVE_YEARS.index(2008)] < GIVE_VALUE[GIVE_YEARS.index(2005)], \
    "the teaching point is that giving FELL into the recession"

# Exhibit 9.15 - share answering yes to "have you donated money in the past month?", 2018.
REGIONS = ["Australia & NZ", "North America", "Western Europe", "Southeastern Asia",
           "Northern Europe", "Central Asia", "Eastern Asia", "Southern Europe",
           "Southern Asia", "Western Asia", "Caribbean", "Eastern Africa",
           "Eastern Europe", "Central America", "South America", "Western Africa",
           "Northern Africa", "Middle Africa", "Southern Africa"]
REGION_PCT = [70, 59, 51, 50, 48, 35, 34, 31, 29, 26, 25, 24, 23, 21, 19, 18, 16, 15, 10]
assert len(REGIONS) == len(REGION_PCT) == 19
assert REGION_PCT == sorted(REGION_PCT, reverse=True)

# Exhibit 9.16 - London vehicle-kilometres, 2002 vs 2003.  Publisher's stated values.
VEH = ["Cars", "Vans", "Trucks", "Taxis", "Buses", "Motorcycles", "Bicycles"]
VEH_2002 = [780, 295, 80, 280, 70, 170, 75]
VEH_2003 = [500, 290, 75, 350, 75, 180, 100]
assert len(VEH) == len(VEH_2002) == len(VEH_2003)
CAR_DROP = (VEH_2003[0] - VEH_2002[0]) / VEH_2002[0]
assert -0.37 < CAR_DROP < -0.35, "car use fell by about a third"
assert VEH_2003[VEH.index("Taxis")] > VEH_2002[VEH.index("Taxis")]
assert VEH_2003[VEH.index("Bicycles")] > VEH_2002[VEH.index("Bicycles")]


# ====================================================================== helpers
def money(x, _=None):
    return r"\$%.2f" % x


def _elec_axes(ax):
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 0.40)
    ax.set_xticks(range(0, 900, 100))
    ax.set_yticks(np.arange(0, 0.41, 0.05))
    ax.set_yticklabels([r"\$%.2f" % v for v in np.arange(0, 0.41, 0.05)])
    ax.set_xlabel("Quantity of electricity (billions of kWh)")
    ax.set_ylabel("Price (per kWh)")


def _drop(ax, q, p, color=GREY):
    ax.plot([q, q], [0, p], ls=":", lw=1.0, color=color, zorder=1)
    ax.plot([0, q], [p, p], ls=":", lw=1.0, color=color, zorder=1)


# ============================================================== 1. Exhibit 9.1
def elec_market():
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    q = np.linspace(0, 800, 400)
    ax.plot(q, e_d(q), color=BLUE, lw=2.6, zorder=3)
    ax.plot(q, e_s(q), color=RED, lw=2.6, zorder=3)
    ax.text(730, e_d(730) - 0.012, "D", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(700, e_s(700) + 0.008, "S", color=RED, fontsize=13, fontweight="bold")
    _drop(ax, E_QM, E_PM)
    ax.plot([E_QM], [E_PM], "o", ms=8, mfc="white", mec=INK, mew=1.6, zorder=5)
    ax.annotate(r"market equilibrium" "\n" r"400 billion kWh at \$0.20",
                xy=(E_QM, E_PM), xytext=(470, 0.295), fontsize=10.5, color=INK,
                bbox=BOX, arrowprops=dict(arrowstyle="-", color=GREY, lw=1.0))
    _elec_axes(ax)
    ax.set_title("The market for electricity, with nobody counting the smoke",
                 fontsize=11.5, color=GREY, loc="left", pad=8)
    save(fig, "elec_market")


# ============================================================== 2. Exhibit 9.2
def elec_msc():
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    q = np.linspace(0, 800, 400)
    ax.plot(q, e_d(q), color=BLUE, lw=2.6, zorder=3)
    ax.plot(q, e_s(q), color=RED, lw=2.6, zorder=3)
    ax.plot(q, e_msc(q), color=DGOLD, lw=2.6, zorder=3)
    ax.text(730, e_d(730) - 0.012, "D", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(640, e_s(640) - 0.030, "S = marginal cost", color=RED, fontsize=10.5,
            fontweight="bold", bbox=BOX)
    ax.text(430, e_msc(430) + 0.018, "MSC = marginal cost + marginal external cost",
            color=DGOLD, fontsize=10.5, fontweight="bold", bbox=BOX)
    _drop(ax, E_QM, E_PM)
    _drop(ax, E_QO, E_PO, color=GREEN)
    ax.plot([E_QM], [E_PM], "o", ms=8, mfc="white", mec=INK, mew=1.6, zorder=5)
    ax.plot([E_QO], [E_PO], "o", ms=8, mfc=GREEN, mec="white", mew=1.6, zorder=5)
    # the wedge, drawn at the market quantity
    ax.annotate("", xy=(E_QM, e_msc(E_QM)), xytext=(E_QM, E_PM),
                arrowprops=dict(arrowstyle="<->", color=DGOLD, lw=1.8))
    ax.text(E_QM + 14, (E_PM + e_msc(E_QM)) / 2, r"marginal external" "\n" r"cost = \$0.10",
            color=DGOLD, fontsize=10, fontweight="bold", va="center", bbox=BOX)
    ax.text(E_QO - 14, 0.335, "socially\noptimal\n300", color=GREEN, fontsize=10,
            fontweight="bold", ha="right", va="top", bbox=BOX)
    ax.text(E_QM + 8, 0.055, "market\n400", color=INK, fontsize=10, va="top", bbox=BOX)
    _elec_axes(ax)
    ax.set_title("Adding the cost the plant does not pay", fontsize=11.5,
                 color=GREY, loc="left", pad=8)
    save(fig, "elec_msc")


# ============================================================== 3. Exhibit 9.3
def elec_dwl():
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    q = np.linspace(0, 800, 400)
    tri = [(E_QO, E_PO), (E_QM, E_PM), (E_QM, e_msc(E_QM))]
    ax.add_patch(Polygon(tri, closed=True, fc=TINT_GOLD, ec=DGOLD, lw=1.2, zorder=2))
    ax.plot(q, e_d(q), color=BLUE, lw=2.6, zorder=3)
    ax.plot(q, e_s(q), color=RED, lw=2.6, zorder=3)
    ax.plot(q, e_msc(q), color=DGOLD, lw=2.6, zorder=3)
    ax.text(730, e_d(730) - 0.012, "D", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(690, e_s(690) - 0.030, "S", color=RED, fontsize=13, fontweight="bold", bbox=BOX)
    ax.text(600, e_msc(600) + 0.012, "MSC", color=DGOLD, fontsize=12,
            fontweight="bold", bbox=BOX)
    _drop(ax, E_QM, E_PM)
    _drop(ax, E_QO, E_PO, color=GREEN)
    ax.plot([E_QM], [E_PM], "o", ms=8, mfc="white", mec=INK, mew=1.6, zorder=5)
    ax.plot([E_QO], [E_PO], "o", ms=8, mfc=GREEN, mec="white", mew=1.6, zorder=5)
    ax.annotate("every unit from 300 to 400 costs society\n"
                "more than it is worth to the buyer\n"
                r"deadweight loss = $\bf{\$5\ billion}$",
                xy=(365, 0.245), xytext=(470, 0.30), fontsize=10.5, color=INK,
                bbox=BOX, arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.2))
    _elec_axes(ax)
    ax.set_title("The cost of the externality, as an area", fontsize=11.5,
                 color=GREY, loc="left", pad=8)
    save(fig, "elec_dwl")


# ============================================================== 4. Exhibit 9.8
def elec_tax():
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    q = np.linspace(0, 800, 400)
    ax.plot(q, e_d(q), color=BLUE, lw=2.6, zorder=3)
    ax.plot(q, e_s(q), color=RED, lw=2.0, ls=(0, (5, 3)), zorder=3)
    ax.plot(q, e_msc(q), color=RED, lw=2.6, zorder=4)
    ax.text(730, e_d(730) - 0.012, "D", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(690, e_s(690) - 0.032, "S before the tax", color=RED, fontsize=10,
            bbox=BOX)
    ax.text(400, e_msc(400) + 0.030, "S after the tax = MSC", color=RED, fontsize=10.5,
            fontweight="bold", bbox=BOX)
    _drop(ax, E_QO, E_PO, color=GREEN)
    ax.plot([E_QM], [E_PM], "o", ms=7, mfc="white", mec=LGREY, mew=1.4, zorder=5)
    ax.plot([E_QO], [E_PO], "o", ms=8, mfc=GREEN, mec="white", mew=1.6, zorder=6)
    ax.annotate("", xy=(E_QO, E_PO), xytext=(E_QO, E_PPROD),
                arrowprops=dict(arrowstyle="<->", color=DGOLD, lw=1.8))
    ax.text(E_QO - 14, (E_PO + E_PPROD) / 2,
            "tax = \$0.10\n= the marginal external cost",
            color=DGOLD, fontsize=10.5, fontweight="bold", ha="right", va="center",
            bbox=BOX)
    ax.text(E_QO - 14, 0.335, "the market now\nchooses 300", color=GREEN, fontsize=10,
            fontweight="bold", ha="right", va="top", bbox=BOX)
    ax.text(E_QM + 12, E_PM + 0.006, "old equilibrium", color=GREY, fontsize=9.5,
            va="bottom", bbox=BOX)
    _elec_axes(ax)
    ax.set_title("A Pigouvian tax makes the firm's own curve tell the truth",
                 fontsize=11.5, color=GREY, loc="left", pad=8)
    save(fig, "elec_tax")


# =========================================================== 5. Exhibits 9.4 / 9.5
def _educ_axes(ax):
    ax.set_xlim(0, 80)
    ax.set_ylim(0, 80)
    ax.set_xticks(range(0, 81, 10))
    ax.set_yticks(range(0, 81, 10))
    ax.set_yticklabels([r"\$%d" % v for v in range(0, 81, 10)])
    ax.set_xlabel("Quantity of education (millions of years)")
    ax.set_ylabel("Price (thousands)")


def educ_dwl():
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    q = np.linspace(0, 80, 400)
    tri = [(U_QM, U_PM), (U_QM, u_msb(U_QM)), (U_QO, U_PO)]
    ax.add_patch(Polygon(tri, closed=True, fc=TINT_GOLD, ec=DGOLD, lw=1.2, zorder=2))
    ax.plot(q, u_d(q), color=BLUE, lw=2.6, zorder=3)
    ax.plot(q, u_msb(q), color=DGOLD, lw=2.6, zorder=3)
    ax.plot(q, u_s(q), color=RED, lw=2.6, zorder=3)
    ax.text(66, u_d(66) - 5, "D = marginal benefit", color=BLUE, fontsize=10.5,
            fontweight="bold", ha="right", bbox=BOX)
    ax.text(13, 74, "MSB = marginal benefit\n+ marginal external benefit",
            color=DGOLD, fontsize=10, fontweight="bold", ha="left", va="top", bbox=BOX)
    ax.text(70, u_s(70) + 2, "S", color=RED, fontsize=13, fontweight="bold", bbox=BOX)
    _drop(ax, U_QM, U_PM)
    _drop(ax, U_QO, U_PO, color=GREEN)
    ax.plot([U_QM], [U_PM], "o", ms=8, mfc="white", mec=INK, mew=1.6, zorder=5)
    ax.plot([U_QO], [U_PO], "o", ms=8, mfc=GREEN, mec="white", mew=1.6, zorder=5)
    ax.annotate("the years between 40 and 50 were\nworth more than they cost",
                xy=(45, 49), xytext=(10, 26), fontsize=10.5, color=INK, bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.2))
    ax.text(U_QM - 2, 76, "market\n40", color=INK, fontsize=10, ha="right",
            va="top", bbox=BOX)
    ax.text(U_QO + 2, 76, "socially optimal\n50", color=GREEN, fontsize=10,
            fontweight="bold", va="top", bbox=BOX)
    _educ_axes(ax)
    ax.set_title("A positive externality: the market stops too early",
                 fontsize=11.5, color=GREY, loc="left", pad=8)
    save(fig, "educ_dwl")


# ============================================================== 6. Exhibit 9.9
def educ_subsidy():
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    q = np.linspace(0, 80, 400)
    ax.plot(q, u_d(q), color=BLUE, lw=2.0, ls=(0, (5, 3)), zorder=3)
    ax.plot(q, u_msb(q), color=BLUE, lw=2.6, zorder=4)
    ax.plot(q, u_s(q), color=RED, lw=2.6, zorder=3)
    ax.text(72, u_d(72) - 5, "D before the subsidy", color=BLUE, fontsize=10,
            ha="right", bbox=BOX)
    ax.text(78, u_msb(78) + 3, "D after the subsidy = MSB", color=BLUE,
            fontsize=10.5, fontweight="bold", ha="right", bbox=BOX)
    ax.text(70, u_s(70) + 2, "S", color=RED, fontsize=13, fontweight="bold", bbox=BOX)
    _drop(ax, U_QO, U_PO, color=GREEN)
    ax.plot([U_QM], [U_PM], "o", ms=7, mfc="white", mec=LGREY, mew=1.4, zorder=5)
    ax.plot([U_QO], [U_PO], "o", ms=8, mfc=GREEN, mec="white", mew=1.6, zorder=6)
    ax.annotate("", xy=(U_QM, u_msb(U_QM)), xytext=(U_QM, U_PM),
                arrowprops=dict(arrowstyle="<->", color=DGOLD, lw=1.8))
    ax.text(U_QM - 2, (U_PM + u_msb(U_QM)) / 2,
            "subsidy = \$20 thousand\n= the marginal external benefit",
            color=DGOLD, fontsize=10, fontweight="bold", ha="right", va="center", bbox=BOX)
    ax.text(U_QO + 2, 76, "consumption rises\nto 50", color=GREEN, fontsize=10,
            fontweight="bold", va="top", bbox=BOX)
    _educ_axes(ax)
    ax.set_title("A Pigouvian subsidy pays the buyer what the bystander gains",
                 fontsize=11.5, color=GREY, loc="left", pad=8)
    save(fig, "educ_subsidy")


# ============================================== 7. the two cases side by side
def neg_pos():
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))
    q = np.linspace(0, 800, 300)
    ax = axes[0]
    ax.plot(q, e_d(q), color=BLUE, lw=2.4)
    ax.plot(q, e_s(q), color=RED, lw=2.4)
    ax.plot(q, e_msc(q), color=DGOLD, lw=2.4)
    ax.plot([E_QM], [E_PM], "o", ms=7, mfc="white", mec=INK, mew=1.5, zorder=5)
    ax.plot([E_QO], [E_PO], "o", ms=7, mfc=GREEN, mec="white", mew=1.5, zorder=5)
    ax.plot([E_QM, E_QM], [0, E_PM], ls=":", lw=1.0, color=GREY)
    ax.plot([E_QO, E_QO], [0, E_PO], ls=":", lw=1.0, color=GREEN)
    ax.text(760, e_d(760), "D", color=BLUE, fontsize=12, fontweight="bold", bbox=BOX)
    ax.text(690, e_s(690) - 0.035, "S", color=RED, fontsize=12, fontweight="bold", bbox=BOX)
    ax.text(560, e_msc(560) + 0.012, "MSC", color=DGOLD, fontsize=11,
            fontweight="bold", bbox=BOX)
    ax.annotate("", xy=(E_QM, 0.028), xytext=(E_QO, 0.028),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.text((E_QO + E_QM) / 2, 0.045, "too much", ha="center", fontsize=11,
            fontweight="bold", color=RED, bbox=BOX)
    ax.set_xlim(0, 800); ax.set_ylim(0, 0.40)
    ax.set_xticks([E_QO, E_QM]); ax.set_xticklabels(["300\noptimal", "400\nmarket"])
    ax.set_yticks([])
    ax.set_title("NEGATIVE externality: a cost lands on a bystander",
                 fontsize=11, color=RED, loc="left", fontweight="bold", pad=8)
    ax.set_xlabel("the extra cost sits ABOVE supply, so the optimum is to the LEFT")

    ax = axes[1]
    q2 = np.linspace(0, 80, 300)
    ax.plot(q2, u_d(q2), color=BLUE, lw=2.4)
    ax.plot(q2, u_msb(q2), color=DGOLD, lw=2.4)
    ax.plot(q2, u_s(q2), color=RED, lw=2.4)
    ax.plot([U_QM], [U_PM], "o", ms=7, mfc="white", mec=INK, mew=1.5, zorder=5)
    ax.plot([U_QO], [U_PO], "o", ms=7, mfc=GREEN, mec="white", mew=1.5, zorder=5)
    ax.plot([U_QM, U_QM], [0, U_PM], ls=":", lw=1.0, color=GREY)
    ax.plot([U_QO, U_QO], [0, U_PO], ls=":", lw=1.0, color=GREEN)
    ax.text(76, u_d(76), "D", color=BLUE, fontsize=12, fontweight="bold", bbox=BOX)
    ax.text(70, u_s(70) + 3, "S", color=RED, fontsize=12, fontweight="bold", bbox=BOX)
    ax.text(62, u_msb(62) + 4, "MSB", color=DGOLD, fontsize=11,
            fontweight="bold", bbox=BOX)
    ax.annotate("", xy=(U_QO, 5), xytext=(U_QM, 5),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.text((U_QO + U_QM) / 2, 8.5, "too little", ha="center", fontsize=11,
            fontweight="bold", color=GREEN, bbox=BOX)
    ax.set_xlim(0, 80); ax.set_ylim(0, 80)
    ax.set_xticks([U_QM, U_QO]); ax.set_xticklabels(["40\nmarket", "50\noptimal"])
    ax.set_yticks([])
    ax.set_title("POSITIVE externality: a benefit lands on a bystander",
                 fontsize=11, color=GREEN, loc="left", fontweight="bold", pad=8)
    ax.set_xlabel("the extra benefit sits ABOVE demand, so the optimum is to the RIGHT")
    fig.tight_layout()
    save(fig, "neg_pos")


# ================================================= 8. Exhibits 9.6 and 9.7
def quakes():
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))
    ax = axes[0]
    ax.bar(OK_YEARS, OK_COUNT, color=BLUE, width=0.72)
    ax.set_xlim(1999.2, 2019.8)
    ax.set_xticks(range(2000, 2020, 3))
    ax.set_ylabel("Earthquakes per year")
    ax.set_title("Oklahoma, 2000-2019", fontsize=11.5, color=INK,
                 loc="left", fontweight="bold", pad=8)
    ax.annotate("887 in 2015", xy=(2015, 887), xytext=(2007.5, 780), fontsize=10.5,
                color=INK, bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.1))
    ax.set_xlabel("wastewater from fracking, injected deep, triggering old faults")

    ax = axes[1]
    keys = sorted(KS)
    xs = [(y - 2013) * 12 + m for y, m in keys]
    m2 = [KS[k][0] for k in keys]
    m3 = [KS[k][1] for k in keys]
    m4 = [KS[k][2] for k in keys]
    ax.bar(xs, m2, color=BLUE, width=0.85, label="magnitude 2")
    ax.bar(xs, m3, bottom=m2, color=DGOLD, width=0.85, label="magnitude 3")
    ax.bar(xs, m4, bottom=[a + b for a, b in zip(m2, m3)], color=RED, width=0.85,
           label="magnitude 4")
    order_x = (KS_ORDER_YM[0] - 2013) * 12 + KS_ORDER_YM[1]
    ax.axvline(order_x, color=GREEN, lw=2.0, ls="--", zorder=5)
    ax.text(order_x + 1.0, 85, "March 2015\ninjection caps ordered", color=GREEN,
            fontsize=10, fontweight="bold", ha="left", va="top", bbox=BOX)
    ticks = [(y - 2013) * 12 + 1 for y in range(2013, 2017)]
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(y) for y in range(2013, 2017)])
    ax.set_xlim(min(xs) - 1, max(xs) + 1)
    ax.set_ylim(0, 88)
    ax.set_ylabel("Earthquakes per month")
    ax.set_title("Kansas, before and after a command-and-control order",
                 fontsize=11.5, color=INK, loc="left", fontweight="bold", pad=8)
    ax.legend(frameon=False, fontsize=9.5, loc="upper left", bbox_to_anchor=(0.0, 1.0))
    ax.set_xlabel("the order capped saltwater injection at 16,000 then 8,000 barrels a day")
    fig.tight_layout()
    save(fig, "quakes")


# ============================================ 9. Exhibits 9.11 and 9.12 contrasted
def summation():
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))
    qi = np.linspace(0, 8, 200)

    ax = axes[0]
    ax.plot(qi, ind_d(qi), color=LGREY, lw=1.8)
    ax.plot(qi, ind_d(qi), color=LGREY, lw=1.8)
    qm = np.linspace(0, 16, 200)
    ax.plot(qm, priv_mkt(qm), color=BLUE, lw=2.8, zorder=4)
    ax.text(7.8, ind_d(6.6) + 5, "you (and Jim,\nidentical)", color=GREY, fontsize=10,
            ha="center", bbox=BOX)
    ax.text(15.6, priv_mkt(13.4), "market demand", color=BLUE, fontsize=10.5,
            fontweight="bold", ha="right", bbox=BOX)
    ax.plot([3, 3], [0, 50], ls=":", lw=1.0, color=GREY)
    ax.plot([6, 6], [0, 50], ls=":", lw=1.0, color=GREY)
    ax.plot([0, 6], [50, 50], ls=":", lw=1.0, color=GREY)
    ax.annotate("", xy=(3, 50), xytext=(0, 50),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
    ax.annotate("", xy=(6, 50), xytext=(3, 50),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
    ax.plot([3, 6], [50, 50], "o", ms=6, mfc=GREEN, mec="white", mew=1.2, zorder=6)
    ax.text(3.0, 74, r"3 + 3 = 6", color=GREEN, fontsize=12, fontweight="bold",
            ha="center", bbox=BOX)
    ax.text(7.4, 96, r"at \$50 each of you buys 3," "\n" "so the market buys 6",
            color=GREEN, fontsize=10.5, fontweight="bold", bbox=BOX)
    ax.set_xlim(0, 16); ax.set_ylim(0, 200)
    ax.set_xticks(range(0, 17, 2))
    ax.set_yticks(range(0, 201, 40))
    ax.set_yticklabels([r"\$%d" % v for v in range(0, 201, 40)])
    ax.set_xlabel("Pairs of jeans")
    ax.set_ylabel("Price")
    ax.set_title("PRIVATE good: add the quantities SIDEWAYS", fontsize=11.5,
                 color=INK, loc="left", fontweight="bold", pad=8)

    ax = axes[1]
    ax.plot(qi, ind_d(qi), color=LGREY, lw=1.8)
    ax.plot(qi, pub_mkt(qi), color=BLUE, lw=2.8, zorder=4)
    ax.text(9.4, ind_d(6.4), "you (and Jim,\nidentical)", color=GREY, fontsize=10,
            ha="left", bbox=BOX)
    ax.text(9.4, pub_mkt(5.9), "market demand", color=BLUE, fontsize=10.5,
            fontweight="bold", ha="left", bbox=BOX)
    ax.plot([3, 3], [0, 100], ls=":", lw=1.0, color=GREY)
    ax.annotate("", xy=(3, 50), xytext=(3, 0),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
    ax.annotate("", xy=(3, 100), xytext=(3, 50),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
    ax.plot([3, 3], [50, 100], "o", ms=6, mfc=GREEN, mec="white", mew=1.2, zorder=6)
    ax.text(3.9, 75, r"\$50 + \$50 = \$100", color=GREEN, fontsize=12,
            fontweight="bold", va="center", bbox=BOX)
    ax.text(4.6, 148, "the 3rd mission is worth \$50 to each\n"
                      r"of you, so it is worth \$100 to society",
            color=GREEN, fontsize=10.5, fontweight="bold", ha="center", bbox=BOX)
    ax.set_xlim(0, 16); ax.set_ylim(0, 200)
    ax.set_xticks(range(0, 17, 2))
    ax.set_yticks(range(0, 201, 40))
    ax.set_yticklabels([r"\$%d" % v for v in range(0, 201, 40)])
    ax.set_xlabel("Space missions")
    ax.set_ylabel("Price")
    ax.set_title("PUBLIC good: add the prices UPWARDS", fontsize=11.5,
                 color=INK, loc="left", fontweight="bold", pad=8)
    fig.tight_layout()
    save(fig, "summation")


# ============================================================= 10. Exhibit 9.13
def public_eq():
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    q = np.linspace(0, 8, 300)
    ax.plot(q, pub_mkt(q), color=BLUE, lw=2.8, zorder=3)
    ax.plot(q, pub_s(q), color=RED, lw=2.8, zorder=3)
    ax.text(7.6, pub_mkt(6.9), "D = everyone's value, added upwards", color=BLUE,
            fontsize=10.5, fontweight="bold", ha="right", bbox=BOX)
    ax.text(5.5, pub_s(5.6) + 6, "S = marginal social cost", color=RED, fontsize=10.5,
            fontweight="bold", ha="center", bbox=BOX)
    ax.plot([PUB_QO, PUB_QO], [0, 80], ls=":", lw=1.0, color=GREEN)
    ax.plot([0, PUB_QO], [80, 80], ls=":", lw=1.0, color=GREEN)
    ax.plot([PUB_QO], [80], "o", ms=9, mfc=GREEN, mec="white", mew=1.8, zorder=6)
    ax.annotate("provide 4 missions: the 4th is worth\n"
                "\$80 to society and costs \$80 to supply",
                xy=(PUB_QO, 80), xytext=(0.35, 44), fontsize=10.5, color=INK, bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2))
    ax.set_xlim(0, 8); ax.set_ylim(0, 170)
    ax.set_xticks(range(0, 9))
    ax.set_yticks(range(0, 171, 20))
    ax.set_yticklabels([r"\$%d" % v for v in range(0, 171, 20)])
    ax.set_xlabel("Space missions")
    ax.set_ylabel("Price")
    ax.set_title("The right amount of a public good is still where MB meets MC",
                 fontsize=11.5, color=GREY, loc="left", pad=8)
    save(fig, "public_eq")


# ======================================================= 11. Exhibits 9.14 / 9.15
def giving():
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))
    ax = axes[0]
    ax.plot(GIVE_YEARS, GIVE_VALUE, color=LGREY, lw=1.4, zorder=2)
    ax.plot(GIVE_YEARS, GIVE_VALUE, "o", ms=6, color=BLUE, zorder=3)
    i05, i08 = GIVE_YEARS.index(2005), GIVE_YEARS.index(2008)
    ax.plot(GIVE_YEARS[i05:i08 + 1], GIVE_VALUE[i05:i08 + 1], color=RED, lw=2.4, zorder=4)
    ax.annotate("giving fell into the recession -\nexactly when it was needed most",
                xy=(2008, 350), xytext=(1983, 430), fontsize=10, color=RED, bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
    ax.set_xlim(1976, 2020)
    ax.set_ylim(0, 500)
    ax.set_yticks(range(0, 501, 100))
    ax.set_yticklabels([r"\$%d" % v for v in range(0, 501, 100)])
    ax.set_ylabel("Total giving (billions, 2019 dollars)")
    ax.set_title("Americans give, and the total has grown", fontsize=11.5,
                 color=INK, loc="left", fontweight="bold", pad=8)
    ax.set_xlabel("markers are the years the exhibit reports; the line between them is a guide only")

    ax = axes[1]
    ypos = np.arange(len(REGIONS))
    colors = [BLUE if r == "North America" else LGREY for r in REGIONS]
    ax.barh(ypos, REGION_PCT, color=colors, height=0.72)
    ax.set_yticks(ypos)
    ax.set_yticklabels(REGIONS, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(0, 80)
    ax.set_xticks(range(0, 81, 20))
    ax.set_xticklabels(["%d%%" % v for v in range(0, 81, 20)])
    ax.set_title("Donated money in the past month, 2018", fontsize=11.5,
                 color=INK, loc="left", fontweight="bold", pad=8)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    save(fig, "giving")


# ============================================================= 12. Exhibit 9.16
def congestion():
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    x = np.arange(len(VEH))
    w = 0.38
    ax.bar(x - w / 2, VEH_2002, w, color=LGREY, label="2002 - last year without the charge")
    ax.bar(x + w / 2, VEH_2003, w, color=BLUE, label="2003 - first year with the charge")
    ax.bar([x[0] + w / 2], [VEH_2003[0]], w, color=RED)
    ax.set_xticks(x)
    ax.set_xticklabels(VEH)
    ax.set_ylabel("Vehicle-kilometres (thousands)")
    ax.set_ylim(0, 900)
    ax.annotate("cars down about a third", xy=(0 + w / 2, VEH_2003[0]),
                xytext=(1.15, 680), fontsize=11, color=RED, fontweight="bold", bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax.text(3.6, 470, "taxis, buses, motorcycles\nand bicycles all rose", fontsize=10,
            color=GREEN, fontweight="bold", bbox=BOX)
    ax.legend(frameon=False, fontsize=9.5, loc="upper right")
    ax.set_title("London's congestion charge: a price on a negative externality",
                 fontsize=11.5, color=GREY, loc="left", pad=8)
    save(fig, "congestion")


# ============================================================= 13. the commons
def commons():
    """The asymmetry that destroys a common pool resource, drawn as one picture.

    Not a publisher exhibit - this is Mateer & Coppock's grazing commons (100 farmers,
    100 cows, capacity 100) rendered as the arithmetic behind the tragedy.
    """
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    ax.axhline(COMMONS_CAPACITY, color=GREEN, lw=2.0, ls="--", zorder=2)
    ax.text(-0.50, COMMONS_CAPACITY + 30, "what the commons can carry: 100 cows",
            color=GREEN, fontsize=11, fontweight="bold", bbox=BOX)
    bars = ax.bar([0, 1], [COMMONS_CAPACITY, COMMONS_IF_ALL_ADD],
                  width=0.42, color=[BLUE, RED])
    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(0, 285)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["100 farmers,\none cow each", "100 farmers,\ntwo cows each"])
    ax.set_ylabel("Cows on the commons")
    for b, v in zip(bars, [COMMONS_CAPACITY, COMMONS_IF_ALL_ADD]):
        ax.text(b.get_x() + b.get_width() / 2, v + 6, str(v), ha="center",
                fontsize=13, fontweight="bold", color=INK)
    ax.annotate("each farmer keeps ALL of the second cow\n"
                "but bears only 1/100th of the damage -\n"
                "so every one of them adds it",
                xy=(0.79, 190), xytext=(-0.52, 278), fontsize=10.5, color=RED, bbox=BOX,
                va="top", ha="left",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax.set_title("Nobody wanted this outcome and everybody chose it",
                 fontsize=11.5, color=GREY, loc="left", pad=8)
    save(fig, "commons")


FIGURES = [elec_market, elec_msc, elec_dwl, elec_tax, educ_dwl, educ_subsidy,
           neg_pos, quakes, summation, public_eq, giving, congestion, commons]

if __name__ == "__main__":
    print("ch09 figures -> %s" % OUT)
    for f in FIGURES:
        f()
    print("%d figures" % len(FIGURES))
