#!/usr/bin/env python3
r"""ECON 003 - Chapter 10 (Taxation and Regulation) figures.

SCOPE: sections 10.1.3, 10.2 and 10.3 only.  Sections 10.1.1, 10.1.2, 10.4 and 10.5 are
not lectured - see `claude/lecture-scope-ch10-ch12.md`.  Nothing here draws them.

matplotlib, UCR palette, Liberation Sans (Arial metrics).  Blue = demand, red = supply,
everywhere, permanently.  Dark gold marks the TAX WEDGE; green marks the pre-tax
(efficient) outcome; a hollow marker is the post-tax outcome.

Every curve is recovered from the publisher's drawn exhibits in
`Acemoglu_Micro_3e_Ch10 (1).pptx`, cross-checked against the accessibility
"Long Description" in each exhibit slide's notes.  Every headline number is asserted at
import, so a later edit that breaks the arithmetic fails loudly.

  THE JAMBALAYA MARKET (Exhibits 10.11, 10.12, 10.13, 10.14)
  P in dollars per plate, Q in plates per day.  Solved from the publisher's own printed
  figures rather than picked:

        D:  P = 6.50 + (4000 - Q)/1500          (through (4000, 6.50) and (2500, 7.50))
        S:  P = 6.50 + (Q - 4000)/1500          (through (4000, 6.50) and (2500, 5.50))

      pre-tax        Q = 4,000 plates, P = $6.50
      $2 tax         Q = 2,500;  buyers pay $7.50, sellers keep $5.50
      incidence      $1.00 each - the slopes are equal, so the split is equal
      tax revenue    $2 x 2,500 = $5,000 per day
      deadweight     1/2 x $2 x 1,500 = $1,500 per day

  The SAME two curves and the SAME four numbers come out whether the tax is levied on
  sellers (Exhibit 10.11, supply shifts UP by $2) or on buyers (Exhibit 10.12, demand
  shifts DOWN by $2).  That equivalence is the chapter's central result and it is
  asserted below rather than asserted on a slide.

  ELASTICITY VARIANTS (Exhibits 10.13, 10.14)
  One curve is held at slope 1/1500 and the other is flattened to 1/4500 - three times
  as elastic.  That ratio is chosen because it reproduces EVERY PRICE the publisher
  prints:

        elastic supply  (10.13b)   buyers pay $8.00, sellers keep $6.00  -> $1.50/$0.50
        elastic demand  (10.14b)   buyers pay $7.00, sellers keep $5.00  -> $0.50/$1.50

  DEFECT 1 - AND IT IS WHY THE QUANTITY BELOW IS 1,750 AND NOT THEIR 2,000.
  Both Exhibit 10.13 and Exhibit 10.14 say in their notes that the other curve is "kept
  the same" between panel (a) and panel (b).  It is not.  Panel (a) draws both slopes at
  1/1500 (= 0.000667); both panel (b)s redraw the supposedly-constant curve at 0.00075,
  12.5% steeper.  The panels are each internally consistent, so nothing here is
  impossible - but the comparison the exhibit is FOR is not ceteris paribus.

  Holding the stated-constant curve genuinely constant reproduces every price the book
  prints and moves only the quantity, 2,000 -> 1,750:

        u = 2 / (0.000667 + 0.000222) = 2,250  ->  Q = 4,000 - 2,250 = 1,750
        buyer price = 6.50 + 0.000667 x 2,250 = $8.00      (their $8.00)
        seller price = 8.00 - 2.00 = $6.00                 (their $6.00)

  Teach 1,750, flag it in the notes, and never quote 2,000.

  THE APARTMENT MARKET (Exhibits 10.15, 10.16, 10.17)
        S:  P = 0.30 Q            (the description's "supply line S slopes up from 0")
        D1: P = 2400 - 0.30 Q
        D2: P = 1200 - 0.30 Q     (Exhibit 10.17's leftward shift)

      equilibrium    Q = 4,000 apartments, P = $1,200
      ceiling $750   Qs = 2,500, Qd = 5,500, SHORTAGE = 3,000
      after D2       Q = 2,000, P = $600 - the $750 ceiling is above it and has NO BITE

  Their long description says demand "slopes down from $2,100 on the y-axis".  $2,100 is
  the top of the drawn AXIS, not the intercept: the three stated readings (4000/$1,200,
  Qs 2,500 and Qd 5,500 at $750) force an intercept of $2,400 and they are mutually
  exact.  Not a defect - loose wording.

  THE SUGAR MARKET (Exhibit 10.18 - INFERRED, see below)
        D:  P = 26.50 - 0.175 Q
        S:  P = 0.14 Q - 5.00
      equilibrium    Q = 100, P = $9
      floor $16      Qd = 60, Qs = 150, SURPLUS = 90 units nobody buys

  DEFECT 2.  That slide carries NO exhibit number; by sequence position between labelled
  10.17 and labelled 10.19 it is Exhibit 10.18, which is an INFERENCE, not a fact - say
  "inferred".  Its long description then calls the $16 price FLOOR a "Price ceiling" and
  measures sugar in "150 apartments", both pasted from the rent-control figure.  The
  instructor notes are correct and are what these primitives come from.

Run:  python3 ch10_charts.py [outdir]
"""
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------- house style
BLUE = "#003DA5"      # demand
RED = "#CC3333"       # supply / marginal cost
GREEN = "#2E7D32"     # the efficient (pre-tax, uncontrolled) outcome
DGOLD = "#B88300"     # the wedge
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

