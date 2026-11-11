#!/usr/bin/env python3
"""ECON 003 chapter cover art generator — UCR navy/gold system.
Emits one 1920x1080 SVG per chapter; render to PNG with Chromium."""

import os, math

W, H = 1920, 1080

NAVY_D  = "#00214F"
NAVY    = "#003DA5"
GOLD    = "#FFB81D"
WHITE   = "#FFFFFF"
FONT    = "Liberation Sans, Arial, Helvetica, sans-serif"

# ---- right-hand diagram panel -------------------------------------------
PX0, PY0, PW_, PH_ = 1040, 170, 780, 740      # panel box
OX, OY = PX0 + 140, PY0 + 615                  # plot origin (bottom-left)
PW, PH = 500, 450                              # plot extents

def px(t): return OX + t * PW
def py(v): return OY - v * PH

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---- primitives ---------------------------------------------------------
def line(x1, y1, x2, y2, stroke, w=3, dash=None, op=1.0, cap="round"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{w}" stroke-opacity="{op}" '
            f'stroke-linecap="{cap}"{d}/>')

def path(d, stroke=None, w=3, fill="none", dash=None, op=1.0, fop=1.0):
    s = f' stroke="{stroke}" stroke-width="{w}" stroke-opacity="{op}" stroke-linecap="round" stroke-linejoin="round"' if stroke else ''
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" fill-opacity="{fop}"{s}{dd}/>'

def dot(x, y, r=11, fill=GOLD, ring=True):
    o = ""
    if ring:
        o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r+9:.1f}" fill="none" stroke="{WHITE}" stroke-width="2.5" stroke-opacity="0.55"/>'
    o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"/>'
    return o

def txt(x, y, s, size=22, fill=WHITE, weight="bold", anchor="start", op=1.0, ls=0, rot=None, style=""):
    tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot is not None else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" fill-opacity="{op}" text-anchor="{anchor}" '
            f'letter-spacing="{ls}"{tr} {style}>{esc(s)}</text>')

def axes(xlab, ylab):
    o  = line(OX, py(1.06), OX, OY, WHITE, 3, op=0.5, cap="square")
    o += line(OX, OY, px(1.10), OY, WHITE, 3, op=0.5, cap="square")
    o += f'<path d="M {px(1.10)+2:.1f} {OY:.1f} l -14 -7 l 0 14 z" fill="{WHITE}" fill-opacity="0.5"/>'
    o += f'<path d="M {OX:.1f} {py(1.06)-2:.1f} l -7 14 l 14 0 z" fill="{WHITE}" fill-opacity="0.5"/>'
    o += txt(px(1.10), OY + 42, xlab, 21, WHITE, "bold", "end", 0.62, 1.5)
    o += txt(OX - 30, OY, ylab, 21, WHITE, "bold", "start", 0.62, 1.5, rot=-90)
    return o

def curve(pts, stroke, w=4, dash=None, op=1.0):
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return path(d, stroke, w, dash=dash, op=op)

def poly(pts, fill, fop=0.30, stroke=None, w=2):
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    return path(d, stroke, w, fill=fill, fop=fop)

def guides(x, y):
    """dashed drop-lines from a point to both axes"""
    return line(OX, y, x, y, WHITE, 2, "7 9", 0.45) + line(x, y, x, OY, WHITE, 2, "7 9", 0.45)

def tag(x, y, s, fill=GOLD, size=21, anchor="start"):
    return txt(x, y, s, size, fill, "bold", anchor, 1.0, 0.5)

