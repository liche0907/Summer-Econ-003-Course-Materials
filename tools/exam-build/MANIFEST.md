# What is in this folder — ECON 003 question-bank machine

Restored from `ECON003_QB_source_v*.tar.gz`. Read this before touching anything.
The pool is **150 items**: 125 adapted from Pearson + 25 originals.

---

## LIVE — the six files that ARE the question bank

Everything else in this folder is scaffolding or scratch. If these six survive, the bank survives.

| File | What it holds |
|---|---|
| `rev.json` | **The source of truth for Pearson items.** All 120 source questions with `parts[]`, `subs[]`, `keep[]`, `status`, and provenance (real Pearson ID, bank file, page range). Items NOT present in `batch2.js` are rendered straight from here. |
| `batch2.js` | **Every individually reworked item.** Overrides `rev.json` for the same question number. Carries the rewritten stem, options, key, figure reference and a `src:` line explaining what changed and why. |
| `originals.js` | **The 25 originals** written for this exam, plus 6 rejected ones. `state:'ok'` = in the bank; `state:'drop'` = written and rejected. Each has a `gap:` field saying which hole it fills. |
| `dropped.js` | The rejected originals, rendered into the Not-In-Bank document so nothing vanishes silently. |
| `seltier.json` | Original difficulty tier per item (83 routine / 37 challenging), extracted from the Selection sheet of `ECON003_Master_Question_Bank.xlsx`. |
| `tieroverride.json` | **Instructor tier overrides, keyed by item label.** Beats both `seltier.json` and the tier in `batch2.js`. 42 entries. Changing one line here re-tiers an item. |

### How an item's tier is resolved

`tieroverride.json[label]` → `batch2` item tier → `batch2` question tier → `seltier.json[uid]`

### The CUT set

Hard-coded identically in `mkbank.js`, `mkbanks.js`, `mkreview.js`, `mkqti.js`:

```
{115, 87, 67, 56, 106, 32, 28, 71, 19, 24}
```

**Any drop must be added to all four**, or the builds disagree. This list is the single most
error-prone thing in the folder — the Q101/Q106 mutual-cancellation bug and the Q19/Q24 non-removal
both came from it.

---

## LIVE — generators (run with `node`)

| Script | Output |
|---|---|
| `mkbank.js` | `ECON003_Midterm_Question_Bank_vN.docx` — the pool by section. **Asserts before writing** and refuses to emit on ≠1 key, <4 options, duplicate option, missing figure, no tier, or a shuffle-unsafe option. |
| `mkbanks.js` | `ECON003_Midterm_By_Bank_vN.docx` — the same items grouped into the ten Canvas banks, **key reordered to option A** for fast entry. Also asserts every item lands in exactly one bank. |
| `mkreview.js` | `ECON003_Midterm_To_Review_vN.docx` **plus `_vN.snapshot.json`** — the exact text of every item as sent, so a returned copy can be diffed mechanically. Does not touch his working copy unless `--refresh-working`. |
| `mkdropped.js` | `ECON003_Midterm_Not_In_Bank_vN.docx` |
| `mkqti.js` | `qti_build/` (objectbank form → imports as Classic banks) and `qti_assessment/` (one assessment-form package per bank → New Quizzes Item Bank importer). Zip these by hand. |
| `mksg2.js` | `ECON003_Midterm_Study_Guide_vN.docx` — currently v5, with the two "Watch the wording" boxes. |
| `ver.js` | The versioning helper. `writeVersioned(base, buf, extras)` → next `_vN`. **Nothing is ever overwritten.** |

---

## LIVE — figures

**16 PNGs are referenced by the current pool.** These are the only ones that matter:

```
fg_q31 fg_q42 fg_q44 fg_q52 fg_q63 fg_q72 fg_q75 fg_q85
fg_q102 fg_q104 fg_q105 fg_q120
fg_o442 fg_o511 fg_o554 fg_o623
```

`mkbank.js` fails the build if any is missing, so a missing figure cannot ship silently.

