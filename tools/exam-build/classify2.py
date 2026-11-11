import json,re,collections
R=json.load(open('/tmp/audit_final.json'))
DRAWTOOL=re.compile(r'drawing tool|graphing question|Using the (line|point|rectangle|multipoint|curved line)|Sketch the|Show (the effect of|it on the graph)|^\s*Draw the .*on Panel',re.I|re.M)
for r in R:
    r['drawtool']=bool(DRAWTOOL.search(r['raw']))
    if r['scope']!='IN': c='OUT'
    elif r['drawtool']:  c='DRAWTOOL'
    elif r['nclip']>0:   c='CLIPPED'
    elif r['nparts']>=2: c='SPLIT'
    elif r['cata'] or r['cloze'] or r['numeric'] or r['nopt']==0: c='CONVERT'
    elif r['nopt']>=4:   c='CLEAN'
    else:                c='CONVERT'
    r['cls']=c
json.dump(R,open('/tmp/audit_final.json','w'))
ORD=['CLEAN','CONVERT','SPLIT','CLIPPED','DRAWTOOL','OUT']
agg=collections.defaultdict(collections.Counter)
for r in R:
    a=agg[r['ch']]; a[r['cls']]+=1; a['n']+=1
    if r['scope']=='IN' and r['fig']: a['fig']+=1
print('%-4s %5s | %6s %8s %6s %8s %9s | %4s %8s %6s'%('ch','raw','CLEAN','CONVERT','SPLIT','CLIPPED','DRAWTOOL','OUT','in-scope','w/fig'))
tot=collections.Counter()
for ch in sorted(agg):
    a=agg[ch]
    for k in ORD+['n','fig']: tot[k]+=a[k]
    print('%-4d %5d | %6d %8d %6d %8d %9d | %4d %8d %6d'%(ch,a['n'],a['CLEAN'],a['CONVERT'],a['SPLIT'],a['CLIPPED'],a['DRAWTOOL'],a['OUT'],a['n']-a['OUT'],a['fig']))
print('%-4s %5d | %6d %8d %6d %8d %9d | %4d %8d %6d'%('ALL',tot['n'],tot['CLEAN'],tot['CONVERT'],tot['SPLIT'],tot['CLIPPED'],tot['DRAWTOOL'],tot['OUT'],tot['n']-tot['OUT'],tot['fig']))
