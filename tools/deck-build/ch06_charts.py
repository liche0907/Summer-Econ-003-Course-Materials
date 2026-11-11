#!/usr/bin/env python3
"""ECON 003 - Chapter 6 (Sellers and Incentives) figures.

Their photographs, our charts. matplotlib, UCR palette, Liberation Sans (Arial metrics).

ONE FIRM, TWO TABLES.  The running example is a McDonald's franchise, carried over from
the Mateer & Coppock deck the instructor used last time.  Both tables are that deck's:

  * production  - meals against number of workers (its slide 16)
  * costs       - TVC against meals, with TFC = $100 (its slide 26)

Everything else in this file - every average, every margin, every labelled crossing,
every profit and loss figure - is computed from those two tables.  Nothing is drawn to
look right.

The publisher's own firm, The Wisconsin Cheeseman, is not used on any slide; its key
figures live in the speaker notes so the instructor can bridge to the textbook.

Run:  python3 ch06_charts.py [outdir]
"""
import sys
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy.interpolate import PchipInterpolator

# ----------------------------------------------------------------- house style
BLUE = "#003DA5"      # demand / marginal revenue / price lines
RED = "#CC3333"       # supply / marginal cost
GREEN = "#2E7D32"     # average total cost, and the "profit" side of a contrast
DGOLD = "#B88300"     # average variable cost
INK = "#333333"
GREY = "#666666"
LGREY = "#BBBBBB"
TINT_GREEN = "#E4F0E4"
TINT_RED = "#F7DEDE"
TINT_BLUE = "#DCE6F5"

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
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)
    print("  ", name)


def money(x, _=None):
    return f"${x:,.2f}"


def dollars0(x, _=None):
    return f"${x:,.0f}"


# ======================================================= TABLE 1 - PRODUCTION
# Meals served per hour as the manager adds workers.  Restaurant size fixed.
WORKERS = np.arange(0, 11)
MEALS = np.array([0, 5, 15, 30, 42, 52, 60, 65, 67, 63, 55])
MP = np.diff(MEALS)                       # 5 10 15 12 10 8 5 2 -4 -8

# ============================================================ TABLE 2 - COSTS
QQTAB = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])   # meals per hour
TVC = np.array([0, 30, 50, 65, 77, 87, 100, 120, 160, 220, 300], dtype=float)
TFC = 100.0

TC = TVC + TFC
Qc = QQTAB[1:].astype(float)              # the cost curves are defined for Q > 0
AVC = TVC[1:] / Qc
AFC = TFC / Qc
ATC = TC[1:] / Qc
MC = np.diff(TVC) / np.diff(QQTAB)        # $ per meal, charged to the row it completes

# ---- the crossings the lecture actually names, all straight out of the table
Q_MCMIN, P_MCMIN = 50.0, MC[4]                    # $1.00
Q_AVCMIN, P_AVCMIN = 60.0, TVC[6] / 60            # $1.6667  - the shutdown price
Q_ATCMIN, P_ATCMIN = 70.0, TC[7] / 70             # $3.1429  - the long-run price
Q_STAR, P_STAR = 80.0, 4.00                       # MC(80) = 40/10 = $4.00
Q_LOSS, P_LOSS = 70.0, 2.00                       # MC(70) = 20/10 = $2.00
Q_HIGH, P_HIGH = 90.0, 6.00                       # MC(90) = 60/10 = $6.00

PROFIT_STAR = P_STAR * Q_STAR - TC[8]             # 320 - 260 = $60
PROFIT_HIGH = P_HIGH * Q_HIGH - TC[9]             # 540 - 320 = $220
LOSS_OPEN = TC[7] - P_LOSS * Q_LOSS               # 220 - 140 = $80
COVERS = P_LOSS * Q_LOSS - TVC[7]                 # 140 - 120 = $20 toward overhead
PS_STAR = P_STAR * Q_STAR - TVC[8]                # 320 - 160 = $160 producer surplus

assert abs(MC[7] - 4.00) < 1e-12 and abs(MC[6] - 2.00) < 1e-12
assert abs(PROFIT_STAR - 60) < 1e-9 and abs(LOSS_OPEN - 80) < 1e-9
assert abs(COVERS - 20) < 1e-9 and abs(PS_STAR - 160) < 1e-9
assert abs(PS_STAR - PROFIT_STAR - TFC) < 1e-9    # PS exceeds profit by exactly the FC

# Smooth interpolators, so a drawn curve passes exactly through every table point.
_mc = PchipInterpolator(Qc, MC)

# ---------------------------------------------------------------- MC, drawn honestly
# The table's MC column is a BLOCK average: the 71st-80th meals cost $4.00 each.  Plot
# that $4.00 at Q = 80 - the right edge of the block - and the whole MC curve sits about
# five meals too far right, so it cuts AVC at 67 (low point 60) and ATC at 76 (low point
# 70).  The textbook claim then fails on its own diagram.
#
# A difference quotient equals the derivative somewhere INSIDE the interval, so the
# block average belongs at the block's MIDPOINT.  Placed there, MC cuts AVC at 61.3 and
# ATC at 71.2 - within about one meal of each low point, which at chart scale is under
# a tenth of an inch.  The tangency reads as exact.
#
# The cost is that a price line then meets the smooth curve five meals left of the
# quantity the table says to serve.  So the tangency diagrams draw BOTH: the faint
# staircase, on which P = $4 -> 80 meals is exactly right, and the smooth curve through
# the block midpoints, which is what the staircase becomes as the blocks shrink.
# Decision diagrams keep _mc and are untouched.
MC_MID = (QQTAB[1:] + QQTAB[:-1]) / 2.0           # 5, 15, 25, ... 95
_mc_smooth = PchipInterpolator(MC_MID, MC, extrapolate=True)
STEP_X = np.r_[0.0, Qc]                           # 0, 10, 20, ... 100
STEP_Y = np.r_[MC[0], MC]                         # held over the interval ENDING at x


def _first_cross(f, g, lo, hi):
    x = np.linspace(lo, hi, 20000)
    d = f(x) - g(x)
    i = np.where(np.sign(d[:-1]) != np.sign(d[1:]))[0]
    return float(x[i[0]])


def draw_mc_blocks(ax, alpha=0.38, lw=1.3):
    """The table's MC as the step function it actually is, faint, behind the curve."""
    ax.step(STEP_X, STEP_Y, where="pre", color=RED, lw=lw, alpha=alpha, zorder=3)


def draw_mc_smooth(ax, lw=2.2, lo=8.0, hi=100.0, label=True):
    g = np.linspace(lo, hi, 500)
    ax.plot(g, _mc_smooth(g), color=RED, lw=lw, zorder=5)
    if label:
        ax.annotate("MC", (hi, float(_mc_smooth(hi))), textcoords="offset points",
                    xytext=(5, 0), color=RED, fontsize=11, fontweight="bold", zorder=12)
_atc = PchipInterpolator(Qc, ATC)
_avc = PchipInterpolator(Qc, AVC)
_afc = PchipInterpolator(Qc, AFC)
QQ = np.linspace(10, 100, 600)


# ------------------------------------------------------------------- THE AXIS RULE
# Number an axis only where a number on it is actually read.  On every firm and market
# diagram in this chapter a PRICE is designated - $4, $3.14, $1.67 - so the vertical
# axis carries dollars.  Nobody reads a quantity off these pictures, so the horizontal
# axis carries none, and the gridlines run horizontally only.
#
# And the unit is "Meals".  Not "meals per hour", which students hear as a rate and
# stumble over; and never "thousands of meals per hour" on a market axis - a unit that
# is precise, correct and meaningless to a first-year.  Same word on both panels; the
# panel title says whether it is the market or the restaurant.
#
# Workers stay numbered: "the 3rd worker adds 15 meals" is a number students DO read.
# So do the data charts - Dallas Fed, menu prices, the fee split.  Those are evidence.
Q_CROSS_AVC = _first_cross(_mc_smooth, _avc, 30, 99)      # ~61.3, against min AVC at 60
Q_CROSS_ATC = _first_cross(_mc_smooth, _atc, 30, 99)      # ~71.2, against min ATC at 70
assert abs(Q_CROSS_AVC - Q_AVCMIN) < 2.0, Q_CROSS_AVC
assert abs(Q_CROSS_ATC - Q_ATCMIN) < 2.0, Q_CROSS_ATC


def cost_axes(ax, ymax=8.6, xmax=108, ylabel="Price / cost per meal"):
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_xlabel("Meals")
    ax.set_xticks([])                       # see THE AXIS RULE above
    ax.set_ylabel(ylabel)
    ax.yaxis.set_major_formatter(FuncFormatter(dollars0))
    ax.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    ax.set_axisbelow(True)


BOX = dict(boxstyle="square,pad=0.12", fc="white", ec="none", alpha=0.92)


def qticks(ax, *extra):
    """Put the quantity numbers back.

    THE AXIS RULE has an exception, and it is the instructor's: a diagram where the
    student reads a specific quantity off the picture - "$4 buys 80 meals" - needs the
    number on the axis to read.  Diagrams that only make a shape argument do not.
    """
    ax.set_xticks(sorted({0, 20, 40, 60, 80, 100} | set(extra)))


