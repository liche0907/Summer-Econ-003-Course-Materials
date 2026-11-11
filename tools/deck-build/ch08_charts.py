#!/usr/bin/env python3
"""ECON 003 - Chapter 8 (Trade) figures.

matplotlib, UCR palette, Liberation Sans (Arial metrics).  Blue = demand, red = supply,
everywhere, permanently.

EVERY NUMBER IS DERIVED, NOT DRAWN TO LOOK RIGHT.  Two stated primitives generate the
whole chapter, and every headline figure is asserted at import so a later edit that
breaks the arithmetic fails loudly.

  PARTS 1-3   two producers, an eight-hour day, two goods
                Maya  12 burritos/h  or  12 smoothies/h   ->   B +  S = 96
                Owen   4 burritos/h  or   8 smoothies/h   ->  2B +  S = 64
              opportunity cost of one burrito:  Maya 1 smoothie,  Owen 2 smoothies
              so Maya has the comparative advantage in burritos, Owen in smoothies,
              EVEN THOUGH Maya has the absolute advantage in both (12>4 and 12>8).
              That is the whole teaching point and the numbers are chosen for it.

              autarky      Maya 6h on burritos -> (72 B, 24 S)
                           Owen 4h on burritos -> (16 B, 32 S)      total (88, 56)
              specialise   Maya 96 B,  Owen 64 S                    total (96, 64)
              so specialisation raises BOTH totals, by 8 and 8.  This is not automatic:
              with a 50/50 autarky split it is arithmetically impossible when one
              producer has the absolute advantage in both goods.  The autarky hours
              (6 and 4) were solved for, not assumed - see the assertions below.

              terms of trade  1 burrito = 1.5 smoothies, which lies strictly between
              the two opportunity costs (1 and 2), as it must for both to gain.
              Maya ships 18 B, receives 27 S  ->  (78 B, 27 S)   gains +6 B, +3 S
              Owen ships 27 S, receives 18 B  ->  (18 B, 37 S)   gains +2 B, +5 S
              both consume OUTSIDE their own production possibilities curve.

  PART 4      the US market for raw sugar, cents per pound against millions of pounds
              per week.  Illustrative linear schedules, but deliberately scaled to the
              real price range (US raw sugar traded at 35.50 c/lb in June 2026):
                D:  Qd = 100 - P          S:  Qs = P - 20
              autarky                P = 60,  Q = 40
              world price 40         Qs 20, Qd 60, imports 40
                                     CS +1000, PS -600,  net gain +400
              world price 80         Qs 60, Qd 20, exports 40
                                     CS -600,  PS +1000, net gain +400
              tariff of 10 on top of a world price of 40   ->   domestic price 50
                                     Qs 30, Qd 50, imports 20
                                     CS -550, PS +250, revenue +200, DWL -100
              and the deadweight loss splits into two equal triangles of 50 each, the
              production distortion (A) and the consumption distortion (B).  The book's
              end-of-chapter question asks students to explain exactly those two areas,
              so they are lettered A and B on the figure to match.

REAL DATA ON THREE FIGURES, and only these three.  Everything else above is a stated
model.  Sources and dates are on the slide credit lines:
  sugar_prices    ICE No. 11 (world) and No. 16 (US) raw sugar, monthly, IMF via FRED
                  series PSUGAISAUSDM and PSUGAUSAUSDM, both updated 13 July 2026.
  tariff_rate     duties collected / value of imports.  2024 and 2025 from USAFacts on
                  Census data (page updated 16 Apr 2026); June 2026 from Penn Wharton
                  (published 10 Aug 2026).  Same definition throughout - the Yale
                  Budget Lab's 11.0% is the STATUTORY average and is drawn separately,
                  because mixing the two definitions overstates the change.
  household_cost  Yale Budget Lab \\$1,100 and Tax Foundation \\$900, both 11 Aug 2026.

Run:  python3 ch08_charts.py [outdir]
"""
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

# ----------------------------------------------------------------- house style
BLUE = "#003DA5"      # demand, and the first producer
RED = "#CC3333"       # supply
GREEN = "#2E7D32"     # gains, the "benefit" side of a contrast
DGOLD = "#B88300"     # the second producer, secondary curves
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


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, facecolor="white")
    plt.close(fig)
    print("  ", name)


# ======================================================== PRIMITIVES, PARTS 1-3
HOURS = 8
MAYA_B, MAYA_S = 12, 12        # units per hour
OWEN_B, OWEN_S = 4, 8

MAYA_MAX_B, MAYA_MAX_S = MAYA_B * HOURS, MAYA_S * HOURS      # 96, 96
OWEN_MAX_B, OWEN_MAX_S = OWEN_B * HOURS, OWEN_S * HOURS      # 32, 64

# opportunity cost of ONE burrito, in smoothies
MAYA_OC = MAYA_S / MAYA_B      # 1.0
OWEN_OC = OWEN_S / OWEN_B      # 2.0

# autarky: hours each spends on burritos
MAYA_H, OWEN_H = 6, 4
MAYA_A = (MAYA_B * MAYA_H, MAYA_S * (HOURS - MAYA_H))        # (72, 24)
OWEN_A = (OWEN_B * OWEN_H, OWEN_S * (HOURS - OWEN_H))        # (16, 32)
AUT_B, AUT_S = MAYA_A[0] + OWEN_A[0], MAYA_A[1] + OWEN_A[1]  # (88, 56)

