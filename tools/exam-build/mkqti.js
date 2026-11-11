/* Build a QTI 1.2 package Canvas can import: ten object banks, images included. */
const fs=require('fs'), path=require('path');
const B2=require('./batch2.js');
const REV=JSON.parse(fs.readFileSync('./rev.json','utf8'));
const SEL=JSON.parse(fs.readFileSync('./seltier.json','utf8'));
const TIER=JSON.parse(fs.readFileSync('./tieroverride.json','utf8'));
const ORIG=require('./originals.js');
const CUT={115:1,87:1,67:1,56:1,106:1,32:1,28:1,71:1,19:1,24:1};  // 19: quadratic MB; 24: "people always optimize" - both removed by hand Aug 14

const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
                      .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
const FILEBASE='$IMS-CC-FILEBASE$/econ003_midterm';

/* ---------- collect (same rules as the docx builders) ---------- */
const b2n={}; B2.forEach(q=>b2n[Number(q.id.slice(1))]=q);
const items=[];
B2.forEach(q=>{const n=Number(q.id.slice(1)); if(CUT[n]) return;
  q.items.forEach(it=>{ if(n===88&&it.lab==='88b') return; items.push({
    lab:it.lab, uid:q.uid, sec:it.sec||q.sec,
    tier:TIER[it.lab]||it.tier||q.tier||(SEL[q.uid]||{}).tier,
    lead:it.lead||[], ask:it.ask||'', table:it.table||null, fig:it.fig||q.fig||null,
    opts:it.opts.map(o=>[o[0],!!o[1]])});});
});
REV.forEach(x=>{const n=x.n; if(CUT[n]||b2n[n]) return;
  let groups=(x.subs||[]).concat(x.keep||[]);
  if(!groups.length){ if(x.status==='DROPPED') return;
    const p0=(x.parts&&x.parts[0])||{lead:[],opts:[]};
    groups=[{letter:'',lead:p0.lead||[],opts:p0.opts||[],ans:p0.ans}]; }
  groups.forEach(s=>{
    const lead=(s.lead||[]).slice(); const askLine=lead.length>1?lead.pop():'';
    const norm=z=>String(z).replace(/^[A-H]\.\s*/,'').replace(/\s+/g,' ')
      .replace(/[‘’]/g,"'").replace(/[“”]/g,'"').replace(/[−–—]/g,'-')
      .replace(/[.\s]+$/,'').trim().toLowerCase();
    const A=norm(String(s.ans||''));
    let opts=(s.opts||[]).map(o=>[o.replace(/^[A-H]\.\s*/,''), A&&norm(o)===A]);
    if(A && !opts.some(o=>o[1])){ let best=-1,len=-1;
      opts.forEach((o,i)=>{const q2=norm(o[0]);
        if(q2&&(A.startsWith(q2)||q2.startsWith(A))&&q2.length>len){len=q2.length;best=i;}});
      if(best>=0) opts[best][1]=true; }
    items.push({lab:String(n)+(s.letter||''), uid:x.uid, sec:x.sec,
      tier:TIER[String(n)+(s.letter||'')]||(SEL[x.uid]||{}).tier,
      lead, ask:askLine, table:null, fig:null, opts:opts.map(o=>[o[0],!!o[1]])});
  });
});
ORIG.filter(x=>x.state==='ok').forEach(x=>items.push({
  lab:x.id, uid:x.uid, sec:x.sec, tier:x.tier,
  lead:x.lead||[], ask:x.ask||'', table:x.table||null, fig:x.fig||null,
  opts:x.opts.map(o=>[o[0],!!o[1]])}));

/* key first, matching the by-bank document */
items.forEach(it=>{ const k=it.opts.filter(o=>o[1]), r=it.opts.filter(o=>!o[1]); it.opts=k.concat(r); });

/* ---------- banks ---------- */
const CH=['1','3','4','5','6'];
const banks=[];
for(const ch of CH) for(const tier of ['routine','challenging']){
  banks.push({ch, tier,
    id:'ch'+ch+'_'+tier,
    title:'ECON003 Midterm — Ch'+ch+' '+tier[0].toUpperCase()+tier.slice(1),
    list:items.filter(i=>i.sec.split('.')[0]===ch && i.tier===tier)
              .sort((a,b)=>a.sec.localeCompare(b.sec)||a.lab.localeCompare(b.lab))});
}

/* ---------- assertions ---------- */
{
  const bad=[];
  items.forEach(it=>{
    if(it.opts.filter(o=>o[1]).length!==1) bad.push(it.lab+': key count');
    if(it.opts.length<4) bad.push(it.lab+': <4 options');
    if(!it.opts[0][1]) bad.push(it.lab+': key not first');
    if(it.fig && !fs.existsSync(it.fig)) bad.push(it.lab+': missing '+it.fig);
    if(!it.tier) bad.push(it.lab+': no tier');
  });
  const placed=banks.reduce((a,b)=>a+b.list.length,0);
  if(placed!==items.length) bad.push('placed '+placed+' of '+items.length);
  if(bad.length){ console.error('BUILD REFUSED:'); bad.forEach(x=>console.error('  '+x)); process.exit(1); }
}