The `fig_qNN.py` scripts regenerate them one item at a time; `figs_orig.py` regenerates the originals'
figures. House style: heavy black line (lw 2.3–2.8), white ground, no gridlines unless a value must be
read off the axis, labels outside the plot right, 185–190 dpi.

The other ~57 PNGs are screenshots, crops of publisher pages, and abandoned drafts. Safe to ignore.

---

## DEAD / SCRATCH — do not build on these

- **`orig.js`** — an earlier originals file, **required by nothing**. Superseded by `originals.js`.
  Do not edit it thinking you are editing the originals.
- **`mksg.js`** — the first study-guide generator. `mksg2.js` is the live one.
- `mkbatch2.js`, `mkclean.js`, `mkcompare.js`, `mkdoc.js`, `mkrework.js` — one-off document builders
  from earlier rounds. Kept for reference; none feed the current build.
- `review_snapshot.json` — an untagged duplicate of `..._To_Review_v1.snapshot.json`.
- The ~40 loose `.py` files (`extract.py`, `classify.py`, `select.py`, `selfaudit.py`, `tiers.py`,
  `repairs.py`, and the rest) are the PDF-extraction and audit pipeline that produced `rev.json` in
  the first place. Useful if a new source bank has to be ingested; irrelevant to editing the pool.
  **Note:** `selfaudit.py` once restored Q19 against an instructor removal. Do not re-run it blind.

---

## Sanity check after restoring

```
node mkbank.js      # must print: assertions passed: 150 items
node mkbanks.js     # must print: 150 items, all placed in one of ten banks
```

If either refuses, something did not survive the round trip. Fix that before writing a question.

---

## POST-MIDTERM ADDITIONS (Aug 25)

| File | What it is |
|---|---|
| `midterm_item_analysis.csv` | Canvas item analysis for the midterm — ~73 students, 149 scored items. Difficulty, discrimination, answer-frequency JSON per item. The evidence base for everything else here. |
| `ECON003_Final_MidtermHalf_Pool_v4.csv` | **THE authoritative midterm-half pool for the final.** 136 items with label, UID, section, chapter, tier, observed p, discrimination, n. Selection v1–v3 have been deleted: v1/v2 were keyed on UID (not unique) and v3 trimmed to 72, which the instructor overruled. |

### Standing rule set Aug 25 — prune for defect, not for coverage ratio

An item leaves the pool because it is broken (not measuring, mis-keyed, answered correctly by
everyone) — never because the pool exceeds a coverage target. The 3× figure in
`exam-midterm-blueprint.md` was a construction budget for writing 150 items in three days, not a
ceiling on a pool that already exists.

### Tier rule for the final's midterm half

**Challenging = hardest 30% of the chapter by observed p; routine = the rest.** Chapter 1 has no
challenging bank at all (measured discrimination 0.216, half of every other chapter) — all 15 of its
items are routine. **Nine banks, not ten.** Draw 17 routine / 7 challenging = 24 of the final's 60.

`tieroverride.json` still holds the MIDTERM tiers. The final's tiers live in the v4 CSV, not in that
file. Do not confuse them.

### Fix applied to `mkqti.js`

Line 98 used to write `title="<uid>"`, so multi-part splits (7a/7b, 23a/23b, 89a/89b/89c and ten
more) shared one Canvas title and the item analysis could not be keyed on it. It now writes
`title="<uid> · <lab>"`. **Verified in a rebuild. Do not revert.**

---

## FINAL BUILD — post-midterm half (Aug 26)

### The keys were never missing

These three banks export in a **different solution format** from the midterm-era ones: no `Answer:`
line, instead the selected option carries a **filled blue radio** and its whole line is set in
**Arial-BoldMT**; dropdown choices are bold; numeric answers are typed into the answer box (also bold,
and already inline in the extracted stem). `finalkeys.py` recovers **259 of 269** keys; the 10 misses
are drawing-tool items whose answer is the drawn object.

