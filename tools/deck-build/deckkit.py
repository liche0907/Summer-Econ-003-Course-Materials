"""
deckkit.py — slide construction kit for ECON 003 (UCR).

Rebuilt for Chapter 5 by measuring ECON003_Ch04_Demand_Supply_Equilibrium_UCR_v3.pptx.
Every geometry constant below was read out of that file's XML, not recalled.
Conventions live in claude/slide-ground-rules.md.

Canvas 10.000 x 5.625 in. Arial throughout. Metric-aware auto-fit uses Liberation Sans,
which is metric-compatible with Arial.
"""
from __future__ import annotations

import copy
import re

from PIL import Image, ImageFont
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

# ----------------------------------------------------------------------------- palette
BLUE = "003DA5"      # UCR blue - titles, demand curves, takeaways field
GOLD = "FFB81D"      # UCR gold - accent bars
DGOLD = "B88300"     # dark gold - gold text on white
GREEN = "2E7D32"     # correct / benefit / positive
RED = "CC3333"       # wrong / cost / negative, and supply curves
INK = "333333"
INK2 = "444444"
GREY = "666666"
GREY2 = "999999"
RULE = "DDDDDD"
WHITE = "FFFFFF"
TINT_BLUE = "F2F6FC"
TINT_NEUTRAL = "F7F7F7"
TINT_RED = "FDF4F4"
TINT_GREEN = "F1F8F1"
TINT_GOLD = "FFF6E0"

# ------------------------------------------------------------------------- geometry
SLIDE_W, SLIDE_H = 10.0, 5.625
M = 0.60                       # left margin
CONTENT_W = 8.80               # full-width panel
TITLE_W = 8.70
TITLE_FIT_W = 8.50            # measure titles against this, not TITLE_W

TAB = dict(x=0.60, y=0.25, w=0.60, h=0.06)
TITLE_BOX = dict(x=0.60, y=0.48, w=8.70, h=0.54)

CARD_X3 = (0.60, 3.70, 6.80)
CARD_W3 = 2.60
CARD_X2 = (0.60, 5.20)
CARD_W2 = 4.20
STRIP_X5 = (0.60, 2.36, 4.12, 5.88, 7.64)
STRIP_W5 = 1.66

CARD_PAD_X = 0.18              # 164592 EMU
CARD_PAD_Y = 0.23              # 210312 EMU
LABEL_GAP = 173736 / 914400    # 0.19 in, measured constant between label and body
CARD_PAD_B = 128017 / 914400   # 0.14 in, bottom inset of the body box

# single-line spAutoFit height PowerPoint writes = 1.25 x font size
LINE_FACTOR = 1.25

_FONT_CACHE: dict[tuple[bool, int], ImageFont.FreeTypeFont] = {}
_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
_BLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


# ------------------------------------------------------------------------ metrics
def _font(size_pt: float, bold: bool) -> ImageFont.FreeTypeFont:
    """Liberation Sans at 4x scale for sub-point measurement precision."""
    key = (bold, int(round(size_pt * 4)))
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ImageFont.truetype(_BLD if bold else _REG, key[1])
    return _FONT_CACHE[key]


def text_width_in(s: str, size_pt: float, bold: bool = False) -> float:
    """Width of s in inches when set in Arial at size_pt."""
    if not s:
        return 0.0
    f = _font(size_pt, bold)
    return f.getlength(s) / 4.0 / 72.0


def wrap(text: str, width_in: float, size_pt: float, bold: bool = False) -> list[str]:
    """Greedy wrap to width_in. Honours explicit newlines already in text."""
    out: list[str] = []
    for para in text.split("\n"):
        if not para.strip():
            out.append("")
            continue
        words, line = para.split(), ""
        for w in words:
            trial = f"{line} {w}".strip()
            if text_width_in(trial, size_pt, bold) <= width_in or not line:
                line = trial
            else:
                out.append(line)
                line = w
        out.append(line)
    return out


