#!/usr/bin/env python3
"""ECON 003 Ch04 — exhibit figures, UCR palette, Arial metrics (Liberation Sans)."""
import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

BLUE = "#003DA5"; GOLD = "#FFB81D"; DGOLD = "#B88300"
RED  = "#CC3333"; GREEN = "#2E7D32"
INK  = "#333333"; MID = "#666666"; LIGHT = "#999999"; RULE = "#DDDDDD"

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
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_xlabel(xlab, fontsize=11, labelpad=6)
    ax.set_ylabel(ylab, fontsize=11, labelpad=6)
    ax.tick_params(length=4, width=1.0)

def guide(ax, x, y, x0=0, y0=0, color=MID):
    ax.plot([x0, x], [y, y], ls=(0, (4, 3)), lw=1.0, color=color, zorder=1)
    ax.plot([x, x], [y0, y], ls=(0, (4, 3)), lw=1.0, color=color, zorder=1)

def dot(ax, x, y, color="#444444", s=55, z=6):
    ax.plot([x], [y], "o", ms=math.sqrt(s), color=color, zorder=z,
            mec="white", mew=1.2)

# ---------------------------------------------------------------- oil market
# Qd = 35 - 17.83*ln(P/50)   Qs = 35 + 8.916*ln(P/50)
BD, BS = 17.83, 8.916
def qd(P, shift=0.0):  return 35 + shift - BD * np.log(P / 50.0)
def qs(P, shift=0.0):  return 35 + shift + BS * np.log(P / 50.0)
def eq(ds=0.0, ss=0.0):
    L = (ss - ds) / -(BD + BS)
    P = 50 * math.exp(L)
    return P, qd(P, ds)
def Pd(Q, shift=0.0): return 50 * np.exp((35 + shift - Q) / BD)
def Ps(Q, shift=0.0): return 50 * np.exp((Q - 35 - shift) / BS)


# =========================================================== Exhibit 4.1
def ex41():
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    P = np.linspace(0.4, 7.0, 200); Q = 350 - 50 * P
    ax.plot(Q, P, color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    for p in [6, 5, 4, 3, 2, 1]:
        q = 350 - 50 * p
        guide(ax, q, p, color=RULE)
        dot(ax, q, p)
    frame(ax, "Quantity  (gallons per year)", "Price  ($ per gallon)", (0, 360), (0, 7.3))
    ax.set_xticks([0, 50, 100, 150, 200, 250, 300, 350])
    ax.set_yticks([0, 1, 2, 3, 4, 5, 6, 7])
    ax.text(300, 5.4, "Demand curve", color=BLUE, fontsize=12, fontweight="bold", ha="right")
    save(fig, "ex41_chloe_demand")


# =========================================================== Exhibit 4.2
def ex42():
    fig, axes = plt.subplots(1, 3, figsize=(11.6, 3.5))
    sets = [("Sue", 100, BLUE), ("Carlos", 200, "#2C6FBB"), ("Sue + Carlos  =  market", 300, BLUE)]
    for ax, (name, step, col) in zip(axes, sets):
        prices = np.array([1, 2, 3, 4, 5])
        qty = step * (6 - prices)
        ax.plot(qty, prices, color=col, lw=3.0, solid_capstyle="round", zorder=3)
        for p, q in zip(prices, qty):
            dot(ax, q, p, s=40)
        frame(ax, "Quantity (gallons/year)", "Price ($/gallon)", (0, step * 5 * 1.12), (0, 5.9))
        ax.set_title(name, fontsize=12, fontweight="bold", color=BLUE, pad=8)
        ax.set_yticks([1, 2, 3, 4, 5])
    axes[2].set_title(sets[2][0], fontsize=12, fontweight="bold", color=DGOLD, pad=8)
    axes[2].lines[0].set_color(DGOLD)
    for ln in axes[2].lines[1:]:
        ln.set_markerfacecolor("#444444")
    # annotate the $3 row
    for ax, q in zip(axes, [300, 600, 900]):
        ax.plot([0, q], [3, 3], ls=(0, (4, 3)), lw=1.1, color=DGOLD, zorder=2)
        ax.plot([q, q], [0, 3], ls=(0, (4, 3)), lw=1.1, color=DGOLD, zorder=2)
        ax.text(q * 1.06, 3.25, f"{q:,}", fontsize=12, color=DGOLD, fontweight="bold")
    axes[2].text(1400, 4.6, "300 + 600 = 900", fontsize=11.5, color=DGOLD,
                 fontweight="bold", ha="right")
    fig.subplots_adjust(wspace=0.34)
    save(fig, "ex42_aggregate_demand")


# =========================================================== Exhibit 4.3
def ex43():
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    Q = np.linspace(22, 55, 300)
    ax.plot(Q, Pd(Q), color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
    guide(ax, 35, 50)
    dot(ax, 35, 50)
    frame(ax, "Quantity  (billions of barrels of oil per year)", "Price  ($ per barrel)", (0, 56), (0, 105))
    ax.set_xticks([0, 10, 20, 35, 50]); ax.set_yticks([0, 20, 40, 50, 60, 80, 100])
    ax.text(52, 20, "Market\ndemand curve", color=BLUE, fontsize=11.5, fontweight="bold", ha="right", va="bottom")
    save(fig, "ex43_market_demand_oil")


# =========================================================== Exhibit 4.4
def ex44():
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))
    # (a) shifts
    ax = axes[0]
    Qg = np.linspace(4, 46, 200)
    ax.plot(Qg, Pd(Qg), color=BLUE, lw=3.0, zorder=3)
    ax.plot(Qg, Pd(Qg, 9), color="#7FA8DC", lw=3.0, zorder=2)
    ax.plot(Qg, Pd(Qg, -9), color="#7FA8DC", lw=3.0, zorder=2)
    ax.annotate("", xy=(44, 34), xytext=(34, 34),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.4))
    ax.annotate("", xy=(16, 34), xytext=(26, 34),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.4))
    ax.text(45, 40, "increase\nin demand", color=GREEN, fontsize=10.5, fontweight="bold", ha="right")
    ax.text(15, 40, "decrease\nin demand", color=RED, fontsize=10.5, fontweight="bold", ha="left")
    frame(ax, "Quantity", "Price", (0, 50), (0, 105))
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(a)  A SHIFT of the demand curve", fontsize=12, fontweight="bold", color=BLUE, pad=9)
    ax.text(25, 8, "caused by anything EXCEPT\nthe good's own price", fontsize=10.5, color=MID, ha="center")
    # (b) movement
    ax = axes[1]
    ax.plot(Qg, Pd(Qg), color=BLUE, lw=3.0, zorder=3)
    for q, p, lab in [(24, Pd(24), "A"), (40, Pd(40), "B")]:
        guide(ax, q, p, color=RULE); dot(ax, q, p)
    ax.annotate("", xy=(39, Pd(39) + 2), xytext=(25, Pd(25) - 2),
                arrowprops=dict(arrowstyle="-|>", color=DGOLD, lw=2.4,
                                connectionstyle="arc3,rad=0.0"))
    ax.text(24, Pd(24) + 5, "A", fontsize=12, fontweight="bold", color=INK)
    ax.text(40.5, Pd(40) + 4, "B", fontsize=12, fontweight="bold", color=INK)
    frame(ax, "Quantity", "Price", (0, 50), (0, 105))
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(b)  A MOVEMENT along the demand curve", fontsize=12, fontweight="bold", color=DGOLD, pad=9)
    ax.text(25, 8, "caused ONLY by a change in\nthe good's own price", fontsize=10.5, color=MID, ha="center")
    fig.subplots_adjust(wspace=0.18)
    save(fig, "ex44_shift_vs_movement")


