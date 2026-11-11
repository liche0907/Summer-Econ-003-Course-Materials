const {Document,Packer,Paragraph,TextRun,HeadingLevel,BorderStyle,ShadingType,PageBreak,
       Table,TableRow,TableCell,WidthType,ImageRun,AlignmentType}=require('docx');
const fs=require('fs');
const N=JSON.parse(fs.readFileSync('/tmp/POOL2.json','utf8'));
const SECN={'7.1':'Perfect Competition and Efficiency','7.3':'Allocation of Resources Across Industries','7.4':'Prices Guide the Invisible Hand','7.5':'Equity and Efficiency','8.1':'The Production Possibilities Curve','8.2':'The Basis for Trade: Comparative Advantage','8.3':'Trade Between States','8.4':'Trade Between Countries','8.5':'Arguments Against Free Trade','9.1':'Externalities','9.2':'Private Solutions to Externalities','9.3':'Government Solutions to Externalities','9.4':'Public Goods','9.5':'Common Pool Resource Goods','10.1':'§10.1.3 Tax Incidence and Deadweight Loss','10.2':'§10.2 Regulation','10.3':'§10.3 Government Failures','12.1':'Introducing a New Market Structure','12.2':'Sources of Market Power','12.3':"The Monopolist's Problem",'12.4':'Choosing the Optimal Quantity and Price','12.5':'The Cost of Monopoly','12.7':'§12.7 Policy Toward Monopoly (not examined)'};
const SECS={'7':['7.1','7.3','7.4','7.5'],'8':['8.1','8.2','8.3','8.4','8.5'],'9':['9.1','9.2','9.3','9.4','9.5'],'10':['10.1','10.2','10.3'],'12':['12.1','12.2','12.3','12.4','12.5','12.7']};
const p=(t,o={})=>new Paragraph({children:[new TextRun({text:t,...o})],spacing:{after:o.after??60},indent:o.indent,alignment:o.alignment});
function tbl(t){
  const cols=t.header.length, W=Math.floor(8000/cols), widths=Array(cols).fill(W);
  const row=(cells,head)=>new TableRow({children:cells.map(c=>new TableCell({
      width:{size:W,type:WidthType.DXA},
      shading:head?{type:ShadingType.CLEAR,fill:'EDEDED'}:undefined,
      children:[new Paragraph({children:[new TextRun({text:String(c??''),bold:!!head,size:19})],
                spacing:{before:40,after:40},alignment:AlignmentType.CENTER})]}))});
  return new Table({columnWidths:widths,width:{size:8000,type:WidthType.DXA},
    rows:[row(t.header,true),...t.rows.map(r=>row(r,false))]});
}
const kids=[];
kids.push(new Paragraph({text:'ECON 003 — Final Exam',heading:HeadingLevel.TITLE}));
kids.push(new Paragraph({text:'Post-midterm pool, Ch 7 · 8 · 9 · 10 · 12 — v13, FINAL',heading:HeadingLevel.HEADING_1}));
kids.push(p('27 August 2026 — final. All 120 read one by one and timed; American spelling; the structural audit passes clean. Exam window is three hours, 10:00 AM – 1:00 PM. 120 items: 82 drawn from the Pearson banks and rebuilt for Canvas, 38 written for this exam. §12.7 is not examined.',{italics:true}));
kids.push(p('Every item was transcribed from the printed page image, not from the PDF text layer. Tables are set as tables; every figure is drawn, not described. An item printed with four options keeps four — nothing was padded. Keyed by answer text, no shuffle-unsafe options.',{}));
kids.push(p('Draw: 36 of the final’s 60 — Ch 7 = 7 · Ch 8 = 8 · Ch 9 = 8 · Ch 10 = 5 · Ch 12 = 8, at 24 routine / 12 challenging. Pool coverage 3.2–3.5× in every chapter and tier. 79 routine / 41 challenging. 33 figure placements + 11 tables = 37% of items visual.',{}));
kids.push(p('Section, difficulty and visual coverage are mapped in the companion Map document. ⚑ marks an item where something still needs your decision.',{}));
kids.push(p('Approval convention: delete what you approve. Anything still present is rejected.',{bold:true}));
kids.push(new Paragraph({children:[new PageBreak()]}));
let n=0,figs=0;
for(const ch of ['7','8','9','10','12']){
  kids.push(new Paragraph({text:'Chapter '+ch,heading:HeadingLevel.HEADING_1,pageBreakBefore:ch!=='7'}));
  for(const sec of SECS[ch]){
    const g=N.filter(x=>x.sec===sec); if(!g.length) continue;
    kids.push(new Paragraph({text:sec+'  '+SECN[sec],heading:HeadingLevel.HEADING_2}));
    kids.push(p(g.length+' items · '+g.filter(x=>x.tier==='routine').length+' routine / '+g.filter(x=>x.tier==='challenging').length+' challenging · '+g.filter(x=>x.src==='original').length+' written for this exam',{italics:true,size:18,after:140}));
    for(const tier of ['routine','challenging'])
    for(const x of g.filter(y=>y.tier===tier)){
      n++;
      const tag=(x.src==='original'?'ORIGINAL':x.cls);
      kids.push(new Paragraph({spacing:{before:240,after:50},border:{top:{style:BorderStyle.SINGLE,size:6,color:'AAAAAA'}},
        children:[new TextRun({text:'['+n+']  '+x.label+'   ',bold:true,size:22}),
                  new TextRun({text:sec+' · '+tier+' · '+tag,size:16,color:'666666'})]}));
      (x.stem||[]).forEach(s=>kids.push(p(s,{after:60})));
      (x.tables||[]).forEach(t=>{ if(t&&t.header&&t.header.length){
        if(t.caption) kids.push(p(t.caption,{italics:true,size:18,after:40}));
        kids.push(tbl(t)); kids.push(p('',{after:80}));}});
      if(x.fig&&fs.existsSync('figs/'+x.fig+'.png')){
        figs++;
        kids.push(new Paragraph({spacing:{before:60,after:60},children:[new ImageRun({
          type:'png',data:fs.readFileSync('figs/'+x.fig+'.png'),transformation:{width:400,height:315}})]}));
        kids.push(p('figure: '+x.fig+'.png  — drawn for this exam, house style',{size:15,color:'888888',italics:true,after:60}));
      }
      x.options.forEach(([L,t])=>kids.push(p(L+'.  '+t,{indent:{left:420},after:26,size:20})));
      kids.push(new Paragraph({spacing:{before:40,after:40},indent:{left:420},
        children:[new TextRun({text:'KEY: ',bold:true,size:20}),new TextRun({text:x.key,size:20,bold:true})]}));
      (x.distractors||[]).forEach(d=>kids.push(p('· '+String(d).replace(/\s+/g,' ').trim(),{indent:{left:560},size:16,color:'444444',after:14})));
      if(x.note) kids.push(p((x.src==='original'?'why: ':'changed: ')+String(x.note).replace(/\s+/g,' '),{indent:{left:420},size:16,italics:true,color:'555555',after:30}));
      if(x.gap) kids.push(p('gap: '+x.gap,{indent:{left:420},size:16,italics:true,color:'555555',after:30}));
      (x.issues||[]).filter(i=>['clipped','missing_word','garbled','figure_unreadable'].includes(i.type))
        .forEach(i=>kids.push(new Paragraph({spacing:{after:30},indent:{left:420},children:[
          new TextRun({text:'⚑ FETCH FROM PEARSON ('+i.type+', '+(i.where||'')+'): ',bold:true,size:16,color:'A03000'}),
          new TextRun({text:String(i.note||i.text||'').replace(/\s+/g,' '),size:16,color:'A03000'})]})));
      if(x.review) kids.push(new Paragraph({spacing:{after:60},indent:{left:420},children:[
        new TextRun({text:'⚑ '+String(x.review).replace(/\s+/g,' '),bold:true,size:16,color:'A03000'})]}));
    }
  }
}
const doc=new Document({sections:[{properties:{page:{size:{width:12240,height:15840}}},children:kids}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync('ECON003_Final_PostMidterm_Pool_v13.docx',b);
  console.log('wrote pool v6:',n,'items,',figs,'figures embedded');});
