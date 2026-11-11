#!/usr/bin/env python3
r"""ECON 003 - Chapter 12 (Monopoly) figures.

SCOPE: sections 12.1-12.5 and 12.7.  Section 12.6, price discrimination, is NOT lectured
by instruction - see `claude/lecture-scope-ch10-ch12.md`.  Exhibits 12.12 and 12.13 are
therefore not drawn here.  EXHIBIT 12.7 WAS CUT AND IS NOW BACK, on request, as
`tr_regions` - total revenue alone, cut into the three regions the Exhibit 12.5 table
implies.  See that function's docstring for why it earns the page after all.

matplotlib, UCR palette, Liberation Sans (Arial metrics).  Blue = demand, red = marginal
cost (it IS supply), green = average total cost, dark gold = marginal revenue.  Blue and
red match every other deck in the course and the publisher's own exhibits.

  CLARITIN (Exhibits 12.3, 12.4, 12.5, 12.6, 12.8, 12.9, 12.10, 12.11)
  P in dollars per pill, Q in millions of pills a year.  Recovered exactly from the
  publisher's Exhibit 12.4 ("slopes down from (0, $6) to (800, $2)") and their Exhibit
  12.5 table, which is a real PowerPoint table and was read cell by cell:

        D:   P  = 6 - 0.005 Q          reaches $0 at Q = 1,200
        MR:  MR = 6 - 0.010 Q          reaches $0 at Q =   600
        MC   = $1.00, constant         FIXED COST = $10m,  TC = 10 + Q
        ATC  = 10/Q + 1

      monopoly      MR = MC at Q = 500;  price read off DEMAND: P = $3.50
                    ATC(500) = $1.02,  profit = (3.50 - 1.02) x 500 = $1,240m
      competitive   P = MC = $1.00  ->  Q = 1,000
      CS            competitive $2,500m   monopoly $625m
      PS            competitive $0        monopoly $1,250m
      DEADWEIGHT    1/2 x (3.50 - 1.00) x (1,000 - 500) = $625m

  Every one of those falls out of the publisher's own two numbers ($6 intercept, $1
  marginal cost) and is asserted at import below.

  THREE DEFECTS IN THE PUBLISHER'S OWN MATERIAL.  All three are in the accessibility
  "Long Description" text rather than in the drawn figures, so a student using a screen
  reader gets them and a student looking at the picture does not.

    1. Exhibit 12.11's description says "The M C line intersects the M R line at about
       560 million pills."  It is 500.  Their own instructor notes say 500 twice, and
       their own P_M of $3.50 requires 500 (6 - 0.005 x 500 = 3.50; 6 - 0.005 x 560 =
       3.20).  THIS ONE HAS CONSEQUENCES - a student who takes 560 mis-draws both the
       profit rectangle and the deadweight-loss triangle.
    2. Exhibit 12.8's description plots Q_H at "(560 million, $0.50)".  MR = $0.50 at
       Q = 550, and their own notes say "the 550th unit has a marginal revenue of $0.50".
    3. Exhibit 12.7's description ends the total-revenue curve at "about $100 million" at
       Q = 1,200.  TR = P x Q and P = $0 there, so TR = $0.  `tr_regions` draws it at
       zero, and asserts it.

  A FOURTH, AND IT IS NOT AN ERROR BUT A TRAP.  Exhibit 12.5's "Marginal Revenue" column
  is the DERIVATIVE, MR = 6 - 0.01Q, evaluated at each row - not the difference of the
  total-revenue column.  A student differencing TR across the table's 100-unit steps gets
  the value at the MIDPOINT: (1,000 - 550)/100 = $4.50, where the table's row for Q = 200
  prints $4.00.  Both are right; they answer different questions.  Say so out loud - the
  previous offering's final asked students to "difference TR to get MR".

  THE REGULATED NATURAL MONOPOLY (section 12.7, built on Exhibit 12.2's shape)
  THE PUBLISHER'S OWN SLIDE FOR THIS CANNOT WORK.  Their price-regulation slide re-uses
  Exhibit 12.11, where MC = ATC = $1 - so the fair-return price (P = ATC) and the
  efficient price (P = MC) are THE SAME NUMBER and the entire point is invisible.  Their
  notes hedge it in the subjunctive: "If ATC is greater than $1, however, this firm will
  claim that it will experience economic losses."

  So this figure is drawn on a natural monopoly with genuine economies of scale, stated
  as primitives rather than picked, and labelled in the notes as our own worked example:

        a regional water utility.  Q in thousands of households, P in $ per month,
        costs in thousands of dollars per month.
        D:   P = 10 - 0.01 Q       MR: 10 - 0.02 Q
        TC = 1,200 + 2 Q   ->   MC = $2 (constant),  ATC = 1200/Q + 2  (falling)

      unregulated monopoly   MR = MC  ->  Q = 400,  P = $6,  ATC = $5,  profit +$400
      FAIR RETURN  P = ATC   ->  Q = 600,  P = $4,  ATC = $4,  profit    $0
      EFFICIENT    P = MC    ->  Q = 800,  P = $2,  ATC = $3.50, profit -$1,200

  ATC lies above MC at every quantity, which is exactly what makes P = MC unsustainable
  without a subsidy - and that is the lesson the publisher's own figure cannot show.
  Deadweight loss falls from $800 (unregulated) to $200 (fair return).

Run:  python3 ch12_charts.py [outdir]
"""
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------- house style
BLUE = "#003DA5"      # demand
RED = "#CC3333"       # marginal cost - it IS supply
GREEN = "#2E7D32"     # average total cost, and the efficient outcome
DGOLD = "#B88300"     # marginal revenue
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
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.06,
})

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
BOX = dict(fc="white", ec="none", alpha=0.90, pad=1.6)


