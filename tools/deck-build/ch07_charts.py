#!/usr/bin/env python3
"""ECON 003 - Chapter 7 (Perfect Competition and the Invisible Hand) figures.

Their photographs, our charts.  matplotlib, UCR palette, Liberation Sans (Arial metrics).

EVERY NUMBER IS DERIVED, NOT DRAWN TO LOOK RIGHT.  Three primitives generate the whole
chapter:

  Part 1  the seven-buyer / seven-seller iPhone market, reservation values 10..70
  Part 2  two plants with quadratic total costs
              TC_old(Q) = 100,000 + 0.00025 Q^2      MC_old = 0.0005 Q
              TC_new(Q) = 125,000 + 0.0001  Q^2      MC_new = 0.0002 Q
          chosen so that at the market price P = $10 the publisher's own headline
          figures fall out exactly:  old plant Q = 20,000, TC = $200,000, profit $0;
          new plant Q = 50,000, ATC = $7.50, TC = $375,000, profit $125,000.
  Part 3  one firm technology  TC(q) = 240 + 0.15 q^2,  min ATC = $12 at q = 40
  Part 4  bottled water  S: Qs = 2P,  D1: Qd = 90 - P,  D2: Qd = 120 - P
          Uber       S: Qs = P,   D1: Qd = 30 - P,  D2: Qd = 60 - 2P

WHERE THE PUBLISHER'S EXHIBIT 7.7 CANNOT BE REPRODUCED, AND WHY.  Exhibit 7.7 panel (b)
says that with all 70,000 units forced into the new plant, ATC = $22.50 (so TC =
$1,575,000) and the marginal cost of the 70,000th unit is about $30.  Those two claims
cannot both come from one cost curve.  If MC is $10 at 50,000 and rises to $30 at
70,000, then the extra 20,000 units cost at most 20,000 x $30 = $600,000, so
TC(70,000) <= $975,000 and ATC <= $13.93 - nowhere near $22.50.  Formally: with
TC = F + AQ - CQ^2 + BQ^3 and the four conditions MC(50k)=10, ATC(50k)=7.50,
MC(70k)=30, ATC(70k)=22.50 the cubic solves to B < 0, i.e. marginal cost eventually
falls.  No well-behaved cost function generates the publisher's numbers.

So this file derives the honest version from the quadratic above and reports it:
producing all 70,000 at the new plant costs $615,000 against $575,000 for the efficient
split, an ATC of $8.79 and a marginal cost of $14 on the last unit.  The CEO's order
costs the firm $40,000 - AFTER crediting the $100,000 of fixed cost saved by closing the
old plant.  The story is the publisher's; only the arithmetic is repaired.

Run:  python3 ch07_charts.py [outdir]
"""
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

# ----------------------------------------------------------------- house style
BLUE = "#003DA5"      # demand, marginal revenue, price lines
RED = "#CC3333"       # supply, marginal cost
GREEN = "#2E7D32"     # average total cost, the "benefit" side of a contrast
DGOLD = "#B88300"     # secondary cost curve, highlights
GOLD = "#FFB81D"
INK = "#333333"
GREY = "#666666"
LGREY = "#BBBBBB"
TINT_GREEN = "#E4F0E4"
TINT_RED = "#F7DEDE"
TINT_BLUE = "#DCE6F5"
TINT_GOLD = "#FBEFCF"

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


def thousands(x, _=None):
    return f"{x:,.0f}"


# =========================================================== PART 1 primitives
BUYERS = [("Madeline", 70), ("Katie", 60), ("Sean", 50), ("Dave", 40),
          ("Ian", 30), ("Kim", 20), ("Ty", 10)]
SELLERS = [("Tom", 10), ("Mary", 20), ("Jeff", 30), ("Phil", 40),
           ("Adam", 50), ("Matt", 60), ("Fiona", 70)]
P_STAR, Q_STAR = 40, 4


def _steps(values):
    """Step coordinates for a staircase curve: unit k is offered at values[k-1]."""
    xs, ys = [], []
    for i, v in enumerate(values):
        xs += [i, i + 1]
        ys += [v, v]
    return xs, ys


def _stair_axes(ax, names=True, xmax=7.6, label_x=None):
    bx, by = _steps([v for _, v in BUYERS])
    sx, sy = _steps([v for _, v in SELLERS])
    ax.step(bx, by, where="post", color=BLUE, lw=2.4, solid_joinstyle="miter")
    ax.plot(bx, by, color=BLUE, lw=2.4, drawstyle="steps-post")
    ax.plot(sx, sy, color=RED, lw=2.4, drawstyle="steps-post")
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, 80)
    ax.set_xticks(range(0, 8))
    ax.set_yticks(range(0, 81, 10))
    ax.set_yticklabels([f"${v}" for v in range(0, 81, 10)])
    ax.set_xlabel("Quantity (iPhones)")
    ax.set_ylabel("Price")
    if names:
        for i, (n, v) in enumerate(BUYERS):
            ax.annotate(n, (i + 0.5, v), xytext=(0, 5), textcoords="offset points",
                        ha="center", fontsize=8.5, color=BLUE)
        for i, (n, v) in enumerate(SELLERS):
            ax.annotate(n, (i + 0.5, v), xytext=(0, -13), textcoords="offset points",
                        ha="center", fontsize=8.5, color=RED)
    lx = label_x if label_x is not None else xmax - 0.05
    ax.annotate("Demand", (lx, 6), color=BLUE, fontsize=11, fontweight="bold",
                ha="right", va="center")
    ax.annotate("Supply", (lx, 76), color=RED, fontsize=11, fontweight="bold",
                ha="right", va="center")


def _surplus_blocks(ax, upto, price=P_STAR):
    """Shade the CS block above the price and the PS block below it, unit by unit."""
    for i in range(upto):
        v = BUYERS[i][1]
        if v > price:
            ax.add_patch(Rectangle((i, price), 1, v - price, facecolor=TINT_BLUE,
                                   edgecolor=BLUE, lw=0.6, zorder=0))
        c = SELLERS[i][1]
        if c < price:
            ax.add_patch(Rectangle((i, c), 1, price - c, facecolor=TINT_RED,
                                   edgecolor=RED, lw=0.6, zorder=0))


