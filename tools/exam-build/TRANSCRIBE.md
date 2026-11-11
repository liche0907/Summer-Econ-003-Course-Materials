# Build spec — ECON 003 final, post-midterm pool

You are producing **exam-ready items** from publisher source, working **by reading rendered page
images** rather than by extracting text. Each item gets two blocks: a faithful transcription of what is
printed, and the final version that will go on the exam. The goal is a draft complete enough that the
instructor reviews once and revises once — so the final block must be genuinely finished, not a sketch.
The PDF's text layer is unreliable: it interleaves figure axis labels into the sentence, joins words,
flattens tables into a single line, and silently truncates long options at the page margin. **Trust
only what you can see in the image.**

## What you get
A manifest JSON: one record per item with `label`, `pdf_item_number` (the item's printed number on the
page — find that number to locate the item), `sec`, `tier`, `images` (page PNGs, relative to the
working directory), `extracted_key` (what my text-layer extractor recovered — **verify it against the
image**, it is a hypothesis not a fact), and `has_proposed_rewrite`.

Read every page image you are given. An item may span two pages.

## How the answer is marked on the page
- **Multiple choice** — the correct option has a **filled blue radio button** and its text is **bold**.
- **Dropdown** — under a `(1)`, `(2)` marker, the chosen value is the one with the filled radio / bold.
- **Numeric or short answer** — the value is already **typed into the answer box** inside the sentence.
  That is the answer, not part of the question. Transcribe the sentence with `______` where the box is
  and record the value in `answer_boxes`.
- Some items are **check-all-that-apply** — several options filled. Record all of them.

## Output — one JSON array, written to the file named in your task
```json
[{
  "label": "<copy from manifest>",
  "pdf_item_number": 12,
  "stem": ["clean paragraph", "second paragraph"],
  "tables": [{"caption":"", "header":["Quantity","Total Revenue"], "rows":[["0","$0"],["1","$10,000"]]}],
  "figure": null,
  "options": [["A","full option text"],["B","..."]],
  "key": "full text of the correct option, or the filled value(s)",
  "answer_boxes": [{"blank":"(1)","answer":"Producer A"}],
  "issues": [{"type":"clipped","where":"option A","text":"…as read on the page","note":"what to fetch"}],

  "final": {
    "stem": ["the exam-ready stem, self-contained"],
    "tables": [{"caption":"","header":[],"rows":[]}],
    "figure": null,
    "options": [["A","..."],["B","..."],["C","..."],["D","..."],["E","..."]],
    "key": "full text of the correct option",
    "distractors": [["B","which specific student error this catches"]],
    "tier": "routine | challenging",
    "changed": "what you changed from the printed item and why, one or two sentences",
    "review": "" 
  }
}]
```

