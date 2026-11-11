import pickle, json, sys
sys.path.insert(0,'.')
from clean import clean_text as cl
m=pickle.load(open('/tmp/master.pkl','rb'))
sel=[i for i in m if i.get('sel')]
sel.sort(key=lambda i:(i['ch'],{'P':0,'R':1}[i['sel']],i['uid']))
out=[]
for i in sel:
    conv='S' if i.get('salvage')=='Yes' else i['tier']
    w=cl(i['why'])
    act={'A':'Use as written.','S':'Delete the drawing instruction, keep the MC, supply the figure.',
         'D':'Redraw the figure in house style; convert the drawing task into an MC on the result.'}.get(conv, w[:1].upper()+w[1:]+'.')
    if i['sel']=='R': act='Swap all numbers and recompute the key; expand to 5 options. '+act
    if i['qtype2']=='G-fig': act+=f" FIGURE: render {i['bank']} p{i['pages'][0]}-{i['pages'][-1]} and redraw."
    if i.get('trunc'): act+=' VERIFY wording against the render.'
    out.append(dict(uid=i['uid'],ch=i['ch'],sec=i['sec'],bucket=i['sel'],qtype=i['qtype2'],
        dtier=i['dtier'],diff=i['difficulty'],conv=conv,pid=cl(i['pid']),nopt=i['nopt'],
        fig=(i['qtype2']=='G-fig'),src=f"{i['bank']} p{i['pages'][0]}-{i['pages'][-1]}",
        stem=[l.strip() for l in cl(i['stem']).split('\n') if l.strip()],
        opts=[l.strip() for l in cl(i['opts']).split('\n') if l.strip()],
        ans=[l.strip() for l in cl(i['ans']).split('\n') if l.strip()], act=act))
json.dump(out, open('/tmp/sel.json','w'))
print('exported',len(out)); print('check:',out[1]['stem'][0])