# ---------------------------------------------------------------- 1. staircase
fig, ax = plt.subplots(figsize=(8.9, 3.7))
_stair_axes(ax)
ax.plot([Q_STAR], [P_STAR], "o", color=INK, ms=7, zorder=5)
ax.annotate(r"Equilibrium: $\$$40, 4 iPhones", (Q_STAR, P_STAR),
            xytext=(34, -36), textcoords="offset points", fontsize=11,
            fontweight="bold", color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
save(fig, "ch07_fig_staircase.png")

# ------------------------------------------------------- 2. surplus at Q = 4
fig, ax = plt.subplots(figsize=(8.9, 3.7))
_surplus_blocks(ax, 4)
_stair_axes(ax, names=False, xmax=9.9, label_x=7.15)
ax.axhline(P_STAR, color=INK, lw=1.1, ls="--")
ax.annotate(r"$P = \$$40", (0.08, 41.5), fontsize=10.5, color=INK, fontweight="bold")
ax.annotate("Consumer surplus\n\\$30 + \\$20 + \\$10 + \\$0 = \\$60", (7.45, 74),
            fontsize=10.5, color=BLUE, fontweight="bold", va="top")
ax.annotate("Producer surplus\n\\$30 + \\$20 + \\$10 + \\$0 = \\$60", (7.45, 30),
            fontsize=10.5, color=RED, fontweight="bold", va="top")
ax.annotate(r"Social surplus = \$120", (7.45, 50), fontsize=12, color=INK,
            fontweight="bold")
save(fig, "ch07_fig_surplus.png")

# ------------------------------------------------ 3. three panels (Exhibit 7.3)
CASES = [("(a) Cap of 2 iPhones", 2), ("(b) Left alone", 4), ("(c) Floor of 5 iPhones", 5)]
fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.2))
for ax, (label, q) in zip(axes, CASES):
    _surplus_blocks(ax, min(q, 4))
    if q == 5:  # the forced fifth trade destroys value: cost 50, benefit 30
        ax.add_patch(Rectangle((4, 30), 1, 20, facecolor=TINT_GOLD, edgecolor=DGOLD,
                               lw=1.0, hatch="///", zorder=1))
        ax.annotate("Loss\n\\$20", (4.5, 40), ha="center", va="center", fontsize=9.5,
                    color=DGOLD, fontweight="bold")
    _stair_axes(ax, names=False, xmax=7.2)
    ax.axhline(P_STAR, color=INK, lw=0.9, ls="--")
    ax.axvline(q, color=INK, lw=1.4)
    ss = {2: 100, 4: 120, 5: 100}[q]
    ax.set_title(f"{label}\nSocial surplus = ${ss}", fontsize=10.5, color=INK,
                 fontweight="bold", pad=8)
    ax.set_ylabel("Price" if ax is axes[0] else "")
    ax.set_xlabel("Quantity")
    if q == 2:
        ax.annotate("Sean would pay \\$50\nJeff would sell at \\$30", (2.15, 76),
                    fontsize=8.5, color=DGOLD, fontweight="bold", va="top")
fig.tight_layout()
save(fig, "ch07_fig_three_panels.png")

# =========================================================== PART 2 primitives
F_OLD, A_OLD = 100_000.0, 0.00025
F_NEW, A_NEW = 125_000.0, 0.0001
P_CHIP = 10.0


def tc_old(q):
    return F_OLD + A_OLD * q ** 2


def tc_new(q):
    return F_NEW + A_NEW * q ** 2


def mc_old(q):
    return 2 * A_OLD * q


def mc_new(q):
    return 2 * A_NEW * q


def atc(tc, q):
    return tc(q) / q


Q_OLD, Q_NEW, Q_TOTAL = 20_000.0, 50_000.0, 70_000.0
assert abs(mc_old(Q_OLD) - 10) < 1e-9 and abs(atc(tc_old, Q_OLD) - 10) < 1e-9
assert abs(mc_new(Q_NEW) - 10) < 1e-9 and abs(atc(tc_new, Q_NEW) - 7.5) < 1e-9
assert tc_old(Q_OLD) == 200_000 and tc_new(Q_NEW) == 375_000
COST_SPLIT = tc_old(Q_OLD) + tc_new(Q_NEW)                     # 575,000
COST_ALLNEW = tc_new(Q_TOTAL)                                   # 615,000
assert COST_SPLIT == 575_000 and COST_ALLNEW == 615_000
PROFIT_SPLIT = P_CHIP * Q_TOTAL - COST_SPLIT                    # 125,000
PROFIT_ALLNEW = P_CHIP * Q_TOTAL - COST_ALLNEW                  # 85,000
assert PROFIT_SPLIT == 125_000 and PROFIT_ALLNEW == 85_000


def _plant_axes(ax, qmax=80_000, pmax=40):
    ax.set_xlim(0, qmax)
    ax.set_ylim(0, pmax)
    ax.set_xticks(range(0, qmax + 1, 20_000))
    ax.set_xticklabels([f"{v:,.0f}" for v in range(0, qmax + 1, 20_000)])
    ax.set_yticks(range(0, pmax + 1, 10))
    ax.set_yticklabels([f"${v}" for v in range(0, pmax + 1, 10)])
    ax.set_xlabel("Quantity (chips per day)")
    ax.set_ylabel("Price")


# -------------------------------------------------- 4. two MC curves (Ex 7.4)
q = np.linspace(2_000, 78_000, 400)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ax.plot(q, mc_old(q), color=RED, lw=2.4)
ax.plot(q, mc_new(q), color=DGOLD, lw=2.4)
ax.annotate(r"$MC_{OLD}$", (62_000, mc_old(62_000)), color=RED, fontsize=12,
            fontweight="bold", xytext=(-46, 8), textcoords="offset points")
ax.annotate(r"$MC_{NEW}$", (74_000, mc_new(74_000)), color=DGOLD, fontsize=12,
            fontweight="bold", xytext=(-52, 8), textcoords="offset points")
_plant_axes(ax)
ax.annotate("The old plant costs more to run\nat every level of output",
            (4_000, 34), fontsize=10.5, color=INK, va="top")
save(fig, "ch07_fig_two_plants_mc.png")

# --------------------------------------------------- 5. old plant (Ex 7.5)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
qq = np.linspace(4_000, 52_000, 400)
ax.plot(qq, mc_old(qq), color=RED, lw=2.4)
ax.plot(qq, atc(tc_old, qq), color=GREEN, lw=2.4)
ax.add_patch(Rectangle((0, 0), Q_OLD, P_CHIP, facecolor=TINT_RED, edgecolor=RED,
                       lw=1.0, zorder=0))
