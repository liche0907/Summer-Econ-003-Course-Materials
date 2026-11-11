import subprocess, re, pickle, collections, difflib, openpyxl
SRC='/mnt/user-data/uploads/ECON003_26S/Assignments'
BANKS=[('QB1&3','QB/QB1&3.pdf','QB/QB1&3.xlsx'),('QB4&5','QB/QB4&5.pdf','QB/QB4&5.xlsx'),('QB6','QB/QB6.pdf','QB/QB6.xlsx')]
HDR=re.compile(r'^\s*\d+/\d+/\d+,\s*\d+:\d+\s*[AP]M.*$',re.M)
FTR=re.compile(r'https://tdx\.acs\.pearson\.com\S*\s*\d+/\d+')
PRE=re.compile(r'^\s*(Instructor:|Student:|Course:|Date:|INTRODUCTION TO MICROECONOMICS).*$',re.M)
ZWC=re.compile(r'[\u200b\u200c\u200d\ufeff\u00ad]')
clean=lambda t: PRE.sub('',FTR.sub('',HDR.sub('',ZWC.sub(' ',t))))
CUE=re.compile(r'\b(graph|figure|exhibit|diagram|the table|following table|curve shown|shown in the|accompanying|drawing tool|shown above|in the graph)\b',re.I)
sq=lambda x: re.sub(r'[ \t]+',' ',re.sub(r'\n{2,}','\n',x)).strip()

def img_pages(p):
    out=subprocess.run(['pdfimages','-list',f'{SRC}/{p}'],capture_output=True,text=True).stdout
    s=set()
    for ln in out.splitlines()[2:]:
        f=ln.split()
        if len(f)>4 and f[0].isdigit():
            try:
                if int(f[3])>80 and int(f[4])>80: s.add(int(f[0]))
            except ValueError: pass
    return s

def split_item(raw):
    b=re.sub(r'^\s*\d+\.\s*','',raw.strip())
    m=list(re.finditer(r'^\s*.?(Answers?):\s*',b,re.M))
    qpart,apart,plural=(b[:m[-1].start()],b[m[-1].start():],m[-1].group(1)=='Answers') if m else (b,'',False)
    om=re.search(r'^\s{4,}A\.\s',qpart,re.M)
    stem,opts=(qpart[:om.start()],qpart[om.start():]) if om else (qpart,'')
    ans=re.sub(r'^\s*.?Answers?:\s*','',apart).strip()
    nums=sorted(set(re.findall(r'\((\d+)\)',ans)))
    alines=[l for l in ans.split(chr(10)) if re.match(r'\s*[A-Z]\.\s',l)]
    letters=re.findall(r'(?:^|\s)([A-Z])\.\s',ans)
    nparts=(len(nums)+len(alines)) if plural else 1
    fmt='cloze+mc' if nums and letters else 'cloze' if nums else 'mc'
    nopt=len(set(re.findall(r'^\s{4,}([A-Z])\.\s',opts,re.M)))
    cata=bool(re.search(r'[Cc]heck all that apply',qpart)) or (len(alines)==1 and len(set(letters))>1 and not nums)
    return dict(stem=sq(stem),opts=sq(opts),ans=sq(ans),parts=max(nparts,1),fmt=fmt,nopt=nopt,cata=cata)

def parse(key,pdf):
    pgs=subprocess.run(['pdftotext','-layout',f'{SRC}/{pdf}','-'],capture_output=True,text=True).stdout.split('\f')
    imgs=img_pages(pdf); items=[]; buf=''; start=1
    for pno,raw in enumerate(pgs,1):
        c=clean(raw)
        while (m:=re.search(r'^\s*ID:\s*(.+?)\s*$',c,re.M)):
            buf+=c[:m.start()]
            items.append(dict(bank=key,pid=m.group(1).strip(),raw=buf,pages=list(range(start,pno+1))))
            buf=''; start=pno; c=c[m.end():]
        buf+=c
    for it in items:
        it.update(split_item(it['raw']))
        img=any(p in imgs for p in it['pages']); cue=bool(CUE.search(it['stem']+' '+it['opts']))
        it['figure']='Yes' if (img and cue) else 'Likely' if (img or cue) else 'No'
    return items

items=[]
for key,pdf,xls in BANKS:
    its=parse(key,pdf)
    ws=openpyxl.load_workbook(f'{SRC}/{xls}',data_only=True)['Sheet1']
    rows=[r for r in ws.iter_rows(min_row=2,values_only=True) if r[1]]
    assert len(rows)==len(its),(key,len(rows),len(its))
    nm=lambda s: re.sub(r'\s*\((algo|static)\)\s*$','',str(s).strip(),flags=re.I).lower()
    for it,r in zip(its,rows):
        assert nm(r[1])==nm(it['pid']),(r[1],it['pid'])
        v=re.search(r'\((algo|static)\)',str(r[1]),re.I)
        t=str(r[5]); secs=sum(int(x)*f for x,f in zip(re.findall(r'(\d+)[ms]',t)[::-1],[1,60]))
        it.update(order=r[0],section=r[2],difficulty=r[7],time_raw=t,time_s=secs,
                  variant=v.group(1).lower() if v else '',
                  qtype=re.sub(r'\s*\d.*$','',it['pid']).strip().title())
    items+=its