# Arial's default single-spaced line box is ~1.2 x the point size. Multiply by the
# paragraph line-spacing percentage to get the real rendered height. Measured against
# LibreOffice renders of the Ch04 deck; the earlier 1.0 factor under-ran by ~17% and
# let card bodies spill past their panels.
LINE_H = 1.20


def text_h(n_lines: int, size_pt: float, line_pct: float = 1.0) -> float:
    """Rendered height in inches of n_lines at size_pt with the given line spacing."""
    return n_lines * size_pt * LINE_H * max(line_pct, 1.0) / 72.0


def fit_size(text: str, width_in: float, height_in: float, start_pt: float,
             min_pt: float, line_pct: float = 1.30, bold: bool = False) -> tuple[float, list[str]]:
    """Largest size in [min_pt, start_pt] at which the wrapped text fits height_in."""
    size = start_pt
    while size >= min_pt:
        lines = wrap(text, width_in, size, bold)
        if text_h(len(lines), size, line_pct) <= height_in:
            return size, lines
        size -= 0.5
    return min_pt, wrap(text, width_in, min_pt, bold)


def fit_one_line(text: str, width_in: float, start_pt: float, min_pt: float,
                 bold: bool = True) -> float:
    """Largest size at which text stays on ONE line inside width_in."""
    size = start_pt
    while size > min_pt and text_width_in(text, size, bold) > width_in:
        size -= 0.5
    return size


def autofit_h(n_lines: int, size_pt: float, line_pct: float = 1.0) -> float:
    """Height in inches PowerPoint's spAutoFit would write for n_lines."""
    if line_pct <= 1.0:
        return n_lines * size_pt * LINE_FACTOR / 72.0
    return n_lines * size_pt * line_pct * LINE_FACTOR / 1.25 / 72.0


# ------------------------------------------------------------------------ raw XML
def _rgb(h: str) -> RGBColor:
    return RGBColor.from_string(h)


def rect(slide, x, y, w, h, fill=None, line=None, line_w=9525):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                Inches(w), Inches(h))
    sh.shadow.inherit = False
    if fill:
        sh.fill.solid()
        sh.fill.fore_color.rgb = _rgb(fill)
    else:
        sh.fill.background()
    if line:
        sh.line.color.rgb = _rgb(line)
        sh.line.width = Emu(line_w)
    else:
        sh.line.fill.background()
    return sh