# ---- chapter diagrams ---------------------------------------------------
def d_ch01():
    """Benefit vs cost bars, net benefit bracket."""
    o = ""
    bw = 118
    b1 = px(0.18); b2 = px(0.58)
    hb, hc = 0.88, 0.52
    o += f'<rect x="{b1:.1f}" y="{py(hb):.1f}" width="{bw}" height="{OY-py(hb):.1f}" fill="{GOLD}" fill-opacity="0.92" rx="4"/>'
    o += f'<rect x="{b2:.1f}" y="{py(hc):.1f}" width="{bw}" height="{OY-py(hc):.1f}" fill="none" stroke="{WHITE}" stroke-width="3.5" stroke-opacity="0.85" rx="4"/>'
    o += txt(b1 + bw/2, OY + 40, "BENEFIT", 20, GOLD, "bold", "middle", 1, 1.5)
    o += txt(b2 + bw/2, OY + 40, "COST", 20, WHITE, "bold", "middle", 0.85, 1.5)
    # net bracket
    bx = px(0.95)
    o += line(b1 + bw, py(hb), bx + 14, py(hb), WHITE, 2, "6 8", 0.5)
    o += line(b2 + bw, py(hc), bx + 14, py(hc), WHITE, 2, "6 8", 0.5)
    o += line(bx, py(hb), bx, py(hc), GOLD, 3.5)
    o += line(bx - 9, py(hb), bx + 9, py(hb), GOLD, 3.5)
    o += line(bx - 9, py(hc), bx + 9, py(hc), GOLD, 3.5)
    o += tag(bx + 26, py((hb + hc)/2) + 8, "NET", GOLD, 22)
    o += axes("OPTION", "VALUE")
    return o, "BENEFITS − COSTS: THE CORE TEST"

def d_ch03():
    """Net-benefit hill with marked optimum."""
    pts = [(px(t), py(-3.4*(t-0.55)**2 + 0.92)) for t in [i/120 for i in range(6, 113)]]
    o  = curve(pts, GOLD, 5)
    xstar, ystar = px(0.55), py(0.92)
    o += guides(xstar, ystar)
    o += dot(xstar, ystar)
    o += tag(xstar + 34, ystar - 18, "OPTIMUM")
    o += txt(OX - 18, ystar + 8, "max", 19, WHITE, "bold", "end", 0.7)
    o += txt(xstar, OY + 40, "Q*", 22, WHITE, "bold", "middle", 0.9)
    o += axes("QUANTITY", "NET BENEFIT")
    return o, "PICK THE PEAK, NOT THE TOTAL"

def d_ch04():
    """Supply-demand cross."""
    o  = curve([(px(0.05), py(0.95)), (px(1.02), py(0.12))], WHITE, 4.5)
    o += curve([(px(0.05), py(0.12)), (px(1.02), py(0.95))], GOLD, 4.5)
    x, y = px(0.535), py(0.535)
    o += guides(x, y); o += dot(x, y)
    o += tag(px(1.02) + 10, py(0.12) - 4, "D", WHITE, 24)
    o += tag(px(1.02) + 10, py(0.95) + 6, "S", GOLD, 24)
    o += txt(OX - 18, y + 8, "P*", 22, WHITE, "bold", "end", 0.9)
    o += txt(x, OY + 40, "Q*", 22, WHITE, "bold", "middle", 0.9)
    o += axes("QUANTITY", "PRICE")
    return o, "WHERE THE TWO SIDES MEET"

def d_ch05():
    """Budget line + indifference curve tangency."""
    o = curve([(px(0.06), py(0.95)), (px(0.95), py(0.08))], WHITE, 4.5)
    ic = []
    for i in range(0, 101):
        t = 0.16 + i/100 * 0.72
        v = 0.2332 / (t - 0.055)
        if 0.03 <= v <= 1.02:
            ic.append((px(t), py(v)))
    o += curve(ic, GOLD, 4.5)
    x, y = px(0.5434), py(0.4775)
    o += guides(x, y); o += dot(x, y)
    o += tag(px(0.16), py(0.86), "BUDGET", WHITE, 20)
    o += tag(px(0.90), py(0.34), "U", GOLD, 24)
    o += axes("GOOD X", "GOOD Y")
    return o, "BEST BUNDLE YOU CAN AFFORD"

