import json,re,collections
R=json.load(open('/tmp/audit_final.json'))

OUT_101 = {'Concept Question 10.1.7','Concept Question 10.1.8','Concept Question 10.1.10',
           'Concept Check 10.1.1.1','Concept Check 10.1.1.2','Concept Check 10.1.2.1',
           'Concept Check 10.1.2.2','Concept Check 10.1.2.3','Concept Check 10.1.2.4'}

def basepid(p): return re.sub(r'\s*\((algo|static)\)\s*$','',p or '').strip()

OPTBLK=re.compile(r'^\s*A\.\s',re.M)
NUMENT=re.compile(r'Enter your (answer|response)|Round your (answer|response)|\(Enter',re.I)
DRAW=re.compile(r'drawing tool|graphing question|Using the (line|point|rectangle|multipoint|curved line)|Sketch the|Show (the effect|it on the graph)|Draw the',re.I)

for r in R:
    p=basepid(r['pid']); r['base']=p
    r['nparts']=len(OPTBLK.findall(r['raw'])) or (1 if r['nopt'] else 0)
    r['numeric']=bool(NUMENT.search(r['raw']))
    r['draw']=bool(DRAW.search(r['raw']))
    # scope
    if r['ch']==10 and r['sec']=='10.1' and p in OUT_101: r['scope']='OUT-10.1.1/2'
    else: r['scope']='IN'
    # effort class (most expensive wins)
    if r['scope']!='IN':                 c='OUT'
    elif r['draw']:                      c='REDRAW'
    elif r['nclip']>0:                   c='CLIPPED'
    elif r['nparts']>=2:                 c='SPLIT'
    elif r['cata']:                      c='CONVERT'
    elif r['cloze'] or r['numeric'] or r['nopt']==0: c='CONVERT'
    elif r['nopt']>=4:                   c='CLEAN'
    else:                                c='CONVERT'
    r['cls']=c

json.dump(R,open('/tmp/audit_final.json','w'))

ORD=['CLEAN','CONVERT','SPLIT','CLIPPED','REDRAW','OUT']
agg=collections.defaultdict(collections.Counter)
for r in R: agg[r['ch']][r['cls']]+=1; agg[r['ch']]['n']+=1; agg[r['ch']]['fig']+= (r['fig'] and r['scope']=='IN')
print('%-4s %5s | %6s %8s %6s %8s %7s | %5s %6s %6s'%('ch','raw','CLEAN','CONVERT','SPLIT','CLIPPED','REDRAW','OUT','inscope','figs'))
tot=collections.Counter()
for ch in sorted(agg):
    a=agg[ch]; ins=a['n']-a['OUT']
    for k in ORD+['n','fig']: tot[k]+=a[k]
    print('%-4s %5d | %6d %8d %6d %8d %7d | %5d %6d %6d'%(ch,a['n'],a['CLEAN'],a['CONVERT'],a['SPLIT'],a['CLIPPED'],a['REDRAW'],a['OUT'],ins,a['fig']))
print('%-4s %5d | %6d %8d %6d %8d %7d | %5d %6d %6d'%('ALL',tot['n'],tot['CLEAN'],tot['CONVERT'],tot['SPLIT'],tot['CLIPPED'],tot['REDRAW'],tot['OUT'],tot['n']-tot['OUT'],tot['fig']))
