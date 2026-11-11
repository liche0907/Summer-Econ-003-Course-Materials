#!/usr/bin/env python3
"""ECON 003 - Chapter 8 (Trade) figures, v3: THE PUBLISHER'S OWN NUMBERS.

Their photographs, our charts.  matplotlib, UCR palette, Liberation Sans (Arial metrics).
Blue = demand, red = supply, everywhere, permanently.

v1 and v2 were built before the Acemoglu Ch08 deck was available and used an invented
worked example.  This file throws that away.  Every primitive below is read out of
`Slides/Pearson/Acemoglu_Micro_3e_Ch08 (1).pptx` - from its tables, its slide text and
its accessibility long-descriptions - so the figures reproduce the book's exhibits by
number, and a student revising from the book sees the same numbers.

  EXHIBIT 8.1  Your Production Schedule - an 8-hour day
                 YOU     1 website/hour  or  2 programs/hour  ->   8 websites or 16 programs
                 OLIVIA  2 websites/hour or  1 program/hour   ->  16 websites or  8 programs
               opportunity cost, from Exhibit 8.3:
                 you     1 website = 2 programs      1 program = 1/2 website
                 Olivia  1 website = 1/2 program     1 program = 2 websites

  EXHIBIT 8.2  The Production Possibilities Curve - your PPC, with the book's four
               lettered points:  B(6,4) and D(4,8) ON,  A(4,4) INSIDE,  C(8,8) OUTSIDE,
               and the D->B move: give up 4 programs, get 2 websites.

  EXHIBIT 8.3  Two Production Possibilities Curves - yours and Olivia's.

  EXHIBIT 8.4  The Gains from Specialization - the joint PPC.  Point T = (16 websites,
               16 programs), intercepts 24 programs and 24 websites.  Left of T the slope
               is Olivia's, right of T it is yours.

  EXHIBIT 8.5  An Illustration of Absolute Advantage - you take a web-design course and
               can now make 24 websites or 16 programs, so you can out-produce Olivia at
               BOTH.  New opportunity costs:
                 you     1 website = 2/3 program (0.67)   1 program = 3/2 websites (1.50)
                 Olivia  1 website = 1/2 program (0.50)   1 program = 2   websites (2.00)
               Olivia still has the comparative advantage in websites, you in programs.
               Terms of trade for a program therefore lie between 3/2 and 2 websites.

  EXHIBIT 8.6  Ratio of interstate to international exports, all 50 states + DC.  Values
               transcribed from the deck's own long-description (it states they are
               approximate, and the slide says so).

  EXHIBIT 8.7  A PPC with Increasing Opportunity Cost - apples against oranges, curve
               through 6.6 oranges and 7 apples, with A(1,4) inside, B on, C(8,3) outside.

  EXHIBIT 8.8  How Improved Technology Shifts the PPC - PPC A (6.6, 7) -> PPC B (7.6, 10).

  EXHIBITS 8.12-8.15   The Danish market for tennis shoes.  From the long-descriptions:
               supply runs from $10 at Q=0, demand from $90 at Q=0, crossing at
               (2 million pairs, $50).  That is exactly
                    S:  P = 10 + 20Q       D:  P = 90 - 20Q
               and every one of the book's stated quantities falls out of it:
                 world price $75  ->  Qd 0.75m, Qs 3.25m, EXPORTS 2.5m      (Exhibit 8.13)
                 world price $25  ->  Qs 0.75m, Qd 3.25m, IMPORTS 2.5m      (Exhibit 8.14)
                 $15 tariff on $25 -> P $40, Qs 1.5m, Qd 2.5m, imports 1.0m (Exhibit 8.15)
                 tariff revenue (their area I) = $15 x 1.0m = $15 million, which is the
                 figure printed on their slide 97.  Deadweight loss = their G + J.
               All asserted below.

  EBE PROBLEM  New England textiles.  Their stated points - equilibrium ($15, 15m), world
               price $5 giving Qs 5m and Qd 25m, a $5 tariff giving Qs 10m and Qd 20m -
               are reproduced exactly by  S: Qs = P,  D: Qd = 30 - P.

ONE PUBLISHER ERROR, FLAGGED ON THE SLIDE FACE.  Their slide 76 heads Exhibit 8.14 with
"When world price is above domestic price: Import".  It is BELOW - their own notes on the
same slide say the world price is $25 against a domestic $50, and their slide 69 states
the export case correctly.  The deck teaches the correct version and flags it without
naming them, per the ground rules.

Run:  python3 ch08_charts_v3.py [outdir]
"""
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

BLUE = "#003DA5"      # demand, and YOU
RED = "#CC3333"       # supply
GREEN = "#2E7D32"     # gains
DGOLD = "#B88300"     # Olivia, secondary curves
GOLD = "#FFB81D"
INK = "#333333"
GREY = "#666666"
LGREY = "#BBBBBB"
TINT_GREEN = "#E4F0E4"
TINT_RED = "#F7DEDE"
TINT_BLUE = "#DCE6F5"
TINT_GOLD = "#FBEFCF"

plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 11,
    "axes.edgecolor": "#888888", "axes.linewidth": 0.9,
    "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": GREY, "ytick.color": GREY,
    "xtick.labelsize": 10, "ytick.labelsize": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 200, "savefig.dpi": 200,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.06,
})

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)
    print("  ", name)


