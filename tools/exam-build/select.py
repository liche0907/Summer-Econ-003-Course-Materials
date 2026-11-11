import pickle, collections, json
m=pickle.load(open('/tmp/master.pkl','rb'))
for i in m: i['sel']=''

NEED={'P':{1:10,3:13,4:20,5:20,6:19},'R':{1:5,3:6,4:9,5:9,6:9}}
DIFF={'P':{1:(8,2),3:(10,3),4:(13,7),5:(13,7),6:(12,7)},
      'R':{1:(4,1),3:(5,1),4:(6,3),5:(6,3),6:(6,3)}}
TYPE={'P':{1:{'G-fig':0,'G-reason':0,'Quant':3,'Concept':5,'Defn':2},
           3:{'G-fig':1,'G-reason':0,'Quant':6,'Concept':6,'Defn':0},
           4:{'G-fig':8,'G-reason':5,'Quant':2,'Concept':3,'Defn':2},
           5:{'G-fig':5,'G-reason':4,'Quant':6,'Concept':3,'Defn':2},
           6:{'G-fig':6,'G-reason':4,'Quant':4,'Concept':2,'Defn':3}},
      'R':{1:{'G-fig':0,'G-reason':0,'Quant':2,'Concept':2,'Defn':1},
           3:{'G-fig':1,'G-reason':0,'Quant':2,'Concept':3,'Defn':0},
           4:{'G-fig':2,'G-reason':2,'Quant':1,'Concept':3,'Defn':1},
           5:{'G-fig':3,'G-reason':2,'Quant':2,'Concept':2,'Defn':0},
           6:{'G-fig':2,'G-reason':2,'Quant':2,'Concept':2,'Defn':1}}}
COST=lambda i: 0 if i['tier']=='A' else 5 if i['tier']=='B' else 10 if i.get('salvage')=='Yes' else 40 if i['tier']=='C' else 70

log=[]
for bucket in ['P','R']:
    for ch in [1,3,4,5,6]:
        want=NEED[bucket][ch]
        pool=[i for i in m if i['ch']==ch and not i['sel']
              and ((i['used_in']!=[]) if bucket=='R' else (i['used_in']==[]))]
        tq=dict(TYPE[bucket][ch]); r,c=DIFF[bucket][ch]; dq={'routine':r,'challenging':c}
        chosen=[]
        while len(chosen)<want and pool:
            best=None;bs=-1e9
            for i in pool:
                s=0
                s+= 120 if tq.get(i['qtype2'],0)>0 else -40
                s+= 120 if dq.get(i['dtier'],0)>0 else -40
                s-= COST(i)
                s+= min(i['nopt'],5)          # prefer richer option sets
                if s>bs: bs, best = s, i
            chosen.append(best); pool.remove(best)
            tq[best['qtype2']]=tq.get(best['qtype2'],0)-1
            dq[best['dtier']]-=1
        for i in chosen: i['sel']=bucket
        got_t=collections.Counter(i['qtype2'] for i in chosen)
        got_d=collections.Counter(i['dtier'] for i in chosen)
        got_c=collections.Counter(i['tier'] if i.get('salvage')!='Yes' else 'S' for i in chosen)
        log.append((bucket,ch,len(chosen),want,dict(got_t),dict(got_d),dict(got_c)))
pickle.dump(m,open('/tmp/master.pkl','wb'))

TY=['G-fig','G-reason','Quant','Concept','Defn']
for bucket in ['P','R']:
    print(f"\n=== {'PEARSON-NEW' if bucket=='P' else 'REUSED'} ===")
    print(f"{'Ch':>3}{'got':>5}{'want':>5} | "+''.join(f'{t:>10}' for t in TY)+f" | {'rout':>5}{'chal':>5} | conversion")
    for b,ch,g,w,t,d,cst in log:
        if b!=bucket: continue
        tgt=TYPE[b][ch]
        tt=''.join(f"{t.get(x,0)}/{tgt.get(x,0):<7}" for x in TY)
        print(f"{ch:>3}{g:>5}{w:>5} | {tt} | {d.get('routine',0):>5}{d.get('challenging',0):>5} | {cst}")
sel=[i for i in m if i['sel']]
print(f"\nTOTAL SELECTED: {len(sel)}  (P {len([i for i in sel if i['sel']=='P'])}, R {len([i for i in sel if i['sel']=='R'])})")
print('type mix:',dict(collections.Counter(i['qtype2'] for i in sel)))
print('difficulty:',dict(collections.Counter(i['dtier'] for i in sel)))
print('conversion tiers:',dict(collections.Counter(i['tier'] if i.get('salvage')!='Yes' else 'Salvage' for i in sel)))
gf=[i for i in sel if i['qtype2']=='G-fig']
print(f"\nFIGURE WORK: {len(gf)} figure-based items selected")
print('  render+crop only (already Tier A/B/Salvage):',len([i for i in gf if i['tier'] in 'AB' or i.get('salvage')=='Yes']))
print('  need full redraw + conversion (Tier C/D):',len([i for i in gf if i['tier'] in 'CD' and i.get('salvage')!='Yes']))
