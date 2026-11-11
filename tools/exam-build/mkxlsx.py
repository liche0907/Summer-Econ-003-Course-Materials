import pickle, re, collections
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

m=pickle.load(open('/tmp/master.pkl','rb'))
from clean import clean_text
CTL=re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')
def cl(s): return CTL.sub('',clean_text(s))

norm=lambda p: re.sub(r'\s*\((algo|static)\)\s*$','',p,flags=re.I).strip().lower()
bych=collections.defaultdict(set)
for i in m: bych[norm(i['pid'])].add(i['ch'])
for i in m: i['collide']='Yes' if len(bych[norm(i['pid'])])>1 else 'No'

BLUE='003DA5'; GOLD='FFB81D'; LIGHT='EEF2FA'
hf=Font(name='Arial',size=10,bold=True,color='FFFFFF')
bf=Font(name='Arial',size=10)
hfill=PatternFill('solid',fgColor=BLUE)
thin=Side(style='thin',color='BBBBBB'); bd=Border(bottom=thin)

wb=Workbook(); ws=wb.active; ws.title='Master'
COLS=[('UID',14),('Ch',5),('Sec',6),('Section Title',34),('Type',17),('Pearson ID',26),
      ('ID Collision',12),('Variant',8),('Used',6),('Used In',14),('Difficulty',11),
      ('Est Time (s)',12),('Parts',6),('Format',10),('Options',8),('Multi-Select',12),
      ('Figure',8),('Src Pages',16),('Tier',6),('Salvage',9),('Conversion Note',52),('Stem',80),('Option Text',60),('Answer',44),('Verify Text',11),('Selected',10)]
for c,(h,w) in enumerate(COLS,1):
    cell=ws.cell(1,c,h); cell.font=hf; cell.fill=hfill
    cell.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
    ws.column_dimensions[get_column_letter(c)].width=w
ws.row_dimensions[1].height=30

m.sort(key=lambda i:(i['ch'],i['sec'],i['order']))
TFILL={'A':PatternFill('solid',fgColor='D9EAD3'),'B':PatternFill('solid',fgColor='FFF2CC'),
       'C':PatternFill('solid',fgColor='FCE5CD'),'D':PatternFill('solid',fgColor='F4CCCC')}
for r,i in enumerate(m,2):
    row=[i['uid'],i['ch'],i['sec'],cl(i['section']),i['qtype'],cl(i['pid']),i['collide'],
         i['variant'],'Yes' if i['used_in'] else 'No',', '.join(i['used_in']),i['difficulty'],
         i['time_s'],i['parts'],i['fmt'],i['nopt'],'Yes' if i['cata'] else '',i['figure'],f"{i['bank']} p{i['pages'][0]}-{i['pages'][-1]}",
         i['tier'],i['salvage'],i['why'],cl(i['stem']),cl(i['opts']),cl(i['ans']),i.get('trunc',''),i.get('sel','')]
    for c,v in enumerate(row,1):
        cell=ws.cell(r,c,v); cell.font=bf; cell.border=bd
        cell.alignment=Alignment(vertical='top',wrap_text=(c>=21),
            horizontal='center' if c in (2,3,7,8,9,11,12,13,14,15,16,17,19,20) else 'left')
    ws.cell(r,19).fill=TFILL[i['tier']]
    if i['used_in']:
        for c in (9,10): ws.cell(r,c).fill=PatternFill('solid',fgColor=LIGHT)
    ws.row_dimensions[r].height=30
ws.freeze_panes='A2'; ws.auto_filter.ref=f'A1:Z{len(m)+1}'

# ---------------- Summary (formulas only) ----------------
s=wb.create_sheet('Summary')
s['A1']='ECON 003 — Master Question Bank: coverage against the midterm blueprint'
s['A1'].font=Font(name='Arial',size=13,bold=True,color=BLUE)
s['A2']='All figures are live COUNTIFS over the Master sheet. Edit a Tier or Used cell there and this updates.'
s['A2'].font=Font(name='Arial',size=9,italic=True,color='666666')
hdr=['Chapter','Bank','Tier A','Tier B','Tier C','Tier D','A+B unused','Need (Pearson-new)','Margin',
     'A+B used','Need (reuse)','Margin ']
for c,h in enumerate(hdr,1):
    cell=s.cell(4,c,h); cell.font=hf; cell.fill=hfill
    cell.alignment=Alignment(horizontal='center',wrap_text=True); s.column_dimensions[get_column_letter(c)].width=15