/* ---------- html body for one item ---------- */
function bodyHtml(it){
  let h='';
  it.lead.forEach(l=>h+='<p>'+esc(l)+'</p>');
  if(it.table){
    h+='<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;">';
    it.table.forEach((row,ri)=>{ h+='<tr>';
      row.forEach(c=>h+= ri===0 ? '<th>'+esc(c)+'</th>' : '<td>'+esc(c)+'</td>');
      h+='</tr>'; });
    h+='</table>';
  }
  if(it.fig) h+='<p><img src="'+FILEBASE+'/'+path.basename(it.fig)+'" alt="figure"></p>';
  if(it.ask) h+='<p><strong>'+esc(it.ask)+'</strong></p>';
  return h;
}

function itemXml(it,i){
  const ident='i_'+it.lab.replace(/[^A-Za-z0-9]/g,'_');
  let x='';
  x+='    <item ident="'+ident+'" title="'+esc(it.uid+' \u00b7 '+it.lab)+'">\n';  // lab included: multi-part splits shared one title on the midterm, making item analysis untraceable
  x+='      <itemmetadata><qtimetadata>\n';
  x+='        <qtimetadatafield><fieldlabel>question_type</fieldlabel><fieldentry>multiple_choice_question</fieldentry></qtimetadatafield>\n';
  x+='        <qtimetadatafield><fieldlabel>points_possible</fieldlabel><fieldentry>1</fieldentry></qtimetadatafield>\n';
  x+='        <qtimetadatafield><fieldlabel>original_answer_ids</fieldlabel><fieldentry>'+it.opts.map((o,j)=>ident+'_a'+j).join(',')+'</fieldentry></qtimetadatafield>\n';
  x+='      </qtimetadata></itemmetadata>\n';
  x+='      <presentation>\n';
  x+='        <material><mattext texttype="text/html">'+esc(bodyHtml(it))+'</mattext></material>\n';
  x+='        <response_lid ident="response1" rcardinality="Single">\n';
  x+='          <render_choice>\n';
  it.opts.forEach((o,j)=>{
    x+='            <response_label ident="'+ident+'_a'+j+'">';
    x+='<material><mattext texttype="text/html">'+esc('<p>'+esc(o[0])+'</p>')+'</mattext></material>';
    x+='</response_label>\n';
  });
  x+='          </render_choice>\n';
  x+='        </response_lid>\n';
  x+='      </presentation>\n';
  const keyIdx=it.opts.findIndex(o=>o[1]);
  x+='      <resprocessing>\n';
  x+='        <outcomes><decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/></outcomes>\n';
  x+='        <respcondition continue="No">\n';
  x+='          <conditionvar><varequal respident="response1">'+ident+'_a'+keyIdx+'</varequal></conditionvar>\n';
  x+='          <setvar action="Set" varname="SCORE">100</setvar>\n';
  x+='        </respcondition>\n';
  x+='      </resprocessing>\n';
  x+='    </item>\n';
  return x;
}

function assessmentXml(bk){
  let x='<?xml version="1.0" encoding="UTF-8"?>\n';
  x+='<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" '
   + 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
   + 'xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 '
   + 'http://www.imsglobal.org/profile/cc/ccv1p2/ccv1p2_qtiasiv1p2p1_v1p0.xsd">\n';
  x+='  <assessment ident="a_'+bk.id+'" title="'+esc(bk.title)+'">\n';
  x+='    <qtimetadata>\n';
  x+='      <qtimetadatafield><fieldlabel>cc_maxattempts</fieldlabel><fieldentry>1</fieldentry></qtimetadatafield>\n';
  x+='    </qtimetadata>\n';
  x+='    <section ident="root_section">\n';
  bk.list.forEach((it,i)=>{ x+=itemXml(it,i); });
  x+='    </section>\n';
  x+='  </assessment>\n</questestinterop>\n';
  return x;
}

function metaXml(bk){
  let x='<?xml version="1.0" encoding="UTF-8"?>\n';
  x+='<quiz identifier="a_'+bk.id+'" xmlns="http://canvas.instructure.com/xsd/cccv1p0" '
   + 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n';
  x+='  <title>'+esc(bk.title)+'</title>\n';
  x+='  <quiz_type>assignment</quiz_type>\n';
  x+='  <points_possible>'+bk.list.length+'.0</points_possible>\n';
  x+='  <shuffle_answers>true</shuffle_answers>\n';
  x+='  <allowed_attempts>1</allowed_attempts>\n';
  x+='  <scoring_policy>keep_highest</scoring_policy>\n';
  x+='</quiz>\n';
  return x;
}

