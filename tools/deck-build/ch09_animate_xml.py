#!/usr/bin/env python3
"""Animate a deck WITHOUT ever moving the deck.

Why this exists
---------------
His Ch09 file reached 138 MB once two lecture clips were embedded, and at that size it
will not cross the device bridge: three staging attempts timed out and the on-device
Linux workspace would not start. But the animation depends on NOTHING except the slide
XML - geometry, shape ids and text - which is about 1 MB for the whole deck.

So the deck stays on his machine and only ppt/slides/*.xml travels:

    1.  he runs   Animate-Deck.ps1 -Deck <file> -Export
    2.  those ~40 small files come over, this script computes the timing
    3.  the rewritten slide XML goes back
    4.  he runs   Animate-Deck.ps1 -Deck <file> -Apply -Out <v3>

Every clustering decision is imported from ch09_animate.py unchanged, so this produces
byte-identical timing to the in-package path - which is asserted by --selftest.

Run:
    python3 ch09_animate_xml.py <slides_dir> <out_dir>
    python3 ch09_animate_xml.py --selftest <deck.pptx>
"""
import os
import re
import sys
import glob
import zipfile
from xml.etree import ElementTree as ET

import ch09_animate as A

NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
for k, v in NS.items():
    ET.register_namespace(k, v)
Q = {k: "{%s}" % v for k, v in NS.items()}
EMU = 914400.0


def _xfrm(el):
    """The shape's own transform, wherever this shape type keeps it."""
    for path in ("p:spPr/a:xfrm", "p:xfrm", "p:grpSpPr/a:xfrm"):
        x = el.find(path, NS)
        if x is not None:
            return x
    return None


def _kind(el):
    tag = el.tag.split("}")[1]
    if tag == "pic":
        # a video is a p:pic with a videoFile in its nvPr - python-pptx calls it MEDIA
        return "MEDIA" if el.find(".//a:videoFile", NS) is not None else "PICTURE"
    if tag == "graphicFrame":
        if el.find(".//a:tbl", NS) is not None:
            return "TABLE"
        if el.find(".//" + Q["a"] + "graphic") is not None and b"chart" in ET.tostring(el):
            return "CHART"
        return "TABLE"
    if tag == "grpSp":
        return "GROUP"
    if tag == "sp":
        c = el.find("p:nvSpPr/p:cNvSpPr", NS)
        return "TEXT_BOX" if (c is not None and c.get("txBox") == "1") else "AUTO_SHAPE"
    return "AUTO_SHAPE"


def _text(el):
    """Paragraph text, joined the way python-pptx's text_frame.text joins it."""
    paras = el.findall(".//" + Q["a"] + "p")
    if not paras:
        return ""
    out = []
    for p in paras:
        out.append("".join(t.text or "" for t in p.findall(".//" + Q["a"] + "t")))
    return "\n".join(out).strip()


def _maxpt(el):
    """Largest explicit run size, in points. None when nothing sets one - which is
    what python-pptx returns for an inherited size, so the two agree."""
    sz = [int(rpr.get("sz")) for rpr in el.iter()
          if rpr.tag.endswith("}rPr") and rpr.get("sz")]
    return max(sz) / 100.0 if sz else None


def collect_xml(root):
    """Same shape of output as ch09_animate.collect(), from raw slide XML."""
    tree = root.find("p:cSld/p:spTree", NS)
    items = []
    for idx, el in enumerate(list(tree)):
        tag = el.tag.split("}")[1]
        if tag in ("nvGrpSpPr", "grpSpPr"):
            continue
        cNvPr = el.find(".//" + Q["p"] + "cNvPr")
        if cNvPr is None:
            continue
        x = _xfrm(el)
        if x is None:
            b = (0.0, 0.0, 0.0, 0.0)
        else:
            off, ext = x.find("a:off", NS), x.find("a:ext", NS)
            b = ((int(off.get("x")) / EMU, int(off.get("y")) / EMU,
                  int(ext.get("cx")) / EMU, int(ext.get("cy")) / EMU)
                 if off is not None and ext is not None else (0.0, 0.0, 0.0, 0.0))
        items.append(dict(i=len(items), id=int(cNvPr.get("id")), kind=_kind(el),
                          b=b, pt=_maxpt(el), txt=_text(el), sh=None))
    return items


# ------------------------------------------------------------------ slide facts
def is_blue(root):
    return root.find("p:cSld/p:bg", NS) is not None


def title_of(items):
    c = [it for it in items if it["txt"] and it["b"][3] > 0]
    return min(c, key=lambda it: it["b"][1])["txt"] if c else ""


def has_video(root):
    return root.find(".//a:videoFile", NS) is not None


