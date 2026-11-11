# ECON 003 FINAL — QTI build handoff

Everything needed to build the final's Canvas packages is in this folder. Nothing has to be
reconstructed from conversation. **Exam: Sat Aug 29, 10:00 AM – 1:00 PM Pacific.**

## Build it

    node mkqti_final.js      # -> QTI_IB/  (19 per-bank packages)
    python3 verify_final.py  # structural check

Then zip each bank folder with the manifest at the ZIP ROOT:

    cd QTI_IB && for d in */; do b=${d%/}; (cd "$b" && zip -qrX "../../IB_ZIPS/$b.zip" .); done

## The form that matters

`reference/ECON003_Midterm_QTI_itembank_v1.zip` is the package that actually produced working
**New Quizzes item banks** for the Aug 15 midterm. Match it exactly. Its layout, per bank:

    imsmanifest.xml                    identifier="m_<bank_id>"
    <bank_id>/<bank_id>.xml            <assessment ident="a_<bank_id>"> -> <section ident="root_section">
    <bank_id>/assessment_meta.xml      <quiz> xmlns=http://canvas.instructure.com/xsd/cccv1p0
    web_resources/econ003_final/*.png

Manifest resources in order: the `imsqti_xmlv1p2` resource carrying
`<dependency identifierref="meta_<id>"/>`; the
`associatedcontent/imscc_xmlv1p1/learning-application-resource` meta resource; a `webcontent` resource.

**ONE ZIP PER BANK. Ten separate imports is what was done in August** — `QB/QTI/MT/` holds the ten
extracted zips, timestamped ~7 hours after the container, which is the record of it.

### Forms that do NOT work — already tried and failed Aug 27

| Form | Result |
|---|---|
| `<objectbank>` + `bank_title`, one combined zip | imports as **Classic** question banks (`/courses/<id>/question_banks`), never appears under Item Banks |
| 19 `<assessment>` resources merged into ONE manifest (`merge_one.py`) | **empty item bank** |

`mkquiz_one.py` builds a different thing: one quiz with 19 embedded draw groups
(`<selection_number>`), no item banks at all. One import. Untested in Canvas.

## Data sources

| File | Holds |
|---|---|
| `POOL2.json` | the live post-midterm 120 (final rounds 3-6 + the full manual read) |
| `batch2.js`, `rev.json`, `originals.js` | midterm-material items, same sources the midterm shipped from |
| `seltier.json`, `tieroverride.json` | tier resolution |
| `ECON003_Final_MidtermHalf_Pool_v4.csv` | which 136 midterm items survive, and their re-tiering |
| `figs/`, `fg_q*.png`, `fg_o*.png` | all 35 referenced figures |

`CUT = {115,87,67,56,106,32,28,71,19,24}` is hard-coded in `mkqti_final.js`; the midterm generators
hard-code the same set in four places. Any drop must go in all of them or the builds disagree.

## Invariants the build asserts (do not relax)

- 256 items, 19 banks, 35 figures, 43 image references.
- Every item: >=4 options, exactly one scoring condition, **key is the FIRST option**
  -> **shuffle answers MUST be ON in Canvas.**
- Item `ident="i_<bank_id>_<n>"`, unique across all packages. `title="<uid> <label>"`, plain ASCII.
- Every `$IMS-CC-FILEBASE$` reference resolves inside its own package and is listed in that manifest.

## Banks and draws — 60 items

| Bank | Pool | Draw | Bank | Pool | Draw |
|---|---|---|---|---|---|
| m_ch1_routine | 15 | 2 | p_ch7_routine | 16 | 5 |
| m_ch3_routine | 13 | 3 | p_ch7_challenging | 7 | 2 |
| m_ch3_challenging | 5 | 1 | p_ch8_routine | 20 | 6 |
| m_ch4_routine | 23 | 4 | p_ch8_challenging | 7 | 2 |
| m_ch4_challenging | 10 | 2 | p_ch9_routine | 18 | 5 |
| m_ch5_routine | 24 | 4 | p_ch9_challenging | 11 | 3 |
| m_ch5_challenging | 10 | 2 | p_ch10_routine | 9 | 3 |
| m_ch6_routine | 25 | 4 | p_ch10_challenging | 7 | 2 |
| m_ch6_challenging | 11 | 2 | p_ch12_routine | 16 | 5 |
|  |  |  | p_ch12_challenging | 9 | 3 |

Midterm material 24 · post-midterm 36. Routine 41 · challenging 19.
Ch1 has no challenging bank — its measured discrimination was half of every other chapter.

## Canvas settings

Per `canvas-exam-setup.md` in the project. Differences from the midterm: **time limit 3 h 0 m**
(not 2 h), 19 draw groups (not 10), 60 items (not 50), Aug 29 dates, and accommodations must be
re-entered — they do not carry over. **Due must equal Until.** Points: 60 groups at 1.0 = 60;
do not use 35 to mirror the 35% weight, the category weight handles that.

## If an import produces an empty bank — check BEFORE rebuilding

Four rebuilds were burned on Aug 27 inferring from file structure. Check, in order:

1. `/courses/<id>/content_migrations` -> the migration's **"View Issues"** link. The only place
   Canvas states a real error.
2. `/courses/<id>/question_banks` — content there means an objectbank-form package went in.
3. New Quizzes -> Item Banks -> **both** "Manage Banks" and "Shared with Me". Item banks are owned by
   a **user**, not a course; the midterm's arrived under Shared with Me. Confirm the importing account.

Smallest possible test: `IB_ZIPS/m_ch1_routine.zip` — 6 KB, 15 items, no images. Import that alone
before doing all 19.