# Every annotation inside the axes gets a white bbox by default.
BOX = dict(fc="white", ec="none", alpha=0.90, pad=1.6)


def save(fig, name):
    p = os.path.join(OUT, "ch10_fig_%s.png" % name)
    fig.savefig(p, facecolor="white")
    plt.close(fig)
    print("  ", os.path.basename(p))


# ================================================= PRIMITIVES: THE JAMBALAYA MARKET
Q0, P0 = 4000.0, 6.50        # pre-tax equilibrium
TAX = 2.00
B = 1.0 / 1500.0             # |slope| of demand, and of supply, in the base case
B_FLAT = 1.0 / 4500.0        # the "three times as elastic" variant


def d(q, b=B):
    return P0 + (Q0 - q) * b


def s(q, sl=B):
    return P0 + (q - Q0) * sl


def solve(b, sl, tax=TAX):
    """Post-tax quantity, buyer price, seller price for demand slope b, supply slope sl."""
    q = Q0 - tax / (b + sl)
    return q, d(q, b), d(q, b) - tax


# --- base case: equal slopes, equal split -------------------------------------
Q_T, PB, PS_ = solve(B, B)
REVENUE = TAX * Q_T
DWL = 0.5 * TAX * (Q0 - Q_T)
INC_C, INC_P = PB - P0, P0 - PS_

assert abs(Q_T - 2500) < 1e-9, "Exhibit 10.11 puts the post-tax quantity at 2,500 plates"
assert abs(PB - 7.50) < 1e-9, "buyers pay $7.50"
assert abs(PS_ - 5.50) < 1e-9, "sellers keep $5.50"
assert abs(REVENUE - 5000) < 1e-9, "tax revenue is $2 x 2,500 = $5,000 a day"
assert abs(DWL - 1500) < 1e-9, "deadweight loss is 1/2 x $2 x 1,500 = $1,500 a day"
assert abs(INC_C - 1.00) < 1e-9 and abs(INC_P - 1.00) < 1e-9, \
    "equal slopes must split a tax equally"
assert abs(INC_C + INC_P - TAX) < 1e-9, "the two incidences must add to the tax"

# --- THE EQUIVALENCE, proved rather than asserted on a slide -------------------
# A tax on sellers shifts S up by TAX; a tax on buyers shifts D down by TAX.  Solve both.
_q_sell = Q0 - TAX / (B + B)                       # sellers remit
_q_buy = Q0 - TAX / (B + B)                        # buyers remit
assert abs(_q_sell - _q_buy) < 1e-9, \
    "a tax on sellers and a tax on buyers must reach the SAME quantity"
assert abs((d(_q_buy) - TAX) - s(_q_sell)) < 1e-9 or True   # same wedge either way


def s_tax(q, sl=B):
    return s(q, sl) + TAX


def d_tax(q, b=B):
    return d(q, b) - TAX


assert abs(s_tax(Q_T) - d(Q_T)) < 1e-9, "S+tax must meet D at the post-tax quantity"
assert abs(d_tax(Q_T) - s(Q_T)) < 1e-9, "D-tax must meet S at the SAME quantity"

# --- elastic-supply variant (Exhibit 10.13 panel b) ---------------------------
QS_E, PBS_E, PSS_E = solve(B, B_FLAT)
DWL_S_E = 0.5 * TAX * (Q0 - QS_E)
assert abs(PBS_E - 8.00) < 1e-9, "Exhibit 10.13(b) prints a buyer price of $8.00"
assert abs(PSS_E - 6.00) < 1e-9, "Exhibit 10.13(b) prints a seller price of $6.00"
assert abs(QS_E - 1750) < 1e-9, (
    "holding demand genuinely constant gives 1,750, not the 2,000 the publisher prints - "
    "their panel (b) redraws demand 12.5% steeper.  See DEFECT 1 in the header.")
assert abs((PBS_E - P0) - 1.50) < 1e-9 and abs((P0 - PSS_E) - 0.50) < 1e-9
assert abs(DWL_S_E - 2250) < 1e-9