def draw_costs(ax, mc=True, atc=True, avc=True, lw=2.2, label=True):
    if mc:
        ax.plot(QQ, _mc(QQ), color=RED, lw=lw, zorder=5)
        if label:
            ax.annotate("MC", (100, MC[-1]), textcoords="offset points",
                        xytext=(5, 0), color=RED, fontsize=11, fontweight="bold",
                        zorder=12)
    if atc:
        ax.plot(QQ, _atc(QQ), color=GREEN, lw=lw, zorder=4)
        if label:
            ax.annotate("ATC", (100, ATC[-1]), textcoords="offset points",
                        xytext=(5, -2), color=GREEN, fontsize=11, fontweight="bold",
                        zorder=12, bbox=BOX)
    if avc:
        ax.plot(QQ, _avc(QQ), color=DGOLD, lw=lw, zorder=3)
        if label:
            ax.annotate("AVC", (100, AVC[-1]), textcoords="offset points",
                        xytext=(5, -10), color=DGOLD, fontsize=11, fontweight="bold",
                        zorder=12, bbox=BOX)


# ==================================================================== production
def fig_production():
    fig, ax = plt.subplots(figsize=(6.0, 3.3))
    f = PchipInterpolator(WORKERS[:9], MEALS[:9])
    xs = np.linspace(0, 8, 300)
    ax.plot(xs, f(xs), color=BLUE, lw=2.6, zorder=4)
    ax.plot(WORKERS[8:], MEALS[8:], color=BLUE, lw=2.6, zorder=4)
    ax.scatter(WORKERS, MEALS, s=30, color=BLUE, zorder=6)
    ax.scatter(WORKERS[9:], MEALS[9:], s=44, color=RED, zorder=7)

    ax.annotate("67 meals with 8 workers\n— the peak", (8, 67), xytext=(5.6, 78),
                fontsize=9.5, color=INK, ha="center", va="top",
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
    ax.annotate("the 9th and 10th\ntake output DOWN", (9.6, 58), xytext=(7.2, 22),
                fontsize=9.5, color=RED, ha="center",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    ax.annotate("steepest here: the\n3rd worker adds 15", (3, 30), xytext=(1.9, 62),
                fontsize=9.5, color=GREEN, ha="center",
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 82)
    ax.set_xticks(range(0, 11))
    ax.set_xlabel("Number of workers")
    ax.set_ylabel("Meals")
    ax.grid(True, color="#EEEEEE", lw=0.7)
    ax.set_axisbelow(True)
    save(fig, "ch06_fig_production.png")


def fig_marginal_product():
    fig, ax = plt.subplots(figsize=(7.6, 2.75))
    n = WORKERS[1:]
    ax.bar(n[:3], MP[:3], color=GREEN, width=0.66, zorder=3)
    ax.bar(n[3:8], MP[3:8], color=BLUE, width=0.66, zorder=3)
    ax.bar(n[8:], MP[8:], color=RED, width=0.66, zorder=3)
    ax.axhline(0, color="#888888", lw=1.0)
    for xi, v in zip(n, MP):
        ax.annotate(f"{v:+d}", (xi, v), textcoords="offset points",
                    xytext=(0, 4 if v > 0 else -12), ha="center", fontsize=8.5,
                    color=INK)
    ax.annotate("rising:\nspecialisation", (1.6, 19.4), fontsize=9.5, color=GREEN,
                ha="center", va="top", fontweight="bold")
    ax.annotate("falling: diminishing returns", (6.4, 19.4), fontsize=9.5, color=BLUE,
                ha="center", va="top", fontweight="bold")
    ax.annotate("negative: they get\nin each other's way", (9.5, -8.5), fontsize=9,
                color=RED, ha="center", va="top", fontweight="bold")
    ax.set_xlim(0.3, 10.7)
    ax.set_ylim(-15, 20)
    ax.set_xticks(range(1, 11))
    ax.set_xlabel("Number of workers")
    ax.set_ylabel("Extra meals")
    ax.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    ax.set_axisbelow(True)
    save(fig, "ch06_fig_marginal_product.png")


# =============================================================== the cost curves
def fig_cost_curves():
    """The tangency diagram - so MC has to actually touch both low points here."""
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    cost_axes(ax)
    ax.plot(QQ, _atc(QQ), color=GREEN, lw=2.2, zorder=4)
    ax.annotate("ATC", (100, ATC[-1]), textcoords="offset points", xytext=(5, -2),
                color=GREEN, fontsize=11, fontweight="bold", zorder=12, bbox=BOX)
    ax.plot(QQ, _avc(QQ), color=DGOLD, lw=2.2, zorder=3)
    ax.annotate("AVC", (100, AVC[-1]), textcoords="offset points", xytext=(5, -10),
                color=DGOLD, fontsize=11, fontweight="bold", zorder=12, bbox=BOX)
    draw_mc_blocks(ax)
    draw_mc_smooth(ax)
    ax.scatter([Q_AVCMIN], [P_AVCMIN], s=48, color=DGOLD, zorder=9,
               edgecolor="white", lw=1.3)
    ax.scatter([Q_ATCMIN], [P_ATCMIN], s=48, color=GREEN, zorder=9,
               edgecolor="white", lw=1.3)
    ax.annotate(f"min AVC = \\${P_AVCMIN:.2f}\nat 60 meals", (Q_AVCMIN, P_AVCMIN),
                xytext=(30, 4.9), fontsize=9.5, color=DGOLD, fontweight="bold",
                ha="center", bbox=BOX, zorder=12,
                arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.0))
    ax.annotate(f"min ATC = \\${P_ATCMIN:.2f}\nat 70 meals", (Q_ATCMIN, P_ATCMIN),
                xytext=(63, 6.9), fontsize=9.5, color=GREEN, fontweight="bold",
                ha="center", bbox=BOX, zorder=12,
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))
    ax.annotate("MC passes through the low point\nof each average curve",
                (27, 0.55), fontsize=9.5, color=RED, ha="center", va="center",
                fontweight="bold", zorder=12)
    ax.annotate("faint steps = the table's 10-meal blocks", (106, 0.55), fontsize=7.5,
                color=GREY, ha="right", va="center", zorder=12)
    save(fig, "ch06_fig_cost_curves.png")


