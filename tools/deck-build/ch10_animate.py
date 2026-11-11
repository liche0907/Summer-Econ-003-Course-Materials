#!/usr/bin/env python3
"""ch10_animate.py - the animation pass for Chapter 10, run on HIS edited v3.

`ch07_animate.py` with four changes, and every one of them is his instruction:

  1. PICTURES STEP WITH THEIR TEXT, not as leftovers.  The clusterer already
     attaches a picture to the card it sits in or beside; what it cannot do is know
     what a picture MEANS.  Nearest-centre geometry put the corruption photograph on
     slide 20 into the KICKER's step (its centre is 0.09 in from the kicker's, and
     1.68 in from its own card's), which would have shown a money-bag handshake
     while the sentence about deadweight loss came up.  So the seven pictures he
     pasted in carry an explicit owner - see OWNER below, with what each one is.

  2. A PICTURE THAT COVERS TEXT IS HIDDEN WHEN THAT TEXT ARRIVES.  Computed, not
     declared: every picture is tested against every text box, and where it covers
     one that appears in a LATER step, an EXIT is folded into that later step.  One
     click both hides the picture and shows the sentence.  Only slide 20 triggers
     it - his three photographs sit across the kicker AND across the last line of
     their own cards' bodies.

  3. Steps may now MIX entry and exit effects, which (2) needs.  `timing_xml` took
     one mode for a whole step; it now takes a mode per shape.

  4. SLIDES 11 AND 17 ARE SKIPPED.  He built two clip pages with embedded video and
     PowerPoint has written its own `p:timing` on both.  Ground rules S5: never
     overwrite it - doing so breaks playback.  Slide 17's still photograph therefore
     stays static too, which is the honest trade.

Everything else is ch07's: click-triggered Appear only, Ch03's behaviour (title, tab
and definition box static; one click per card left to right; the kicker last; the
main figure static because it is the setting the argument is built on), the two
thin-shape fixes, and geometry-only clustering with no naming convention to maintain.

Run:  python3 ch10_animate.py <in.pptx> <out.pptx>
"""
import sys
import re
import zipfile

from pptx import Presentation
from pptx.oxml.ns import qn

SRC = sys.argv[1] if len(sys.argv) > 1 else "v2_slide5fixed.pptx"
DST = sys.argv[2] if len(sys.argv) > 2 else "ch07_animated.pptx"

STATIC_TYPES = {"PICTURE", "TABLE", "MEDIA", "GROUP", "CHART"}
ROADMAP = 3           # "Three Questions, One Hour" -- static in Ch03, so static here
RECAP = 21            # "Chapter 10: The Full Picture"
CLIP_PAGES = set()    # his two clip pages are handled by SKIP, not by this
SKIP = {11, 17}       # embedded video: PowerPoint owns their p:timing (S5)

# What each picture he pasted in MEANS, and therefore which step it belongs to.
# The value is matched against the step's label (its first line of text).  This is
# the one place in the pass where meaning beats geometry, and it is needed because
# a photograph placed under a card row is nearer to the kicker than to its card.
OWNER = {
    (5, 11):  "TAX INCIDENCE",       # three retail receipts -> the who-remits paragraph
    (16, 18): "DIRECT REGULATION",   # FDA APPROVED stamps -> the FDA is named in that card
    (16, 20): "PRICE CONTROLS",      # a MINIMUM WAGE ballot box -> a price floor
    (16, 19): "PRICE CONTROLS",      # a storefront papered with RENT / SUSPEND notices
    (20, 23): "BUREAUCRATIC COST",   # an office drowning in paperwork
    (20, 24): "CORRUPTION",          # a handshake with a money bag held behind the back
    (20, 25): "THE UNDERGROUND",     # gloved hands with a taped brick
}
# Section dividers are found by their solid blue background, so cutting or adding a
# part does not need a constant changed here. The takeaways page is also blue and is
# the last slide, which is how it stays animated -- five clicks, one bullet each.


# ---------------------------------------------------------------- geometry ---
def box(sh):
    return ((sh.left or 0) / 914400, (sh.top or 0) / 914400,
            (sh.width or 0) / 914400, (sh.height or 0) / 914400)


def area(b):
    return max(b[2], 0) * max(b[3], 0)


def inter(a, b):
    ix = max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))
    return ix * iy


