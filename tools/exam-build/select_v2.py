import csv,re,collections,json
rows=list(csv.DictReader(open('ECON003_Final_PostMidterm_Audit_v2.csv',encoding='utf-8')))
def secs(t):
    m=re.findall(r'(\d+)\s*m',t); s=re.findall(r'(\d+)\s*s',t)
    return (int(m[0])*60 if m else 0)+(int(s[0]) if s else 0)
for r in rows: r['t']=secs(r['est_time'])

# lecture content slides per section, + examinable-page boost (examinable pages count double)
SLIDES={'7.1':10,'7.2':0,'7.3':7,'7.4':13,'7.5':5,
        '8.1':5,'8.2':7,'8.3':4,'8.4':7,'8.5':4,
        '9.1':9,'9.2':3,'9.3':9,'9.4':7,'9.5':5,
        '10.1':8,'10.2':3,'10.3':1,
        '12.1':1,'12.2':4,'12.3':6,'12.4':2,'12.5':2,'12.7':2}
EXAM  ={'7.1':1,'7.3':2,'7.4':1,'7.5':0,
        '8.1':1,'8.2':2,'8.3':0,'8.4':1,'8.5':2,
        '9.1':2,'9.2':1,'9.3':1,'9.4':3,'9.5':0,
        '10.1':5,'10.2':1,'10.3':0,
        '12.1':0,'12.2':1,'12.3':3,'12.4':2,'12.5':2,'12.7':1}
W={s:SLIDES[s]+EXAM.get(s,0) for s in SLIDES}

DRAW  ={'7':7,'8':8,'9':8,'10':5,'12':8}
DRAW_R={'7':5,'8':6,'9':5,'10':3,'12':5}
DRAW_C={'7':2,'8':2,'9':3,'10':2,'12':3}
POOL  ={'7':23,'8':27,'9':27,'10':17,'12':26}
PEARS ={'7':20,'8':26,'9':25,'10':10,'12':19}
SECS_OF={'7':['7.1','7.3','7.4','7.5'],'8':['8.1','8.2','8.3','8.4','8.5'],
         '9':['9.1','9.2','9.3','9.4','9.5'],'10':['10.1','10.2','10.3'],
         '12':['12.1','12.2','12.3','12.4','12.5','12.7']}

def largest_remainder(weights,total):
    tw=sum(weights.values()); raw={k:total*w/tw for k,w in weights.items()}
    out={k:int(v) for k,v in raw.items()}; rem=total-sum(out.values())
    for k in sorted(raw,key=lambda k:-(raw[k]-out[k]))[:rem]: out[k]+=1
    return out

# ---- OUT OF SCOPE: 7.2 never lectured
for r in rows:
    if r['sec']=='7.2': r['scope']='OUT-7.2-not-lectured'

cand=[r for r in rows if r['scope']=='IN' and r['cls']!='DRAWTOOL' and r['key_printed']=='1']
LBL={'Easy':0,'Moderate':1,'Hard':2,'':1}

# ---- tier: rank within chapter by est_time (publisher label breaks ties)
for ch in DRAW:
    items=[r for r in cand if r['ch']==ch]
    n_c=round(len(items)*DRAW_C[ch]/DRAW[ch])
    for i,r in enumerate(sorted(items,key=lambda r:(-r['t'],-LBL[r['pub_diff']]))):
        r['tier']='challenging' if i<n_c else 'routine'

print('%-5s %-6s %5s %8s %8s %7s'%('ch','sec','wgt','poolTgt','supply','shortfall->orig'))
PLAN={}
for ch in ['7','8','9','10','12']:
    w={s:W[s] for s in SECS_OF[ch]}
    tgt=largest_remainder(w,POOL[ch])
    PLAN[ch]=tgt
    for s in SECS_OF[ch]:
        sup=len([r for r in cand if r['sec']==s])
        print('%-5s %-6s %5d %8d %8d %7s'%(ch,s,w[s],tgt[s],sup,'' if sup>=tgt[s] else '+%d'%(tgt[s]-sup)))
json.dump({'PLAN':PLAN,'W':W},open('/tmp/plan.json','w'))

# ---------- final selection ----------
ORIG={'7':{'7.1':1,'7.4':1},'8':{'8.2':1,'8.4':1},'9':{'9.1':1,'9.4':1},
      '10':{'10.1':7},'12':{'12.7':3,'12.3':1,'12.4':1,'12.5':1,'12.2':1}}
COST={'CLEAN':0,'CONVERT':1,'CLIPPED':2,'SPLIT':2}
SEL=[];SHORT=[]
for ch in ['7','8','9','10','12']:
    for s in SECS_OF[ch]:
        need=PLAN[ch][s]-ORIG[ch].get(s,0)
        pot=[r for r in cand if r['sec']==s]
        nC=round(need*DRAW_C[ch]/DRAW[ch])
        for tier,k in (('challenging',nC),('routine',need-nC)):
            p=[r for r in pot if r['tier']==tier]
            p.sort(key=lambda r:(COST[r['cls']], 1 if r['practiced_in'] else 0, -r['t']))
            take=p[:k]
            if len(take)<k: SHORT.append((ch,s,tier,k-len(take)))
            for r in take: r['pool_tier']=tier; SEL.append(r)
# fill any tier shortfall from the other tier in the same section
for ch,s,tier,n in SHORT:
    other='routine' if tier=='challenging' else 'challenging'
    p=[r for r in cand if r['sec']==s and r['tier']==other and 'pool_tier' not in r]
    p.sort(key=lambda r:(COST[r['cls']],-r['t']) if tier=='challenging' else (COST[r['cls']],r['t']))
    for r in p[:n]: r['pool_tier']=tier; SEL.append(r)
print('\nPearson selected:',len(SEL),' originals:',sum(sum(v.values()) for v in ORIG.values()),
      ' pool:',len(SEL)+sum(sum(v.values()) for v in ORIG.values()))
import collections
print('%-4s %6s %6s %6s | %-28s | %6s'%('ch','Pears','R','C','class mix','reuse'))
for ch in ['7','8','9','10','12']:
    g=[r for r in SEL if r['ch']==ch]
    cm=collections.Counter(r['cls'] for r in g)
    print('%-4s %6d %6d %6d | %-28s | %d'%(ch,len(g),
      sum(1 for r in g if r['pool_tier']=='routine'),sum(1 for r in g if r['pool_tier']=='challenging'),
      ' '.join('%s:%d'%(k[:5],v) for k,v in cm.most_common()),
      sum(1 for r in g if r['practiced_in'])))
pr=sum(1 for r in SEL if r['practiced_in'])
print('reuse %d/%d = %.0f%%'%(pr,len(SEL),100*pr/len(SEL)))
print('needs rework: CONVERT %d  CLIPPED %d  SPLIT %d  = %d of %d'%(
   sum(1 for r in SEL if r['cls']=='CONVERT'),sum(1 for r in SEL if r['cls']=='CLIPPED'),
   sum(1 for r in SEL if r['cls']=='SPLIT'),
   sum(1 for r in SEL if r['cls']!='CLEAN'),len(SEL)))
json.dump({'sel':SEL,'orig':ORIG,'plan':PLAN},open('/tmp/sel2.json','w'))