Cross-validated against the filled blue disc, an independent vector signal
(`non_stroking_color ≈ (0, 0.46, 1.0)`, ~8 pt): **175 option lines agree, 0 disagreements** on which
option is correct. Bold-without-disc = check-all-that-apply (checkbox, not radio).

**Two bugs to not reintroduce:**
- Side-by-side dropdowns share a text line. Bound the choice-column search at the next `(n)` marker's
  x, or blank (1) comes back empty on every two-blank item.
- **Publisher IDs are NOT unique.** "Review Question 1" exists in both halves of `QB7&8`. Join on
  `(bank, order)` only. Same class of bug as the `mkqti.js` shared-title one.

### Scope, beyond what earlier docs record

- **§7.2 was never lectured** — the Ch 7 deck cut all of Part 2 (the two-plant CEO story). 4 items out.
  `final-exam-scope.md` still says Ch 7 is covered "full"; superseded.
- §10.1.1 / §10.1.2 out (9 items). §12.6 is moot — `QB12.pdf` contains no price-discrimination
  material at all. **§12.7 has zero bank items** though it is lectured and was examined last time.

### Files

| File | What |
|---|---|
| `ECON003_Final_PostMidterm_Audit_v2.csv` | all 269 source items: scope, effort class, recovered key, practice-set tag |
| `ECON003_Final_PostMidterm_Pool_v1.csv` | the 120-item pool — 100 drawn + 20 original slots with `gap:` text |
| `ECON003_Final_PostMidterm_Pool_v1.docx` | the pool for review; each rework proposed under its original |
| `ECON003_Final_PostMidterm_ToReview_v1.docx` | the 12 flagged items + 9 structural checks |
| `gaps.json` | the 20 original briefs |
| `house_rules_rework.md` | the binding rework rules handed to the rework agents |
| `proposed_ch*.md` | the 29 proposed replacements, source form |

Generators: `extract_final.py` → `audit_final.py` → `classify2.py` → `dots.py` → `finalkeys.py` →
`select_v2.py` → `render_items.py` → `parse_proposed.py` → `mkpool.js` / `mkreview2.js`.

**The midterm machine is untouched** — `node mkbank.js` still prints *assertions passed: 150 items*.

### Draw

Ch 7 = 7 · Ch 8 = 8 · Ch 9 = 8 · Ch 10 = 5 · Ch 12 = 8, of 36. 24 routine / 12 challenging.
Sections weighted by **lecture content slides + examinable pages counted twice**, not by publisher
item counts. **19 Canvas draw groups, not 20** — Ch 1 has no challenging bank.

---

## v2 REBUILD FROM PAGE IMAGES (Aug 26) — this supersedes the v1 pool

**The text layer was never trustworthy for these banks.** It joins words across the export's
zero-width spaces, folds figure axis labels into the middle of sentences, and flattens tables into one
run-on line. All 110 source pages were rendered (`pages/`, 150 dpi) and read as images; every item in
the pool was transcribed from the picture.

### Rules that now govern the pool

1. **A wrong or non-unique solution removes the item.** Not a patched key — removal. Nine items went.
   A dropdown, a clipped option, an "all of the above" or a multi-part stem is a *presentation* defect
   and is repaired instead.
2. **Multi-part items are split**, not trimmed. 100 source items → 134 exam items. This is what fixed
   Chapter 10's supply.
3. **Replicate the printed item's real form.** If it is a table plus a question, the final is a table
   plus a question. Do not substitute a numeric problem for a qualitative one.
4. **Figures are drawn, not described** — `figs_final.py`, 13 figures, house style.

### Second wrong publisher key in this course

`CC 10.1.3.1` — asks why incidence is independent of who is taxed; the printed key answers a different
question and asserts full pass-through. Q110 on the midterm was the first. **Verify every key.**

### Files

