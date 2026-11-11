const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,AlignmentType,PageBreak,
       BorderStyle,Table,TableRow,TableCell,WidthType,ShadingType,PageOrientation}=require('docx');
const D=JSON.parse(fs.readFileSync('/tmp/sel.json','utf8'));
const BLUE='003DA5', GOLD='B88300', INK='333333', MUT='666666', RED='CC3333', GRN='2E7D32';
const F='Arial';
const p=(o)=>new Paragraph(o);
const t=(text,o={})=>new TextRun({text,font:F,...o});
const CONV={A:['Use as written','D9EAD3'],B:['Mechanical revision','FFF2CC'],
            S:['Salvage — drop drawing task','DEEAF6'],C:['Rewrite','FCE5CD'],D:['Redraw','F4CCCC']};
const TYPE={'G-fig':'Figure-based','G-reason':'Graph reasoning','Quant':'Computation',
            'Concept':'Conceptual','Defn':'Definition'};
const kids=[];

// ---- cover ----
kids.push(p({spacing:{before:2200,after:120},children:[t('ECON 003 — Introduction to Microeconomics',{size:26,color:MUT})]}));
kids.push(p({spacing:{after:80},children:[t('Midterm Exam — Selected Question Pool',{bold:true,size:44,color:BLUE})]}));
kids.push(p({spacing:{after:400},border:{bottom:{style:BorderStyle.SINGLE,size:12,color:GOLD}},children:[t('')]}));
[['Exam','Saturday, August 15, 2026 · 10:00 AM – 12:00 PM PDT · online'],
 ['Coverage','Chapters 1, 3, 4, 5, 6'],
 ['Delivery','Canvas draws 50 items from a 150-item pool, stratified by chapter and difficulty'],
 ['This document','The 120 items selected from the Pearson bank. 30 originals still to be written.'],
 ['Source','Assignments/QB/ECON003_Master_Question_Bank.xlsx — Selection tab'],
 ['Generated','August 12, 2026']].forEach(([k,v])=>{
  kids.push(p({spacing:{after:100},children:[t(k+':  ',{bold:true,size:20,color:BLUE}),t(v,{size:20,color:INK})]}));
});
kids.push(p({spacing:{before:400,after:120},children:[t('Composition',{bold:true,size:24,color:BLUE})]}));
const counts={};D.forEach(d=>{counts[d.qtype]=(counts[d.qtype]||0)+1});
Object.entries(TYPE).forEach(([k,v])=>kids.push(p({spacing:{after:40},indent:{left:240},
  children:[t('· '+v+' — ',{size:20,color:INK}),t(String(counts[k]||0),{size:20,bold:true,color:BLUE})]})));
const cv={};D.forEach(d=>{cv[d.conv]=(cv[d.conv]||0)+1});
kids.push(p({spacing:{before:240,after:120},children:[t('Work required',{bold:true,size:24,color:BLUE})]}));
Object.entries(CONV).forEach(([k,[lab]])=>kids.push(p({spacing:{after:40},indent:{left:240},
  children:[t('· '+lab+' — ',{size:20,color:INK}),t(String(cv[k]||0),{size:20,bold:true,color:BLUE})]})));
kids.push(p({spacing:{before:200},children:[t('Answers are shown for every item. Reused items additionally need their numbers swapped and keys recomputed before use.',{size:18,italics:true,color:MUT})]}));
kids.push(p({children:[new PageBreak()]}));

// ---- questions ----
let lastCh=null,lastBucket=null,n=0;
D.forEach(d=>{
  if(d.ch!==lastCh){
    if(lastCh!==null) kids.push(p({children:[new PageBreak()]}));
    kids.push(p({heading:HeadingLevel.HEADING_1,spacing:{after:60},
      children:[t('Chapter '+d.ch,{bold:true,size:32,color:BLUE})]}));
    kids.push(p({spacing:{after:220},border:{bottom:{style:BorderStyle.SINGLE,size:8,color:'DDDDDD'}},children:[t('')]}));
    lastCh=d.ch; lastBucket=null;
  }
  if(d.bucket!==lastBucket){
    kids.push(p({spacing:{before:160,after:160},shading:{type:ShadingType.CLEAR,fill:'EEF2FA'},
      children:[t('  '+(d.bucket==='P'?'PEARSON-NEW — unused bank items':'REUSED — already seen in homework or quiz')+'  ',
        {bold:true,size:19,color:BLUE})]}));
    lastBucket=d.bucket;
  }
  n++;
  const [lab,fill]=CONV[d.conv];
  kids.push(p({spacing:{before:260,after:60},keepNext:true,children:[
    t(String(n)+'.  ',{bold:true,size:22,color:INK}),
    t(d.uid,{bold:true,size:22,color:BLUE}),
    t('   §'+d.sec+' · '+TYPE[d.qtype]+' · '+d.dtier+' · Pearson: '+d.diff+' · '+d.nopt+' options',{size:16,color:MUT}),
  ]}));
  kids.push(p({spacing:{after:100},keepNext:true,shading:{type:ShadingType.CLEAR,fill},
    children:[t('  '+lab+(d.fig?'  ·  figure needed':'')+'  ',{size:15,bold:true,color:INK})]}));
  if(d.fig) kids.push(p({spacing:{after:60},indent:{left:280},children:[
    t('Note: the text below is interleaved with the figure\u2019s own labels and axis values. Read the source page before rewriting this item.',
      {size:16,italics:true,color:'B88300'})]}));
  d.stem.forEach(l=>kids.push(p({spacing:{after:40},indent:{left:280},children:[t(l,{size:21,color:INK})]})));
  if(d.opts.length) kids.push(p({spacing:{before:60},children:[t('')]}));
  d.opts.forEach(l=>kids.push(p({spacing:{after:20},indent:{left:560},children:[t(l,{size:20,color:INK})]})));
  kids.push(p({spacing:{before:80,after:20},indent:{left:280},
    children:[t('Answer:  ',{bold:true,size:20,color:GRN}),t(d.ans.join('  |  '),{size:20,color:GRN})]}));
  kids.push(p({spacing:{after:60},indent:{left:280},
    children:[t('Action:  ',{bold:true,size:17,color:RED}),t(d.act,{size:17,color:MUT}),
              t('   [source: '+d.src+' · '+d.pid+']',{size:15,color:'999999'})]}));
});

const doc=new Document({
  styles:{default:{document:{run:{font:F,size:21,color:INK}}}},
  sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:1080,bottom:1080,left:1080,right:1080}}},
    children:kids}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync('ECON003_Midterm_Selected_Questions.docx',b);
  console.log('written',b.length,'bytes,',n,'questions');});