def dot(ax, x, y, color, label=None, dx=7, dy=7, size=52, ha="left", va="bottom", fs=10.5):
    ax.scatter([x], [y], s=size, color=color, zorder=6, edgecolor="white", linewidth=1.1)
    if label:
        ax.annotate(label, (x, y), xytext=(dx, dy), textcoords="offset points",
                    fontsize=fs, color=color, fontweight="bold", ha=ha, va=va)


# ===================================================== PRIMITIVES: YOU AND OLIVIA
HOURS = 8
YOU_W, YOU_P = 8, 16            # websites, programs, whole day (before the course)
OLI_W, OLI_P = 16, 8
YOU_W2 = 24                     # after the web-design course

YOU_OC_W = YOU_P / YOU_W        # 2 programs per website
YOU_OC_P = YOU_W / YOU_P        # 0.5 websites per program
OLI_OC_W = OLI_P / OLI_W        # 0.5
OLI_OC_P = OLI_W / OLI_P        # 2.0
YOU2_OC_W = YOU_P / YOU_W2      # 2/3
YOU2_OC_P = YOU_W2 / YOU_P      # 3/2

T = (OLI_W, YOU_P)              # point T: Olivia all websites, you all programs
JOINT_P = YOU_P + OLI_P         # 24 programs
JOINT_W = YOU_W + OLI_W         # 24 websites

assert (YOU_OC_W, YOU_OC_P) == (2.0, 0.5)
assert (OLI_OC_W, OLI_OC_P) == (0.5, 2.0)
assert abs(YOU2_OC_W - 2/3) < 1e-12 and YOU2_OC_P == 1.5
assert YOU2_OC_W < OLI_OC_W is False or OLI_OC_W < YOU2_OC_W, "Olivia keeps websites"
assert OLI_OC_W < YOU2_OC_W, "Olivia must still be the cheap website producer"
assert YOU2_OC_P < OLI_OC_P, "you must still be the cheap program producer"
assert T == (16, 16) and JOINT_P == 24 and JOINT_W == 24
# left of T the joint slope is Olivia's, right of T it is yours
assert JOINT_P - OLI_W * OLI_OC_W == YOU_P
assert YOU_P - YOU_W * YOU_OC_W == 0
TOT_LO, TOT_HI = YOU2_OC_P, OLI_OC_P          # 1.5 to 2 websites per program
assert (TOT_LO, TOT_HI) == (1.5, 2.0)


# ============================================================ Exhibit 8.2
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ax.set_xlim(0, 10.4)
ax.set_ylim(0, 20)
ax.set_xlabel("Number of websites produced")
ax.set_ylabel("Number of computer programs produced")
ax.fill_between([0, YOU_W], [YOU_P, 0], color=TINT_BLUE, alpha=0.55, zorder=1)
ax.plot([0, YOU_W], [YOU_P, 0], color=BLUE, lw=2.6, zorder=4)

ax.plot([4, 6], [8, 8], color=RED, lw=2.0, zorder=5)
ax.plot([6, 6], [8, 4], color=RED, lw=2.0, zorder=5)
ax.annotate("get 2 websites", (5, 8.5), fontsize=10, color=RED, fontweight="bold",
            ha="center")
ax.annotate("give up\n4 programs", (6.25, 6.2), fontsize=10, color=RED,
            fontweight="bold", ha="left", va="center")

ax.set_yticks(range(0, 21, 4))
dot(ax, 4, 8, BLUE, "D", dx=-16, dy=3, fs=13)
dot(ax, 6, 4, BLUE, "B", dx=-6, dy=-18, ha="right", va="top", fs=13)
dot(ax, 4, 4, GREY, "A  inside — possible,\nbut wasteful", dx=-10, dy=-8, ha="right",
    va="top", fs=10)
dot(ax, 8, 8, RED, "C  outside —\nnot possible", dx=-6, dy=8, ha="right", fs=10)
ax.annotate("Your production\npossibilities curve", (1.3, 11.4), fontsize=10.5,
            color=BLUE, fontweight="bold", ha="left")