| File | What |
|---|---|
| `ECON003_Final_PostMidterm_Pool_v2.docx` | the 120-item pool, tables set, figures embedded |
| `ECON003_Final_PostMidterm_ToReview_v2.docx` | Pearson fetch list, the nine removals, judgment calls, reserve |
| `ECON003_Final_PostMidterm_Pool_v2.csv` | machine-readable index |
| `manual_review_log.md` | every decision made from a page image, with the reasoning |
| `originals_all.json` | the 19 originals |
| `figs_final.py` · `figs/` | the figure generators and PNGs — numbers asserted at import |
| `TRANSCRIBE.md` · `house_rules_rework.md` | the binding specs used to build it |
| `/tmp`-staged intermediates rebuilt by | `render_items.py` → `select_v2.py` → `mkpool2.js` / `mkreview3.js` |

### Figure numbers that must keep closing

- Ch 9 hog tax: `D: P = 10 − Q`, `S: P = 0.25 + 0.95Q`, `MSC = S + 2.36` → 5/5, 3.79/6.21, 3.85, 7.36.
- Ch 12 natural monopoly: `D: P = 12 − 0.02Q`, `MC = 2`, `F = 800` → monopoly 250/$7, fair return
  400/$4, marginal-cost 500/$2 with an $800 loss.
- Ch 10 wedge: `D: P = 12 − 0.5Q`, `S: P = 2 + 0.5Q`, $2 tax → Q 10→8, buyers $8, sellers $6,
  revenue $16, DWL $2.

`figs_final.py` asserts all of these at import, so an edit that breaks the arithmetic fails loudly.

**The midterm machine is still untouched — `node mkbank.js` prints "assertions passed: 150 items".**

---

## Post-midterm round 3 — 26 August 2026

Twenty-nine instructions applied. Pool rebuilt, renumbered and re-tiered.

**Live state: `/tmp/POOL2.json` — 120 items, 82 Pearson / 38 original, 79 routine / 41 challenging,
11 tables + 33 figure placements from 22 distinct figures (37% visual), coverage 3.2–3.5× everywhere.
`/tmp/RESERVE2.json` — 50 finished spares.**

### Rebuild order

```
render_items.py → select_v2.py → select_final2.py → rebuild_pool.py
  → fix_round3a.py → apply_r3.py (reads replacements_r3.json)
  → figs_v2.py  (draws figs/, asserts every number at import)
  → node mkpool3.js     -> ECON003_Final_PostMidterm_Pool_v6.docx
  → python3 mkcsv6.py   -> ECON003_Final_PostMidterm_Pool_v6.csv
  → node mkproposal.js  -> ECON003_Final_PostMidterm_Round3_v1.docx  (reads /tmp/instructions.json)
```

`mkpool3.js` and `mkcsv6.py` walk the pool in the same order — chapter → section → routine before
challenging — so the `[n]` in the document and the `n` in the CSV are the same item. Anything that
changes that ordering must change both.

### Rules added this round

10. An item printed with four options keeps four. Never pad to five.
11. No item may reference another ("use the same market as…") — random draw breaks it. Q82 was the
    last one; the stem now carries its own set-up.
12. Every stem must end in a question or an imperative. Q84 and Q101 did not, and neither was
    answerable. Check this mechanically after any edit that touches a stem.
13. Two items drawn from the same table must not have the same answer. Q113 and Q115 both asked for
    the profit-maximising output; Q115 now asks where total revenue peaks.
14. A set-up sentence must not contain another item's answer. Q43 stated the no-trade social surplus
    that Q44 asks for.

### Figures now 22, all asserted

Added: `fg_f_c08_ppc_linear`, `fg_f_o07_ceiling_areas`, `fg_f_o07_entry_shift`,
`fg_f_o07_surplus_areas`, `fg_f_o08_gains_ppc`, `fg_f_o10_incidence_areas`, `fg_f_o10_demand_shift`,
`fg_f_o12_profit_plain`. Retired: `fg_f_o12_profitrect` (shaded the answer), `fg_f_c09_pigou_base`,
`fg_f_c10_inelastic`. Numbers that must keep closing are asserted at import of `figs_v2.py`.

### Files delivered