def save(fig, name):
    p = os.path.join(OUT, "ch12_fig_%s.png" % name)
    fig.savefig(p, facecolor="white")
    plt.close(fig)
    print("  ", os.path.basename(p))


# ============================================================ PRIMITIVES: CLARITIN
C_INT, C_SLOPE = 6.0, 0.005            # Exhibit 12.4: (0, $6) to (800, $2)
C_MC = 1.0                             # Exhibit 12.5: constant $1.00
C_FC = 10.0                            # Exhibit 12.5: fixed cost $10 million


def c_d(q):
    return C_INT - C_SLOPE * q


def c_mr(q):
    return C_INT - 2 * C_SLOPE * q


def c_atc(q):
    return C_FC / q + C_MC


def c_tr(q):
    return c_d(q) * q


C_QM = (C_INT - C_MC) / (2 * C_SLOPE)       # 500  - MR = MC
C_PM = c_d(C_QM)                            # 3.50 - read off DEMAND, never off MR
C_QC = (C_INT - C_MC) / C_SLOPE             # 1000 - P = MC
C_PC = C_MC                                 # 1.00
C_ATCM = c_atc(C_QM)                        # 1.02
C_PROFIT = (C_PM - C_ATCM) * C_QM           # 1240
C_CS_C = 0.5 * (C_INT - C_PC) * C_QC        # 2500
C_CS_M = 0.5 * (C_INT - C_PM) * C_QM        # 625
C_PS_M = (C_PM - C_MC) * C_QM               # 1250
C_DWL = 0.5 * (C_PM - C_MC) * (C_QC - C_QM)  # 625

assert abs(c_d(800) - 2.0) < 1e-12, "Exhibit 12.4 runs from (0, $6) to (800, $2)"
assert abs(c_d(1200)) < 1e-12, "Exhibit 12.7 puts the demand intercept at Q = 1,200"
assert abs(c_mr(600)) < 1e-12, "Exhibit 12.7 puts MR = 0 at Q = 600"
assert abs(C_QM - 500) < 1e-9, (
    "MR = MC at 500, not the 'about 560' Exhibit 12.11's description gives - see "
    "DEFECT 1 in the header")
assert abs(C_PM - 3.50) < 1e-12, "the publisher's own P_M is $3.50, which requires Q = 500"
assert abs(c_mr(550) - 0.50) < 1e-12, "MR = $0.50 at Q = 550, their notes agree - DEFECT 2"
assert abs(C_QC - 1000) < 1e-9 and abs(C_PC - 1.0) < 1e-12
assert C_PM > c_mr(C_QM), "the monopolist sets P ABOVE MR = MC"
assert abs(c_mr(C_QM) - C_MC) < 1e-12
assert abs(C_ATCM - 1.02) < 1e-12, "Exhibit 12.5 prints ATC = $1.02 at Q = 500"
assert abs(C_PROFIT - 1240) < 1e-9, "profit = (3.50 - 1.02) x 500 = $1,240m"
assert abs(c_tr(C_QM) - 1750) < 1e-9, "Exhibit 12.5 prints TR = $1,750m at Q = 500"
assert abs(c_tr(600) - 1800) < 1e-9, "TR peaks at $1,800m where MR = 0, at Q = 600"
assert c_tr(600) > c_tr(C_QM), "TR is maximised at a LARGER quantity than profit"
assert abs(C_DWL - 625) < 1e-9
assert abs((C_CS_C - C_CS_M) - (C_PS_M + C_DWL)) < 1e-9, \
    "every dollar of lost consumer surplus is either TRANSFERRED or DESTROYED"
assert C_QM < C_QC and C_PM > C_PC, "monopoly means less output at a higher price"
assert abs(c_tr(700) - c_tr(C_QM)) < 1e-9, \
    "the table prints \$1,750 TWICE, at Q = 500 and again at Q = 700 - the whole point " \
    "of the total-revenue page"
