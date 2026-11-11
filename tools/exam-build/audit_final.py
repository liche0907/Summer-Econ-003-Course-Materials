import subprocess, re, pickle, collections, json, openpyxl
SRC='/mnt/user-data/uploads/ECON003_26S/Assignments/QB'
BANKS={'QB7&8':'QB7&8','QB9&10':'QB9&10','QB12':'QB12'}

# ---- xlsx metadata, in Order sequence (matches PDF order 1:1, verified by count) ----
meta={}
for b in BANKS:
    wb=openpyxl.load_workbook(f'{SRC}/{b}.xlsx'); ws=wb['Sheet1']
    rows=[r for r in ws.iter_rows(min_row=2,values_only=True) if r[0] is not None]
    meta[b]=[{'order':int(r[0]),'pid':r[1],'sectitle':r[2],'time':r[5],'diff':r[7]} for r in rows]

its=pickle.load(open('/tmp/items_final.pkl','rb'))
bybank=collections.defaultdict(list)
for x in its: bybank[x['bank']].append(x)

# ---- section titles -> chapter + section number ----
SEC={
 'Perfect Competition and Efficiency':(7,'7.1'),
 'Extending the Reach of the Invisible Hand: From the Individual to the Firm':(7,'7.2'),
 'Extending the Reach of the Invisible Hand: Allocation of Resources Across Industries':(7,'7.3'),
 'Prices Guide the Invisible Hand':(7,'7.4'),
 'Equity and Efficiency':(7,'7.5'),
 'The Production Possibilities Curve':(8,'8.1'),
 'The Basis for Trade: Comparative Advantage':(8,'8.2'),
 'Trade Between States':(8,'8.3'),
 'Trade Between Countries':(8,'8.4'),
 'Arguments Against Free Trade':(8,'8.5'),
 'Externalities':(9,'9.1'),
 'Private Solutions to Externalities':(9,'9.2'),
 'Government Solutions to Externalities':(9,'9.3'),
 'Public Goods':(9,'9.4'),
 'Common Pool Resource Goods':(9,'9.5'),
 'Taxation and Government Spending in the United States':(10,'10.1'),
 'Regulation':(10,'10.2'),
 'Government Failures':(10,'10.3'),
 'Introducing a New Market Structure':(12,'12.1'),
 'Sources of Market Power':(12,'12.2'),
 "The Monopolist's Problem":(12,'12.3'),
 'Choosing the Optimal Quantity and Price':(12,'12.4'),
 'The "Broken" Invisible Hand: The Cost of Monopoly':(12,'12.5'),
}
def secof(t):
    for k,v in SEC.items():
        if t.strip()==k.strip(): return v
    return (0,'?')

OPTRE=re.compile(r'^\s*([A-Z])\.\s(.*)$',re.M)
rows=[]
for b in BANKS:
    m=meta[b]; p=bybank[b]
    assert len(m)==len(p), (b,len(m),len(p))
    for mm,pp in zip(m,p):
        raw=pp['raw']
        ch,sec=secof(mm['sectitle'])
        opts=OPTRE.findall(raw)
        nopt=len(opts)
        # clipped option: line has no terminal punctuation and is long
        clipped=[l for _,l in opts if len(l)>=105 and not re.search(r'[.?!)"​]\s*$',l.strip())]
        # cloze / dropdown item: "(1)" style blanks
        blanks=sorted(set(re.findall(r'\((\d)\)',raw)))
        cloze = len(blanks)>=1 and nopt==0
        multiblank = len(blanks)>=2
        cata = bool(re.search(r'[Cc]heck all that apply|[Ss]elect all',raw))
        draw = bool(re.search(r'drawing tool|Draw (a|the)|line tool|point tool|Use the (line|point|multipoint)',raw,re.I))
        rows.append(dict(bank=b,order=mm['order'],pid=mm['pid'],sectitle=mm['sectitle'],ch=ch,sec=sec,
            pdiff=mm['diff'],time=mm['time'],pages=pp['pages'],fig=pp['figure'],nopt=nopt,
            nclip=len(clipped),cloze=cloze,nblank=len(blanks),cata=cata,draw=draw,
            raw=raw))
json.dump([{k:v for k,v in r.items()} for r in rows], open('/tmp/audit_final.json','w'))
print('rows',len(rows))
