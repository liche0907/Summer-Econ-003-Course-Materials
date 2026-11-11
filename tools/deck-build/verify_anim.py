#!/usr/bin/env python3
"""The check that would have caught it: resolve every animation target INSIDE its own
part, with the part named by the package and the ids read from p:cNvPr - not a:cNvPr,
which matches nothing on a slide and makes the whole check silently vacuous."""
import sys, zipfile, collections
from lxml import etree
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
V = sys.argv[1]
z = zipfile.ZipFile(V)
rid = {r.get("Id"): r.get("Target")
       for r in etree.fromstring(z.read("ppt/_rels/presentation.xml.rels"))}
pres = etree.fromstring(z.read("ppt/presentation.xml"))
order = ["ppt/slides/" + rid[s.get(R + "id")].split("/")[-1]
         for s in pres.find(P + "sldIdLst")]
bad = 0; tim = 0; clicks = 0
for i, part in enumerate(order, 1):
    raw = z.read(part).decode("utf8")
    if raw.count("<p:timing>") > 1:
        print(f"  slide {i} ({part}): stacked timing"); bad += 1
    x = etree.fromstring(z.read(part))
    ids = collections.Counter(c.get("id")
                              for c in x.find(P + "cSld").find(P + "spTree").iter(P + "cNvPr"))
    assert ids, f"{part}: no p:cNvPr found - wrong namespace"
    for k, v in ids.items():
        if v > 1: print(f"  slide {i} ({part}): duplicate shape id {k}"); bad += 1
    t = x.find(P + "timing")
    if t is None:
        continue
    tim += 1
    for g in t.iter(P + "spTgt"):
        if g.get("spid") not in ids:
            print(f"  slide {i} ({part}): animates spid {g.get('spid')}, "
                  f"which is not on this slide"); bad += 1
    cids = [c.get("id") for c in t.iter(P + "cTn") if c.get("id")]
    if len(cids) != len(set(cids)):
        print(f"  slide {i} ({part}): duplicate cTn id"); bad += 1
    clicks += len([c for c in t.iter(P + "cTn") if c.get("nodeType") == "clickEffect"])
sch = etree.XMLSchema(etree.parse(
    "/mnt/skills/public/pptx/scripts/office/schemas/ISO-IEC29500-4_2016/pml.xsd"))
for part in order:
    if not sch.validate(etree.fromstring(z.read(part))):
        print(f"  {part}: fails pml.xsd - {sch.error_log[0].message[:120]}"); bad += 1
print(f"{V}: {len(order)} slides, {tim} animated, {clicks} clicks, {bad} problems")
sys.exit(1 if bad else 0)
