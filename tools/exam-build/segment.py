import re, pickle, collections
OPTL=re.compile(r'^([A-Z])\.\s')
m=pickle.load(open('/tmp/master.pkl','rb'))

def answers(c):
    """every separately-marked answer in the item"""
    txt='\n'.join(c['ansl'])
    drops=re.findall(r'\((\d+)\)\s*([^\n(]*)', txt)
    letters=[l for l in c['ansl'] if OPTL.match(l.strip())]
    # bare numeric / short scalar answers (not part of a dropdown or lettered line)
    nums=[l.strip() for l in c['ansl']
          if re.fullmatch(r'[-−$]?\s*[\d,]+(\.\d+)?%?', l.strip())]
    return drops, letters, nums

for i in m:
    c=i['clean']
    d,l,n=answers(c)
    c['ndrop2']=len({k for k,_ in d}); c['nlet']=len(l); c['nnum']=len(n)
    c['tasks']=c['ndrop2']+max(c['nruns'],c['nlet'])+c['nnum']
    if c['tasks']==0: c['tasks']=1
pickle.dump(m,open('/tmp/master.pkl','wb'))

sel=[i for i in m if i.get('sel')]
print('SELECTED — corrected answer-task count per item:',
      dict(sorted(collections.Counter(i['clean']['tasks'] for i in sel).items())))
multi=[i for i in sel if i['clean']['tasks']>1]
print('multi-task selected items:',len(multi),'(was 25 before counting numeric answers)')
print('  by chapter:',dict(sorted(collections.Counter(i['ch'] for i in multi).items())))
print('  by type   :',dict(collections.Counter(i['qtype2'] for i in multi)))
print('  total answer-tasks across them:',sum(i['clean']['tasks'] for i in multi))
print('  extra questions if fully split:',sum(i['clean']['tasks']-1 for i in multi))
print()
print('  time carried by multi-task items: %d of %d min across the 120'
      % (sum(i['time_s'] for i in multi)/60, sum(i['time_s'] for i in sel)/60))