assert c_tr(1200) == 0.0, \
    "TR = P x Q and P = \$0 at Q = 1,200, so TR is ZERO there - not the 'about \$100 " \
    "million' Exhibit 12.7's description gives (DEFECT 3)"
assert c_mr(C_QM) == C_MC and 0 < c_mr(550) < C_MC, \
    "between Q = 500 and Q = 600 marginal revenue is POSITIVE but BELOW marginal cost - " \
    "revenue still rising while profit already falls. That gap IS the middle region."

# the $5 -> $4 worked example the publisher runs on Exhibit 12.6
EX_P1, EX_Q1, EX_P2, EX_Q2 = 5.0, 200.0, 4.0, 400.0
QTY_EFFECT = (EX_Q2 - EX_Q1) * EX_P2         # +800
PRICE_EFFECT = -(EX_P1 - EX_P2) * EX_Q1      # -200
assert abs(c_d(EX_Q1) - EX_P1) < 1e-12 and abs(c_d(EX_Q2) - EX_P2) < 1e-12
assert abs(QTY_EFFECT - 800) < 1e-9 and abs(PRICE_EFFECT + 200) < 1e-9
assert abs((QTY_EFFECT + PRICE_EFFECT) / (EX_Q2 - EX_Q1) - 3.0) < 1e-9, \
    "net $600 over 200 extra pills is $3 a pill - and $3 is LESS than the $4 price"
assert 3.0 < EX_P2, "MR < P, which is the whole point of the page"

# the Exhibit 12.5 table, as printed, so the deck can quote rows without re-deriving
TABLE_Q = [100, 200, 300, 400, 500, 600, 700, 800]
for _q in TABLE_Q:
    assert abs(c_d(_q) - (6 - 0.005 * _q)) < 1e-12
assert [c_mr(q) for q in (100, 200, 500, 600)] == [5.0, 4.0, 1.0, 0.0]

# ================================================ PRIMITIVES: THE WATER UTILITY
W_INT, W_SLOPE = 10.0, 0.01
W_MC = 2.0
W_FC = 1200.0


def w_d(q):
    return W_INT - W_SLOPE * q


def w_mr(q):
    return W_INT - 2 * W_SLOPE * q


def w_atc(q):
    return W_FC / q + W_MC


W_QM = (W_INT - W_MC) / (2 * W_SLOPE)        # 400
W_PM = w_d(W_QM)                             # 6
W_QE = (W_INT - W_MC) / W_SLOPE              # 800  - P = MC
W_PE = W_MC                                  # 2
W_QF = 600.0                                 # P = ATC, the larger root
W_PF = w_d(W_QF)                             # 4

assert abs(W_PM - 6.0) < 1e-12 and abs(w_atc(W_QM) - 5.0) < 1e-12
assert abs((W_PM - w_atc(W_QM)) * W_QM - 400.0) < 1e-9, "unregulated profit is +$400"
assert abs(W_PF - 4.0) < 1e-12 and abs(w_atc(W_QF) - 4.0) < 1e-12, \
    "the FAIR-RETURN price is where demand meets ATC: $4 at 600 thousand households"
assert abs((W_PF - w_atc(W_QF)) * W_QF) < 1e-9, "fair return means ZERO economic profit"
assert abs(w_atc(W_QE) - 3.50) < 1e-12
assert abs((W_PE - w_atc(W_QE)) * W_QE + 1200.0) < 1e-9, \
    "pricing at MC loses exactly the fixed cost - which is why it needs a subsidy"
assert all(w_atc(q) > W_MC for q in (100, 400, 600, 800, 1000)), \
    "ATC lies ABOVE MC everywhere - the thing the publisher's own figure cannot show"
assert w_atc(800) < w_atc(400) < w_atc(200), "ATC must be FALLING: that is what makes it natural"
W_DWL_M = 0.5 * (W_PM - W_MC) * (W_QE - W_QM)        # 800
W_DWL_F = 0.5 * (W_PF - W_MC) * (W_QE - W_QF)        # 200
assert abs(W_DWL_M - 800) < 1e-9 and abs(W_DWL_F - 200) < 1e-9
assert W_DWL_F < W_DWL_M, "regulation shrinks the deadweight loss without eliminating it"


# ====================================================================== helpers
def _c_axes(ax, xmax=1200, ymax=6.6):
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_xticks([0, 200, 400, 500, 600, 800, 1000, 1200])
    ax.set_yticks([0, 1, 2, 3.5, 5, 6])
    ax.set_yticklabels([r"\$0", r"\$1", r"\$2", r"\$3.50", r"\$5", r"\$6"])
    ax.set_xlabel("Pills per year (millions)")
    ax.set_ylabel("Price per pill")