def d_ch06():
    """Marginal-cost staircase under a price line."""
    o = ""
    steps = [0.14, 0.24, 0.36, 0.50, 0.68, 0.90]
    n = len(steps); wdt = 1.0 / n
    pline = 0.60
    for i, h in enumerate(steps):
        x1, x2 = px(i*wdt + 0.02), px((i+1)*wdt)
        col = GOLD if h <= pline else WHITE
        fop = 0.30 if h <= pline else 0.0
        o += f'<rect x="{x1:.1f}" y="{py(h):.1f}" width="{x2-x1:.1f}" height="{OY-py(h):.1f}" fill="{GOLD}" fill-opacity="{fop}" stroke="{col}" stroke-width="3" stroke-opacity="0.9"/>'
    o += line(OX, py(pline), px(1.05), py(pline), GOLD, 4.5)
    o += tag(px(1.05) + 8, py(pline) + 8, "P", GOLD, 24)
    o += tag(px(0.06), py(0.99), "SELL WHILE  P ≥ MC", WHITE, 20)
    o += axes("UNITS SOLD", "MARGINAL COST")
    return o, "EVERY UNIT PAYS ITS OWN WAY"

def d_ch07():
    """U-shaped ATC tangent to a horizontal price line: zero profit."""
    pts = [(px(t), py(4.6*(t-0.55)**2 + 0.42)) for t in [i/120 for i in range(8, 118)]]
    pts = [(x, y) for x, y in pts if y >= py(1.02)]
    o  = curve(pts, WHITE, 4.5)
    o += line(OX, py(0.42), px(1.05), py(0.42), GOLD, 4.5)
    x, y = px(0.55), py(0.42)
    o += dot(x, y)
    o += tag(px(1.05) + 8, y + 8, "P = MR", GOLD, 21)
    o += tag(px(0.80), py(0.90), "ATC", WHITE, 22)
    o += txt(x, OY + 40, "q*", 22, WHITE, "bold", "middle", 0.9)
    o += line(x, y, x, OY, WHITE, 2, "7 9", 0.45)
    o += axes("FIRM OUTPUT", "COST / PRICE")
    return o, "PRICE IS PUSHED TO THE FLOOR"

def d_ch08():
    """PPF plus a flatter trade line reaching beyond it."""
    ppf = []
    for i in range(0, 101):
        t = i/100 * 0.94 + 0.03
        v = 0.92 * math.sqrt(max(0.0, 1 - (t/0.97)**2))
        ppf.append((px(t), py(v)))
    # world-price line: tangent to the PPF at t=0.50, so it lies above it everywhere
    t0 = 0.50; v0 = 0.92 * math.sqrt(1 - (t0/0.97)**2)
    slope = -0.92 * (t0/0.97**2) / math.sqrt(1 - (t0/0.97)**2)
    tl = lambda t: v0 + slope * (t - t0)
    lo, hi = 0.03, 0.97
    o  = curve(ppf, WHITE, 4.5)
    o += poly([(px(t), py(tl(t))) for t in [lo + i/100*(hi-lo) for i in range(101)]]
              + list(reversed(ppf)), GOLD, 0.13)
    o += curve([(px(t), py(tl(t))) for t in [lo + i/100*(hi-lo) for i in range(101)]],
               GOLD, 4.5, dash="14 10")
    o += dot(px(t0), py(v0), 9, WHITE, False)
    o += tag(px(t0) - 30, py(v0) - 52, "PRODUCE", WHITE, 20, "end")
    x, y = px(0.78), py(tl(0.78))
    o += dot(x, y)
    o += tag(x + 34, y - 14, "CONSUME")
    o += tag(px(0.13), py(0.42), "PPF", WHITE, 22)
    o += axes("GOOD X", "GOOD Y")
    return o, "BOTH SIDES END UP OUTSIDE THE CURVE"

