import re
_ZW=str.maketrans({'​':' ','‌':' ','‍':'','﻿':'','­':''})
def clean_text(s):
    s=str(s or '').translate(_ZW)
    s=re.sub(r'[ \t]+',' ',s)
    s=re.sub(r' +([.,;:!?%\)\]])',r'\1',s)      # no space before closing punctuation
    s=re.sub(r'([\(\[]) +',r'\1',s)             # no space after opening bracket
    s=re.sub(r'\$ +','$',s)                     # $ 40 -> $40
    s=re.sub(r' +\n','\n',s)
    s=re.sub(r'\n +','\n',s)
    return s.strip()
