# -*- coding: utf-8 -*-
import json,re,os,collections
P=json.load(open('/tmp/POOL2.json'))
bad=collections.defaultdict(list)
XREF=re.compile(r'\b(as before|previous question|use the same|the figure above|earlier question|refer to (the )?(previous|earlier))\b',re.I)
for x in P:
    q=x['_q']; opts=[o[1] for o in x['options']]; stem=' '.join(x['stem'])
    if len(opts)<4: bad['fewer than 4 options'].append(q)
    if len(set(opts))!=len(opts): bad['duplicate option text'].append(q)
    if opts.count(x['key'])!=1: bad['key not exactly once in options'].append(q)
    if [o[0] for o in x['options']]!=list('ABCDE')[:len(opts)]: bad['option letters not A..'].append(q)
    if any(re.search(r'\ball of the above\b|\bnone of the above\b',o,re.I) for o in opts): bad['all/none of the above'].append(q)
    if XREF.search(stem): bad['cross-reference'].append(q)
    # a stem is valid if it ASKS (a question sentence) or CUES A COMPLETION
    # a question mark, or a sentence that BEGINS with an interrogative/imperative
    asks = bool(re.search(r'\?', stem)) or any(
        re.match(r'\s*(which|what|how|why|where|who|complete|identify|state|trace|explain|say)\b', s, re.I)
        for s in x['stem'])
    completes = stem.rstrip().endswith(':') or '______' in stem or bool(
        re.search(r'\b(if|that|because|to|is)\s*$', stem.rstrip()))
    if not (asks or completes): bad['stem neither asks nor cues a completion'].append(q)
    if x.get('fig') and not os.path.exists('figs/'+x['fig']+'.png'): bad['missing figure file'].append(q)
    for t in (x.get('tables') or []):
        if t and t.get('header') and any(len(r)!=len(t['header']) for r in t.get('rows',[])):
            bad['ragged table'].append(q)
    if x['src']=='pearson' and x.get('printed_n') in (4,) and len(opts)!=4: bad['padded a 4-option printed item'].append(q)
seen=collections.defaultdict(list)
for x in P: seen[(x['sec'],x['key'].strip().lower())].append(x['_q'])
for k,v in seen.items():
    if len(v)>1: bad['same key twice in one section'].append(tuple(v))
print('ITEMS',len(P),'| contiguous',[x['_q'] for x in P]==list(range(1,len(P)+1)))
if bad:
    for k,v in bad.items(): print('  FAIL',k,v)
else: print('  all structural checks pass')

DRAW={'7':(5,2),'8':(6,2),'9':(5,3),'10':(3,2),'12':(5,3)}
SECN={'7.1':'Perfect competition and efficiency','7.3':'Allocation across industries','7.4':'Prices guide the invisible hand','7.5':'Equity and efficiency',
 '8.1':'The production possibilities curve','8.2':'Comparative advantage','8.3':'Trade between states','8.4':'Trade between countries','8.5':'Arguments against free trade',
 '9.1':'Externalities','9.2':'Private solutions','9.3':'Government solutions','9.4':'Public goods','9.5':'Common pool resources',
 '10.1':'§10.1.3 tax incidence and deadweight loss','10.2':'§10.2 regulation','10.3':'§10.3 government failures',
 '12.1':'A new market structure','12.2':'Sources of market power','12.3':"The monopolist's problem",'12.4':'Optimal quantity and price','12.5':'The cost of monopoly'}
rows=[]
for sec in sorted(SECN,key=lambda s:(int(s.split('.')[0]),float(s.split('.')[1]))):
    g=[x for x in P if x['sec']==sec]
    if not g: continue
    r=sum(1 for x in g if x['tier']=='routine'); t=sum(1 for x in g if x.get('tables') and any(u and u.get('header') for u in x['tables']))
    f=sum(1 for x in g if x.get('fig')); o=sum(1 for x in g if x['src']=='original')
    rows.append([sec,SECN[sec],len(g),r,len(g)-r,o,t,f,round(100*(t+f)/len(g))])
crows=[]
for ch in ['7','8','9','10','12']:
    g=[x for x in P if x['sec'].split('.')[0]==ch]
    r=sum(1 for x in g if x['tier']=='routine'); c=len(g)-r
    dr,dc=DRAW[ch]
    t=sum(1 for x in g if x.get('tables') and any(u and u.get('header') for u in x['tables']))
    f=sum(1 for x in g if x.get('fig'))
    crows.append([ch,len(g),r,c,dr+dc,dr,dc,round(r/dr,1),round(c/dc,1),round(100*(t+f)/len(g))])
json.dump({'sec':rows,'ch':crows},open('/tmp/mapping.json','w'),ensure_ascii=False,indent=1)
print()
print('%-6s %-38s %3s %4s %4s %4s %4s %4s %5s'%('§','','n','R','C','orig','tab','fig','vis'))
for r in rows: print('%-6s %-38s %3d %4d %4d %4d %4d %4d %4d%%'%tuple(r))
print()
print('%-4s %3s %4s %4s %5s %4s %4s %6s %6s %5s'%('ch','n','R','C','draw','dR','dC','covR','covC','vis'))
for r in crows: print('%-4s %3d %4d %4d %5d %4d %4d %5.1fx %5.1fx %4d%%'%tuple(r))
tot_t=sum(1 for x in P if x.get('tables') and any(u and u.get('header') for u in x['tables']))
tot_f=sum(1 for x in P if x.get('fig'))
print()
print('TOTAL %d items · %d routine / %d challenging · %d Pearson / %d original'%(
 len(P),sum(1 for x in P if x['tier']=='routine'),sum(1 for x in P if x['tier']!='routine'),
 sum(1 for x in P if x['src']=='pearson'),sum(1 for x in P if x['src']=='original')))
print('VISUAL %d tables + %d figure placements = %d%% of items, from %d distinct figures'%(
 tot_t,tot_f,round(100*(tot_t+tot_f)/len(P)),len(set(x['fig'] for x in P if x.get('fig')))))
