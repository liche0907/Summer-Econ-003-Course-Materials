#!/usr/bin/env python3
"""Rebuild Ch06 v3 by SPLICING into the instructor's own package.

Why this exists. v2 was produced by applying the edits with python-pptx and calling
prs.save(), which rewrites EVERY part in the package — masters, layouts, theme, the two
embedded .mp4 clips, docProps, [Content_Types].xml, every relationship file. That is
291 of 365 parts rewritten to change fourteen of them, and PowerPoint refused to open the
result even though the package validates clean by every check available here: no
duplicate shape ids, no dangling relationships, no missing content types, correct child
order in every p:sld, unique p:cTn ids, clean zip.

So this build stops trying to find the offending part and instead stops touching parts
it has no business touching. It starts from a byte copy of HIS file and substitutes only:

  * the slide XML of the two slides whose content changes, plus the new slide
  * the notes XML of those same slides
  * the image blobs of the nine figures being replaced
  * one .rels file, and only because its Id -> Target mapping genuinely differs
  * [Content_Types].xml, ppt/presentation.xml and its .rels — hand-patched, additively,
    to register one new slide

Everything else — both .mp4s, every photograph, the master, the layouts, the theme —
comes through untouched, byte for byte, exactly as PowerPoint wrote it.

    python3 splice_ch06_v3.py         # writes the static deck, then ch06_animate.py runs
"""
import json
import re
import zipfile

from lxml import etree

ORIG = "/mnt/user-data/uploads/ECON003_26S/Slides/ECON003_Ch06_Sellers_and_Incentives_UCR.pptx"
FULL = "_full.pptx"        # the python-pptx build, used only as a source of new XML
OUT = "_v3_static.pptx"

zo = zipfile.ZipFile(ORIG)
zf = zipfile.ZipFile(FULL)
orig_names = zo.namelist()
full_names = set(zf.namelist())

# ---- exactly what the edit script says it changed, and nothing else --------------
manifest = set(json.load(open("_manifest.json")))
take_from_full = [n for n in orig_names if n in manifest]
added = sorted(manifest - set(orig_names))
added += [n for n in full_names - set(orig_names) if n.startswith("ppt/media/")]

# A rewritten slide may need a relationship it did not have before - a re-added icon
# that resolved to a different image part, say. Take a .rels file ONLY when its
# Id -> Target mapping actually differs; python-pptx re-serialises every rels file it
# writes, and carrying those cosmetic rewrites through is exactly what this build
# exists to avoid.
def relmap(blob):
    x = etree.fromstring(blob)
    return {r.get("Id"): (r.get("Type"), r.get("Target"), r.get("TargetMode"))
            for r in x}


for part in sorted(manifest):
    if not part.endswith(".xml"):
        continue
    d, f = part.rsplit("/", 1)
    rels = f"{d}/_rels/{f}.rels"
    if rels not in full_names:
        continue
    if rels not in orig_names:
        added.append(rels)
    elif relmap(zo.read(rels)) != relmap(zf.read(rels)):
        take_from_full.append(rels)
        print("   rels genuinely changed:", rels)
added = sorted(set(added))

print("parts taken from the python-pptx build:")
for n in take_from_full:
    print("   ", n)
print("new parts:", added)

# ---- the new slide's number, and how it plugs in --------------------------------
new_slide = max(int(m.group(1)) for n in full_names
                for m in [re.match(r"ppt/slides/slide(\d+)\.xml$", n)] if m)
assert f"ppt/slides/slide{new_slide}.xml" in added, "expected exactly one new slide"

pres = zo.read("ppt/presentation.xml").decode("utf8")
rels = zo.read("ppt/_rels/presentation.xml.rels").decode("utf8")
ctypes = zo.read("[Content_Types].xml").decode("utf8")

rid = "rId%d" % (max(int(x) for x in re.findall(r'Id="rId(\d+)"', rels)) + 1)
sid = max(int(x) for x in re.findall(r'<p:sldId id="(\d+)"', pres)) + 1

# the new slide follows "Why Long-Run Supply Is Flat"; find that slide's rId, then its
# position in the id list, so the insert does not depend on any slide number
anchor_part = None
for n in orig_names:
    if re.match(r"ppt/slides/slide\d+\.xml$", n) and \
            b"Why Long-Run Supply Is Flat" in zo.read(n):
        anchor_part = n.split("/")[-1]
assert anchor_part, "anchor slide not found"
anchor_rid = re.search(r'Id="([^"]+)"[^>]*Target="slides/%s"' % anchor_part, rels).group(1)
m = re.search(r'<p:sldId id="\d+" r:id="%s"/>' % anchor_rid, pres)
assert m, "anchor sldId not found"
pres = pres[:m.end()] + f'<p:sldId id="{sid}" r:id="{rid}"/>' + pres[m.end():]

rels = rels.replace("</Relationships>",
                    f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org'
                    f'/officeDocument/2006/relationships/slide" '
                    f'Target="slides/slide{new_slide}.xml"/></Relationships>')

for part, ct in ((f"/ppt/slides/slide{new_slide}.xml",
                  "application/vnd.openxmlformats-officedocument."
                  "presentationml.slide+xml"),
                 (f"/ppt/notesSlides/notesSlide{new_slide}.xml",
                  "application/vnd.openxmlformats-officedocument."
                  "presentationml.notesSlide+xml")):
    assert f'PartName="{part}"' not in ctypes
    ctypes = ctypes.replace("</Types>",
                            f'<Override PartName="{part}" ContentType="{ct}"/></Types>')

PATCHED = {"ppt/presentation.xml": pres.encode("utf8"),
           "ppt/_rels/presentation.xml.rels": rels.encode("utf8"),
           "[Content_Types].xml": ctypes.encode("utf8")}

# ---- write, preserving his compression choices for every carried-over part -------
zout = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
for it in zo.infolist():
    if it.filename in PATCHED:
        data = PATCHED[it.filename]
    elif it.filename in set(take_from_full):
        data = zf.read(it.filename)
    else:
        data = zo.read(it.filename)
    info = zipfile.ZipInfo(it.filename, date_time=it.date_time)
    info.compress_type = it.compress_type          # his .mp4s stay stored, not re-deflated
    info.external_attr = it.external_attr
    zout.writestr(info, data)
for n in added:
    info = zipfile.ZipInfo(n, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = (zipfile.ZIP_STORED if n.endswith((".png", ".jpg", ".jpeg"))
                          else zipfile.ZIP_DEFLATED)
    zout.writestr(info, zf.read(n))
zout.close()

carried = len(orig_names) - len(take_from_full) - len(PATCHED)
print(f"\n{OUT}: {carried} parts carried through byte-identical, "
      f"{len(take_from_full)} replaced, {len(PATCHED)} patched, {len(added)} added")