# =============================================================== market and firm
def fig_market_and_firm():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.1))
    q = np.linspace(0, 100, 200)
    a1.plot(q, 7.0 - 0.06 * q, color=BLUE, lw=2.4)
    a1.plot(q, 1.0 + 0.06 * q, color=RED, lw=2.4)
    a1.annotate("D", (95, 7.0 - 0.06 * 95), color=BLUE, fontsize=11,
                fontweight="bold", va="bottom")
    a1.annotate("S", (57, 1.0 + 0.06 * 57), color=RED, fontsize=11,
                fontweight="bold", va="bottom")
    a1.plot([0, 50], [4, 4], color=GREY, lw=0.9, ls=":")
    a1.plot([50, 50], [0, 4], color=GREY, lw=0.9, ls=":")
    a1.scatter([50], [4], s=44, color=INK, zorder=6)
    a1.set_xlim(0, 100)
    a1.set_ylim(0, 8.6)
    a1.set_yticks([0, 2, 4, 6, 8])
    a1.yaxis.set_major_formatter(FuncFormatter(dollars0))
    a1.set_xticks([])
    a1.set_xlabel("Meals, the whole market")
    a1.set_ylabel("Price per meal")
    a1.set_title("(a)  The market sets the price", fontsize=10.5, color=INK,
                 fontweight="bold", pad=8)
    a1.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    a1.set_axisbelow(True)

    a2.axhline(4, color=BLUE, lw=2.6)
    a2.annotate(r"D = MR = P = \$4", (104, 4), textcoords="offset points",
                xytext=(-4, 9), fontsize=10.5, color=BLUE, fontweight="bold",
                ha="right")
    a2.set_xlim(0, 108)
    a2.set_ylim(0, 8.6)
    a2.set_yticks([0, 2, 4, 6, 8])
    a2.yaxis.set_major_formatter(FuncFormatter(dollars0))
    a2.set_xticks([])
    a2.set_xlabel("Meals, this restaurant")
    a2.set_title("(b)  This restaurant takes it", fontsize=10.5, color=INK,
                 fontweight="bold", pad=8)
    a2.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    a2.set_axisbelow(True)
    a2.annotate("sell as many as you like at \\$4\nand none at all at \\$4.01",
                (54, 4), xytext=(54, 1.5), fontsize=9.5, color=GREY, ha="center",
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
    fig.tight_layout()
    save(fig, "ch06_fig_market_and_firm.png")


# =========================================================== profit maximisation
def fig_profit_max():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    cost_axes(ax, ymax=8.6)
    atc_star = ATC[7]                      # $3.25 at 80 meals
    ax.add_patch(plt.Rectangle((0, atc_star), Q_STAR, P_STAR - atc_star,
                               facecolor=TINT_GREEN, edgecolor=GREEN, lw=1.2, zorder=2))
    draw_costs(ax, avc=False)
    ax.axhline(P_STAR, color=BLUE, lw=2.4, zorder=6)
    ax.annotate(r"MR = P = \$4", (14, P_STAR), textcoords="offset points",
                xytext=(0, 7), fontsize=10, color=BLUE, fontweight="bold")
    ax.plot([Q_STAR, Q_STAR], [0, P_STAR], color=GREY, lw=1.0, ls=":")
    ax.scatter([Q_STAR], [P_STAR], s=50, color=INK, zorder=9)
    ax.annotate("MR = MC here", (Q_STAR, P_STAR), xytext=(52, 6.9), fontsize=9.5,
                color=INK, fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    ax.annotate(f"ATC = \\${atc_star:.2f}", (14, atc_star), textcoords="offset points",
                xytext=(0, -15), fontsize=9.5, color=GREEN, fontweight="bold")
    ax.annotate(f"PROFIT  \\${PROFIT_STAR:.0f}", (Q_STAR / 2, (P_STAR + atc_star) / 2),
                ha="center", va="center", fontsize=11.5, color=GREEN,
                fontweight="bold", zorder=10)
    qticks(ax)                                   # 80 meals is read off this one
    save(fig, "ch06_fig_profit_max.png")


def fig_three_prices():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    cost_axes(ax, ymax=8.6)
    draw_costs(ax, avc=False)
    for p, qq in [(P_HIGH, Q_HIGH), (P_STAR, Q_STAR), (P_LOSS, Q_LOSS)]:
        ax.axhline(p, color=BLUE, lw=2.0, zorder=5)
        ax.plot([qq, qq], [0, p], color=GREY, lw=0.9, ls=":")
        ax.scatter([qq], [p], s=40, color=INK, zorder=9)
        ax.annotate(f"MR = \\${p:.0f}", (30, p), textcoords="offset points",
                    xytext=(0, 6), fontsize=9.5, color=BLUE, fontweight="bold")
    ax.annotate("higher price  →  further up MC  →  more meals", (55, 7.6),
                fontsize=10, color=INK, ha="center", fontweight="bold")
    qticks(ax, 70, 90)                           # all three quantities are read off
    ax.set_xticks([0, 20, 40, 60, 70, 80, 90])
    save(fig, "ch06_fig_three_prices.png")


# ================================================ losing money and staying open
def fig_loss_but_open():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    cost_axes(ax, ymax=6.4)
    atc_l, avc_l = ATC[6], AVC[6]          # 3.1429 and 1.7143 at 70 meals
    ax.add_patch(plt.Rectangle((0, P_LOSS), Q_LOSS, atc_l - P_LOSS,
                               facecolor=TINT_RED, edgecolor=RED, lw=1.2, zorder=2))
    ax.add_patch(plt.Rectangle((0, avc_l), Q_LOSS, P_LOSS - avc_l,
                               facecolor=TINT_GREEN, edgecolor=GREEN, lw=1.2, zorder=2))
    draw_costs(ax)
    ax.axhline(P_LOSS, color=BLUE, lw=2.4, zorder=6)
    ax.annotate(r"P = MR = \$2", (86, P_LOSS), textcoords="offset points",
                xytext=(0, 7), fontsize=10, color=BLUE, fontweight="bold")
    ax.plot([Q_LOSS, Q_LOSS], [0, atc_l], color=GREY, lw=1.0, ls=":")
    ax.annotate(f"LOSS  \\${LOSS_OPEN:.0f}", (Q_LOSS / 2, (P_LOSS + atc_l) / 2),
                ha="center", va="center", fontsize=11, color=RED, fontweight="bold",
                zorder=10)
    ax.annotate(f"the green sliver covers \\${COVERS:.0f}\nof the \\$100 overhead",
                (Q_LOSS * 0.62, (avc_l + P_LOSS) / 2), xytext=(88, 0.85),
                ha="center", fontsize=9, color=GREEN, fontweight="bold", zorder=12,
                bbox=BOX, arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))
    ax.annotate("P below ATC  →  a loss\nP above AVC  →  open anyway", (54, 5.4),
                fontsize=10.5, color=INK, ha="center", fontweight="bold")
    qticks(ax, 70)                               # 70 meals is read off this one
    save(fig, "ch06_fig_loss_but_open.png")


def fig_shutdown():
    fig, ax = plt.subplots(figsize=(6.4, 3.5))
    cost_axes(ax, ymax=6.4)
    ax.add_patch(plt.Rectangle((0, 0), 108, P_AVCMIN, facecolor="#F4F4F4",
                               edgecolor="none", zorder=1))
    ax.plot(QQ, _atc(QQ), color=GREEN, lw=2.2, zorder=4)
    ax.annotate("ATC", (100, ATC[-1]), textcoords="offset points", xytext=(5, -2),
                color=GREEN, fontsize=11, fontweight="bold", zorder=12, bbox=BOX)
    ax.plot(QQ, _avc(QQ), color=DGOLD, lw=2.2, zorder=3)
    ax.annotate("AVC", (100, AVC[-1]), textcoords="offset points", xytext=(5, -10),
                color=DGOLD, fontsize=11, fontweight="bold", zorder=12, bbox=BOX)
    draw_mc_blocks(ax)
    draw_mc_smooth(ax)
    ax.axhline(P_AVCMIN, color=GREY, lw=1.5, ls=(0, (6, 3)), zorder=4)
    ax.annotate(f"shutdown price = min AVC = \\${P_AVCMIN:.2f}", (4, P_AVCMIN),
                textcoords="offset points", xytext=(0, 9), fontsize=10, color=GREY,
                fontweight="bold", bbox=BOX, zorder=12)
    ax.axhline(1.50, color=BLUE, lw=2.4, zorder=6)
    ax.annotate(r"P = \$1.50", (4, 1.50), textcoords="offset points",
                xytext=(0, -15), fontsize=10, color=BLUE, fontweight="bold")
    ax.annotate("every meal loses money on its\ningredients alone → serve nobody",
                (74, 0.60), fontsize=10, color=RED, ha="center", fontweight="bold",
                bbox=BOX, zorder=12)
    ax.scatter([Q_AVCMIN], [P_AVCMIN], s=48, color=DGOLD, zorder=9,
               edgecolor="white", lw=1.3)
    save(fig, "ch06_fig_shutdown.png")


def fig_supply_curve():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    cost_axes(ax, ymax=8.6)
    dead = np.linspace(8, Q_CROSS_AVC, 200)
    live = np.linspace(Q_CROSS_AVC, 100, 400)
    ax.plot(dead, _mc_smooth(dead), color=LGREY, lw=2.0, zorder=3)
    ax.plot(QQ, _avc(QQ), color=DGOLD, lw=1.8, zorder=3, alpha=0.75)
    ax.plot(live, _mc_smooth(live), color=RED, lw=3.8, zorder=6)
    ax.plot([0, 0], [0, P_AVCMIN], color=RED, lw=3.8, zorder=6)
    ax.scatter([Q_AVCMIN], [P_AVCMIN], s=54, color=RED, zorder=9,
               edgecolor="white", lw=1.4)
    ax.annotate("THIS is the restaurant's supply curve:\nthe part of MC above AVC",
                (88, _mc_smooth(88)), xytext=(45, 7.3), fontsize=10, color=RED,
                fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax.annotate(f"below \\${P_AVCMIN:.2f}\nquantity supplied = 0", (0, P_AVCMIN / 2),
                xytext=(24, 2.6), fontsize=9.5, color=RED, fontweight="bold",
                ha="center", arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    ax.annotate("AVC", (100, AVC[-1]), textcoords="offset points", xytext=(5, -10),
                color=DGOLD, fontsize=11, fontweight="bold")
    save(fig, "ch06_fig_supply_curve.png")


# =============================================== producer surplus, and it is not profit
def fig_producer_surplus():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    cost_axes(ax, ymax=8.6)
    band = QQ[QQ <= Q_STAR]
    ax.fill_between(band, _mc(band), P_STAR, where=_mc(band) <= P_STAR,
                    color=TINT_RED, edgecolor=RED, lw=1.1, zorder=2)
    ax.plot(QQ, _mc(QQ), color=RED, lw=2.4, zorder=5)
    ax.plot(QQ, _atc(QQ), color=GREEN, lw=1.8, zorder=4, alpha=0.8)
    ax.axhline(P_STAR, color=BLUE, lw=2.4, zorder=6)
    ax.plot([Q_STAR, Q_STAR], [0, P_STAR], color=GREY, lw=1.0, ls=":")
    ax.annotate(r"P = \$4", (14, P_STAR), textcoords="offset points",
                xytext=(0, 7), fontsize=10, color=BLUE, fontweight="bold")
    ax.annotate("MC", (100, MC[-1]), textcoords="offset points", xytext=(5, 0),
                color=RED, fontsize=11, fontweight="bold", zorder=12)
    ax.annotate("ATC", (100, ATC[-1]), textcoords="offset points", xytext=(5, -2),
                color=GREEN, fontsize=11, fontweight="bold", zorder=12,
                bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none", alpha=0.92))
    ax.annotate(f"PRODUCER\nSURPLUS\n\\${PS_STAR:.0f}", (42, 2.5), ha="center",
                va="center", fontsize=11, color=RED, fontweight="bold", zorder=10)
    ax.annotate("= revenue \\$320 − variable cost \\$160", (54, 7.6), fontsize=10,
                color=INK, ha="center", fontweight="bold")
    save(fig, "ch06_fig_producer_surplus.png")


# ============================================== why the average curves bend
def fig_cost_anatomy():
    """AFC falls forever, AVC turns up, and ATC is the race between them."""
    fig, ax = plt.subplots(figsize=(6.6, 3.2))
    q = np.linspace(20, 100, 500)
    ax.plot(q, _afc(q), color=BLUE, lw=2.2, ls=(0, (5, 2)))
    ax.plot(q, _avc(q), color=DGOLD, lw=2.2)
    ax.plot(q, _atc(q), color=GREEN, lw=2.6)
    ax.annotate("AFC = \\$100 / Q\nfalls forever", (34, _afc(34)), xytext=(46, 6.6),
                fontsize=9.5, color=BLUE, fontweight="bold", ha="center", bbox=BOX,
                zorder=12, arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.0))
    ax.annotate("AVC turns up as\ndiminishing returns bite", (86, _avc(86)),
                xytext=(62, 1.05), fontsize=9.5, color=DGOLD, fontweight="bold",
                ha="center", bbox=BOX, zorder=12,
                arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.0))
    ax.annotate("ATC = AFC + AVC", (100, ATC[-1]), textcoords="offset points",
                xytext=(-6, 12), fontsize=10.5, color=GREEN, fontweight="bold",
                ha="right", bbox=BOX, zorder=12)
    ax.annotate("", (70, AVC[6]), xytext=(70, ATC[6]),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.2))
    ax.annotate("this gap IS\naverage fixed cost", (70, (AVC[6] + ATC[6]) / 2),
                xytext=(28, 3.9), fontsize=9, color=GREY, ha="center", bbox=BOX,
                zorder=12, arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
    ax.set_xlim(0, 108)
    ax.set_ylim(0, 8.0)
    ax.set_xlabel("Meals")
    ax.set_xticks([])
    ax.set_ylabel("Cost per meal")
    ax.yaxis.set_major_formatter(FuncFormatter(dollars0))
    ax.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    ax.set_axisbelow(True)
    save(fig, "ch06_fig_cost_anatomy.png")


# ============================================== what a price rise adds to the seller
def _ps_panel(ax, price, qstar, tvc, title_txt):
    band = QQ[QQ <= qstar]
    ax.fill_between(band, _mc(band), price, where=_mc(band) <= price,
                    color=TINT_RED, edgecolor=RED, lw=1.1, zorder=2)
    ax.plot(QQ, _mc(QQ), color=RED, lw=2.4, zorder=5)
    ax.axhline(price, color=BLUE, lw=2.4, zorder=6)
    ax.plot([qstar, qstar], [0, price], color=GREY, lw=1.0, ls=":")
    ax.set_xlim(0, 108)
    ax.set_ylim(0, 8.6)
    ax.set_xlabel("Meals")
    ax.set_xticks([])
    ax.yaxis.set_major_formatter(FuncFormatter(dollars0))
    ax.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    ax.set_axisbelow(True)
    ax.set_title(title_txt, fontsize=10.5, color=INK, fontweight="bold", pad=8)
    ax.annotate("MC", (100, MC[-1]), textcoords="offset points", xytext=(-4, 4),
                color=RED, fontsize=10, fontweight="bold", ha="right")
    qticks(ax, int(qstar))                       # each panel's own quantity is read off
    return price * qstar - tvc


def fig_ps_price_rise():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.8, 3.2))
    ps1 = _ps_panel(a1, P_STAR, Q_STAR, TVC[8], "(a)  At \$4 a meal")
    a1.set_ylabel("Price / cost per meal")
    a1.annotate(f"\\${ps1:.0f}", (40, 2.4), ha="center", va="center", fontsize=13,
                color=RED, fontweight="bold", zorder=9)
    ps2 = _ps_panel(a2, P_HIGH, Q_HIGH, TVC[9], "(b)  At \$6 a meal")
    a2.annotate(f"\\${ps2:.0f}", (42, 2.8), ha="center", va="center", fontsize=13,
                color=RED, fontweight="bold", zorder=9)
    a2.annotate(f"+\\${ps2 - ps1:.0f}", (70, 7.4), fontsize=11, color=GREEN,
                fontweight="bold", ha="center")
    assert abs(ps1 - 160) < 1e-9 and abs(ps2 - 320) < 1e-9
    fig.tight_layout()
    save(fig, "ch06_fig_ps_price_rise.png")


