"""Pull the dropdown choice sets out of a Pearson print page: (1) a / b / c."""
import pymupdf, re, statistics
from reader import _chars, _gutter
SUP={'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'}

def _segments(page):
    cs=_chars(page); g=_gutter(cs,page.rect.width)
    L=[c for c in cs if g is None or c['x0']<g]
    if not L: return []
    body=statistics.median([c['sz'] for c in L])
    rows={}
    for c in L:
        if c['sz']<body*0.92: continue
        rows.setdefault(round(c['y1']),[]).append(c)
    out=[]
    for y in sorted(rows):
        cs2=sorted(rows[y],key=lambda c:c['x0']); segs=[]; txt=''; sx=None; prev=None
        for c in cs2:
            if prev is not None and c['x0']-prev>6:
                segs.append((sx,txt)); txt=''; sx=c['x0']
            elif sx is None: sx=c['x0']
            elif prev is not None and c['x0']-prev > c['sz']*0.25: txt+=' '
            txt+=c['c']; prev=c['x1']
        if txt: segs.append((sx,txt))
        out.append((y,segs))
    return out

def choice_sets(pdf_path, pages):
    """-> {blank_number: [choice, ...]} for the given 1-based page numbers"""
    doc=pymupdf.open(pdf_path); res={}
    for pno in pages:
        if pno-1>=len(doc): continue
        rows=_segments(doc[pno-1])
        for idx,(y,segs) in enumerate(rows):
            marks=[(sx,m.group(1)) for sx,s in segs for m in [re.match(r'^\((\d+)\)',s)] if m]
            if not marks: continue
            # column x for each marker = the segment that follows it on this row
            cols={}
            for sx,num in marks:
                after=[(x,t) for x,t in segs if x>sx+4]
                same=[(x,t) for x,t in after if all(x<ox or ox<=sx for ox,_ in marks if ox>sx)]
                cand=[(x,t) for x,t in segs if x>sx+4 and not re.match(r'^\(\d+\)',t)]
                cand=[c for c in cand if not any(sx<mx<=c[0] for mx,_ in marks)]
                if cand: cols[num]=[cand[0][0],[cand[0][1]]]
            if not cols: continue
            for y2,segs2 in rows[idx+1:idx+7]:
                if any(re.match(r'^\s*Answers?:',t) for _,t in segs2): break
                if any(re.match(r'^\(\d+\)',t) for _,t in segs2): break
                hit=False
                for num,(cx,lst) in cols.items():
                    for x,t in segs2:
                        if abs(x-cx)<7 and t.strip():
                            lst.append(t); hit=True
                if not hit: break
            for num,(cx,lst) in cols.items():
                clean=[re.sub(r'\s{2,}',' ',t).strip() for t in lst]
                clean=[re.sub(r'\s{2,}',' ',c) for c in clean if c]
                if len(clean)>=2: res.setdefault(int(num),clean)
    return res
