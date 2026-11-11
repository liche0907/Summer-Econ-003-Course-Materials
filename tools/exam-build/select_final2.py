import json,collections
N=json.load(open('/tmp/NORM_ALL.json'))
ORIG=json.load(open('originals_all.json'))
# lecture-weighted section targets; 12.7 removed and its 3 slots redistributed inside Ch 12
TGT={'7.1':7,'7.3':5,'7.4':8,'7.5':3,'8.1':5,'8.2':7,'8.3':3,'8.4':7,'8.5':5,
     '9.1':7,'9.2':3,'9.3':7,'9.4':7,'9.5':3,'10.1':12,'10.2':4,'10.3':1,
     '12.1':1,'12.2':6,'12.3':10,'12.4':5,'12.5':4}
assert sum(TGT.values())==120, sum(TGT.values())
osec=collections.defaultdict(list)
for o in ORIG: osec[o['sec']].append(o)
bysec=collections.defaultdict(list)
for x in N: bysec[x['sec']].append(x)
def score(x):
    return (0 if x['fig'] else 1, 1 if x['review'] else 0, len([i for i in x['issues'] if i['type']!='_resolved']))
POOL=[];RES=[];SHORT=[]
for s,t in TGT.items():
    need=t-len(osec[s])
    cand=sorted(bysec[s],key=score)
    if need>len(cand): SHORT.append((s,need-len(cand)))
    POOL+=cand[:need]; RES+=[dict(x,_why='section already at its lecture-weighted target') for x in cand[need:]]
    for o in osec[s]:
        POOL.append(dict(label=o['label'],sec=s,bank='',order='',tier=o['tier'],src='original',
            fig=o['figure'],stem=o['stem'],tables=[],options=o['options'],key=o['key'],
            distractors=['%s — %s'%(a,b) for a,b in o['distractors']],note=o.get('why',''),
            gap=o.get('gap',''),review='',issues=[],printed_n=0,cls='ORIGINAL'))
print('shortfalls:',SHORT)
print('POOL',len(POOL),'| pearson',sum(1 for x in POOL if x['src']=='pearson'),
      '| original',sum(1 for x in POOL if x['src']=='original'),'| reserve',len(RES))
c=collections.Counter(x['sec'] for x in POOL)
print('off target:',[s for s in TGT if c[s]!=TGT[s]])
# tiers: match each chapter's draw ratio
DRAW={'7':(5,2),'8':(6,2),'9':(5,3),'10':(3,2),'12':(5,3)}
import re
def numish(x):
    t=' '.join(x['stem'])+' '+' '.join(t for _,t in x['options'])
    return bool(re.search(r'\$\s?\d|\d+\s?(units|percent|%)|=\s*\d',t))
bych=collections.defaultdict(list)
for x in POOL: bych[x['sec'].split('.')[0]].append(x)
for ch,g in bych.items():
    R,C=DRAW[ch]; nC=round(len(g)*C/(R+C))
    def sc(x):
        s=3 if x['tier']=='challenging' else 0
        if x['src']=='original': s+= 1.5 if x['tier']=='challenging' else -1.5
        s+= 1 if x['fig'] else 0
        s+= 1 if x['tables'] else 0
        s+= 1 if numish(x) else 0
        return -s
    for i,x in enumerate(sorted(g,key=sc)): x['tier']='challenging' if i<nC else 'routine'
    print('  ch%-3s %2d items -> %2d routine / %2d challenging  (draw %d/%d, cov %.1fx/%.1fx)'%(
        ch,len(g),len(g)-nC,nC,R,C,(len(g)-nC)/R,nC/C))
t=collections.Counter(x['tier'] for x in POOL)
print('pool tiers:',dict(t),'= %.0f%% challenging'%(100*t['challenging']/len(POOL)))
print('option counts:',dict(collections.Counter(len(x['options']) for x in POOL)))
print('figures:',sum(1 for x in POOL if x['fig']),'| tables:',sum(1 for x in POOL if x['tables']))
json.dump(POOL,open('/tmp/POOL2.json','w'),indent=1); json.dump(RES,open('/tmp/RESERVE2.json','w'),indent=1)
