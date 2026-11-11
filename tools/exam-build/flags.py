import re
TERM=re.compile(r"""[.?!:;"')\]]$""")
FUNC={'is','of','the','a','an','and','or','to','in','for','that','while','with','from',
      'at','by','on','as','but','than','their','its','would','will','be','are','was','not','if'}
def truncated(t):
    t=(t or '').strip()
    if len(t)<=55 or TERM.search(t): return False
    last=re.sub(r'[^A-Za-z]','',t.split()[-1]).lower() if t.split() else ''
    return len(last)<=3 or last in FUNC          # cut mid-word or mid-phrase
TEXTBOOK=re.compile(r'(as a preview of upcoming|in the next chapter|in a later chapter|as we will see|recall from the|evidence-based economics|in this chapter|your textbook)', re.I)