# =========================================================== Exhibit 4.6
def ex46():
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    q = np.array([0.0, 0.6, 1.0, 1.2]); p = np.array([10, 25, 50, 75])
    qs_ = np.linspace(0, 1.32, 200)
    # smooth interpolation through the four points
    coef = np.polyfit(q, p, 3)
    ax.plot(qs_, np.polyval(coef, qs_), color=RED, lw=3.0, solid_capstyle="round", zorder=3)
    for qq, pp in zip(q, p):
        guide(ax, qq, pp, color=RULE); dot(ax, qq, pp)
    frame(ax, "Quantity  (billions of barrels of oil per year)", "Price  ($ per barrel)", (0, 1.4), (0, 92))
    ax.set_xticks([0, 0.6, 1.0, 1.2]); ax.set_yticks([0, 10, 25, 50, 75])
    ax.text(1.36, 30, "ExxonMobil's\nsupply curve", color=RED, fontsize=11.5, fontweight="bold", ha="right")
    save(fig, "ex46_exxon_supply")


# =========================================================== Exhibit 4.7
def ex47():
    fig, axes = plt.subplots(1, 3, figsize=(11.6, 3.5))
    p = np.array([10, 25, 50, 75])
    sets = [("Chevron", np.array([0.0, 0.4, 0.7, 0.9])),
            ("ExxonMobil", np.array([0.0, 0.6, 1.0, 1.2])),
            ("Chevron + ExxonMobil  =  market", np.array([0.0, 1.0, 1.7, 2.1]))]
    for i, (ax, (name, q)) in enumerate(zip(axes, sets)):
        col = RED if i < 2 else DGOLD
        coef = np.polyfit(q, p, 3)
        qs_ = np.linspace(0, q[-1] * 1.1, 200)
        ax.plot(qs_, np.polyval(coef, qs_), color=col, lw=3.0, zorder=3)
        for qq, pp in zip(q, p):
            dot(ax, qq, pp, s=40)
        frame(ax, "Quantity (bn barrels/year)", "Price ($/barrel)", (0, q[-1] * 1.18), (0, 92))
        ax.set_title(name, fontsize=12, fontweight="bold", color=col, pad=8)
        ax.set_yticks([0, 25, 50, 75])
        ax.plot([0, q[2]], [50, 50], ls=(0, (4, 3)), lw=1.1, color=DGOLD, zorder=2)
        ax.plot([q[2], q[2]], [0, 50], ls=(0, (4, 3)), lw=1.1, color=DGOLD, zorder=2)
        ax.text(q[2] * 1.04, 53, f"{q[2]:.1f}", fontsize=12, color=DGOLD, fontweight="bold")
    axes[2].text(2.4, 15, "0.7 + 1.0 = 1.7", fontsize=11.5, color=DGOLD,
                 fontweight="bold", ha="right")
    fig.subplots_adjust(wspace=0.34)
    save(fig, "ex47_aggregate_supply")


