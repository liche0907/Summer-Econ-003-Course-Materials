import json, re, pickle, unicodedata
from choices import choice_sets
from flags import truncated, TEXTBOOK
SRC='/mnt/user-data/uploads/ECON003_26S/Assignments/QB'
BK={'QB1&3':'QB1&3.pdf','QB4&5':'QB4&5.pdf','QB6':'QB6.pdf'}
D=json.load(open('/tmp/clean.json'))['items']
try: MERGE={int(k):v for k,v in json.load(open('/tmp/merge.json')).items()}
except Exception: MERGE={}
sq=lambda x:' '.join(str(x).split())
for _d in D:                                   # adopt the instructor's repaired wording
    fix=MERGE.get(_d['n'],{})
    if not fix: continue
    _d['fixed']=0
    for _p in _d['parts']:
        for _i,_o in enumerate(_p['opts']):
            if sq(_o) in fix:
                _p['opts'][_i]=fix[sq(_o)]; _d['fixed']+=1
m={x['uid']:x for x in pickle.load(open('/tmp/master.pkl','rb'))}
norm=lambda s: re.sub(r'[^a-z0-9]','',s.lower())
DRAW=re.compile(r'(drawing\s*tool|use the (line|point|multipoint|curved|rectangle|three point)|plot each point|label your (curve|line))',re.I)