ax.set_title("Exhibit 8.2 — one website costs you two programs, everywhere on the line",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08v3_fig_ex82_ppc.png")


# ============================================================ Exhibit 8.3
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ax.set_xlim(0, 19)
ax.set_ylim(0, 19)
ax.set_xlabel("Number of websites produced")
ax.set_ylabel("Number of computer programs produced")
ax.plot([0, YOU_W], [YOU_P, 0], color=BLUE, lw=2.6, zorder=4, label="Your PPC")
ax.plot([0, OLI_W], [OLI_P, 0], color=DGOLD, lw=2.6, zorder=4, label="Olivia's PPC")
for x, y, c in [(0, YOU_P, BLUE), (YOU_W, 0, BLUE), (0, OLI_P, DGOLD), (OLI_W, 0, DGOLD)]:
    ax.scatter([x], [y], s=42, color=c, zorder=5)
ax.annotate("16 programs", (0.3, YOU_P + 0.5), fontsize=10, color=BLUE, fontweight="bold")
ax.annotate("8 websites", (YOU_W + 0.3, 0.5), fontsize=10, color=BLUE, fontweight="bold")
ax.annotate("8 programs", (0.3, OLI_P + 0.5), fontsize=10, color=DGOLD, fontweight="bold")
ax.annotate("16 websites", (OLI_W - 0.3, 0.5), fontsize=10, color=DGOLD,
            fontweight="bold", ha="right")
ax.annotate("YOU\n1 website costs 2 programs", (9.4, 12.6), fontsize=10.5, color=BLUE,
            fontweight="bold", ha="left")
ax.annotate("OLIVIA\n1 website costs ½ a program", (9.4, 8.4), fontsize=10.5,
            color=DGOLD, fontweight="bold", ha="left")
ax.set_title("Exhibit 8.3 — same axes, different slopes. The slopes are the whole story.",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08v3_fig_ex83_two.png")


# ============================================================ Exhibit 8.4
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ax.set_xlim(0, 27)
ax.set_ylim(0, 27)
ax.set_xlabel("Number of websites produced")
ax.set_ylabel("Number of computer programs produced")
ax.fill_between([0, T[0], JOINT_W], [JOINT_P, T[1], 0], color=TINT_BLUE, alpha=0.5,
                zorder=1)
ax.plot([0, T[0], JOINT_W], [JOINT_P, T[1], 0], color=GREEN, lw=2.8, zorder=4)
ax.plot([0, YOU_W], [YOU_P, 0], color=BLUE, lw=1.8, ls="--", zorder=3)
ax.plot([0, OLI_W], [OLI_P, 0], color=DGOLD, lw=1.8, ls="--", zorder=3)
dot(ax, T[0], T[1], GREEN, "T  (16, 16)\nyou: 16 programs\nOlivia: 16 websites",
    dx=10, dy=6, fs=10.5)
ax.annotate("same slope as\nOlivia's PPC", (6.0, 21.6), fontsize=9.5, color=DGOLD,
            fontweight="bold", ha="left")
ax.annotate("same slope as\nyour PPC", (20.4, 8.6), fontsize=9.5, color=BLUE,
            fontweight="bold", ha="center")
ax.annotate("Your PPC", (1.0, 12.6), fontsize=9.5, color=BLUE, fontweight="bold",
            bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.4))
ax.annotate("Olivia's PPC", (11.4, 1.4), fontsize=9.5, color=DGOLD, fontweight="bold",
            bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.4))