# =========================================================== supply shifters
def supply_shift_panel():
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))
    Qg = np.linspace(20, 50, 200)
    ax = axes[0]
    ax.plot(Qg, Ps(Qg), color=RED, lw=3.0, zorder=3)
    ax.plot(Qg, Ps(Qg, 8), color="#E8A0A0", lw=3.0, zorder=2)
    ax.plot(Qg, Ps(Qg, -8), color="#E8A0A0", lw=3.0, zorder=2)
    ax.annotate("", xy=(46, 62), xytext=(37, 62), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=2.4))
    ax.annotate("", xy=(26, 62), xytext=(35, 62), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.4))
    ax.text(47, 70, "increase\nin supply", color=GREEN, fontsize=10.5, fontweight="bold", ha="right")
    ax.text(25, 70, "decrease\nin supply", color=RED, fontsize=10.5, fontweight="bold", ha="left")
    frame(ax, "Quantity", "Price", (18, 52), (0, 105)); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(a)  A SHIFT of the supply curve", fontsize=12, fontweight="bold", color=RED, pad=9)
    ax.text(0.5, 0.04, "input prices · technology · number of sellers · sellers' expectations",
            transform=ax.transAxes, fontsize=10.2, color=MID, ha="center")
    ax = axes[1]
    ax.plot(Qg, Ps(Qg), color=RED, lw=3.0, zorder=3)
    for q in (28, 40):
        guide(ax, q, Ps(q), x0=18, color=RULE); dot(ax, q, Ps(q))
    ax.text(26.9, Ps(28) + 5, "A", fontsize=12, fontweight="bold")
    ax.text(40.7, Ps(40) - 3, "B", fontsize=12, fontweight="bold")
    ax.annotate("", xy=(39.4, Ps(39.4) - 3), xytext=(28.8, Ps(28.8) + 2),
                arrowprops=dict(arrowstyle="-|>", color=DGOLD, lw=2.2))
    frame(ax, "Quantity", "Price", (18, 52), (0, 105)); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("(b)  A MOVEMENT along the supply curve", fontsize=12, fontweight="bold", color=DGOLD, pad=9)
    ax.text(0.04, 0.94, "a change in the good's own price,\nand nothing else",
            transform=ax.transAxes, fontsize=10.5, color=MID, ha="left", va="top")
    fig.subplots_adjust(wspace=0.18)
    save(fig, "supply_shift_vs_movement")


# =========================================================== Exhibit 4.10
def ex410():
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    Qd_ = np.linspace(22, 52, 300); Qs_ = np.linspace(20, 44, 300)
    ax.plot(Qd_, Pd(Qd_), color=BLUE, lw=3.0, zorder=3)
    ax.plot(Qs_, Ps(Qs_), color=RED, lw=3.0, zorder=3)
    guide(ax, 35, 50); dot(ax, 35, 50, s=90)
    frame(ax, "Quantity  (billions of barrels of oil per year)", "Price  ($ per barrel)", (0, 54), (0, 105))
    ax.set_xticks([0, 10, 20, 35, 50]); ax.set_yticks([0, 20, 40, 50, 60, 80, 100])
    ax.text(50, 22, "Demand", color=BLUE, fontsize=12, fontweight="bold", ha="right")
    ax.text(43, 92, "Supply", color=RED, fontsize=12, fontweight="bold", ha="left")
    ax.annotate("competitive equilibrium\n$50  ·  35 billion barrels", xy=(35, 50), xytext=(9, 68),
                fontsize=11, fontweight="bold", color=DGOLD,
                arrowprops=dict(arrowstyle="->", color=DGOLD, lw=1.6))
    save(fig, "ex410_equilibrium")


def _sd_base(ax, xlim=(0, 54), ylim=(0, 105)):
    Qd_ = np.linspace(22, 52, 300); Qs_ = np.linspace(20, 44, 300)
    ax.plot(Qd_, Pd(Qd_), color=BLUE, lw=3.0, zorder=3)
    ax.plot(Qs_, Ps(Qs_), color=RED, lw=3.0, zorder=3)
    frame(ax, "Quantity  (billions of barrels per year)", "Price  ($ per barrel)", xlim, ylim)
    ax.set_yticks([0, 20, 40, 50, 60, 80, 100])


# =========================================================== excess supply
def excess_supply():
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    _sd_base(ax)
    ax.plot([0, 38], [70, 70], ls=(0, (4, 3)), lw=1.2, color=INK)
    for q in (29, 38):
        ax.plot([q, q], [0, 70], ls=(0, (4, 3)), lw=1.0, color=MID)
    ax.axvspan(29, 38, ymin=0.0, ymax=70 / 105, color=GOLD, alpha=0.22, zorder=1)
    dot(ax, 35, 50, s=70); dot(ax, 29, 70, s=55, color=BLUE); dot(ax, 38, 70, s=55, color=RED)
    ax.annotate("", xy=(38, 79), xytext=(29, 79), arrowprops=dict(arrowstyle="<|-|>", color=DGOLD, lw=2.0))
    ax.text(33.5, 84, "excess supply = 9", ha="center", fontsize=11.5, fontweight="bold", color=DGOLD)
    ax.text(1.5, 72.5, "market price $70", fontsize=11, color=INK)
    ax.set_xticks([0, 10, 20, 29, 35, 38, 50])
    ax.text(28.4, 63, "Qd 29", color=BLUE, fontsize=10.5, fontweight="bold", ha="right")
    ax.text(38.8, 63, "Qs 38", color=RED, fontsize=10.5, fontweight="bold", ha="left")
    ax.text(52, 5, "sellers cut the price", fontsize=10.5, color=MID, ha="right", style="italic")
    save(fig, "excess_supply")