# complete specialisation along comparative advantage
SPEC_B, SPEC_S = MAYA_MAX_B, OWEN_MAX_S                      # (96, 64)

TOT = 1.5                       # terms of trade: smoothies per burrito
SHIP_B = 18                     # burritos Maya ships
SHIP_S = int(SHIP_B * TOT)      # 27 smoothies back

MAYA_T = (MAYA_MAX_B - SHIP_B, SHIP_S)                       # (78, 27)
OWEN_T = (SHIP_B, OWEN_MAX_S - SHIP_S)                       # (18, 37)

# -- assertions: if any of this stops being true, the deck is wrong, loudly ----
assert (MAYA_B > OWEN_B) and (MAYA_S > OWEN_S), "Maya must have BOTH absolute advantages"
assert MAYA_OC < OWEN_OC, "Maya must have the comparative advantage in burritos"
assert MAYA_OC == 1.0 and OWEN_OC == 2.0
assert MAYA_A == (72, 24) and OWEN_A == (16, 32)
assert (AUT_B, AUT_S) == (88, 56)
assert (SPEC_B, SPEC_S) == (96, 64)
assert SPEC_B > AUT_B and SPEC_S > AUT_S, "specialisation must raise BOTH totals"
assert MAYA_OC < TOT < OWEN_OC, "terms of trade must lie between the opportunity costs"
assert MAYA_T == (78, 27) and OWEN_T == (18, 37)
assert MAYA_T[0] + OWEN_T[0] == SPEC_B and MAYA_T[1] + OWEN_T[1] == SPEC_S, \
    "consumption must add up to production"
assert MAYA_T[0] > MAYA_A[0] and MAYA_T[1] > MAYA_A[1], "Maya must gain in BOTH goods"
assert OWEN_T[0] > OWEN_A[0] and OWEN_T[1] > OWEN_A[1], "Owen must gain in BOTH goods"
# each consumes outside their own PPC
assert MAYA_T[0] / MAYA_MAX_B + MAYA_T[1] / MAYA_MAX_S > 1
assert OWEN_T[0] / OWEN_MAX_B + OWEN_T[1] / OWEN_MAX_S > 1

MAYA_GAIN = (MAYA_T[0] - MAYA_A[0], MAYA_T[1] - MAYA_A[1])   # (+6, +3)
OWEN_GAIN = (OWEN_T[0] - OWEN_A[0], OWEN_T[1] - OWEN_A[1])   # (+2, +5)


# ========================================================= PRIMITIVES, PART 4
# US market for raw sugar.  P in cents per pound, Q in millions of pounds per week.
def qd(p):
    return 100.0 - p


def qs(p):
    return p - 20.0


P_AUT = 60.0
Q_AUT = qd(P_AUT)
P_LOW = 40.0            # world price, importing case
P_HIGH = 80.0           # world price, exporting case
TARIFF = 10.0
P_TAR = P_LOW + TARIFF

IMP_QS, IMP_QD = qs(P_LOW), qd(P_LOW)                # 20, 60
IMPORTS = IMP_QD - IMP_QS                            # 40
EXP_QS, EXP_QD = qs(P_HIGH), qd(P_HIGH)              # 60, 20
EXPORTS = EXP_QS - EXP_QD                            # 40
TAR_QS, TAR_QD = qs(P_TAR), qd(P_TAR)                # 30, 50
TAR_IMPORTS = TAR_QD - TAR_QS                        # 20


def cs(p):
    """Consumer surplus under a linear demand with choke price 100."""
    return 0.5 * (100.0 - p) ** 2


def ps(p):
    """Producer surplus above a linear supply that starts at 20."""
    return 0.5 * max(p - 20.0, 0.0) ** 2


CS_AUT, PS_AUT = cs(P_AUT), ps(P_AUT)                # 800, 800
IMP_CS_GAIN = cs(P_LOW) - CS_AUT                     # +1000
IMP_PS_LOSS = ps(P_LOW) - PS_AUT                     # -600
IMP_NET = IMP_CS_GAIN + IMP_PS_LOSS                  # +400
EXP_CS_LOSS = cs(P_HIGH) - CS_AUT                    # -600
EXP_PS_GAIN = ps(P_HIGH) - PS_AUT                    # +1000
EXP_NET = EXP_CS_LOSS + EXP_PS_GAIN                  # +400

TAR_CS = cs(P_TAR) - cs(P_LOW)                       # -550
TAR_PS = ps(P_TAR) - ps(P_LOW)                       # +250
TAR_REV = TARIFF * TAR_IMPORTS                       # +200
TAR_DWL = -(TAR_CS + TAR_PS + TAR_REV)               # 100
AREA_A = 0.5 * (TAR_QS - IMP_QS) * TARIFF            # 50, production distortion
AREA_B = 0.5 * (IMP_QD - TAR_QD) * TARIFF            # 50, consumption distortion

assert (P_AUT, Q_AUT) == (60.0, 40.0)
assert (IMP_QS, IMP_QD, IMPORTS) == (20.0, 60.0, 40.0)
assert (EXP_QS, EXP_QD, EXPORTS) == (60.0, 20.0, 40.0)
assert (TAR_QS, TAR_QD, TAR_IMPORTS) == (30.0, 50.0, 20.0)
assert (IMP_CS_GAIN, IMP_PS_LOSS, IMP_NET) == (1000.0, -600.0, 400.0)
assert (EXP_CS_LOSS, EXP_PS_GAIN, EXP_NET) == (-600.0, 1000.0, 400.0)
assert (TAR_CS, TAR_PS, TAR_REV) == (-550.0, 250.0, 200.0)
assert TAR_DWL == 100.0 and AREA_A == 50.0 and AREA_B == 50.0
assert AREA_A + AREA_B == TAR_DWL, "the two triangles must be the whole deadweight loss"


