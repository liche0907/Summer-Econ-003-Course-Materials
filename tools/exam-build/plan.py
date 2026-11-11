import re, pickle, json, collections
m=pickle.load(open('/tmp/master.pkl','rb'))
D=json.load(open('/tmp/sel.json')); order={d['uid']:n+1 for n,d in enumerate(D)}
OPTL=re.compile(r'^([A-Z])\.\s')
DROPMARK=re.compile(r'\((\d+)\)')

def segments(c):
    """cut the item into parts: each part = its own lead-in text + its option run."""
    segs=[]; buf=[]
    lines=list(c['stem'])
    # rebuild interleaved order: stem lines and runs alternate in source order,
    # runs already extracted, so attach the k-th run to the text collected before it
    ri=0
    for ln in lines:
        buf.append(ln)
    # source order was lost for >1 run; use per-run lead-in = text up to first option of that run
    if c['nruns']<=1:
        segs.append(dict(text=buf, run=c['runs'][0] if c['runs'] else None))
    else:
        # split the stem text evenly at sentence boundaries that introduce each run
        cut=[]; cur=[]
        for ln in buf:
            cur.append(ln)
            if re.search(r'[?_.]\s*$', ln) and len(cut)<c['nruns']-1 and len(cur)>=1:
                cut.append(cur); cur=[]
        cut.append(cur)
        while len(cut)<c['nruns']: cut.append([])
        for k,r in enumerate(c['runs']): segs.append(dict(text=cut[k] if k<len(cut) else [], run=r))
    drops=sorted({k for k,_ in re.findall(r'\((\d+)\)\s*([^\n(]*)','\n'.join(c['ansl']))})
    return segs, drops

def action(i):
    c=i['clean']; t=c['tasks']
    if t==1: return 'KEEP','Single question — no change.'
    if t>=4: return 'REDUCE',f'{t} answer-tasks. Keep one core question; the scaffolding is what makes it long.'
    if c['nruns']>=2: return 'SPLIT',f'{c["nruns"]} independent multiple-choice questions — split, restating context in each.'
    if c['nruns']==1 and c['ndrop2']>=1: return 'SPLIT',f'One MC plus {c["ndrop2"]} dropdown blank(s) — split into the MC and one combination-option item.'
    if c['nnum']>=2: return 'REDUCE',f'{c["nnum"]} numeric answers chained — keep the terminal question and give students the intermediate values.'
    return 'REDUCE','Collapse to a single core question.'

sel=[i for i in m if i.get('sel')]
for i in sel:
    i['segs'],i['drops']=segments(i['clean'])
    i['act'],i['actwhy']=action(i)
pickle.dump(m,open('/tmp/master.pkl','wb'))
c=collections.Counter(i['act'] for i in sel)
print('ACTIONS:',dict(c))
split=[i for i in sel if i['act']=='SPLIT']; red=[i for i in sel if i['act']=='REDUCE']
print(f'  SPLIT {len(split)} items -> {sum(i["clean"]["tasks"] for i in split)} questions (+{sum(i["clean"]["tasks"]-1 for i in split)})')
print(f'  REDUCE {len(red)} items -> {len(red)} questions (drops {sum(i["clean"]["tasks"]-1 for i in red)} tasks of work)')
print(f'  pool after: {len([i for i in sel if i["act"]=="KEEP"]) + sum(i["clean"]["tasks"] for i in split) + len(red)} questions from the 120 selected')
print()
print('REDUCE list (heaviest first):')
for i in sorted(red,key=lambda i:-i['clean']['tasks'])[:12]:
    print(f"  Q{order[i['uid']]:>3} {i['uid']} Ch{i['ch']} {i['clean']['tasks']:>2} tasks {i['time_s']:>4}s | {i['clean']['stem'][0][:64] if i['clean']['stem'] else ''}")
