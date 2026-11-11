import json,re,csv,collections
A={ (r['bank'],r['order']):r for r in json.load(open('/tmp/audit_final.json')) }
S=json.load(open('/tmp/sel2.json'))
sel=S['sel']
OPT=re.compile(r'^\s*([A-Z])\.\s(.*)$',re.M)

TWO={'it','is','at','in','of','to','be','we','by','or','on','as','an','no','so','do','if','up','he','my','us'}
def zwsp(t):
    """Pearson embeds U+200B as a line-break hint; sometimes between words, sometimes inside one.
    Split when what follows looks like a new word, join otherwise."""
    out=[];i=0
    while True:
        j=t.find('\u200b',i)
        if j<0: out.append(t[i:]); break
        out.append(t[i:j])
        m=re.match(r'[A-Za-z0-9$]+',t[j+1:])
        nxt=m.group(0) if m else ''
        if (not nxt) or len(nxt)>=3 or nxt.lower() in TWO or not t[j+1:j+2].isalpha():
            out.append(' ')
        i=j+1
    return ''.join(out)
def clean(t): return zwsp( re.sub(r'[ \t]+',' ',re.sub(r'\n{3,}','\n\n',t)).strip())
def render(r):
    raw=A[(r['bank'],int(r['order']))]['raw']
    raw=re.sub(r'^\s*\d+\.\s*','',raw.strip())
    m=list(OPT.finditer(raw))
    if m:
        stem=raw[:m[0].start()]; opts=[(x.group(1),clean(x.group(2))) for x in m]
    else:
        stem=raw; opts=[]
    return clean(stem), opts
out=[]
for r in sel:
    stem,opts=render(r)
    out.append(dict(bank=r['bank'],order=int(r['order']),pid=r['pid'],ch=r['ch'],sec=r['sec'],
                    tier=r['pool_tier'],cls=r['cls'],pub=r['pub_diff'],t=r['t'],
                    fig=r['page_has_figure']=='1',practiced=r['practiced_in'],
                    key_kind=r['key_kind'],key_mc=r['key_mc'],key_dd=r['key_dropdown'],
                    key_filled=r['key_filled'],pages=r['pdf_pages'],
                    stem=stem,opts=opts))
out.sort(key=lambda r:(int(r['ch']) if r['ch']!='10' else 10, r['sec'], r['tier'], r['order']))
json.dump(out,open('/tmp/items_sel.json','w'),indent=0)
print('rendered',len(out))
print('needing rework:',sum(1 for r in out if r['cls']!='CLEAN'))
print()
for r in out[:2]:
    print('---',r['pid'],r['sec'],r['tier'],r['cls'],'| KEY:',r['key_mc'][:70] or r['key_dd'][:70] or r['key_filled'][:70])
    print('   STEM:',r['stem'][:220])
    for L,tx in r['opts'][:6]: print('     %s. %s'%(L,tx[:100]))
