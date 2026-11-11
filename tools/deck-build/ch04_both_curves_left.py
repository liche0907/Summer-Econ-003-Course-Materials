#!/usr/bin/env python3
"""Rebuild the both-curves-shift panel for the Hormuz storyline.

The two slides before it now shift supply LEFT (Hormuz) and demand LEFT
(efficiency, EVs). Both left means the QUANTITY is determinate -- it falls -- and
the PRICE is what the diagram cannot pin down. The old figure ran the fracking
case (demand left, supply RIGHT), which is the mirror image and contradicts the
build-up.

Same oil market as every other figure in the deck:
    Qd = 35 + d - 17.83*ln(P/50)      Qs = 35 + s + 8.916*ln(P/50)

Demand held at d = -5, the shift used on the previous slide; the supply shift is
varied so each crossing lands on a round price:

    (a) s = -2.182   P 50 -> 45   Q 35 -> 31.9    demand shift dominates
    (b) s = -5.000   P 50 -> 50   Q 35 -> 30      the two exactly offset
    (c) s = -7.549   P 50 -> 55   Q 35 -> 28.3    supply shift dominates
"""
import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE = "#003DA5"; GOLD = "#FFB81D"; DGOLD = "#B88300"
RED = "#CC3333"; INK = "#333333"; MID = "#666666"; RULE = "#DDDDDD"

plt.rcParams.update({
    "font.family": "Liberation Sans",
    "font.size": 12,
    "axes.edgecolor": INK, "axes.linewidth": 1.1,
    "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK, "ytick.color": INK,
    "xtick.labelsize": 11.5, "ytick.labelsize": 11.5,
    "figure.dpi": 200, "savefig.dpi": 200,
    "savefig.facecolor": "white", "figure.facecolor": "white",
})

BD, BS = 17.83, 8.916


def qd(P, shift=0.0):
    return 35 + shift - BD * np.log(P / 50.0)


def eq(ds=0.0, ss=0.0):
    L = (ss - ds) / -(BD + BS)
    P = 50 * math.exp(L)
    return P, qd(P, ds)


def Pd(Q, shift=0.0):
    return 50 * np.exp((35 + shift - Q) / BD)


def Ps(Q, shift=0.0):
    return 50 * np.exp((Q - 35 - shift) / BS)


def guide(ax, x, y, x0=0, y0=0, color=MID):
    ax.plot([x0, x], [y, y], ls=(0, (4, 3)), lw=1.0, color=color, zorder=1)
    ax.plot([x, x], [y0, y], ls=(0, (4, 3)), lw=1.0, color=color, zorder=1)


def dot(ax, x, y, color="#444444", s=55, z=6):
    ax.plot([x], [y], "o", ms=math.sqrt(s), color=color, zorder=z,
            mec="white", mew=1.2)


def frame(ax, xlab, ylab, xlim, ylim):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_xlabel(xlab, fontsize=12, labelpad=6)
    ax.set_ylabel(ylab, fontsize=12, labelpad=6)
    ax.tick_params(length=4, width=1.0)


def num(v):
    return f"{v:,.1f}".rstrip("0").rstrip(".")


def both_left(path):
    # solved so the crossings land on $45 / $50 / $55
    S_A = -5.0 + BD_LN(0.9)
    S_C = -5.0 + BD_LN(1.1)
    cases = [(-5.0, S_A, "(a)  price FALLS", "the demand shift is bigger"),
             (-5.0, -5.0, "(b)  price UNCHANGED", "the two shifts are equal"),
             (-5.0, S_C, "(c)  price RISES", "the supply shift is bigger")]
    fig, axes = plt.subplots(1, 3, figsize=(11.6, 3.6))
    Qg = np.linspace(16, 56, 300)
    for ax, (ds, ss, lab, why) in zip(axes, cases):
        ax.plot(Qg, Pd(Qg), color="#9CB9DE", lw=2.4)
        ax.plot(Qg, Ps(Qg), color="#E8A0A0", lw=2.4)
        ax.plot(Qg, Pd(Qg, ds), color=BLUE, lw=2.8)
        ax.plot(Qg, Ps(Qg, ss), color=RED, lw=2.8)
        P1, Q1 = eq(ds, ss)
        guide(ax, 35, 50, x0=16, color=RULE); dot(ax, 35, 50, s=45, color="#999999")
        guide(ax, Q1, P1, x0=16, color=MID); dot(ax, Q1, P1, s=65, color=DGOLD)
        frame(ax, "Quantity", "Price", (16, 56), (0, 105))
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(lab, fontsize=12.8, fontweight="bold", color=DGOLD, pad=22)
        ax.text(0.5, 1.012,
                f"price $50 → ${P1:,.0f}      quantity 35 → {num(Q1)}",
                transform=ax.transAxes, va="bottom", ha="center",
                fontsize=11.4, color=INK)
        # bottom-right is the one corner every curve has left by this point
        ax.text(0.97, 0.045, why, transform=ax.transAxes, ha="right",
                fontsize=10.5, color=MID, style="italic")
    fig.subplots_adjust(wspace=0.16)
    # the legend and the punchline go under the whole figure, clear of the curves
    fig.text(0.5, -0.045,
             "pale = before      bold = after            "
             "quantity falls in all three — only the price is left open",
             ha="center", va="top", fontsize=11.4, color=MID)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)


def BD_LN(r):
    """Supply-shift offset that puts the new crossing at price 50*r.

    eq() uses L = (ss - ds) / -(BD + BS) and P = 50*exp(L), so pinning P = 50*r
    means ss = ds - (BD + BS)*ln(r).
    """
    return -(BD + BS) * math.log(r)


if __name__ == "__main__":
    for ds, ss in [(-5.0, -5.0 + BD_LN(0.9)), (-5.0, -5.0), (-5.0, -5.0 + BD_LN(1.1))]:
        P, Q = eq(ds, ss)
        print(f"  demand {ds:+.3f}  supply {ss:+.3f}  ->  P ${P:.4f}   Q {Q:.4f}")
    both_left("both_curves_left.png")
    from PIL import Image
    im = Image.open("both_curves_left.png")
    print("size", im.size, "aspect", im.size[0] / im.size[1])
