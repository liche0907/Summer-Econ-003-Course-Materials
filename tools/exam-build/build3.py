import re, pickle, collections, statistics
from reader import read_pdf
SRC='/mnt/user-data/uploads/ECON003_26S/Assignments/QB'
BANKS=[('QB1&3','QB1&3.pdf'),('QB4&5','QB4&5.pdf'),('QB6','QB6.pdf')]
IDRE=re.compile(r'^ID:\s*(.+)$'); OPT=re.compile(r'^([A-Z])\.\s*(.*)$')
ANS=re.compile(r'^Answers?:\s*(.*)$'); NUMQ=re.compile(r'^(\d+)\.\s*(.*)$')
NUMONLY=re.compile(r'^[-−$]?\s*[\d,]+(\.\d+)?%?$')

items=[]
for key,fn in BANKS:
    cur={'main':[],'side':[],'pages':[]}
    for pno,pg in enumerate(read_pdf(f'{SRC}/{fn}'),1):
        cur['side']+=[t for t,_ in pg['side']]; cur['pages'].append(pno)
        for t,x in pg['main']:
            m=IDRE.match(t)
            if m:
                cur['pid']=m.group(1).strip(); cur['bank']=key; items.append(cur)
                cur={'main':[],'side':[],'pages':[pno]}
            else: cur['main'].append((t,x))
assert len(items)==323, len(items)

def parse(it):
    lines=list(it['main'])
    if lines and NUMQ.match(lines[0][0]): lines[0]=(NUMQ.match(lines[0][0]).group(2), lines[0][1])
    optxs=[x for t,x in lines if OPT.match(t)]
    optx=statistics.mode(optxs) if optxs else 1e9
    parts=[]; lead=[]; run=[]; ansblk=[]; inans=False
    def flush():
        if lead or run: parts.append(dict(lead=lead[:], opts=run[:]))
    for t,x in lines:
        a=ANS.match(t)
        if a:
            inans=True
            if a.group(1).strip(): ansblk.append(a.group(1).strip())
            continue
        if inans: ansblk.append(t); continue
        o=OPT.match(t)
        if o and abs(x-optx)<3:
            run.append((o.group(1),o.group(2)))
        elif run and x>optx+4:
            run[-1]=(run[-1][0],(run[-1][1]+' '+t).strip())          # wrapped option text
        else:
            if run: flush(); lead=[]; run=[]                          # new part begins
            lead.append(t)
    flush()
    if not parts: parts=[dict(lead=[t for t,_ in lines],opts=[])]
    # answers: a new answer starts at a letter, a (n) marker, or a bare number
    ans=[]; 
    for t in ansblk:
        t=t.strip()
        if OPT.match(t) or re.match(r'^\(\d+\)',t) or NUMONLY.match(t): ans.append(t)
        elif ans: ans[-1]=(ans[-1]+' '+t).strip()
        else: ans.append(t)
    return parts, ans

for it in items:
    it['parts'],it['ans']=parse(it)
    lets=[a for a in it['ans'] if OPT.match(a)]
    drops=[a for a in it['ans'] if re.match(r'^\(\d+\)',a)]
    nums=[a for a in it['ans'] if NUMONLY.match(a)]
    it['tasks']=max(1,len(lets)+len(drops)+len(nums))
    # map the k-th lettered answer onto the k-th part that has options
    withopt=[p for p in it['parts'] if p['opts']]
    for k,p in enumerate(withopt): p['ans']=lets[k] if k<len(lets) else ''
    it['other_ans']=drops+nums
pickle.dump(items,open('/tmp/items3.pkl','wb'))
print('parsed',len(items))
print('parts per item:',dict(sorted(collections.Counter(len(i['parts']) for i in items).items())))
print('tasks per item:',dict(sorted(collections.Counter(i['tasks'] for i in items).items())))
q=[i for i in items if i['pid'].startswith('Concept Question 1.2.4')][0]
print('\nQ7 CHECK —',q['pid'])
for n,p in enumerate(q['parts'],1):
    print(f'  Part {n}:')
    for l in p['lead']: print('     ',l[:96])
    for L,t in p['opts']: print(f'      {L}. {t[:88]}')
    print('      ANS:',p.get('ans','')[:96])