# ======================================================== REAL DATA, PART 4
# ICE No. 11 (world) and No. 16 (US) raw sugar, US cents per pound, monthly.
SUGAR_MONTHS = ["Mar 2026", "Apr 2026", "May 2026", "Jun 2026"]
SUGAR_WORLD = [14.80, 14.09, 14.77, 13.91]
SUGAR_US = [33.40, 34.76, 36.00, 35.50]
SUGAR_GAP = SUGAR_US[-1] - SUGAR_WORLD[-1]           # 21.59
SUGAR_RATIO = SUGAR_US[-1] / SUGAR_WORLD[-1]         # 2.55x
assert round(SUGAR_GAP, 2) == 21.59
assert 2.5 < SUGAR_RATIO < 2.6

# the statutory numbers, from the tariff schedule and the Federal Register
TRQ_TONNES = 1_117_195               # FY2027 raw cane sugar TRQ, metric tons raw value
IN_QUOTA = 0.66                      # cents per pound, 1.4606 c/kg
OVER_QUOTA = 15.36                   # cents per pound, 33.87 c/kg

# average effective tariff rate: duties collected / value of imports
TAR_YEARS = ["2024", "2025", "Jun 2026"]
TAR_RATES = [2.3, 7.7, 7.1]
STATUTORY_2026 = 11.0                # Yale Budget Lab, a DIFFERENT definition

# Fajgelbaum & Khandelwal, Brookings Papers on Economic Activity, March 2026:
# roughly 90% of the tariff showed up in tariff-inclusive US prices (range 80-100%).
PASSTHROUGH = 90.0

HH_LABELS = ["Tax Foundation", "Yale Budget Lab"]
HH_COST = [900, 1100]


# ================================================================== helpers
def ppc_axes(ax, maxb, maxs, xlab="Burritos per day", ylab="Smoothies per day"):
    ax.set_xlim(0, maxb * 1.12)
    ax.set_ylim(0, maxs * 1.12)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)


def dot(ax, x, y, color, label=None, dx=6, dy=6, size=52, ha="left", va="bottom",
        weight="bold", fs=10.5):
    ax.scatter([x], [y], s=size, color=color, zorder=6, edgecolor="white", linewidth=1.1)
    if label:
        ax.annotate(label, (x, y), xytext=(dx, dy), textcoords="offset points",
                    fontsize=fs, color=color, fontweight=weight, ha=ha, va=va)


# ============================================================ 1. one PPC
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ppc_axes(ax, MAYA_MAX_B, MAYA_MAX_S)
ax.fill_between([0, MAYA_MAX_B], [MAYA_MAX_S, 0], color=TINT_BLUE, alpha=0.55, zorder=1)
ax.plot([0, MAYA_MAX_B], [MAYA_MAX_S, 0], color=BLUE, lw=2.6, zorder=4)

dot(ax, 72, 24, BLUE, "C  on the curve\nevery hour used", dx=9, dy=9)
dot(ax, 40, 20, GREY, "D  inside\nan hour wasted", dx=9, dy=-9, va="top")
dot(ax, 52, 72, RED, "U  outside\nnot enough hours", dx=9, dy=9)
# both axes span the same range, so a -45 degree label lies along the curve exactly
ax.annotate("Maya's production possibilities curve", (5, 93), fontsize=10.5,
            color=BLUE, fontweight="bold", rotation=-45, rotation_mode="anchor",
            ha="left", va="bottom")
ax.annotate("attainable\nand efficient", (6, 26), fontsize=10.5, color=BLUE,
            fontweight="bold", ha="left")