def _drop(ax, q, p, color=GREY, to_y=True, to_x=True):
    if to_y:
        ax.plot([q, q], [0, p], ls=":", lw=1.0, color=color, zorder=1)
    if to_x:
        ax.plot([0, q], [p, p], ls=":", lw=1.0, color=color, zorder=1)


# ============================================================ 1. Exhibit 12.2
def nat_mono():
    """Average total cost still falling when one firm has served the whole market."""
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    q = np.linspace(60, 1000, 400)
    ax.plot(q, w_atc(q), color=GREEN, lw=2.8, zorder=3)
    ax.axhline(W_MC, color=RED, lw=2.6, zorder=3)
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 14)
    ax.set_xticks([0, 200, 400, 600, 800, 1000])
    ax.set_yticks([0, 2, 5, 8, 11, 14])
    ax.set_yticklabels([r"\$0", r"\$2", r"\$5", r"\$8", r"\$11", r"\$14"])
    ax.set_xlabel("Households served (thousands)")
    ax.set_ylabel("Cost per household per month")
    ax.text(930, W_MC + 0.45, "MC", color=RED, fontsize=13, fontweight="bold")
    ax.text(880, w_atc(880) + 0.75, "ATC", color=GREEN, fontsize=13, fontweight="bold")
    ax.annotate("one firm serving everyone:\n" + r"ATC = \$3.50",
                xy=(800, w_atc(800)), xytext=(690, 8.4), fontsize=10, color=GREEN,
                ha="center", bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.1))
    ax.annotate("two firms, half the market each:\n" + r"ATC = \$5.00 — the same water costs more",
                xy=(400, w_atc(400)), xytext=(430, 11.6), fontsize=10, color=INK,
                ha="center", bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))
    ax.plot([800], [w_atc(800)], "o", ms=8, color=GREEN, zorder=5)
    ax.plot([400], [w_atc(400)], "o", ms=8, mfc="white", mec=INK, mew=1.6, zorder=5)
    save(fig, "nat_mono")