def overlaps(a, b):
    i = inter(a, b)
    if i <= 0:
        return False
    # A hairline is decoration on whatever CONTAINS it -- a card's accent bar belongs
    # to that card's panel. Judging it by area fraction instead merges it with
    # anything that merely overhangs it, and on slide 41 a question text box whose
    # auto-fit height runs four hundredths of an inch past the top of the card row
    # below it dragged BOTH cards into the same click as the question. Require a
    # hairline to be essentially inside the other shape before uniting them.
    if min(a[3], b[3]) <= 0.09:
        small = a if a[3] <= b[3] else b
        return i >= 0.90 * area(small)
    return i > 0.45 * min(area(a), area(b))


def near_below(a, b):
    """A hairline rule sitting directly above its kicker line."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ah <= 0.09 and 0 < by - (ay + ah) < 0.30 and abs(ax - bx) < 0.6 \
        and abs(aw - bw) < 1.2


def near_right(a, b):
    """A small bullet square and the text immediately to its right."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    if aw > 0.32 or ah > 0.32:
        return False
    return 0 <= bx - (ax + aw) < 0.75 \
        and abs((ay + ah / 2) - (by + bh / 2)) < 0.28


def maxpt(sh):
    if not sh.has_text_frame:
        return None
    v = [r.font.size.pt for p in sh.text_frame.paragraphs
         for r in p.runs if r.font.size]
    return max(v) if v else None


# ---------------------------------------------------------------- clustering --
DOMINANT = 8.0        # sq in -- the slide's main figure; it frames, it does not step
SATELLITE_LONG = 2.5  # in    -- above this it is a photograph, not a spot icon
SATELLITE_AREA = 3.5  # sq in
REACH = 3.2           # in    -- how far a spot icon may look for its card
ADJACENT = 1.5        # in    -- horizontal gap a row-aligned picture may bridge
TUCKED = 0.8          # in    -- a lone card only adopts a picture this close
ICON_LONG = 0.62      # in    -- a glyph this small is decoration, placed first
ICON_AREA = 0.50      # sq in
ICON_REACH = 1.30     # in    -- how far a glyph may look for its owner


def structural(it):
    """Frame furniture -- present from the moment the slide opens."""
    x, y, w, h = it["b"]
    return ((y < 0.45 and h < 0.12)                     # gold tab / divider rule
            or (0.35 <= y <= 0.62 and w > 7.5)          # title
            or (0.95 <= y <= 1.40 and w > 8.0)          # definition box
            or (y >= 5.05 and (it["pt"] or 99) <= 8))   # credit / source line


def build_units(items):
    """A picture is not a bare shape: it comes with its hairline frame and its
    caption, and the three must always move together."""
    panels = [it["b"] for it in items
              if it["kind"] == "AUTO_SHAPE" and not it["txt"] and area(it["b"]) >= 1.0
              and not any(o["kind"] == "PICTURE"
                          and inter(it["b"], o["b"]) > 0.60 * area(it["b"])
                          for o in items)]

    units = []
    taken = set()
    for it in items:
        if it["kind"] not in ("PICTURE", "TABLE", "GROUP") or it["i"] in taken:
            continue
        grp = [it]
        taken.add(it["i"])
        for o in items:
            if o["i"] in taken or o["kind"] not in ("AUTO_SHAPE", "TEXT_BOX"):
                continue
            if structural(o) or area(o["b"]) <= 0:
                continue
            ox, oy, ow, oh = o["b"]
            px, py, pw, ph = it["b"]
            if not o["txt"] and inter(o["b"], it["b"]) > 0.60 * area(o["b"]):
                grp.append(o)
                taken.add(o["i"])
                continue
            hoverlap = max(0, min(ox + ow, px + pw) - max(ox, px))
            in_panel = any(inter(o["b"], p) > 0.75 * area(o["b"]) for p in panels)
            if (o["txt"] and (o["pt"] or 99) <= 11.5 and oh <= 0.35 and not in_panel
                    and hoverlap > 0.5 * min(ow, pw)
                    and (0 <= oy - (py + ph) < 0.9 or 0 <= py - (oy + oh) < 0.9)):
                grp.append(o)
                taken.add(o["i"])
        grp.sort(key=lambda k: k["i"])
        units.append(grp)
    return units, taken


