const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,BorderStyle,ShadingType,ImageRun,
       Table,TableRow,TableCell,WidthType,AlignmentType}=require('docx');
const {writeVersioned}=require('./ver.js');
const D=require('./dropped.js');
const B='003DA5',G='B88300',INK='222222',MUT='777777',GRN='2E7D32',AMB='B45F06',F='Arial';
const p=o=>new Paragraph(o), t=(x,o={})=>new TextRun({text:x,font:F,...o});
const img=(f,w,h)=>p({alignment:AlignmentType.CENTER,spacing:{before:100,after:100},
  children:[new ImageRun({type:'png',data:fs.readFileSync(f),transformation:{width:w,height:h}})]});
const stem=x=>p({spacing:{after:50},indent:{left:260},children:[t(x,{size:21,color:INK})]});
const ask =x=>p({spacing:{before:60,after:52},indent:{left:260},children:[t(x,{size:21,bold:true,color:INK})]});
const opt=(x,ok,i)=>p({spacing:{after:22},indent:{left:600},children:[
  t(String.fromCharCode(65+i)+'. '+x,{size:20,color:ok?GRN:INK,bold:!!ok}),
  ok?t('   ✓ key',{size:17,bold:true,color:GRN}):t('')]});
const note=x=>p({spacing:{before:60,after:70},indent:{left:260},children:[t(x,{size:17,italics:true,color:MUT})]});
function tbl(rows){const w=rows[0].map(()=>Math.floor(8600/rows[0].length));
  return new Table({columnWidths:w,rows:rows.map((r,ri)=>new TableRow({children:r.map((c,ci)=>
    new TableCell({width:{size:w[ci],type:WidthType.DXA},margins:{top:50,bottom:50,left:110,right:110},
      shading:ri===0?{type:ShadingType.CLEAR,fill:'EFEFEF'}:undefined,
      children:[p({children:[t(String(c),{size:18,bold:ri===0,color:INK})]})]}))}))});}
const k=[];
k.push(p({spacing:{before:500,after:70},children:[t('ECON 003 — Midterm',{size:26,color:MUT})]}));
k.push(p({spacing:{after:60},children:[t('Currently NOT in the bank',{bold:true,size:40,color:B})]}));
k.push(p({spacing:{after:240},border:{bottom:{style:BorderStyle.SINGLE,size:12,color:G}},children:[t('')]}));
k.push(p({spacing:{after:200},children:[t('Five originals that are out. Everything else you have seen is in the bank. If any of these should be in too, say which.',{size:20,color:INK})]}));
D.forEach(x=>{
  k.push(p({spacing:{before:250,after:40},keepNext:true,children:[
    t(x.id+'  ',{bold:true,size:23,color:INK}), t(x.uid,{bold:true,size:22,color:B}),
    t('   §'+x.sec+' · '+x.tier,{size:16,color:MUT})]}));
  (x.lead||[]).forEach(l=>k.push(stem(l)));
  if(x.table) k.push(tbl(x.table));
  if(x.fig) k.push(img(x.fig,x.figw||360,x.figh||278));
  if(x.ask) k.push(ask(x.ask));
  x.opts.forEach((o,i)=>k.push(opt(o[0],!!o[1],i)));
  if(x.note) k.push(note(x.note));
});
const doc=new Document({styles:{default:{document:{run:{font:F,size:20,color:INK}}}},
  sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:900,bottom:900,left:900,right:900}}},children:k}]});
Packer.toBuffer(doc).then(b=>{const o=writeVersioned('ECON003_Midterm_Not_In_Bank',b);console.log('->',o.name,'|',D.length,'items');});