# ============================================================ 2. Exhibit 12.3
def demand_pc_mono():
    """The price taker's flat line and the price maker's whole market curve."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.9))
    for ax in (a1, a2):
        ax.set_xlim(0, 1200)
        ax.set_ylim(0, 6.6)
        ax.set_xticks([0, 400, 800, 1200])
        ax.set_yticks([0, 1, 2, 4, 6])
        ax.set_yticklabels([r"\$0", r"\$1", r"\$2", r"\$4", r"\$6"])
        ax.set_xlabel("Quantity the FIRM sells")
        ax.set_ylabel("Price")

    a1.axhline(3.0, color=BLUE, lw=2.8, zorder=3)
    a1.text(1080, 3.24, "D = MR", color=BLUE, fontsize=12, fontweight="bold")
    a1.annotate("sell one more, or a thousand more —\nthe price does not move",
                xy=(700, 3.0), xytext=(600, 1.35), fontsize=10, color=INK, ha="center",
                bbox=BOX, arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))
    a1.set_title("(a)  The PRICE TAKER's demand curve", fontsize=11.5, color=INK, pad=6)

    q = np.linspace(0, 1200, 400)
    a2.plot(q, c_d(q), color=BLUE, lw=2.8, zorder=3)
    a2.text(1080, c_d(1080) + 0.30, "D", color=BLUE, fontsize=13, fontweight="bold")
    for qq in (200, 400):
        a2.plot([qq], [c_d(qq)], "o", ms=7, color=BLUE, zorder=5)
        _drop(a2, qq, c_d(qq))
    a2.annotate("to sell 400 instead of 200\nit must drop the price to " + r"\$4",
                xy=(400, c_d(400)), xytext=(730, 4.6), fontsize=10, color=BLUE,
                ha="center", bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.1))
    a2.set_title("(b)  The PRICE MAKER's demand curve", fontsize=11.5, color=INK, pad=6)
    fig.tight_layout(w_pad=2.4)
    save(fig, "demand_pc_mono")


# ============================================================ 3. Exhibit 12.6
def qty_price_effect():
    """Cut the price from $5 to $4: win a green box, lose a pink one."""
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    _c_axes(ax, xmax=900, ymax=6.6)
    ax.set_xticks([0, 200, 400, 600, 800])
    ax.set_yticks([0, 1, 2, 4, 5, 6])
    ax.set_yticklabels([r"\$0", r"\$1", r"\$2", r"\$4", r"\$5", r"\$6"])
    q = np.linspace(0, 900, 400)
    ax.plot(q, c_d(q), color=BLUE, lw=2.8, zorder=3)
    ax.text(840, c_d(840) + 0.30, "D", color=BLUE, fontsize=13, fontweight="bold")

    ax.fill_between([0, EX_Q1], EX_P2, EX_P1, color=TINT_RED, zorder=0)
    ax.fill_between([EX_Q1, EX_Q2], 0, EX_P2, color=TINT_GREEN, zorder=0)
    ax.plot([0, EX_Q1, EX_Q1], [EX_P1, EX_P1, 0], lw=1.0, ls=":", color=GREY, zorder=2)
    ax.plot([0, EX_Q2, EX_Q2], [EX_P2, EX_P2, 0], lw=1.0, ls=":", color=GREY, zorder=2)
    ax.plot([EX_Q1], [EX_P1], "o", ms=7, color=BLUE, zorder=5)
    ax.plot([EX_Q2], [EX_P2], "o", ms=7, color=BLUE, zorder=5)

    ax.text(295, 1.75, "QUANTITY EFFECT\n" + r"200 more x \$4 = $+$\$800",
            fontsize=10, color=GREEN, fontweight="bold", ha="center", bbox=BOX)
    ax.annotate("PRICE EFFECT\n" + r"200 old x $-$\$1 = $-$\$200",
                xy=(100, 4.5), xytext=(430, 5.6), fontsize=10, color=RED,
                fontweight="bold", ha="center", bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
    ax.text(650, 4.85, r"net $+$\$600 over 200 extra pills" "\n"
                       r"MARGINAL REVENUE = \$3 — below the \$4 price",
            fontsize=10, color=INK, fontweight="bold", ha="center", bbox=BOX)
    save(fig, "qty_price_effect")


# ================================================== 4. Exhibits 12.8 and 12.9
def mr_mc():
    """Find the quantity where MR = MC, then go UP to demand for the price."""
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    _c_axes(ax)
    q = np.linspace(0, 1200, 400)
    ax.plot(q, c_d(q), color=BLUE, lw=2.8, zorder=3)
    ax.plot(q[q <= 600], c_mr(q[q <= 600]), color=DGOLD, lw=2.6, zorder=3)
    ax.axhline(C_MC, color=RED, lw=2.6, zorder=3)
    ax.text(950, c_d(950) + 0.40, "D", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(560, 1.55, "MR", color=DGOLD, fontsize=12.5, fontweight="bold", bbox=BOX)
    ax.text(1105, C_MC + 0.34, "MC", color=RED, fontsize=13, fontweight="bold", bbox=BOX)

    ax.annotate("", xy=(C_QM, C_PM), xytext=(C_QM, C_MC),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.8))
    ax.plot([0, C_QM], [C_PM, C_PM], ls=":", lw=1.2, color=INK, zorder=2)
    ax.plot([C_QM], [C_MC], "o", ms=8, color=DGOLD, zorder=5)
    ax.plot([C_QM], [C_PM], "o", ms=9, color=BLUE, zorder=5)
    ax.text(C_QM + 22, 0.42, "STEP 1\n" + r"MR = MC at 500", fontsize=9.5, color=DGOLD,
            fontweight="bold", bbox=BOX)
    ax.text(C_QM + 22, 4.35, "STEP 2\ngo UP to DEMAND", fontsize=9.5, color=INK,
            fontweight="bold", bbox=BOX)
    ax.text(28, C_PM + 0.22, "STEP 3\n" + r"the price is \$3.50", fontsize=9.5,
            color=BLUE, fontweight="bold", bbox=BOX)
    ax.annotate("the price is NOT " + r"\$1" "\n" r"\$1 is the marginal COST",
                xy=(C_QM + 10, C_MC + 0.04), xytext=(800, 2.45), fontsize=9.5, color=RED,
                ha="center", bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
    save(fig, "mr_mc")


# =========================================================== 5. Exhibit 12.10
def profit_rect():
    """Price above average total cost, times quantity.

    ATC is drawn from Q = 2 so the curve sweeps down from about $6 the way the
    publisher's Exhibit 12.10 draws it.  It then hugs MC, and that is not a drawing
    artefact - it is the economics of the industry: a $10m fixed cost spread over 500m
    pills is two cents a pill.  Say that out loud rather than letting the figure imply
    that ATC and MC are the same thing.
    """
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    _c_axes(ax, ymax=6.6)
    q = np.linspace(0, 1200, 400)
    qa = np.linspace(2, 1200, 900)
    ax.plot(q, c_d(q), color=BLUE, lw=2.8, zorder=3)
    ax.plot(q[q <= 600], c_mr(q[q <= 600]), color=DGOLD, lw=2.2, zorder=3)
    ax.axhline(C_MC, color=RED, lw=2.4, zorder=3)
    ax.plot(qa, c_atc(qa), color=GREEN, lw=2.6, zorder=4)
    ax.fill_between([0, C_QM], C_ATCM, C_PM, color=TINT_GREEN, zorder=0)
    ax.plot([0, C_QM, C_QM], [C_PM, C_PM, 0], ls=":", lw=1.1, color=GREY, zorder=2)
    ax.plot([C_QM], [C_PM], "o", ms=8, color=BLUE, zorder=5)

    ax.text(860, c_d(860) + 0.42, "D", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(560, 1.55, "MR", color=DGOLD, fontsize=12, fontweight="bold", bbox=BOX)
    ax.text(1115, C_MC - 0.52, "MC", color=RED, fontsize=12.5, fontweight="bold", bbox=BOX)
    ax.text(250, 2.28, r"PROFIT = (\$3.50 $-$ \$1.02) x 500 = \$1,240 million",
            fontsize=10.5, color=GREEN, fontweight="bold", ha="center", bbox=BOX)
    ax.text(32, 3.30, "ATC", color=GREEN, fontsize=12.5, fontweight="bold", bbox=BOX)
    ax.text(880, 3.95, "ATC falls fast, then hugs MC:\n"
                       r"a \$10m fixed cost over 500m pills"
                       "\n" r"is 2¢ each, so ATC(500) = \$1.02",
            fontsize=9.5, color=GREEN, ha="center", bbox=BOX)
    ax.annotate("nothing competes it away —\nthat is what a barrier to entry IS",
                xy=(190, 2.75), xytext=(330, 5.55), fontsize=9.5, color=INK, ha="center",
                bbox=BOX, arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    save(fig, "profit_rect")


# =========================================================== 6. Exhibit 12.11
def pc_vs_mono():
    """The same market, run twice."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.9))
    q = np.linspace(0, 1200, 400)

    for ax in (a1, a2):
        ax.set_xlim(0, 1200)
        ax.set_ylim(0, 6.6)
        ax.set_xticks([0, 500, 1000, 1200])
        ax.set_yticks([0, 1, 3.5, 6])
        ax.set_yticklabels([r"\$0", r"\$1", r"\$3.50", r"\$6"])
        ax.set_xlabel("Pills per year (millions)")
        ax.set_ylabel("Price per pill")
        ax.plot(q, c_d(q), color=BLUE, lw=2.8, zorder=3)
        ax.axhline(C_MC, color=RED, lw=2.5, zorder=3)

    qc = np.linspace(0, C_QC, 200)
    a1.fill_between(qc, c_d(qc), C_MC, color=TINT_BLUE, zorder=0)
    a1.plot([C_QC], [C_PC], "o", ms=8, color=GREEN, zorder=5)
    a1.text(230, 3.15, r"CS = \$2,500m", color=BLUE, fontsize=11, fontweight="bold",
            bbox=BOX)
    a1.text(1115, c_d(1115) - 0.02, "D", color=BLUE, fontsize=13, fontweight="bold")
    a1.text(1180, C_MC + 0.30, "MC = ATC", color=RED, fontsize=10.5, fontweight="bold",
            ha="right", bbox=BOX)
    a1.text(C_QC - 40, 0.30, r"1,000 at \$1", fontsize=10, color=GREEN,
            fontweight="bold", ha="right", bbox=BOX)
    a1.set_title("(a)  Perfect competition:  P = MC", fontsize=11.5, color=INK, pad=6)

    a2.plot(q[q <= 600], c_mr(q[q <= 600]), color=DGOLD, lw=2.3, zorder=3)
    qm = np.linspace(0, C_QM, 150)
    a2.fill_between(qm, c_d(qm), C_PM, color=TINT_BLUE, zorder=0)
    a2.fill_between([0, C_QM], C_MC, C_PM, color=TINT_GREEN, zorder=0)
    tri = np.linspace(C_QM, C_QC, 120)
    a2.fill_between(tri, c_d(tri), C_MC, color=TINT_GOLD, zorder=0)
    a2.plot([0, C_QM, C_QM], [C_PM, C_PM, 0], ls=":", lw=1.1, color=GREY, zorder=2)
    a2.plot([C_QM], [C_PM], "o", ms=8, color=BLUE, zorder=5)
    a2.plot([C_QC], [C_PC], "o", ms=7, mfc="white", mec=GREEN, mew=1.8, zorder=5)
    a2.text(120, 4.55, r"CS = \$625m", color=BLUE, fontsize=10.5, fontweight="bold",
            bbox=BOX)
    a2.text(120, 2.10, r"PS = \$1,250m" "\n" "(taken from CS)", color=GREEN,
            fontsize=10.5, fontweight="bold", bbox=BOX)
    a2.annotate(r"DWL = \$625m" "\n" "(taken from nobody's pocket)",
                xy=(660, 1.9), xytext=(880, 4.3), fontsize=10, color=DGOLD,
                fontweight="bold", ha="center", bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.1))
    a2.text(1115, c_d(1115) - 0.02, "D", color=BLUE, fontsize=13, fontweight="bold")
    a2.text(430, 2.05, "MR", color=DGOLD, fontsize=11.5, fontweight="bold", bbox=BOX)
    a2.text(760, C_MC - 0.55, "MC", color=RED, fontsize=12, fontweight="bold", bbox=BOX)
    a2.text(C_QM - 25, 0.28, r"500 at \$3.50", fontsize=10, color=BLUE,
            fontweight="bold", ha="right", bbox=BOX)
    a2.set_title("(b)  Monopoly:  P > MR = MC", fontsize=11.5, color=INK, pad=6)

    fig.tight_layout(w_pad=2.4)
    save(fig, "pc_vs_mono")


