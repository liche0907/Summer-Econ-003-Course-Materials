/* ECON 003 FINAL — QTI 1.2 package Canvas can import.
   19 item banks: 9 from the midterm material, 10 from the post-midterm pool.
   Refuses to build unless every item has exactly one key, >=4 options and its figure present. */
const fs=require('fs'), path=require('path');
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
                      .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
const FB='$IMS-CC-FILEBASE$/econ003_final';

/* ============ A · post-midterm 120, from the live pool ============ */
const POOL=JSON.parse(fs.readFileSync('./POOL2.json','utf8'));
const items=[];
POOL.forEach(x=>{
  const opts=x.options.map(o=>[o[1], o[1]===x.key]);
  items.push({lab:x.label, uid:'F-'+x.sec.replace('.','_')+'-'+x._q, sec:x.sec, tier:x.tier,
    half:'post', lead:x.stem.slice(0,-1), ask:x.stem[x.stem.length-1],
    tables:(x.tables||[]).filter(t=>t&&t.header),
    fig:x.fig?('figs/'+x.fig+'.png'):null, opts});
});

/* ============ B · midterm material, from the same sources the midterm shipped from ============ */
const B2=require('./batch2.js');
const REV=JSON.parse(fs.readFileSync('./rev.json','utf8'));
const SEL=JSON.parse(fs.readFileSync('./seltier.json','utf8'));
const TIER=JSON.parse(fs.readFileSync('./tieroverride.json','utf8'));
const ORIG=require('./originals.js');
const CUT={115:1,87:1,67:1,56:1,106:1,32:1,28:1,71:1,19:1,24:1};
const mid=[];
const b2n={}; B2.forEach(q=>b2n[Number(q.id.slice(1))]=q);
B2.forEach(q=>{const n=Number(q.id.slice(1)); if(CUT[n]) return;
  q.items.forEach(it=>{ if(n===88&&it.lab==='88b') return; mid.push({
    lab:it.lab, uid:q.uid, sec:it.sec||q.sec,
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
    mid.push({lab:String(n)+(s.letter||''), uid:x.uid, sec:x.sec,
      lead, ask:askLine, table:null, fig:null, opts:opts.map(o=>[o[0],!!o[1]])});
  });
});
ORIG.filter(x=>x.state==='ok').forEach(x=>mid.push({
  lab:x.id, uid:x.uid, sec:x.sec, lead:x.lead||[], ask:x.ask||'',
  table:x.table||null, fig:x.fig||null, opts:x.opts.map(o=>[o[0],!!o[1]])}));

/* keep only the 136 the final draws from, and take the RE-TIERED tier from the v4 pool */
const rows=fs.readFileSync('ECON003_Final_MidtermHalf_Pool_v4.csv','utf8').trim().split(/\r?\n/).slice(1);
const keep={};
rows.forEach(r=>{const c=r.split(','); keep[c[0]+'||'+c[1]]={sec:c[2],ch:c[3],tier:c[4]};});
let matched=0, unmatched=[];
mid.forEach(it=>{
  const k=keep[it.lab+'||'+it.uid];          // (label, uid) — a label alone is not unique
  if(k){ it.tier=k.tier; it.sec=k.sec; it.half='mid'; it.tables=it.table?[{header:it.table[0],rows:it.table.slice(1)}]:[]; matched++; items.push(it); }
});
Object.keys(keep).forEach(k=>{ if(!mid.some(it=>it.lab+'||'+it.uid===k)) unmatched.push(k); });

/* key first, so the by-bank document and the package agree */
items.forEach(it=>{ const a=it.opts.filter(o=>o[1]), b=it.opts.filter(o=>!o[1]); it.opts=a.concat(b); });

/* ============ banks ============ */
const banks=[];
[['1',['routine']],['3',['routine','challenging']],['4',['routine','challenging']],
 ['5',['routine','challenging']],['6',['routine','challenging']]].forEach(([ch,tiers])=>{
  tiers.forEach(tier=>banks.push({id:'m_ch'+ch+'_'+tier,
    title:'ECON003 Final - Midterm Ch'+ch+' '+tier[0].toUpperCase()+tier.slice(1),
    list:items.filter(i=>i.half==='mid'&&i.sec.split('.')[0]===ch&&i.tier===tier)}));
});
['7','8','9','10','12'].forEach(ch=>['routine','challenging'].forEach(tier=>
  banks.push({id:'p_ch'+ch+'_'+tier,
    title:'ECON003 Final - Ch'+ch+' '+tier[0].toUpperCase()+tier.slice(1),
    list:items.filter(i=>i.half==='post'&&i.sec.split('.')[0]===ch&&i.tier===tier)})));

/* ============ assertions ============ */
{
  const bad=[];
  items.forEach(it=>{
    const n=it.opts.filter(o=>o[1]).length;
    if(n!==1) bad.push(it.lab+' ('+it.uid+'): '+n+' keys');
    if(it.opts.length<4) bad.push(it.lab+': <4 options');
    if(!it.opts[0][1]) bad.push(it.lab+': key not first');
    if(it.fig && !fs.existsSync(it.fig)) bad.push(it.lab+': missing '+it.fig);
    if(!it.tier) bad.push(it.lab+': no tier');
    if(new Set(it.opts.map(o=>o[0])).size!==it.opts.length) bad.push(it.lab+': duplicate option');
  });
  const ids=items.map(i=>i.uid+' · '+i.lab);
  if(new Set(ids).size!==ids.length) bad.push('duplicate item titles');
  const placed=banks.reduce((a,b)=>a+b.list.length,0);
  if(placed!==items.length) bad.push('placed '+placed+' of '+items.length);
  if(items.filter(i=>i.half==='post').length!==120) bad.push('post-midterm not 120');
  if(bad.length){ console.error('BUILD REFUSED:'); bad.slice(0,40).forEach(x=>console.error('  '+x)); process.exit(1); }
}

/* ============ xml ============ */
function bodyHtml(it){
  let h='';
  (it.lead||[]).forEach(l=>h+='<p>'+esc(l)+'</p>');
  (it.tables||[]).forEach(t=>{
    h+='<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;"><tr>';
    t.header.forEach(c=>h+='<th>'+esc(c)+'</th>'); h+='</tr>';
    t.rows.forEach(r=>{h+='<tr>'; r.forEach(c=>h+='<td>'+esc(c)+'</td>'); h+='</tr>';});
    h+='</table>';
  });
  if(it.fig) h+='<p><img src="'+FB+'/'+path.basename(it.fig)+'" alt="figure for this question"></p>';
  if(it.ask) h+='<p><strong>'+esc(it.ask)+'</strong></p>';
  return h;
}
function itemXml(it,i,pfx){
  const ident='i_'+pfx+'_'+i;
  let x='    <item ident="'+ident+'" title="'+esc(it.uid+' '+it.lab)+'">\n';
  x+='      <itemmetadata><qtimetadata>\n';
  x+='        <qtimetadatafield><fieldlabel>question_type</fieldlabel><fieldentry>multiple_choice_question</fieldentry></qtimetadatafield>\n';
  x+='        <qtimetadatafield><fieldlabel>points_possible</fieldlabel><fieldentry>1</fieldentry></qtimetadatafield>\n';
  x+='        <qtimetadatafield><fieldlabel>original_answer_ids</fieldlabel><fieldentry>'+it.opts.map((o,j)=>ident+'_a'+j).join(',')+'</fieldentry></qtimetadatafield>\n';
  x+='      </qtimetadata></itemmetadata>\n';
  x+='      <presentation>\n';
  x+='        <material><mattext texttype="text/html">'+esc(bodyHtml(it))+'</mattext></material>\n';
  x+='        <response_lid ident="response1" rcardinality="Single">\n          <render_choice>\n';
  it.opts.forEach((o,j)=>{ x+='            <response_label ident="'+ident+'_a'+j+'">'
    +'<material><mattext texttype="text/html">'+esc('<p>'+esc(o[0])+'</p>')+'</mattext></material>'
    +'</response_label>\n'; });
  x+='          </render_choice>\n        </response_lid>\n      </presentation>\n';
  x+='      <resprocessing>\n';
  x+='        <outcomes><decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/></outcomes>\n';
  x+='        <respcondition continue="No">\n';
  x+='          <conditionvar><varequal respident="response1">'+ident+'_a0</varequal></conditionvar>\n';
  x+='          <setvar action="Set" varname="SCORE">100</setvar>\n';
  x+='        </respcondition>\n      </resprocessing>\n    </item>\n';
  return x;
}
function bankXml(bk){
  let x='<?xml version="1.0" encoding="UTF-8"?>\n<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" '
   +'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
   +'xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 '
   +'http://www.imsglobal.org/profile/cc/ccv1p2/ccv1p2_qtiasiv1p2p1_v1p0.xsd">\n';
  x+='  <assessment ident="a_'+bk.id+'" title="'+esc(bk.title)+'">\n    <qtimetadata>\n';
  x+='      <qtimetadatafield><fieldlabel>cc_maxattempts</fieldlabel><fieldentry>1</fieldentry></qtimetadatafield>\n';
  x+='    </qtimetadata>\n    <section ident="root_section">\n';
  bk.list.forEach((it,i)=>{ x+=itemXml(it,i+1,bk.id); });
  x+='    </section>\n  </assessment>\n</questestinterop>\n';
  return x;
}
function metaXml(bk){
  return '<?xml version="1.0" encoding="UTF-8"?>\n<quiz identifier="a_'+bk.id+'" '
   +'xmlns="http://canvas.instructure.com/xsd/cccv1p0" '
   +'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
   +'  <title>'+esc(bk.title)+'</title>\n'
   +'  <quiz_type>assignment</quiz_type>\n'
   +'  <points_possible>'+bk.list.length.toFixed(1)+'</points_possible>\n'
   +'  <shuffle_answers>true</shuffle_answers>\n'
   +'  <allowed_attempts>1</allowed_attempts>\n'
   +'  <scoring_policy>keep_highest</scoring_policy>\n</quiz>\n';
}

/* ===== write — ONE PACKAGE PER BANK, exactly the form that worked for the midterm ===== */
const OUT='QTI_IB';
fs.rmSync(OUT,{recursive:true,force:true});
const allfigs=[...new Set(items.filter(i=>i.fig).map(i=>i.fig))].sort();
banks.forEach(bk=>{
  const d=OUT+'/'+bk.id;
  fs.mkdirSync(d+'/'+bk.id,{recursive:true});
  fs.mkdirSync(d+'/web_resources/econ003_final',{recursive:true});
  fs.writeFileSync(d+'/'+bk.id+'/'+bk.id+'.xml', bankXml(bk));
  fs.writeFileSync(d+'/'+bk.id+'/assessment_meta.xml', metaXml(bk));
  const figs=[...new Set(bk.list.filter(i=>i.fig).map(i=>i.fig))].sort();
  figs.forEach(f=>fs.copyFileSync(f, d+'/web_resources/econ003_final/'+path.basename(f)));
  let m='<?xml version="1.0" encoding="UTF-8"?>\n<manifest identifier="m_'+bk.id+'" '
   +'xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" '
   +'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n';
  m+='  <metadata><schema>IMS Content</schema><schemaversion>1.1.3</schemaversion></metadata>\n';
  m+='  <organizations/>\n  <resources>\n';
  m+='    <resource identifier="r_'+bk.id+'" type="imsqti_xmlv1p2" href="'+bk.id+'/'+bk.id+'.xml">\n';
  m+='      <file href="'+bk.id+'/'+bk.id+'.xml"/>\n';
  m+='      <dependency identifierref="meta_'+bk.id+'"/>\n    </resource>\n';
  m+='    <resource identifier="meta_'+bk.id+'" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="'+bk.id+'/assessment_meta.xml">\n';
  m+='      <file href="'+bk.id+'/assessment_meta.xml"/>\n    </resource>\n';
  if(figs.length) m+='    <resource identifier="web_'+bk.id+'" type="webcontent" href="web_resources/econ003_final/">\n';
  figs.forEach(f=>{ m+='      <file href="web_resources/econ003_final/'+path.basename(f)+'"/>\n'; });
  m+=(figs.length?'    </resource>\n':'')+'  </resources>\n</manifest>\n';
  fs.writeFileSync(d+'/imsmanifest.xml', m);
});
console.log('midterm-material items matched: '+matched+' of 136');
if(unmatched.length) console.log('  NOT MATCHED ('+unmatched.length+'): '+unmatched.slice(0,10).join(', '));
console.log('\nper-bank packages:');
banks.forEach(b=>console.log('  '+b.id.padEnd(20)+b.title.padEnd(46)+String(b.list.length).padStart(3)+' items'));
console.log('\ntotal '+items.length+' items · '+allfigs.length+' distinct figures · '+banks.length+' packages');
