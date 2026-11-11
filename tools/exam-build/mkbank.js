const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,PageBreak,BorderStyle,ShadingType,ImageRun,
       Table,TableRow,TableCell,WidthType,AlignmentType}=require('docx');

const {writeVersioned}=require('./ver.js');
const B2=require('./batch2.js');
const REV=JSON.parse(fs.readFileSync('./rev.json','utf8'));
const SEL=JSON.parse(fs.readFileSync('./seltier.json','utf8'));
const TIER=JSON.parse(fs.readFileSync('./tieroverride.json','utf8'));
const ORIG=require('./originals.js');

const CUT={115:1,87:1,67:1,56:1,106:1,32:1,28:1,71:1,19:1,24:1};  // 19: quadratic MB; 24: "people always optimize" - both removed by hand Aug 14
const B='003DA5',G='B88300',INK='222222',MUT='777777',RED='CC3333',GRN='2E7D32',AMB='B45F06',F='Arial';
const p=o=>new Paragraph(o), t=(x,o={})=>new TextRun({text:x,font:F,...o});

const DEFECT={
  // all 16 flagged items repaired Aug 14. Add entries here as new defects surface.
};

const img=(f,w,h)=>p({alignment:AlignmentType.CENTER,spacing:{before:100,after:100},
  children:[new ImageRun({type:'png',data:fs.readFileSync(f),transformation:{width:w,height:h}})]});
const stem=x=>p({spacing:{after:50},indent:{left:260},children:[t(x,{size:21,color:INK})]});
const ask =x=>p({spacing:{before:60,after:52},indent:{left:260},children:[t(x,{size:21,bold:true,color:INK})]});
const opt=(x,ok,i)=>p({spacing:{after:22},indent:{left:600},children:[
  t(String.fromCharCode(65+i)+'. '+x,{size:20,color:ok?GRN:INK,bold:!!ok}),
  ok?t('   ✓ key',{size:17,bold:true,color:GRN}):t('')]});
const note=x=>p({spacing:{before:60,after:70},indent:{left:260},children:[t(x,{size:17,italics:true,color:MUT})]});
const flag=x=>p({spacing:{before:60,after:70},indent:{left:260},shading:{type:ShadingType.CLEAR,fill:'FDECEA'},
  children:[t('  ⚑ NEEDS WORK — '+x+'  ',{size:17,bold:true,color:RED})]});

function tbl(rows,widths){
  const w=widths||rows[0].map(()=>Math.floor(8600/rows[0].length));
  return new Table({columnWidths:w,
    rows:rows.map((r,ri)=>new TableRow({children:r.map((c,ci)=>new TableCell({
      width:{size:w[ci],type:WidthType.DXA},margins:{top:50,bottom:50,left:110,right:110},
      shading:ri===0?{type:ShadingType.CLEAR,fill:'EFEFEF'}:undefined,
      children:[p({children:[t(String(c),{size:18,bold:ri===0,color:INK})]})]}))}))});
}

/* ---------- collect every live item ---------- */
const b2n={}; B2.forEach(q=>b2n[Number(q.id.slice(1))]=q);
const items=[];
B2.forEach(q=>{
  const n=Number(q.id.slice(1));
  if(CUT[n]) return;
  q.items.forEach(it=>{ if(n===88 && it.lab==='88b') return; items.push({
    n, lab:it.lab, uid:q.uid, sec:it.sec||q.sec,
    tier:TIER[it.lab]||it.tier||q.tier||(SEL[q.uid]||{}).tier||'—',
    lead:it.lead||[], ask:it.ask||'', table:it.table||null,
    fig:it.fig||q.fig||null, figw:it.figw||360, figh:it.figh||278,
    opts:it.opts.map(o=>[o[0],!!o[1]]), note:it.note||'', src:'rework'});});
});
REV.forEach(x=>{
  const n=x.n;
  if(CUT[n]||b2n[n]) return;
  let groups=(x.subs||[]).concat(x.keep||[]);
  if(!groups.length){
    if(x.status==='DROPPED') return;
    const p0=(x.parts&&x.parts[0])||{lead:[],opts:[]};
    groups=[{letter:'',lead:p0.lead||[],opts:p0.opts||[],ans:p0.ans}];
  }
  groups.forEach(s=>{
    const lead=(s.lead||[]).slice();
    const askLine = lead.length>1 ? lead.pop() : '';
    const raw=(s.opts||[]);
    const ansTxt=String(s.ans||'').replace(/^[A-H]\.\s*/,'').trim();
    const norm=z=>String(z).replace(/^[A-H]\.\s*/,'').replace(/\s+/g,' ')
                    .replace(/[\u2018\u2019]/g,"'").replace(/[\u201c\u201d]/g,'"')
                    .replace(/[\u2212\u2013\u2014]/g,'-').replace(/[.\s]+$/,'').trim().toLowerCase();
    const A=norm(ansTxt);
    let opts=raw.map(o=>[o.replace(/^[A-H]\.\s*/,''), A && norm(o)===A]);
    if(A && !opts.some(o=>o[1])){                    // exact match failed - fall back to prefix,
      let best=-1, len=-1;                           // but keep only the single longest match
      opts.forEach((o,i)=>{ const n=norm(o[0]);
        if(n && (A.startsWith(n)||n.startsWith(A)) && n.length>len){len=n.length;best=i;} });
      if(best>=0) opts[best][1]=true;
    }
    opts=opts.map(o=>[o[0],!!o[1]]);
    items.push({n, lab:String(n)+(s.letter||''), uid:x.uid, sec:x.sec,
      tier:TIER[String(n)+(s.letter||'')]||(SEL[x.uid]||{}).tier||'—',
      lead, ask:askLine, table:null, fig:null, opts, note:'', src:'as printed'});
  });
});
/* ---------- approved originals join the bank ---------- */
ORIG.filter(x=>x.state==='ok').forEach(x=>items.push({
  n:900, lab:x.id, uid:x.uid, sec:x.sec, tier:x.tier,
  lead:x.lead||[], ask:x.ask||'', table:x.table||null,
  fig:x.fig||null, figw:x.figw||360, figh:x.figh||278,
  opts:x.opts.map(o=>[o[0],!!o[1]]), note:x.note||'', src:'original'}));

