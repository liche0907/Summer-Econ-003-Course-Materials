import pymupdf, re, statistics

SUPMAP={'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹',
        'n':'ⁿ','+':'⁺','-':'⁻','x':'ˣ'}
ZW='​‌‍﻿­'

def _chars(page):
    out=[]
    for b in page.get_text('rawdict')['blocks']:
        for l in b.get('lines',[]):
            d=l.get('dir',(1,0))
            if abs(d[1])>0.5: continue          # drop rotated axis labels
            for s in l['spans']:
                for c in s.get('chars',[]):
                    if c['c'] in ZW or not c['c'].strip(): continue
                    x0,y0,x1,y1=c['bbox']
                    out.append(dict(c=c['c'],x0=x0,x1=x1,y1=y1,sz=s['size']))
    return out

def _gutter(chars,width):
    """widest empty vertical band right of 40% width; None if no clean split"""
    if len(chars)<20: return None
    occ=[False]*(int(width)+2)
    for c in chars:
        for x in range(max(0,int(c['x0'])),min(len(occ)-1,int(c['x1'])+1)): occ[x]=True
    bands=[]; run=None
    for x in range(int(width*0.38),int(width*0.95)):
        if not occ[x]: run = x if run is None else run
        else:
            if run is not None and x-run>=22: bands.append((run,x))
            run=None
    if run is not None and int(width*0.95)-run>=22: bands.append((run,int(width*0.95)))
    # leftmost band that still leaves a real block of text to its right (not just the footer)
    for a,b in bands:
        g=(a+b)//2
        if sum(1 for c in chars if c['x0']>=g) >= 15: return g
    return None

def _lines(chars):
    if not chars: return []
    body=statistics.median([c['sz'] for c in chars])
    big=[c for c in chars if c['sz']>=body*0.92] or chars
    lines=[]
    for c in sorted(big,key=lambda c:(round(c['y1'],1),c['x0'])):
        for ln in lines:
            if abs(ln['y']-c['y1'])<=2.5: ln['cs'].append(c); break
        else: lines.append(dict(y=c['y1'],cs=[c]))
    for c in chars:
        if c['sz']>=body*0.92: continue
        cand=[ln for ln in lines if 0 < ln['y']-c['y1'] <= 6]
        if cand: min(cand,key=lambda l:l['y']-c['y1'])['cs'].append(dict(**c,sup=True))
    out=[]
    for ln in sorted(lines,key=lambda l:l['y']):
        cs=sorted(ln['cs'],key=lambda c:c['x0']); t=''; prev=None
        for c in cs:
            if prev is not None and c['x0']-prev > c['sz']*0.25: t+=' '
            t += SUPMAP.get(c['c'],c['c']) if c.get('sup') else c['c']
            prev=c['x1']
        t=re.sub(r' {2,}',' ',t).strip()
        if t: out.append((t, min(c['x0'] for c in cs)))
    return out

DROP=re.compile(r'^(\d+/\d+/\d+,\s*\d+:\d+\s*[AP]M|MT1|\d+/\d+|Instructor:|Student:|Course:|Date:|INTRODUCTION TO)')
def read_pdf(path):
    doc=pymupdf.open(path); pages=[]
    for p in doc:
        cs=[c for c in _chars(p)]
        g=_gutter(cs,p.rect.width)
        L=[c for c in cs if g is None or c['x0']<g]
        R=[c for c in cs if g is not None and c['x0']>=g]
        clean=lambda ls:[(t,x) for t,x in ls if not DROP.match(t) and 'tdx.acs.pearson' not in t]
        pages.append(dict(main=clean(_lines(L)), side=clean(_lines(R))))
    return pages