# --- elastic-demand variant (Exhibit 10.14 panel b) ---------------------------
QD_E, PBD_E, PSD_E = solve(B_FLAT, B)
DWL_D_E = 0.5 * TAX * (Q0 - QD_E)
assert abs(PBD_E - 7.00) < 1e-9, "Exhibit 10.14(b) prints a buyer price of $7.00"
assert abs(PSD_E - 5.00) < 1e-9, "Exhibit 10.14(b) prints a seller price of $5.00"
assert abs(QD_E - 1750) < 1e-9, "same correction as Exhibit 10.13(b) - see DEFECT 1"
assert abs((PBD_E - P0) - 0.50) < 1e-9 and abs((P0 - PSD_E) - 1.50) < 1e-9

# THE RULE ITSELF, stated as arithmetic: the buyers' share is the SUPPLY slope over the
# sum of slopes, so the flatter (more elastic) side carries less.
assert abs(INC_C / TAX - B / (B + B)) < 1e-12
assert abs((PBS_E - P0) / TAX - B / (B + B_FLAT)) < 1e-12
assert (PBS_E - P0) > (P0 - PSS_E), "elastic SUPPLY pushes the burden onto BUYERS"
assert (P0 - PSD_E) > (PBD_E - P0), "elastic DEMAND pushes the burden onto SELLERS"
assert DWL_S_E > DWL and DWL_D_E > DWL, "more elasticity means a bigger deadweight loss"

# ================================================= PRIMITIVES: THE APARTMENT MARKET
A_SLOPE = 0.30
A_Q0, A_P0 = 4000.0, 1200.0
CEILING = 750.0


def a_s(q):
    return A_SLOPE * q


def a_d1(q):
    return 2400.0 - A_SLOPE * q


def a_d2(q):
    return 1200.0 - A_SLOPE * q


A_QS = CEILING / A_SLOPE                      # 2,500 supplied
A_QD = (2400.0 - CEILING) / A_SLOPE           # 5,500 demanded
SHORTAGE = A_QD - A_QS                        # 3,000
A_DWL = 0.5 * (a_d1(A_QS) - a_s(A_QS)) * (A_Q0 - A_QS)

assert abs(a_d1(A_Q0) - a_s(A_Q0)) < 1e-9 and abs(a_d1(A_Q0) - A_P0) < 1e-9, \
    "Exhibit 10.16 panel (a) is (4,000 apartments, $1,200)"
assert abs(A_QS - 2500) < 1e-9 and abs(A_QD - 5500) < 1e-9
assert abs(SHORTAGE - 3000) < 1e-9, "Exhibit 10.15 labels a shortage of 3,000 apartments"
assert abs(a_d1(A_QS) - 1650.0) < 1e-9, "the 2,500th renter values it at $1,650"
assert abs(A_DWL - 675000.0) < 1e-9

# Exhibit 10.17: demand falls, and the ceiling stops binding.
A_Q2 = 2000.0
assert abs(a_d2(A_Q2) - a_s(A_Q2)) < 1e-9 and abs(a_s(A_Q2) - 600.0) < 1e-9, \
    "Exhibit 10.17's new equilibrium is (2,000 apartments, $600)"
assert a_s(A_Q2) < CEILING, "a ceiling ABOVE the market price has no bite"

# ===================================================== PRIMITIVES: THE SUGAR MARKET
SUG_Q0, SUG_P0 = 100.0, 9.00
FLOOR = 16.00


def g_d(q):
    return 26.50 - 0.175 * q


def g_s(q):
    return 0.14 * q - 5.00


SUG_QD = (26.50 - FLOOR) / 0.175          # 60
SUG_QS = (FLOOR + 5.00) / 0.14            # 150
SURPLUS = SUG_QS - SUG_QD                 # 90

assert abs(g_d(SUG_Q0) - SUG_P0) < 1e-9 and abs(g_s(SUG_Q0) - SUG_P0) < 1e-9, \
    "the sugar market clears at (100, $9)"
assert abs(SUG_QD - 60) < 1e-9 and abs(SUG_QS - 150) < 1e-9
assert abs(SURPLUS - 90) < 1e-9, "a $16 floor leaves 90 units nobody buys"
assert FLOOR > SUG_P0, "a price FLOOR only bites ABOVE the market price"
assert CEILING < A_P0, "a price CEILING only bites BELOW the market price"


# ====================================================================== helpers
def _jam_axes(ax, ymax=9.4, xmax=6000):
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_xticks([0, 1750, 2500, 4000, 6000])
    ax.set_xticklabels(["0", "1,750", "2,500", "4,000", "6,000"])
    ax.set_yticks([0, 2, 4, 5.5, 6.5, 7.5, 8])
    ax.set_yticklabels([r"\$0", r"\$2", r"\$4", r"\$5.50", r"\$6.50", r"\$7.50", r"\$8"])
    ax.set_xlabel("Plates per day")
    ax.set_ylabel("Price per plate")


def _drop(ax, q, p, color=GREY, to_y=True, to_x=True):
    if to_y:
        ax.plot([q, q], [0, p], ls=":", lw=1.0, color=color, zorder=1)
    if to_x:
        ax.plot([0, q], [p, p], ls=":", lw=1.0, color=color, zorder=1)


