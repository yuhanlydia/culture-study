# Source audit — r001, 2026-10-08
Status: source review; no scientific execution. Exact source identities and acquisition scope are in [sources.lock.json](sources.lock.json). The initial repository contained administrative documents only. No historical scientific results were recovered from it.

## Primary benchmark reading
[CB-PAPER](https://aclanthology.org/2025.acl-long.1247.pdf): ACL 2025 final article; read scientific sections 1–4, relevant results/limitations and Appendix D prompts; not all 39 pages. It distinguishes single-mode and multi-mode questions and reports a substantial aggregate gap. This supports investigating coverage failures, not a causal diagnosis for our 1B/7B models. Its region-option similarity shortcut also motivates simple controls.

[CB-DATA](https://huggingface.co/datasets/kellycyy/CulturalBench): official card/tree and native viewer schema read. Released cardinalities differ from the final paper; the selected release must be named in every report. The guessed author GitHub path returned 404. The leaderboard Space page was accessible, but source-file requests failed in this web tool. Official extraction code is not yet qualified.

[BLEND-PAPER](https://proceedings.neurips.cc/paper_files/paper/2024/file/8eb88844dafefa92a26aaec9f3acad93-Paper-Datasets_and_Benchmarks_Track.pdf): NeurIPS 2024 Datasets and Benchmarks article, scientific sections through limitations read (roughly pp. 1–10); appendices not completely read. Its published human audit concerns GPT-4 failures, not these small models.

[BLEND-CODE](https://github.com/nlee0212/BLEnD/tree/7b9c131719e7fe5f9bed0f8b855532d613cc9f2b): README, evaluator, exact-match functions, evaluation utilities and multiple-choice generation/evaluation read; inference source and relevant utility branches read. Full recursive tree inspected; data files were not downloaded. The current repository contains a 2026 SemEval extension, outside the original benchmark scope selected here.

## Actual source issues, not executed failures
- BLEnD README names a combined MCQ CSV absent from the inspected tree. The complete v1.1 input consists of two shards. Its row count remains unknown until Local census.
- Its inference entry uses `parser.add.argument`; it also refers to an undeclared `args.gpus`. These are static observations, not observed runtime error logs.
- Its MCQ branch in `evaluation/evaluate.py` refers to undefined output-path variables. Our adapter invokes preserved scorer functions instead of that CLI.
- SAQ eligibility follows the actual pinned code: three combined no-answer/not-applicable votes, five idk votes, or no aggregated answer cause exclusion. Preserve this precisely; the paper's prose is not a silent patch.
- SEM-W relies on the first annotation's count and first matching annotation. Annotation order is consequential.
- The official Greek branch selects CLTK `grc`; the original Sundanese and third-party CULNIG matchers differ in token ordering/normalization. Neither discrepancy licenses quietly replacing the official scorer.
- Original multilingual scoring has real lexicon, Java/Spark, spaCy and CLTK resource dependencies. Source reads and an AST bridge do not qualify their behavior.

## Limits and bounded repair
The inspected repositories contain implementations and benchmark assets, but no attributable per-question baseline/strong-alternative output pair for the requested small-model scope was located. This is a reading-scope statement, not a claim that none exists anywhere.

HF revision API, some CSV raw pages and Space source requests failed through the web tool. These are access limitations; they do not establish missing datasets. Local metadata resolution is required before acquisition. BLEnD is pinned to a complete Git commit and every required file's Git blob ID.

Source summaries, mathematical inference and unknowns are separately identified. No paper aggregate has been converted into invented failed episodes, model results, run logs or gate decisions.