s.row_dimensions[4].height=32
needP={1:13,3:16,4:20,5:18,6:15}; needR={1:6,3:8,4:9,5:8,6:7}
N=len(m)+1
for n,ch in enumerate([1,3,4,5,6]):
    r=5+n
    s.cell(r,1,f'Ch {ch}')
    s.cell(r,2,f'=COUNTIF(Master!$B$2:$B${N},{ch})')
    for k,t in enumerate('ABCD'):
        s.cell(r,3+k,f'=COUNTIFS(Master!$B$2:$B${N},{ch},Master!$S$2:$S${N},"{t}")')
    s.cell(r,7,f'=COUNTIFS(Master!$B$2:$B${N},{ch},Master!$I$2:$I${N},"No",Master!$S$2:$S${N},"A")'
               f'+COUNTIFS(Master!$B$2:$B${N},{ch},Master!$I$2:$I${N},"No",Master!$S$2:$S${N},"B")')
    s.cell(r,8,needP[ch]); s.cell(r,9,f'=G{r}-H{r}')
    s.cell(r,10,f'=COUNTIFS(Master!$B$2:$B${N},{ch},Master!$I$2:$I${N},"Yes",Master!$S$2:$S${N},"A")'
                f'+COUNTIFS(Master!$B$2:$B${N},{ch},Master!$I$2:$I${N},"Yes",Master!$S$2:$S${N},"B")')
    s.cell(r,11,needR[ch]); s.cell(r,12,f'=J{r}-K{r}')
tr=10
s.cell(tr,1,'TOTAL').font=Font(name='Arial',size=10,bold=True)
for c in range(2,13):
    L=get_column_letter(c); s.cell(tr,c,f'=SUM({L}5:{L}9)')
for c in range(1,13):
    for r in range(5,11):
        cell=s.cell(r,c); cell.font=Font(name='Arial',size=10,bold=(r==tr))
        cell.alignment=Alignment(horizontal='center' if c>1 else 'left')
        cell.border=Border(top=Side(style='thin',color=BLUE)) if r==tr else bd
s['A12']='Ch 4 plan: +5 salvaged drawing items, +5 Tier D items redrawn in house style with the drawing task converted to MC. Decided Aug 12.'
s['A12'].font=Font(name='Arial',size=9,italic=True,color='CC3333')

s2r=14
s.cell(s2r,1,'Usage against Pearson difficulty (unused Tier A+B only)').font=Font(name='Arial',size=11,bold=True,color=BLUE)
for c,h in enumerate(['Chapter','Easy','Moderate','Hard'],1):
    cell=s.cell(s2r+1,c,h); cell.font=hf; cell.fill=hfill; cell.alignment=Alignment(horizontal='center')
for n,ch in enumerate([1,3,4,5,6]):
    r=s2r+2+n; s.cell(r,1,f'Ch {ch}')
    for k,d in enumerate(['Easy','Moderate','Hard']):
        s.cell(r,2+k,f'=COUNTIFS(Master!$B$2:$B${N},{ch},Master!$I$2:$I${N},"No",Master!$K$2:$K${N},"{d}",Master!$S$2:$S${N},"A")'
                     f'+COUNTIFS(Master!$B$2:$B${N},{ch},Master!$I$2:$I${N},"No",Master!$K$2:$K${N},"{d}",Master!$S$2:$S${N},"B")')
    for c in range(1,5):
        s.cell(r,c).font=bf; s.cell(r,c).alignment=Alignment(horizontal='center' if c>1 else 'left'); s.cell(r,c).border=bd