# ============================================================ long-run average cost
def fig_lrac():
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    q = np.linspace(15, 210, 500)
    plants = [(40, 4.20, 3.0), (75, 3.15, 3.2), (120, 3.15, 3.2), (175, 3.90, 3.0)]
    for qk, ck, a in plants:
        y = ck + a * ((q - qk) / qk) ** 2
        m = y < 7.4
        ax.plot(q[m], y[m], color=LGREY, lw=1.6, zorder=3)
    env = np.minimum.reduce([ck + a * ((q - qk) / qk) ** 2 for qk, ck, a in plants])
    ax.plot(q, env, color=BLUE, lw=3.0, zorder=6)
    ax.annotate("Long-run ATC", (206, env[-1]), textcoords="offset points",
                xytext=(-4, 13), fontsize=10.5, color=BLUE, fontweight="bold",
                ha="right")
    ax.annotate("four possible\nrestaurant sizes", (40, 4.20), xytext=(38, 6.5),
                fontsize=9, color=GREY, ha="center",
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
    for x0, x1, lab, col in [(15, 75, "ECONOMIES\nOF SCALE", GREEN),
                             (75, 120, "CONSTANT\nRETURNS", INK),
                             (120, 210, "DISECONOMIES\nOF SCALE", RED)]:
        ax.annotate(lab, ((x0 + x1) / 2, 0.75), ha="center", fontsize=9,
                    color=col, fontweight="bold")
    for xv in (75, 120):
        ax.axvline(xv, color="#DDDDDD", lw=1.0, zorder=1)
    ax.set_xlim(15, 210)
    ax.set_ylim(0, 7.4)
    ax.set_xlabel("Meals")
    ax.set_xticks([])
    ax.set_ylabel("Average total cost")
    ax.yaxis.set_major_formatter(FuncFormatter(dollars0))
    ax.grid(True, axis="y", color="#F4F4F4", lw=0.7)
    ax.set_axisbelow(True)
    save(fig, "ch06_fig_lrac.png")


# ============================================================== entry and exit
# THE MARKET PANEL IS SOLVED, NOT DRAWN BY EYE.
#
# The old version hard-coded a demand intercept and a supply shift and then drew dotted
# price lines at $4.00, $3.14 and $2.00 on top.  None of the three actually met the
# curves: the entry panel's second equilibrium sat at $3.34 and the exit panel's at
# $3.20 and $2.60.  A student reading the picture rather than the label saw a different
# number, which is the one thing a diagram must never do.
#
# Both panels now take the equilibria as INPUT - the (quantity, price) pairs the story
# needs - and solve for the lines that pass through them.  Every intersection is then
# asserted before the figure is saved.  Quantities are illustrative and the axis is
# unnumbered, so the scale is free; the prices are the chapter's and are exact.


def _line_through(p1, p2):
    """(slope, intercept) of the straight line through two (q, p) points."""
    (q1, y1), (q2, y2) = p1, p2
    m = (y2 - y1) / (q2 - q1)
    return m, y1 - m * q1


def _draw_line(ax, m, b, color, ls="-", lw=2.4, ymax=8.6, qmax=100):
    q = np.linspace(0, qmax, 400)
    y = b + m * q
    ok = (y >= 0) & (y <= ymax)
    ax.plot(q[ok], y[ok], color=color, lw=lw, ls=ls, zorder=4)
    return q[ok], y[ok]


def _eq_dot(ax, q, p, color=INK):
    ax.plot([0, q], [p, p], color=GREY, lw=0.9, ls=":", zorder=2)
    ax.plot([q, q], [0, p], color=GREY, lw=0.9, ls=":", zorder=2)
    ax.scatter([q], [p], s=46, color=color, zorder=9)


def _market_axes(ax, title):
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 8.6)
    ax.set_xticks([])
    ax.set_yticks([0.0, 2.0, P_ATCMIN, P_STAR, 6.0, 8.0])
    ax.set_yticklabels(["$0", "$2", "$3.14", "$4", "$6", "$8"])
    ax.set_xlabel("Meals, the whole market")
    ax.set_ylabel("Price per meal")
    ax.set_title(title, fontsize=10.5, color=INK, fontweight="bold", pad=8)
    ax.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    ax.set_axisbelow(True)


def entry_market_panel(ax):
    """Demand fixed.  Restaurants open, supply swings right, price $4.00 -> $3.14."""
    E1, E2 = (40.0, P_STAR), (62.0, P_ATCMIN)
    dm, db = _line_through(E1, E2)                 # demand runs through both equilibria
    sm, sb = P_STAR / E1[0], 0.0                   # S1 out of the origin, through E1
    sb2 = E2[1] - sm * E2[0]                       # S2: same slope, through E2
    assert abs((db - sb) / (sm - dm) - E1[0]) < 1e-9
    assert abs((db - sb2) / (sm - dm) - E2[0]) < 1e-9
    _market_axes(ax, "(a)  The market")
    _draw_line(ax, dm, db, BLUE)
    ax.annotate("D", (6, db + dm * 6), textcoords="offset points", xytext=(-2, 5),
                color=BLUE, fontsize=10.5, fontweight="bold", ha="right")
    _draw_line(ax, sm, sb, RED)
    ax.annotate("S$_1$", (72, sb + sm * 72), textcoords="offset points",
                xytext=(-3, 5), color=RED, fontsize=10.5, fontweight="bold", ha="right",
                bbox=BOX, zorder=11)
    _draw_line(ax, sm, sb2, RED, ls=(0, (5, 2)))
    ax.annotate("S$_2$", (95, sb2 + sm * 95), textcoords="offset points",
                xytext=(4, -2), color=RED, fontsize=10.5, fontweight="bold", zorder=11)
    _eq_dot(ax, *E1)
    _eq_dot(ax, *E2)
    ax.annotate("", (51, E2[1]), xytext=(51, E1[1]),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.2))
    return E1, E2