items.sort((a,b)=>a.sec===b.sec ? (a.n-b.n||a.lab.localeCompare(b.lab)) : a.sec.localeCompare(b.sec));


/* ---------- build-time assertions: refuse to emit a bad file ---------- */
{
  const problems=[];
  items.forEach(it=>{
    const k=it.opts.filter(o=>o[1]).length;
    if(k!==1) problems.push(it.lab+' has '+k+' keys');
    if(it.opts.length<4) problems.push(it.lab+' has only '+it.opts.length+' options');
    const seen=new Set();
    it.opts.forEach(o=>{const n=String(o[0]).replace(/\s+/g,' ').trim().toLowerCase();
      if(seen.has(n)) problems.push(it.lab+' has a duplicate option'); seen.add(n);});
    if(it.fig && !fs.existsSync(it.fig)) problems.push(it.lab+' points at a missing figure '+it.fig);
    if(!it.tier||it.tier==='—') problems.push(it.lab+' has no tier');
    if(/\[MINE\]|All of the above|Both A and B/i.test(it.opts.map(o=>o[0]).join(' ')))
      problems.push(it.lab+' has a shuffle-unsafe or leaked-tag option');
  });
  if(problems.length){
    console.error('BUILD REFUSED — '+problems.length+' problem(s):');
    problems.forEach(p=>console.error('  '+p));
    process.exit(1);
  }
  console.log('assertions passed: '+items.length+' items, one key each, >=4 options, figures present, tiers set');
}

/* ---------- document ---------- */
const k=[];
const nVis=items.filter(i=>i.fig||i.table).length;
const nCh =items.filter(i=>i.tier==='challenging').length;
const nBad=items.filter(i=>DEFECT[i.lab]).length;

k.push(p({spacing:{before:800,after:80},children:[t('ECON 003 — Midterm',{size:26,color:MUT})]}));
k.push(p({spacing:{after:70},children:[t('Question Bank — current state',{bold:true,size:42,color:B})]}));
k.push(p({spacing:{after:300},border:{bottom:{style:BorderStyle.SINGLE,size:12,color:G}},children:[t('')]}));
[['Items',String(items.length)+' live questions, ordered by section \u2014 '+items.filter(i=>i.src==='original').length+' of them originals written for this exam, the rest adapted from Pearson.'],
 ['Tiers',nCh+' challenging, '+(items.length-nCh)+' routine.'],
 ['Visuals',nVis+' carry a figure or a table.'],
 ['Needs work',nBad+' items are flagged in red where they sit. The same list is on the next page.'],
 ['Keys','Marked ✓ on the option itself, by text — never by Pearson’s answer letter.'],
 ['Generated','August 13, 2026']].forEach(([a,b])=>k.push(p({spacing:{after:100},
   children:[t(a+':  ',{bold:true,size:20,color:B}),t(b,{size:20,color:INK})]})));
k.push(p({children:[new PageBreak()]}));

k.push(p({spacing:{after:140},children:[t('Items that need work',{bold:true,size:28,color:B})]}));
k.push(tbl([['Item','§','What is wrong']].concat(
  items.filter(i=>DEFECT[i.lab]).map(i=>['Q'+i.lab,i.sec,DEFECT[i.lab]])),[1100,700,6800]));
k.push(p({children:[new PageBreak()]}));

let sec=null;
items.forEach(it=>{
  if(it.sec!==sec){
    sec=it.sec;
    k.push(p({spacing:{before:300,after:120},keepNext:true,
      border:{bottom:{style:BorderStyle.SINGLE,size:8,color:G}},
      children:[t('§ '+sec,{bold:true,size:30,color:B}),
                t('    '+items.filter(x=>x.sec===sec).length+' items',{size:18,color:MUT})]}));
  }
  k.push(p({spacing:{before:240,after:40},keepNext:true,children:[
    t((it.src==='original'?'':'Q')+it.lab+'  ',{bold:true,size:23,color:INK}),
    t(it.uid,{bold:true,size:22,color:B}),
    t('   '+it.tier+' · '+it.src,{size:16,color:MUT})]}));
  if(DEFECT[it.lab]) k.push(flag(DEFECT[it.lab]));
  it.lead.forEach(l=>k.push(stem(l)));
  if(it.table) k.push(tbl(it.table));
  if(it.fig) k.push(img(it.fig,it.figw,it.figh));
  if(it.ask) k.push(ask(it.ask));
  it.opts.forEach((o,i)=>k.push(opt(o[0],o[1],i)));
  const nk=it.opts.filter(o=>o[1]).length;
  if(nk===0) k.push(flag('No key could be matched to an option — check this one.'));
  if(nk>1)  k.push(flag(nk+' options are marked as the key — check this one.'));
  if(it.note) k.push(note(it.note));
});

const doc=new Document({styles:{default:{document:{run:{font:F,size:20,color:INK}}}},
  sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:900,bottom:900,left:900,right:900}}},children:k}]});
Packer.toBuffer(doc).then(b=>{const o=writeVersioned('ECON003_Midterm_Question_Bank',b);
  console.log('->',o.name);
  console.log('written',b.length,'| items',items.length,'| visuals',nVis,'| challenging',nCh,'| flagged',nBad);});