| File | What |
|---|---|
| `ECON003_Final_PostMidterm_Round3_v1.docx` | **the one to review** — his list item by item, the 38 new/replacement questions in full, the section × difficulty × visual map |
| `ECON003_Final_PostMidterm_Pool_v6.docx` | the whole 120-item pool, tables set, 33 figures embedded |
| `ECON003_Final_PostMidterm_Pool_v6.csv` | machine-readable index, same numbering as the docx |
| `ECON003_Final_Figures_v5.zip` | the 22 figures at 190 dpi |
| `ECON003_QB_source_v12.tar.gz` | everything above plus generators, `/tmp` state and the review log |

**The midterm machine is still untouched — `node mkbank.js` prints "assertions passed: 150 items".**

### What v12 does not carry

`pages/` (17 MB of 150-dpi page renders of the three Pearson PDFs) is excluded to keep the tarball
inside the device transfer limit. Regenerate with `pdftoppm -r 150 -png <bank>.pdf pages/<bank>` before
re-running any of the key-recovery or transcription scripts; nothing else depends on it.

---

## FINAL — 27 August 2026

**`/tmp/POOL2.json` (copied to `POOL2.json`) — 120 items. `audit_final2.py` passes clean.**
120 items · 79 routine / 41 challenging · 82 Pearson / 38 written · 11 tables + 29 figure placements
from 23 distinct figures = 33% visual · coverage 3.0–3.7× in every chapter and tier.

### Rebuild order

```
figs_v2.py                     -> figs/*.png   (numbers asserted at import)
node mkpool7.js                -> ECON003_Final_PostMidterm_Pool_v10.docx
python3 mkcsv6.py              -> ECON003_Final_PostMidterm_Pool_v10.csv
python3 audit_final2.py        -> structural audit + the section/chapter mapping -> /tmp/mapping.json
node mkmap.js                  -> ECON003_Final_PostMidterm_Map_v1.docx
python3 rescan.py              -> overlap scan -> /tmp/rescan.json
```

### Two checks that must run after every edit, not at the end

**`audit_final2.py`** — key exactly once in its own options; 4–5 options, no duplicates, no
"all of the above"; option letters contiguous; no cross-reference to another item; **a stem that
either asks a question or cues a completion**; figure file present; tables not ragged; a printed
four-option item still at four; and no two items in one section sharing an answer.

> The stem test is the one that matters. An earlier version checked only that a stem ended in a full
> stop, and **six items passed while asking nothing at all** — they set out a situation and stopped.
> Two of that class had already been caught by hand. A stem must ASK (a question sentence) or CUE a
> COMPLETION (trailing colon, a blank, or a dangling conjunction); nine legitimate sentence-completion
> items pass on the second test.

**`rescan.py`** — every same-chapter pair scored on stem-vocabulary overlap, **key overlap** and
shared option text; reported when at least two fire. A shared figure is recorded but never on its own
a reason to flag. Five pairs survive and all are deliberate second readings of one table or figure.

### Rules added since round 3

15. An annotation on a figure must not point at the answer, and **both panels of a two-panel figure
    must be marked the same way** — one annotated panel is a tell.
16. A cloze item's blanks must each carry information. Never pair a given word with its own opposite
    in the blank ("small … the ______ fixed cost" hands over the answer).
17. Numbers a student is meant to read off a figure do not belong in the stem.
18. `ticks()` guard scales with tick spacing; a fixed tolerance silently fails on a wide axis.

### Files

| File | What |
|---|---|
| `ECON003_Final_PostMidterm_Pool_v10.docx` / `.csv` | the 120, final |
| `ECON003_Final_PostMidterm_Map_v1.docx` | section × difficulty × visual mapping |
| `ECON003_Final_Figures_v8.zip` | the 23 figures, 190 dpi |
| `ECON003_Final_Study_Guide_v7.docx` / `.pdf` | student-facing |
| `ECON003_QB_source_v13.tar.gz` | this directory, without `pages/` |

**Next: QTI export, then Canvas per `canvas-exam-setup.md` — 19 draw groups, option shuffle on.**
