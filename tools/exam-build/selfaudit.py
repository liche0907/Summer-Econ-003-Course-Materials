"""Fifth pass — my own read of every item I touched, instead of waiting to be told.

Four classes of my own error, found by reading the questions back:

  1. FALSE "TEXT MISSING". A stem that ends in a connective ("...total cost
     would", "...it is likely that") is not truncated when the options finish
     the sentence. My detector fired on the connective and parked good items.
  2. FALSE "NEEDS REWRITE". Items that are already a single clean multiple
     choice with one key were flagged because the answer block listed more
     than one line.
  3. WRONG DROP. Q19 was dropped as "requires a quadratic". It does not — the
     margin condition is linear (MB = 10 − 2x, MC = 2, so x = 4), exactly the
     structure of Q23, which I kept.
  4. CARRIED THE WRONG LINE. Where part 1's ask ends in a blank rather than a
     question mark, it was carried into part 2 as if it were scenario, so
     part 2 opened with part 1's question.
"""
import json, re

R = {x['n']: x for x in json.load(open('/tmp/rev.json'))}
log = []

BLANKLINE = re.compile(r'_{3,}')


def completes(part):
    """Do the options finish the stem's sentence?"""
    opts = [re.sub(r'^[A-H]\.\s*', '', o).strip() for o in (part.get('opts') or [])]
    if len(opts) < 3:
        return False
    return sum(1 for o in opts if o[:1].islower()) >= len(opts) - 1


# ---- 1. false TEXT MISSING ----
for x in R.values():
    if x['status'] != 'TEXT MISSING':
        continue
    withopt = [p for p in x['parts'] if p.get('opts')]
    if len(withopt) == 1 and completes(withopt[0]) and withopt[0].get('ans'):
        x['status'] = 'NO CHANGE'
        x['why'] = ('Not truncated after all — the stem ends in a connective because the options '
                    'finish the sentence. My truncation check misread that. Use as written.')
        log.append('Q%-4d %-16s TEXT MISSING → NO CHANGE (sentence-completion stem)' % (x['n'], x['uid']))

# ---- 2. false NEEDS REWRITE ----
for x in R.values():
    if x['status'] != 'NEEDS REWRITE':
        continue
    withopt = [p for p in x['parts'] if p.get('opts')]
    blanks = [o for o in x['other'] if re.match(r'^\(\d+\)', o)]
    if len(withopt) == 1 and len(withopt[0]['opts']) >= 4 and withopt[0].get('ans') and not blanks:
        x['status'] = 'NO CHANGE'
        x['why'] = ('Already one clean multiple-choice question — I flagged it because Pearson’s '
                    'answer block runs over several lines, not because the item needs anything.')
        log.append('Q%-4d %-16s NEEDS REWRITE → NO CHANGE (already a single clean MC)' % (x['n'], x['uid']))

# ---- 3. Q19 restored ----
x = R.get(19)
if x and x['status'] == 'DROPPED':
    x['status'] = 'REVISED'
    x['repaired'] = ['dropped in error — the optimum is found from a linear margin condition, no quadratic formula']
    x['why'] = 'Restored. Same structure as Q23: marginal benefit 10 − 2x set against marginal cost $2 gives 4 slices.'
    x['keep'] = []
    x['dropdd'] = True
    x['subs'] = [dict(letter='a', tr=0, draw=False,
                      lead=['Your total benefit from eating x slices of pizza is 10x − x² dollars, and each slice costs $2.',
                            'How many slices do you eat?'],
                      opts=['A. 2', 'B. 3', 'C. 4', 'D. 5', 'E. 8'],
                      ans='C. 4', prov=['src'] * 5)]
    log.append('Q19   E3-C03-CQ04    DROPPED → restored (no quadratic is needed; MB = 10 − 2x, MC = 2)')

# ---- 4. part 1's ask was carried into part 2 ----
for x in R.values():
    parts = x['parts']
    if not parts:
        continue
    p1 = parts[0]['lead']
    askish = {l for l in p1 if BLANKLINE.search(l) or l.rstrip().endswith('?')}
    for grp in ('subs', 'keep'):
        for i, s in enumerate(x.get(grp) or []):
            if i == 0:
                continue
            new = [l for l in s['lead'] if l not in askish]
            if new and new != s['lead']:
                s['lead'] = new
                log.append('Q%-4d %-16s %s[%d] — dropped part 1’s own question from the carried lead'
                           % (x['n'], x['uid'], grp, i))

json.dump(list(R.values()), open('/tmp/rev.json', 'w'))
print('\n'.join(log))
print('---', len(log), 'corrections')