ax.hlines(P_CHIP, 0, Q_OLD, color=BLUE, lw=2.2)
ax.vlines(Q_OLD, 0, P_CHIP, color=INK, lw=1.0, ls="--")
ax.plot([Q_OLD], [P_CHIP], "o", color=INK, ms=6, zorder=5)
ax.annotate(r"$P = MR = \$$10", (300, 11.2), fontsize=11, color=BLUE, fontweight="bold")
ax.annotate(r"$MC_{OLD}$", (44_000, mc_old(44_000)), color=RED, fontsize=12,
            fontweight="bold", xytext=(-44, 6), textcoords="offset points")
ax.annotate(r"$ATC_{OLD}$", (48_000, atc(tc_old, 48_000)), color=GREEN, fontsize=12,
            fontweight="bold", xytext=(-52, 8), textcoords="offset points")
ax.annotate("Total cost\n20,000 × \\$10 = \\$200,000", (Q_OLD * 0.5, P_CHIP * 0.45),
            ha="center", va="center", fontsize=10, color=RED, fontweight="bold")
ax.annotate("Q = 20,000", (Q_OLD, 0), xytext=(6, 16), textcoords="offset points",
            fontsize=10, color=INK)
_plant_axes(ax)
ax.set_title(r"Old plant:  P = MC = ATC = \$10, so economic profit is \$0",
             fontsize=11, color=INK, fontweight="bold", pad=9)
save(fig, "ch07_fig_old_plant.png")

# --------------------------------------------------- 6. new plant (Ex 7.6)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
qq = np.linspace(6_000, 78_000, 400)
ax.plot(qq, mc_new(qq), color=RED, lw=2.4)
ax.plot(qq, atc(tc_new, qq), color=GREEN, lw=2.4)
ax.add_patch(Rectangle((0, 0), Q_NEW, 7.5, facecolor=TINT_RED, edgecolor=RED,
                       lw=1.0, zorder=0))
ax.add_patch(Rectangle((0, 7.5), Q_NEW, 2.5, facecolor=TINT_GREEN, edgecolor=GREEN,
                       lw=1.0, zorder=0))
ax.hlines(P_CHIP, 0, Q_NEW, color=BLUE, lw=2.2)
ax.hlines(7.5, 0, Q_NEW, color=GREEN, lw=1.0, ls="--")
ax.vlines(Q_NEW, 0, P_CHIP, color=INK, lw=1.0, ls="--")
ax.plot([Q_NEW], [P_CHIP], "o", color=INK, ms=6, zorder=5)
ax.annotate(r"$P = MR = \$$10", (300, 11.2), fontsize=11, color=BLUE, fontweight="bold")
ax.annotate(r"$ATC = \$$7.50", (300, 5.4), fontsize=10.5, color=GREEN, fontweight="bold")
ax.annotate(r"$MC_{NEW}$", (70_000, mc_new(70_000)), color=RED, fontsize=12,
            fontweight="bold", xytext=(-52, 6), textcoords="offset points")
ax.annotate(r"$ATC_{NEW}$", (76_000, atc(tc_new, 76_000)), color=GREEN, fontsize=12,
            fontweight="bold", xytext=(-58, 8), textcoords="offset points")
ax.annotate("Costs: $375,000", (Q_NEW * 0.5, 3.6), ha="center", fontsize=10,
            color=RED, fontweight="bold")
ax.annotate("Profit: $125,000", (Q_NEW * 0.5, 8.4), ha="center", fontsize=10,
            color=GREEN, fontweight="bold")
ax.annotate("Q = 50,000", (Q_NEW, 0), xytext=(6, 16), textcoords="offset points",
            fontsize=10, color=INK)
_plant_axes(ax)
ax.set_title(r"New plant:  P = MC = \$10 at 50,000, ATC = \$7.50, profit \$125,000",
             fontsize=11, color=INK, fontweight="bold", pad=9)
save(fig, "ch07_fig_new_plant.png")

# ------------------------------------- 7. enforced production schedule (Ex 7.7)
# Same plant, same axes, two quantities: the one the plant manager would pick, and the
# one head office ordered.  ATC(70,000) = 615,000 / 70,000 = $8.7857 and MC(70,000) = $14.
atc70 = atc(tc_new, Q_TOTAL)
fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.0))
qq2 = np.linspace(6_000, 78_000, 400)

for ax, (qsel, sub, col) in zip(axes, [
        (Q_NEW, "(a) The plant manager's quantity: 50,000\n"
                "Costs \\$375,000 · profit \\$125,000", GREEN),
        (Q_TOTAL, "(b) Head office orders 70,000\n"
                  "Costs \\$615,000 · profit \\$85,000", RED)]):
    a_sel = atc(tc_new, qsel)
    ax.add_patch(Rectangle((0, 0), qsel, a_sel, facecolor=TINT_RED, edgecolor=RED, lw=1.0))
    ax.add_patch(Rectangle((0, a_sel), qsel, P_CHIP - a_sel, facecolor=TINT_GREEN,
                           edgecolor=GREEN, lw=1.0))
    ax.plot(qq2, mc_new(qq2), color=RED, lw=2.3)
    ax.plot(qq2, atc(tc_new, qq2), color=GREEN, lw=2.3)
    ax.hlines(P_CHIP, 0, 78_000, color=BLUE, lw=2.0)
    ax.hlines(a_sel, 0, qsel, color=GREEN, lw=1.0, ls="--")
    ax.vlines(qsel, 0, mc_new(qsel), color=INK, lw=1.0, ls="--")
    ax.plot([qsel], [mc_new(qsel)], "o", color=RED, ms=7, zorder=6)
    ax.annotate(r"$P = \$$10", (400, 10.6), fontsize=10.5, color=BLUE, fontweight="bold")
    ax.annotate(f"ATC = ${a_sel:,.2f}", (400, a_sel - 2.1), fontsize=10,
                color=GREEN, fontweight="bold")
    ax.annotate(f"MC = ${mc_new(qsel):,.0f}", (qsel, mc_new(qsel)),
                xytext=(-104, 30), textcoords="offset points", fontsize=10.5,
                color=RED, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.1))
    ax.annotate(f"{qsel:,.0f}", (qsel, 0), xytext=(-4, 14),
                textcoords="offset points", ha="right", fontsize=10, color=INK)
    _plant_axes(ax, pmax=20)
    ax.set_yticks(range(0, 21, 5))
    ax.set_yticklabels([f"${v}" for v in range(0, 21, 5)])
    ax.set_title(sub, fontsize=10.5, color=col, fontweight="bold", pad=8)
