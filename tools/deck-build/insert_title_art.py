#!/usr/bin/env python3
"""insert_title_art.py — put the chapter theme image into the title slide's triangle.

ALT is per-chapter: edit it before running. Ch07 was a trading floor, Ch08 a container port.

The Ch07 title card shipped with NO picture, by instruction, so the `rtTriangle` shape
has to be created rather than re-pointed. Its geometry is not guessable: it is lifted
verbatim from the Ch06 v5 title card, which is the template of record.

    flipH="1"   off 6128426, 2889115 EMU   ext 3015574, 2254385 EMU   prst="rtTriangle"

This is a surgical package edit (ground rules S8.4): the zip is rebuilt entry by entry,
so only `slide1.xml`, `slide1.xml.rels` and the new media part differ. Every other part
comes through byte-identical.

Run:  python3 insert_title_art.py <in.pptx> <art.png> <out.pptx> ["alt text"]
"""
import re
import shutil
import sys
import zipfile

IN, ART, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
# ALT is per-chapter.  It used to be a constant that had to be hand-edited before every
# run, which is exactly the kind of thing that silently ships the previous chapter's
# description.  Pass it as a fourth argument instead; the old default still applies.
_ALT_ARG = sys.argv[4] if len(sys.argv) > 4 else None

SLIDE = "ppt/slides/slide1.xml"
RELS = "ppt/slides/_rels/slide1.xml.rels"

ALT = _ALT_ARG or ("A container terminal: gantry cranes working a container ship at the "
                   "quay, with stacked shipping containers in the yard beyond")
assert "\"" not in ALT and "<" not in ALT, "alt text goes into an XML attribute"

with zipfile.ZipFile(IN) as z:
    names = z.namelist()
    slide = z.read(SLIDE).decode("utf-8")
    rels = z.read(RELS).decode("utf-8")
    ctypes = z.read("[Content_Types].xml").decode("utf-8")

assert "rtTriangle" not in slide, "slide1 already carries a triangle picture"

# --- a free media name, a free relationship id, a free shape id
media_idx = 1 + max([int(m.group(1)) for n in names
                     for m in [re.match(r"ppt/media/image(\d+)\.", n)] if m] or [0])
media_name = f"ppt/media/image{media_idx}.png"
_rid_n = 1 + max(int(m) for m in re.findall(r'Id="rId(\d+)"', rels))
rid = f"rId{_rid_n}"
sid = 1 + max(int(m) for m in re.findall(r'<p:cNvPr id="(\d+)"', slide))

PIC = (
    f'<p:pic><p:nvPicPr><p:cNvPr id="{sid}" name="Picture {sid - 1}" descr="{ALT}"/>'
    '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
    f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
    '<p:spPr><a:xfrm flipH="1"><a:off x="6128426" y="2889115"/>'
    '<a:ext cx="3015574" cy="2254385"/></a:xfrm>'
    '<a:prstGeom prst="rtTriangle"><a:avLst/></a:prstGeom></p:spPr></p:pic>'
)

# The wedge is the backdrop for the card, so it goes FIRST in the shape tree — behind
# the blue/gold group and the two text boxes. Appending it instead would bury the title.
i = slide.index("</p:grpSpPr>") + len("</p:grpSpPr>")
new_slide = slide[:i] + PIC + slide[i:]

new_rels = rels.replace(
    "</Relationships>",
    f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/'
    f'2006/relationships/image" Target="../media/image{media_idx}.png"/></Relationships>')

if 'Extension="png"' not in ctypes:
    ctypes = ctypes.replace(
        "<Types ", '<Types ', 1).replace(
        "</Types>", '<Default Extension="png" ContentType="image/png"/></Types>')

art = open(ART, "rb").read()

with zipfile.ZipFile(IN) as zin, zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SLIDE:
            data = new_slide.encode("utf-8")
        elif item.filename == RELS:
            data = new_rels.encode("utf-8")
        elif item.filename == "[Content_Types].xml":
            data = ctypes.encode("utf-8")
        zout.writestr(item, data)
    zout.writestr(media_name, art)

print(f"{OUT}")
print(f"  media   {media_name}  ({len(art):,} bytes)")
print(f"  rel     {rid}")
print(f"  shape   id {sid}, first in the tree so it sits behind the card")