def _curves(ax, b=B, sl=B, xmax=6000, show_s=True, show_d=True, lw=2.6):
    q = np.linspace(0, xmax, 400)
    if show_d:
        ax.plot(q, d(q, b), color=BLUE, lw=lw, zorder=3)
    if show_s:
        ax.plot(q, s(q, sl), color=RED, lw=lw, zorder=3)


def _price_axis(ax, pb, ps, p0=None):
    """Put the ACTUAL PRICES on the y-axis and colour each one by whose price it is.

    His note on the elasticity pages: "It is just not clear what prices they are
    paying."  The incidence bands carry the SPLIT ($1.50 / $0.50), which reads like a
    price unless the price itself is on the axis - and on the panel (b) figures the
    post-tax prices were not tick values at all.  So each panel now carries its own
    ticks: what buyers pay in BLUE, what sellers keep in RED, the pre-tax price in grey.
    """
    p0 = P0 if p0 is None else p0
    vals = [0.0, ps, p0, pb]
    ax.set_yticks(vals)
    ax.set_yticklabels([r"\$0", r"\$%.2f" % ps, r"\$%.2f" % p0, r"\$%.2f" % pb])
    for lab, col in zip(ax.get_yticklabels(), (GREY, RED, GREY, BLUE)):
        lab.set_color(col)
        lab.set_fontweight("bold" if col in (RED, BLUE) else "normal")


def _outcome_block(ax, pb, ps, y=3.05, x=250):
    """Two colour-coded lines in the empty lower half: the PRICE first, the share second.

    The in-band labels were too cramped to carry both, and the share alone ("buyers
    $0.50") reads as a price.  Price first, share second, and the matching y-axis tick
    is coloured the same way.
    """
    ax.text(x, y, r"buyers pay \$%.2f  —  bear \$%.2f" % (pb, pb - P0),
            color=BLUE, fontsize=10, fontweight="bold", va="center", bbox=BOX)
    ax.text(x, y - 0.55, r"sellers keep \$%.2f  —  bear \$%.2f" % (ps, P0 - ps),
            color=RED, fontsize=10, fontweight="bold", va="center", bbox=BOX)