fig.tight_layout()
save(fig, "ch07_fig_enforced.png")

# --------------------------------- 8. the cost of every possible split (original)
qo = np.linspace(500, 70_000, 600)
cost = tc_old(qo) + tc_new(Q_TOTAL - qo)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
ax.plot(qo, cost / 1000, color=BLUE, lw=2.6)
ax.plot([Q_OLD], [COST_SPLIT / 1000], "o", color=GREEN, ms=9, zorder=5)
ax.annotate("Cheapest split\n20,000 old + 50,000 new\n\\$575,000",
            (Q_OLD, COST_SPLIT / 1000), xytext=(24, 34), textcoords="offset points",
            fontsize=10, color=GREEN, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2))
ax.plot([0], [COST_ALLNEW / 1000], "o", color=RED, ms=9, zorder=5)
ax.annotate("Old plant closed — all 70,000\nat the new plant: \\$615,000",
            (0, COST_ALLNEW / 1000), xytext=(34, 104), textcoords="offset points",
            fontsize=10, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax.set_xlim(-3_000, 72_000)
ax.set_ylim(550, 1_500)
ax.set_xticks(range(0, 70_001, 10_000))
ax.set_xticklabels([f"{v:,.0f}" for v in range(0, 70_001, 10_000)])
ax.set_xlabel("Chips made at the OLD plant (the rest go to the new one)")
ax.set_ylabel("Total cost of making 70,000 chips ($000)")
ax.set_title("Only one split equalises marginal cost — and it is the cheapest one",
             fontsize=11, color=INK, fontweight="bold", pad=9)
save(fig, "ch07_fig_split_cost.png")

# =========================================================== PART 3 primitives
# One firm technology, both industries:  TC(q) = 240 + 0.15 q^2
#   MC = 0.3q,  ATC = 240/q + 0.15q,  min ATC = $12 at q = 40 (where MC = ATC = 12)
# Market demand in both industries:  Qd = 1,200 - 20P  (thousand units per day)
# Market supply with n firms:  Qs = n * P / 300  (each firm supplies P/0.3 units)
F_F, A_F = 240.0, 0.15


def f_mc(x):
    return 2 * A_F * x


def f_atc(x):
    return F_F / x + A_F * x


assert abs(f_mc(40) - 12) < 1e-9 and abs(f_atc(40) - 12) < 1e-9
Q_PROFIT, P_PROFIT = 60.0, 18.0      # P = MC = $18 -> q = 60, ATC = $13
assert abs(f_mc(Q_PROFIT) - P_PROFIT) < 1e-9 and abs(f_atc(Q_PROFIT) - 13) < 1e-9
PROFIT_FIRM = (P_PROFIT - f_atc(Q_PROFIT)) * Q_PROFIT           # 300
Q_LOSS, P_LOSS = 30.0, 9.0           # P = MC = $9  -> q = 30, ATC = $12.50
assert abs(f_mc(Q_LOSS) - P_LOSS) < 1e-9 and abs(f_atc(Q_LOSS) - 12.5) < 1e-9
LOSS_FIRM = (f_atc(Q_LOSS) - P_LOSS) * Q_LOSS                   # 105
assert PROFIT_FIRM == 300 and LOSS_FIRM == 105


def demand(p):
    return 1_200 - 20 * p


# firm counts that make each starting price an exact short-run equilibrium
N_ENTRY_1 = demand(18) * 300 / 18      # 14,000 firms at $18
N_ENTRY_2 = demand(12) * 300 / 12      # 24,000 firms at $12
N_EXIT_1 = demand(9) * 300 / 9         # 34,000 firms at $9
N_EXIT_2 = demand(12) * 300 / 12       # 24,000 firms at $12
assert (N_ENTRY_1, N_ENTRY_2, N_EXIT_1) == (14_000, 24_000, 34_000)


def _firm_axes(ax, qmax=110, pmax=40, unit="tons per day"):
    ax.set_xlim(0, qmax)
    ax.set_ylim(0, pmax)
    ax.set_yticks(range(0, pmax + 1, 10))
    ax.set_yticklabels([f"${v}" for v in range(0, pmax + 1, 10)])
    ax.set_xlabel(f"One firm's quantity ({unit})")
    ax.set_ylabel("Price")


def _firm_curves(ax, qmax=110):
    x = np.linspace(8, qmax - 4, 400)
    ax.plot(x, f_mc(x), color=RED, lw=2.3)
    ax.plot(x, f_atc(x), color=GREEN, lw=2.3)
    ax.annotate("MC", (qmax - 22, f_mc(qmax - 22)), color=RED, fontsize=12,
                fontweight="bold", xytext=(-4, 8), textcoords="offset points")
    ax.annotate("ATC", (qmax - 6, f_atc(qmax - 6)), color=GREEN, fontsize=12,
                fontweight="bold", xytext=(-32, 8), textcoords="offset points")


# ------------------------------------------- 9. economic profit (Exhibit 7.9)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
_firm_curves(ax)
ax.add_patch(Rectangle((0, 13), Q_PROFIT, P_PROFIT - 13, facecolor=TINT_GREEN,
                       edgecolor=GREEN, lw=1.1, zorder=0))
ax.hlines(P_PROFIT, 0, Q_PROFIT, color=BLUE, lw=2.2)
ax.hlines(13, 0, Q_PROFIT, color=GREEN, lw=1.0, ls="--")
ax.vlines(Q_PROFIT, 0, P_PROFIT, color=INK, lw=1.0, ls="--")
ax.plot([Q_PROFIT], [P_PROFIT], "o", color=INK, ms=6, zorder=5)
ax.annotate(r"$P = MR = \$$18", (2, 19.0), fontsize=11, color=BLUE, fontweight="bold")
ax.annotate(r"$ATC = \$$13", (2, 9.6), fontsize=10.5, color=GREEN, fontweight="bold")
ax.annotate("Profit\n60 × \\$5 = \\$300 a day", (Q_PROFIT * 0.5, 15.5), ha="center",
            va="center", fontsize=10.5, color=GREEN, fontweight="bold")
ax.annotate("q = 60", (Q_PROFIT, 0), xytext=(6, 14), textcoords="offset points",
            fontsize=10, color=INK)
_firm_axes(ax)
ax.set_title(r"Paper delivery at \$18 a ton: price is above average total cost",
             fontsize=11, color=INK, fontweight="bold", pad=9)
save(fig, "ch07_fig_paper_profit.png")

# --------------------------------------------- 10. economic loss (Exhibit 7.11)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
_firm_curves(ax)
ax.add_patch(Rectangle((0, P_LOSS), Q_LOSS, 12.5 - P_LOSS, facecolor=TINT_RED,
                       edgecolor=RED, lw=1.1, zorder=0))
ax.hlines(P_LOSS, 0, Q_LOSS, color=BLUE, lw=2.2)
ax.hlines(12.5, 0, Q_LOSS, color=GREEN, lw=1.0, ls="--")
ax.vlines(Q_LOSS, 0, 12.5, color=INK, lw=1.0, ls="--")
ax.plot([Q_LOSS], [P_LOSS], "o", color=INK, ms=6, zorder=5)
ax.annotate(r"$ATC = \$$12.50", (2, 13.6), fontsize=10.5, color=GREEN, fontweight="bold")
ax.annotate(r"$P = MR = \$$9", (2, 6.0), fontsize=11, color=BLUE, fontweight="bold")
ax.annotate("Loss\n30 × \\$3.50 = \\$105 a day", (Q_LOSS, 10.75),
            xytext=(44, 46), textcoords="offset points", ha="left", va="center",
            fontsize=10.5, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
ax.annotate("q = 30", (Q_LOSS, 0), xytext=(6, 14), textcoords="offset points",
            fontsize=10, color=INK)
_firm_axes(ax, unit="ton-miles per day")
ax.set_title(r"Grain trucking at \$9: price is below average total cost",
             fontsize=11, color=INK, fontweight="bold", pad=9)
save(fig, "ch07_fig_trucking_loss.png")


# ----------------------------------- 11 & 12. entry and exit (Ex 7.10 and 7.12)
def market_panel(ax, n1, n2, p1, p2, xlabel, title, colour, pmax):
    xmax = max(n1, n2) * pmax / 300 * 1.06
    P = np.linspace(0.4, pmax, 300)
    ax.plot(demand(P), P, color=BLUE, lw=2.4)
    ax.plot(n1 * P / 300, P, color=RED, lw=2.4)
    ax.plot(n2 * P / 300, P, color=DGOLD, lw=2.4)
    q1, q2 = demand(p1), demand(p2)
    for p_, q_ in ((p1, q1), (p2, q2)):
        ax.plot([q_], [p_], "o", color=INK, ms=6, zorder=6)
        ax.hlines(p_, 0, q_, color=INK, lw=0.9, ls=":")
        ax.vlines(q_, 0, p_, color=INK, lw=0.9, ls=":")
        ax.annotate(f"${p_:,.0f}", (0, p_), xytext=(4, 4),
                    textcoords="offset points", fontsize=10, color=INK,
                    fontweight="bold")
    ax.annotate(r"$S_1$", (n1 * pmax / 300, pmax), color=RED, fontsize=13,
                fontweight="bold", xytext=(4, -14), textcoords="offset points")
    ax.annotate(r"$S_2$", (n2 * pmax / 300, pmax), color=DGOLD, fontsize=13,
                fontweight="bold", xytext=(4, -14), textcoords="offset points")
    ax.annotate("D", (demand(pmax * 0.14), pmax * 0.14), color=BLUE, fontsize=13,
                fontweight="bold", xytext=(6, -4), textcoords="offset points")
    ya = pmax * 0.62
    ax.annotate("", xy=(n2 * ya / 300, ya), xytext=(n1 * ya / 300, ya),
                arrowprops=dict(arrowstyle="-|>", color=colour, lw=2.6))
    ax.set_ylim(0, pmax)
    ax.set_xlim(0, xmax)
    ax.set_yticks(range(0, int(pmax) + 1, 6))
    ax.set_yticklabels([f"${v}" for v in range(0, int(pmax) + 1, 6)])
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Price")
    ax.set_title(title, fontsize=10.5, color=INK, fontweight="bold", pad=8)


def firm_panel(ax, p_start, q_start, atc_start, tint, edge, label, title, unit):
    _firm_curves(ax)
    lo, hi = sorted([p_start, atc_start])
    ax.add_patch(Rectangle((0, lo), q_start, hi - lo, facecolor=tint, edgecolor=edge,
                           lw=1.1, zorder=0))
    ax.hlines(p_start, 0, q_start, color=BLUE, lw=2.0)
    ax.hlines(12, 0, 40, color=DGOLD, lw=2.0)
    ax.vlines(q_start, 0, max(p_start, atc_start), color=INK, lw=0.9, ls="--")
    ax.plot([40], [12], "o", color=DGOLD, ms=7, zorder=6)
    ax.annotate(label, (q_start * 0.5, (lo + hi) / 2), ha="center", va="center",
                fontsize=10, color=edge, fontweight="bold")
    ax.annotate("Long run: \\$12 = min ATC,\nq = 40, profit zero", (40, 12),
                xytext=(20, -46), textcoords="offset points", fontsize=9.5,
                color=DGOLD, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.0))
    _firm_axes(ax, unit=unit)
    ax.set_title(title, fontsize=10.5, color=INK, fontweight="bold", pad=8)


fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))
market_panel(axes[0], N_ENTRY_1, N_ENTRY_2, 18, 12,
             "Market quantity (thousand tons per day)",
             "(a) Paper delivery market — entry shifts supply RIGHT", GREEN, 24)
