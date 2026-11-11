import os,glob,shutil,re
SRC='QTI_IB'; OUT='QTI_ONE'
shutil.rmtree(OUT,ignore_errors=True)
os.makedirs(OUT+'/web_resources/econ003_final',exist_ok=True)
banks=sorted(os.path.basename(d) for d in glob.glob(SRC+'/*'))
figs=set()
for b in banks:
    os.makedirs(OUT+'/'+b,exist_ok=True)
    shutil.copy(SRC+'/'+b+'/'+b+'/'+b+'.xml', OUT+'/'+b+'/'+b+'.xml')
    shutil.copy(SRC+'/'+b+'/'+b+'/assessment_meta.xml', OUT+'/'+b+'/assessment_meta.xml')
    for p in glob.glob(SRC+'/'+b+'/web_resources/econ003_final/*'):
        shutil.copy(p, OUT+'/web_resources/econ003_final/'+os.path.basename(p)); figs.add(os.path.basename(p))
figs=sorted(figs)
m=['<?xml version="1.0" encoding="UTF-8"?>',
'<manifest identifier="econ003_final_itembanks" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">',
'  <metadata><schema>IMS Content</schema><schemaversion>1.1.3</schemaversion></metadata>',
'  <organizations/>','  <resources>']
for b in banks:
    m+=['    <resource identifier="r_%s" type="imsqti_xmlv1p2" href="%s/%s.xml">'%(b,b,b),
        '      <file href="%s/%s.xml"/>'%(b,b),
        '      <dependency identifierref="meta_%s"/>'%b,
        '    </resource>',
        '    <resource identifier="meta_%s" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="%s/assessment_meta.xml">'%(b,b),
        '      <file href="%s/assessment_meta.xml"/>'%b,
        '    </resource>']
m.append('    <resource identifier="web_res" type="webcontent" href="web_resources/econ003_final/">')
for f in figs: m.append('      <file href="web_resources/econ003_final/%s"/>'%f)
m+=['    </resource>','  </resources>','</manifest>','']
open(OUT+'/imsmanifest.xml','w').write('\n'.join(m))
print('merged',len(banks),'banks,',len(figs),'figures')
