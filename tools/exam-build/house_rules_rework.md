# ECON 003 final — item rework rules (binding)

You are converting Pearson MyLab items into Canvas-safe multiple choice for a UCR intro
microeconomics final. Canvas shuffles the options, so anything order-dependent breaks.

## Hard rules
1. **Five options** on anything you touch. Minimum 4. **Plausibility beats count — never invent
   filler.** If a fifth plausible distractor does not exist, keep four and say so.
2. **No "All of the above", "Both A and B", "None of the other options"** — they break under shuffling.
   If the source item's key IS "all of the above", rewrite the item so one option is the single best
   answer, or convert to "Which of the following is NOT…".
3. **Key by answer TEXT, never a letter.** State the key as the full option text.
4. **Numeric option values must not give away the key by frequency.** Where several options are
   numbers, the pattern is: two options carry the key's value in different framings, two carry one
   distractor's value, one stands alone — and **the lone value must be a distractor, never the key**.
   Only applies where the item has numeric options.
5. **No quadratics** unless the item is solved by substituting integers.
6. **Canvas has no plotting tool.** A drawing task becomes a read-off-the-graph or choose-the-correct-
   description item.
7. **Every distractor must be diagnosable** — it should correspond to a specific, nameable student
   error (wrong curve, wrong side of the wedge, average instead of marginal, MC instead of ATC,
   arithmetic right but model wrong). Say which error each distractor catches.

## Conversions
- **Dropdown / cloze (the `(1) … (2) …` format)** → a single multi-blank stem with five options, each
  option supplying the whole combination. This is the previous final's own house style:
  *"If firms are incurring economic losses, we expect firms to ______ the market, causing the market
  ______ curve to shift to the ______."* → `a. enter; demand; left` … Keep blanks to 3 or fewer; if the
  source has 4+ blanks, drop the least diagnostic ones and say which.
- **Numeric / short answer** → MC with five values, following rule 4.
- **Check all that apply** → single-best-answer MC.
- **Clipped option** (the source PDF truncated it mid-word) → rewrite that option fully; keep its
  evident meaning.
- **Multi-part** → split into independent items, each self-contained.

## Figures
If the item depends on a figure or table, the figure must be **redrawn** (matplotlib house style: heavy
black line lw 2.3–2.8, white ground, no gridlines unless a value is read off the axis, labels outside
the plot right, 185–190 dpi). **Do not assume the reader has the publisher's picture.** Either
(a) restate the numbers in the stem as a small table so the item is self-contained, or (b) specify
exactly what the redrawn figure must show. Say which you chose.

## Course scope — do not go outside it
Chapters 7, 8, 9 in full; Chapter 10 only §10.1.3 (tax incidence and deadweight loss), §10.2
(regulation), §10.3 (government failures); Chapter 12 only §12.1–12.5 and §12.7.
**Never lectured, so never assume it:** progressive/regressive tax structure and average-vs-marginal
tax rate (§10.1.2); price discrimination (§12.6); allocating output across a firm's own plants (§7.2).
**Tax incidence was NOT taught in Chapter 9** — never write "as you saw in Chapter 9" about incidence.
Chapter 7 is the safe callback for consumer/producer surplus, deadweight loss and price controls.

## Publisher defects — do not inherit these
- Exhibits 10.13/10.14 are not ceteris paribus though their notes claim they are; the correct
  post-tax quantity is **1,750**, not 2,000.
- Exhibit 12.11's description puts MR = MC at 560 — it is **500**.
- Exhibit 12.5's Marginal Revenue column is the **derivative**, not the difference of its own TR
  column; differencing across 100-unit steps gives the midpoint value. Both conventions appear in the
  wild, so be explicit about which one an item wants.
- Verify the economics yourself. A publisher key has already been found wrong once in this course.

## Output format — one block per item, exactly this shape
```
### <pid> · <sec> · <tier> · was: <cls>
ORIGINAL KEY: <the key as extracted>
PROPOSED:
STEM: <full stem, self-contained>
FIGURE: <none | what the redrawn figure must show>
  A. <option>
  B. <option>
  C. <option>
  D. <option>
  E. <option>
KEY: <full text of the correct option>
DISTRACTORS: <one short line per distractor naming the error it catches>
SRC: <what changed and why, one or two sentences>
FLAG: <REVIEW: reason | none>   ← set REVIEW if the key is arguable, the economics is contestable,
                                   a figure must be drawn, or you had to change what the item asks
```
