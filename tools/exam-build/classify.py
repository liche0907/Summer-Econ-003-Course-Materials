import pickle, re, collections
m=pickle.load(open('/tmp/master.pkl','rb'))
DRAW=re.compile(r'drawing\s*tool|Use the (Line|Point|Multipoint|Curved)',re.I)
TABLE=re.compile(r'Create a table|complete the (following )?table|fill in the table',re.I)
for i in m:
    t=i['raw']
    i['draw']=bool(DRAW.search(t)); i['table']=bool(TABLE.search(t))
    i['numeric']= (i['nopt']==0 and i['fmt']=='mc')
    p,n,c=i['parts'],i['nopt'],i['cata']
    if i['draw']:                       tier,why='D','drawing-tool item — needs a static figure + new stem'
    elif p>=4:                          tier,why='D',f'{p} parts — scaffolding is the item'
    elif i['table']:                    tier,why='D','table-construction item'
    elif p==1 and n>=4 and not c:       tier,why='A','drop-in'
    elif p==1 and c:                    tier,why='C','check-all-that-apply — rewrite as single answer'
    elif p==1 and n in (2,3):           tier,why='B',f'only {n} options — add distractors'
    elif p==1 and i['numeric']:         tier,why='B','numeric entry — write 4 numeric distractors'
    elif p==1 and n==0:                 tier,why='B','single dropdown — render choices as options'
    elif p in (2,3) and i['fmt'] in ('cloze','cloze+mc'):
                                        tier,why='C',f'{p}-part cloze — collapse to combination options'
    elif p in (2,3):                    tier,why='C',f'{p} parts — split or collapse'
    else:                               tier,why='C','review'
    i['tier'],i['why']=tier,why
    i['needs_fig']= i['figure']=='Yes'

# salvage: a drawing-tool item that also carries a self-contained 4+ option MC
for i in m:
    i['salvage']=''
    if i['tier']=='D' and 'drawing-tool' in i['why']:
        opts=re.findall(r'^\s{4,}([A-Z])\.\s', i['raw'], re.M)
        runs=[];cur=[]
        for L in opts:
            if L=='A':
                if cur: runs.append(cur)
                cur=['A']
            elif cur and ord(L)==ord(cur[-1])+1: cur.append(L)
        if cur: runs.append(cur)
        if any(len(r)>=4 for r in runs):
            i['salvage']='Yes'
            i['why']='drawing-tool item, BUT carries a usable 4-option MC — keep the rendered graph, delete the drawing task, keep the MC'
pickle.dump(m,open('/tmp/master.pkl','wb'))

print('TIER TOTALS:',dict(sorted(collections.Counter(i['tier'] for i in m).items())))
print()
print('A = drop-in | B = mechanical revision | C = judgment revision | D = skip')
print()
hdr=f"{'Ch':>4} | {'A':>4}{'B':>4}{'C':>4}{'D':>4} | {'A+B unused':>11}{'A+B used':>9} | {'need P':>7}{'need R':>7}"
print(hdr); print('-'*len(hdr))
needP={1:13,3:16,4:20,5:18,6:15}; needR={1:6,3:8,4:9,5:8,6:7}
for ch in [1,3,4,5,6]:
    s=[i for i in m if i['ch']==ch]; c=collections.Counter(i['tier'] for i in s)
    ab=[i for i in s if i['tier'] in 'AB']
    un=len([i for i in ab if not i['used_in']]); us=len([i for i in ab if i['used_in']])
    print(f"{ch:>4} | {c['A']:>4}{c['B']:>4}{c['C']:>4}{c['D']:>4} | {un:>11}{us:>9} | {needP[ch]:>7}{needR[ch]:>7}")
ab=[i for i in m if i['tier'] in 'AB']
print(f"\nTOTAL A+B: {len(ab)}   unused {len([i for i in ab if not i['used_in']])} (need 82)   used {len([i for i in ab if i['used_in']])} (need 38)")
print('\nB breakdown:',dict(collections.Counter(i['why'] for i in m if i['tier']=='B')))
print('\nC breakdown:',dict(collections.Counter(i['why'] for i in m if i['tier']=='C')))
print('\nD breakdown:',dict(collections.Counter(i['why'] for i in m if i['tier']=='D')))
print('\nneeds figure asset (Yes):',sum(i['needs_fig'] for i in m),' of which tier A+B:',sum(1 for i in ab if i['needs_fig']))