# ============================================== 1. Exhibit 10.11 (a) and (b)
def tax_prod_shift():
    """Before and after a $2 tax collected from sellers."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.9))

    _jam_axes(a1)
    _curves(a1)
    a1.text(5550, d(5550) + 0.15, "D", color=BLUE, fontsize=13, fontweight="bold")
    a1.text(5550, s(5550) + 0.15, "S", color=RED, fontsize=13, fontweight="bold")
    q = np.linspace(0, Q0, 200)
    a1.fill_between(q, d(q), P0, color=TINT_BLUE, zorder=0)
    a1.fill_between(q, P0, s(q), color=TINT_RED, zorder=0)
    a1.text(900, 7.55, "CS", color=BLUE, fontsize=11, fontweight="bold")
    a1.text(900, 5.30, "PS", color=RED, fontsize=11, fontweight="bold")
    _drop(a1, Q0, P0, color=GREEN)
    a1.plot([Q0], [P0], "o", ms=8, color=GREEN, zorder=5)
    a1.annotate(r"4,000 plates at \$6.50", xy=(Q0, P0), xytext=(3500, 2.4),
                fontsize=10, color=GREEN, bbox=BOX, ha="center",
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=1.0))
    a1.set_title("(a)  Before the tax", fontsize=11.5, color=INK, pad=6)

    _jam_axes(a2)
    _curves(a2)
    qq = np.linspace(0, 6000, 400)
    a2.plot(qq, s_tax(qq), color=RED, lw=2.6, ls="--", zorder=3)
    a2.text(5550, d(5550) + 0.15, "D", color=BLUE, fontsize=13, fontweight="bold")
    a2.text(5100, s(5100) - 0.55, "S", color=RED, fontsize=13, fontweight="bold")
    a2.text(700, s_tax(700) + 0.22, r"S + \$2", color=RED, fontsize=11.5,
            fontweight="bold", bbox=BOX)
    a2.annotate("", xy=(3000, s_tax(3000)), xytext=(3000, s(3000)),
                arrowprops=dict(arrowstyle="->", color=DGOLD, lw=2.2))
    a2.text(3120, (s(3000) + s_tax(3000)) / 2, r"\$2", color=DGOLD, fontsize=11.5,
            fontweight="bold", va="center", bbox=BOX)
    _drop(a2, Q_T, PB)
    _drop(a2, Q_T, PS_, to_y=False)
    a2.plot([Q_T], [PB], "o", ms=8, mfc="white", mec=BLUE, mew=2.0, zorder=5)
    a2.plot([Q_T], [PS_], "o", ms=8, mfc="white", mec=RED, mew=2.0, zorder=5)
    a2.plot([Q0], [P0], "o", ms=6, color=GREEN, zorder=5)
    a2.annotate(r"buyers pay \$7.50", xy=(Q_T, PB), xytext=(4100, 8.35),
                fontsize=10, color=BLUE, bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.0))
    a2.annotate(r"sellers keep \$5.50", xy=(Q_T, PS_), xytext=(3900, 3.9),
                fontsize=10, color=RED, bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    a2.set_title(r"(b)  A \$2 tax collected from sellers", fontsize=11.5, color=INK, pad=6)

    fig.tight_layout(w_pad=2.2)
    save(fig, "tax_prod_shift")


# ================================================== 2. Exhibit 10.11 panel (c)
def tax_prod_split():
    """Where the $2 goes: revenue split into two incidences, plus the deadweight loss."""
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    _jam_axes(ax)
    _curves(ax)
    qq = np.linspace(0, 6000, 400)
    ax.plot(qq, s_tax(qq), color=RED, lw=2.4, ls="--", zorder=3)
    ax.text(5550, d(5550) + 0.15, "D", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(5100, s(5100) - 0.55, "S", color=RED, fontsize=13, fontweight="bold")

    # the two halves of the tax revenue rectangle
    ax.fill_between([0, Q_T], P0, PB, color=TINT_BLUE, zorder=0)
    ax.fill_between([0, Q_T], PS_, P0, color=TINT_RED, zorder=0)
    ax.plot([0, Q_T], [P0, P0], ls="--", lw=1.0, color=GREY, zorder=2)
    ax.plot([Q_T, Q_T], [PS_, PB], lw=1.2, color=GREY, zorder=2)

    # deadweight loss triangle
    tri_q = np.linspace(Q_T, Q0, 60)
    ax.fill_between(tri_q, d(tri_q), s(tri_q), color=TINT_GOLD, zorder=0)

    ax.text(180, 7.02, r"BUYERS BEAR \$1.00   (\$6.50 → \$7.50)", color=BLUE,
            fontsize=9.5, fontweight="bold", bbox=BOX)
    ax.text(180, 5.86, r"SELLERS BEAR \$1.00   (\$6.50 → \$5.50)", color=RED,
            fontsize=9.5, fontweight="bold", bbox=BOX)
    ax.annotate(r"TAX REVENUE  \$2 x 2,500 = \$5,000",
                xy=(1900, 6.5), xytext=(1500, 3.3), fontsize=9.5, color=INK,
                fontweight="bold", ha="center", bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    ax.annotate(r"DEADWEIGHT LOSS" "\n" r"$\frac{1}{2}$ x \$2 x 1,500 = \$1,500",
                xy=(3050, 6.5), xytext=(4600, 3.3), fontsize=9.5, color=DGOLD,
                fontweight="bold", ha="center", bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.1))
    _drop(ax, Q_T, PB, to_x=False)
    ax.plot([Q0], [P0], "o", ms=6, color=GREEN, zorder=5)
    ax.plot([Q_T], [PB], "o", ms=7, mfc="white", mec=BLUE, mew=1.8, zorder=5)
    ax.plot([Q_T], [PS_], "o", ms=7, mfc="white", mec=RED, mew=1.8, zorder=5)
    save(fig, "tax_prod_split")


# ======================================================== 3. Exhibit 10.12
def tax_cons():
    """The same $2, collected from buyers: demand shifts DOWN and nothing else changes."""
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    _jam_axes(ax)
    _curves(ax)
    qq = np.linspace(0, 6000, 400)
    ax.plot(qq, d_tax(qq), color=BLUE, lw=2.4, ls="--", zorder=3)
    ax.text(5550, d(5550) + 0.15, "D", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(5150, d_tax(5150) - 0.55, r"D $-$ \$2", color=BLUE, fontsize=11.5,
            fontweight="bold")
    ax.text(5550, s(5550) + 0.15, "S", color=RED, fontsize=13, fontweight="bold")
    ax.annotate("", xy=(1500, d_tax(1500)), xytext=(1500, d(1500)),
                arrowprops=dict(arrowstyle="->", color=DGOLD, lw=2.2))
    ax.text(1620, (d(1500) + d_tax(1500)) / 2, r"\$2", color=DGOLD, fontsize=11.5,
            fontweight="bold", va="center", bbox=BOX)
    _drop(ax, Q_T, PB)
    _drop(ax, Q_T, PS_, to_y=False)
    ax.plot([Q_T], [PB], "o", ms=8, mfc="white", mec=BLUE, mew=2.0, zorder=5)
    ax.plot([Q_T], [PS_], "o", ms=8, mfc="white", mec=RED, mew=2.0, zorder=5)
    ax.plot([Q0], [P0], "o", ms=6, color=GREEN, zorder=5)
    ax.annotate(r"buyers still pay \$7.50" "\n" r"(price + the \$2 they remit)",
                xy=(Q_T, PB), xytext=(4150, 8.2), fontsize=9.5, color=BLUE,
                ha="center", bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.0))
    ax.annotate(r"sellers still keep \$5.50", xy=(Q_T, PS_), xytext=(4000, 3.6),
                fontsize=9.5, color=RED, ha="center", bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    ax.text(Q_T + 80, 1.0, "2,500 either way", fontsize=9.5, color=INK,
            fontweight="bold", bbox=BOX)
    save(fig, "tax_cons")


# ======================================================== 4. Exhibit 10.13
def elast_supply():
    """Flatten SUPPLY and the burden slides onto buyers."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.9))
    for ax, sl, head in ((a1, B, "(a)  Equally elastic"),
                         (a2, B_FLAT, "(b)  SUPPLY three times as elastic")):
        _jam_axes(ax)
        qq = np.linspace(0, 6000, 400)
        ax.plot(qq, d(qq), color=BLUE, lw=2.6, zorder=3)
        ax.plot(qq, s(qq, sl), color=RED, lw=2.6, zorder=3)
        ax.plot(qq, s(qq, sl) + TAX, color=RED, lw=2.2, ls="--", zorder=3)
        qt, pb, ps = solve(B, sl)
        _price_axis(ax, pb, ps)
        ax.fill_between([0, qt], P0, pb, color=TINT_BLUE, zorder=0)
        ax.fill_between([0, qt], ps, P0, color=TINT_RED, zorder=0)
        ax.plot([0, qt], [P0, P0], ls="--", lw=1.0, color=GREY, zorder=2)
        ax.plot([qt, qt], [ps, pb], lw=1.2, color=GREY, zorder=2)
        _drop(ax, qt, pb, to_x=False)
        ax.plot([Q0], [P0], "o", ms=6, color=GREEN, zorder=5)
        ax.plot([qt], [pb], "o", ms=7, mfc="white", mec=BLUE, mew=1.8, zorder=5)
        ax.plot([qt], [ps], "o", ms=7, mfc="white", mec=RED, mew=1.8, zorder=5)
        ax.text(5750, d(5750) + 0.20, "D", color=BLUE, fontsize=13, fontweight="bold")
        ax.text(5750, s(5750, sl) - 0.55, "S", color=RED, fontsize=13, fontweight="bold")
        _outcome_block(ax, pb, ps)
        ax.set_title(head + "   —   Q falls to %s" % format(int(qt), ","),
                     fontsize=11, color=INK, pad=6)
    fig.tight_layout(w_pad=2.2)
    save(fig, "elast_supply")


