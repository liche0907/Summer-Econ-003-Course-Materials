#!/usr/bin/env python3
"""prune_media.py - drop media parts nothing references any more.

python-pptx never garbage-collects.  Deleting slide 15's hand-drawn shapes left three
image parts in the package with no relationship pointing at them - his two group
members and one duplicate - and the file grew 7.1 MB -> 9.3 MB while LOSING content.
Rebuild the zip entry by entry, keeping everything a .rels file still names.
"""
import re
import sys
import zipfile

SRC, DST = sys.argv[1], sys.argv[2]

z = zipfile.ZipFile(SRC)
used = set()
for it in z.infolist():
    if not it.filename.endswith(".rels"):
        continue
    base = it.filename.rsplit("/_rels/", 1)[0]
    for tgt in re.findall(r'Target="([^"]+)"', z.read(it.filename).decode("utf8")):
        if tgt.startswith("http"):
            continue
        p = (base + "/" + tgt).split("/")
        out = []
        for seg in p:
            if seg == "..":
                out.pop()
            elif seg != ".":
                out.append(seg)
        used.add("/".join(out))

media = [i.filename for i in z.infolist() if i.filename.startswith("ppt/media/")]
dead = [m for m in media if m not in used]

out = zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED)
kept = 0
for it in z.infolist():
    if it.filename in dead:
        continue
    out.writestr(it, z.read(it.filename))
    kept += 1
out.close()
z.close()
print("media parts: %d, orphaned: %d" % (len(media), len(dead)))
for d in dead:
    print("   dropped", d)
print("wrote %s (%d parts)" % (DST, kept))