def exit_market_panel(ax):
    """Demand falls $3.14 -> $2.00; restaurants close; supply swings left, price back."""
    sm, sb = P_LOSS / 30.0, 0.0                    # S1 out of the origin, exactly
    E1 = (30.0, P_LOSS)                            # after demand falls
    E0 = (P_ATCMIN / sm, P_ATCMIN)                 # where it started, on the same S1
    E2 = (14.0, P_ATCMIN)                          # after exit, back to min ATC
    dm = (E1[1] - E2[1]) / (E1[0] - E2[0])         # demand slope, set by the D2 story
    d1b = E0[1] - dm * E0[0]
    d2b = E1[1] - dm * E1[0]
    sb2 = E2[1] - sm * E2[0]                       # S2: same slope, through E2
    assert abs((d1b - sb) / (sm - dm) - E0[0]) < 1e-6
    assert abs((d2b - sb) / (sm - dm) - E1[0]) < 1e-6
    assert abs((d2b - sb2) / (sm - dm) - E2[0]) < 1e-6
    _market_axes(ax, "(a)  The market")
    _draw_line(ax, sm, sb, RED)
    ax.annotate("S$_1$", (97, sb + sm * 97), textcoords="offset points",
                xytext=(4, -2), color=RED, fontsize=10.5, fontweight="bold", zorder=11)
    _draw_line(ax, sm, sb2, RED, ls=(0, (5, 2)))
    ax.annotate("S$_2$", (63, sb2 + sm * 63), textcoords="offset points",
                xytext=(-3, 5), color=RED, fontsize=10.5, fontweight="bold", ha="right",
                bbox=BOX, zorder=11)
    _draw_line(ax, dm, d1b, BLUE)
    ax.annotate("D$_1$", (86, d1b + dm * 86), textcoords="offset points",
                xytext=(4, 2), color=BLUE, fontsize=10.5, fontweight="bold", zorder=11)
    _draw_line(ax, dm, d2b, BLUE, ls=(0, (5, 2)))
    ax.annotate("D$_2$", (53, d2b + dm * 53), textcoords="offset points",
                xytext=(3, 3), color=BLUE, fontsize=10.5, fontweight="bold", zorder=11)
    _eq_dot(ax, *E0)
    _eq_dot(ax, *E1)
    _eq_dot(ax, *E2)
    ax.annotate("", (E0[0] - 4, E1[1]), xytext=(E0[0] - 4, E0[1]),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2.0))
    ax.annotate("", (E2[0] + 3, E2[1]), xytext=(E2[0] + 3, E1[1]),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.0))
    return E0, E1, E2


def fig_entry():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.8, 3.3))
    entry_market_panel(a1)
    a1.annotate("more McDonald's open\n→ supply shifts right\n→ price falls",
                (27, 8.35), fontsize=9, color=GREEN, ha="center", va="top",
                fontweight="bold", zorder=12)
    cost_axes(a2, ymax=8.6, ylabel="")
    draw_mc_smooth(a2, lw=2.2, label=False)
    a2.plot(QQ, _atc(QQ), color=GREEN, lw=2.2)
    atc_star = ATC[7]
    a2.add_patch(plt.Rectangle((0, atc_star), Q_STAR, P_STAR - atc_star,
                               facecolor=TINT_GREEN, edgecolor=GREEN, lw=1.0, zorder=2))
    a2.axhline(P_STAR, color=BLUE, lw=2.0, zorder=6)
    a2.axhline(P_ATCMIN, color=BLUE, lw=2.0, ls=(0, (5, 2)), zorder=6)
    a2.scatter([Q_ATCMIN], [P_ATCMIN], s=44, color=INK, zorder=9)
    a2.annotate(r"profit \$60", (Q_STAR / 2, (P_STAR + atc_star) / 2), ha="center",
                va="center", fontsize=9, color=GREEN, fontweight="bold", zorder=10)
    a2.annotate("at \\$3.14, P = min ATC\nprofit = 0", (Q_ATCMIN, P_ATCMIN),
                xytext=(40, 6.4), fontsize=9, color=INK, fontweight="bold",
                ha="center", arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    for lab, arr, col in [("MC", float(_mc_smooth(100)), RED), ("ATC", ATC[-1], GREEN)]:
        a2.annotate(lab, (100, arr), textcoords="offset points", xytext=(4, -3),
                    color=col, fontsize=10, fontweight="bold")
    a2.set_title("(b)  One restaurant", fontsize=10.5, color=INK, fontweight="bold",
                 pad=8)
    a2.set_xlabel("Meals, this restaurant")
    fig.tight_layout()
    save(fig, "ch06_fig_exit.png" if False else "ch06_fig_entry.png")


def fig_exit():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.8, 3.3))
    exit_market_panel(a1)
    a1.annotate("demand falls → price drops to \\$2\nthen restaurants close\n→ price climbs back",
                (78, 8.45), fontsize=8.5, color=INK, ha="center", va="top",
                fontweight="bold", zorder=12, bbox=BOX)
    cost_axes(a2, ymax=8.6, ylabel="")
    draw_mc_smooth(a2, lw=2.2, label=False)
    a2.plot(QQ, _atc(QQ), color=GREEN, lw=2.2)
    a2.plot(QQ, _avc(QQ), color=DGOLD, lw=1.8)
    atc_l = ATC[6]
    a2.add_patch(plt.Rectangle((0, P_LOSS), Q_LOSS, atc_l - P_LOSS,
                               facecolor=TINT_RED, edgecolor=RED, lw=1.0, zorder=2))
    a2.axhline(P_LOSS, color=BLUE, lw=2.0, zorder=6)
    a2.annotate(r"loss \$80", (Q_LOSS / 2, (P_LOSS + atc_l) / 2), ha="center",
                va="center", fontsize=9, color=RED, fontweight="bold", zorder=10)
    a2.annotate("restaurants close until\nP is back to \\$3.14", (52, 7.4), fontsize=9,
                color=INK, ha="center", fontweight="bold")
    for lab, arr, col in [("MC", float(_mc_smooth(100)), RED), ("ATC", ATC[-1], GREEN),
                          ("AVC", AVC[-1], DGOLD)]:
        a2.annotate(lab, (100, arr), textcoords="offset points", xytext=(4, -3),
                    color=col, fontsize=10, fontweight="bold")
    a2.set_title("(b)  One restaurant", fontsize=10.5, color=INK, fontweight="bold",
                 pad=8)
    a2.set_xlabel("Meals, this restaurant")
    fig.tight_layout()
    save(fig, "ch06_fig_exit.png")


def fig_lr_supply():
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    q = np.linspace(0, 100, 300)
    for d, st, lab in [(7.0, "-", "D$_1$"), (5.8, (0, (4, 2)), "D$_2$"),
                       (8.2, (0, (4, 2)), "D$_3$")]:
        ax.plot(q, d - 0.06 * q, color=BLUE, lw=2.0, alpha=0.55, ls=st)
        qd = (d - P_ATCMIN) / 0.06
        ax.scatter([qd], [P_ATCMIN], s=40, color=INK, zorder=8)
        ax.annotate(lab, (5, d - 0.30), color=BLUE, fontsize=10, fontweight="bold",
                    va="bottom", ha="left")
    ax.axhline(P_ATCMIN, color=RED, lw=3.2, zorder=6)
    ax.annotate("LONG-RUN SUPPLY", (16, P_ATCMIN), textcoords="offset points",
                xytext=(0, 10), fontsize=10.5, color=RED, fontweight="bold",
                ha="center")
    ax.annotate(f"at min ATC = \\${P_ATCMIN:.2f}", (16, P_ATCMIN),
                textcoords="offset points", xytext=(0, -20), fontsize=9.5, color=RED,
                ha="center")
    ax.annotate("demand moves, price does not —\nonly the number of restaurants changes",
                (58, 7.9), fontsize=10, color=INK, ha="center", fontweight="bold",
                va="top")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 8.6)
    ax.set_yticks([0, 2, P_ATCMIN, 6, 8])
    ax.set_yticklabels(["$0", "$2", "$3.14", "$6", "$8"])
    ax.set_xticks([])
    ax.set_xlabel("Meals, the whole market")
    ax.set_ylabel("Price per meal")
    ax.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    ax.set_axisbelow(True)
    save(fig, "ch06_fig_lr_supply.png")


# ================================================ the seller's problem, and the margin
def fig_sellers_problem():
    fig, ax = plt.subplots(figsize=(6.6, 2.3))
    ax.axis("off")
    boxes = [("PRODUCTION", "inputs → outputs", BLUE),
             ("COSTS", "outputs → dollars out", RED),
             ("REVENUES", "outputs → dollars in", GREEN)]
    for i, (lab, sub, col) in enumerate(boxes):
        x = 0.04 + i * 0.335
        ax.add_patch(plt.Rectangle((x, 0.36), 0.28, 0.44, transform=ax.transAxes,
                                   facecolor="white", edgecolor=col, lw=2.0))
        ax.text(x + 0.14, 0.65, lab, transform=ax.transAxes, ha="center",
                fontsize=12, color=col, fontweight="bold")
        ax.text(x + 0.14, 0.48, sub, transform=ax.transAxes, ha="center",
                fontsize=9.5, color=GREY)
        if i < 2:
            ax.annotate("", (x + 0.325, 0.58), xytext=(x + 0.285, 0.58),
                        xycoords=ax.transAxes, textcoords=ax.transAxes,
                        arrowprops=dict(arrowstyle="->", color=GREY, lw=1.6))
    ax.text(0.5, 0.16, "…and the three together answer one question:  "
                       "how much should I make?", transform=ax.transAxes,
            ha="center", fontsize=10.5, color=INK, fontweight="bold")
    save(fig, "ch06_fig_sellers_problem.png")