ax.set_title("Eight hours, two things to make: everything Maya could produce in a day",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08_fig_ppc_one.png")


# ============================================== 2. the slope IS opportunity cost
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ppc_axes(ax, MAYA_MAX_B, MAYA_MAX_S)
ax.plot([0, MAYA_MAX_B], [MAYA_MAX_S, 0], color=BLUE, lw=2.6, zorder=4)

x0, y0 = 48, 48
x1, y1 = 60, 36
ax.plot([x0, x1], [y0, y0], color=RED, lw=2.2, zorder=5)
ax.plot([x1, x1], [y0, y1], color=RED, lw=2.2, zorder=5)
dot(ax, x0, y0, BLUE, "", size=44)
dot(ax, x1, y1, BLUE, "", size=44)
ax.annotate("+12 burritos", ((x0 + x1) / 2, y0 + 2.5), fontsize=10.5, color=RED,
            fontweight="bold", ha="center")
ax.annotate("−12 smoothies", (x1 + 2.5, (y0 + y1) / 2), fontsize=10.5, color=RED,
            fontweight="bold", ha="left", va="center")
ax.annotate("slope = −1\nso 1 burrito costs 1 smoothie",
            (MAYA_MAX_B * 0.60, MAYA_MAX_S * 0.78), fontsize=11, color=BLUE,
            fontweight="bold", ha="center")
ax.set_title("The slope of the curve is the opportunity cost — that is what it is FOR",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08_fig_ppc_slope.png")


# ============================================================ 3. two PPCs
fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))
for ax, (name, mb, ms, col, oc) in zip(axes, [
        ("Maya", MAYA_MAX_B, MAYA_MAX_S, BLUE, MAYA_OC),
        ("Owen", OWEN_MAX_B, OWEN_MAX_S, DGOLD, OWEN_OC)]):
    ax.set_xlim(0, 108)
    ax.set_ylim(0, 108)
    ax.set_xlabel("Burritos per day")
    ax.set_ylabel("Smoothies per day")
    ax.plot([0, mb], [ms, 0], color=col, lw=2.6, zorder=4)
    ax.fill_between([0, mb], [ms, 0], color=col, alpha=0.10, zorder=1)
    ax.scatter([mb, 0], [0, ms], s=44, color=col, zorder=5)
    ax.annotate(f"{mb} burritos", (mb, 0), xytext=(4, 8), textcoords="offset points",
                fontsize=10, color=col, fontweight="bold")
    ax.annotate(f"{ms} smoothies", (0, ms), xytext=(6, 2), textcoords="offset points",
                fontsize=10, color=col, fontweight="bold")
    ax.set_title(f"{name}   ·   1 burrito costs {oc:g} smoothie{'s' if oc != 1 else ''}",
                 fontsize=11.5, color=col, fontweight="bold", pad=8)
fig.suptitle("Same axes, same scale: Maya's curve is further out everywhere — and flatter",
             fontsize=11, color=INK, fontweight="bold", y=1.03)
save(fig, "ch08_fig_ppc_two.png")


# ================================================= 4. absolute advantage bars
fig, ax = plt.subplots(figsize=(8.6, 3.6))
xs = np.arange(2)
w = 0.34
ax.bar(xs - w / 2, [MAYA_B, MAYA_S], width=w, color=BLUE, label="Maya")
ax.bar(xs + w / 2, [OWEN_B, OWEN_S], width=w, color=DGOLD, label="Owen")
for i, (a, b) in enumerate([(MAYA_B, OWEN_B), (MAYA_S, OWEN_S)]):
    ax.annotate(str(a), (i - w / 2, a), xytext=(0, 4), textcoords="offset points",
                ha="center", fontsize=11, color=BLUE, fontweight="bold")
    ax.annotate(str(b), (i + w / 2, b), xytext=(0, 4), textcoords="offset points",
                ha="center", fontsize=11, color=DGOLD, fontweight="bold")
ax.set_xticks(xs)
ax.set_xticklabels(["Burritos per hour", "Smoothies per hour"], fontsize=11)
ax.set_ylabel("Units produced in one hour")
ax.set_ylim(0, 15.5)
ax.legend(frameon=False, fontsize=10.5, loc="upper right")
ax.set_title("Maya is faster at both. Absolute advantage says nothing about who should "
             "do what.", fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08_fig_advantage.png")


# ============================== 5. consumption beyond your own PPC (two panels)
fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))
# Each panel is scaled to its own producer, but BOTH axes shrink by the same 2.08x
# factor from Maya's panel to Owen's, so the slopes stay visually comparable.
panels = [
    ("Maya", MAYA_MAX_B, MAYA_MAX_S, BLUE, MAYA_A, MAYA_T,
     [(MAYA_MAX_B, 0), (0, MAYA_MAX_B * TOT)], 100, 150),
    ("Owen", OWEN_MAX_B, OWEN_MAX_S, DGOLD, OWEN_A, OWEN_T,
     [(0, OWEN_MAX_S), (OWEN_MAX_S / TOT, 0)], 48, 72),
]
for ax, (name, mb, ms, col, aut, tr, line, xm, ym) in zip(axes, panels):
    ax.set_xlim(0, xm)
    ax.set_ylim(0, ym)
    ax.set_xlabel("Burritos per day")
    ax.set_ylabel("Smoothies per day")
    ax.plot([0, mb], [ms, 0], color=col, lw=2.4, zorder=4)
    ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]],
            color=GREEN, lw=2.4, ls="--", zorder=4)
    dot(ax, aut[0], aut[1], GREY, f"alone ({aut[0]}, {aut[1]})", dx=-10, dy=-18,
        ha="right", va="top", fs=10)
    dot(ax, tr[0], tr[1], GREEN, f"with trade ({tr[0]}, {tr[1]})", dx=6, dy=10, fs=10)
    if name == "Maya":       # label the two curves once; Owen's panel has no room
        ax.annotate("what they can MAKE", (mb * 0.30, ms * 0.50), fontsize=9.5,
                    color=col, fontweight="bold", ha="center",
                    bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.6))
        ax.annotate("what they can EAT", (mb * 0.34, ms * 0.94), fontsize=9.5,
                    color=GREEN, fontweight="bold", ha="center",
                    bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.6))
    ax.set_title(f"{name}", fontsize=11.5, color=col, fontweight="bold", pad=8)
fig.suptitle("Trade at 1 burrito = 1.5 smoothies puts BOTH of them outside their own "
             "curve  (note: the two panels are drawn to different scales)",
             fontsize=11, color=INK, fontweight="bold", y=1.03)
save(fig, "ch08_fig_trade_line.png")


