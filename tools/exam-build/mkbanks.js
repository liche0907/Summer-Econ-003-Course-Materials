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
const B='003DA5',G='B88300',INK='222222',MUT='777777',GRN='2E7D32',F='Arial';
const p=o=>new Paragraph(o), t=(x,o={})=>new TextRun({text:x,font:F,...o});
const img=(f,w,h)=>p({alignment:AlignmentType.CENTER,spacing:{before:100,after:100},
  children:[new ImageRun({type:'png',data:fs.readFileSync(f),transformation:{width:w,height:h}})]});
const stem=x=>p({spacing:{after:50},indent:{left:260},children:[t(x,{size:21,color:INK})]});
const ask =x=>p({spacing:{before:60,after:52},indent:{left:260},children:[t(x,{size:21,bold:true,color:INK})]});
const opt=(x,ok,i)=>p({spacing:{after:22},indent:{left:600},children:[
  t(String.fromCharCode(65+i)+'. '+x,{size:20,color:ok?GRN:INK,bold:!!ok}),
  ok?t('   ✓ key',{size:17,bold:true,color:GRN}):t('')]});
const note=x=>p({spacing:{before:60,after:70},indent:{left:260},children:[t(x,{size:17,italics:true,color:MUT})]});
function tbl(rows,widths){const w=widths||rows[0].map(()=>Math.floor(8600/rows[0].length));
  return new Table({columnWidths:w,rows:rows.map((r,ri)=>new TableRow({children:r.map((c,ci)=>
    new TableCell({width:{size:w[ci],type:WidthType.DXA},margins:{top:50,bottom:50,left:110,right:110},
      shading:ri===0?{type:ShadingType.CLEAR,fill:'EFEFEF'}:undefined,
      children:[p({children:[t(String(c),{size:18,bold:ri===0,color:INK})]})]}))}))});}

/* ---------- collect ---------- */
const b2n={}; B2.forEach(q=>b2n[Number(q.id.slice(1))]=q);
const items=[];
B2.forEach(q=>{const n=Number(q.id.slice(1)); if(CUT[n]) return;
  q.items.forEach(it=>{ if(n===88 && it.lab==='88b') return; items.push({
    n, lab:it.lab, uid:q.uid, sec:it.sec||q.sec,
    tier:TIER[it.lab]||it.tier||q.tier||(SEL[q.uid]||{}).tier,
    lead:it.lead||[], ask:it.ask||'', table:it.table||null,
    fig:it.fig||q.fig||null, figw:it.figw||360, figh:it.figh||278,
    opts:it.opts.map(o=>[o[0],!!o[1]]), note:it.note||'', src:'Pearson'});});
});
REV.forEach(x=>{const n=x.n; if(CUT[n]||b2n[n]) return;
  let groups=(x.subs||[]).concat(x.keep||[]);
  if(!groups.length){ if(x.status==='DROPPED') return;
    const p0=(x.parts&&x.parts[0])||{lead:[],opts:[]};
    groups=[{letter:'',lead:p0.lead||[],opts:p0.opts||[],ans:p0.ans}]; }
  groups.forEach(s=>{
    const lead=(s.lead||[]).slice();
    const askLine = lead.length>1 ? lead.pop() : '';
    const raw=(s.opts||[]);
    const norm=z=>String(z).replace(/^[A-H]\.\s*/,'').replace(/\s+/g,' ')
      .replace(/[‘’]/g,"'").replace(/[“”]/g,'"')
      .replace(/[−–—]/g,'-').replace(/[.\s]+$/,'').trim().toLowerCase();
    const A=norm(String(s.ans||''));
    let opts=raw.map(o=>[o.replace(/^[A-H]\.\s*/,''), A && norm(o)===A]);
    if(A && !opts.some(o=>o[1])){ let best=-1,len=-1;
      opts.forEach((o,i)=>{const q2=norm(o[0]);
        if(q2 && (A.startsWith(q2)||q2.startsWith(A)) && q2.length>len){len=q2.length;best=i;}});
      if(best>=0) opts[best][1]=true; }
    items.push({n, lab:String(n)+(s.letter||''), uid:x.uid, sec:x.sec,
      tier:TIER[String(n)+(s.letter||'')]||(SEL[x.uid]||{}).tier,
      lead, ask:askLine, table:null, fig:null,
      opts:opts.map(o=>[o[0],!!o[1]]), note:'', src:'Pearson'});
  });
});
ORIG.filter(x=>x.state==='ok').forEach(x=>items.push({
  n:900, lab:x.id, uid:x.uid, sec:x.sec, tier:x.tier,
  lead:x.lead||[], ask:x.ask||'', table:x.table||null,
  fig:x.fig||null, figw:x.figw||360, figh:x.figh||278,
  opts:x.opts.map(o=>[o[0],!!o[1]]), note:x.note||'', src:'original'}));

/* ---------- key first: the answer is always A ---------- */
items.forEach(it=>{
  const key=it.opts.filter(o=>o[1]), rest=it.opts.filter(o=>!o[1]);
  it.opts=key.concat(rest);
});

/* ---------- the ten banks ---------- */
const CH=['1','3','4','5','6'];
const DRAW={'1':{routine:5,challenging:1},'3':{routine:6,challenging:2},
            '4':{routine:8,challenging:4},'5':{routine:8,challenging:4},'6':{routine:8,challenging:4}};
const banks=[];
for(const ch of CH) for(const tier of ['routine','challenging']){
  const list=items.filter(i=>i.sec.split('.')[0]===ch && i.tier===tier)
                  .sort((a,b)=>a.sec.localeCompare(b.sec)||a.n-b.n||a.lab.localeCompare(b.lab));
  banks.push({ch, tier, list, draw:DRAW[ch][tier],
              name:'ECON003 Midterm — Ch'+ch+' '+tier[0].toUpperCase()+tier.slice(1)});
}

