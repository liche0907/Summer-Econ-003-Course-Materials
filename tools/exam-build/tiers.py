import pickle, collections, statistics
m=pickle.load(open('/tmp/master.pkl','rb'))
# cognitive-load score: Pearson difficulty dominates, estimated time breaks ties inside a band
RANK={'Easy':0,'Moderate':1,'Hard':2}
for i in m: i['load']=RANK.get(i['difficulty'],1)*10000 + (i['time_s'] or 0)
# per chapter, mark the top 40% of the ELIGIBLE pool by load as 'challenging'
for ch in [1,3,4,5,6]:
    el=[i for i in m if i['ch']==ch and (i['tier'] in 'ABCD')]
    el.sort(key=lambda i:-i['load'])
    cut=int(round(len(el)*0.40))
    for n,i in enumerate(el): i['dtier']='challenging' if n<cut else 'routine'
pickle.dump(m,open('/tmp/master.pkl','wb'))
for ch in [1,3,4,5,6]:
    el=[i for i in m if i['ch']==ch]
    c=collections.Counter(i['dtier'] for i in el)
    ready=[i for i in el if (i['tier'] in 'AB' or i.get('salvage')=='Yes')]
    rc=collections.Counter(i['dtier'] for i in ready)
    print(f"Ch{ch}: bank r/c {c['routine']:>3}/{c['challenging']:<3}  |  ready-pool r/c {rc['routine']:>3}/{rc['challenging']:<3}"
          f"  (unused ready r/c {len([i for i in ready if i['dtier']=='routine' and not i['used_in']]):>2}/"
          f"{len([i for i in ready if i['dtier']=='challenging' and not i['used_in']]):<2})")