def d_ch09():
    """Private vs social cost, with the wedge."""
    o  = curve([(px(0.05), py(0.95)), (px(1.02), py(0.10))], WHITE, 4.5)          # D
    o += curve([(px(0.05), py(0.10)), (px(1.02), py(0.80))], WHITE, 4.5, op=0.75) # private S
    o += curve([(px(0.05), py(0.40)), (px(1.02), py(1.10))], GOLD, 4.5)           # social S
    xm, ym = px(0.582), py(0.484)   # market eq
    xs, ys = px(0.394), py(0.648)   # social eq
    o += poly([(xs, ys), (xm, ym), (xm, py(0.784))], GOLD, 0.35, GOLD, 2)
    o += dot(xm, ym, 9, WHITE, False)
    o += dot(xs, ys)
    o += tag(px(1.02) + 10, py(1.10) + 4, "S", GOLD, 24)
    o += tag(px(1.02) + 10, py(0.80) + 6, "s", WHITE, 22)
    o += tag(px(1.02) + 10, py(0.10) + 6, "D", WHITE, 24)
    o += tag(xs - 14, ys - 26, "SOCIAL", GOLD, 20, "end")
    o += tag(xm + 26, ym + 30, "MARKET", WHITE, 20)
    o += axes("QUANTITY", "PRICE")
    return o, "THE COST NOBODY IS BILLED FOR"

def d_ch10():
    """Tax wedge + deadweight-loss triangle."""
    o  = curve([(px(0.05), py(0.95)), (px(1.02), py(0.10))], WHITE, 4.5)
    o += curve([(px(0.05), py(0.10)), (px(1.02), py(0.95))], WHITE, 4.5)
    qt = 0.40
    D  = lambda t: 0.95 - (t - 0.05) / 0.97 * 0.85
    S  = lambda t: 0.10 + (t - 0.05) / 0.97 * 0.85
    xb, yb = px(qt), py(D(qt))          # price buyers pay, on D
    xs, ys = px(qt), py(S(qt))          # price sellers keep, on S
    xe, ye = px(0.535), py(D(0.535))    # untaxed equilibrium
    o += f'<rect x="{OX:.1f}" y="{yb:.1f}" width="{xb-OX:.1f}" height="{ys-yb:.1f}" fill="{GOLD}" fill-opacity="0.26"/>'
    o += line(OX, yb, xb, yb, GOLD, 3, "8 8", 0.8)
    o += line(OX, ys, xs, ys, GOLD, 3, "8 8", 0.8)
    o += line(xb, yb, xs, ys, GOLD, 6)
    o += poly([(xb, yb), (xs, ys), (xe, ye)], "#FF5A5A", 0.45, "#FF8A8A", 2.5)
    o += dot(xe, ye, 8, WHITE, False)
    o += tag(OX + 26, (yb + ys)/2 + 8, "TAX REVENUE", GOLD, 20)
    o += tag(xe + 42, ye + 34, "LOST TRADES", "#FF9C9C", 20)
    o += axes("QUANTITY", "PRICE")
    return o, "SOMETHING IS ALWAYS LEFT ON THE TABLE"

def d_ch12():
    """Monopoly: D, MR, MC, profit rectangle."""
    o  = curve([(px(0.05), py(0.98)), (px(1.02), py(0.14))], WHITE, 4.5)          # D
    o += curve([(px(0.05), py(0.98)), (px(0.56), py(0.14))], GOLD, 4.5, dash="14 10")  # MR
    o += line(OX, py(0.32), px(1.02), py(0.32), WHITE, 4, op=0.75)               # MC
    qm = 0.451
    xq = px(qm); yp = py(0.633)
    o += f'<rect x="{OX:.1f}" y="{yp:.1f}" width="{xq-OX:.1f}" height="{py(0.32)-yp:.1f}" fill="{GOLD}" fill-opacity="0.24" stroke="{GOLD}" stroke-width="2"/>'
    o += guides(xq, yp)
    o += dot(xq, yp)
    o += tag(px(1.02) + 10, py(0.14) + 6, "D", WHITE, 24)
    o += tag(px(0.575), py(0.16), "MR", GOLD, 21)
    o += tag(px(1.02) + 10, py(0.32) + 8, "MC", WHITE, 22)
    o += tag(OX + 30, py(0.475), "PROFIT", GOLD, 21)
    o += txt(OX - 18, yp + 8, "Pm", 22, WHITE, "bold", "end", 0.9)
    o += txt(xq, OY + 40, "Qm", 22, WHITE, "bold", "middle", 0.9)
    o += axes("QUANTITY", "PRICE")
    return o, "ONE SELLER SETS THE PRICE"