# ================================== 7. section 12.7 - regulating a natural monopoly
def nat_mono_reg():
    """Three prices on one natural monopoly: what the firm wants, and two the law can set."""
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    q = np.linspace(0, 1000, 400)
    qa = np.linspace(120, 1000, 400)
    ax.plot(q, w_d(q), color=BLUE, lw=2.8, zorder=3)
    ax.plot(q[q <= 500], w_mr(q[q <= 500]), color=DGOLD, lw=2.2, zorder=3)
    ax.plot(qa, w_atc(qa), color=GREEN, lw=2.6, zorder=3)
    ax.axhline(W_MC, color=RED, lw=2.5, zorder=3)
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 10.4)
    ax.set_xticks([0, 400, 600, 800, 1000])
    ax.set_yticks([0, 2, 3.5, 4, 5, 6, 8, 10])
    ax.set_yticklabels([r"\$0", r"\$2", r"\$3.50", r"\$4", r"\$5", r"\$6", r"\$8", r"\$10"])
    ax.set_xlabel("Households served (thousands)")
    ax.set_ylabel("Monthly price")
    ax.text(960, w_d(960) + 0.35, "D", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(455, 0.42, "MR", color=DGOLD, fontsize=12, fontweight="bold", bbox=BOX)
    ax.text(940, W_MC - 0.62, "MC", color=RED, fontsize=12.5, fontweight="bold")
    ax.text(920, w_atc(920) + 0.40, "ATC", color=GREEN, fontsize=12.5, fontweight="bold")

    for qq, pp, col, lab in ((W_QM, W_PM, RED, "UNREGULATED"),
                             (W_QF, W_PF, GOLD, "FAIR RETURN"),
                             (W_QE, W_PE, GREEN, "EFFICIENT")):
        ax.plot([0, qq, qq], [pp, pp, 0], ls=":", lw=1.0, color=GREY, zorder=1)
        ax.plot([qq], [pp], "o", ms=8, color=(DGOLD if col is GOLD else col), zorder=5)
    ax.text(W_QM + 18, W_PM + 0.30, r"MONOPOLY  \$6 x 400" "\n" r"profit $+$\$400",
            fontsize=9.5, color=RED, fontweight="bold", bbox=BOX)
    ax.text(W_QF + 18, W_PF + 0.28, r"FAIR RETURN  P = ATC = \$4 x 600" "\n"
                                    r"zero economic profit",
            fontsize=9.5, color=DGOLD, fontweight="bold", bbox=BOX)
    ax.text(W_QE + 12, 0.95, r"EFFICIENT  P = MC = \$2 x 800" "\n"
                             r"loses \$1,200 — needs a subsidy",
            fontsize=9.5, color=GREEN, fontweight="bold", ha="right", bbox=BOX)
    save(fig, "nat_mono_reg")


# ============================== 8. Exhibit 12.7, restored on request, region by region
def tr_regions():
    """TOTAL REVENUE against quantity, cut into the three regions the table implies.

    Exhibit 12.7 was cut from this deck as redundant with the quantity-effect page, and
    he asked for it back with the regions marked.  It is worth having back: the table on
    the revenue-and-cost page already contains the turn - $1,750 at 500, $1,800 at 600,
    $1,750 AGAIN at 700 - and almost nobody reads a table well enough to see it.

    THE Y-AXIS TICKS ARE THE TABLE'S TOTAL-REVENUE COLUMN, on purpose, so a student can
    put a finger on a row and find it on the curve.  $1,750 is left off the axis and
    labelled twice on the curve instead, because it happens twice.

    TWO REGIONS, NAMED IN THE PREVIOUS PAGE'S OWN TERMS - the QUANTITY EFFECT against
    the PRICE EFFECT.  That is the whole point of putting the page here rather than
    anywhere else: the quantity-effect / price-effect page says what marginal revenue is
    made of, and this one says what happens when the two of them trade places.

        Q < 600     QUANTITY EFFECT WINS.  MR > \$0, so TOTAL REVENUE RISES.
        Q > 600     PRICE EFFECT WINS.   MR < \$0, so TOTAL REVENUE FALLS.

    THE SPLIT IS MR = 0, NOT MR = MC, and the distinction cost a draft.  An earlier
    version shaded 500-600 as a third region on the grounds that MR is positive there but
    already below MC.  True, and irrelevant to THIS curve: that band is the distance
    between where PROFIT peaks and where REVENUE peaks, and it is only 100 units wide
    because MC happens to be \$1.  Set MC to zero and it disappears.  A region of the
    total-revenue curve has to be a property of total revenue.

    Q = 500 IS STILL MARKED, as a POINT rather than a boundary - "the firm stops here,
    MR = MC" - because revenue-maximising and profit-maximising are different quantities
    and that is the classic exam trap.  It just is not a region.

    The publisher's own description of Exhibit 12.7 ends total revenue at "about $100
    million" at Q = 1,200, where the price is $0 - see DEFECT 3 in the header.  This
    figure ends it at zero, which is where P x Q puts it.
    """
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 2150)
    ax.set_xticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 1000, 1200])
    ax.set_yticks([0, 550, 1000, 1350, 1600, 1800])
    ax.set_yticklabels([r"\$0", r"\$550", r"\$1,000", r"\$1,350", r"\$1,600", r"\$1,800"])
    ax.set_xlabel("Pills per year (millions)")
    ax.set_ylabel("Total revenue (\$ millions)")

    # TWO regions, split at the apex, and the split is MR = 0 - NOT MR = MC.  An earlier
    # draft shaded 500-600 as a third region; that band is the distance between where
    # PROFIT peaks and where REVENUE peaks, and it exists only because MC happens to be
    # $1.  Set MC to zero and it vanishes.  It is not a property of the revenue curve, so
    # it is not a region of it.  Q = 500 is still marked, as a point on the curve.
    ax.axvspan(0, 600, color=TINT_GREEN, zorder=0)
    ax.axvspan(600, 1200, color=TINT_RED, zorder=0)

    q = np.linspace(0, 1200, 600)
    ax.plot(q, c_tr(q), color=BLUE, lw=2.8, zorder=4)

    # the table's own rows, on the curve
    for qq in (100, 200, 300, 400):
        ax.plot([qq], [c_tr(qq)], "o", ms=5, color=BLUE, zorder=5)
    ax.plot([600], [1800], "o", ms=9, color=BLUE, zorder=6)
    ax.plot([C_QM], [1750], "o", ms=9, color=DGOLD, zorder=6)
    ax.plot([700], [1750], "o", ms=6, color=GREY, zorder=6)
    ax.plot([C_QM, C_QM], [0, 1750], ls=":", lw=1.2, color=DGOLD, zorder=2)
    ax.plot([600, 600], [0, 1800], ls=":", lw=1.2, color=BLUE, zorder=2)
    ax.plot([0, 700], [1750, 1750], ls=":", lw=1.0, color=GREY, zorder=1)

    ax.text(600, 1960, r"APEX — MR = \$0,  TR \$1,800", color=BLUE, fontsize=10.5,
            fontweight="bold", ha="center", va="center", bbox=BOX, zorder=7)
    ax.annotate("THE FIRM STOPS HERE\n" + r"MR = MC = \$1",
                xy=(C_QM, 1750), xytext=(430, 1010), color=DGOLD, fontsize=10,
                fontweight="bold", ha="center", va="center", bbox=BOX, zorder=7,
                arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.2))
    ax.text(790, 1830, r"\$1,750 again, at 700", color=GREY, fontsize=9,
            fontweight="bold", ha="left", va="center", zorder=7)

    # The two wide region labels sit on the SAME baseline, low, where the parabola is
    # clear of them at both ends. A white bbox laid across the curve reads as a break in
    # it, and this curve's whole point is that it is smooth through the peak - the first
    # placement clipped it twice, once near Q = 100 and once near Q = 1,150.
    ax.text(300, 300, "QUANTITY EFFECT WINS\n" + r"MR $>$ \$0  —  TR RISES",
            color=GREEN, fontsize=11, fontweight="bold", ha="center", va="center",
            bbox=BOX, zorder=7)
    ax.text(900, 300, "PRICE EFFECT WINS\n" + r"MR $<$ \$0  —  TR FALLS",
            color=RED, fontsize=11, fontweight="bold", ha="center", va="center",
            bbox=BOX, zorder=7)
    save(fig, "tr_regions")


if __name__ == "__main__":
    print("Chapter 12 figures ->", OUT)
    nat_mono()
    demand_pc_mono()
    qty_price_effect()
    mr_mc()
    profit_rect()
    pc_vs_mono()
    nat_mono_reg()
    tr_regions()
    print("done.")