CH={'The Scope of Economics':(1,'1.1'),'Three Principles of Economics':(1,'1.2'),
 'The First Principle of Economics: Optimization':(1,'1.3'),'The Second Principle of Economics: Equilibrium':(1,'1.4'),
 'The Third Principle of Economics: Empiricism':(1,'1.5'),'Is Economics Good for You?':(1,'1.6'),
 'Optimization: Trying to Choose the Best Feasible Option':(3,'3.1'),'Optimization Application: Renting the Optimal Apartment':(3,'3.2'),
 'Optimization Using Marginal Analysis':(3,'3.3'),'Markets':(4,'4.1'),'How Do Buyers Behave?':(4,'4.2'),
 'How Do Sellers Behave?':(4,'4.3'),'Supply and Demand in Equilibrium':(4,'4.4'),
 'What Would Happen if the Government Tried to Dictate the Price of Gasoline?':(4,'4.5'),
 "The Buyer's Problem":(5,'5.1'),'Putting It All Together':(5,'5.2'),"From the Buyer's Problem to the Demand Curve":(5,'5.3'),
 'Consumer Surplus':(5,'5.4'),'Demand Elasticities':(5,'5.5'),'Appendix: Representing Preferences with Indifference Curves':(5,'5.A'),
 'Sellers in a Perfectly Competitive Market':(6,'6.1'),"The Seller's Problem":(6,'6.2'),
 "From the Seller's Problem to the Supply Curve":(6,'6.3'),'Producer Surplus':(6,'6.4'),
 'From the Short Run to the Long Run':(6,'6.5'),'From the Firm to the Market: Long-Run Competitive Equilibrium':(6,'6.6'),
 'When Firms Have Different Cost Structures':(6,'6.A')}
for it in items: it['ch'],it['sec']=CH[it['section']]

# ---- usage flags -------------------------------------------------------
def blocks(p):
    t=clean(subprocess.run(['pdftotext','-layout',f'{SRC}/{p}','-'],capture_output=True,text=True).stdout)
    s=re.split(r'^\s*ID:\s*(.+?)\s*$',t,flags=re.M)
    return [(s[i].strip(),s[i-1]) for i in range(1,len(s),2)]
sig=lambda b: re.sub(r'\s+',' ',re.sub(r'[\d.,$%]+',' ',b)).strip()[:600]
for it in items: it['used_in']=[]; it['amb']=False
PAIRS=[('HW1','HW/HW1.pdf','QB1&3',None),('Q1','HW/Q1.pdf','QB1&3',None),('HW2','HW/HW2.pdf','QB4&5',None),
       ('Q2','HW/Q2.pdf','QB4&5',None),('HW3A','HW/HW3A.pdf','QB6',None),('Q3','HW/Q3.pdf','QB6',10)]
missing=[]
for label,pdf,bank,lim in PAIRS:
    bs=blocks(pdf)[:lim] if lim else blocks(pdf)
    for qid,body in bs:
        c=[i for i in items if i['bank']==bank and re.sub(r'\s*\((algo|static)\)\s*$','',i['pid'],flags=re.I).lower()==qid.lower()]
        if not c: missing.append((label,qid)); continue
        if len(c)==1: pick=c[0]
        else:
            sc=sorted(((difflib.SequenceMatcher(None,sig(body),sig(x['raw'])).ratio(),n) for n,x in enumerate(c)),reverse=True)
            pick=c[sc[0][1]]; pick['amb']= (sc[0][0]-sc[1][0])<0.05
        pick['used_in'].append(label)

# ---- unique IDs --------------------------------------------------------
ABBR={'Review Question':'RQ','Concept Question':'CQ','Concept Check':'CC','Text Problem':'TP'}
items.sort(key=lambda i:(i['ch'],i['sec'],i['order']))
seq=collections.Counter()
for it in items:
    a=ABBR.get(it['qtype'],'XX'); k=(it['ch'],a); seq[k]+=1
    it['uid']=f"E3-C{it['ch']:02d}-{a}{seq[k]:02d}"
    it['pid_unique']=f"Ch{it['ch']} {it['pid']}"
pickle.dump(items,open('/tmp/master.pkl','wb'))
print('items:',len(items))
print('unique UIDs:',len({i["uid"] for i in items}))
print('collided native IDs made unique:', sum(1 for _,v in collections.Counter(re.sub(r'\s*\((algo|static)\)\s*$','',i['pid'],flags=re.I) for i in items).items() if v>1))
print('used:',sum(1 for i in items if i['used_in']),' ambiguous-resolved:',sum(1 for i in items if i['amb']))
print('HW/quiz IDs not in bank:',missing)
print('figure:',dict(collections.Counter(i['figure'] for i in items)))
print('cata:',sum(i['cata'] for i in items),' nopt=0:',sum(1 for i in items if i['nopt']==0))