# =========================================================== excess demand
def excess_demand():
    fig, ax = plt.subplots(figsize=(6.9, 4.1))
    _sd_base(ax)
    ax.plot([0, 44], [30, 30], ls=(0, (4, 3)), lw=1.2, color=INK)
    for q in (30, 44):
        ax.plot([q, q], [0, 30], ls=(0, (4, 3)), lw=1.0, color=MID)
    ax.axvspan(30, 44, ymin=0.0, ymax=30 / 105, color=RED, alpha=0.13, zorder=1)
    dot(ax, 35, 50, s=70); dot(ax, 30, 30, s=55, color=RED); dot(ax, 44, 30, s=55, color=BLUE)
    ax.annotate("", xy=(44, 39), xytext=(30, 39), arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=2.0))
    ax.text(37, 43, "excess demand = 14", ha="center", fontsize=11.5, fontweight="bold", color=RED)
    ax.text(1.5, 32.5, "market price $30", fontsize=11, color=INK)
    ax.set_xticks([0, 10, 20, 30, 35, 44])
    ax.text(29.4, 22, "Qs 30", color=RED, fontsize=10.5, fontweight="bold", ha="right")
    ax.text(44.8, 22, "Qd 44", color=BLUE, fontsize=10.5, fontweight="bold", ha="left")
    ax.text(52, 5, "buyers bid the price up", fontsize=10.5, color=MID, ha="right", style="italic")
    save(fig, "excess_demand")


# =========================================================== single shifts
def one_shift(name, ds=0.0, ss=0.0, title=""):
    fig, ax = plt.subplots(figsize=(6.9, 4.2))
    Qg = np.linspace(18, 54, 300)
    ax.plot(Qg, Pd(Qg), color=("#9CB9DE" if ds else BLUE), lw=2.6, zorder=3)
    ax.plot(Qg, Ps(Qg), color=("#E8A0A0" if ss else RED), lw=2.6, zorder=3)
    if ds: ax.plot(Qg, Pd(Qg, ds), color=BLUE, lw=3.2, zorder=4)
    if ss: ax.plot(Qg, Ps(Qg, ss), color=RED, lw=3.2, zorder=4)
    P0, Q0 = 50.0, 35.0
    P1, Q1 = eq(ds, ss)
    guide(ax, Q0, P0, color=RULE); dot(ax, Q0, P0, s=55, color="#999999")
    guide(ax, Q1, P1, color=MID);  dot(ax, Q1, P1, s=95, color=DGOLD)
    frame(ax, "Quantity  (billions of barrels per year)", "Price  ($ per barrel)", (18, 56), (0, 108))
    ax.set_xticks([Q1, Q0]); ax.set_xticklabels([f"{Q1:,.0f}", f"{Q0:,.0f}"])
    ax.set_yticks([min(P0, P1), max(P0, P1)])
    ax.set_yticklabels([f"${min(P0,P1):,.0f}", f"${max(P0,P1):,.0f}"])
    # curve labels, anchored where each curve leaves the plotting box
    qtop = lambda sh: 35 + sh + BS * math.log(100 / 50.0)     # supply where P = 100
    XR = 53.6                                                 # right edge for demand labels
    if ss:
        ax.text(qtop(0) + 0.5, 99, "S₁", color="#E8A0A0", fontsize=13, fontweight="bold", va="top")
        ax.text(qtop(ss) - 2.4, 99, "S₂", color=RED, fontsize=13, fontweight="bold", va="top")
        ax.text(XR + 0.6, Pd(XR), "D", color=BLUE, fontsize=13, fontweight="bold", va="center")
    if ds:
        ax.text(XR + 0.6, Pd(XR), "D₁", color="#9CB9DE", fontsize=13, fontweight="bold", va="center")
        ax.text(XR + 0.6, Pd(XR, ds) - 1, "D₂", color=BLUE, fontsize=13, fontweight="bold", va="center")
        ax.text(qtop(0) + 0.5, 99, "S", color=RED, fontsize=13, fontweight="bold", va="top")
    # result strip — sits above the axes so it never collides with a curve
    dirP = "▲ up" if P1 > P0 else "▼ down"; dirQ = "▲ up" if Q1 > Q0 else "▼ down"
    ax.text(0.5, 1.012,
            f"price  ${P0:,.0f} → ${P1:,.0f}  {dirP}          "
            f"quantity  {Q0:,.0f} → {Q1:,.1f}  {dirQ}",
            transform=ax.transAxes, va="bottom", ha="center", fontsize=11.5,
            fontweight="bold", color=DGOLD)
    if title:
        ax.set_title(title, fontsize=12.5, fontweight="bold", color=BLUE, pad=26)
    save(fig, name)


