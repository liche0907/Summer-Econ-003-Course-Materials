#!/usr/bin/env python3
"""
ECON 003 Ch05 (Consumers and Incentives) — exhibit figures.
UCR palette, Arial metrics (Liberation Sans). Blue = demand, red = the contrast side.

Every number below is derived from a stated functional form so labelled crossings
land on clean values (ground rules S6).

  Budget line      $50 j + $25 s = $300          -> intercepts 6 jeans / 12 sweaters
  Jeans demand     P = 125 - 25 Q                -> (1,100) (2,75) (3,50) (4,25)
  Market demand    P = 125 - 1.25 Q  (Q in mn)   -> at P=50, Q=60, CS = $2.25 bn
  Trout cards      P = 6 - Q                     -> midpoint (3,3) is unit elastic
  Solar lights     P = 9 - 0.5 Q  (Q in 100s)    -> (2,8) (6,6) (8,5) (10,4) (14,2)
  Greta            $10 cigs / $2 pizza, $150     -> 15 packs or 75 slices; tax -> 10 packs
"""
import math
import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

BLUE = "#003DA5"; GOLD = "#FFB81D"; DGOLD = "#B88300"
RED = "#CC3333"; GREEN = "#2E7D32"
INK = "#333333"; MID = "#666666"; LIGHT = "#999999"; RULE = "#DDDDDD"

plt.rcParams.update({
    "font.family": "Liberation Sans",
    "font.size": 11,
    "axes.edgecolor": INK, "axes.linewidth": 1.1,
    "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK, "ytick.color": INK,
    "xtick.labelsize": 10.5, "ytick.labelsize": 10.5,
    "figure.dpi": 200, "savefig.dpi": 200,
    "savefig.facecolor": "white", "figure.facecolor": "white",
})

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    p = os.path.join(OUT, name + ".png")
    fig.savefig(p, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("wrote", p)


def frame(ax, xlab, ylab, xlim, ylim):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xlabel(xlab, fontsize=11, labelpad=6)
    ax.set_ylabel(ylab, fontsize=11, labelpad=6)
    ax.tick_params(length=4, width=1.0)


def guide(ax, x, y, x0=0, y0=0, color=MID, lw=1.0):
    ax.plot([x0, x], [y, y], ls=(0, (4, 3)), lw=lw, color=color, zorder=1)
    ax.plot([x, x], [y0, y], ls=(0, (4, 3)), lw=lw, color=color, zorder=1)


def dot(ax, x, y, color="#444444", s=55, z=6):
    ax.plot([x], [y], "o", ms=math.sqrt(s), color=color, zorder=z,
            mec="white", mew=1.2)


def arrow(ax, xy0, xy1, color=INK, lw=1.8):
    ax.annotate("", xy=xy1, xytext=xy0,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=16))


# ======================================================= Exhibit 5.1 budget set
def _budget_axes(ax, xmax=8, ymax=14):
    frame(ax, "Quantity of jeans", "Quantity of sweaters", (0, xmax), (0, ymax))
    ax.set_xticks(range(0, xmax + 1, 2))
    ax.set_yticks(range(0, ymax + 1, 2))


def ex51_budget(shade=True, name="ex51_budget_set"):
    fig, ax = plt.subplots(figsize=(6.0, 4.1))
    j = np.array([0, 6]); s = 12 - 2 * j
    if shade:
        ax.add_patch(Polygon([(0, 0), (0, 12), (6, 0)], closed=True,
                             facecolor="#E8EFFA", edgecolor="none", zorder=0))
        ax.text(1.45, 3.1, "BUDGET SET", fontsize=11.5, fontweight="bold",
                color=BLUE, ha="center")
    ax.plot(j, s, color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    pts = [("A", 0, 12), ("B", 2, 8), ("C", 4, 4), ("D", 6, 0)]
    for lab, x, y in pts:
        dot(ax, x, y, color=BLUE)
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=(9, 8),
                    fontsize=12, fontweight="bold", color=BLUE)
    ax.text(5.9, 10.6, "$50 j  +  $25 s  =  $300", fontsize=12, fontweight="bold",
            color=INK, ha="right")
    ax.text(5.9, 9.6, "budget constraint", fontsize=10.5, color=MID, ha="right")
    _budget_axes(ax)
    save(fig, name)


