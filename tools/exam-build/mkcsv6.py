import json,csv
P=json.load(open('/tmp/POOL2.json'))
SECS={'7':['7.1','7.3','7.4','7.5'],'8':['8.1','8.2','8.3','8.4','8.5'],
      '9':['9.1','9.2','9.3','9.4','9.5'],'10':['10.1','10.2','10.3'],
      '12':['12.1','12.2','12.3','12.4','12.5','12.7']}
order=[]
for ch in ['7','8','9','10','12']:
    for sec in SECS[ch]:
        g=[x for x in P if x['sec']==sec]
        for tier in ['routine','challenging']:
            order+=[x for x in g if x['tier']==tier]
assert len(order)==len(P),(len(order),len(P))
with open('ECON003_Final_PostMidterm_Pool_v13.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['n','label','sec','ch','tier','source','status','printed_options','n_options',
                'figure','has_table','seconds','key','stem'])
    for i,x in enumerate(order,1):
        stem=' '.join(x.get('stem') or [])
        w.writerow([i,x['label'],x['sec'],x['sec'].split('.')[0],x['tier'],x['src'],
                    ('ORIGINAL' if x['src']=='original' else x.get('cls','rebuilt')),
                    x.get('printed_n',0),len(x['options']),x.get('fig') or '',
                    1 if (x.get('tables') and any(t and t.get('header') for t in x['tables'])) else 0,
                    x.get('_t',''),x['key'],stem[:300]])
print('wrote csv',len(order))
