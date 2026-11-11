import re,os,glob,shutil
DRAW={'m_ch1_routine':2,'m_ch3_routine':3,'m_ch3_challenging':1,'m_ch4_routine':4,'m_ch4_challenging':2,
'm_ch5_routine':4,'m_ch5_challenging':2,'m_ch6_routine':4,'m_ch6_challenging':2,
'p_ch7_routine':5,'p_ch7_challenging':2,'p_ch8_routine':6,'p_ch8_challenging':2,
'p_ch9_routine':5,'p_ch9_challenging':3,'p_ch10_routine':3,'p_ch10_challenging':2,
'p_ch12_routine':5,'p_ch12_challenging':3}
ORDER=['m_ch1_routine','m_ch3_routine','m_ch3_challenging','m_ch4_routine','m_ch4_challenging',
'm_ch5_routine','m_ch5_challenging','m_ch6_routine','m_ch6_challenging',
'p_ch7_routine','p_ch7_challenging','p_ch8_routine','p_ch8_challenging',
'p_ch9_routine','p_ch9_challenging','p_ch10_routine','p_ch10_challenging',
'p_ch12_routine','p_ch12_challenging']
OUT='QTI_QUIZ'; QID='econ003_final_quiz'
shutil.rmtree(OUT,ignore_errors=True)
os.makedirs(OUT+'/'+QID,exist_ok=True); os.makedirs(OUT+'/web_resources/econ003_final',exist_ok=True)
figs=set(); secs=[]; total=0
for b in ORDER:
    src='QTI_IB/%s/%s/%s.xml'%(b,b,b)
    s=open(src).read()
    title=re.search(r'<assessment ident="[^"]*" title="([^"]*)"',s).group(1)
    items=re.findall(r'( {4}<item ident=.*?</item>\n)',s,re.S)
    assert items, b
    total+=DRAW[b]
    for p in glob.glob('QTI_IB/%s/web_resources/econ003_final/*'%b):
        shutil.copy(p,OUT+'/web_resources/econ003_final/'+os.path.basename(p)); figs.add(os.path.basename(p))
    x ='    <section ident="g_%s" title="%s">\n'%(b,title)
    x+='      <selection_ordering>\n        <selection>\n'
    x+='          <selection_number>%d</selection_number>\n'%DRAW[b]
    x+='          <selection_extension><points_per_item>1.0</points_per_item></selection_extension>\n'
    x+='        </selection>\n      </selection_ordering>\n'
    x+=''.join(items)
    x+='    </section>\n'
    secs.append((b,title,len(items),DRAW[b],x))
q ='<?xml version="1.0" encoding="UTF-8"?>\n<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/profile/cc/ccv1p2/ccv1p2_qtiasiv1p2p1_v1p0.xsd">\n'
q+='  <assessment ident="%s" title="ECON 003 Final Exam">\n    <qtimetadata>\n'%QID
q+='      <qtimetadatafield><fieldlabel>cc_maxattempts</fieldlabel><fieldentry>1</fieldentry></qtimetadatafield>\n'
q+='    </qtimetadata>\n    <section ident="root_section">\n'
q+=''.join(s[4] for s in secs)
q+='    </section>\n  </assessment>\n</questestinterop>\n'
open('%s/%s/%s.xml'%(OUT,QID,QID),'w').write(q)
meta='''<?xml version="1.0" encoding="UTF-8"?>
<quiz identifier="%s" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <title>ECON 003 Final Exam</title>
  <quiz_type>assignment</quiz_type>
  <points_possible>%.1f</points_possible>
  <shuffle_answers>true</shuffle_answers>
  <time_limit>180</time_limit>
  <allowed_attempts>1</allowed_attempts>
  <one_question_at_a_time>true</one_question_at_a_time>
  <cant_go_back>false</cant_go_back>
  <scoring_policy>keep_highest</scoring_policy>
</quiz>
'''%(QID,float(total))
open('%s/%s/assessment_meta.xml'%(OUT,QID),'w').write(meta)
m=['<?xml version="1.0" encoding="UTF-8"?>',
'<manifest identifier="econ003_final_quiz_pkg" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">',
'  <metadata><schema>IMS Content</schema><schemaversion>1.1.3</schemaversion></metadata>','  <organizations/>','  <resources>',
'    <resource identifier="r_%s" type="imsqti_xmlv1p2" href="%s/%s.xml">'%(QID,QID,QID),
'      <file href="%s/%s.xml"/>'%(QID,QID),
'      <dependency identifierref="meta_%s"/>'%QID,'    </resource>',
'    <resource identifier="meta_%s" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="%s/assessment_meta.xml">'%(QID,QID),
'      <file href="%s/assessment_meta.xml"/>'%QID,'    </resource>',
'    <resource identifier="web_res" type="webcontent" href="web_resources/econ003_final/">']
for f in sorted(figs): m.append('      <file href="web_resources/econ003_final/%s"/>'%f)
m+=['    </resource>','  </resources>','</manifest>','']
open(OUT+'/imsmanifest.xml','w').write('\n'.join(m))
for b,t,n,d,_ in secs: print('  %-22s %-34s pool %3d  draw %2d'%(b,t,n,d))
print('\n1 quiz · 19 groups · %d drawn from %d items · %d figures'%(total,sum(s[2] for s in secs),len(figs)))