def textbox(slide, x, y, w, h, runs, size=12, bold=False, color=INK,
            align="l", line_pct=None, anchor="t", italic=False):
    """runs: a string, or a list of (text, dict-of-overrides) tuples per line."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "ctr": MSO_ANCHOR.MIDDLE,
                          "b": MSO_ANCHOR.BOTTOM}[anchor]

    lines = runs if isinstance(runs, list) else [(l, {}) for l in str(runs).split("\n")]
    algn = {"l": PP_ALIGN.LEFT, "ctr": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]

    for i, item in enumerate(lines):
        txt, over = item if isinstance(item, tuple) else (item, {})
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = over.get("align_p", algn)
        if line_pct:
            p.line_spacing = line_pct
        r = p.add_run()
        r.text = txt
        f = r.font
        f.name = "Arial"
        f.size = Pt(over.get("size", size))
        f.bold = over.get("bold", bold)
        f.italic = over.get("italic", italic)
        f.color.rgb = _rgb(over.get("color", color))
    return tb


# ------------------------------------------------------------- standing patterns
def title(slide, text, tab_color=GOLD):
    """Title accent tab + title text. Shrinks to stay on ONE line, never wraps."""
    rect(slide, TAB["x"], TAB["y"], TAB["w"], TAB["h"], fill=tab_color)
    # Fit against TITLE_FIT_W (8.50), not the box's 8.70: a title measured at exactly
    # the box width still wraps once the renderer rounds. Ch04 lost a title to that.
    size = fit_one_line(text, TITLE_FIT_W, 32, 19, bold=True)
    h = autofit_h(1, size)
    textbox(slide, TITLE_BOX["x"], TITLE_BOX["y"], TITLE_W, h, text,
            size=size, bold=True, color=BLUE, anchor="ctr")
    return size


def defbox(slide, y, text, tint=TINT_BLUE, border=BLUE, color=BLUE, size=17,
           width=CONTENT_W, x=M):
    """Full-width definition panel. Height grows to fit its own text."""
    inner_x, inner_w = x + 0.30, width - 0.60
    size, lines = size, []
    for para in text.split("\n"):
        lines.extend(wrap(para, inner_w, size, bold=True) or [""])
    h = max(text_h(len(lines), size, 1.25) + 0.22, 0.60)
    rect(slide, x, y, width, h, fill=tint, line=border)
    textbox(slide, inner_x, y, inner_w, h, "\n".join(lines),
            size=size, bold=True, color=color, align="ctr", line_pct=1.25, anchor="ctr")
    return y + h


def _card(slide, x, y, w, h, accent, label, body, body_size=12, label_size=None,
          icon=None, body_color=INK2, fill=WHITE, border=RULE):
    rect(slide, x, y, w, h, fill=fill, line=border)
    rect(slide, x, y, w, 0.06, fill=accent)
    inner_x = x + CARD_PAD_X
    inner_w = w - 2 * CARD_PAD_X
    # An icon sits top-right inside the card, so the label may not run under it.
    label_w = inner_w - (0.42 if icon else 0.0)
    lsize = label_size or (13 if accent == BLUE else 12)
    lsize = fit_one_line(label, label_w, lsize, 9, bold=True)
    llines = wrap(label.upper(), label_w, lsize, bold=True)
    lh = text_h(len(llines), lsize, 1.15)
    ly = y + CARD_PAD_Y
    lcolor = DGOLD if accent == GOLD else (accent if accent in (BLUE, GREEN, RED) else GREY)
    textbox(slide, inner_x, ly, label_w, lh, "\n".join(llines),
            size=lsize, bold=True, color=lcolor, line_pct=1.15)
    by = ly + lh + LABEL_GAP
    bh = (y + h - CARD_PAD_B) - by
    if body:
        bsize, blines = fit_size(body, inner_w, bh, body_size, 8.0, 1.28)
        textbox(slide, inner_x, by, inner_w, bh, "\n".join(blines),
                size=bsize, color=body_color, line_pct=1.28)
    if icon:
        slide.shapes.add_picture(icon, Inches(x + w - 0.46), Inches(y + 0.17),
                                 Inches(0.28), Inches(0.28))


def cards3(slide, y, h, items, body_size=12):
    """items: list of (accent, LABEL, body[, icon])"""
    for x, it in zip(CARD_X3, items):
        acc, lab, body = it[0], it[1], it[2]
        icon = it[3] if len(it) > 3 else None
        _card(slide, x, y, CARD_W3, h, acc, lab, body, body_size, icon=icon)


def cards2(slide, y, h, items, body_size=12, width=CARD_W2, xs=CARD_X2):
    for x, it in zip(xs, items):
        acc, lab, body = it[0], it[1], it[2]
        icon = it[3] if len(it) > 3 else None
        fill = it[4] if len(it) > 4 else WHITE
        _card(slide, x, y, width, h, acc, lab, body, body_size, icon=icon, fill=fill)


def cards4(slide, y, h, items, body_size=11.5):
    xs = (0.60, 2.83, 5.06, 7.29)
    for x, it in zip(xs, items):
        acc, lab, body = it[0], it[1], it[2]
        icon = it[3] if len(it) > 3 else None
        _card(slide, x, y, 2.11, h, acc, lab, body, body_size, icon=icon)


def strip5(slide, y, items, icon_dir=None, label_size=10, h=1.30):
    """items: list of (label_two_lines, icon_path_or_None)"""
    for x, (label, icon) in zip(STRIP_X5, items):
        if icon:
            slide.shapes.add_picture(icon, Inches(x + STRIP_W5 / 2 - 0.19),
                                     Inches(y), Inches(0.38), Inches(0.38))
        lines = wrap(label, STRIP_W5 - 0.05, label_size, bold=True)
        textbox(slide, x, y + 0.50, STRIP_W5, text_h(len(lines), label_size, 1.2),
                "\n".join(lines), size=label_size, bold=True, color=BLUE,
                align="ctr", line_pct=1.2)


def kicker(slide, text, y=4.45, width=CONTENT_W, x=M, size=13, color=INK):
    """Bottom hairline rule + one bold centred sentence. The 'so what' of the slide."""
    rect(slide, x, y, width, 0.06, fill=RULE)
    lines = wrap(text, width, size, bold=True)
    textbox(slide, x, y + 0.18, width, text_h(len(lines), size, 1.2),
            "\n".join(lines), size=size, bold=True, color=color,
            align="ctr", line_pct=1.2)


def blue_field(slide):
    """Solid UCR-blue slide background. Section dividers and the takeaways page only."""
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = _rgb(BLUE)


def divider(slide, part, headline):
    """Section divider on the blue field. Geometry lifted from Ch03 slides 6/16/30.

    PART n is 16 pt REGULAR gold, not bold - the headline carries the weight.
    """
    blue_field(slide)
    rect(slide, 4.20, 1.50, 1.60, 0.06, fill=GOLD)
    textbox(slide, 0, 1.70, SLIDE_W, 0.50, part, size=16, bold=False,
            color=GOLD, align="ctr")
    lines = [l for l in headline.split("\n")]
    size = 40
    while size > 26 and any(text_width_in(l, size, True) > 9.0 for l in lines):
        size -= 0.5
    textbox(slide, 0, 2.30, SLIDE_W, text_h(len(lines), size, 1.15),
            "\n".join(lines), size=size, bold=True, color=WHITE, align="ctr",
            line_pct=1.15)


def band(slide, y, text, kind="formula", size=15, x=M, width=CONTENT_W, pad=0.22):
    """Bordered strip. kind: formula (blue) / answer (green) / flag (red) / note (gold)."""
    style = {
        "formula": (TINT_BLUE, BLUE, BLUE),
        "answer": (TINT_GREEN, GREEN, GREEN),
        "flag": (TINT_RED, RED, RED),
        "note": (TINT_GOLD, DGOLD, DGOLD),
        "neutral": (TINT_NEUTRAL, RULE, INK),
    }[kind]
    inner_w = width - 2 * pad - 0.16
    lines: list[str] = []
    for para in text.split("\n"):
        lines.extend(wrap(para, inner_w, size, bold=True) or [""])
    h = text_h(len(lines), size, 1.25) + 0.22
    rect(slide, x, y, width, h, fill=style[0], line=style[1])
    textbox(slide, x + pad + 0.08, y, inner_w, h, "\n".join(lines),
            size=size, bold=True, color=style[2], align="ctr",
            line_pct=1.25, anchor="ctr")
    return y + h


def table(slide, x, y, w, h, rows, col_w, header_fill=INK, header_size=10,
          body_size=9.5, first_col_fill=None, first_col_bold=True,
          zebra=True, align=None, row_h=None):
    """rows[0] is the header row."""
    gf = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y),
                                Inches(w), Inches(h))
    tbl = gf.table
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Inches(cw)
    hdr_h = row_h or 0.38
    tbl.rows[0].height = Inches(hdr_h)
    body_h = (h - hdr_h) / max(1, len(rows) - 1)
    for r in range(1, len(rows)):
        tbl.rows[r].height = Inches(body_h)

    # kill the default banded table style
    tblPr = tbl._tbl.find(qn("a:tblPr"))
    if tblPr is not None:
        tblPr.set("firstRow", "1")
        tblPr.set("bandRow", "0")

    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.10)
            cell.margin_top = cell.margin_bottom = Inches(0.05)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if r == 0:
                fill_c, txt_c, bold, sz = header_fill, WHITE, True, header_size
            elif c == 0 and first_col_fill:
                fill_c, txt_c, bold, sz = first_col_fill, WHITE, first_col_bold, body_size
            else:
                fill_c = (WHITE if (r % 2 == 1 or not zebra) else TINT_NEUTRAL)
                txt_c, bold, sz = INK, False, body_size
            cell.fill.solid()
            cell.fill.fore_color.rgb = _rgb(fill_c)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = {"l": PP_ALIGN.LEFT, "ctr": PP_ALIGN.CENTER,
                           "r": PP_ALIGN.RIGHT}[(align or ["l"] * len(row))[c]]
            run = p.add_run()
            run.text = str(val)
            run.font.name = "Arial"
            run.font.size = Pt(sz)
            run.font.bold = bold
            run.font.color.rgb = _rgb(txt_c)
    return gf


def picture(slide, path, x, y, w, h=None):
    if h is None:
        return slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w))
    return slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))


def picture_fit(slide, path, x, y, max_w, max_h, align="ctr"):
    """Scale a figure to fit inside a box, preserving aspect, and centre it there.

    matplotlib's bbox_inches='tight' means the saved aspect ratio is NOT the figsize
    that produced it, so sizing on width alone silently pushes axis labels through the
    bottom rule. Read the real pixel dimensions instead.
    """
    with Image.open(path) as im:
        pw, ph = im.size
    scale = min(max_w / pw, max_h / ph)
    w, h = pw * scale, ph * scale
    if align == "ctr":
        x = x + (max_w - w) / 2
    y = y + (max_h - h) / 2
    return slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))


def credit(slide, text, x=M, y=5.20, width=CONTENT_W, align="l"):
    """A non-attributive source line. Publisher attribution does NOT go here - it goes
    in the speaker notes. The only publisher credit allowed on a slide face is
    image_credit() below."""
    textbox(slide, x, y, width, 0.16, text, size=7, color=GREY2, align=align)


IMAGE_CREDIT = "Image: Acemoglu, Laibson & List, Microeconomics 3e"


def image_credit(slide):
    """The one piece of on-slide attribution the ground rules permit: 7 pt, bottom-right
    at y=5.40. Names the book, not the publisher. Every slide carrying a publisher
    photograph gets exactly this and nothing else."""
    textbox(slide, M, 5.40, CONTENT_W, 0.20, IMAGE_CREDIT,
            size=7, color=GREY2, align="r")


# ------------------------------------------------------------------ photographs
# Their photographs, our charts. Feature size, never a thumbnail: a picture is a UNIT
# of image + hairline frame + caption, and a unit of 8 sq in or more reads as the
# slide's main figure. The deprecated photo_strip pattern produced postage stamps and
# is not used for photographs.

def photo(slide, path, x, y, max_w, max_h, frame=True, align="ctr"):
    """Fit a photograph into a box preserving aspect, with a #DDDDDD hairline frame.

    Returns (x, y, w, h) of the placed picture so a caption can be hung off it.
    """
    with Image.open(path) as im:
        pw, ph = im.size
    scale = min(max_w / pw, max_h / ph)
    w, h = pw * scale, ph * scale
    if align == "ctr":
        x = x + (max_w - w) / 2
    slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
    if frame:
        rect(slide, x, y, w, h, fill=None, line=RULE)
    return x, y, w, h


def photo_split(slide, path, x, y, max_w, max_h, caption, cap_size=10.5):
    """Photograph with a one-line caption beneath it, centred on the picture.

    Captions stay to ONE line and about 0.30 in high on purpose - the animation pass
    tells a caption from a card body by point size and height.
    """
    px, py, pw, ph = photo(slide, path, x, y, max_w, max_h)
    cap_size = fit_one_line(caption, max(pw, 1.4), cap_size, 8, bold=False)
    textbox(slide, px, py + ph + 0.06, pw, 0.30, caption,
            size=cap_size, color=GREY, align="ctr")
    return px, py, pw, ph


def photo_question(slide, path, px, py, pw, ph, qx, qy, qw,
                   question, body, q_size=15):
    """Wide-band photograph with a posed question set large beside it.

    For the publisher's live-classroom prompts. The lectures are recorded, so the
    question goes on the SLIDE (14-15 pt) and the instruction to pause goes in the
    notes. Never label it as theirs.
    """
    photo(slide, path, px, py, pw, ph)
    lines = [(question, {"size": q_size, "bold": True, "color": DGOLD}), ("", {})]
    for ln in wrap(body, qw, 11.5):
        lines.append((ln, {"size": 11.5, "bold": False, "color": INK2}))
    textbox(slide, qx, qy, qw, 1.60, lines, line_pct=1.25)


# ------------------------------------------------------------------ clip pages
# A clip gets TWO consecutive slides: the clip alone, then the analysis. Page 1 carries
# no diagram on purpose - while the clip runs the screen should be the clip. Linked,
# never embedded: embedded media carries its own p:timing, which fights the animation
# pass and inflates the file.

def hyperlink(shape_or_run, url):
    """Attach a hyperlink to a run (works for both http URLs and relative file paths)."""
    shape_or_run.hyperlink.address = url


def clip_page(slide, source_label, blurb, url, url_label=None, watch_for=None):
    """Page 1 of a clip pair: a large play panel, the source, a one-line blurb, the
    link, and one gold 'watch for' band. No diagram, no cards.

    `url` may be an http link or a path relative to the .pptx (for a local mp4).
    """
    panel_y, panel_h = 1.15, 2.72
    rect(slide, M, panel_y, CONTENT_W, panel_h, fill=TINT_NEUTRAL, line=RULE)

    # The panel stacks label -> play mark -> blurb -> link, top to bottom, with the
    # link pinned near the panel floor so a three-line blurb still clears it.
    cx, cy = SLIDE_W / 2, panel_y + 0.87
    disc = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - 0.42), Inches(cy - 0.42),
                                  Inches(0.84), Inches(0.84))
    disc.shadow.inherit = False
    disc.fill.solid()
    disc.fill.fore_color.rgb = _rgb(GOLD)
    disc.line.fill.background()
    tri = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE,
                                 Inches(cx - 0.15), Inches(cy - 0.19),
                                 Inches(0.34), Inches(0.38))
    tri.shadow.inherit = False
    tri.rotation = 90
    tri.fill.solid()
    tri.fill.fore_color.rgb = _rgb(WHITE)
    tri.line.fill.background()

    textbox(slide, M, panel_y + 0.22, CONTENT_W, 0.24, f"CLIP  ·  {source_label.upper()}",
            size=11, bold=True, color=GREY, align="ctr")

    blines = wrap(blurb, 7.40, 13, bold=True)   # the blurb renders bold - measure it bold
    textbox(slide, 1.30, cy + 0.56, 7.40, text_h(len(blines), 13, 1.25),
            "\n".join(blines), size=13, bold=True, color=INK, align="ctr", line_pct=1.25)

    tb = textbox(slide, M, panel_y + panel_h - 0.38, CONTENT_W, 0.22,
                 url_label or url, size=10, color=BLUE, align="ctr")
    tb.text_frame.paragraphs[0].runs[0].hyperlink.address = url

    if watch_for:
        band(slide, 4.12, watch_for, kind="note", size=13.5)


# ------------------------------------------------------------------ closing pair
def recap_table(slide, chapter_line, rows, closing):
    """'Chapter N: The Full Picture' - the hour re-indexed as one grid."""
    title(slide, chapter_line)
    header = ["", "What it says", "Key terms", "Where you saw it"]
    table(slide, 0.35, 1.15, 9.30, 3.31, [header] + rows,
          col_w=[1.55, 3.20, 2.15, 2.40], first_col_fill=BLUE, header_size=10,
          body_size=9.5)
    lines = wrap(closing, 9.30, 12.5, bold=True)
    textbox(slide, 0.35, 4.62, 9.30, text_h(len(lines), 12.5, 1.15),
            "\n".join(lines), size=12.5, bold=True, color=INK, align="ctr",
            line_pct=1.15)


def takeaways_page(slide, chapter_line, bullets):
    """The blue field. Five bullets is the house length."""
    blue_field(slide)

    rect(slide, 3.50, 0.40, 3.00, 0.06, fill=GOLD)
    textbox(slide, 0, 0.60, SLIDE_W, 0.40, "KEY TAKEAWAYS", size=14, bold=True,
            color=GOLD, align="ctr", anchor="ctr")
    # starts at 40 pt and shrinks to fit 9.00 in - Ch04's line lands at 30.5
    size = fit_one_line(chapter_line, 9.00, 40, 20, bold=True)
    textbox(slide, 0, 1.00, SLIDE_W, autofit_h(1, size), chapter_line,
            size=size, bold=True, color=WHITE, align="ctr", anchor="ctr")
    y = 1.95
    for b in bullets:
        rect(slide, 1.10, y, 0.25, 0.25, fill=GOLD)
        lines = wrap(b, 7.60, 13.5)
        textbox(slide, 1.60, y - 0.05, 7.60, text_h(len(lines), 13.5, 1.2),
                "\n".join(lines), size=13.5, color=WHITE, line_pct=1.2, anchor="ctr")
        y += 0.62


# ------------------------------------------------------------------------ notes
_TIMING = re.compile(r"^\s*\[?\d{1,2}:\d{2}\s*[–\-—]\s*\d{1,2}:\d{2}\]?\s*", re.M)


def notes(slide, text):
    """Speaker notes. Strips any timing marker on the way in - see ground rules S4."""
    cleaned = _TIMING.sub("", text).strip()
    slide.notes_slide.notes_text_frame.text = cleaned


# ------------------------------------------------------------------ deck plumbing
def blank_slide(prs):
    layout = next(l for l in prs.slide_masters[0].slide_layouts if l.name == "DEFAULT")
    s = prs.slides.add_slide(layout)
    for shp in list(s.shapes):
        shp._element.getparent().remove(shp._element)
    return s


def drop_slides_after(prs, keep):
    """Delete every slide past index `keep`-1, cleanly (rels included)."""
    xml_slides = prs.slides._sldIdLst
    ids = list(xml_slides)
    for sldId in ids[keep:]:
        rId = sldId.get(qn("r:id"))
        prs.part.drop_rel(rId)
        xml_slides.remove(sldId)


def retitle_title_slide(slide, chapter_line, subtitle_lines):
    """Change ONLY the words on the copied title card. Never move anything."""
    def _retext(shape, new_lines):
        """Replace text run-by-run, preserving every run's formatting.

        The Ch04 title card puts 'ECON 003' and the campus line in two RUNS of one
        paragraph, not two paragraphs - blanking run 2 silently drops the campus line.
        So walk runs across all paragraphs in order and refill them one line each.
        """
        runs = [r for p in shape.text_frame.paragraphs for r in p.runs]
        for i, run in enumerate(runs):
            run.text = new_lines[i] if i < len(new_lines) else ""

    for sh in slide.shapes:
        if not sh.has_text_frame or not sh.text_frame.text.strip():
            continue
        t = sh.text_frame.text
        if t.strip().lower().startswith("chapter"):
            _retext(sh, chapter_line)
        elif "ECON 003" in t:
            _retext(sh, subtitle_lines)