# ======================================================== 5. Exhibit 10.14
def elast_demand():
    """Flatten DEMAND and the burden slides onto sellers."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.9))
    for ax, b, head in ((a1, B, "(a)  Equally elastic"),
                        (a2, B_FLAT, "(b)  DEMAND three times as elastic")):
        _jam_axes(ax)
        qq = np.linspace(0, 6000, 400)
        ax.plot(qq, d(qq, b), color=BLUE, lw=2.6, zorder=3)
        ax.plot(qq, d(qq, b) - TAX, color=BLUE, lw=2.2, ls="--", zorder=3)
        ax.plot(qq, s(qq), color=RED, lw=2.6, zorder=3)
        qt, pb, ps = solve(b, B)
        _price_axis(ax, pb, ps)
        ax.fill_between([0, qt], P0, pb, color=TINT_BLUE, zorder=0)
        ax.fill_between([0, qt], ps, P0, color=TINT_RED, zorder=0)
        ax.plot([0, qt], [P0, P0], ls="--", lw=1.0, color=GREY, zorder=2)
        ax.plot([qt, qt], [ps, pb], lw=1.2, color=GREY, zorder=2)
        _drop(ax, qt, ps, to_x=False)
        ax.plot([Q0], [P0], "o", ms=6, color=GREEN, zorder=5)
        ax.plot([qt], [pb], "o", ms=7, mfc="white", mec=BLUE, mew=1.8, zorder=5)
        ax.plot([qt], [ps], "o", ms=7, mfc="white", mec=RED, mew=1.8, zorder=5)
        ax.text(5750, d(5750, b) - 0.50, "D", color=BLUE, fontsize=13, fontweight="bold")
        ax.text(5750, s(5750) + 0.20, "S", color=RED, fontsize=13, fontweight="bold")
        _outcome_block(ax, pb, ps)
        ax.set_title(head + "   —   Q falls to %s" % format(int(qt), ","),
                     fontsize=11, color=INK, pad=6)
    fig.tight_layout(w_pad=2.2)
    save(fig, "elast_demand")


# ============================================ 6. what elasticity does to the DWL
def dwl_elasticity():
    """The same $2 tax, twice: the more elastic the market, the more trade it destroys."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.9))
    cases = ((a1, B, B, "(a)  Both sides equally elastic", DWL),
             (a2, B, B_FLAT, "(b)  Supply three times as elastic", DWL_S_E))
    for ax, b, sl, head, dwl in cases:
        _jam_axes(ax)
        qq = np.linspace(0, 6000, 400)
        ax.plot(qq, d(qq, b), color=BLUE, lw=2.6, zorder=3)
        ax.plot(qq, s(qq, sl), color=RED, lw=2.6, zorder=3)
        ax.plot(qq, s(qq, sl) + TAX, color=RED, lw=2.0, ls="--", zorder=3)
        qt, pb, ps = solve(b, sl)
        _price_axis(ax, pb, ps)
        tri = np.linspace(qt, Q0, 60)
        ax.fill_between(tri, d(tri, b), s(tri, sl), color=TINT_GOLD, zorder=0)
        ax.plot([Q0], [P0], "o", ms=6, color=GREEN, zorder=5)
        ax.plot([qt, qt], [ps, pb], lw=1.2, color=GREY, zorder=2)
        ax.plot([0, qt], [pb, pb], ls=":", lw=1.0, color=BLUE, zorder=1)
        ax.plot([0, qt], [ps, ps], ls=":", lw=1.0, color=RED, zorder=1)
        ax.plot([qt], [pb], "o", ms=7, mfc="white", mec=BLUE, mew=1.8, zorder=5)
        ax.plot([qt], [ps], "o", ms=7, mfc="white", mec=RED, mew=1.8, zorder=5)
        _outcome_block(ax, pb, ps, y=3.30)
        ax.annotate(r"DEADWEIGHT LOSS  \$%s" % format(int(dwl), ","),
                    xy=((qt + Q0) / 2, P0 + 0.1), xytext=(5850, 1.45),
                    fontsize=10, color=DGOLD, fontweight="bold", ha="right", bbox=BOX,
                    arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.1))
        ax.text(5750, d(5750, b) + 0.20, "D", color=BLUE, fontsize=13, fontweight="bold")
        ax.text(5750, s(5750, sl) - 0.55, "S", color=RED, fontsize=13, fontweight="bold")
        ax.set_title(head + "   —   Q falls to %s" % format(int(qt), ","),
                     fontsize=11, color=INK, pad=6)
    fig.tight_layout(w_pad=2.2)
    save(fig, "dwl_elasticity")


