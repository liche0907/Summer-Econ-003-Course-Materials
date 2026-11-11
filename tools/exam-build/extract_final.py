import subprocess, re, pickle, collections, json, os
SRC='/mnt/user-data/uploads/ECON003_26S/Assignments'
QB={'QB7&8':'QB/QB7&8.pdf','QB9&10':'QB/QB9&10.pdf','QB12':'QB/QB12.pdf'}

def pages_text(pdf):
    t=subprocess.run(['pdftotext','-layout',f'{SRC}/{pdf}','-'],capture_output=True,text=True).stdout
    return t.split('\f')

def img_pages(pdf):
    out=subprocess.run(['pdfimages','-list',f'{SRC}/{pdf}'],capture_output=True,text=True).stdout
    s=set()
    for ln in out.splitlines()[2:]:
        p=ln.split()
        if len(p)>2 and p[0].isdigit():
            # ignore tiny decorative images
            try:
                w,h=int(p[3]),int(p[4])
            except: continue
            if w>80 and h>80: s.add(int(p[0]))
    return s

HDR=re.compile(r'^\s*\d+/\d+/\d+,\s*\d+:\d+\s*[AP]M.*$',re.M)
FTR=re.compile(r'https://tdx\.acs\.pearson\.com\S*\s*\d+/\d+')
def clean(t): return FTR.sub('',HDR.sub('',t))

def parse_bank(key):
    pdf=QB[key]; pgs=pages_text(pdf); imgs=img_pages(pdf)
    items=[]; buf=''; startpg=1
    for pno,raw in enumerate(pgs,1):
        c=clean(raw)
        while True:
            m=re.search(r'^\s*ID:\s*(.+?)\s*$', c, re.M)
            if not m: break
            buf+=c[:m.start()]
            items.append({'bank':key,'pid':m.group(1).strip(),'raw':buf,
                          'pages':list(range(startpg,pno+1))})
            buf=''; startpg=pno
            c=c[m.end():]
        buf+=c
    for it in items:
        it['figure']= any(p in imgs for p in it['pages'])
    return items

def split_item(raw):
    b=re.sub(r'^\s*\d+\.\s*','',raw.strip())
    m=list(re.finditer(r'^\s*.?(Answers?):\s*', b, re.M))
    if m:
        qpart=b[:m[-1].start()]; apart=b[m[-1].start():]
        plural=m[-1].group(1)=='Answers'
    else:
        qpart=b; apart=''; plural=False
    om=re.search(r'^\s{4,}A\.\s', qpart, re.M)
    stem=qpart[:om.start()] if om else qpart
    opts=qpart[om.start():] if om else ''
    def sq(x): return re.sub(r'[ \t]+',' ',re.sub(r'\n{2,}','\n',x)).strip()
    ans=re.sub(r'^\s*.?Answers?:\s*','',apart).strip()
    nums=sorted(set(re.findall(r'\((\d+)\)', ans)))
    letters=re.findall(r'(?:^|\s)([A-Z])\.\s', ans)
    nparts=(len(nums)+(1 if letters else 0)) if plural else 1
    fmt='cloze+mc' if nums and letters else 'cloze' if nums else 'mc'
    nopt=len(set(re.findall(r'^\\s{4,}([A-Z])\\.\\s', opts, re.M)))
    cata = bool(re.search(r'[Cc]heck all that apply', qpart)) or (nparts==1 and len(set(letters))>1)
    return sq(stem), sq(opts), sq(ans), max(nparts,1), fmt, nopt, cata

all_items=[]
for k in QB:
    its=parse_bank(k)
    for it in its:
        it['stem'],it['opts'],it['ans'],it['parts'],it['fmt'],it['nopt'],it['cata']=split_item(it['raw'])
    print(k, len(its), 'items,', sum(i['figure'] for i in its), 'with figures')
    all_items+=its
pickle.dump(all_items, open('/tmp/items_final.pkl','wb'))
print('total', len(all_items))
print()
x=all_items[1]
print('SAMPLE ---'); print('pid:',x['pid'],'| parts',x['parts'],'| fmt',x['fmt'],'| nopt',x['nopt'],'| fig',x['figure'])
print('STEM:',x['stem'][:300]); print('OPTS:',x['opts'][:300]); print('ANS:',x['ans'][:200])
