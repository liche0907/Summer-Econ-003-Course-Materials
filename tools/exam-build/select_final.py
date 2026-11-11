import csv,re,collections,json
rows=list(csv.DictReader(open('ECON003_Final_PostMidterm_Audit_v2.csv',encoding='utf-8')))
def secs(t):
    m=re.findall(r'(\d+)\s*m',t); s=re.findall(r'(\d+)\s*s',t)
    return (int(m[0])*60 if m else 0)+(int(s[0]) if s else 0)
for r in rows: r['t']=secs(r['est_time'])

DRAW  ={'7':7,'8':8,'9':8,'10':5,'12':8}
DRAW_R={'7':5,'8':6,'9':5,'10':3,'12':5}
DRAW_C={'7':2,'8':2,'9':3,'10':2,'12':3}
POOL  ={'7':23,'8':27,'9':27,'10':17,'12':26}
PEARS ={'7':20,'8':25,'9':25,'10':11,'12':19}

cand=[r for r in rows if r['scope']=='IN' and r['cls']!='DRAWTOOL' and r['key_printed']=='1']
LBL={'Easy':0,'Moderate':1,'Hard':2,'':1}

# ---- tier: rank within chapter by (est_time, publisher label); top share -> challenging
sel_tier={}
for ch in DRAW:
    items=[r for r in cand if r['ch']==ch]
    share=DRAW_C[ch]/DRAW[ch]
    n_c=round(len(items)*share)
    ranked=sorted(items,key=lambda r:(-r['t'],-LBL[r['pub_diff']]))
    for i,r in enumerate(ranked): sel_tier[(r['bank'],r['order'])]='challenging' if i<n_c else 'routine'
    cut=ranked[n_c-1]['t'] if n_c else None
    print('ch%-3s items=%-3d challenging=%-3d cut at est_time>=%ss'%(ch,len(items),n_c,cut))

for r in cand: r['tier']=sel_tier[(r['bank'],r['order'])]

# ---- pool tier targets, proportional to draw tiers
POOL_R={};POOL_C={}
for ch in POOL:
    c=round(POOL[ch]*DRAW_C[ch]/DRAW[ch]); POOL_C[ch]=c; POOL_R[ch]=POOL[ch]-c
print('\npool tiers:',{c:(POOL_R[c],POOL_C[c]) for c in POOL})

# ---- Pearson share of each tier, proportional
PE_R={};PE_C={}
for ch in POOL:
    frac=PEARS[ch]/POOL[ch]
    PE_C[ch]=min(POOL_C[ch],round(POOL_C[ch]*frac)); PE_R[ch]=PEARS[ch]-PE_C[ch]
    if PE_R[ch]>POOL_R[ch]:
        d=PE_R[ch]-POOL_R[ch]; PE_R[ch]-=d; PE_C[ch]=min(POOL_C[ch],PE_C[ch]+d)
print('pearson per tier:',{c:(PE_R[c],PE_C[c]) for c in POOL})
print('originals per tier:',{c:(POOL_R[c]-PE_R[c],POOL_C[c]-PE_C[c]) for c in POOL})

COST={'CLEAN':0,'CONVERT':1,'CLIPPED':2,'SPLIT':2}
def pick(ch,tier,n):
    """section-balanced greedy, cheapest-first, reuse-aware"""
    pot=[r for r in cand if r['ch']==ch and r['tier']==tier]
    if n>len(pot): return pot,n-len(pot)
    bysec=collections.defaultdict(list)
    for r in pot: bysec[r['sec']].append(r)
    for s in bysec:
        bysec[s].sort(key=lambda r:(COST[r['cls']], 0 if r['practiced_in'] else 1, -r['t']))
    quota={s:len(v)*n/len(pot) for s,v in bysec.items()}
    out=[];taken=collections.Counter()
    while len(out)<n:
        # section with the largest unmet quota that still has stock
        c=[s for s in bysec if taken[s]<len(bysec[s])]
        if not c: break
        s=max(c,key=lambda s:(quota[s]-taken[s], len(bysec[s])))
        out.append(bysec[s][taken[s]]); taken[s]+=1
    return out,max(0,n-len(out))

SEL=[];GAPS=[]
for ch in ['7','8','9','10','12']:
    for tier,need in (('routine',PE_R[ch]),('challenging',PE_C[ch])):
        got,short=pick(ch,tier,need)
        for r in got: r['pool_tier']=tier; SEL.append(r)
        if short: GAPS.append((ch,tier,short))
print('\nselected Pearson items:',len(SEL),' target',sum(PEARS.values()))
if GAPS: print('SHORTFALL:',GAPS)
json.dump([{k:v for k,v in r.items()} for r in SEL],open('/tmp/sel.json','w'))