# =========================================================== both shift
def both_shift():
    fig, axes = plt.subplots(1, 3, figsize=(11.6, 3.6))
    cases = [(-8, 2, "(a)  quantity FALLS"), (-6, 3, "(b)  quantity UNCHANGED"), (-3, 8, "(c)  quantity RISES")]
    Qg = np.linspace(16, 56, 300)
    for ax, (ds, ss, lab) in zip(axes, cases):
        ax.plot(Qg, Pd(Qg), color="#9CB9DE", lw=2.4)
        ax.plot(Qg, Ps(Qg), color="#E8A0A0", lw=2.4)
        ax.plot(Qg, Pd(Qg, ds), color=BLUE, lw=2.8)
        ax.plot(Qg, Ps(Qg, ss), color=RED, lw=2.8)
        P1, Q1 = eq(ds, ss)
        guide(ax, 35, 50, x0=16, color=RULE); dot(ax, 35, 50, s=45, color="#999999")
        guide(ax, Q1, P1, x0=16, color=MID);  dot(ax, Q1, P1, s=65, color=DGOLD)
        frame(ax, "Quantity", "Price", (16, 56), (0, 105))
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(lab, fontsize=11.5, fontweight="bold", color=DGOLD, pad=22)
        ax.text(0.5, 1.012, f"price $50 → ${P1:,.0f}      quantity 35 → {Q1:,.0f}",
                transform=ax.transAxes, va="bottom", ha="center", fontsize=10.2, color=INK)
    axes[0].text(0.03, 0.06, "pale = before        bold = after", transform=axes[0].transAxes,
                 fontsize=9.8, color=MID, style="italic")
    fig.subplots_adjust(wspace=0.16)
    save(fig, "both_curves_shift")


# =========================================================== roses / beer
def roses_beer():
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.9))
    Qg = np.linspace(16, 56, 300)
    # roses: demand right, supply steep (inelastic) -> price spikes
    ax = axes[0]
    steepS = lambda Q, sh=0: 50 * np.exp((Q - 35 - sh) / 3.2)
    ax.plot(Qg, Pd(Qg), color="#9CB9DE", lw=2.6)
    ax.plot(Qg, Pd(Qg, 12), color=BLUE, lw=3.0)
    Qr = np.linspace(28, 42, 200)
    ax.plot(Qr, steepS(Qr), color=RED, lw=3.0)
    L = 12 / (BD + 3.2); P1 = 50 * math.exp(L); Q1 = 35 + 3.2 * L
    guide(ax, 35, 50, x0=16, color=RULE); dot(ax, 35, 50, s=50, color="#999999")
    guide(ax, Q1, P1, x0=16, color=MID); dot(ax, Q1, P1, s=80, color=DGOLD)
    ax.annotate("", xy=(48, 34), xytext=(40, 34), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2))
    frame(ax, "Quantity of roses", "Price", (16, 56), (0, 130)); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("ROSES  ·  demand shifts right, supply barely moves", fontsize=11.5, fontweight="bold", color=RED, pad=9)
    ax.text(0.5, 0.04, "price rises a lot, quantity rises a little", transform=ax.transAxes,
            fontsize=10.5, color=MID, ha="center")
    # beer: both shift right -> quantity up, price ~flat
    ax = axes[1]
    ax.plot(Qg, Pd(Qg), color="#9CB9DE", lw=2.6); ax.plot(Qg, Ps(Qg), color="#E8A0A0", lw=2.6)
    ax.plot(Qg, Pd(Qg, 8), color=BLUE, lw=3.0); ax.plot(Qg, Ps(Qg, 16), color=RED, lw=3.0)
    P1, Q1 = eq(8, 16)
    guide(ax, 35, 50, x0=16, color=RULE); dot(ax, 35, 50, s=50, color="#999999")
    guide(ax, Q1, P1, x0=16, color=MID); dot(ax, Q1, P1, s=80, color=DGOLD)
    ax.annotate("", xy=(50, 30), xytext=(42, 30), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2))
    ax.annotate("", xy=(50, 78), xytext=(42, 78), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.2))
    frame(ax, "Quantity of beer", "Price", (16, 56), (0, 130)); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("BEER  ·  BOTH curves shift right", fontsize=11.5, fontweight="bold", color=BLUE, pad=9)
    ax.text(0.5, 0.04, "quantity rises a lot, price barely moves — or falls", transform=ax.transAxes,
            fontsize=10.5, color=MID, ha="center")
    fig.subplots_adjust(wspace=0.16)
    save(fig, "roses_beer")


# =========================================================== price ceiling
def price_ceiling():
    fig, ax = plt.subplots(figsize=(6.9, 4.2))
    P = np.linspace(0.2, 8.0, 200)
    QD = 200 - 20 * P; QS = 20 + 25 * P
    ax.plot(QD, P, color=BLUE, lw=3.0, zorder=3)
    ax.plot(QS, P, color=RED, lw=3.0, zorder=3)
    guide(ax, 120, 4.0, color=RULE); dot(ax, 120, 4.0, s=60, color="#999999")
    ax.axhline(3.0, color=DGOLD, lw=2.6, zorder=4)
    ax.text(4, 3.12, "PRICE CEILING  $3.00", color=DGOLD, fontsize=11, fontweight="bold", ha="left")
    for q, c in ((95, RED), (140, BLUE)):
        ax.plot([q, q], [0, 3.0], ls=(0, (4, 3)), lw=1.0, color=MID)
        dot(ax, q, 3.0, s=55, color=c)
    ax.axvspan(95, 140, ymin=0, ymax=3.0 / 8.4, color=RED, alpha=0.12, zorder=1)
    ax.annotate("", xy=(140, 2.2), xytext=(95, 2.2), arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=2.0))
    ax.text(117.5, 2.35, "shortage = 45", ha="center", fontsize=11.5, fontweight="bold", color=RED)
    frame(ax, "Quantity  (millions of gallons per day)", "Price  ($ per gallon)", (0, 200), (0, 8.4))
    ax.set_xticks([0, 50, 95, 120, 140, 200]); ax.set_yticks([0, 2, 3, 4, 6, 8])
    ax.set_yticklabels(["0", "$2", "$3", "$4", "$6", "$8"])
    ax.text(4, 4.15, "free-market price $4.00", fontsize=10.5, color=MID)
    ax.text(93, 3.30, "Qs 95", color=RED, fontsize=11, fontweight="bold", ha="right")
    ax.text(142, 3.30, "Qd 140", color=BLUE, fontsize=11, fontweight="bold", ha="left")
    save(fig, "price_ceiling")