def collect(slide):
    items = []
    for idx, sh in enumerate(slide.shapes):
        items.append(dict(i=idx, id=sh.shape_id, kind=str(sh.shape_type).split()[0],
                          b=box(sh), pt=maxpt(sh),
                          txt=sh.text_frame.text.strip() if sh.has_text_frame else "",
                          sh=sh))
    return items


def steps_for(slide, sno=0):
    items = collect(slide)
    units, in_unit = build_units(items)

    for it in items:
        it["static"] = (
            it["i"] in in_unit
            or it["kind"] in STATIC_TYPES
            or structural(it)
            or not (it["txt"] or it["kind"] == "AUTO_SHAPE")
        )

    live = [it for it in items if not it["static"]]
    parent = {it["i"]: it["i"] for it in live}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for a in live:
        for b in live:
            if a["i"] >= b["i"]:
                continue
            if (overlaps(a["b"], b["b"])
                    or near_below(a["b"], b["b"]) or near_below(b["b"], a["b"])
                    or near_right(a["b"], b["b"]) or near_right(b["b"], a["b"])):
                union(a["i"], b["i"])

    groups = {}
    for it in live:
        groups.setdefault(find(it["i"]), []).append(it)

    def bbox(g):
        x0 = min(i["b"][0] for i in g)
        y0 = min(i["b"][1] for i in g)
        x1 = max(i["b"][0] + i["b"][2] for i in g)
        y1 = max(i["b"][1] + i["b"][3] for i in g)
        return (x0, y0, x1 - x0, y1 - y0)

    kept, key, strays = [], {}, []
    for g in groups.values():
        g.sort(key=lambda k: k["i"])
        # A lone small-type box is usually a caption. But a photo page's BODY
        # paragraph is also 11.5 pt and also stands alone, and dropping it took the
        # whole substance off the TAX INCIDENCE page - and then stranded the receipts
        # photograph, whose owner had just been deleted. Size is what tells them
        # apart: a caption is a line, a body is a block.
        if (len(g) == 1 and g[0]["txt"] and (g[0]["pt"] or 99) <= 11.5
                and area(g[0]["b"]) <= 1.20):
            strays.append(g)                  # small-type label: usually noise...
            continue
        key[id(g)] = (min(i["b"][1] for i in g), min(i["b"][0] for i in g))
        kept.append(g)

    # ...unless several of them stand in a row at the same height and the same
    # width. That is a five-across strip, not noise, and Ch03/Ch04 give a strip
    # one click per column. Without this the whole strip collapses into the band
    # underneath it.
    for g in strays:
        gb = g[0]["b"]
        peers = [h for h in strays
                 if abs(h[0]["b"][1] - gb[1]) < 0.12 and abs(h[0]["b"][3] - gb[3]) < 0.30
                 and abs(h[0]["b"][2] - gb[2]) < 0.35]
        if len(peers) >= 3 and gb[2] <= 2.2:
            key[id(g)] = (gb[1], gb[0])
            kept.append(g)

    # Freeze every group's box BEFORE any picture joins it. Groups grow as units are
    # attached, and measuring against a grown box makes placement depend on the order
    # units happen to be visited -- which is how an icon sitting inside card 1 ended up
    # animating with card 2.
    frozen = {id(g): bbox(g) for g in kept}

    def edge_dist(a, b):
        dx = max(0, max(a[0] - (b[0] + b[2]), b[0] - (a[0] + a[2])))
        dy = max(0, max(a[1] - (b[1] + b[3]), b[1] - (a[1] + a[3])))
        return (dx * dx + dy * dy) ** 0.5

    extra, placed = [], set()

    # --- his pictures first, by MEANING ---------------------------------------
    # Attach before any geometric rule runs, so a photograph that happens to sit
    # nearer the kicker than its own card still lands on its own card.
    def _label(g):
        return next((i["txt"].split("\n")[0] for i in g if i["txt"]), "")

    for u in units:
        want = {OWNER.get((sno, it["id"])) for it in u if it["kind"] == "PICTURE"}
        want.discard(None)
        if len(want) != 1:
            continue
        target = want.pop()
        hit = next((g for g in kept if target.upper() in _label(g).upper()), None)
        if hit is not None:
            hit.extend(u)
            hit.sort(key=lambda k: k["i"])
            placed.add(id(u))

    # --- spot icons first, by nearest frozen box ------------------------------
    # A 0.3-0.6 in glyph is decoration on whatever it sits nearest. Deciding these
    # up front, on frozen geometry, keeps them out of the general rules below.
    for u in units:
        ub = bbox(u)
        if max(ub[2], ub[3]) > ICON_LONG or area(ub) > ICON_AREA:
            continue
        cands = [(g, frozen[id(g)]) for g in kept
                 if not (frozen[id(g)][2] > 9.0 and frozen[id(g)][3] > 3.5)]
        if not cands:
            continue
        d, g = min(((edge_dist(ub, gb), g) for g, gb in cands), key=lambda t: t[0])
        if d <= ICON_REACH:
            g.extend(u)
            g.sort(key=lambda k: k["i"])
            placed.add(id(u))

    for u in units:
        if id(u) in placed:
            continue
        ub = bbox(u)
        if area(ub) >= DOMINANT:
            continue                          # the slide's main figure -- frames it
        cands = [(g, frozen[id(g)]) for g in kept
                 if not (frozen[id(g)][2] > 9.0 and frozen[id(g)][3] > 3.5)]
        if not cands:
            continue

        best = max(cands, key=lambda c: inter(ub, c[1]))
        if inter(ub, best[1]) >= 0.75 * area(ub):
            best[0].extend(u)
            best[0].sort(key=lambda k: k["i"])
            continue

        row = []
        for g, gb in cands:
            vov = max(0, min(ub[1] + ub[3], gb[1] + gb[3]) - max(ub[1], gb[1]))
            gap = max(ub[0] - (gb[0] + gb[2]), gb[0] - (ub[0] + ub[2]))
            if vov >= 0.60 * ub[3] and gap >= 0:
                row.append((gap, g, gb))
        if row and min(r[0] for r in row) <= ADJACENT:
            # A lone neighbour only adopts a picture that is genuinely tucked against
            # it. A half-slide illustration one inch clear of the only card on the
            # slide is not that card's decoration -- it is the other column.
            if len(row) == 1 and min(r[0] for r in row) <= TUCKED \
                    and area(ub) <= SATELLITE_AREA:
                row[0][1].extend(u)
                row[0][1].sort(key=lambda k: k["i"])
            else:
                key[id(u)] = (ub[1], ub[0])
                extra.append(u)
            continue

        long_side, ar = max(ub[2], ub[3]), area(ub)
        if long_side <= SATELLITE_LONG and ar <= SATELLITE_AREA:
            cx, cy = ub[0] + ub[2] / 2, ub[1] + ub[3] / 2
            scored = [((((c[1][0] + c[1][2] / 2) - cx) ** 2
                        + ((c[1][1] + c[1][3] / 2) - cy) ** 2) ** 0.5, k)
                      for k, c in enumerate(cands)]
            d, k = min(scored)
            g = cands[k][0]
            if d <= REACH:
                g.extend(u)
                g.sort(key=lambda k: k["i"])
        else:
            key[id(u)] = (ub[1], ub[0])        # a picture with no owner is its own beat
            extra.append(u)

    kept.extend(extra)

    out = []
    for g in kept:
        y, x = key[id(g)]
        out.append(dict(y=y, x=x, ids=[i["id"] for i in g], shapes=g, mode="entr",
                        label=next((i["txt"].split("\n")[0] for i in g if i["txt"]),
                                   "(picture)")))
    # Bucket by row before sorting left-to-right. Rounding y to a tenth of an inch
    # put a card whose panel starts at 1.83 ahead of a picture beside it at 1.91,
    # so the sequence ran right-to-left across a row. A 0.35 in bucket is coarse
    # enough that anything on the same row sorts by x, as it reads.
    out.sort(key=lambda c: (round(c["y"] / 0.35), c["x"]))

    # A step that draws nothing but a hairline is a wasted click. The gold rule under
    # a section's intro line is an underline for the text above it, not a beat of its
    # own, so fold it back into the step before it. (The kicker's rule never lands
    # here: near_below already ties it to its sentence.)
    merged = []
    for st in out:
        rule_only = all(not sh["txt"] and sh["b"][3] <= 0.09 for sh in st["shapes"])
        if rule_only and merged:
            merged[-1]["ids"].extend(st["ids"])
        else:
            merged.append(st)
    # --- hide a picture at the moment the text it covers arrives ---------------
    # His instruction: "if pics are blocking texts behind it, hide the pictures in
    # the end as we show the text."  Derived rather than declared - a picture is
    # tested against every text box, and if it covers one that appears in a LATER
    # step, an exit for that picture is folded INTO that step, so a single click
    # both clears the picture and brings the sentence up.
    by_id = {it["id"]: it for it in items}
    first_step = {}
    for k, st in enumerate(merged):
        for sid in st["ids"]:
            first_step.setdefault(sid, k)

    for st in merged:
        st["modes"] = ["entr"] * len(st["ids"])

    for k, st in enumerate(merged):
        for sid in list(st["ids"]):
            pic = by_id.get(sid)
            if pic is None or pic["kind"] != "PICTURE" or area(pic["b"]) < 0.60:
                continue
            for t in items:
                if not t["txt"] or structural(t) or t["id"] == sid:
                    continue
                cov = inter(pic["b"], t["b"])
                if cov < 0.05:
                    continue
                j = first_step.get(t["id"])
                if j is None or j <= k:
                    continue
                if sid not in merged[j]["ids"]:
                    merged[j]["ids"].append(sid)
                    merged[j]["modes"].append("exit")

    for st in merged:
        st.pop("shapes", None)
    return merged