def fig_margin():
    """The margin, and what entry does to it.

    ILLUSTRATIVE ROUND NUMBERS - the deck's own, not figures from any film.
    """
    fig, ax = plt.subplots(figsize=(9.4, 2.15))
    rows = [("Today: one seller outside the bank — price $2.00", 2.00, 0.20, GREEN),
            ("Later: anyone can set up the same stall — price $0.30", 0.30, 0.20, RED)]
    for i, (lab, price, mc, col) in enumerate(rows):
        y = 1 - i
        ax.barh(y, mc, height=0.42, color=DGOLD, zorder=3)
        ax.barh(y, price - mc, left=mc, height=0.42, color=col, alpha=0.35,
                edgecolor=col, lw=1.4, zorder=3)
        ax.annotate(lab, (0, y + 0.30), fontsize=10, color=INK, fontweight="bold",
                    va="bottom")
        if price - mc > 0.9:
            ax.annotate(f"margin \\${price - mc:.2f}", (mc + (price - mc) / 2, y),
                        ha="center", va="center", fontsize=10.5, color=col,
                        fontweight="bold", zorder=6)
        else:
            ax.annotate(f"margin \\${price - mc:.2f}", (price, y),
                        textcoords="offset points", xytext=(10, 0), va="center",
                        fontsize=10.5, color=col, fontweight="bold", zorder=6)
    ax.annotate("cost of\nmaking one", (0.10, -0.55), ha="center", fontsize=9,
                color=DGOLD, fontweight="bold")
    ax.set_xlim(0, 2.45)
    ax.set_ylim(-0.85, 1.62)
    ax.set_yticks([])
    ax.set_xlabel("Dollars per unit sold")
    ax.xaxis.set_major_formatter(FuncFormatter(money))
    ax.grid(True, axis="x", color="#EEEEEE", lw=0.7)
    ax.set_axisbelow(True)
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    save(fig, "ch06_fig_margin.png")


# ================================================== three elasticities of supply
def fig_supply_elasticity():
    fig, axes = plt.subplots(1, 3, figsize=(8.2, 2.8))
    for ax in axes:
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_xlim(0, 10); ax.set_ylim(0, 10)
        ax.set_xlabel("Quantity", fontsize=9.5)
    axes[0].set_ylabel("Price", fontsize=9.5)

    axes[0].axhline(5, color=RED, lw=2.6)
    axes[0].set_yticks([5]); axes[0].set_yticklabels([r"\$5"], fontsize=9.5)
    axes[0].set_title("(a)  Perfectly elastic\n" + r"$\varepsilon_S=\infty$",
                      fontsize=10, color=INK, pad=6)

    axes[1].plot([0, 8], [0, 9.6], color=RED, lw=2.6)
    for xa, ya in [(4, 4.8), (6, 7.2)]:
        axes[1].plot([0, xa], [ya, ya], color=GREY, lw=0.9, ls=":")
        axes[1].plot([xa, xa], [0, ya], color=GREY, lw=0.9, ls=":")
    axes[1].set_yticks([4.8, 7.2]); axes[1].set_yticklabels([r"\$5", r"\$6"], fontsize=9.5)
    axes[1].set_xticks([4, 6]); axes[1].set_xticklabels(["100", "120"], fontsize=9.5)
    axes[1].annotate("+20% price\n+20% quantity", (7.6, 3.0), ha="center", fontsize=9,
                     color=RED, fontweight="bold")
    axes[1].set_title("(b)  Unit elastic\n" + r"$\varepsilon_S=1$", fontsize=10,
                      color=INK, pad=6)

    axes[2].plot([5, 5], [0, 9], color=RED, lw=2.6)
    for ya in (5, 6):
        axes[2].plot([0, 5], [ya, ya], color=GREY, lw=0.9, ls=":")
    axes[2].set_yticks([5, 6]); axes[2].set_yticklabels([r"\$5", r"\$6"], fontsize=9.5)
    axes[2].set_xticks([5]); axes[2].set_xticklabels(["100"], fontsize=9.5)
    axes[2].annotate("+20% price\n0% quantity", (7.6, 3.0), ha="center", fontsize=9,
                     color=RED, fontweight="bold")
    axes[2].set_title("(c)  Perfectly inelastic\n" + r"$\varepsilon_S=0$", fontsize=10,
                      color=INK, pad=6)
    fig.tight_layout()
    save(fig, "ch06_fig_supply_elasticity.png")


# ============================================== ethanol: plants and average size
ETH = [
    (1999, 50, 1778.7), (2000, 54, 1840.2), (2001, 56, 2006.6), (2002, 61, 2738.0),
    (2003, 68, 3189.8), (2004, 72, 3698.8), (2005, 81, 4397.7), (2006, 95, 6317.4),
    (2007, 110, 11622.9), (2008, 139, 13424.4), (2009, 170, 14541.4),
    (2010, 193, 13614.0), (2011, 194, 13728.0), (2012, 193, 13852.0),
    (2013, 187, 13681.0), (2014, 195, 14369.0), (2015, 195, 14903.0),
    (2016, 198, 15505.0), (2017, 200, 16288.0), (2018, 200, 16868.0),
    (2019, 201, 17378.0), (2020, 197, 17546.0), (2021, 192, 17380.0),
    (2022, 187, 17663.0), (2023, 187, 18010.0),
]