function bankXml(bk){
  let x='<?xml version="1.0" encoding="UTF-8"?>\n';
  x+='<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" '
   + 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
   + 'xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 '
   + 'http://www.imsglobal.org/profile/cc/ccv1p2/ccv1p2_qtiasiv1p2p1_v1p0.xsd">\n';
  x+='  <objectbank ident="ob_'+bk.id+'">\n';
  x+='    <qtimetadata>\n';
  x+='      <qtimetadatafield><fieldlabel>bank_title</fieldlabel><fieldentry>'+esc(bk.title)+'</fieldentry></qtimetadatafield>\n';
  x+='    </qtimetadata>\n';
  bk.list.forEach((it,i)=>{ x+=itemXml(it,i); });
  x+='  </objectbank>\n';
  x+='</questestinterop>\n';
  return x;
}

/* ---------- write the package ---------- */
const OUT='qti_build';
fs.rmSync(OUT,{recursive:true,force:true});
fs.mkdirSync(OUT+'/web_resources/econ003_midterm',{recursive:true});

const figs=[...new Set(items.filter(i=>i.fig).map(i=>i.fig))];
figs.forEach(f=>fs.copyFileSync(f, OUT+'/web_resources/econ003_midterm/'+path.basename(f)));

banks.forEach(bk=>{
  fs.mkdirSync(OUT+'/'+bk.id,{recursive:true});
  fs.writeFileSync(OUT+'/'+bk.id+'/'+bk.id+'.xml', bankXml(bk));
});

let man='<?xml version="1.0" encoding="UTF-8"?>\n';
man+='<manifest identifier="econ003_midterm_qti" '
   + 'xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" '
   + 'xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" '
   + 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n';
man+='  <metadata><schema>IMS Content</schema><schemaversion>1.1.3</schemaversion></metadata>\n';
man+='  <organizations/>\n  <resources>\n';
banks.forEach(bk=>{
  man+='    <resource identifier="res_'+bk.id+'" type="imsqti_xmlv1p2" href="'+bk.id+'/'+bk.id+'.xml">\n';
  man+='      <file href="'+bk.id+'/'+bk.id+'.xml"/>\n    </resource>\n';
});
man+='    <resource identifier="res_webres" type="webcontent" href="web_resources/econ003_midterm/">\n';
figs.forEach(f=>{ man+='      <file href="web_resources/econ003_midterm/'+path.basename(f)+'"/>\n'; });
man+='    </resource>\n';
man+='  </resources>\n</manifest>\n';
fs.writeFileSync(OUT+'/imsmanifest.xml', man);

/* ---------- second format: one assessment-style package per bank ---------- */
const OUT2='qti_assessment';
fs.rmSync(OUT2,{recursive:true,force:true});
banks.forEach(bk=>{
  const d=OUT2+'/'+bk.id;
  fs.mkdirSync(d+'/'+bk.id,{recursive:true});
  fs.mkdirSync(d+'/web_resources/econ003_midterm',{recursive:true});
  figs.forEach(f=>fs.copyFileSync(f, d+'/web_resources/econ003_midterm/'+path.basename(f)));
  fs.writeFileSync(d+'/'+bk.id+'/'+bk.id+'.xml', assessmentXml(bk));
  fs.writeFileSync(d+'/'+bk.id+'/assessment_meta.xml', metaXml(bk));
  let m='<?xml version="1.0" encoding="UTF-8"?>\n';
  m+='<manifest identifier="m_'+bk.id+'" '
   + 'xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" '
   + 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n';
  m+='  <metadata><schema>IMS Content</schema><schemaversion>1.1.3</schemaversion></metadata>\n';
  m+='  <organizations/>\n  <resources>\n';
  m+='    <resource identifier="r_'+bk.id+'" type="imsqti_xmlv1p2" href="'+bk.id+'/'+bk.id+'.xml">\n';
  m+='      <file href="'+bk.id+'/'+bk.id+'.xml"/>\n';
  m+='      <dependency identifierref="meta_'+bk.id+'"/>\n    </resource>\n';
  m+='    <resource identifier="meta_'+bk.id+'" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="'+bk.id+'/assessment_meta.xml">\n';
  m+='      <file href="'+bk.id+'/assessment_meta.xml"/>\n    </resource>\n';
  m+='    <resource identifier="web_'+bk.id+'" type="webcontent" href="web_resources/econ003_midterm/">\n';
  figs.forEach(f=>{ m+='      <file href="web_resources/econ003_midterm/'+path.basename(f)+'"/>\n'; });
  m+='    </resource>\n  </resources>\n</manifest>\n';
  fs.writeFileSync(d+'/imsmanifest.xml', m);
});

console.log('banks:');
banks.forEach(b=>console.log('  '+b.title.padEnd(46)+b.list.length+' items'));
console.log('items '+items.length+' · figures '+figs.length);
