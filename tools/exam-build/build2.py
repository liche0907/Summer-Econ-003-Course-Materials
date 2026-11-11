import re, pickle, collections
from reader import read_pdf
SRC='/mnt/user-data/uploads/ECON003_26S/Assignments/QB'
BANKS=[('QB1&3','QB1&3.pdf'),('QB4&5','QB4&5.pdf'),('QB6','QB6.pdf')]
IDRE=re.compile(r'^ID:\s*(.+)$')
OPT=re.compile(r'^([A-Z])\.\s*(.*)$')
ANS=re.compile(r'^Answers?:\s*(.*)$')
NUMQ=re.compile(r'^(\d+)\.\s*(.*)$')

items=[]
for key,fn in BANKS:
    pages=read_pdf(f'{SRC}/{fn}')
    cur={'main':[],'side':[],'pages':[]}
    for pno,pg in enumerate(pages,1):
        cur['side']+=pg['side']; cur['pages'].append(pno)
        for ln in pg['main']:
            m=IDRE.match(ln)
            if m:
                cur['pid']=m.group(1).strip(); cur['bank']=key
                items.append(cur)
                cur={'main':[],'side':[],'pages':[pno]}
            else:
                cur['main'].append(ln)
print('items parsed:', len(items), collections.Counter(i['bank'] for i in items))

def parse(it):
    lines=list(it['main'])
    if lines and NUMQ.match(lines[0]): lines[0]=NUMQ.match(lines[0]).group(2)
    stem=[]; runs=[]; cur=None; ans=[]; inans=False
    for ln in lines:
        a=ANS.match(ln)
        if a:
            inans=True
            if a.group(1).strip(): ans.append(a.group(1).strip())
            if cur: runs.append(cur); cur=None
            continue
        if inans: ans.append(ln); continue
        o=OPT.match(ln)
        if o:
            L=o.group(1)
            if L=='A':
                if cur: runs.append(cur)
                cur=[(L,o.group(2))]
            elif cur and ord(L)==ord(cur[-1][0])+1: cur.append((L,o.group(2)))
            else:
                if cur: runs.append(cur); cur=None
                stem.append(ln)
        else:
            if cur: cur[-1]=(cur[-1][0], (cur[-1][1]+' '+ln).strip())
            else: stem.append(ln)
    if cur: runs.append(cur)
    return stem, runs, ans

for it in items:
    it['stem'],it['runs'],it['ansl']=parse(it)
    it['nruns']=len(it['runs'])
    it['ndrop']=len(set(re.findall(r'\((\d+)\)', ' '.join(it['ansl']))))
    it['ntasks']=it['nruns']+it['ndrop']
pickle.dump(items,open('/tmp/items2.pkl','wb'))
print('option-runs per item:', dict(sorted(collections.Counter(i['nruns'] for i in items).items())))
print('dropdown groups per item:', dict(sorted(collections.Counter(i['ndrop'] for i in items).items())))
print('answer-tasks per item:', dict(sorted(collections.Counter(i['ntasks'] for i in items).items())))