firm_panel(axes[1], 18, 60, 13, TINT_GREEN, GREEN, "Profit\n\\$300",
           "(b) One firm — the profit is competed away", "tons per day")
fig.tight_layout()
save(fig, "ch07_fig_entry.png")

fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))
market_panel(axes[0], N_EXIT_1, N_EXIT_2, 9, 12,
             "Market quantity (thousand ton-miles per day)",
             "(a) Grain trucking market — exit shifts supply LEFT", RED, 18)
firm_panel(axes[1], 9, 30, 12.5, TINT_RED, RED, "Loss\n\\$105",
           "(b) One firm — the loss is competed away", "ton-miles per day")
fig.tight_layout()
save(fig, "ch07_fig_exit.png")

# ------------------------------------------- 13. where it stops: P = MC = min ATC
fig, ax = plt.subplots(figsize=(8.6, 3.6))
_firm_curves(ax)
ax.hlines(12, 0, 110, color=BLUE, lw=2.2)
ax.vlines(40, 0, 12, color=INK, lw=1.0, ls="--")
ax.plot([40], [12], "o", color=INK, ms=8, zorder=6)
ax.annotate(r"$P = MC = ATC = \$$12", (42, 12), xytext=(16, 30),
            textcoords="offset points", fontsize=11.5, color=INK, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.2))