def fig_ethanol_plants():
    yr = np.array([r[0] for r in ETH])
    pl = np.array([r[1] for r in ETH], dtype=float)
    cap = np.array([r[2] for r in ETH])
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.plot(yr, pl, color=BLUE, lw=2.6, zorder=5)
    ax.scatter([2019], [201], s=48, color=BLUE, zorder=7)
    ax.annotate("201 plants, 2019", (2019, 201), xytext=(2019.5, 258), fontsize=9.5,
                color=BLUE, fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.0))
    ax.axvline(2006, color=GREY, lw=1.1, ls=(0, (4, 3)))
    ax.annotate("Jan 2006:\n\"addicted to oil\"", (2005.8, 268), fontsize=9,
                color=GREY, ha="center", va="top")
    ax.axvline(2011.95, color=GREY, lw=1.1, ls=(0, (4, 3)))
    ax.annotate("Dec 2011:\nblender's credit\nexpires", (2012.3, 268), fontsize=9,
                color=GREY, ha="center", va="top")
    ax.set_ylim(0, 285)
    ax.set_xlim(1999, 2023)
    ax.set_ylabel("Number of ethanol plants", color=BLUE)
    ax.tick_params(axis="y", colors=BLUE)
    ax.grid(True, color="#F2F2F2", lw=0.7)
    ax.set_axisbelow(True)

    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.plot(yr, cap / pl, color=RED, lw=2.6, zorder=5)
    ax2.set_ylim(0, 140)
    ax2.set_ylabel("Average plant size (million gal/yr)", color=RED)
    ax2.tick_params(axis="y", colors=RED)
    ax2.annotate("average plant size:\n34 → 96 million gal/yr", (2022, cap[-2] / pl[-2]),
                 xytext=(2014.5, 34), fontsize=9.5, color=RED, fontweight="bold",
                 ha="center", arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    save(fig, "ch06_fig_ethanol_plants.png")


ETH_SCHED = [(1.40, 2), (1.35, 4), (1.30, 6), (1.25, 8), (1.20, 10), (1.15, 12),
             (1.10, 14), (1.05, 16), (1.00, 18), (0.95, 20), (0.90, 22), (0.85, 24)]


def fig_ethanol_subsidy():
    fig, ax = plt.subplots(figsize=(6.3, 3.4))
    p = np.array([r[0] for r in ETH_SCHED])
    qd = np.array([r[1] for r in ETH_SCHED], dtype=float)
    ax.plot(qd, p, color=BLUE, lw=2.6, zorder=5)
    ax.annotate("market demand", (23.5, 0.865), color=BLUE, fontsize=10,
                fontweight="bold", ha="right")
    ax.axhline(1.00, color=GREEN, lw=2.2, ls=(0, (5, 2)), zorder=4)
    ax.axhline(1.05, color=RED, lw=2.6, zorder=6)
    ax.annotate("ATC with the OLD 25¢ subsidy = \\$1.00", (0.5, 1.00),
                textcoords="offset points", xytext=(0, -15), fontsize=9.5,
                color=GREEN, fontweight="bold")
    ax.annotate("ATC with the NEW 20¢ subsidy = \\$1.05", (0.5, 1.05),
                textcoords="offset points", xytext=(0, 7), fontsize=9.5, color=RED,
                fontweight="bold")
    ax.scatter([16], [1.05], s=60, color=INK, zorder=9)
    ax.plot([16, 16], [0.84, 1.05], color=GREY, lw=1.0, ls=":")
    ax.annotate("long-run equilibrium\n16 m gallons ÷ 2 m per plant\n= 8 sellers",
                (16, 1.05), xytext=(9.5, 1.31), fontsize=9.5, color=INK,
                fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
    ax.scatter([18], [1.00], s=44, color=GREY, zorder=8)
    ax.annotate("at \\$1.00 every seller\nloses \\$100,000", (18, 1.00),
                xytext=(21.5, 1.10), fontsize=9, color=RED, ha="center",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
    ax.set_xlim(0, 26)
    ax.set_ylim(0.84, 1.45)
    ax.set_xlabel("Millions of gallons on the market")
    ax.set_ylabel("Price per gallon")
    ax.yaxis.set_major_formatter(FuncFormatter(money))
    ax.grid(True, color="#EEEEEE", lw=0.7)
    ax.set_axisbelow(True)
    save(fig, "ch06_fig_ethanol_subsidy.png")


# ============================================== LIVE: the shutdown rule in the field
DF = [("Eagle Ford", 26, 61), ("Permian – Delaware", 33, 62),
      ("Permian – Midland", 35, 62), ("Other US shale", 41, 63),
      ("Other US non-shale", 45, 66), ("Permian – other", 45, 70)]


def fig_dallas_fed():
    fig, ax = plt.subplots(figsize=(6.8, 3.5))
    ycs = np.arange(len(DF))
    op = np.array([r[1] for r in DF], dtype=float)
    nw = np.array([r[2] for r in DF], dtype=float)
    for y, a, b in zip(ycs, op, nw):
        ax.plot([a, b], [y, y], color="#DDDDDD", lw=6, zorder=2,
                solid_capstyle="round")
    ax.scatter(op, ycs, s=90, color=DGOLD, zorder=6,
               label="keep an existing well running")
    ax.scatter(nw, ycs, s=90, color=GREEN, zorder=6, label="drill a NEW well")
    ax.set_yticks(ycs)
    ax.set_yticklabels([r[0] for r in DF], fontsize=10)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("WTI crude price needed, US$ per barrel")
    ax.xaxis.set_major_formatter(FuncFormatter(dollars0))
    ax.grid(True, axis="x", color="#EEEEEE", lw=0.7)
    ax.set_axisbelow(True)
    ax.axvline(78.18, color=BLUE, lw=2.2, zorder=5)
    ax.annotate("WTI \\$78\n7 Aug 2026", (80.5, 2.6), fontsize=9, color=BLUE,
                fontweight="bold", ha="left", va="center")
    ax.axvspan(17, 29, color=TINT_RED, zorder=0)
    ax.annotate("Apr–May 2020\n\\$17–29", (23, -0.72), fontsize=8.5, color=RED,
                ha="center", fontweight="bold")
    ax.annotate("this is AVC", (26, 0), textcoords="offset points", xytext=(0, -20),
                fontsize=9, color=DGOLD, fontweight="bold", ha="center")
    ax.annotate("this is ATC", (61, 0), textcoords="offset points", xytext=(0, -20),
                fontsize=9, color=GREEN, fontweight="bold", ha="center")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.20), ncol=2, frameon=False,
              fontsize=9.5)
    save(fig, "ch06_fig_dallas_fed.png")


# ============================================== LIVE: corn against soybeans
FARMDOC = [("Central Illinois\n(high productivity)", -45, 67),
           ("Southern\nIllinois", -91, 30)]


def fig_corn_soy():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.0))
    x = np.arange(len(FARMDOC))
    corn = [r[1] for r in FARMDOC]
    soy = [r[2] for r in FARMDOC]
    a1.bar(x - 0.185, corn, width=0.35, color=DGOLD, label="Corn")
    a1.bar(x + 0.185, soy, width=0.35, color=GREEN, label="Soybeans")
    for xi, v in zip(x - 0.185, corn):
        a1.annotate(f"−${abs(v)}", (xi, v), textcoords="offset points",
                    xytext=(0, -13), ha="center", fontsize=9, color=DGOLD,
                    fontweight="bold")
    for xi, v in zip(x + 0.185, soy):
        a1.annotate(f"+${v}", (xi, v), textcoords="offset points", xytext=(0, 4),
                    ha="center", fontsize=9, color=GREEN, fontweight="bold")
    a1.axhline(0, color="#888888", lw=1.0)
    a1.set_xticks(x)
    a1.set_xticklabels([r[0] for r in FARMDOC], fontsize=8.5)
    a1.set_ylabel("Operator and land return, $ per acre")
    a1.yaxis.set_major_formatter(FuncFormatter(dollars0))
    a1.legend(frameon=False, fontsize=9, loc="upper right")
    a1.set_title("(a)  Projected 2026 returns", fontsize=10.5, color=INK,
                 fontweight="bold", pad=8)
    a1.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    a1.set_axisbelow(True)
    a1.set_ylim(-125, 118)

    cornA, soyA = [98.788, 95.343], [81.215, 85.365]
    x2 = np.arange(2)
    a2.bar(x2 - 0.185, cornA, width=0.35, color=DGOLD)
    a2.bar(x2 + 0.185, soyA, width=0.35, color=GREEN)
    for xi, v in zip(x2 - 0.185, cornA):
        a2.annotate(f"{v:.1f}", (xi, v), textcoords="offset points", xytext=(0, 3),
                    ha="center", fontsize=8.5, color=DGOLD, fontweight="bold")
    for xi, v in zip(x2 + 0.185, soyA):
        a2.annotate(f"{v:.1f}", (xi, v), textcoords="offset points", xytext=(0, 3),
                    ha="center", fontsize=8.5, color=GREEN, fontweight="bold")
    a2.annotate("corn −3%,  soybeans +5%", (0.5, 118), fontsize=9.5, color=INK,
                ha="center", va="top", fontweight="bold")
    a2.set_xticks(x2)
    a2.set_xticklabels(["2025", "2026"])
    a2.set_ylim(0, 126)
    a2.set_ylabel("Million acres planted")
    a2.set_title("(b)  What farmers actually planted", fontsize=10.5, color=INK,
                 fontweight="bold", pad=8)
    a2.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    a2.set_axisbelow(True)
    fig.tight_layout()
    save(fig, "ch06_fig_corn_soy.png")


# ============================== entry, market side only (Part 1: needs only Ch04)
def fig_entry_market():
    """Entry shifts market supply right and the price falls.

    Deliberately market-only and free of cost curves: this runs in Part 1, before any
    of the firm's cost machinery exists.  The firm-side version is fig_entry().
    """
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    q = np.linspace(0, 100, 300)
    ax.plot(q, 7.0 - 0.06 * q, color=BLUE, lw=2.4)
    ax.annotate("D", (7, 7.0 - 0.42), color=BLUE, fontsize=11, fontweight="bold",
                va="bottom", ha="left")
    y1 = 1.0 + 0.06 * q
    m1 = y1 <= 8.4
    ax.plot(q[m1], y1[m1], color=RED, lw=2.4)
    y2 = 1.0 + 0.06 * (q - 33.33)
    m2 = (y2 >= 0) & (y2 <= 8.4)
    ax.plot(q[m2], y2[m2], color=RED, lw=2.4, ls=(0, (5, 2)))
    ax.annotate("S$_1$", (13, 1.0 + 0.06 * 13), textcoords="offset points",
                xytext=(-4, 4), color=RED, fontsize=11, fontweight="bold",
                va="bottom", ha="right")
    ax.annotate("S$_2$", (86, 1.0 + 0.06 * (86 - 33.33)), color=RED, fontsize=11,
                fontweight="bold", va="bottom", ha="left")

    for qq, pp in ((50.0, 4.0), (66.67, 3.0)):
        ax.plot([0, qq], [pp, pp], color=GREY, lw=0.9, ls=":")
        ax.plot([qq, qq], [0, pp], color=GREY, lw=0.9, ls=":")
        ax.scatter([qq], [pp], s=48, color=INK, zorder=8)
    ax.annotate("", (26, 3.0), xytext=(26, 4.0),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.2))
    ax.annotate("more sellers arrive\n→ supply shifts right\n→ the price falls",
                (26, 8.25), fontsize=10, color=GREEN, ha="center", va="top",
                fontweight="bold")
    ax.annotate("and nothing went wrong —\nsomebody just copied him", (82, 1.15),
                fontsize=9.5, color=INK, ha="center", va="top")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 8.4)
    ax.set_yticks([0, 3, 4, 6, 8])
    ax.set_yticklabels(["$0", "$3", "$4", "$6", "$8"])
    ax.set_xticks([])
    ax.set_xlabel("Ploughed driveways, the whole market")
    ax.set_ylabel("Price")
    ax.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    ax.set_axisbelow(True)
    save(fig, "ch06_fig_entry_market.png")


# ============================================== McDonald's: where the money goes
# Every figure here is sourced on its slide. AUV: McDonald's 2025 FDD Item 19 (2024
# sales, ~12,023 domestic traditional FRANCHISED restaurants open >= 1 year).
# Fees: 2025 FDD Items 5 and 6.  All three are percentages of GROSS SALES.
MCD_AUV = 3_966_000.0
MCD_ROYALTY = 0.05      # new franchisees from 1 Jan 2024; 4% grandfathered
MCD_ADVERT = 0.04       # "not less than 4%"
MCD_RENT_ILLUS = 0.10   # illustrative: FDD Item 19 discloses 0.00%-33.33%


def fig_mcd_costs():
    """What comes off the top of one restaurant's gross sales, before anything else."""
    fig, ax = plt.subplots(figsize=(8.6, 2.5))
    segs = [("Rent to McDonald's", MCD_RENT_ILLUS, RED),
            ("Royalty", MCD_ROYALTY, DGOLD),
            ("Ad fund", MCD_ADVERT, BLUE),
            ("Everything else — food, crew, power,\nand whatever is left over", 0.81, "#E7EBF2")]
    left = 0.0
    for lab, frac, col in segs:
        ax.barh(0, frac, left=left, height=0.5, color=col,
                edgecolor="white", lw=1.6, zorder=3)
        if frac >= 0.04 and col != "#E7EBF2":
            ax.annotate(f"{frac*100:.0f}%", (left + frac / 2, 0), ha="center",
                        va="center", fontsize=11, fontweight="bold",
                        color="white", zorder=6)
        left += frac
    ax.annotate("Rent  10%\n(illustrative)", (MCD_RENT_ILLUS / 2, 0.34), ha="center",
                va="bottom", fontsize=9, color=RED, fontweight="bold")
    ax.annotate("Royalty 5%", (0.125, -0.34), ha="center", va="top", fontsize=9,
                color=DGOLD, fontweight="bold")
    ax.annotate("Ad fund 4%", (0.17, 0.34), ha="center", va="bottom", fontsize=9,
                color=BLUE, fontweight="bold")
    ax.annotate("81%  —  everything else: food, crew, power, and whatever is left over",
                (0.595, 0), ha="center", va="center", fontsize=11, color=INK,
                fontweight="bold", zorder=6)
    ax.annotate("$3,966,000 of gross sales in an average year", (0.5, 0.72),
                ha="center", va="center", fontsize=11.5, color=INK, fontweight="bold")
    ax.annotate("19% is gone before a single burger is paid for", (0.095, -0.66),
                ha="left", va="center", fontsize=10, color=RED, fontweight="bold")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(-0.95, 0.95)
    ax.set_yticks([])
    ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    save(fig, "ch06_fig_mcd_costs.png")


