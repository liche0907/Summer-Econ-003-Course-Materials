import os,re,glob,xml.etree.ElementTree as ET
from collections import Counter
OUT='QTI_FINAL'
NS='{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}'
man=open(OUT+'/imsmanifest.xml').read()
mroot=ET.fromstring(man)
MNS='{http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1}'
res=mroot.findall('.//'+MNS+'resource')
print('resources:',len(res),'types:',Counter(r.get('type') for r in res))
listed=set(f.get('href') for f in mroot.findall('.//'+MNS+'file'))
missing_on_disk=[h for h in listed if not os.path.exists(os.path.join(OUT,h))]
print('manifest files:',len(listed),'missing on disk:',missing_on_disk)
ondisk=set()
for dp,dn,fn in os.walk(OUT):
    for f in fn:
        p=os.path.relpath(os.path.join(dp,f),OUT).replace('\\','/')
        if p!='imsmanifest.xml': ondisk.add(p)
print('files on disk not in manifest:',sorted(ondisk-listed))

total=0; problems=[]; idents=Counter(); imgrefs=Counter()
banks=sorted(glob.glob(OUT+'/*/*.xml'))
print('bank xml files:',len(banks))
for b in banks:
    root=ET.parse(b).getroot()
    ob=root.find(NS+'objectbank')
    assert ob is not None, b+' has no objectbank'
    title=ob.find('.//'+NS+'fieldentry')
    items=ob.findall(NS+'item')
    total+=len(items)
    print(' %-22s %-38s %3d items'%(os.path.basename(b)[:-4], title.text, len(items)))
    for it in items:
        idents[it.get('ident')]+=1
        labs=[r.get('ident') for r in it.findall('.//'+NS+'response_label')]
        if len(labs)<4: problems.append((b,it.get('ident'),'only %d options'%len(labs)))
        if len(set(labs))!=len(labs): problems.append((b,it.get('ident'),'dup option idents'))
        # correct answer
        keys=[]
        for rc in it.findall('.//'+NS+'respcondition'):
            sv=rc.find('.//'+NS+'setvar')
            if sv is not None and float(sv.text)>0:
                ve=rc.find('.//'+NS+'varequal')
                keys.append(ve.text)
        if len(keys)!=1: problems.append((b,it.get('ident'),'%d scoring conditions'%len(keys)))
        elif keys[0]!=labs[0]: problems.append((b,it.get('ident'),'key %s is not first option %s'%(keys[0],labs[0])))
        for m in re.findall(r'\$IMS-CC-FILEBASE\$/([^"\'\s>]+)', ET.tostring(it,encoding='unicode')):
            imgrefs[m.replace('%20',' ')]+=1
print('TOTAL ITEMS:',total)
dup=[k for k,v in idents.items() if v>1]
print('duplicate item idents across package:',len(dup), dup[:5])
print('distinct image refs:',len(imgrefs),'total refs:',sum(imgrefs.values()))
bad=[r for r in imgrefs if not os.path.exists(OUT+'/web_resources/'+r.split('/',1)[1] if r.startswith('econ003_final/') else OUT+'/web_resources/'+r)]
for r in sorted(imgrefs):
    p=OUT+'/web_resources/'+r
    if not os.path.exists(p): problems.append(('IMG',r,'missing file'))
    elif 'web_resources/'+r not in listed: problems.append(('IMG',r,'not in manifest'))
unused=set(os.path.relpath(p,OUT+'/web_resources').replace('\\','/') for p in glob.glob(OUT+'/web_resources/econ003_final/*'))-set(imgrefs)
print('stored but unreferenced images:',sorted(unused))
print('PROBLEMS:',len(problems))
for p in problems[:40]: print('  ',p)