ax.set_title("Exhibit 8.4 — T is outside BOTH curves, and only trade gets you there",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08v3_fig_ex84_gains.png")


# ============================================================ Exhibit 8.5
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ax.set_xlim(0, 27)
ax.set_ylim(0, 19)
ax.set_xlabel("Number of websites produced")
ax.set_ylabel("Number of computer programs produced")
ax.plot([0, YOU_W2], [YOU_P, 0], color=BLUE, lw=2.8, zorder=4)
ax.plot([0, OLI_W], [OLI_P, 0], color=DGOLD, lw=2.6, zorder=4)
ax.plot([0, YOU_W], [YOU_P, 0], color=LGREY, lw=1.6, ls=":", zorder=2)
ax.annotate("your OLD curve", (3.4, 9.6), fontsize=9, color=GREY, fontweight="bold",
            rotation=-52, ha="center")
ax.annotate("YOUR NEW PPC\n24 websites or 16 programs", (12.6, 12.4), fontsize=10.5,
            color=BLUE, fontweight="bold", ha="left")
ax.annotate("OLIVIA — unchanged\n16 websites or 8 programs", (9.2, 4.2), fontsize=10.5,
            color=DGOLD, fontweight="bold", ha="left")
for x, y, c in [(0, YOU_P, BLUE), (YOU_W2, 0, BLUE), (0, OLI_P, DGOLD), (OLI_W, 0, DGOLD)]:
    ax.scatter([x], [y], s=42, color=c, zorder=5)
ax.set_title("Exhibit 8.5 — now you beat Olivia at BOTH. She should still make the "
             "websites.", fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08v3_fig_ex85_absolute.png")


# ============================================================ Exhibit 8.6
STATES = [("AL",10),("AK",3.2),("AZ",7.2),("AR",14),("CA",8.5),("CO",18.5),("CT",16),
          ("DE",7.5),("FL",5.8),("GA",10),("HI",29.8),("ID",6),("IL",11.2),("IN",10.4),
          ("IA",12.2),("KS",17.9),("KY",11.2),("LA",4.6),("ME",11.8),("MD",12.8),
          ("MA",8.2),("MI",6.4),("MN",12),("MS",11.2),("MO",16.2),("MT",18.6),
          ("NE",13.9),("NV",6),("NH",11.4),("NJ",11.4),("NM",15.4),("NY",6),("NC",12.2),
          ("ND",9.9),("OH",11.4),("OK",24.6),("OR",7),("PA",13.2),("RI",18),("SC",5.4),
          ("SD",36.8),("TN",9.8),("TX",6.2),("UT",4.6),("VT",4.6),("VA",12.2),("WA",3),
          ("WV",4),("WI",12.5),("WY",16.6),("DC",0.25)]
fig, ax = plt.subplots(figsize=(11.0, 3.9))
xs = np.arange(len(STATES))
vals = [v for _, v in STATES]
cols = [RED if v < 1 else (BLUE if n in ("CA",) else DGOLD) for n, v in STATES]
ax.bar(xs, vals, color=cols, width=0.72)
ax.axhline(1, color=INK, lw=1.2, ls="--")
ax.annotate("ratio = 1: equal value sent to other states and to other countries",
            (12, 1.9), fontsize=9.5, color=INK, fontweight="bold", ha="left",
            bbox=dict(fc="white", ec="none", alpha=0.92, pad=1.6))
ax.set_xticks(xs)
ax.set_xticklabels([n for n, _ in STATES], fontsize=6.2, rotation=90)
ax.set_ylabel("Interstate exports ÷ international exports")
ax.set_xlim(-1, len(STATES))
ax.set_ylim(0, 40)
ax.annotate("California 8.5×", (4, 12.0), fontsize=9.5, color=BLUE, fontweight="bold",
            ha="center", bbox=dict(fc="white", ec="none", alpha=0.92, pad=1.4))
ax.annotate("only DC (0.25×) sends more\nabroad than to other states", (49.5, 22),
            fontsize=9.5, color=RED, fontweight="bold", ha="right",
            bbox=dict(fc="white", ec="none", alpha=0.92, pad=1.6))
ax.annotate("", xy=(50, 1.6), xytext=(48, 20.4),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
ax.set_title("Exhibit 8.6 — every state but one trades far more with other states than "
             "with the world", fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08v3_fig_ex86_states.png")


# ============================================================ Exhibit 8.7
def bowed(a, b, n=300):
    t = np.linspace(0, np.pi / 2, n)
    return a * np.sin(t), b * np.cos(t)

fig, ax = plt.subplots(figsize=(8.6, 3.6))
ox, oy = bowed(6.6, 7.0)
ax.fill_between(ox, oy, color=TINT_BLUE, alpha=0.55, zorder=1)
ax.plot(ox, oy, color=BLUE, lw=2.8, zorder=4)
ax.set_xlim(0, 10)
ax.set_ylim(0, 8.6)
ax.set_xlabel("Production of oranges")
ax.set_ylabel("Production of apples")
by = 7.0 * np.sqrt(max(0.0, 1 - (3.0 / 6.6) ** 2))
dot(ax, 3.0, by, BLUE, "B — possible\nand efficient", dx=9, dy=6, fs=10)
dot(ax, 1.0, 4.0, GREY, "A — possible\nbut inefficient", dx=9, dy=-6, va="top", fs=10)
dot(ax, 8.0, 3.0, RED, "C — impossible\n(in the short run)", dx=-9, dy=6, ha="right",
    fs=10)
ax.annotate("the first oranges\ncost few apples", (0.35, 1.1), fontsize=9.5, color=GREEN,
            fontweight="bold", ha="left")
ax.annotate("the last oranges\ncost many", (6.9, 5.2), fontsize=9.5, color=RED,
            fontweight="bold", ha="left")
ax.set_title("Exhibit 8.7 — a whole economy's curve bows out, because cost RISES",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08v3_fig_ex87_increasing.png")


# ============================================================ Exhibit 8.8
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ax1x, ax1y = bowed(6.6, 7.0)
ax2x, ax2y = bowed(7.6, 10.0)
ax.fill_between(ax2x, ax2y, color=TINT_GOLD, alpha=0.55, zorder=1)
ax.fill_between(ax1x, ax1y, color=TINT_BLUE, alpha=0.75, zorder=2)
ax.plot(ax1x, ax1y, color=BLUE, lw=2.6, zorder=4)
ax.plot(ax2x, ax2y, color=DGOLD, lw=2.6, zorder=4)
for t in (0.35, 0.75, 1.15):
    x1, y1 = 6.6 * np.sin(t), 7.0 * np.cos(t)
    x2, y2 = 7.6 * np.sin(t), 10.0 * np.cos(t)
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 11.6)
ax.set_xlabel("Production of oranges")
ax.set_ylabel("Production of apples")
ax.annotate("PPC A", (2.0, 3.6), fontsize=11, color=BLUE, fontweight="bold")
ax.annotate("PPC B", (6.4, 7.2), fontsize=11, color=DGOLD, fontweight="bold")
ax.set_title("Exhibit 8.8 — more resources, better resources or better technology moves "
             "the whole curve", fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08v3_fig_ex88_shift.png")


# ============================== PRIMITIVES: DENMARK, TENNIS SHOES (Exhibits 8.12-8.15)
def d_qd(p):
    return (90.0 - p) / 20.0


def d_qs(p):
    return (p - 10.0) / 20.0


P_DOM = 50.0
Q_DOM = d_qd(P_DOM)
P_EXP = 75.0
P_IMP = 25.0
TARIFF = 15.0
P_TAR = P_IMP + TARIFF

EXP_QD, EXP_QS = d_qd(P_EXP), d_qs(P_EXP)          # 0.75, 3.25
EXPORTS = EXP_QS - EXP_QD                          # 2.5
IMP_QS, IMP_QD = d_qs(P_IMP), d_qd(P_IMP)          # 0.75, 3.25
IMPORTS = IMP_QD - IMP_QS                          # 2.5
TAR_QS, TAR_QD = d_qs(P_TAR), d_qd(P_TAR)          # 1.5, 2.5
TAR_IMPORTS = TAR_QD - TAR_QS                      # 1.0


def d_cs(p):
    return (90.0 - p) ** 2 / 40.0


def d_ps(p):
    return (p - 10.0) ** 2 / 40.0


AREA_C_EXPORT = 0.5 * EXPORTS * (P_EXP - P_DOM)    # 31.25, the export gain
AREA_D_IMPORT = 0.5 * IMPORTS * (P_DOM - P_IMP)    # 31.25, the import gain
TAR_REVENUE = TARIFF * TAR_IMPORTS                 # 15.0  (their area I)
DWL_G = 0.5 * (TAR_QS - IMP_QS) * TARIFF           # 5.625
DWL_J = 0.5 * (IMP_QD - TAR_QD) * TARIFF           # 5.625
DWL = DWL_G + DWL_J                                # 11.25

assert (Q_DOM, P_DOM) == (2.0, 50.0)
assert (EXP_QD, EXP_QS, EXPORTS) == (0.75, 3.25, 2.5)
assert (IMP_QS, IMP_QD, IMPORTS) == (0.75, 3.25, 2.5)
assert (TAR_QS, TAR_QD, TAR_IMPORTS) == (1.5, 2.5, 1.0)
assert TAR_REVENUE == 15.0, "their slide prints $15 million of tariff revenue"
assert abs((d_ps(P_EXP) - d_ps(P_DOM)) - (d_cs(P_DOM) - d_cs(P_EXP)) - AREA_C_EXPORT) < 1e-9
assert abs((d_cs(P_IMP) - d_cs(P_DOM)) - (d_ps(P_DOM) - d_ps(P_IMP)) - AREA_D_IMPORT) < 1e-9
assert abs((d_cs(P_IMP) - d_cs(P_TAR)) - (d_ps(P_TAR) - d_ps(P_IMP)) - TAR_REVENUE - DWL) < 1e-9
assert DWL == 11.25


def shoe_frame(ax):
    q = np.linspace(0, 4.4, 200)
    ax.plot(q, 90 - 20 * q, color=BLUE, lw=2.6, zorder=4)
    ax.plot(q, 10 + 20 * q, color=RED, lw=2.6, zorder=4)
    ax.set_xlim(0, 4.4)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Quantity (millions of pairs)")
    ax.set_ylabel("Price per pair")
    ax.annotate(r"$D_{shoes}$", (4.0, 90 - 20 * 4.0 + 3), fontsize=11.5, color=BLUE,
                fontweight="bold")
    ax.annotate(r"$S_{shoes}$", (3.85, 10 + 20 * 3.85 + 3), fontsize=11.5, color=RED,
                fontweight="bold", ha="right")


# ============================================================ Exhibit 8.12
fig, ax = plt.subplots(figsize=(8.6, 3.6))
shoe_frame(ax)
ax.add_patch(Polygon([(0, P_DOM), (0, 90), (Q_DOM, P_DOM)], fc=TINT_BLUE, ec="none",
                     zorder=2))
ax.add_patch(Polygon([(0, P_DOM), (0, 10), (Q_DOM, P_DOM)], fc=TINT_RED, ec="none",
                     zorder=2))
ax.plot([0, Q_DOM], [P_DOM, P_DOM], color=INK, lw=1.0, ls=":", zorder=3)
ax.plot([Q_DOM, Q_DOM], [0, P_DOM], color=INK, lw=1.0, ls=":", zorder=3)
dot(ax, Q_DOM, P_DOM, INK, "", size=48)
ax.annotate("consumer\nsurplus", (0.55, 66), fontsize=10.5, color=BLUE, fontweight="bold")
ax.annotate("producer\nsurplus", (0.55, 28), fontsize=10.5, color=RED, fontweight="bold")
ax.annotate(r"\$50, 2 million pairs", (Q_DOM + 0.1, P_DOM + 2), fontsize=10.5, color=INK,
            fontweight="bold")
ax.set_title("Exhibit 8.12 — Denmark's tennis-shoe market with the border closed",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08v3_fig_ex812_denmark.png")


# ============================================================ Exhibit 8.13
fig, ax = plt.subplots(figsize=(8.6, 3.6))
shoe_frame(ax)
ax.add_patch(Polygon([(0, P_EXP), (0, 90), (EXP_QD, P_EXP)], fc=TINT_BLUE, ec=BLUE,
                     lw=0.7, zorder=2))
ax.add_patch(Polygon([(0, P_DOM), (0, P_EXP), (EXP_QD, P_EXP), (Q_DOM, P_DOM)],
                     fc=TINT_GOLD, ec=DGOLD, lw=0.7, zorder=2))
ax.add_patch(Polygon([(Q_DOM, P_DOM), (EXP_QD, P_EXP), (EXP_QS, P_EXP)], fc=TINT_GREEN,
                     ec=GREEN, lw=0.9, zorder=2))
ax.add_patch(Polygon([(0, 10), (0, P_DOM), (Q_DOM, P_DOM)], fc=TINT_RED, ec="none",
                     zorder=2))
ax.axhline(P_EXP, color=GREEN, lw=2.0, ls="--", zorder=3)
ax.plot([EXP_QD, EXP_QS], [P_EXP, P_EXP], color=GREEN, lw=5.0, alpha=0.35, zorder=3,
        solid_capstyle="butt")
for lab, x, y, c in [("D", 0.28, 82, BLUE), ("B", 0.30, 60, DGOLD),
                     ("C", 2.30, 70, GREEN), ("A", 0.30, 30, RED)]:
    ax.annotate(lab, (x, y), fontsize=13, color=c, fontweight="bold")
ax.annotate(r"$P_{world}$ = \$75", (4.3, P_EXP + 3), fontsize=10.5, color=GREEN,
            fontweight="bold", ha="right")
ax.annotate("exports = 2.5 million pairs", ((EXP_QD + EXP_QS) / 2, P_EXP + 4),
            fontsize=10.5, color=GREEN, fontweight="bold", ha="center",
            bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.6))
ax.set_title("Exhibit 8.13 — world price ABOVE the domestic price, so Denmark exports",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08v3_fig_ex813_export.png")


# ============================================================ Exhibit 8.14
fig, ax = plt.subplots(figsize=(8.6, 3.6))
shoe_frame(ax)
ax.add_patch(Polygon([(0, P_DOM), (0, 90), (Q_DOM, P_DOM)], fc=TINT_BLUE, ec=BLUE,
                     lw=0.7, zorder=2))
ax.add_patch(Polygon([(0, P_IMP), (0, P_DOM), (Q_DOM, P_DOM), (IMP_QS, P_IMP)],
                     fc=TINT_GOLD, ec=DGOLD, lw=0.7, zorder=2))
ax.add_patch(Polygon([(Q_DOM, P_DOM), (IMP_QS, P_IMP), (IMP_QD, P_IMP)], fc=TINT_GREEN,
                     ec=GREEN, lw=0.9, zorder=2))
ax.add_patch(Polygon([(0, 10), (0, P_IMP), (IMP_QS, P_IMP)], fc=TINT_RED, ec="none",
                     zorder=2))
ax.axhline(P_IMP, color=GREEN, lw=2.0, ls="--", zorder=3)
ax.plot([IMP_QS, IMP_QD], [P_IMP, P_IMP], color=GREEN, lw=5.0, alpha=0.35, zorder=3,
        solid_capstyle="butt")
for lab, x, y, c in [("B", 0.30, 62, BLUE), ("C", 0.30, 34, DGOLD),
                     ("D", 2.05, 34, GREEN), ("A", 0.28, 15, RED)]:
    ax.annotate(lab, (x, y), fontsize=13, color=c, fontweight="bold")
ax.annotate(r"$P_{world}$ = \$25", (4.3, P_IMP + 3), fontsize=10.5, color=GREEN,
            fontweight="bold", ha="right")
ax.annotate("imports = 2.5 million pairs", ((IMP_QS + IMP_QD) / 2, P_IMP - 10),
            fontsize=10.5, color=GREEN, fontweight="bold", ha="center",
            bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.6))
ax.set_title("Exhibit 8.14 — world price BELOW the domestic price, so Denmark imports",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08v3_fig_ex814_import.png")


# ============================================================ Exhibit 8.15
fig, ax = plt.subplots(figsize=(8.6, 3.6))
shoe_frame(ax)
ax.add_patch(Rectangle((TAR_QS, P_IMP), TAR_IMPORTS, TARIFF, fc=TINT_GOLD, ec=DGOLD,
                       lw=1.0, zorder=2))
ax.add_patch(Polygon([(IMP_QS, P_IMP), (TAR_QS, P_IMP), (TAR_QS, P_TAR)], fc=TINT_RED,
                     ec=RED, lw=1.0, zorder=2))
ax.add_patch(Polygon([(TAR_QD, P_TAR), (IMP_QD, P_IMP), (TAR_QD, P_IMP)], fc=TINT_RED,
                     ec=RED, lw=1.0, zorder=2))
ax.add_patch(Polygon([(0, P_IMP), (0, P_TAR), (TAR_QS, P_TAR), (IMP_QS, P_IMP)],
                     fc=TINT_GREEN, ec=GREEN, lw=0.8, zorder=2))
ax.axhline(P_IMP, color=GREY, lw=1.6, ls="--", zorder=3)
ax.axhline(P_TAR, color=RED, lw=2.0, ls="--", zorder=3)
ax.annotate("G", (TAR_QS - 0.20, P_IMP + 2.5), fontsize=12.5, color=RED,
            fontweight="bold", ha="right")
ax.annotate("J", (TAR_QD + 0.08, P_IMP + 2.5), fontsize=12.5, color=RED,
            fontweight="bold")
ax.annotate("E", (0.30, P_IMP + 4), fontsize=12.5, color=GREEN, fontweight="bold")
ax.annotate("I  =  \\$15m", ((TAR_QS + TAR_QD) / 2, P_IMP + TARIFF / 2), fontsize=10.5,
            color=DGOLD, fontweight="bold", ha="center", va="center")
ax.annotate(r"tariff = \$15", (4.3, P_TAR + 3), fontsize=10.5, color=RED,
            fontweight="bold", ha="right")
ax.annotate(r"$P_{world}$ = \$25", (0.10, P_IMP - 11), fontsize=10.5, color=GREY,
            fontweight="bold", ha="left",
            bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.4))
ax.annotate("imports 2.5m → 1.0m\nG + J = \\$11.25m, lost to nobody", (2.55, 8),
            fontsize=10.5, color=RED, fontweight="bold", ha="left", va="bottom",
            bbox=dict(fc="white", ec="none", alpha=0.9, pad=2.0))
ax.set_title("Exhibit 8.15 — a \\$15 tariff lifts the price to \\$40 and halves imports "
             "twice over", fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08v3_fig_ex815_tariff.png")


# =================================================== EBE problem: New England textiles
def t_qs(p):
    return p


def t_qd(p):
    return 30.0 - p


T_EQ_P, T_EQ_Q = 15.0, 15.0
T_WORLD, T_TARIFF = 5.0, 5.0
T_TAR_P = T_WORLD + T_TARIFF
assert (t_qs(T_EQ_P), t_qd(T_EQ_P)) == (15.0, 15.0)
assert (t_qs(T_WORLD), t_qd(T_WORLD)) == (5.0, 25.0)
assert (t_qs(T_TAR_P), t_qd(T_TAR_P)) == (10.0, 20.0)
WORKERS_PER_M = 10
JOBS_NOTRADE = WORKERS_PER_M * t_qs(T_EQ_P)        # 150
JOBS_FREE = WORKERS_PER_M * t_qs(T_WORLD)          # 50
assert JOBS_NOTRADE - JOBS_FREE == 100

fig, ax = plt.subplots(figsize=(8.6, 3.6))
q = np.linspace(0, 30, 200)
ax.plot(q, q, color=RED, lw=2.6, zorder=4)
ax.plot(q, 30 - q, color=BLUE, lw=2.6, zorder=4)
ax.axhline(T_WORLD, color=GREEN, lw=2.0, ls="--", zorder=3)
ax.axhline(T_TAR_P, color=RED, lw=1.8, ls="--", zorder=3)
ax.add_patch(Rectangle((10, T_WORLD), 10, T_TARIFF, fc=TINT_GOLD, ec=DGOLD, lw=1.0,
                       zorder=2))
ax.annotate("G", (14.6, 7.0), fontsize=13, color=DGOLD, fontweight="bold")
dot(ax, T_EQ_Q, T_EQ_P, INK, r"no trade:  \$15, 15m units", dx=8, dy=8, fs=10)
for x, y in [(5, 5), (25, 5), (10, 10), (20, 10)]:
    ax.scatter([x], [y], s=34, color=INK, zorder=6)
ax.annotate(r"world price \$5", (29.5, T_WORLD + 2), fontsize=10.5, color=GREEN,
            fontweight="bold", ha="right")
ax.annotate(r"with a \$5 tariff:  \$10", (29.5, T_TAR_P + 2), fontsize=10.5, color=RED,
            fontweight="bold", ha="right")
ax.annotate("domestic output\n15m → 5m units", (2.0, 20.0), fontsize=10.5, color=INK,
            fontweight="bold", ha="left")
ax.set_xlim(0, 30)
ax.set_ylim(0, 30)
ax.set_xlabel("Quantity (millions of units)")
ax.set_ylabel("Price")
ax.set_title("Practice — New England textiles, and what free trade does to employment",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch08v3_fig_textiles.png")


print("\nPublisher figures reproduced exactly:")
print(f"  you  {YOU_W} sites / {YOU_P} programs   OC: site {YOU_OC_W:g}, program {YOU_OC_P:g}")
print(f"  Olivia {OLI_W} sites / {OLI_P} programs OC: site {OLI_OC_W:g}, program {OLI_OC_P:g}")
print(f"  point T {T}, joint intercepts {JOINT_P} programs / {JOINT_W} websites")
print(f"  after the course: you {YOU_W2} sites / {YOU_P} programs, "
      f"OC site {YOU2_OC_W:.2f}, program {YOU2_OC_P:.2f}")
print(f"  terms of trade for a program: between {TOT_LO:g} and {TOT_HI:g} websites")
print(f"  Denmark closed  \\${P_DOM:.0f} x {Q_DOM:.0f}m pairs")
print(f"  export \\${P_EXP:.0f}  Qd {EXP_QD:.2f} Qs {EXP_QS:.2f} exports {EXPORTS:.1f}m, "
      f"net gain (area C) \\${AREA_C_EXPORT:.2f}m")
print(f"  import \\${P_IMP:.0f}  Qs {IMP_QS:.2f} Qd {IMP_QD:.2f} imports {IMPORTS:.1f}m, "
      f"net gain (area D) \\${AREA_D_IMPORT:.2f}m")
print(f"  tariff \\${TARIFF:.0f} -> P \\${P_TAR:.0f}, imports {TAR_IMPORTS:.1f}m, "
      f"revenue (area I) \\${TAR_REVENUE:.0f}m, DWL (G+J) \\${DWL:.2f}m")
print(f"  textiles: {JOBS_NOTRADE:.0f} jobs at no trade, {JOBS_FREE:.0f} at free trade "
      f"= {JOBS_NOTRADE - JOBS_FREE:.0f} fewer")


# ============================================== OPENER: where the US sits in trade
# A KPI ROW OF STAT TILES, not a chart — four headline numbers is the case the form
# guidance says must not become a grouped bar chart.  Values sit in INK; a coloured
# mark carries identity, so nothing is legible by colour alone.
#
# Four facets, chosen by the instructor: how much of what Americans buy is foreign,
# the trade balance against GDP, what has happened to the price of tradable goods,
# and what the US actually specialises in selling.  All verified:
#
#  1  ~90% of US personal consumption expenditure traces to US-made output; ~10% to
#     imports.  Hale, Hobijn, Nechio & Wilson, FRBSF Economic Letter 2019-01 (11%,
#     2017 data, goods AND services) and Hobijn & Nechio, FRBSF EL 2025-12 (9%, 2023
#     data, goods only).  THE TWO ARE NOT COMPARABLE - do not say the share "fell".
#     "Roughly a tenth" is safe on both vintages, which is why the tile says ~10%.
#  2  CY2025 goods-and-services deficit $931.96bn on GDP $30,762.1bn = 3.03%.
#     Goods deficit $1,259.62bn; services SURPLUS $327.66bn (offsets 26% of goods).
#     Census/BEA annual revision published 9 June 2026 - these are revised figures.
#  3  BLS CPI-U, US city average, NSA, Jan 2000 -> Jul 2026:
#     toys -72.6%, apparel +5.8%, all items +97.8%, tuition/childcare +188.1%.
#     Televisions deliberately excluded: the index falls ~97%, which invites a fight
#     about hedonic quality adjustment and there is no clean current series.
#  4  CY2025 exports $3,429.8bn = goods $2,191.9bn (63.9%) + services $1,237.9bn
#     (36.1%).  Travel $213.2bn, financial services $208.8bn, IP charges $191.4bn -
#     travel alone is a bigger export than automotive vehicles and parts ($160.3bn).
IMPORT_SHARE = 10                      # % of consumer spending traced to imports
DEFICIT_PCT = 3.0                      # goods+services deficit, % of GDP, CY2025
GOODS_DEF, SERV_SUR = 1259.62, 327.66  # $bn, CY2025 revised
CPI = [("Toys", -72.6, BLUE), ("Clothing", 5.8, BLUE),
       ("Average", 97.8, GREY), ("College", 188.1, RED)]
# Top US export sectors, 2025, $bn. Goods from UN Comtrade / ITC at HS-chapter level;
# services from BEA international transactions (FRED IEAXS* series). Gold (HS 71,
# ~$148bn) is excluded: it doubled in 2025 on bullion movements and is not something
# America makes. "Machinery incl. computers" is excluded as too bucket-y to teach from.
EXPORTS = [("Energy", 309, DGOLD), ("Business services", 284, GREEN),
           ("Financial services", 214, GREEN), ("Travel & education", 214, GREEN),
           ("Patents & software", 195, GREEN), ("Aircraft", 164, DGOLD)]

assert abs((GOODS_DEF - SERV_SUR) / 30762.1 * 100 - DEFICIT_PCT) < 0.05
assert EXPORTS[0][1] == max(v for _, v, _ in EXPORTS), "energy leads - keep it honest"

fig = plt.figure(figsize=(11.0, 3.9))
gs = fig.add_gridspec(1, 4, wspace=0.32, left=0.02, right=0.98, top=0.99, bottom=0.02)

TILES = [
    ("MADE ABROAD", f"~{IMPORT_SHARE}%", RED,
     "of every dollar Americans spend\ntraces back to an import"),
    ("THE TRADE DEFICIT", f"{DEFICIT_PCT}%", DGOLD,
     "of GDP in 2025 — and the US runs\na surplus in services"),
    ("PRICES SINCE 2000", "−73%", BLUE,
     "toys. What you can ship got cheaper;\nwhat you cannot got dearer"),
    ("WHAT AMERICA SELLS", "\\$195bn", GREEN,
     "a year just for the right to use\nAmerican patents, software, brands"),
]

for i, (label, value, colour, sub) in enumerate(TILES):
    ax = fig.add_subplot(gs[0, i])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(Rectangle((0, 0.955), 1, 0.045, fc=colour, ec="none"))
    ax.text(0, 0.90, label, fontsize=10, color=GREY, fontweight="bold", va="top")
    ax.text(0, 0.665, value, fontsize=40, color=INK, fontweight="bold", va="center")
    ax.text(0, 0.46, sub, fontsize=10.5, color=INK, va="top", linespacing=1.45)

    if i == 0:
        # ten squares, one filled: "one dollar in ten"
        for k in range(10):
            x = 0.015 + k * 0.093
            ax.add_patch(Rectangle((x, 0.145), 0.072, 0.105,
                                   fc=RED if k == 0 else "#FFFFFF",
                                   ec=RED if k == 0 else LGREY, lw=1.0))
        ax.text(0.015, 0.10, "one dollar in ten", fontsize=9, color=GREY, va="top")

    elif i == 1:
        # goods deficit against the services surplus. Names sit in a left column and
        # the bars in a right one - an outside label on the long bar will not fit in a
        # 2.75 in panel, and inside it would be red on red.
        zero, sc = 0.866, 0.55 / 1588.0
        ax.plot([zero, zero], [0.06, 0.30], color=INK, lw=0.9)
        for y, nm, v, c in [(0.215, "Goods  −\\$1.26tn", -GOODS_DEF, RED),
                            (0.115, "Services  +\\$0.33tn", SERV_SUR, GREEN)]:
            ax.add_patch(Rectangle((zero if v > 0 else zero + v * sc, y),
                                   abs(v) * sc, 0.055, fc=c, ec="none"))
            ax.text(0.015, y + 0.0275, nm, fontsize=8, color=c, fontweight="bold",
                    va="center")

    elif i == 2:
        # four CPI bars. Same left-column treatment, and the value rides in the label
        # so nothing has to fit in the gap beyond a bar end.
        zero, sc = 0.584, 0.55 / 261.0
        ax.plot([zero, zero], [0.03, 0.325], color=INK, lw=0.9)
        for k, (nm, v, c) in enumerate(CPI):
            y = 0.275 - k * 0.072
            ax.add_patch(Rectangle((zero if v > 0 else zero + v * sc, y),
                                   abs(v) * sc, 0.048, fc=c, ec="none"))
            ax.text(0.015, y + 0.024, f"{nm}  {v:+.0f}%", fontsize=7.5, color=c,
                    fontweight="bold", va="center")

    else:
        # six ranked export sectors, goods and services on one axis - that mixing IS
        # the point. Energy and aircraft are in deliberately: a "finance and software"
        # story alone would drop the biggest US export sector of all.
        sc = 0.42 / 309.0
        for k, (nm, v, c) in enumerate(EXPORTS):
            y = 0.285 - k * 0.050
            ax.add_patch(Rectangle((0.55, y), v * sc, 0.034, fc=c, ec="none"))
            ax.text(0.53, y + 0.017, nm, fontsize=7, color=c, fontweight="bold",
                    ha="right", va="center")
            ax.text(0.56 + v * sc, y + 0.017, f"{v:.0f}", fontsize=6.5, color=GREY,
                    va="center")

save(fig, "ch08v3_fig_opener.png")