### stem
Clean, readable prose, as a human would read it off the page. Fix the extraction's damage: rejoin
words broken by the export, remove figure axis labels and table cells that do not belong in the
sentence, and drop the publisher's own instruction boilerplate (`(Enter your answer as a whole
number.)`, `(Round your response to two decimal places.)`) — that is answer-format instruction, not
question content. **Do not paraphrase and do not improve the economics.** If a sentence reads wrong on
the page, transcribe it as printed and file an `issue`.

### tables
Every table gets a real structured table. Never leave numbers stranded in the stem. If a table has no
caption on the page, use `""`.

### figure
`null` if the item does not depend on a picture. Otherwise:
```json
"figure": {
  "kind": "supply-demand | ppc | cost-curves | monopoly | externality | tax-wedge | price-control | other",
  "title": "Market for Video Game Consoles",
  "x_label": "Quantity", "y_label": "Price ($)",
  "x_range": [0, 9], "y_range": [0, 1000],
  "series": [
    {"name":"Demand","type":"step|line|curve","points":[[0,900],[1,900],[1,800]],
     "equation":"P = 44 - 3Q", "label_at":[9,100]}
  ],
  "annotations": [{"kind":"point|vline|hline|shade|arrow|text","at":[5,500],"text":"e1"}],
  "reproduce": "one sentence: which printed numbers this figure must reproduce",
  "confidence": "exact | approximate",
  "read_off": "what the student must read off it to answer"
}
```
**The figure will be drawn from this spec, so it must be numerically complete.** Give the actual
coordinates, intercepts and intersections you can see on the page — read them off the gridlines and
axis ticks. If a curve's exact functional form is not recoverable, give the points you *can* read and
set `"confidence":"approximate"`, then say in `reproduce` which printed values the drawing must hit.
For a step function (discrete buyers/sellers) give the full step point list.

### issues — this is the point of the exercise
File one for anything a human must resolve. Types:
- `clipped` — the option or sentence is **cut off at the right margin of the page**. This is a real
  defect in the export and it is common. Quote what is visible and say what is evidently missing.
- `missing_word` — the sentence has a word plainly dropped or two words run together in a way that
  changes the reading.
- `garbled` — text is scrambled, out of order, or a fragment appears where it does not belong.
- `ambiguous` — two options are defensible, the key looks wrong, or the item cannot be answered from
  what is printed.
- `key_mismatch` — the filled radio on the page disagrees with `extracted_key`. **Always report this.**
- `figure_unreadable` — the item needs a figure but the page does not give enough numbers to redraw it.

Each issue must be actionable: `note` says exactly what to fetch from Pearson or what to check.

## Rules
- Transcribe **all** options, in full, in the printed order.
- Keep the publisher's wording. This is transcription, not editing. A separate pass rewrites items.
- Do not invent numbers. If you cannot read a value, file a `figure_unreadable` or `garbled` issue.
- Work item by item and finish every item in your manifest.


---

# The `final` block — the exam-ready item

This is the deliverable. Write it for every item, including ones that came through clean.

## Hard rules (these are the course's standing rules, not suggestions)
1. **Five options** on anything you touch; an item passing through unchanged keeps its native count.
   Minimum 4. **Plausibility beats count — never invent filler.** If a fifth plausible distractor does
   not exist, keep four and say so in `changed`.
2. **No "All of the above", "Both A and B", "None of the other options"** — Canvas shuffles the
   options, so these break. If the printed key is "all of the above", rewrite the item so one option is
   the single best answer.
3. **Key by answer TEXT**, never by letter.
4. **Numeric options must not give away the key by frequency.** Pattern: two options carry the key's
   value in different framings, two carry one distractor's value, one stands alone — **and the lone
   value must be a distractor, never the key.** Only where options are numeric.
5. **No quadratics** unless solved by substituting integers.
6. **Canvas has no plotting tool.** A "draw this" task becomes read-off-the-graph or
   choose-the-correct-description.
7. **Every item must be self-contained.** Canvas draws items at random, so an item may not say "refer
   to the previous question" or depend on a neighbouring item's table.
8. **Every distractor must be diagnosable** — name the specific student error it catches in
   `distractors`. Wrong curve, wrong side of the wedge, average instead of marginal, MC instead of ATC,
   correct arithmetic applied to the wrong model.
9. **Multi-part items are SPLIT, not trimmed.** A printed item with several dropdowns, several
   numeric fills, or two option blocks becomes **two or three separate exam items**, each
   self-contained and each with its own five options and its own key. Emit them as separate records
   with labels `<label> a`, `<label> b`, `<label> c`. Drop a part only if it is out of scope or tests
   nothing (pure answer-format boilerplate), and say so in `changed`. Splitting is how thin chapters
   get supply, so do not collapse a genuinely two-question item into one.
10. **Replicate the item's REAL form, not the text extraction.** Look at the page. If the printed item
   is a table plus a question, your final is a table plus a question. If it is a figure plus a
   question, it is a figure plus a question. The extracted text is damaged evidence, not the item —
   where it disagrees with the page, the page wins, and where the printed item is itself defective,
   fix it and say what you fixed.

## Course scope — never go outside it
Chapters 7, 8, 9 in full **except §7.2**; Chapter 10 only §10.1.3, §10.2, §10.3; Chapter 12 only
§12.1–12.5 and §12.7.
**Never lectured, so never assume it:** §7.2 (allocating output across a firm's own plants — the deck
cut all 12 slides); §10.1.2 (progressive/regressive structure, average vs marginal tax rate, bracket
arithmetic); §12.6 (price discrimination).
**Tax incidence was NOT taught in Chapter 9.** Never write "as you saw in Chapter 9" about incidence.
Chapter 7 is the safe callback for consumer/producer surplus, deadweight loss and price controls.

## Publisher defects — do not inherit
- Exhibits 10.13/10.14 are not ceteris paribus though their notes claim they are; the correct post-tax
  quantity is **1,750**, not 2,000.
- Exhibit 12.11's description puts MR = MC at 560 — it is **500**.
- Exhibit 12.5's Marginal Revenue column is the **derivative**, not the difference of its own TR
  column. Differencing across 100-unit steps gives the midpoint value. Be explicit about which
  convention an item wants.
- A publisher key has already been found economically wrong in this course. **Verify every key
  yourself** by working the economics.

## `review`
Leave `""` when you are confident. Otherwise one sentence saying what the instructor must decide —
the key is arguable, the economics is contestable, you changed what the item asks, or a figure spec is
approximate. Be sparing: flagging everything is the same as flagging nothing.

## Figures in `final`
If the final item needs a picture, give a complete `figure` spec — it will be **drawn** from your
numbers, so it must be numerically closed. House style is fixed (heavy black line, white ground, no
gridlines unless a value must be read off the axis, labels outside the plot right), so give geometry
and labels, not styling.