out=[]
for d in D:
    i=m[d['uid']]
    lead=[l for p in d['parts'] for l in p['lead']]
    alltxt=' '.join(lead+[o for p in d['parts'] for o in p['opts']])
    hasblank=bool(keyedpre) if False else bool([o for o in d['other'] if re.match(r'^\(\d+\)',o)])
    ntr=0
    for ix,t in enumerate(lead):
        if not truncated(t): continue
        nxt=lead[ix+1] if ix+1<len(lead) else ''
        if hasblank and (re.match(r'^\(\d+\)',nxt) or re.search(r'\(\d\)',t)): continue
        ntr+=1
    ntr+=sum(1 for o in [x for p in d['parts'] for x in p['opts']] if truncated(o))
    isdraw=bool(DRAW.search(' '.join(lead)))
    # dropdown choice sets, kept only when one member matches this item's own keyed answer
    keyedpre=None
    keyed=[re.sub(r'^\(\d+\)\s*','',o).strip() for o in d['other'] if re.match(r'^\(\d+\)',o)]
    sets={}
    if keyed:
        raw=choice_sets(f"{SRC}/{BK[i['bank']]}", i['P']['pages'])
        for num,opts in raw.items():
            if any(norm(k) and norm(k) in [norm(o) for o in opts] for k in keyed): sets[num]=opts
    # truncation judged PER PART, and separable parts split regardless
    withopt=[p for p in d['parts'] if p['opts']]
    ptr=[sum(1 for t in list(p['lead'])+list(p['opts']) if truncated(t)) for p in d['parts']]
    separable = len(withopt)>=2
    status, rev, why = None, [], None
    if d['act'] not in ('DROP','REMOVE') and separable:
        subs=[]
        for ix,p in enumerate(d['parts']):
            if not p['opts']: continue
            n_tr=sum(1 for t in list(p['lead'])+list(p['opts']) if truncated(t))
            subs.append(dict(letter=chr(97+len(subs)),lead=p['lead'],opts=p['opts'],
                             ans=p.get('ans',''),tr=n_tr,
                             draw=bool(DRAW.search(' '.join(p['lead'])))))
        out.append(dict(n=d['n'],uid=d['uid'],ch=d['ch'],sec=d['sec'],act=d['act'],tasks=d['tasks'],
                        time=d['time'],parts=d['parts'],other=d['other'],
                        status='SPLIT INTO %d'%len(subs),
                        why='Parts are independent questions. Each becomes its own item, sourced back to %s.'%d['pid'],
                        rev=[],subs=subs,pid=d['pid'],bank=d['bank'],pages=d['pages'],
                        tb=bool(TEXTBOOK.search(' '.join(lead))),fixed=d.get('fixed',0)))
        continue
    if d['act'] in ('DROP','REMOVE'):
        status='DROPPED'; why=d['note']
    elif sets:
        status='REVISED'
        pool=set()
        for v in sets.values(): pool|={norm(w) for c in v for w in c.split()}
        def is_choice_list(l):
            ws=[norm(w) for w in re.sub(r'\(\d\)','',l).split() if norm(w)]
            return len(ws)>=3 and sum(1 for w in ws if w in pool)/len(ws) > 0.6
        ask=[l for l in lead if re.search(r'\(\d\)',l) and not is_choice_list(l)]
        keep=[l for l in lead if l not in ask and not is_choice_list(l)]
        rev=dict(scenario=keep, ask=ask, sets=sets, keyed=keyed,
                 nums=[o for o in d['other'] if not re.match(r'^\(\d+\)',o)])
        why='Scenario kept whole. The blanks become one multiple-choice question built from their own dropdown lists.'
    elif ntr:
        status='TEXT MISSING'; why=f'{ntr} passage(s) still cut off by the Pearson print export. Restore the wording from MyLab, then this can be revised — the numbers and structure are otherwise intact.'
    elif isdraw:
        status='NEEDS FIGURE'; why='Requires the plotting tool. Keep the scenario; supply a static figure and ask about the result. Figure to be drawn in the next batch.'
    elif d['act']=='KEEP' and sum(len(p['opts']) for p in d['parts'])>=4:
        status='NO CHANGE'
    else:
        nums=[o for o in d['other'] if not re.match(r'^\(\d+\)',o)]
        asks=[l for l in lead if re.search(r'(\benter your (response|answer)|__|\bis \$|\bwill be\b.*\.|how many|what is)', l, re.I)]
        def _f(x):
            try: return float(str(x).replace(',','').replace('$','').replace('−','-').strip())
            except Exception: return None
        def _fmt(v):
            if v is None: return None
            if abs(v-round(v))<1e-9: return f'{int(round(v)):,}'
            return f'{v:,.2f}'
        if nums:
            status='REVISED'
            keyv=nums[-1]                       # the terminal answer
            traps=[x for x in nums[:-1]][:3]    # Pearson's own intermediate values
            made=[]
            k=_f(keyv)
            if k is not None:
                seen={_fmt(k)}|{_fmt(_f(t)) for t in traps if _f(t) is not None}
                # other money figures in the scenario are the strongest invented distractors
                scen=' '.join(lead)
                others=[_f(x) for x in re.findall(r'\$\s?([\d,]+(?:\.\d+)?)', scen)]
                lo,hi=abs(k)/12.5, abs(k)*12.5          # only magnitudes a student might actually write
                inrange=lambda v: v is not None and lo<=abs(v)<=hi and abs(v-k)>1e-9
                cands=[k*12, k/12]                        # monthly vs yearly — the commonest slip
                cands+=[v*12 for v in others if v]        # a monthly figure annualised
                cands+=[v for v in others if v]           # a figure lifted straight from the scenario
                cands+=[k*2, k/2, k*10, k/10, -k]
                cands=[v for v in cands if inrange(v)]
                for v in cands:
                    f=_fmt(v)
                    if f and f not in seen and abs(v)>=0.01:
                        seen.add(f); made.append(f)
                    if len(traps)+len(made)>=4: break
            rev=dict(scenario=[l for l in lead if l not in asks], ask=asks or lead[-1:],
                     sets={}, keyed=[], nums=[], numeric=dict(key=keyv,traps=traps,made=made,all=nums))
            why=("Scenario kept whole. The chain of answers collapses to the final question only; "
                 "the intermediate values Pearson asks for become the distractors, so nothing is given away.")
        else:
            status='NEEDS REWRITE'
            why=f"{d['tasks']} separate answers. Scenario is sound — the ask needs collapsing to one question."
    out.append(dict(n=d['n'],uid=d['uid'],ch=d['ch'],sec=d['sec'],act=d['act'],tasks=d['tasks'],
                    time=d['time'],parts=d['parts'],other=d['other'],status=status,why=why,
                    rev=rev,subs=[],pid=d['pid'],bank=d['bank'],pages=d['pages'],
                    tb=bool(TEXTBOOK.search(' '.join(lead))),fixed=d.get('fixed',0)))
json.dump(out,open('/tmp/rev.json','w'))
import collections
print('STATUS ACROSS ALL 120:')
for k,v in collections.Counter(o['status'] for o in out).most_common(): print(f'  {k:<14} {v}')