# ================================================= 6. the joint PPC (kinked)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ax.set_xlim(0, 142)
ax.set_ylim(0, 178)
ax.set_xlabel("Burritos per day, the two of them together")
ax.set_ylabel("Smoothies per day, together")
jx = [0, MAYA_MAX_B, MAYA_MAX_B + OWEN_MAX_B]
jy = [MAYA_MAX_S + OWEN_MAX_S, OWEN_MAX_S, 0]
ax.fill_between(jx, jy, color=TINT_BLUE, alpha=0.5, zorder=1)
ax.plot(jx, jy, color=BLUE, lw=2.6, zorder=4)
dot(ax, SPEC_B, SPEC_S, GREEN, f"both specialise ({SPEC_B}, {SPEC_S})", dx=12, dy=16)
dot(ax, AUT_B, AUT_S, GREY, f"neither trades ({AUT_B}, {AUT_S})", dx=-10, dy=-20,
    ha="right", va="top")
ax.annotate("", xy=(SPEC_B, SPEC_S), xytext=(AUT_B, AUT_S),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.0, shrinkA=7, shrinkB=7))
ax.annotate("+8 burritos and +8 smoothies,\nout of the same sixteen hours",
            (60, 62), fontsize=10.5, color=GREEN, fontweight="bold", ha="center",
            bbox=dict(fc="white", ec="none", alpha=0.9, pad=2.0))
ax.annotate("Maya switches\n(1 smoothie per burrito)", (24, 143), fontsize=9.5,
            color=BLUE, fontweight="bold", ha="left")
ax.annotate("Owen switches\n(2 smoothies per burrito)", (121, 58), fontsize=9.5,
            color=DGOLD, fontweight="bold", ha="center")
ax.set_title("The kink is the answer: specialisation lands them exactly on the corner",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08_fig_ppc_joint.png")


# ====================================== 7. many producers -> a bowed-out PPC
fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))

# four producers, ordered by comparative advantage in good X
prods = [(30, 10), (24, 16), (16, 24), (10, 30)]     # (max X, max Y) each
ax = axes[0]
cx, cy = [0.0], [sum(p[1] for p in prods)]
for mx, my in prods:                                  # steepest OC last
    cx.append(cx[-1] + mx)
    cy.append(cy[-1] - my)
ax.plot(cx, cy, color=BLUE, lw=2.4, marker="o", ms=5, zorder=4)
ax.fill_between(cx, cy, color=TINT_BLUE, alpha=0.5, zorder=1)
ax.set_xlim(0, 88)
ax.set_ylim(0, 88)
ax.set_xlabel("Good X")
ax.set_ylabel("Good Y")
ax.set_title("Four producers: a staircase", fontsize=11.5, color=INK,
             fontweight="bold", pad=8)

ax = axes[1]
t = np.linspace(0, np.pi / 2, 300)
sx, sy = 80 * np.sin(t), 80 * np.cos(t)
ax.plot(sx, sy, color=BLUE, lw=2.6, zorder=4)
ax.fill_between(sx, sy, color=TINT_BLUE, alpha=0.5, zorder=1)
ax.set_xlim(0, 88)
ax.set_ylim(0, 88)
ax.set_xlabel("Good X")
ax.set_ylabel("Good Y")
ax.annotate("cheapest producers\nswitch first", (16, 66), fontsize=10, color=GREY,
            fontweight="bold", ha="left")
ax.annotate("by here only the\nworst are left", (52, 22), fontsize=10, color=GREY,
            fontweight="bold", ha="left")
ax.set_title("A whole economy: a smooth curve, bowed out", fontsize=11.5, color=INK,
             fontweight="bold", pad=8)
fig.suptitle("An economy is millions of different opportunity costs, taken cheapest "
             "first", fontsize=11, color=INK, fontweight="bold", y=1.03)
save(fig, "ch08_fig_ppc_economy.png")


# ================================================== 8. the market, no trade
def market_frame(ax):
    p = np.linspace(20, 100, 200)
    ax.plot(qd(np.linspace(0, 100, 200)), np.linspace(0, 100, 200), color=BLUE, lw=2.6,
            zorder=4)
    ax.plot(qs(p), p, color=RED, lw=2.6, zorder=4)
    ax.set_xlim(0, 92)
    ax.set_ylim(0, 104)
    ax.set_xlabel("Millions of pounds of sugar per week")
    ax.set_ylabel("Cents per pound")
    ax.annotate("D", (qd(12) + 1.5, 12), fontsize=12, color=BLUE, fontweight="bold")
    ax.annotate("S", (qs(92) + 2.2, 92), fontsize=12, color=RED, fontweight="bold")


fig, ax = plt.subplots(figsize=(8.6, 3.6))
market_frame(ax)
ax.add_patch(Polygon([(0, P_AUT), (0, 100), (Q_AUT, P_AUT)], fc=TINT_BLUE, ec="none",
                     zorder=2))
ax.add_patch(Polygon([(0, P_AUT), (0, 20), (Q_AUT, P_AUT)], fc=TINT_RED, ec="none",
                     zorder=2))
ax.plot([0, Q_AUT], [P_AUT, P_AUT], color=INK, lw=1.0, ls=":", zorder=3)
ax.plot([Q_AUT, Q_AUT], [0, P_AUT], color=INK, lw=1.0, ls=":", zorder=3)
dot(ax, Q_AUT, P_AUT, INK, "", size=48)
ax.annotate("CS = 800", (13, 74), fontsize=10.5, color=BLUE, fontweight="bold")
ax.annotate("PS = 800", (13, 44), fontsize=10.5, color=RED, fontweight="bold")
ax.annotate(r"60¢, 40m lb", (Q_AUT + 2, P_AUT + 2), fontsize=10.5, color=INK,
            fontweight="bold")