/* ---------- assertions ---------- */
{
  const problems=[];
  items.forEach(it=>{
    if(it.opts.filter(o=>o[1]).length!==1) problems.push(it.lab+': key count');
    if(it.opts.length<4) problems.push(it.lab+': <4 options');
    if(!it.tier) problems.push(it.lab+': no tier');
    if(it.fig && !fs.existsSync(it.fig)) problems.push(it.lab+': missing figure');
    if(!it.opts[0][1]) problems.push(it.lab+': key is not option A');
  });
  const placed=banks.reduce((a,b)=>a+b.list.length,0);
  if(placed!==items.length) problems.push('only '+placed+' of '+items.length+' items landed in a bank');
  if(problems.length){ console.error('BUILD REFUSED:'); problems.forEach(x=>console.error('  '+x)); process.exit(1); }
  console.log('assertions passed: '+items.length+' items, all placed in one of ten banks');
}

/* ---------- document ---------- */
const k=[];
k.push(p({spacing:{before:600,after:80},children:[t('ECON 003 — Midterm',{size:26,color:MUT})]}));
k.push(p({spacing:{after:70},children:[t('Grouped by Canvas item bank',{bold:true,size:40,color:B})]}));
k.push(p({spacing:{after:260},border:{bottom:{style:BorderStyle.SINGLE,size:12,color:G}},children:[t('')]}));
k.push(p({spacing:{after:140},children:[t('Ten banks, one per chapter per tier, in the order to build them. Each starts on its own page. Create the bank in Canvas with the name shown, add every question under it, then set that bank’s draw to the number in the Draw column.',{size:20,color:INK})]}));
k.push(p({spacing:{before:40,after:120},shading:{type:ShadingType.CLEAR,fill:'FDECEA'},
  children:[t('  THE CORRECT ANSWER IS ALWAYS OPTION A IN THIS DOCUMENT.  ',{bold:true,size:20,color:'CC3333'})]}));
k.push(p({spacing:{after:180},children:[
  t('Options are ordered with the key first so entry is faster \u2014 tick the top option every time. ',{size:20,color:INK}),
  t('Switch on answer shuffling in Canvas, or every answer on the real exam will be A.',{bold:true,size:20,color:INK}),
  t(' In New Quizzes that is \u201cShuffle answers\u201d on the question, or set it for the whole quiz in the quiz settings. No question in this pool refers to an option by its letter, so shuffling is safe on every one.',{size:20,color:INK})]}));
k.push(tbl([['#','Canvas item bank name','Items','Draw','Coverage']].concat(
  banks.map((b,i)=>[String(i+1), b.name, String(b.list.length), String(b.draw),
                    (b.list.length/b.draw).toFixed(1)+'×'])),[600,4400,900,900,1000]));
k.push(p({spacing:{before:160,after:60},children:[
  t('Totals:  ',{bold:true,size:20,color:B}),
  t(items.length+' questions · 35 routine + 15 challenging drawn per student · chapter weights 6 / 8 / 12 / 12 / 12.',{size:20,color:INK})]}));
k.push(p({spacing:{after:60},children:[
  t('Thinnest bank:  ',{bold:true,size:20,color:B}),
  t('Ch3 Routine at '+ (banks.find(b=>b.ch==='3'&&b.tier==='routine').list.length) +' items for 6 drawn. Every other bank is at least 2.3×.',{size:20,color:INK})]}));
k.push(p({children:[new PageBreak()]}));

banks.forEach((bk,bi)=>{
  k.push(p({spacing:{before:0,after:60},keepNext:true,children:[
    t('Bank '+(bi+1)+' of 10',{size:18,color:MUT})]}));
  k.push(p({spacing:{after:40},keepNext:true,children:[t(bk.name,{bold:true,size:32,color:B})]}));
  k.push(p({spacing:{after:180},keepNext:true,
    border:{bottom:{style:BorderStyle.SINGLE,size:8,color:G}},
    children:[t(bk.list.length+' questions in this bank  ·  draw '+bk.draw+' per student  ·  '
                +(bk.list.length/bk.draw).toFixed(1)+'× coverage',{size:19,color:INK})]}));
  bk.list.forEach((it,ix)=>{
    k.push(p({spacing:{before:230,after:40},keepNext:true,children:[
      t((ix+1)+'.  ',{bold:true,size:22,color:MUT}),
      t((it.src==='original'?'':'Q')+it.lab+'  ',{bold:true,size:22,color:INK}),
      t(it.uid,{bold:true,size:20,color:B}),
      t('   §'+it.sec+' · '+it.src,{size:16,color:MUT})]}));
    it.lead.forEach(l=>k.push(stem(l)));
    if(it.table) k.push(tbl(it.table));
    if(it.fig) k.push(img(it.fig,it.figw,it.figh));
    if(it.ask) k.push(ask(it.ask));
    it.opts.forEach((o,i)=>k.push(opt(o[0],o[1],i)));
    if(it.note) k.push(note(it.note));
  });
  if(bi<banks.length-1) k.push(p({children:[new PageBreak()]}));
});

const doc=new Document({styles:{default:{document:{run:{font:F,size:20,color:INK}}}},
  sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:900,bottom:900,left:900,right:900}}},children:k}]});
Packer.toBuffer(doc).then(b=>{const o=writeVersioned('ECON003_Midterm_By_Bank',b);
  console.log('->',o.name);
  banks.forEach((bk,i)=>console.log('  '+(i+1)+'. '+bk.name.padEnd(46)+bk.list.length+' items, draw '+bk.draw));});