# =========================================================== Exhibit 4.5
def ex45():
    fig, ax = plt.subplots(figsize=(6.9, 4.0))
    pts = [("Brazil", 26, 5.55), ("Mexico", 85, 3.40), ("Venezuela", 122, 0.04)]
    for name, q, p in pts:
        dot(ax, q, p, s=110, color=BLUE)
        ax.annotate(name, xy=(q, p), xytext=(q + 4, p + 0.30), fontsize=12,
                    fontweight="bold", color=BLUE)
    qs_ = np.array([p[1] for p in pts]); ps_ = np.array([p[2] for p in pts])
    k = np.polyfit(np.log(qs_), ps_, 1)
    xx = np.linspace(20, 130, 100)
    ax.plot(xx, np.polyval(k, np.log(xx)), color=LIGHT, lw=1.8, ls=(0, (6, 4)), zorder=1)
    frame(ax, "Quantity demanded per person  (gallons of gasoline per year)",
          "Price including taxes and subsidies  ($ per gallon)", (0, 145), (-0.3, 6.4))
    ax.set_xticks([0, 20, 40, 60, 80, 100, 120, 140])
    ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
    ax.set_yticklabels(["0", "$1", "$2", "$3", "$4", "$5", "$6"])
    ax.text(140, 5.9, "2013", fontsize=10.5, color=MID, ha="right")
    save(fig, "ex45_gasoline_countries")


if __name__ == "__main__":
    ex41(); ex42(); ex43(); ex44(); ex46(); ex47()
    supply_shift_panel()
    ex410(); excess_supply(); excess_demand()
    one_shift("shift_supply_left", ss=-4.0, title="Libya, 2011 — supply shifts LEFT")
    one_shift("shift_supply_right", ss=6.0, title="Fracking — supply shifts RIGHT")
    one_shift("shift_demand_left", ds=-5.0, title="Efficiency and substitutes — demand shifts LEFT")
    both_shift(); roses_beer(); price_ceiling(); ex45()


# ============================================== price taker → price maker
def price_taker_to_maker():
    """The demand curve facing ONE seller, as that seller's share of the market grows.

    Economically this is the residual demand curve rotating from horizontal (a
    price taker, who loses every buyer if it raises price at all) toward the market
    demand curve itself (a price maker, who loses only some).
    """
    fig, axes = plt.subplots(1, 3, figsize=(11.6, 2.95))
    P0 = 100.0
    panels = [
        ("ONE CORNER", "a sliver of the market",
         lambda q: np.full_like(q, P0), (0, 12), 8.0, "you take the price"),
        ("SEVERAL NEIGHBOURHOODS", "a noticeable share",
         lambda q: 130 - 1.0 * q, (0, 42), 14.0, "you nudge the price"),
        ("THE WHOLE CITY", "there is nobody else",
         lambda q: 180 - 1.2 * q, (0, 100), 45.0, "you SET the price"),
    ]
    for ax, (lab, sub, fn, xlim, qstar, verdict) in zip(axes, panels):
        q = np.linspace(xlim[0], xlim[1], 200)
        ax.plot(q, fn(q), color=BLUE, lw=3.0, solid_capstyle="round", zorder=3)
        ax.axhline(P0, ls=(0, (4, 3)), lw=1.1, color=LIGHT, zorder=1)
        p = float(fn(np.array([qstar]))[0])
        guide(ax, qstar, p, color=MID)
        dot(ax, qstar, p, s=95, color=DGOLD)
        frame(ax, "Quantity this seller can move", "Price", xlim, (40, 195))
        ax.set_xticks([])
        if abs(p - P0) > 3:
            ax.set_yticks([P0, p])
            ax.set_yticklabels(["street\nprice", f"+{p - P0:,.0f}"], fontsize=9.5)
        else:
            ax.set_yticks([P0]); ax.set_yticklabels(["street\nprice"], fontsize=9.5)
        ax.set_title(lab, fontsize=11.5, fontweight="bold", color=BLUE, pad=20)
        ax.text(0.5, 1.015, sub, transform=ax.transAxes, ha="center", va="bottom",
                fontsize=9.5, color=MID, style="italic")
        ax.text(0.5, 0.05, verdict, transform=ax.transAxes, ha="center",
                fontsize=11.5, fontweight="bold",
                color=MID if verdict.startswith("you take") else DGOLD,
                bbox=dict(boxstyle="square,pad=0.30", fc="white", ec="none"))
    axes[0].text(0.04, 0.86, "flat — raise your\nprice at all and\nyou sell nothing",
                 transform=axes[0].transAxes, fontsize=9.2, color=MID, va="top")
    axes[2].text(0.55, 0.86, "sloped — raise it and\nyou lose some buyers,\nnot all of them",
                 transform=axes[2].transAxes, fontsize=9.2, color=MID, va="top")
    fig.subplots_adjust(wspace=0.34)
    save(fig, "price_taker_to_maker")


