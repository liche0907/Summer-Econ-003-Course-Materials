# Exam-build pipeline

These scripts built the midterm and final question pools for ECON 003 and exported them to Canvas.

**What's missing:** the question data (`rev.json`, `batch2.js`, `originals.js`, the pool CSVs and figures). It's withheld because most items come from the publisher's test bank and the pools hold answer keys. So the scripts are here to read, not to run. `MANIFEST.md` and `HANDOFF.md` describe how the pieces fit together.

## Stages

| Stage | Scripts | What it does |
|---|---|---|
| 1. Extract | `reader.py`, `segment.py`, `extract.py`, `extract_final.py`, `clean.py`, `dots.py`, `choices.py` | Parse MyLab printouts into items: stem, options, key, figure flag. `TRANSCRIBE.md` is the transcription spec |
| 2. Classify | `qtype.py`, `classify*.py`, `flags.py`, `pattern2.py`, `rescan.py` | Tag question type (concept, calculation, graph); flag drawing-tool items (Canvas has none) and cross-chapter references |
| 3. Tier and select | `tiers.py`, `plan.py`, `select*.py`, `mkxlsx.py`, `mkcsv6.py` | Assign routine/challenging tiers and fill each chapter's quota, weighted by lecture time, from reused → publisher-bank → original items. `mkxlsx.py` builds the master bank workbook |
| 4. Time | `timecost.py` | Estimate each item's working time and simulate 20,000 random 50-item draws so a full exam stays at 70–80 minutes |
| 5. Review documents | `build*.py`, `buildrev.py`, `mkdoc.js`, `mkpool10.js`, `mkbank.js`, `mkdropped.js`, `render_items.py`, `house_rules_rework.md` | Produce item-by-item review documents for instructor sign-off |
| 6. Figures | `figlib.py`, `figlib2.py`, `panel.py` | House-style economics diagrams: curves, read-off lines, shaded surplus areas |
| 7. Export | `mkqti.js`, `mkqti_final.js`, `mkbanks.js`, `mkquiz_one.py`, `merge_one.py`, `export.py` | Write Canvas QTI packages, one item bank per chapter × tier |
| 8. Audit | `audit_final*.py`, `selfaudit.py`, `verify_final.py` | Structural checks: one key per item, no duplicate stems, banks deep enough for the draw |
| Study guides | `mksg.js`, `mksg2.js`, `mkfsg.js` | Build the midterm and final study guides in `exams/study-guides` |