ax.set_title("A closed market: the US price is whatever clears the US market",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08_fig_market_autarky.png")


# ================================================== 9. imports at a world price
fig, ax = plt.subplots(figsize=(8.6, 3.6))
market_frame(ax)
ax.axhline(P_LOW, color=GREEN, lw=2.2, ls="--", zorder=3)
ax.plot([IMP_QS, IMP_QD], [P_LOW, P_LOW], color=GREEN, lw=5.0, alpha=0.35, zorder=3,
        solid_capstyle="butt")
ax.add_patch(Polygon([(0, P_AUT), (Q_AUT, P_AUT), (IMP_QD, P_LOW), (0, P_LOW)],
                     fc=TINT_GREEN, ec=GREEN, lw=0.8, zorder=2))
ax.plot([0, IMP_QS], [P_LOW, P_LOW], color=INK, lw=0.8, ls=":", zorder=3)
dot(ax, Q_AUT, P_AUT, GREY, "", size=40)
dot(ax, IMP_QS, P_LOW, RED, "", size=44)
dot(ax, IMP_QD, P_LOW, BLUE, "", size=44)
ax.annotate("world price 40¢", (78, P_LOW + 3), fontsize=10.5, color=GREEN,
            fontweight="bold", ha="right")
ax.annotate(f"imports = {IMPORTS:.0f}m lb", ((IMP_QS + IMP_QD) / 2, P_LOW - 8),
            fontsize=10.5, color=GREEN, fontweight="bold", ha="center")
ax.annotate("consumers gain 1,000\nproducers lose 600\nnet gain 400", (2, 64),
            fontsize=10.5, color=INK, fontweight="bold", ha="left", va="top",
            bbox=dict(fc="white", ec="none", alpha=0.92, pad=2.4))
ax.set_title("Open the border: the price falls to 40¢, and the country gains 400",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08_fig_market_import.png")


# ================================================== 10. exports
fig, ax = plt.subplots(figsize=(8.6, 3.6))
market_frame(ax)
ax.axhline(P_HIGH, color=GREEN, lw=2.2, ls="--", zorder=3)
ax.plot([EXP_QD, EXP_QS], [P_HIGH, P_HIGH], color=GREEN, lw=5.0, alpha=0.35, zorder=3,
        solid_capstyle="butt")
ax.add_patch(Polygon([(0, P_AUT), (Q_AUT, P_AUT), (EXP_QS, P_HIGH), (0, P_HIGH)],
                     fc=TINT_GREEN, ec=GREEN, lw=0.8, zorder=2))
dot(ax, Q_AUT, P_AUT, GREY, "", size=40)
dot(ax, EXP_QD, P_HIGH, BLUE, "", size=44)
dot(ax, EXP_QS, P_HIGH, RED, "", size=44)
ax.annotate("world price 80¢", (2, P_HIGH + 8), fontsize=10.5, color=GREEN,
            fontweight="bold", ha="left", va="bottom",
            bbox=dict(fc="white", ec="none", alpha=0.92, pad=2.0))
ax.annotate(f"exports = {EXPORTS:.0f}m lb", ((EXP_QD + EXP_QS) / 2, P_HIGH - 9),
            fontsize=10.5, color=GREEN, fontweight="bold", ha="center")
ax.annotate("producers gain 1,000\nconsumers lose 600\nnet gain 400", (46, 26),
            fontsize=10.5, color=INK, fontweight="bold", ha="left", va="top",
            bbox=dict(fc="white", ec="none", alpha=0.92, pad=2.4))
ax.set_title("Same country, higher world price: now we export — and gain 400 again",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08_fig_market_export.png")


# ================================================== 11. a tariff, areas A and B
fig, ax = plt.subplots(figsize=(8.6, 3.6))
market_frame(ax)
ax.axhline(P_LOW, color=GREY, lw=1.6, ls="--", zorder=3)
ax.axhline(P_TAR, color=RED, lw=2.2, ls="--", zorder=3)

# government revenue rectangle
ax.add_patch(Rectangle((TAR_QS, P_LOW), TAR_IMPORTS, TARIFF, fc=TINT_GOLD, ec=DGOLD,
                       lw=0.9, zorder=2))
# deadweight loss triangles
ax.add_patch(Polygon([(IMP_QS, P_LOW), (TAR_QS, P_LOW), (TAR_QS, P_TAR)],
                     fc=TINT_RED, ec=RED, lw=1.0, zorder=2))
ax.add_patch(Polygon([(TAR_QD, P_TAR), (IMP_QD, P_LOW), (TAR_QD, P_LOW)],
                     fc=TINT_RED, ec=RED, lw=1.0, zorder=2))
ax.annotate("A", (TAR_QS - 3.6, P_LOW + 2.0), fontsize=12.5, color=RED, fontweight="bold")
ax.annotate("B", (TAR_QD + 1.8, P_LOW + 2.0), fontsize=12.5, color=RED, fontweight="bold")
ax.annotate("tariff revenue 200", ((TAR_QS + TAR_QD) / 2, P_LOW + TARIFF / 2),
            fontsize=9.5, color=DGOLD, fontweight="bold", ha="center", va="center")

for q, c in [(TAR_QS, RED), (TAR_QD, BLUE)]:
    dot(ax, q, P_TAR, c, "", size=42)
ax.annotate("with tariff  50¢", (90, P_TAR + 2.5), fontsize=10.5, color=RED,
            fontweight="bold", ha="right")
ax.annotate("world price  40¢", (90, P_LOW - 8.0), fontsize=10.5, color=GREY,
            fontweight="bold", ha="right")
ax.annotate(f"imports fall {IMPORTS:.0f} → {TAR_IMPORTS:.0f} million pounds\n"
            "A + B = 100 lost, and nobody collects it", (3, 5), fontsize=10.5,
            color=RED, fontweight="bold", ha="left", va="bottom")
ax.set_title("A 10¢ tariff: A is the production distortion, B the consumption distortion",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08_fig_market_tariff.png")


# ============================================== 12. the tariff ledger, waterfall
fig, ax = plt.subplots(figsize=(8.6, 3.6))
items = [("Consumers", TAR_CS, RED), ("Producers", TAR_PS, GREEN),
         ("Government", TAR_REV, DGOLD), ("Net", TAR_CS + TAR_PS + TAR_REV, RED)]
xs = np.arange(len(items))
for i, (lab, v, c) in enumerate(items):
    ax.bar(i, v, width=0.55, color=c, alpha=0.90 if lab != "Net" else 1.0,
           hatch="" if lab != "Net" else "//", edgecolor=c)
    ax.annotate(f"{v:+,.0f}", (i, v), xytext=(0, 6 if v > 0 else -16),
                textcoords="offset points", ha="center", fontsize=11.5, color=c,
                fontweight="bold")
ax.axhline(0, color=INK, lw=1.1)
ax.set_xticks(xs)
ax.set_xticklabels([i[0] for i in items], fontsize=11)
ax.set_ylabel("Change in surplus")
ax.set_ylim(-700, 400)
ax.annotate("the 100 in the gap between\n+450 gained and 550 lost is the\ndeadweight loss "
            "— it goes nowhere", (2.62, -430), fontsize=10, color=RED, fontweight="bold",
            ha="center")
ax.set_title("Every tariff is a transfer plus a loss. Only the loss is nobody's gain.",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08_fig_tariff_ledger.png")


# ============================================== 13. the two-tier quota (real)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
q1 = TRQ_TONNES / 1e6
ax.plot([0, q1], [IN_QUOTA, IN_QUOTA], color=GREEN, lw=3.0, zorder=4)
ax.plot([q1, q1], [IN_QUOTA, OVER_QUOTA], color=RED, lw=3.0, ls=":", zorder=4)
ax.plot([q1, q1 * 2.05], [OVER_QUOTA, OVER_QUOTA], color=RED, lw=3.0, zorder=4)
ax.axvline(q1, color=INK, lw=1.0, ls="--", zorder=3)
ax.set_xlim(0, q1 * 2.05)
ax.set_ylim(0, 19)
ax.set_xlabel("Raw cane sugar imported in the year (millions of metric tons)")
ax.set_ylabel("Tariff paid, cents per pound")
ax.annotate(f"{IN_QUOTA}¢ per pound\nup to the quota", (q1 * 0.45, IN_QUOTA + 1.2),
            fontsize=11, color=GREEN, fontweight="bold", ha="center")
ax.annotate(f"{OVER_QUOTA}¢ per pound\nafter it", (q1 * 1.48, OVER_QUOTA - 4.6),
            fontsize=11, color=RED, fontweight="bold", ha="center")
ax.annotate(f"the quota:\n{TRQ_TONNES:,} tonnes", (q1, 17.6), fontsize=10.5, color=INK,
            fontweight="bold", ha="center", va="top",
            bbox=dict(fc="white", ec=INK, lw=0.8, pad=3))
ax.set_title("US sugar, FY2027: the tariff is near zero — until one number is reached",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08_fig_quota.png")


# ============================================ 14. US vs world sugar price (real)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
xs = np.arange(len(SUGAR_MONTHS))
ax.plot(xs, SUGAR_US, color=RED, lw=2.6, marker="o", ms=7, label="US raw sugar (No. 16)")
ax.plot(xs, SUGAR_WORLD, color=BLUE, lw=2.6, marker="o", ms=7,
        label="World raw sugar (No. 11)")
ax.fill_between(xs, SUGAR_WORLD, SUGAR_US, color=TINT_RED, alpha=0.55)
for x, (u, w) in enumerate(zip(SUGAR_US, SUGAR_WORLD)):
    ax.annotate(f"{u:.2f}", (x, u), xytext=(0, 7), textcoords="offset points",
                ha="center", fontsize=10, color=RED, fontweight="bold")
    ax.annotate(f"{w:.2f}", (x, w), xytext=(0, -16), textcoords="offset points",
                ha="center", fontsize=10, color=BLUE, fontweight="bold")
ax.annotate(f"a gap of {SUGAR_GAP:.2f}¢\n({SUGAR_RATIO:.2f}× the world price)",
            (len(xs) - 1.5, 24.5), fontsize=11, color=INK, fontweight="bold", ha="center")
ax.set_xticks(xs)
ax.set_xticklabels(SUGAR_MONTHS, fontsize=10.5)
ax.set_ylim(0, 44)
ax.set_ylabel("Cents per pound")
ax.legend(frameon=False, fontsize=10, loc="upper left")
ax.set_title("Americans do not pay the world price for sugar, and have not for decades",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08_fig_sugar_prices.png")


# ============================================ 15. the average tariff rate (real)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
xs = np.arange(len(TAR_YEARS))
cols = [GREY, RED, RED]
ax.bar(xs, TAR_RATES, width=0.5, color=cols)
for x, v in zip(xs, TAR_RATES):
    ax.annotate(f"{v}%", (x, v), xytext=(0, 6), textcoords="offset points", ha="center",
                fontsize=12, color=INK, fontweight="bold")
ax.set_xticks(xs)
ax.set_xticklabels(TAR_YEARS, fontsize=11.5)
ax.set_ylim(0, 15.2)
ax.set_ylabel("Duties collected as a % of import value")
ax.axhline(STATUTORY_2026, color=DGOLD, lw=1.8, ls="--")
ax.text(0.012, 0.985, f"{STATUTORY_2026}% — what the tariff schedule SAYS.  A different "
        "measurement:\nexemptions and carve-outs mean not all of it is actually paid.",
        transform=ax.transAxes, fontsize=9.5, color=DGOLD, fontweight="bold",
        ha="left", va="top")
ax.set_title("What Americans actually paid at the border: roughly a tripling in two years",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08_fig_tariff_rate.png")


# ======================================= 16. who actually pays (real, two panels)
fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))

ax = axes[0]
ax.barh([0], [PASSTHROUGH], height=0.42, color=RED, label="paid by US buyers")
ax.barh([0], [100 - PASSTHROUGH], left=[PASSTHROUGH], height=0.42, color=LGREY,
        label="absorbed by foreign sellers")
ax.annotate(f"{PASSTHROUGH:.0f}%", (PASSTHROUGH / 2, 0), ha="center", va="center",
            fontsize=17, color="white", fontweight="bold")
ax.annotate(f"{100 - PASSTHROUGH:.0f}%", (PASSTHROUGH + 5, 0), ha="center", va="center",
            fontsize=12, color=INK, fontweight="bold")
ax.set_xlim(0, 100)
ax.set_ylim(-1.6, 0.55)
ax.set_yticks([])
ax.set_xlabel("Share of the tariff showing up in the US price")
ax.spines["left"].set_visible(False)
ax.legend(frameon=False, fontsize=10, loc="lower center", ncol=1,
          bbox_to_anchor=(0.5, 0.02))
ax.set_title("Who the tariff lands on", fontsize=11.5, color=INK, fontweight="bold",
             pad=8)

ax = axes[1]
ys = np.arange(len(HH_LABELS))
ax.barh(ys, HH_COST, height=0.42, color=[GREY, RED])
for y, v in zip(ys, HH_COST):
    ax.annotate(f"\\${v:,}", (v, y), xytext=(8, 0), textcoords="offset points",
                va="center", fontsize=13, color=INK, fontweight="bold")
ax.set_yticks(ys)
ax.set_yticklabels(HH_LABELS, fontsize=11)
ax.invert_yaxis()
ax.set_xlim(0, 1500)
ax.set_ylim(1.95, -0.55)
ax.set_xlabel("Estimated cost per US household per year, 2026")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.text(0.5, 0.06, "Two careful estimates, published the same week and 22% apart.\n"
        "Quote the range, not a point.", transform=ax.transAxes, fontsize=10,
        color=GREY, fontweight="bold", ha="center", va="bottom")
ax.set_title("What it adds up to", fontsize=11.5, color=INK, fontweight="bold", pad=8)

fig.subplots_adjust(wspace=0.42)
fig.suptitle("A tariff is paid at the US border, by whoever is standing there",
             fontsize=11, color=INK, fontweight="bold", y=1.03)
save(fig, "ch08_fig_who_pays.png")


print("\nDerived figures used on slides:")
print(f"  Maya   {MAYA_MAX_B} B or {MAYA_MAX_S} S    OC of a burrito {MAYA_OC:g} smoothies")
print(f"  Owen   {OWEN_MAX_B} B or {OWEN_MAX_S} S    OC of a burrito {OWEN_OC:g} smoothies")
print(f"  autarky total        {AUT_B} B, {AUT_S} S")
print(f"  specialised total    {SPEC_B} B, {SPEC_S} S   (+{SPEC_B-AUT_B}, +{SPEC_S-AUT_S})")
print(f"  Maya after trade     {MAYA_T}   gains +{MAYA_GAIN[0]} B, +{MAYA_GAIN[1]} S")
print(f"  Owen after trade     {OWEN_T}   gains +{OWEN_GAIN[0]} B, +{OWEN_GAIN[1]} S")
print(f"  autarky market       {P_AUT:.0f}c x {Q_AUT:.0f}m lb")
print(f"  imports at 40c       {IMPORTS:.0f}m lb   net gain {IMP_NET:+,.0f}")
print(f"  exports at 80c       {EXPORTS:.0f}m lb   net gain {EXP_NET:+,.0f}")
print(f"  tariff of 10c        CS {TAR_CS:+,.0f}  PS {TAR_PS:+,.0f}  rev {TAR_REV:+,.0f}"
      f"  DWL {TAR_DWL:,.0f} (A {AREA_A:.0f} + B {AREA_B:.0f})")
print(f"  sugar gap Jun 2026   {SUGAR_GAP:.2f}c/lb, {SUGAR_RATIO:.2f}x")