if "price_taker_to_maker" not in globals().get("__built__", ""):
    price_taker_to_maker()


# ============================================== surplus → craze → shortage → price rises
def craze_arc():
    """The whole arc of a fad in one row: a good priced above the market, a demand
    shift that outruns the posted price, and the price move that clears it.

    D1: Qd = 100 − 10P     D2: Qd = 220 − 10P     S: Qs = 20 + 10P
    Original equilibrium $4 · 60.  Posted price $6.
    At $6 on D1: Qd 40, Qs 80  → surplus 40.
    At $6 on D2: Qd 160, Qs 80 → shortage 80.
    New equilibrium on D2: $10 · 120.
    """
    D1 = lambda P: 100 - 10 * P
    D2 = lambda P: 220 - 10 * P
    S = lambda P: 20 + 10 * P
    PP = np.linspace(0, 16, 200)

    fig, axes = plt.subplots(1, 3, figsize=(11.6, 3.05))
    titles = ["NOBODY WANTS ONE", "THEN EVERYBODY DOES", "SO THE PRICE GOES UP"]
    subs = ["priced above the market", "same price, new buyers", "the queue is the signal"]

    for i, (ax, t, sub) in enumerate(zip(axes, titles, subs)):
        if i == 0:
            ax.plot(D1(PP), PP, color=BLUE, lw=3.0, zorder=3)
        else:
            ax.plot(D1(PP), PP, color="#9CB9DE", lw=2.2, zorder=2)
            ax.plot(D2(PP), PP, color=BLUE, lw=3.0, zorder=3)
        ax.plot(S(PP), PP, color=RED, lw=3.0, zorder=3)
        frame(ax, "Quantity", "Price", (0, 245), (0, 16))
        ax.set_yticks([4, 6, 10]); ax.set_yticklabels(["$4", "$6", "$10"], fontsize=10)
        ax.set_xticks([])
        ax.set_title(t, fontsize=11.5, fontweight="bold", color=BLUE, pad=20)
        ax.text(0.5, 1.015, sub, transform=ax.transAxes, ha="center", va="bottom",
                fontsize=9.5, color=MID, style="italic")

    # (a) surplus at the posted price
    ax = axes[0]
    ax.plot([0, 245], [6, 6], ls=(0, (4, 3)), lw=1.3, color=INK)
    ax.axvspan(40, 80, ymin=0, ymax=6 / 16, color=GOLD, alpha=0.25, zorder=1)
    dot(ax, 40, 6, s=55, color=BLUE); dot(ax, 80, 6, s=55, color=RED)
    ax.annotate("", xy=(80, 7.2), xytext=(40, 7.2),
                arrowprops=dict(arrowstyle="<|-|>", color=DGOLD, lw=1.9))
    ax.text(60, 7.9, "surplus 40", ha="center", fontsize=11, fontweight="bold", color=DGOLD, bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="none"))
    ax.text(150, 6.3, "posted $6", fontsize=10, color=INK, bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="none"))
    ax.text(0.97, 0.05, "marked down, still unsold", transform=ax.transAxes, ha="right",
            fontsize=10, color=MID, style="italic", bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="none"))

    # (b) the shift, at the same posted price
    ax = axes[1]
    ax.plot([0, 245], [6, 6], ls=(0, (4, 3)), lw=1.3, color=INK)
    ax.axvspan(80, 160, ymin=0, ymax=6 / 16, color=RED, alpha=0.14, zorder=1)
    dot(ax, 80, 6, s=55, color=RED); dot(ax, 160, 6, s=55, color=BLUE)
    ax.annotate("", xy=(160, 7.2), xytext=(80, 7.2),
                arrowprops=dict(arrowstyle="<|-|>", color=RED, lw=1.9))
    ax.text(120, 7.9, "shortage 80", ha="center", fontsize=11, fontweight="bold", color=RED, bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="none"))
    ax.annotate("", xy=(205, 2.3), xytext=(130, 2.3),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.2))
    ax.text(167, 3.3, "tastes change", ha="center", fontsize=10, color=BLUE, fontweight="bold", bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="none"))
    ax.text(0.97, 0.05, "a queue outside the door", transform=ax.transAxes, ha="right",
            fontsize=10, color=MID, style="italic", bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="none"))

    # (c) the market clears again, higher
    ax = axes[2]
    ax.plot([0, 245], [6, 6], ls=(0, (4, 3)), lw=1.1, color=LIGHT)
    guide(ax, 120, 10, color=MID)
    dot(ax, 60, 4, s=45, color="#999999")
    dot(ax, 120, 10, s=100, color=DGOLD)
    ax.annotate("", xy=(112, 9.4), xytext=(90, 6.6),
                arrowprops=dict(arrowstyle="-|>", color=DGOLD, lw=2.2))
    ax.text(0.50, 0.95, "price $6 → $10      quantity 80 → 120", transform=ax.transAxes,
            ha="center", va="top", fontsize=11, fontweight="bold", color=DGOLD,
            bbox=dict(boxstyle="square,pad=0.35", fc="white", ec=RULE, lw=0.9))
    ax.text(0.97, 0.05, "no queue, and more hoops made", transform=ax.transAxes, ha="right",
            fontsize=10, color=MID, style="italic", bbox=dict(boxstyle="square,pad=0.25", fc="white", ec="none"))

    fig.subplots_adjust(wspace=0.26)
    save(fig, "craze_arc")