ax.annotate("Nobody wants in.\nNobody wants out.", (56, 3.6), fontsize=11.5,
            color=DGOLD, fontweight="bold")
ax.annotate("q = 40", (40, 0), xytext=(6, 14), textcoords="offset points",
            fontsize=10, color=INK)
_firm_axes(ax)
ax.set_title("Long-run equilibrium: price sits at the bottom of the ATC curve",
             fontsize=11, color=INK, fontweight="bold", pad=9)
save(fig, "ch07_fig_longrun.png")

# =========================================================== PART 4 primitives
# Bottled water:  S: Qs = 2P    D1: Qd = 90 - P    D2: Qd = 120 - P
W_P1, W_Q1 = 30.0, 60.0
W_P2, W_Q2 = 40.0, 80.0
assert 2 * W_P1 == 90 - W_P1 and 2 * W_P2 == 120 - W_P2
W_CAP = 33.0                                   # New York's 10 per cent threshold
W_QCAP = 2 * W_CAP                              # 66 cases supplied
W_SHORT = (120 - W_CAP) - W_QCAP                # 21 cases short
W_DWL = 0.5 * (W_Q2 - W_QCAP) * ((120 - W_QCAP) - W_CAP)
assert W_QCAP == 66 and W_SHORT == 21 and W_DWL == 147.0


def _wm_axes(ax, qmax=130, pmax=70):
    ax.set_xlim(0, qmax)
    ax.set_ylim(0, pmax)
    ax.set_yticks(range(0, pmax + 1, 10))
    ax.set_yticklabels([f"${v}" for v in range(0, pmax + 1, 10)])
    ax.set_xlabel("Cases of bottled water per hour")
    ax.set_ylabel("Price per case")


def _wm_curves(ax, both=True):
    Q = np.linspace(0, 128, 300)
    ax.plot(Q, Q / 2, color=RED, lw=2.4)                     # S: P = Q/2
    ax.plot(Q, 90 - Q, color=BLUE, lw=2.4)                   # D1: P = 90 - Q
    ax.annotate("S", (124, 62), color=RED, fontsize=13, fontweight="bold")
    ax.annotate(r"$D_1$", (86, 4), color=BLUE, fontsize=12, fontweight="bold")
    if both:
        ax.plot(Q, 120 - Q, color=BLUE, lw=2.4, ls="--")     # D2: P = 120 - Q
        ax.annotate(r"$D_2$", (116, 4), color=BLUE, fontsize=12, fontweight="bold")


# ------------------------------------------------- 14. demand shift (Ex 7.14)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
_wm_curves(ax)
for yy in (20, 40, 60):
    ax.annotate("", xy=(90 - yy + 26, yy), xytext=(90 - yy + 4, yy),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.0, alpha=0.75))
for (p, qq_, c) in ((W_P1, W_Q1, GREY), (W_P2, W_Q2, INK)):
    ax.plot([qq_], [p], "o", color=c, ms=7, zorder=6)
    ax.hlines(p, 0, qq_, color=c, lw=0.9, ls=":")
    ax.vlines(qq_, 0, p, color=c, lw=0.9, ls=":")
ax.annotate(r"$\$$30, 60 cases", (W_Q1, W_P1), xytext=(-104, -22),
            textcoords="offset points", fontsize=10, color=GREY, fontweight="bold")
ax.annotate(r"$\$$40, 80 cases", (W_Q2, W_P2), xytext=(16, 16),
            textcoords="offset points", fontsize=10.5, color=INK, fontweight="bold")
_wm_axes(ax)
ax.set_title("A storm is coming: demand shifts right and the price does the work",
             fontsize=11, color=INK, fontweight="bold", pad=9)
save(fig, "ch07_fig_water_shift.png")

# ---------------------------------------------------- 15. shortage (Ex 7.15)
fig, ax = plt.subplots(figsize=(8.6, 3.6))
_wm_curves(ax)
ax.hlines(W_P1, 0, 120 - W_P1, color=DGOLD, lw=2.4)
ax.annotate(r"Price held at $\$$30", (2, 31.4), fontsize=11, color=DGOLD,
            fontweight="bold")
ax.plot([W_Q1], [W_P1], "o", color=RED, ms=7, zorder=6)
ax.plot([90 - W_P1], [W_P1], "o", color=BLUE, ms=7, zorder=6)
ax.annotate("", xy=(90, W_P1), xytext=(60, W_P1),
            arrowprops=dict(arrowstyle="<|-|>", color=DGOLD, lw=2.2))
ax.annotate("Shortage: 30 cases\n60 supplied, 90 wanted", (75, W_P1),
            xytext=(0, -48), textcoords="offset points", ha="center", fontsize=10.5,
            color=DGOLD, fontweight="bold")
_wm_axes(ax)
ax.set_title("Hold the price and the shortage appears instead",
             fontsize=11, color=INK, fontweight="bold", pad=9)
save(fig, "ch07_fig_water_shortage.png")

# ------------------------------------ 16. deadweight loss, lettered (Ex 7.16)
fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))
Q = np.linspace(0, 128, 300)

ax = axes[0]
ax.add_patch(Polygon([(0, W_P2), (0, 120), (W_Q2, W_P2)], facecolor=TINT_BLUE,
                     edgecolor=BLUE, lw=1.0))
ax.add_patch(Polygon([(0, 0), (0, W_P2), (W_Q2, W_P2)], facecolor=TINT_RED,
                     edgecolor=RED, lw=1.0))