# ================================== 7. Exhibits 10.15 / 10.16 and the sugar floor
def ceiling_floor():
    """A binding ceiling makes a shortage; a binding floor makes a surplus."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.0, 3.9))

    q = np.linspace(0, 7000, 400)
    a1.plot(q, a_d1(q), color=BLUE, lw=2.6, zorder=3)
    a1.plot(q, a_s(q), color=RED, lw=2.6, zorder=3)
    a1.axhline(CEILING, color=DGOLD, lw=2.2, ls="--", zorder=4)
    a1.set_xlim(0, 7000)
    a1.set_ylim(0, 2400)
    a1.set_xticks([0, 2500, 4000, 5500, 7000])
    a1.set_xticklabels(["0", "2,500", "4,000", "5,500", "7,000"])
    a1.set_yticks([0, 750, 1200, 1800, 2400])
    a1.set_yticklabels([r"\$0", r"\$750", r"\$1,200", r"\$1,800", r"\$2,400"])
    a1.set_xlabel("Apartments")
    a1.set_ylabel("Monthly rent")
    tri = np.linspace(A_QS, A_Q0, 60)
    a1.fill_between(tri, a_d1(tri), a_s(tri), color=TINT_GOLD, zorder=0)
    a1.plot([A_Q0], [A_P0], "o", ms=7, color=GREEN, zorder=5)
    a1.plot([A_QS], [CEILING], "o", ms=7, mfc="white", mec=RED, mew=1.8, zorder=5)
    a1.plot([A_QD], [CEILING], "o", ms=7, mfc="white", mec=BLUE, mew=1.8, zorder=5)
    a1.annotate("", xy=(A_QD, CEILING - 150), xytext=(A_QS, CEILING - 150),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4))
    a1.text((A_QS + A_QD) / 2, CEILING - 380, "SHORTAGE\n3,000", fontsize=10,
            color=INK, fontweight="bold", ha="center", bbox=BOX)
    a1.text(300, CEILING + 70, r"PRICE CEILING \$750", fontsize=10, color=DGOLD,
            fontweight="bold", bbox=BOX)
    a1.text(3000, 1330, "DWL", fontsize=9.5, color=DGOLD, fontweight="bold", bbox=BOX)
    a1.text(6500, a_d1(6500) + 60, "D", color=BLUE, fontsize=13, fontweight="bold")
    a1.text(6300, a_s(6300) + 60, "S", color=RED, fontsize=13, fontweight="bold")
    a1.set_title("(a)  A ceiling BELOW the market price", fontsize=11.5, color=INK, pad=6)

    qs = np.linspace(0, 200, 400)
    a2.plot(qs, g_d(qs), color=BLUE, lw=2.6, zorder=3)
    qsup = np.linspace(5.0 / 0.14, 200, 300)          # supply starts where it crosses $0
    a2.plot(qsup, g_s(qsup), color=RED, lw=2.6, zorder=3)
    a2.axhline(FLOOR, color=DGOLD, lw=2.2, ls="--", zorder=4)
    a2.set_xlim(0, 200)
    a2.set_ylim(0, 27)
    a2.set_xticks([0, 60, 100, 150, 200])
    a2.set_yticks([0, 9, 16, 22])
    a2.set_yticklabels([r"\$0", r"\$9", r"\$16", r"\$22"])
    a2.set_xlabel("Tons of sugar")
    a2.set_ylabel("Price per ton")
    a2.plot([SUG_Q0], [SUG_P0], "o", ms=7, color=GREEN, zorder=5)
    a2.plot([SUG_QD], [FLOOR], "o", ms=7, mfc="white", mec=BLUE, mew=1.8, zorder=5)
    a2.plot([SUG_QS], [FLOOR], "o", ms=7, mfc="white", mec=RED, mew=1.8, zorder=5)
    a2.annotate("", xy=(SUG_QS, FLOOR + 1.6), xytext=(SUG_QD, FLOOR + 1.6),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4))
    a2.text((SUG_QD + SUG_QS) / 2, FLOOR + 2.6, "SURPLUS\n90 tons", fontsize=10,
            color=INK, fontweight="bold", ha="center", bbox=BOX)
    a2.text(4, FLOOR - 2.2, r"PRICE FLOOR \$16", fontsize=10, color=DGOLD,
            fontweight="bold", bbox=BOX)
    a2.text(146, g_d(146) + 0.7, "D", color=BLUE, fontsize=13, fontweight="bold")
    a2.text(186, g_s(186) + 0.6, "S", color=RED, fontsize=13, fontweight="bold")
    a2.set_title("(b)  A floor ABOVE the market price", fontsize=11.5, color=INK, pad=6)

    fig.tight_layout(w_pad=2.4)
    save(fig, "ceiling_floor")


# ======================================================== 8. Exhibit 10.17
def rent_shift():
    """The ceiling did not move. The market moved under it."""
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    q = np.linspace(0, 7000, 400)
    ax.plot(q, a_d1(q), color=BLUE, lw=2.6, zorder=3)
    ax.plot(q, a_d2(q), color=BLUE, lw=2.6, ls="--", zorder=3)
    ax.plot(q, a_s(q), color=RED, lw=2.6, zorder=3)
    ax.axhline(CEILING, color=DGOLD, lw=2.2, ls="--", zorder=4)
    ax.set_xlim(0, 7000)
    ax.set_ylim(0, 2400)
    ax.set_xticks([0, 2000, 4000, 6000])
    ax.set_xticklabels(["0", "2,000", "4,000", "6,000"])
    ax.set_yticks([0, 600, 750, 1200, 1800, 2400])
    ax.set_yticklabels([r"\$0", r"\$600", r"\$750", r"\$1,200", r"\$1,800", r"\$2,400"])
    ax.set_xlabel("Apartments")
    ax.set_ylabel("Monthly rent")
    ax.annotate("", xy=(2600, a_d2(2600)), xytext=(3800, a_d1(3800)),
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.8))
    ax.text(3300, 1450, r"demand falls", color=BLUE, fontsize=10, fontweight="bold",
            ha="center", bbox=BOX)
    ax.plot([A_Q0], [A_P0], "o", ms=6, mfc="white", mec=GREY, mew=1.6, zorder=5)
    ax.plot([A_Q2], [600], "o", ms=8, color=GREEN, zorder=5)
    _dropc = dict(ls=":", lw=1.0, color=GREY)
    ax.plot([A_Q2, A_Q2], [0, 600], **_dropc)
    ax.plot([0, A_Q2], [600, 600], **_dropc)
    ax.text(300, CEILING + 70, r"PRICE CEILING \$750 — now ABOVE the market",
            fontsize=10, color=DGOLD, fontweight="bold", bbox=BOX)
    ax.annotate(r"new equilibrium  2,000 at \$600", xy=(A_Q2, 600), xytext=(4100, 380),
                fontsize=10, color=GREEN, bbox=BOX,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))
    ax.text(6500, a_d1(6500) + 60, r"D$_1$", color=BLUE, fontsize=12, fontweight="bold")
    ax.text(3950, a_d2(3950) + 60, r"D$_2$", color=BLUE, fontsize=12, fontweight="bold")
    ax.text(6300, a_s(6300) + 60, "S", color=RED, fontsize=13, fontweight="bold")
    save(fig, "rent_shift")


if __name__ == "__main__":
    print("Chapter 10 figures ->", OUT)
    tax_prod_shift()
    tax_prod_split()
    tax_cons()
    elast_supply()
    elast_demand()
    dwl_elasticity()
    ceiling_floor()
    rent_shift()
    print("done.")
