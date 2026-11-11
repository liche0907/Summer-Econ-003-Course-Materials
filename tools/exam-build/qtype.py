import pickle, re, collections
m=pickle.load(open('/tmp/master.pkl','rb'))
FIGWORD=re.compile(r'\b(graph|figure|diagram|curve shown|shown in the|the given|accompanying|shown above|drawing tool)\b',re.I)
GRAPHREASON=re.compile(r'\b(shift|shifts|shifted|slope|slopes|curve|curves|leftward|rightward|upward|downward|move along|movement along|intersect)\b',re.I)
NUMERIC=re.compile(r'(\$\s?\d|\d+\s*(percent|%)|calculate|compute|elasticity of|how much|what is the (total|marginal|average|value|price|quantity|cost|profit|surplus)|round your response|enter your response)',re.I)
DEFN=re.compile(r'(all of the following.{0,40}except|which of the following is not|is defined as|refers to|best describes|is called|are known as|the term for|definition of|is an example of|which of the following (is|are) (a|an|the) |which of the following (is|are) (the )?(definition|an example|a characteristic))',re.I)
def SHORTOPTS(i):
    o=[l for l in i['opts'].split(chr(10)) if l.strip()]
    return len(o)>=3 and all(len(l.split())<=6 for l in o)

for i in m:
    t=i['stem']+' '+i['opts']
    fig = i['figure']=='Yes' or bool(re.search(r'drawing\s*tool',i['raw'],re.I)) or (i['figure']=='Likely' and FIGWORD.search(t))
    if fig:                          q='G-fig'      # needs an image to answer
    elif GRAPHREASON.search(t):      q='G-reason'   # curve/shift reasoning, no image needed
    elif i['parts']==1 and (DEFN.search(i['stem']) or SHORTOPTS(i)):
                                     q='Defn'       # recall / definition lookup
    elif NUMERIC.search(t):          q='Quant'
    else:                            q='Concept'
    i['qtype2']=q
pickle.dump(m,open('/tmp/master.pkl','wb'))

print('WHOLE BANK by type:',dict(collections.Counter(i['qtype2'] for i in m)))
print()
TY=['G-fig','G-reason','Quant','Concept','Defn']
print('READY SUPPLY (Tier A+B, plus Salvage) — unused / used')
hdr=f"{'Ch':>4} " + ' '.join(f'{t:>12}' for t in TY)
print(hdr); print('-'*len(hdr))
for ch in [1,3,4,5,6]:
    el=[i for i in m if i['ch']==ch and (i['tier'] in 'AB' or i.get('salvage')=='Yes')]
    row=f'{ch:>4} '
    for t in TY:
        s=[i for i in el if i['qtype2']==t]
        row+=f"{len([i for i in s if not i['used_in']]):>5}/{len([i for i in s if i['used_in']]):<6}"
    print(row)
print()
print('RESERVE in Tier C+D (redraw / rewrite candidates), unused:')
hdr2=f"{'Ch':>4} " + ' '.join(f'{t:>10}' for t in TY)
print(hdr2)
for ch in [1,3,4,5,6]:
    res=[i for i in m if i['ch']==ch and i['tier'] in 'CD' and i.get('salvage')!='Yes' and not i['used_in']]
    print(f'{ch:>4} '+' '.join(f"{len([i for i in res if i['qtype2']==t]):>10}" for t in TY))
