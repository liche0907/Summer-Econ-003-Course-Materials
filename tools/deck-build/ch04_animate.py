#!/usr/bin/env python3
"""Inject click-triggered Appear animations into the Ch04 deck.

Grouping and granularity follow what Ch03 actually does, read out of the file:
card rows one click each, the bottom kicker last, roadmap / recap table / dividers
/ photo slides static, and the takeaways page five clicks (one bullet per click).
A slide is animated only if it yields two or more steps -- a lone kicker is not a
sequence, and Ch03 leaves those alone.

python-pptx cannot author animations, so the p:timing tree is written as raw XML
straight into the slide part, and the package is rebuilt entry-by-entry so nothing
else in the file changes.
"""
import re, shutil, zipfile
from pptx import Presentation
from pptx.oxml.ns import qn

SRC = "work.pptx"
DST = "ECON003_Ch04_Demand_Supply_Equilibrium_UCR_v10.pptx"

STATIC_TYPES = {"PICTURE", "TABLE", "MEDIA", "GROUP", "CHART"}
ROADMAP = 3          # Today's Roadmap -- static in Ch03, so static here
RECAP = 51           # the full-picture table


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
    return i > 0 and i > 0.45 * min(area(a), area(b))


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
    # Card panels. Anything sitting inside one is that card's own label or body,
    # never a photo caption -- an ALL-CAPS card label under a chart is otherwise
    # indistinguishable from a caption by size and position alone.
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
            # the hairline frame drawn exactly over the picture
            if not o["txt"] and inter(o["b"], it["b"]) > 0.60 * area(o["b"]):
                grp.append(o)
                taken.add(o["i"])
                continue
            # the 10-11 pt caption directly under (or over) it -- one line, no more.
            # The height test is what keeps a card's body text out: a caption is
            # 0.19-0.30 in tall, a card body is 0.6 in and up.
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


def steps_for(slide):
    items = []
    for idx, sh in enumerate(slide.shapes):
        items.append(dict(i=idx, id=sh.shape_id, kind=str(sh.shape_type).split()[0],
                          b=box(sh), pt=maxpt(sh),
                          txt=sh.text_frame.text.strip() if sh.has_text_frame else "",
                          sh=sh))

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

    kept, key = [], {}
    for g in groups.values():
        g.sort(key=lambda k: k["i"])
        if len(g) == 1 and g[0]["txt"] and (g[0]["pt"] or 99) <= 11.5:
            continue                          # stray small-type label
        # Freeze the reading order now, on the text alone. An icon that joins a
        # card later must not drag the card's place in the sequence with it.
        key[id(g)] = (min(i["b"][1] for i in g), min(i["b"][0] for i in g))
        kept.append(g)

    # --- place the pictures ---------------------------------------------------
    # A picture that illustrates something which animates has to animate with it.
    # Three ways it can belong, tried in order; anything that matches none of them
    # is the slide's setting and stays put.
    extra = []
    for u in units:
        ub = bbox(u)
        if area(ub) >= DOMINANT:
            continue                          # the slide's main figure -- frames it
        cands = [(g, bbox(g)) for g in kept if not (bbox(g)[2] > 9.0 and bbox(g)[3] > 3.5)]
        if not cands:
            continue

        # (a) sitting INSIDE a card -- an icon, an inset photo, a table in a panel
        best = max(cands, key=lambda c: inter(ub, c[1]))
        if inter(ub, best[1]) >= 0.75 * area(ub):
            best[0].extend(u)
            best[0].sort(key=lambda k: k["i"])
            continue

        # (b) standing in the same row as a card, just outside it
        row = []
        for g, gb in cands:
            vov = max(0, min(ub[1] + ub[3], gb[1] + gb[3]) - max(ub[1], gb[1]))
            gap = max(ub[0] - (gb[0] + gb[2]), gb[0] - (ub[0] + ub[2]))
            if vov >= 0.60 * ub[3] and gap >= 0:
                row.append((gap, g, gb))
        if row and min(r[0] for r in row) <= ADJACENT:
            if len(row) == 1:
                row[0][1].extend(u)           # one neighbour: it belongs to that card
                row[0][1].sort(key=lambda k: k["i"])
            else:
                key[id(u)] = (ub[1], ub[0])   # a row of cards: it is the next column
                extra.append(u)
            continue

        # (c) a spot icon orbiting a card
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

    kept.extend(extra)

    out = []
    for g in kept:
        y, x = key[id(g)]
        out.append(dict(y=y, x=x, ids=[i["id"] for i in g],
                        label=next((i["txt"].split("\n")[0] for i in g if i["txt"]),
                                   "(picture)")))
    out.sort(key=lambda c: (round(c["y"], 1), c["x"]))
    return out


# ------------------------------------------------------------------- timing ---
def effect(cid, spid, first):
    node = "clickEffect" if first else "withEffect"
    return (
        f'<p:par><p:cTn id="{cid}" presetID="1" presetClass="entr" presetSubtype="0"'
        f' fill="hold" nodeType="{node}"><p:stCondLst><p:cond delay="0"/>'
        f'</p:stCondLst><p:childTnLst><p:set><p:cBhvr>'
        f'<p:cTn id="{cid + 1}" dur="1" fill="hold"><p:stCondLst>'
        f'<p:cond delay="0"/></p:stCondLst></p:cTn>'
        f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
        f'<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
        f'</p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
        f'</p:childTnLst></p:cTn></p:par>')


def timing_xml(steps):
    cid = 3
    body = []
    for st in steps:
        outer, innr = cid, cid + 1
        cid += 2
        fx = []
        for k, spid in enumerate(st["ids"]):
            fx.append(effect(cid, spid, k == 0))
            cid += 2
        body.append(
            f'<p:par><p:cTn id="{outer}" fill="hold"><p:stCondLst>'
            f'<p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
            f'<p:par><p:cTn id="{innr}" fill="hold"><p:stCondLst>'
            f'<p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            + "".join(fx) +
            '</p:childTnLst></p:cTn></p:par>'
            '</p:childTnLst></p:cTn></p:par>')
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
        '</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')


# --------------------------------------------------------------------- main ---
def main():
    prs = Presentation(SRC)
    last = len(prs.slides._sldIdLst)
    partname = {}
    plan, skipped = {}, []
    for n, s in enumerate(prs.slides, 1):
        partname[n] = str(s.part.partname)
        if n == 1:
            skipped.append((n, "chapter title slide"))
            continue
        if s._element.find(qn("p:timing")) is not None:
            skipped.append((n, "embedded media keeps its own timing"))
            continue
        blue = s._element.find(qn("p:cSld")).find(qn("p:bg")) is not None
        st = steps_for(s)
        if blue and n != last:
            skipped.append((n, "section divider"))
            continue
        if n == ROADMAP:
            skipped.append((n, "roadmap (static in Ch03)"))
            continue
        if n == RECAP:
            skipped.append((n, "recap table"))
            continue
        if len(st) < 2:
            skipped.append((n, "no sequence to carry"))
            continue
        plan[n] = st

    total = sum(len(v) for v in plan.values())
    for n in sorted(plan):
        print(f"slide {n:>2}  {len(plan[n])} clicks")
        for st in plan[n]:
            print(f"           {st['ids']}  {st['label'][:52]}")
    print(f"\n{len(plan)} slides animated, {total} click steps")
    print("static:")
    for n, why in skipped:
        print(f"   {n:>2}  {why}")

    targets = {partname[n].lstrip("/"): plan[n] for n in plan}
    zin = zipfile.ZipFile(SRC)
    zout = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename in targets:
            x = data.decode("utf8")
            t = timing_xml(targets[it.filename])
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