ax.plot(Q, Q / 2, color=RED, lw=2.3)
ax.plot(Q, 120 - Q, color=BLUE, lw=2.3)
ax.hlines(W_P2, 0, W_Q2, color=INK, lw=0.9, ls=":")
ax.vlines(W_Q2, 0, W_P2, color=INK, lw=0.9, ls=":")
ax.annotate("A", (22, 62), fontsize=14, color=BLUE, fontweight="bold")
ax.annotate("B", (22, 20), fontsize=14, color=RED, fontweight="bold")
ax.annotate("S", (124, 62), color=RED, fontsize=12, fontweight="bold")
ax.annotate("D", (114, 4), color=BLUE, fontsize=12, fontweight="bold")
ax.annotate(r"$P_2 = \$$40", (0, W_P2), xytext=(4, 5), textcoords="offset points",
            fontsize=10, color=INK, fontweight="bold")
_wm_axes(ax, pmax=125)
ax.set_title("(a) Free market — social surplus = A + B = \\$4,800",
             fontsize=10.5, color=GREEN, fontweight="bold", pad=8)

ax = axes[1]
pd_at_cap = 120 - W_QCAP                                    # $54
ax.add_patch(Polygon([(0, W_CAP), (0, 120), (W_QCAP, pd_at_cap), (W_QCAP, W_CAP)],
                     facecolor=TINT_BLUE, edgecolor=BLUE, lw=1.0))
ax.add_patch(Polygon([(0, 0), (0, W_CAP), (W_QCAP, W_CAP)], facecolor=TINT_RED,
                     edgecolor=RED, lw=1.0))
ax.add_patch(Polygon([(W_QCAP, W_CAP), (W_QCAP, pd_at_cap), (W_Q2, W_P2)],
                     facecolor=TINT_GOLD, edgecolor=DGOLD, lw=1.2, hatch="///"))
ax.plot(Q, Q / 2, color=RED, lw=2.3)
ax.plot(Q, 120 - Q, color=BLUE, lw=2.3)
ax.hlines(W_CAP, 0, 120 - W_CAP, color=DGOLD, lw=2.2)
ax.vlines(W_QCAP, 0, pd_at_cap, color=INK, lw=0.9, ls=":")
ax.annotate("C", (18, 66), fontsize=14, color=BLUE, fontweight="bold")
ax.annotate("E", (16, 15), fontsize=14, color=RED, fontweight="bold")
ax.annotate("D", (70.5, 42), fontsize=13, color=DGOLD, fontweight="bold")
ax.annotate("S", (124, 62), color=RED, fontsize=12, fontweight="bold")
ax.annotate(r"$P_1 = \$$33", (0, W_CAP), xytext=(4, 5), textcoords="offset points",
            fontsize=10, color=DGOLD, fontweight="bold")
ax.annotate("66 traded, not 80", (W_QCAP, 0), xytext=(-4, 14),
            textcoords="offset points", fontsize=9.5, color=INK)
_wm_axes(ax, pmax=125)
ax.set_title("(b) Price ceiling — social surplus = C + E = \\$4,653\nD is the deadweight loss",
             fontsize=10.5, color=RED, fontweight="bold", pad=8)
fig.tight_layout()
save(fig, "ch07_fig_dwl_letters.png")

# ------------------------------------------ 17. the ten per cent rule, in numbers
fig, ax = plt.subplots(figsize=(8.9, 3.7))
_wm_curves(ax, both=True)
ax.add_patch(Polygon([(W_QCAP, W_CAP), (W_QCAP, pd_at_cap), (W_Q2, W_P2)],
                     facecolor=TINT_GOLD, edgecolor=DGOLD, lw=1.4, hatch="///", zorder=2))
ax.hlines(W_CAP, 0, 120 - W_CAP, color=DGOLD, lw=2.4)
ax.hlines(W_P1, 0, 92, color=GREY, lw=1.0, ls=":")
ax.plot([W_Q2], [W_P2], "o", color=INK, ms=7, zorder=6)
ax.plot([W_QCAP], [W_CAP], "o", color=DGOLD, ms=7, zorder=6)
ax.annotate(r"Pre-storm price $\$$30", (2, 26.4), fontsize=9.5, color=GREY)
ax.annotate(r"Statutory ceiling $\$$33  (30 × 1.10)", (2, 34.4), fontsize=10.5,
            color=DGOLD, fontweight="bold")
ax.annotate(r"Market-clearing price $\$$40", (W_Q2, W_P2), xytext=(12, -30),
            textcoords="offset points", fontsize=10.5, color=INK, fontweight="bold")
ax.annotate("Deadweight loss \\$147\n66 cases sold, not 80\n21 cases short",
            (72, 45), xytext=(-214, 42), textcoords="offset points", fontsize=10.5,
            color=DGOLD, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.2))
_wm_axes(ax)
ax.set_title("A 10% cap on a price that wanted to rise 33%",
             fontsize=11.5, color=INK, fontweight="bold", pad=9)
save(fig, "ch07_fig_ten_percent.png")

# =========================================================== Uber primitives
# S: Qs = P     D1: Qd = 30 - P     D2: Qd = 60 - 2P
U_P1, U_Q1 = 15.0, 15.0
U_P2, U_Q2 = 20.0, 20.0
assert U_P1 == 30 - U_Q1 and 60 - 2 * U_P2 == U_P2
U_SHORT = (60 - 2 * U_P1) - U_P1                       # 15 rides short at $15
U_DWL = 0.5 * (U_Q2 - U_P1) * ((30 - U_P1 / 2) - U_P1)  # 18.75
assert U_SHORT == 15 and U_DWL == 18.75


def _uber_axes(ax):
    ax.set_xlim(0, 34)
    ax.set_ylim(0, 32)
    ax.set_yticks(range(0, 33, 5))
    ax.set_yticklabels([f"${v}" for v in range(0, 33, 5)])
    ax.set_xlabel("Rides per hour")
    ax.set_ylabel("Price per ride")


def _uber_curves(ax):
    Q = np.linspace(0, 32, 200)
    ax.plot(Q, Q, color=RED, lw=2.4)                       # S: P = Q
    ax.plot(Q, 30 - Q, color=BLUE, lw=2.4)                 # D: P = 30 - Q
    ax.plot(Q, 30 - Q / 2, color=BLUE, lw=2.4, ls="--")    # D_surge: P = 30 - Q/2
    ax.annotate("S", (30, 30.6), color=RED, fontsize=13, fontweight="bold")
    ax.annotate("D", (27.5, 2.8), color=BLUE, fontsize=12, fontweight="bold")
    ax.annotate(r"$D_{surge}$", (30, 15), color=BLUE, fontsize=11,
                fontweight="bold", xytext=(-6, 8), textcoords="offset points",
                ha="right")