def ex51_regions():
    """The three regions: on / inside / outside the constraint."""
    fig, ax = plt.subplots(figsize=(6.0, 4.1))
    ax.add_patch(Polygon([(0, 0), (0, 12), (6, 0)], closed=True,
                         facecolor="#E8EFFA", edgecolor="none", zorder=0))
    ax.plot([0, 6], [12, 0], color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    dot(ax, 4, 4, color=BLUE); ax.annotate("on the line\nspends exactly $300",
        (4, 4), textcoords="offset points", xytext=(12, 10), fontsize=10,
        fontweight="bold", color=BLUE)
    dot(ax, 1.6, 3.0, color=GREEN); ax.annotate("inside\naffordable, but\n$300 not all spent",
        (1.6, 3.0), textcoords="offset points", xytext=(10, -34), fontsize=10,
        fontweight="bold", color=GREEN)
    dot(ax, 5.2, 8.5, color=RED); ax.annotate("outside\nunaffordable",
        (5.2, 8.5), textcoords="offset points", xytext=(-6, 14), fontsize=10,
        fontweight="bold", color=RED, ha="center")
    _budget_axes(ax)
    save(fig, "ex51_regions")


def ex53_pivot_in():
    """Price of sweaters $25 -> $50. Pivots on the jeans axis."""
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    ax.plot([0, 6], [12, 0], color=LIGHT, lw=2.4, ls=(0, (5, 3)), zorder=2)
    ax.plot([0, 6], [6, 0], color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    arrow(ax, (2.6, 7.0), (1.9, 4.2), color=RED)
    ax.text(3.2, 10.6, r"$P_{s}$:  \$25 → \$50", fontsize=12, fontweight="bold", color=RED)
    ax.text(4.9, 2.4, "old", fontsize=10.5, color=LIGHT, fontweight="bold")
    ax.text(2.55, 1.05, "new", fontsize=10.5, color=BLUE, fontweight="bold")
    _budget_axes(ax)
    save(fig, "ex53_pivot_in")


def ex54_pivot_out():
    """Price of jeans $50 -> $25. Pivots on the sweater axis."""
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    ax.plot([0, 6], [12, 0], color=LIGHT, lw=2.4, ls=(0, (5, 3)), zorder=2)
    ax.plot([0, 12], [12, 0], color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    arrow(ax, (4.0, 4.6), (7.4, 5.2), color=GREEN)
    ax.text(3.0, 10.6, r"$P_{j}$:  \$50 → \$25", fontsize=12, fontweight="bold", color=GREEN)
    _budget_axes(ax, xmax=13)
    ax.set_xticks(range(0, 14, 2))
    save(fig, "ex54_pivot_out")


def ex55_shift_out():
    """Income $300 -> $600. Parallel shift; slope unchanged."""
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    ax.plot([0, 6], [12, 0], color=LIGHT, lw=2.4, ls=(0, (5, 3)), zorder=2)
    ax.plot([0, 12], [24, 0], color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    arrow(ax, (4.2, 3.8), (7.6, 8.6), color=GREEN)
    ax.text(4.6, 21.4, "income:  $300 → $600", fontsize=12, fontweight="bold", color=GREEN)
    ax.text(6.4, 15.0, "same slope —\nprices did not change", fontsize=10.5,
            color=MID, fontweight="bold")
    _budget_axes(ax, xmax=13, ymax=26)
    ax.set_xticks(range(0, 14, 2)); ax.set_yticks(range(0, 27, 4))
    save(fig, "ex55_shift_out")


# ================================================= Exhibit 5.6 demand for jeans
JEANS = [(1, 100), (2, 75), (3, 50), (4, 25)]


def ex56_demand_jeans():
    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    q = np.array([qq for qq, _ in JEANS]); p = np.array([pp for _, pp in JEANS])
    ax.plot([0.0, 5.0], [125, 0], color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    for qq, pp in JEANS:
        guide(ax, qq, pp, color=RULE)
        dot(ax, qq, pp, color=BLUE)
    frame(ax, "Quantity of jeans", "Price  ($ per pair)", (0, 5.2), (0, 130))
    ax.set_xticks([0, 1, 2, 3, 4, 5]); ax.set_yticks([0, 25, 50, 75, 100, 125])
    ax.text(4.55, 78, "D", fontsize=15, fontweight="bold", color=BLUE)
    save(fig, "ex56_demand_jeans")


def ex57_cs_individual():
    """Consumer surplus for one buyer at P = $50: $50 + $25 = $75."""
    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    ax.plot([0.0, 5.0], [125, 0], color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    ax.plot([0, 3.35], [50, 50], ls=(0, (4, 3)), lw=1.4, color=INK, zorder=2)
    for qq, pp in JEANS:
        dot(ax, qq, pp, color=BLUE)
    for qq, pp in [(1, 100), (2, 75)]:
        ax.add_patch(Rectangle((qq - 0.085, 50), 0.17, pp - 50, facecolor=GOLD,
                               edgecolor=DGOLD, lw=1.0, zorder=4))
        ax.annotate(f"${pp - 50}", (qq, (pp + 50) / 2), fontsize=11.5,
                    fontweight="bold", color=DGOLD, ha="left",
                    textcoords="offset points", xytext=(9, -4), zorder=5)
    ax.text(3.45, 53, r"$P_{market}$ = \$50", fontsize=11, fontweight="bold", color=INK)
    ax.text(2.55, 108, "consumer surplus\n$50 + $25 = $75", fontsize=11.5,
            fontweight="bold", color=DGOLD)
    frame(ax, "Quantity of jeans", "Price  ($ per pair)", (0, 5.2), (0, 130))
    ax.set_xticks([0, 1, 2, 3, 4, 5]); ax.set_yticks([0, 25, 50, 75, 100, 125])
    save(fig, "ex57_cs_individual")


def _market_axes(ax):
    frame(ax, "Quantity sold  (millions of pairs)", "Price  ($ per pair)",
          (0, 85), (0, 132))
    ax.set_xticks([0, 20, 40, 60, 80]); ax.set_yticks([0, 25, 50, 75, 100, 125])


def ex58_cs_market():
    """P = 125 - 1.25Q. At P = 50, Q = 60 -> CS = 0.5 x 60m x $75 = $2.25 bn."""
    fig, ax = plt.subplots(figsize=(6.0, 4.1))
    ax.add_patch(Polygon([(0, 50), (0, 125), (60, 50)], closed=True,
                         facecolor=GOLD, alpha=0.42, edgecolor=DGOLD, lw=1.2, zorder=2))
    ax.plot([0, 80], [125, 25], color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    ax.plot([0, 60], [50, 50], ls=(0, (4, 3)), lw=1.4, color=INK, zorder=3)
    ax.plot([60, 60], [0, 50], ls=(0, (4, 3)), lw=1.4, color=INK, zorder=3)
    dot(ax, 60, 50, color=INK)
    ax.text(13, 74, "CONSUMER\nSURPLUS", fontsize=12, fontweight="bold", color=DGOLD)
    ax.text(11, 61, "½ × 60m × $75", fontsize=10.5, color=DGOLD, fontweight="bold")
    ax.text(62, 53, r"$P_{market}$ = \$50", fontsize=11, fontweight="bold", color=INK)
    ax.text(73, 33, "$D_{market}$", fontsize=13, fontweight="bold", color=BLUE)
    _market_axes(ax)
    save(fig, "ex58_cs_market")


def ex59_cs_price_change():
    """P rises $50 -> $75: Q 60m -> 40m, CS $2.25bn -> $1.00bn, $1.25bn lost."""
    fig, ax = plt.subplots(figsize=(6.2, 4.1))
    ax.add_patch(Polygon([(0, 75), (0, 125), (40, 75)], closed=True,
                         facecolor=GOLD, alpha=0.42, edgecolor=DGOLD, lw=1.2, zorder=3))
    ax.add_patch(Polygon([(0, 50), (0, 75), (40, 75), (60, 50)], closed=True,
                         facecolor=RED, alpha=0.20, edgecolor=RED, lw=1.2, zorder=2))
    ax.plot([0, 80], [125, 25], color=BLUE, lw=3.0, solid_capstyle="round", zorder=4)
    for pp, qq in [(50, 60), (75, 40)]:
        ax.plot([0, qq], [pp, pp], ls=(0, (4, 3)), lw=1.2, color=INK, zorder=3)
        dot(ax, qq, pp, color=INK, s=42)
    arrow(ax, (-6.5, 50), (-6.5, 75), color=RED)
    ax.text(4, 88, "CS now\n$1.00 bn", fontsize=10.5, fontweight="bold", color=DGOLD)
    ax.text(16, 57, "LOST  $1.25 bn", fontsize=11.5, fontweight="bold", color=RED)
    ax.text(43, 79, "now $75", fontsize=11, fontweight="bold", color=INK)
    ax.text(46, 41, "was $50", fontsize=11, fontweight="bold", color=MID)
    ax.text(73, 33, "$D_{market}$", fontsize=13, fontweight="bold", color=BLUE)
    _market_axes(ax)
    ax.set_xlim(-11, 85)
    save(fig, "ex59_cs_price_change")


# ============================================ Exhibit 5.10 smoking-incentive trial
def ex510_smoking():
    """Volpp et al., NEJM 2009. Published rates, not Pearson's redrawn bars."""
    fig, ax = plt.subplots(figsize=(6.0, 3.9))
    labels = ["Incentive group\n(up to $750)", "Information only\n(control)"]
    vals = [14.7, 5.0]
    late = [9.4, 3.6]
    x = np.arange(2); w = 0.34
    b1 = ax.bar(x - w / 2, vals, w, color=BLUE, zorder=3, label="at 9 or 12 months")
    b2 = ax.bar(x + w / 2, late, w, color=GOLD, edgecolor=DGOLD, lw=0.8, zorder=3,
                label="at 15 or 18 months")
    for bars in (b1, b2):
        for r in bars:
            ax.annotate(f"{r.get_height():.1f}%", (r.get_x() + r.get_width() / 2,
                        r.get_height()), textcoords="offset points", xytext=(0, 4),
                        ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylabel("Quit rate  (%)", fontsize=11, labelpad=6)
    ax.set_ylim(0, 18)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, fontsize=10, loc="upper right")
    ax.grid(axis="y", color=RULE, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    save(fig, "ex510_smoking")


# =============================== Exhibit 5.11 elasticity varies along a straight line
def ex511_trout():
    """P = 6 - Q. Midpoint (3,3) is unit elastic."""
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.plot([0, 6], [6, 0], color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    ax.plot([0, 3], [6, 3], color=RED, lw=4.4, solid_capstyle="round", zorder=4, alpha=0.9)
    for lab, x, y, c in [("A", 1, 5, RED), ("", 3, 3, INK), ("B", 5, 1, GREEN)]:
        dot(ax, x, y, color=c)
        if lab:
            ax.annotate(lab, (x, y), textcoords="offset points", xytext=(10, 8),
                        fontsize=13, fontweight="bold", color=c)
    ax.plot([3, 6], [3, 0], color=GREEN, lw=4.4, solid_capstyle="round", zorder=4, alpha=0.9)
    ax.annotate("$E_D$ > 1  elastic", (1.4, 4.7), fontsize=11.5, fontweight="bold",
                color=RED, textcoords="offset points", xytext=(14, 12))
    ax.annotate("$E_D$ = 1", (3, 3), fontsize=11.5, fontweight="bold", color=INK,
                textcoords="offset points", xytext=(12, 12))
    ax.annotate("$E_D$ < 1  inelastic", (4.2, 1.8), fontsize=11.5, fontweight="bold",
                color=GREEN, textcoords="offset points", xytext=(0, 12))
    frame(ax, "Quantity of cards", "Price  ($)", (0, 7), (0, 7))
    ax.set_xticks(range(0, 8)); ax.set_yticks(range(0, 8))
    save(fig, "ex511_trout")


def tr_curve():
    """Total revenue along P = 6 - Q, wide format. Peaks at the unit-elastic midpoint."""
    fig, ax = plt.subplots(figsize=(6.4, 2.05))
    q = np.linspace(0, 6, 300)
    ax.fill_between(q[q <= 3], 0, (q * (6 - q))[q <= 3], color=RED, alpha=0.13)
    ax.fill_between(q[q >= 3], 0, (q * (6 - q))[q >= 3], color=GREEN, alpha=0.13)
    ax.plot(q, q * (6 - q), color=DGOLD, lw=3.0, zorder=3, solid_capstyle="round")
    ax.axvline(3, color=MID, lw=1.1, ls=(0, (4, 3)), zorder=1)
    dot(ax, 3, 9, color=DGOLD)
    ax.annotate("revenue peaks where $E_D$ = 1", (3, 9), fontsize=10.5,
                fontweight="bold", color=DGOLD, ha="center",
                textcoords="offset points", xytext=(0, 9))
    ax.text(1.3, 2.2, "elastic\nhalf", fontsize=10, fontweight="bold",
            color=RED, ha="center")
    ax.text(4.7, 2.2, "inelastic\nhalf", fontsize=10, fontweight="bold",
            color=GREEN, ha="center")
    ax.set_ylabel("Total revenue ($)", fontsize=10)
    ax.set_xlabel("Quantity", fontsize=10)
    ax.set_ylim(0, 12.6); ax.set_yticks([0, 3, 6, 9])
    ax.set_xlim(0, 6.2); ax.set_xticks(range(0, 7))
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=9.5)
    save(fig, "tr_curve")


# ========================================================= solar-light practice
def _solar(ax, marks=()):
    q = np.array([0, 18]); p = 9 - 0.5 * q
    ax.plot(q, p, color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    for qq, pp, col in marks:
        guide(ax, qq, pp, color=RULE, lw=1.2)
        dot(ax, qq, pp, color=col)
        ax.annotate(f"(${pp:g}, {qq:g})", (qq, pp), fontsize=10.5, fontweight="bold",
                    color=col, textcoords="offset points", xytext=(9, 8))
    frame(ax, "Quantity  (hundreds of lights)", "Price  ($)", (0, 16), (0, 9.6))
    ax.set_xticks(range(0, 17, 2)); ax.set_yticks(range(0, 10, 1))
    ax.text(14.6, 2.5, "D", fontsize=15, fontweight="bold", color=BLUE)


def solar(name, marks=()):
    fig, ax = plt.subplots(figsize=(5.9, 3.9))
    _solar(ax, marks)
    save(fig, name)


# =============================================== Exhibit 5.12 the extreme cases
def ex512_extremes():
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.5))
    titles = ["Perfectly elastic\n$E_D$ = ∞", "Unit elastic\n$E_D$ = 1",
              "Perfectly inelastic\n$E_D$ = 0"]
    for ax, t in zip(axes, titles):
        frame(ax, "Quantity", "Price ($)", (0, 8), (0, 7))
        ax.set_xticks(range(0, 9, 2)); ax.set_yticks(range(0, 8, 2))
        ax.set_title(t, fontsize=11.5, fontweight="bold", color=BLUE, pad=10)
    axes[0].plot([0, 8], [3, 3], color=BLUE, lw=3.0, zorder=3)
    axes[0].text(6.4, 3.35, "D", fontsize=14, fontweight="bold", color=BLUE)
    q = np.linspace(0.9, 7.6, 200)
    axes[1].plot(q, 6.0 / q, color=BLUE, lw=3.0, zorder=3)
    for qq, pp in [(2, 3), (3, 2)]:
        guide(axes[1], qq, pp, color=RULE, lw=1.2)
        dot(axes[1], qq, pp, color=BLUE, s=40)
    axes[1].text(5.6, 1.55, "D", fontsize=14, fontweight="bold", color=BLUE)
    axes[2].plot([5, 5], [0, 7], color=BLUE, lw=3.0, zorder=3)
    axes[2].text(5.3, 5.6, "D", fontsize=14, fontweight="bold", color=BLUE)
    save(fig, "ex512_extremes")


# ============================================ total revenue: elastic vs inelastic
def tr_panels():
    """Same $1 price rise on an inelastic and an elastic curve, revenue boxes drawn."""
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 3.9))
    # Both curves pass through ($4, 9). A $1 rise to $5 then moves quantity by
    # -b, so revenue goes 36 -> 5*(9-b).  b = 1 : 40 (up).  b = 4 : 25 (down).
    setups = [
        ("INELASTIC demand", axes[0], 1.0, GREEN, 8,
         "revenue RISES\n$4 × 9 = $36   →   $5 × 8 = $40",
         "|arc E| = 0.53"),
        ("ELASTIC demand", axes[1], 4.0, RED, 5,
         "revenue FALLS\n$4 × 9 = $36   →   $5 × 5 = $25",
         "|arc E| = 2.57"),
    ]
    for name, ax, b, col, q_hi, note, elab in setups:
        # Qd = a - b P  through (P=4, Q=9)  ->  a = 9 + 4b
        a = 9 + 4 * b
        ax.add_patch(Rectangle((0, 0), 9, 4, facecolor=LIGHT, alpha=0.30,
                               edgecolor=MID, lw=1.0, zorder=1))
        ax.add_patch(Rectangle((0, 0), q_hi, 5, facecolor=col, alpha=0.22,
                               edgecolor=col, lw=1.6, zorder=2))
        p_top = a / b                      # price at which Q = 0
        ax.plot([0, a], [p_top, 0], color=BLUE, lw=3.0,
                solid_capstyle="round", zorder=4)
        for pp, q_ in [(4, 9), (5, q_hi)]:
            ax.plot([0, q_], [pp, pp], ls=(0, (3, 3)), lw=1.0, color=INK, zorder=3)
            ax.plot([q_, q_], [0, pp], ls=(0, (3, 3)), lw=1.0, color=INK, zorder=3)
            dot(ax, q_, pp, color=INK, s=36)
        ax.set_title(name, fontsize=12, fontweight="bold", color=col, pad=10)
        ax.text(7.2, 11.4, note, fontsize=10.5, fontweight="bold", color=col, ha="center")
        ax.text(7.2, 9.9, elab, fontsize=10, color=MID, ha="center", fontweight="bold")
        ax.text(2.4, 2.0, "$36", fontsize=11.5, fontweight="bold", color=MID)
        frame(ax, "Quantity", "Price  ($)", (0, 14), (0, 13.4))
        ax.set_xticks(range(0, 15, 2)); ax.set_yticks(range(0, 13, 2))
    save(fig, "tr_panels")


# ================================================= Greta's budget constraint (EBE)
def greta():
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.plot([0, 75], [15, 0], color=LIGHT, lw=2.6, ls=(0, (5, 3)), zorder=2)
    ax.plot([0, 75], [10, 0], color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    dot(ax, 0, 15, color=LIGHT); dot(ax, 0, 10, color=BLUE); dot(ax, 75, 0, color=INK)
    arrow(ax, (24, 10.2), (24, 7.2), color=RED)
    ax.text(30, 13.4, "$5 tax:  pack $10 → $15", fontsize=12, fontweight="bold", color=RED)
    ax.text(46, 6.0, "before tax", fontsize=10.5, color=MID, fontweight="bold")
    ax.text(30, 3.0, "after tax", fontsize=10.5, color=BLUE, fontweight="bold")
    frame(ax, "Slices of pizza  ($2 each)", "Packs of cigarettes", (0, 82), (0, 17))
    ax.set_xticks(range(0, 81, 10)); ax.set_yticks(range(0, 18, 2))
    save(fig, "greta_budget")


# =========================================== clip figures: Kranks and Entourage
# Round numbers throughout. NOTHING here is quoted from either film - the deck supplies
# its own figures so the arithmetic closes, and the notes say so explicitly.

def kranks_ham():
    """Two demands for the same meat. Left: ham in general, substitutes everywhere.
    Right: THE last hickory honey ham on Christmas Eve, quantity fixed at 1.

    Price runs $20 -> $50 and quantity does not move, so %dQ = 0 and E = 0 exactly:
    perfectly inelastic. That is the definitional payoff.
    """
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.6, 3.9))

    q = np.array([0, 9])
    a1.plot(q, 55 - 5 * q, color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    for pp, qq, c in [(50, 1, MID), (20, 7, MID)]:
        guide(a1, qq, pp, color=RULE, lw=1.2)
        dot(a1, qq, pp, color=c, s=42)
    a1.annotate("$50 → buys 1", (1, 50), fontsize=10.5, fontweight="bold", color=INK,
                textcoords="offset points", xytext=(11, -3))
    a1.annotate("$20 → buys 7", (7, 20), fontsize=10.5, fontweight="bold", color=INK,
                textcoords="offset points", xytext=(-4, 12))
    a1.set_title("Ham, in general", fontsize=12.5, fontweight="bold", color=BLUE, pad=10)
    a1.text(6.5, 44, "turkey, roast, another store,\nanother day — substitutes\neverywhere",
            fontsize=9.5, color=MID, ha="center")
    frame(a1, "Quantity of hams", "Price  ($)", (0, 9.5), (0, 60))
    a1.set_xticks(range(0, 10, 2)); a1.set_yticks([0, 20, 40, 60])

    a2.plot([1, 1], [0, 60], color=RED, lw=3.4, solid_capstyle="round", zorder=3)
    for pp in (20, 50):
        a2.plot([0, 1], [pp, pp], ls=(0, (4, 3)), lw=1.2, color=MID, zorder=2)
        dot(a2, 1, pp, color=RED, s=42)
    arrow(a2, (0.42, 21.5), (0.42, 48.5), color=RED)
    a2.annotate("sticker  $20", (1, 20), fontsize=10.5, fontweight="bold", color=MID,
                textcoords="offset points", xytext=(10, -4))
    a2.annotate("she pays  $50", (1, 50), fontsize=10.5, fontweight="bold", color=RED,
                textcoords="offset points", xytext=(10, -4))
    a2.text(4.9, 34, "price × 2.5\nquantity unchanged\n\n" + r"$E_D$ = 0 ÷ 150% = 0",
            fontsize=11, fontweight="bold", color=RED, ha="center")
    a2.set_title("THE last hickory honey ham, Christmas Eve",
                 fontsize=12.5, fontweight="bold", color=RED, pad=10)
    frame(a2, "Quantity of hams", "Price  ($)", (0, 9.5), (0, 60))
    a2.set_xticks(range(0, 10, 2)); a2.set_yticks([0, 20, 40, 60])
    save(fig, "kranks_ham")


def entourage_bargain():
    """The bargaining range. Whoever has the worse outside option - the more inelastic
    side - gives up more of it. Illustrative round numbers, not the film's."""
    fig, ax = plt.subplots(figsize=(6.6, 4.1))

    ax.add_patch(Rectangle((0.62, 2600), 0.76, 800, facecolor=GOLD, alpha=0.30,
                           edgecolor=DGOLD, lw=1.3, zorder=2))
    ax.text(1.12, 3010, "ZONE OF POSSIBLE\nAGREEMENT", fontsize=10.5, fontweight="bold",
            color=DGOLD, ha="center", va="center")

    marks = [
        (2400, "his stated budget", LIGHT),
        (2600, "her walk-away", GREEN),
        (3400, "his true maximum", BLUE),
    ]
    for val, lab, col in marks:
        ax.plot([0.62, 1.38], [val, val], color=col, lw=2.0,
                ls=(0, (5, 3)) if col == LIGHT else "-", zorder=3)
        ax.annotate(f"${val:,}   {lab}", (1.44, val), fontsize=10.5, fontweight="bold",
                    color=col, va="center")

    ax.plot([0.62, 1.38], [3200, 3200], color=RED, lw=3.4, zorder=4)
    ax.annotate("$3,200   the deal", (1.44, 3200), fontsize=11.5, fontweight="bold",
                color=RED, va="center")
    arrow(ax, (0.78, 2630), (0.78, 3180), color=GREEN)
    ax.text(0.55, 2900, "she takes\n\\$600 of\nthe \\$800", fontsize=9.5,
            fontweight="bold", color=GREEN, ha="right", va="center")

    ax.set_xlim(0.05, 3.05)
    ax.set_ylim(2280, 3600)
    ticks = [2400, 2600, 2800, 3000, 3200, 3400, 3600]
    ax.set_yticks(ticks)
    ax.set_yticklabels([f"${v:,}" for v in ticks])
    ax.set_ylabel("Monthly rent", fontsize=11, labelpad=6)
    ax.set_xticks([])
    for sp in ("top", "right", "bottom"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=4, width=1.0, labelsize=10)
    save(fig, "entourage_bargain")


if __name__ == "__main__":
    ex51_budget()
    ex51_regions()
    ex53_pivot_in()
    ex54_pivot_out()
    ex55_shift_out()
    ex56_demand_jeans()
    ex57_cs_individual()
    ex58_cs_market()
    ex59_cs_price_change()
    ex510_smoking()
    ex511_trout()
    tr_curve()
    ex512_extremes()
    tr_panels()
    greta()
    solar("solar_base")
    solar("solar_p8_p4", [(2, 8, RED), (10, 4, RED)])
    solar("solar_p5_p2", [(8, 5, RED), (14, 2, RED)])
    solar("solar_p6_p8", [(6, 6, RED), (2, 8, RED)])
    kranks_ham()
    entourage_bargain()
    print("\nall figures written to", OUT)
