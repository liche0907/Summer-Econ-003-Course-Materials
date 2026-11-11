# -*- coding: utf-8 -*-
"""Working-time estimate per item, in seconds. Keyed by LABEL, never by number,
because item numbers shift whenever anything is added or retired.

Rubric — discrete operations a prepared student must perform:
  45  recall or definition; no reading and no arithmetic
  60  read ONE value off a figure or table, or apply one stated rule
  75  one comparison or one-step calculation
 105  two or three chained steps
 150  build a column across >=3 rows, or two areas off a graph
 200+ full welfare accounting from a schedule, or an assignment problem across two lists
"""
import json,statistics,random,collections
P=json.load(open('/tmp/POOL2.json'))
HAND={

 'Text Problem 3 (algo)':230,   # 4 buyers matched against 4 sellers, then two totals and a difference
 'Text Problem 8 (algo) c':215, # price floor off an 11-row schedule
 'Text Problem 10 (static) c':200, # the ladder, then 3 CS terms and 2 PS terms
 'O-7.1-2':150,'O-7.1-R7':120,'Text Problem 2 (static)':150,
 'Text Problem 11 (static)':None,'Concept Question 7.3.1 (algo)':90,'O-7.4-R14':90,
 'Concept Check 8.1.1.1 (algo)':105,'Concept Question 8.1.5 (algo)':200,
 'Text Problem 2 (algo)':120,'Concept Question 8.2.3 (static)':130,'Text Problem 3 (static)':None,
 'O-8.2-1':110,'O-8.2-R29':100,'Concept Question 8.3.3 (static) a':120,
 'Text Problem 10 (static) b':150,'Text Problem 10 (static) a':150,'O-8.4-1':90,'O-8.4-2':90,
 'Text Problem 9 (algo) a':105,'Text Problem 9 (algo) b':120,
 'Concept Question 9.3.2 (static) a':75,'Concept Question 9.3.3 (static) a':75,
 'Concept Question 9.3.3 (static) b':90,'O-9.3-R63':130,'O-9.3-4':105,'O-9.4-1':130,
 'O-10.1.3-2':130,'O-10.1.3-4':90,'NEW-10.1-a':105,'O-10.1-R78':90,
 'Text Problem 8 (algo) b':215,
 'Review Question 8 (static) b':120,'Concept Question 12.3.5 (static) a':140,'O-12.3-4':105,
 'Text Problem 5 (static) b':180,'Text Problem 5 (static) a':120,'O-12.4-R116':130,
 'O-12.5-1':90,'O-12.5-R119':110,
}
# labels that repeat across chapters need the section too
BYSEC={('Text Problem 11 (static)','7.4'):105,('Text Problem 11 (static)','9.4'):170,
       ('Text Problem 3 (static)','8.2'):160,('Text Problem 3 (static)','12.4'):120}
def default(x):
    b=45 if x['tier']=='routine' else 75
    if x.get('fig'): b+=25
    if x.get('tables') and any(t and t.get('header') for t in x['tables']): b+=35
    return b
for x in P:
    t=BYSEC.get((x['label'],x['sec']))
    if t is None: t=HAND.get(x['label'])
    x['_t']=t if t else default(x)
json.dump(P,open('/tmp/POOL2.json','w'),ensure_ascii=False,indent=1)

DRAW={'7':(5,2),'8':(6,2),'9':(5,3),'10':(3,2),'12':(5,3)}
over=[x for x in sorted(P,key=lambda y:-y['_t']) if x['_t']>180]
print('OVER 3 MINUTES:',len(over))
for x in over: print('  %4ds  Q%-4d %-30s %s'%(x['_t'],x['_q'],x['label'],x['sec']))
print('\n2:30 - 3:00')
for x in sorted(P,key=lambda y:-y['_t']):
    if 150<x['_t']<=180: print('  %4ds  Q%-4d %-30s %s'%(x['_t'],x['_q'],x['label'],x['sec']))
print('\npool mean %.0f s   median %.0f s'%(statistics.mean(x['_t'] for x in P),statistics.median(x['_t'] for x in P)))
print('by chapter (mean s): '+' · '.join('%s %.0f'%(c,statistics.mean(x['_t'] for x in P if x['sec'].split('.')[0]==c)) for c in ('7','8','9','10','12')))

random.seed(7); tot=[];longs=[]
for _ in range(20000):
    s=0;L=0
    for ch,(dr,dc) in DRAW.items():
        g=[x for x in P if x['sec'].split('.')[0]==ch]
        for tier,n in (('routine',dr),('challenging',dc)):
            pick=random.sample([x for x in g if x['tier']==tier],n)
            s+=sum(x['_t'] for x in pick); L+=sum(1 for x in pick if x['_t']>180)
    tot.append(s);longs.append(L)
tot.sort()
print('\n36 DRAWN ITEMS — 20,000 simulated papers')
for lab,v in (('median',.5),('90th pct',.90),('99th pct',.99)):
    print('  %-10s %5.1f min'%(lab,tot[int(v*(len(tot)-1))]/60))
print('  worst      %5.1f min'%(tot[-1]/60))
c=collections.Counter(longs)
print('  items over 3 min per paper:  0 → %.0f%%   1 → %.0f%%   2+ → %.0f%%'%(
  100*c[0]/len(longs),100*c[1]/len(longs),100*sum(v for k,v in c.items() if k>=2)/len(longs)))
print('\n  WINDOW: 180 minutes')
OBS=86.9  # seconds per item actually taken on the midterm (1:12:26 over 50 items)
MOD=statistics.mean(x['_t'] for x in P)
k=OBS/MOD
print('  observed midterm pace %.0f s/item vs model %.0f s/item  ->  calibration x%.2f'%(OBS,MOD,k))
for lab,v in (('median',.5),('90th pct',.90),('99th pct',.99)):
    m=tot[int(v*(len(tot)-1))]/60*k
    print('  calibrated %-9s %5.1f min for 36  ->  whole 60-item paper about %5.1f min of 180'%(lab,m,m*60/36))