craze_arc()


# ============================================== the 2026 gasoline price path
def gas_2026():
    """US and California weekly average regular gasoline, selected weeks of 2026.
    Source: EIA Gasoline and Diesel Fuel Update (weekly retail, all formulations).
    Only weeks where BOTH series were read off EIA are plotted — no interpolation
    is implied beyond the straight segments between them.
    """
    weeks = ["2 Feb", "2 Mar", "9 Mar", "6 Apr", "11 May", "1 Jun", "13 Jul", "27 Jul"]
    us = [2.867, 3.015, 3.502, 4.120, 4.500, 4.305, 3.855, 4.096]
    ca = [4.177, 4.475, 5.093, 5.769, 5.969, 5.853, 5.200, 5.489]
    x = np.arange(len(weeks))

    fig, ax = plt.subplots(figsize=(9.4, 3.35))
    ax.plot(x, ca, color=RED, lw=3.0, marker="o", ms=6, mec="white", mew=1.4, zorder=4)
    ax.plot(x, us, color=BLUE, lw=3.0, marker="o", ms=6, mec="white", mew=1.4, zorder=4)
    ax.fill_between(x, us, ca, color=GOLD, alpha=0.13, zorder=1)

    ax.text(len(weeks) - 1 + 0.12, ca[-1], "California\n$5.49", color=RED,
            fontsize=11, fontweight="bold", va="center")
    ax.text(len(weeks) - 1 + 0.12, us[-1], "US average\n$4.10", color=BLUE,
            fontsize=11, fontweight="bold", va="center")

    # the shock, dated
    ax.axvline(0.0, color=MID, ls=(0, (4, 3)), lw=1.2, zorder=2)
    ax.annotate("war begins\n28 Feb", xy=(0.0, 6.35), xytext=(0.28, 6.35),
                fontsize=9.5, color=MID, va="center",
                arrowprops=dict(arrowstyle="->", color=MID, lw=1.1))
    for xi, lab in ((4, "peak\n11 May"), (6, "ceasefire\ntrough")):
        ax.plot([xi, xi], [0, ca[xi]], ls=(0, (3, 3)), lw=1.0, color=LIGHT, zorder=1)
        ax.text(xi, 6.45, lab, ha="center", fontsize=9.5, color=MID)

    frame(ax, "", "Retail price  ($ per gallon, regular)", (-0.35, len(weeks) + 0.95), (2.4, 6.9))
    ax.set_xticks(x); ax.set_xticklabels(weeks, fontsize=10)
    ax.set_yticks([3, 4, 5, 6]); ax.set_yticklabels(["$3", "$4", "$5", "$6"])
    ax.text(0.02, 0.04, "California pays about $1.39 more per gallon than the US average",
            transform=ax.transAxes, fontsize=10, color=DGOLD, fontweight="bold")
    save(fig, "gas_2026")


# ============================================== where the demand shift comes from
def demand_side():
    """Two facts the front page leaves out."""
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 3.05))

    # (a) China 2026 gasoline demand forecast, decomposed
    ax = axes[0]
    ax.barh([0], [-5.2], color=BLUE, height=0.42, zorder=3, label="structural")
    ax.barh([0], [-0.3], left=[-5.2], color=RED, height=0.42, zorder=3)
    ax.axvline(0, color=INK, lw=1.2)
    ax.text(-2.6, 0.34, "−5.2  electric vehicles", ha="center", fontsize=11,
            fontweight="bold", color=BLUE)
    ax.text(-5.35, -0.42, "−0.3\nthe war", ha="center", fontsize=10.5,
            fontweight="bold", color=RED)
    ax.set_xlim(-6.6, 1.2); ax.set_ylim(-0.95, 0.85)
    ax.set_yticks([]); ax.set_xticks([-6, -4, -2, 0])
    ax.set_xticklabels(["−6%", "−4%", "−2%", "0"], fontsize=10)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_title("CHINA'S 2026 GASOLINE DEMAND", fontsize=11.5, fontweight="bold",
                 color=BLUE, pad=20)
    ax.text(0.5, 1.015, "forecast change on 2025", transform=ax.transAxes, ha="center",
            va="bottom", fontsize=9.5, color=MID, style="italic")

    # (b) US EVs: sales share vs share of the cars actually on the road
    ax = axes[1]
    ax.bar([0, 1], [6, 2], color=[BLUE, LIGHT], width=0.46, zorder=3)
    for xi, v, lab in ((0, 6, "6%"), (1, 2, "2%")):
        ax.text(xi, v + 0.45, lab, ha="center", fontsize=14, fontweight="bold",
                color=BLUE if xi == 0 else MID)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["of new cars\nSOLD", "of cars on\nthe ROAD"], fontsize=10.5)
    ax.set_ylim(0, 9); ax.set_yticks([])
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_title("US BATTERY-ELECTRIC VEHICLES", fontsize=11.5, fontweight="bold",
                 color=BLUE, pad=20)
    ax.text(0.5, 1.015, "the stock turns over slowly", transform=ax.transAxes,
            ha="center", va="bottom", fontsize=9.5, color=MID, style="italic")

    fig.subplots_adjust(wspace=0.24)
    save(fig, "demand_side")


gas_2026()
demand_side()
one_shift("hormuz_supply_left", ss=-4.0,
          title="Hormuz, 2026 — supply shifts LEFT")