# ------------------------------------------------------------------- timing ---
def effect(cid, spid, first, mode):
    """One animation effect. mode: entr | exit | media.

    entr / exit are the Appear and Disappear presets -- a p:set on style.visibility.
    media is the play command PowerPoint writes for an inserted video; it rides in
    the same click step as the video's Appear so one click both shows and starts it.
    """
    node = "clickEffect" if first else "withEffect"
    if mode == "media":
        return (
            f'<p:par><p:cTn id="{cid}" presetID="1" presetClass="mediacall"'
            f' presetSubtype="0" fill="hold" nodeType="{node}">'
            f'<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'<p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr>'
            f'<p:cTn id="{cid + 1}" dur="1" fill="hold"/>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
            f'</p:cBhvr></p:cmd></p:childTnLst></p:cTn></p:par>')
    cls = "exit" if mode == "exit" else "entr"
    val = "hidden" if mode == "exit" else "visible"
    return (
        f'<p:par><p:cTn id="{cid}" presetID="1" presetClass="{cls}" presetSubtype="0"'
        f' fill="hold" nodeType="{node}"><p:stCondLst><p:cond delay="0"/>'
        f'</p:stCondLst><p:childTnLst><p:set><p:cBhvr>'
        f'<p:cTn id="{cid + 1}" dur="1" fill="hold"><p:stCondLst>'
        f'<p:cond delay="0"/></p:stCondLst></p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
        f'</p:cBhvr><p:to><p:strVal val="{val}"/></p:to></p:set>'
        f'</p:childTnLst></p:cTn></p:par>')