# ------------------------------------------- 18. surge pricing (Exhibit 7.17)
fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))

ax = axes[0]
_uber_curves(ax)
ax.hlines(U_P1, 0, 30, color=DGOLD, lw=2.2)
ax.plot([15], [15], "o", color=RED, ms=7, zorder=6)
ax.plot([30], [15], "o", color=BLUE, ms=7, zorder=6)
ax.annotate("", xy=(30, 15), xytext=(15, 15),
            arrowprops=dict(arrowstyle="<|-|>", color=DGOLD, lw=2.2))
ax.annotate("Excess demand: 15 rides", (22.5, 15), xytext=(0, -34),
            textcoords="offset points", ha="center", fontsize=10.5, color=DGOLD,
            fontweight="bold")
ax.annotate(r"Price stuck at $\$$15", (0.6, 16.4), fontsize=10.5, color=DGOLD,
            fontweight="bold")
_uber_axes(ax)
ax.set_title("(a) No surge — 15 rides happen, 15 riders wait",
             fontsize=10.5, color=RED, fontweight="bold", pad=8)

ax = axes[1]
_uber_curves(ax)
ax.hlines(U_P2, 0, U_Q2, color=INK, lw=1.0, ls=":")
ax.vlines(U_Q2, 0, U_P2, color=INK, lw=1.0, ls=":")
ax.plot([U_Q2], [U_P2], "o", color=INK, ms=7, zorder=6)
ax.annotate("", xy=(20, 20), xytext=(15, 15),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.4))
ax.annotate("Drivers come out along\nthe supply curve", (17.5, 17.5), xytext=(-150, -72),
            textcoords="offset points", fontsize=10, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
ax.annotate(r"$\$$20, 20 rides", (U_Q2, U_P2), xytext=(10, 12),
            textcoords="offset points", fontsize=10.5, color=INK, fontweight="bold")
_uber_axes(ax)
ax.set_title(r"(b) Surge to \$20 — 20 rides happen, nobody waits",
             fontsize=10.5, color=GREEN, fontweight="bold", pad=8)
fig.tight_layout()
save(fig, "ch07_fig_surge.png")

# ------------------------------------ 19. the practice problem, with its answer
fig, ax = plt.subplots(figsize=(8.9, 3.7))
_uber_curves(ax)
ax.add_patch(Polygon([(15, 15), (15, 22.5), (20, 20)], facecolor=TINT_GOLD,
                     edgecolor=DGOLD, lw=1.3, hatch="///", zorder=2))
ax.plot([U_P1], [U_P1], "o", color=GREY, ms=7, zorder=6)
ax.plot([U_Q2], [U_P2], "o", color=INK, ms=7, zorder=6)
ax.hlines(15, 0, 30, color=DGOLD, lw=1.6, ls="-")
ax.annotate(r"Before the game: $\$$15, 15 rides", (15, 15), xytext=(-136, -30),
            textcoords="offset points", fontsize=10, color=GREY, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
ax.annotate(r"After, with surge: $\$$20, 20 rides", (U_Q2, U_P2), xytext=(14, 10),
            textcoords="offset points", fontsize=10.5, color=INK, fontweight="bold")
ax.annotate("Deadweight loss if the price\nstays at \\$15: \\$18.75 an hour",
            (16.5, 18), xytext=(-40, 76), textcoords="offset points", fontsize=10.5,
            color=DGOLD, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.2))
_uber_axes(ax)
ax.set_title("The football game lets out: what a fixed price costs",
             fontsize=11.5, color=INK, fontweight="bold", pad=9)
save(fig, "ch07_fig_practice.png")

# ------------------------------------------------------- 20. SFpark, as measured
LABELS = ["Time spent looking\nfor a space",
          "Driving around\nlooking (and its CO2)",
          "Parking citations",
          "Average garage rate",
          "Average meter rate",
          "Hours inside the\n60–80% target"]
VALUES = [-43, -30, -23, -12, -4, +31]
fig, ax = plt.subplots(figsize=(8.6, 3.6))
cols = [GREEN if v < 0 else BLUE for v in VALUES]
bars = ax.barh(range(len(VALUES)), VALUES, color=cols, height=0.62)
ax.set_yticks(range(len(VALUES)))
ax.set_yticklabels(LABELS, fontsize=10)
ax.invert_yaxis()
ax.axvline(0, color=INK, lw=1.0)
ax.set_xlim(-52, 42)
ax.set_xlabel("Change in the pilot areas, 2011–2013 (%)")
for i, v in enumerate(VALUES):
    ax.annotate(f"{v:+d}%", (v, i), xytext=(8 if v > 0 else -8, 0),
                textcoords="offset points", va="center",
                ha="left" if v > 0 else "right", fontsize=10.5,
                color=cols[i], fontweight="bold")
ax.spines["left"].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.set_title("San Francisco let the meter price move. Parking got easier — and cheaper.",
             fontsize=11, color=INK, fontweight="bold", pad=10)
save(fig, "ch07_fig_sfpark.png")

print("\nDerived figures used on slides:")
print(f"  efficient split cost      ${COST_SPLIT:,.0f}   profit ${PROFIT_SPLIT:,.0f}")
print(f"  all-at-new-plant cost     ${COST_ALLNEW:,.0f}   profit ${PROFIT_ALLNEW:,.0f}")
print(f"  cost of the CEO's order   ${PROFIT_SPLIT - PROFIT_ALLNEW:,.0f}")
print(f"  ATC at 70,000 (new)       ${atc(tc_new, Q_TOTAL):,.4f}")
print(f"  MC at 70,000 (new)        ${mc_new(Q_TOTAL):,.2f}")
print(f"  firm profit / loss        ${PROFIT_FIRM:,.0f} / ${LOSS_FIRM:,.0f}")
print(f"  firms, entry industry     {N_ENTRY_1:,.0f} -> {N_ENTRY_2:,.0f}")
print(f"  firms, exit industry      {N_EXIT_1:,.0f} -> {N_EXIT_2:,.0f}")
print(f"  water DWL at a 10% cap    ${W_DWL:,.0f}  shortage {W_SHORT:,.0f} cases")
print(f"  uber DWL at a fixed $15   ${U_DWL:,.2f}  shortage {U_SHORT:,.0f} rides")
