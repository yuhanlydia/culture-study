# Native evaluation contracts
Status: generated_unexecuted qualification design. No scorer PASS.

| Task | Selected input | Primary endpoint | Independent analysis unit |
|---|---|---|---|
| CulturalBench-Easy | Official released test, 1,227 questions | Accuracy over question_idx, one A–D output | question_idx |
| CulturalBench-Hard | Same release, 4,908 rows in 1,227 groups | Fraction of question groups with all four judgments correct | question_idx, never four independent rows |
| BLEnD SAQ | Original 16 cultures; English and available local questions; both inst-4 and pers-3 | Official SEM-B and SEM-W, percentage; average the two prompt scores and report language/culture cells | Shared source ID across cultures/languages/prompts |
| BLEnD MCQ | Both official v1.1 shards, all rows, English | Exact answer_idx equality, country accuracy; retain country and overall denominators | Shared original ID, grouping all distractor variants and cultures |

For BLEnD US/UK do not duplicate identical English and local runs. MCQ variants are not independent observations. For equal-culture summaries, resample global template IDs and recompute the declared macro statistic.

## Inputs, labels and completeness
CB Easy fields: data_idx, question_idx, prompt_question, prompt_option_a/b/c/d, answer, country. Hard: data_idx, question_idx, prompt_question, prompt_option, boolean answer, country. Require unique row IDs, four rows per Hard group, consistent question/country and identical Easy/Hard group sets. Empty option strings must be preserved, not dropped.

BLEnD question CSVs use ID, Question, Translation; prompt CSVs use id, English, Translation. In the actual pinned question-file rows for 14 non-English cultures, Question is local text and Translation is English, contrary to the old paper/README prose. Bind columns from sources.lock.json's saq_input_contract, independently of the prompt-file columns. US/UK retain country-specific Question text in their single English cell. Load actual text and replace only {q}; retain the existing literal country substitution. This supersedes the older inferred question-column convention; full native language/prepared acceptance remains pending. Do not use translated labels, annotation aliases or answer_idx to construct model inputs. MCQ source columns are MCQID, ID, country, prompt, choices, choice_countries, answer_idx. Choices are parsed with JSON, never eval.

Full coverage is an input/receipt requirement. Missing, duplicate or failed model outputs invalidate the completed-run receipt; missing outputs are not excluded from a performance denominator. Non-parsable model answers remain wrong and are separately counted. Do not report subset scores as full native results.

## Scorer interfaces
CB: implement the published group endpoint, but strict first-label extraction is a proposed adapter pending parity with an official implementation/known native predictions. Row accuracy and true/false recall are diagnostic secondary quantities.

BLEnD SAQ: acquire upstream files locally; extract original function definitions without rewriting normalization, exclusions, annotation order, English fallback or language-specific matching. Compare its per-ID and aggregate outputs against the original imported module using the same complete native prediction files. Any mismatch parks all affected SAQ claims. Dependency assets must be pinned and included in the receipt.

BLEnD MCQ: preserve the upstream function and its result parser. Also log strict label parsing; do not switch parser after viewing scores. Our model bridge is independent implementation, not a claim of exact reproduction of the original provider settings.

## Leakage and confirmation
Both inspected releases provide evaluation data, not an established native train/dev allocation suitable for fitting the proposed method. All settings below are fixed prospectively. No test labels for fitting, selecting parameters/prompts, retrieval construction, pseudo-label filtering or culture-neuron discovery. Reading native examples during source audit is recorded; none is described as unseen confirmation.

A second stochastic seed on the same inspected items is not independent item confirmation. Native held-out confirmation and legitimate development resources remain unresolved for a future adaptive method. Do not relabel a test subset as development. This prelude supports baseline qualification and diagnosis, not an ACL efficacy claim.


## Native prompt/view qualification child
The pinned release/source conflict, read scope and source repair are in
[model/NATIVE_EVIDENCE_CONTRACT.md](model/NATIVE_EVIDENCE_CONTRACT.md) and
[sources/NATIVE_VIEW_AUDIT.json](sources/NATIVE_VIEW_AUDIT.json).
Shared culture/template IDs do not certify role/language/support equivalence.
Official averaging of inst-4/pers-3 scores is evaluation aggregation, not pooled inference.
Changed source-lock/prepared identities require the runbook's immutable child acquisition/preparation/run paths.