def timing_xml(steps, media_spid=None):
    """Build the whole p:timing tree. If media_spid is given, the p:video node and
    the click-to-pause interactiveSeq are re-emitted after the main sequence with
    fresh, non-colliding ids."""
    cid = 3
    body = []
    for st in steps:
        outer, innr = cid, cid + 1
        cid += 2
        fx = []
        modes = st.get("modes") or [st.get("mode", "entr")] * len(st["ids"])
        for k, spid in enumerate(st["ids"]):
            mode = modes[k] if k < len(modes) else st.get("mode", "entr")
            # a video step is Appear + play: the set first, then the command
            if mode == "media" and k == 0:
                fx.append(effect(cid, spid, True, "entr"))
                cid += 2
                fx.append(effect(cid, spid, False, "media"))
                cid += 2
                continue
            fx.append(effect(cid, spid, k == 0, mode))
            cid += 2
        body.append(
            f'<p:par><p:cTn id="{outer}" fill="hold"><p:stCondLst>'
            f'<p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
            f'<p:par><p:cTn id="{innr}" fill="hold"><p:stCondLst>'
            f'<p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            + "".join(fx) +
            '</p:childTnLst></p:cTn></p:par>'
            '</p:childTnLst></p:cTn></p:par>')

    tail = ""
    if media_spid is not None:
        v, s1, s2, s3, s4 = cid, cid + 1, cid + 2, cid + 3, cid + 4
        tail = (
            f'<p:video><p:cMediaNode vol="80000"><p:cTn id="{v}" fill="hold"'
            f' display="0"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>'
            f'</p:cTn><p:tgtEl><p:spTgt spid="{media_spid}"/></p:tgtEl>'
            f'</p:cMediaNode></p:video>'
            f'<p:seq concurrent="1" nextAc="seek"><p:cTn id="{s1}"'
            f' restart="whenNotActive" fill="hold" evtFilter="cancelBubble"'
            f' nodeType="interactiveSeq"><p:stCondLst><p:cond evt="onClick" delay="0">'
            f'<p:tgtEl><p:spTgt spid="{media_spid}"/></p:tgtEl></p:cond></p:stCondLst>'
            f'<p:endSync evt="end" delay="0"><p:rtn val="all"/></p:endSync>'
            f'<p:childTnLst><p:par><p:cTn id="{s2}" fill="hold"><p:stCondLst>'
            f'<p:cond delay="0"/></p:stCondLst><p:childTnLst><p:par>'
            f'<p:cTn id="{s3}" fill="hold"><p:stCondLst><p:cond delay="0"/>'
            f'</p:stCondLst><p:childTnLst><p:par><p:cTn id="{s4}" presetID="2"'
            f' presetClass="mediacall" presetSubtype="0" fill="hold"'
            f' nodeType="clickEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst>'
            f'<p:childTnLst><p:cmd type="call" cmd="togglePause"><p:cBhvr>'
            f'<p:cTn id="{s4 + 1}" dur="1" fill="hold"/><p:tgtEl>'
            f'<p:spTgt spid="{media_spid}"/></p:tgtEl></p:cBhvr></p:cmd>'
            f'</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>'
            f'</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn>'
            f'<p:nextCondLst><p:cond evt="onClick" delay="0"><p:tgtEl>'
            f'<p:spTgt spid="{media_spid}"/></p:tgtEl></p:cond></p:nextCondLst>'
            f'</p:seq>')

    return (
        '<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never"'
        ' nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek">'
        '<p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
        + "".join(body) +
        '</p:childTnLst></p:cTn>'
        '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/>'
        '</p:tgtEl></p:cond></p:prevCondLst>'
        '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/>'
        '</p:tgtEl></p:cond></p:nextCondLst></p:seq>'
        + tail +
        '</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')