# ============================== McDonald's: menu prices against food-away-from-home
# McDonald's USA, "McD US Pricing Myths vs Facts", 29 May 2024 - national average
# prices, 2019 vs 2024.  Benchmark: 29% Food Away From Home inflation over the same
# window, McDonald's own comparison in the same document.
MCD_PRICES = [("Medium fries", 2.29, 3.29), ("Egg McMuffin", 3.49, 4.29),
              ("Big Mac", 4.39, 5.29), ("10-pc McNuggets", 4.39, 5.29),
              ("Quarter Pounder\nw/ cheese", 4.49, 5.39)]


def fig_mcd_prices():
    fig, ax = plt.subplots(figsize=(9.0, 2.5))
    labs = [r[0] for r in MCD_PRICES]
    pct = [(b - a) / a * 100 for _, a, b in MCD_PRICES]
    x = np.arange(len(labs))
    cols = [RED if v > 29 else DGOLD for v in pct]
    ax.bar(x, pct, width=0.6, color=cols, zorder=3)
    for xi, v, (lab, a, b) in zip(x, pct, MCD_PRICES):
        ax.annotate(f"+{v:.0f}%", (xi, v), textcoords="offset points", xytext=(0, 4),
                    ha="center", fontsize=10.5, fontweight="bold",
                    color=RED if v > 29 else DGOLD)
        ax.annotate(f"\\${a:.2f} → \\${b:.2f}", (xi, 1.5), ha="center", va="bottom",
                    fontsize=8.5, color="white", fontweight="bold", zorder=6)
    ax.axhline(29, color=BLUE, lw=2.0, ls=(0, (5, 2)), zorder=5)
    ax.annotate("food-away-from-home inflation over the same years:  +29%",
                (len(labs) - 0.55, 30.0), ha="right", va="bottom", fontsize=9.5,
                color=BLUE, fontweight="bold", zorder=7,
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none", alpha=0.95))
    ax.set_xticks(x)
    ax.set_xticklabels(labs, fontsize=9)
    ax.set_ylim(0, 52)
    ax.set_ylabel("Price change, 2019 → 2024", fontsize=9)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    ax.set_axisbelow(True)
    save(fig, "ch06_fig_mcd_prices.png")


# ================================ what long-run equilibrium looks like as a store count
# Every count is McDonald's own.  Panel (a) runs 2013-2025 because that is the span the
# company publishes as an unbroken annual series; 2006-2012 is not shown rather than
# interpolated, and the 2005 level is drawn as a reference line instead of a fake point.
#
# Sources, all retrieved 10 August 2026:
#   2005 .......... McDonald's Q4 2005 earnings release, 8-K Exhibit 99.2, 24 Jan 2006
#   2013-2017 ..... McDonald's Q4 earnings releases, 8-K Exhibit 99.2, 2015-2018
#   2018-2025 ..... McDonald's Forms 10-K, FY2020 / FY2022 / FY2024 / FY2025
#   populations ... each country's national statistical office; US Census Bureau
#                   Vintage 2025, resident population 340,003,797 at 1 July 2025
US_2005 = (2005, 13_727)
US_SERIES = [(2013, 14_278), (2014, 14_350), (2015, 14_259), (2016, 14_155),
             (2017, 14_036), (2018, 13_914), (2019, 13_846), (2020, 13_682),
             (2021, 13_438), (2022, 13_444), (2023, 13_457), (2024, 13_557),
             (2025, 13_706)]
# (country, restaurants YE2025 from "Restaurants by Market 2025", population, source year)
MCD_DENSITY = [("United States", 13_706, 340.003797), ("Australia", 1_092, 27.724744),
               ("Canada", 1_520, 41.472081), ("Japan", 3_025, 123.050),
               ("United Kingdom", 1_507, 69.487), ("Germany", 1_382, 83.500),
               ("South Korea", 401, 51.820)]

assert US_SERIES[-1][1] - US_2005[1] == -21          # twenty years, net minus twenty-one
assert max(c for _, c in US_SERIES) == 14_350        # the 2014 peak
assert min(c for _, c in US_SERIES) == 13_438        # the 2021 trough


def fig_mcd_equilibrium():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.1),
                                 gridspec_kw=dict(width_ratios=[1.22, 1.0]))

    yr = [y for y, _ in US_SERIES]
    ct = [c for _, c in US_SERIES]
    a1.axhline(US_2005[1], color=GREY, lw=1.4, ls=(0, (5, 3)), zorder=3)
    a1.annotate(f"the 2005 level: {US_2005[1]:,}", (2013.2, US_2005[1]),
                textcoords="offset points", xytext=(0, 6), fontsize=8.5, color=GREY,
                fontweight="bold", zorder=8)
    a1.plot(yr, ct, color=BLUE, lw=2.6, zorder=5)
    a1.scatter(yr, ct, s=16, color=BLUE, zorder=6)
    for x, y, lab, col, dy in [(2014, 14_350, "peak 14,350", RED, 12),
                               (2021, 13_438, "low 13,438", RED, -18),
                               (2025, 13_706, "13,706", GREEN, 10)]:
        a1.scatter([x], [y], s=42, color=col, zorder=8, edgecolor="white", lw=1.2)
        a1.annotate(lab, (x, y), textcoords="offset points", xytext=(0, dy),
                    ha="center", fontsize=9, color=col, fontweight="bold", zorder=9,
                    bbox=BOX)
    a1.set_ylim(13_150, 14_720)
    a1.set_xlim(2012.4, 2025.9)
    a1.set_xticks([2013, 2016, 2019, 2022, 2025])
    a1.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    a1.set_ylabel("US McDonald's restaurants")
    a1.set_title("(a)  Twenty years, and it ends where it started",
                 fontsize=10, color=INK, fontweight="bold", pad=8)
    a1.grid(True, axis="y", color="#EEEEEE", lw=0.7)
    a1.set_axisbelow(True)

    labs = [c for c, _, _ in MCD_DENSITY]
    dens = [n / pop for _, n, pop in MCD_DENSITY]
    ypos = np.arange(len(labs))[::-1]
    cols = [BLUE if c == "United States" else LGREY for c, _, _ in MCD_DENSITY]
    a2.barh(ypos, dens, height=0.62, color=cols, zorder=3)
    for y, v in zip(ypos, dens):
        a2.annotate(f"{v:.1f}", (v, y), textcoords="offset points", xytext=(4, 0),
                    va="center", fontsize=9, color=INK, fontweight="bold")
    a2.set_yticks(ypos)
    a2.set_yticklabels(labs, fontsize=9)
    a2.set_xlim(0, 48)
    a2.set_xticks([])
    a2.set_title("(b)  McDonald's per million people, 2025",
                 fontsize=10, color=INK, fontweight="bold", pad=8)
    for sp in ("top", "right", "bottom"):
        a2.spines[sp].set_visible(False)

    fig.tight_layout()
    save(fig, "ch06_fig_mcd_equilibrium.png")


if __name__ == "__main__":
    print("Chapter 6 figures →", OUT)
    for f in (fig_production, fig_marginal_product, fig_cost_curves,
              fig_market_and_firm, fig_profit_max, fig_three_prices,
              fig_loss_but_open, fig_shutdown, fig_supply_curve,
              fig_producer_surplus, fig_cost_anatomy, fig_ps_price_rise,
              fig_lrac, fig_entry, fig_exit, fig_lr_supply,
              fig_sellers_problem, fig_margin, fig_entry_market,
              fig_mcd_costs, fig_mcd_prices, fig_mcd_equilibrium,
              fig_supply_elasticity,
              fig_ethanol_plants, fig_ethanol_subsidy, fig_dallas_fed, fig_corn_soy):
        f()
    print("\nEvery number below comes from the two McDonald's tables:")
    print(f"  MC min      ${P_MCMIN:.2f} at Q={Q_MCMIN:.0f}")
    print(f"  min AVC     ${P_AVCMIN:.4f} at Q={Q_AVCMIN:.0f}   → the shutdown price")
    print(f"  min ATC     ${P_ATCMIN:.4f} at Q={Q_ATCMIN:.0f}   → the long-run price")
    print(f"  P=$4        Q={Q_STAR:.0f}, ATC=${ATC[7]:.2f}, TR=${P_STAR*Q_STAR:.0f}, "
          f"TC=${TC[8]:.0f}, profit=${PROFIT_STAR:.0f}")
    print(f"  P=$6        Q={Q_HIGH:.0f}, TR=${P_HIGH*Q_HIGH:.0f}, TC=${TC[9]:.0f}, "
          f"profit=${PROFIT_HIGH:.0f}")
    print(f"  P=$2        Q={Q_LOSS:.0f}, TR=${P_LOSS*Q_LOSS:.0f}, TC=${TC[7]:.0f}, "
          f"loss=${LOSS_OPEN:.0f}; covers ${COVERS:.0f} of the $100 overhead")
    print(f"  producer surplus at $4 = ${PS_STAR:.0f} = profit ${PROFIT_STAR:.0f} "
          f"+ fixed cost ${TFC:.0f}")