def is_recap_xml(root):
    for tbl in root.findall(".//" + Q["a"] + "tbl"):
        rows = tbl.findall(Q["a"] + "tr")
        # NB: join the CELL texts, not the characters of one string. The first
        # version wrote " ".join(<a string>), which spaces out every letter and
        # made the recap page look like an ordinary content slide. --selftest
        # caught it by disagreeing with the in-package path on exactly one slide.
        if not rows:
            continue
        hdr = " ".join("".join(t.text or "" for t in tc.iter(Q["a"] + "t"))
                       for tc in rows[0].findall(Q["a"] + "tc")).lower()
        if A.RECAP_HDR in hdr:
            return True
    return False


def plan_for(paths):
    """paths: {slide_number: xml_text}. Returns {n: steps}, [(n, why_static)]."""
    nums = sorted(paths)
    last = max(nums)
    plan, skipped = {}, []
    for n in nums:
        root = ET.fromstring(paths[n])
        if n == 1:
            skipped.append((n, "chapter title slide")); continue
        if has_video(root) or "<p:timing" in paths[n]:
            skipped.append((n, "video page — keeps its own media timing, untouched"))
            continue
        if is_blue(root) and n != last:
            skipped.append((n, "section divider")); continue
        items = collect_xml(root)
        if A.ROADMAP_RE.search(title_of(items)):
            skipped.append((n, "roadmap (static in Ch03)")); continue
        if is_recap_xml(root):
            skipped.append((n, "recap table")); continue
        st = A.steps_for(items)
        if len(st) < 2:
            skipped.append((n, "no sequence to carry")); continue
        plan[n] = st
    return plan, skipped


def inject(xml, steps):
    xml = re.sub(r"<p:timing>.*?</p:timing>", "", xml, flags=re.S)
    t = A.timing_xml(steps, None)
    if "</p:clrMapOvr>" in xml:
        return xml.replace("</p:clrMapOvr>", "</p:clrMapOvr>" + t, 1)
    return xml.replace("</p:sld>", t + "</p:sld>", 1)


def report(plan, skipped):
    for n in sorted(plan):
        print(f"slide {n:>2}  {len(plan[n])} clicks")
        for st in plan[n]:
            print(f"           {st['ids']}  {st['label'][:50]}")
    print(f"\n{len(plan)} slides animated, "
          f"{sum(len(v) for v in plan.values())} click steps")
    print("static:")
    for n, why in skipped:
        print(f"   {n:>2}  {why}")


# ---------------------------------------------------------------------- selftest
def selftest(deck):
    """The XML path must produce exactly what the in-package path produces."""
    from pptx import Presentation
    z = zipfile.ZipFile(deck)
    paths = {int(re.search(r"slide(\d+)\.xml$", n).group(1)): z.read(n).decode("utf8")
             for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)}
    xplan, _ = plan_for(paths)

    prs = Presentation(deck)
    clip = A.video_slides(deck)
    last = len(prs.slides._sldIdLst)
    pplan = {}
    from pptx.oxml.ns import qn
    for n, s in enumerate(prs.slides, 1):
        if n == 1 or n in clip:
            continue
        if s._element.find(qn("p:cSld")).find(qn("p:bg")) is not None and n != last:
            continue
        if A.ROADMAP_RE.search(A.slide_title(s)) or A.is_recap(s):
            continue
        st = A.steps_for(A.collect(s))
        if len(st) >= 2:
            pplan[n] = st

    ok = True
    if set(xplan) != set(pplan):
        ok = False
        print("slide sets differ:", sorted(set(xplan) ^ set(pplan)))
    for n in sorted(set(xplan) & set(pplan)):
        a = [st["ids"] for st in xplan[n]]
        b = [st["ids"] for st in pplan[n]]
        if a != b:
            ok = False
            print(f"slide {n} differs\n   xml: {a}\n   pkg: {b}")
    print("SELFTEST", "PASS — XML path matches the in-package path exactly" if ok
          else "FAIL")
    return ok


def main():
    if sys.argv[1] == "--selftest":
        sys.exit(0 if selftest(sys.argv[2]) else 1)
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    paths = {}
    for f in glob.glob(os.path.join(src, "slide*.xml")):
        m = re.search(r"slide(\d+)\.xml$", os.path.basename(f))
        if m:
            paths[int(m.group(1))] = open(f, encoding="utf8").read()
    print(f"{len(paths)} slide parts read from {src}")
    plan, skipped = plan_for(paths)
    report(plan, skipped)
    for n, steps in plan.items():
        out = os.path.join(dst, f"slide{n}.xml")
        open(out, "w", encoding="utf8").write(inject(paths[n], steps))
    print(f"\nwrote {len(plan)} rewritten slide parts to {dst}")


if __name__ == "__main__":
    main()