# --------------------------------------------------------------------- main ---
def main():
    prs = Presentation(SRC)
    last = len(prs.slides._sldIdLst)
    partname, plan, media_on, skipped = {}, {}, {}, []

    for n, s in enumerate(prs.slides, 1):
        partname[n] = str(s.part.partname)
        if n == 1:
            skipped.append((n, "chapter title slide"))
            continue
        if n in CLIP_PAGES or n in SKIP:
            skipped.append((n, "embedded video — PowerPoint owns its p:timing (S5)"))
            continue
        blue = s._element.find(qn("p:cSld")).find(qn("p:bg")) is not None
        if blue and n != last:
            skipped.append((n, "section divider"))
            continue
        if n == ROADMAP:
            skipped.append((n, "roadmap (static in Ch03)"))
            continue
        if n == RECAP:
            skipped.append((n, "recap table"))
            continue
        st = steps_for(s, n)
        if len(st) < 2:
            skipped.append((n, "no sequence to carry"))
            continue
        plan[n] = st

    total = sum(len(v) for v in plan.values())
    for n in sorted(plan):
        print(f"slide {n:>2}  {len(plan[n])} clicks")
        for st in plan[n]:
            md = st.get("modes") or ["entr"] * len(st["ids"])
            shown = " ".join(("%s%s" % (i, "-EXIT" if m == "exit" else ""))
                             for i, m in zip(st["ids"], md))
            print(f"           [{shown}]  {st['label'][:50]}")
    print(f"\n{len(plan)} slides animated, {total} click steps")
    print("static:")
    for n, why in skipped:
        print(f"   {n:>2}  {why}")

    targets = {partname[n].lstrip("/"): (plan[n], media_on.get(n)) for n in plan}
    zin = zipfile.ZipFile(SRC)
    zout = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename in targets:
            steps, vid = targets[it.filename]
            x = data.decode("utf8")
            x = re.sub(r"<p:timing>.*?</p:timing>", "", x, flags=re.S)  # rebuild, not stack
            t = timing_xml(steps, vid)
            if "</p:clrMapOvr>" in x:
                x = x.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + t, 1)
            else:
                x = x.replace("</p:sld>", t + "</p:sld>", 1)
            data = x.encode("utf8")
        zout.writestr(it, data)
    zout.close()
    zin.close()
    print(f"\nwrote {DST}")


if __name__ == "__main__":
    main()