# ---------------- Legend ----------------
lg=wb.create_sheet('Legend')
lg.column_dimensions['A'].width=20; lg.column_dimensions['B'].width=104
lg['A1']='ECON 003 — Master Question Bank'; lg['A1'].font=Font(name='Arial',size=14,bold=True,color=BLUE)
rows=[
 ('','' ),
 ('SOURCE','Pearson MyLab exports QB1&3, QB4&5, QB6 (.xlsx metadata + .pdf full text), merged Aug 12 2026. 323 items, Ch 1/3/4/5/6.'),
 ('',''),
 ('UID','E3-C{chapter}-{type}{nn}. Stable primary key — use this everywhere from now on. RQ=Review Question, CQ=Concept Question, CC=Concept Check, TP=Text Problem.'),
 ('WHY RE-LABELLED','Pearson restarts "Review Question N" and "Text Problem N" numbering in every chapter, so 27 native ID strings point at two different items. Those rows are marked ID Collision = Yes. Never key off the Pearson ID alone.'),
 ('Pearson ID','The native string, kept for traceability back to MyLab.'),
 ('Variant','algo = Pearson regenerates the numbers per student; static = fixed.'),
 ('',''),
 ('Used / Used In','Yes = this item already appeared in a homework or quiz. Used In names which. Resolved by matching question text where the native ID was ambiguous.'),
 ('',''),
 ('TIER','How much work the item needs before it can go on the exam.'),
 ('  A  drop-in','Single part, one correct answer, 4+ written options. Paste straight into Canvas.'),
 ('  B  mechanical','Convertible with no judgment: a single dropdown whose choices become the options; a numeric-entry item needing 4 numeric distractors; an item with only 2-3 options.'),
 ('  C  judgment','Needs a real rewrite: collapse a 2- or 3-part cloze into combination options, or turn a check-all-that-apply into a single-answer item.'),
 ('  D  skip','4+ parts, drawing-tool items, table construction. The scaffolding is what the item measures; converting destroys it. Cheaper to write a fresh question.'),
 ('',''),
 ('Salvage','A Tier D drawing-tool item that also carries a self-contained 4-option MC. Keep the rendered graph, delete the drawing instruction, keep the MC. 16 of these exist and Ch 4 needs them.'),
 ('Src Pages','Bank file and page range — render these to see the figure, or to check the text.'),
 ('Verify Text','Pearson%s print layout clips option text where a side-column graph sits beside it, and pdftotext bleeds axis numbers into the text. Confirmed on one item; eye-check the render for anything flagged Figure = Yes before using its wording.' % chr(39)),
 ('Parts','Number of separately-marked answer parts in the Pearson original.'),
 ('Format','mc = lettered options. cloze = dropdown blanks. cloze+mc = both.'),
 ('Multi-Select','Check-all-that-apply. Canvas scores these differently — must become single-answer.'),
 ('Figure','Yes = this item needs its graph. The graphs are VECTOR, not embedded rasters — pdfimages returns blank canvases. Render the page at 150 dpi and crop instead; Src Pages gives you the page. Likely = one signal only, eyeball it.'),
 ('',''),
 ('NOT IN THIS BANK','HW2 items Evidence 4.0.1 and Evidence 5.0.1 are Evidence-Based Economics questions that Pearson omitted from the export. Q3 #11-15 are Ch 7 and out of midterm scope.'),
 ('CHAPTER 6 NOTE','Sections 6.5, 6.6 and 6.A have titles that read like Chapter 7 (long run, competitive equilibrium, differing cost structures). Pearson numbers them 6.x. They are Chapter 6.'),
]
for r,(a,b) in enumerate(rows,3):
    lg.cell(r,1,a).font=Font(name='Arial',size=10,bold=not a.startswith('  ') and a!='')
    lg.cell(r,1).alignment=Alignment(vertical='top')
    lg.cell(r,2,b).font=Font(name='Arial',size=10)
    lg.cell(r,2).alignment=Alignment(vertical='top',wrap_text=True)
    if b: lg.row_dimensions[r].height=max(14,14*(len(b)//100+1))

# ---------------- Selection sheet ----------------
sel=[i for i in m if i.get('sel')]
sel.sort(key=lambda i:(i['ch'],{'P':0,'R':1}[i['sel']],i['qtype2'],i['uid']))
sh=wb.create_sheet('Selection'); wb.move_sheet('Selection',offset=-1)
sh['A1']='ECON 003 Midterm — selected pool (120 of 150; 30 originals still to write)'
sh['A1'].font=Font(name='Arial',size=13,bold=True,color=BLUE)
SC=[('UID',14),('Ch',5),('Bucket',9),('Question Type',13),('Difficulty Tier',13),
    ('Pearson Difficulty',11),('Conversion',11),('Figure?',9),('Src Pages',15),('Action required',56),('Stem',86)]
for c,(h,w) in enumerate(SC,1):
    cell=sh.cell(3,c,h); cell.font=hf; cell.fill=hfill
    cell.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
    sh.column_dimensions[get_column_letter(c)].width=w
sh.row_dimensions[3].height=30
BK={'P':'Pearson-new','R':'Reused'}
TF={'A':PatternFill('solid',fgColor='D9EAD3'),'B':PatternFill('solid',fgColor='FFF2CC'),
    'S':PatternFill('solid',fgColor='DEEAF6'),'C':PatternFill('solid',fgColor='FCE5CD'),
    'D':PatternFill('solid',fgColor='F4CCCC')}
for r,i in enumerate(sel,4):
    conv='S' if i.get('salvage')=='Yes' else i['tier']
    if conv=='A':   act='Use as written.'
    elif conv=='B': act=i['why'][0].upper()+i['why'][1:]+'.'
    elif conv=='S': act='Delete the drawing instruction, keep the MC, supply the figure.'
    elif conv=='C': act=i['why'][0].upper()+i['why'][1:]+'.'
    else:           act='Redraw the figure in house style; convert the drawing task into an MC on the result.'
    if i['sel']=='R': act='Swap all numbers and recompute the key; expand to 5 options. '+act
    if i['qtype2']=='G-fig': act+=' FIGURE: render Src Pages, redraw in house style.'
    if i.get('trunc'): act+=' VERIFY wording against the render — text may be clipped.'
    row=[i['uid'],i['ch'],BK[i['sel']],i['qtype2'],i['dtier'],i['difficulty'],conv,
         'Yes' if i['qtype2']=='G-fig' else '',f"{i['bank']} p{i['pages'][0]}-{i['pages'][-1]}",act,cl(i['stem'])]
    for c,v in enumerate(row,1):
        cell=sh.cell(r,c,v); cell.font=bf; cell.border=bd
        cell.alignment=Alignment(vertical='top',wrap_text=(c>=10),
            horizontal='center' if c in (2,3,5,6,7,8) else 'left')
    sh.cell(r,7).fill=TF[conv]
    sh.row_dimensions[r].height=30
sh.freeze_panes='A4'; sh.auto_filter.ref=f'A3:K{len(sel)+3}'

out='/home/claude/qb/ECON003_Master_Question_Bank.xlsx'
wb.save(out); print('saved',out,len(m),'rows')
