import re,json,glob
OPTRE=re.compile(r'^\s{0,4}([A-E])[.)]\s+(.*)$')
TAG=re.compile(r'^(ORIGINAL KEY|PROPOSED|STEM|FIGURE|KEY|DISTRACTORS|SRC|FLAG)\s*:?\s*(.*)$')
blocks=[]
for f in sorted(glob.glob('/tmp/proposed_ch*.md')):
    for part in re.split(r'^### ',open(f,encoding='utf-8').read(),flags=re.M)[1:]:
        lines=part.split('\n'); head=lines[0].strip()
        m=re.match(r'(.+?)\s*·\s*([\d.]+)\s*·\s*(\w+)\s*·\s*was:\s*([\w-]+)',head)
        rec=dict(pid=(m.group(1).strip() if m else head),sec=(m.group(2) if m else ''),
                 tier=(m.group(3) if m else ''),cls=(m.group(4) if m else ''),
                 origkey='',stem=[],figure=[],key='',distractors=[],srcline=[],flag=[],opts=[])
        state=None; seen_key=False
        for ln in lines[1:]:
            t=TAG.match(ln)
            if t and not (t.group(1)=='KEY' and state=='opts' and seen_key):
                tag,rest=t.group(1),t.group(2).strip()
                if tag=='ORIGINAL KEY': rec['origkey']=rest; state=None
                elif tag=='PROPOSED': state=None
                elif tag=='STEM': state='stem'; rec['stem'].append(rest)
                elif tag=='FIGURE': state='figure'; rec['figure'].append(rest)
                elif tag=='KEY': rec['key']=rest; seen_key=True; state='key'
                elif tag=='DISTRACTORS': state='dist'; rec['distractors'].append(rest)
                elif tag=='SRC': state='src'; rec['srcline'].append(rest)
                elif tag=='FLAG': state='flag'; rec['flag'].append(rest)
                continue
            o=OPTRE.match(ln)
            if o and state in ('stem','figure','opts') and not seen_key:
                state='opts'; rec['opts'].append([o.group(1),o.group(2).strip()]); continue
            if state=='opts' and rec['opts'] and ln.strip() and not TAG.match(ln):
                rec['opts'][-1][1]+=' '+ln.strip(); continue
            if state=='stem': rec['stem'].append(ln)
            elif state=='figure': rec['figure'].append(ln)
            elif state=='dist': rec['distractors'].append(ln)
            elif state=='src': rec['srcline'].append(ln)
            elif state=='flag': rec['flag'].append(ln)
            elif state=='key' and ln.strip() and not OPTRE.match(ln): rec['key']+=' '+ln.strip()
        j=lambda L:re.sub(r'\s+',' ',' '.join(L)).strip()
        rec['stem']=j(rec['stem']); rec['figure']=j(rec['figure']); rec['key']=j([rec['key']])
        rec['srcline']=j(rec['srcline']); rec['flag']=re.sub(r'\s*-{2,}\s*$','',j(rec['flag'])).strip()
        rec['distractors']=[re.sub(r'\s+',' ',x).strip() for x in
            re.split(r'\n(?=\s{0,4}[A-E]\s*[—.\-])', '\n'.join(rec['distractors'])) if x.strip()]
        rec['opts']=[[L,re.sub(r'\s+',' ',t).strip()] for L,t in rec['opts']]
        blocks.append(rec)
print('parsed',len(blocks))
bad=[(b['pid'],b['sec'],len(b['opts']),bool(b['key'])) for b in blocks if len(b['opts'])<4 or not b['key'] or not b['stem']]
print('incomplete:',bad)
print('REVIEW:',sum(1 for b in blocks if b['flag'].upper().startswith('REVIEW')))
print('opt counts:',sorted({len(b['opts']) for b in blocks}))
long=[(b['pid'],len(b['figure'])) for b in blocks if len(b['figure'])>400]
print('suspiciously long FIGURE fields:',long)
json.dump(blocks,open('/tmp/proposed.json','w'),indent=1)