CHAPTERS = [
    (1,  ["Principles and Practice", "of Economics"], 1, d_ch01),
    (3,  ["Optimization"],                            1, d_ch03),
    (4,  ["Demand, Supply,", "and Equilibrium"],      2, d_ch04),
    (5,  ["Consumers", "and Incentives"],             2, d_ch05),
    (6,  ["Sellers", "and Incentives"],               3, d_ch06),
    (7,  ["Perfect Competition", "and the Invisible Hand"], 3, d_ch07),
    (8,  ["Trade"],                                   4, d_ch08),
    (9,  ["Externalities", "and Public Goods"],       4, d_ch09),
    (10, ["Taxation", "and Regulation"],              5, d_ch10),
    (12, ["Monopoly"],                                5, d_ch12),
]

def build(ch, lines, week, dfn):
    diagram, caption = dfn()
    longest = max(len(s) for s in lines)
    size = 88 if longest <= 12 else (76 if longest <= 22 else 62)
    lead = size * 1.16
    top = 470 - (len(lines) - 1) * lead / 2

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    o.append(f'''<defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="{NAVY_D}"/><stop offset="55%" stop-color="{NAVY}"/><stop offset="100%" stop-color="#012B70"/>
      </linearGradient>
      <radialGradient id="glow" cx="0.72" cy="0.30" r="0.62">
        <stop offset="0%" stop-color="#1E63D8" stop-opacity="0.42"/><stop offset="100%" stop-color="#1E63D8" stop-opacity="0"/>
      </radialGradient>
      <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
        <path d="M 60 0 L 0 0 0 60" fill="none" stroke="#FFFFFF" stroke-opacity="0.055" stroke-width="1"/>
      </pattern>
    </defs>''')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#glow)"/>')

    # oversized chapter numeral, ghosted behind the left column
    o.append(txt(96, 1010, f"{ch:02d}", 460, WHITE, "bold", "start", 0.045))

    # left column
    o.append(f'<rect x="112" y="270" width="104" height="11" fill="{GOLD}" rx="2"/>')
    o.append(txt(112, 348, f"CHAPTER {ch:02d}", 30, GOLD, "bold", "start", 1.0, 7))
    for i, s in enumerate(lines):
        o.append(txt(112, top + i * lead, s, size, WHITE, "bold", "start", 1.0, -0.5))
    ruley = top + (len(lines) - 1) * lead + 62
    o.append(f'<rect x="112" y="{ruley:.0f}" width="330" height="5" fill="{GOLD}" rx="2"/>')
    o.append(txt(112, ruley + 66, "ECON 003 · Introduction to Microeconomics", 30, WHITE, "normal", "start", 0.88))
    o.append(txt(112, 946, f"WEEK {week}  ·  UC RIVERSIDE  ·  SUMMER SESSION B 2026", 21, WHITE, "bold", "start", 0.5, 3.5))

    # right panel
    o.append(f'<rect x="{PX0}" y="{PY0}" width="{PW_}" height="{PH_}" rx="18" fill="#FFFFFF" fill-opacity="0.055" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="2"/>')
    o.append(txt(PX0 + 40, PY0 + 62, caption, 21, GOLD, "bold", "start", 1.0, 3))
    o.append(f'<rect x="{PX0+40}" y="{PY0+84}" width="56" height="4" fill="{GOLD}" fill-opacity="0.75" rx="2"/>')
    o.append(diagram)
    o.append('</svg>')
    return "\n".join(o)

if __name__ == "__main__":
    out = "/home/claude/art/svg"
    os.makedirs(out, exist_ok=True)
    for ch, lines, week, dfn in CHAPTERS:
        s = build(ch, lines, week, dfn)
        with open(f"{out}/ECON003_Ch{ch:02d}_cover.svg", "w") as f:
            f.write(s)
    print("wrote", len(CHAPTERS), "svgs")
