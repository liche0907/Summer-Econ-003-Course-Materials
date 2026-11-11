import pdfplumber,logging,json,collections,re
logging.getLogger('pdfminer').setLevel(logging.ERROR)
SRC='/mnt/user-data/uploads/ECON003_26S/Assignments/QB'
BOLD='Arial-BoldMT'; OPTL=re.compile(r'^([A-Z])\.$'); IDW=re.compile(r'^ID:$')
def blue(c):
    col=c.get('non_stroking_color') or ()
    return len(col)==3 and col[0]<0.15 and 0.3<col[1]<0.6 and col[2]>0.85
out={}
for b in ['QB7&8','QB9&10','QB12']:
    pages=[]
    with pdfplumber.open(f'{SRC}/{b}.pdf') as pdf:
        for pg in pdf.pages:
            dots=[dict(x=round(c['x0'],1),y=round((c['top']+c['bottom'])/2,1))
                  for c in pg.curves if c.get('fill') and blue(c) and 6<c['width']<11]
            ws=[dict(t=w['text'],x=round(w['x0'],1),y=round(w['top'],1),
                     b=1 if BOLD in w['fontname'] else 0)
                for w in pg.extract_words(extra_attrs=['fontname'])]
            pages.append(dict(dots=dots,words=ws))
    out[b]=pages
    print(b,'pages',len(pages),'blue dots',sum(len(p['dots']) for p in pages))
json.dump(out,open('/tmp/dots.json','w'))
