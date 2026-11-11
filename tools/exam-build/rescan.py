# -*- coding: utf-8 -*-
"""Overlap rescan: flags item pairs that test the same thing.
Three independent signals; a pair is reported when at least two fire."""
import json,re,itertools
P=json.load(open('/tmp/POOL2.json'))
STOP=set('''the a an of to in is are and or that this it for on at be as with what which
who where when how why not no all any both each every some more most less than then so
its their they them he she his her you your we our i if but by from into over under
figure shows show shown market markets price prices quantity quantities good goods
firm firms curve curves following statement statements true correct describes describe
one two three four five thousand million units unit'''.split())
def bag(t):
    return set(w for w in re.findall(r'[a-z]+',t.lower()) if w not in STOP and len(w)>2)
def jac(a,b):
    return len(a&b)/max(1,len(a|b))
def cov(a,b):
    return len(a&b)/max(1,min(len(a),len(b)))
rows=[]
for a,b in itertools.combinations(P,2):
    if a['sec'].split('.')[0]!=b['sec'].split('.')[0]: continue
    sa,sb=bag(' '.join(a['stem'])),bag(' '.join(b['stem']))
    ka,kb=bag(a['key']),bag(b['key'])
    oa=set(o[1] for o in a['options']); ob=set(o[1] for o in b['options'])
    sig_stem = cov(sa,sb)>=0.60
    sig_key  = cov(ka,kb)>=0.55
    sig_opt  = len(oa&ob)>=2
    sig_fig  = bool(a.get('fig')) and a.get('fig')==b.get('fig')
    n=sum([sig_stem,sig_key,sig_opt])
    if n>=2:
        rows.append(dict(qa=a['_q'],la=a['label'],qb=b['_q'],lb=b['label'],sec=a['sec']+'/'+b['sec'],
                         stem=round(cov(sa,sb),2),key=round(cov(ka,kb),2),shared_opts=len(oa&ob),
                         same_fig=sig_fig,
                         ta=(' '.join(a['stem']))[:70],tb=(' '.join(b['stem']))[:70],
                         ka=a['key'][:70],kb=b['key'][:70]))
rows.sort(key=lambda r:-(r['key']+r['stem']))
json.dump(rows,open('/tmp/rescan.json','w'),ensure_ascii=False,indent=1)
print('flagged pairs:',len(rows))
for r in rows:
    print('\nQ%-4d %-30s  vs  Q%-4d %-30s  [%s]'%(r['qa'],r['la'],r['qb'],r['lb'],r['sec']))
    print('   stem %.2f · key %.2f · shared options %d · same figure %s'%(r['stem'],r['key'],r['shared_opts'],r['same_fig']))
    print('   A:',r['ta']); print('      key:',r['ka'])
    print('   B:',r['tb']); print('      key:',r['kb'])
