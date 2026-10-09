# Source review of generated baseline code
Status: generated_unexecuted. No import, syntax compilation, unit test, inference or scoring run was performed.

## Derivation-to-code mapping
| Mathematical object | Code |
|---|---|
| M01 group Bayes decision boundary | inference.py whole-continuation log-probability; no first-token shortcut or asserted joint optimization |
| M02/M03 native group intersection | scoring.py cb_hard uses exactly four retained rows, reports incorrect-row counts |
| M04 consistency counterexample | No self-training/consensus candidate implemented; covered mechanism remains a comparator lead |
| M05 existential score limitation | official.py preserves original SAQ functions; raw responses and fixed generation caps retained |
| M06 channel ambiguity | inference.py records raw response, strict and official extraction, token IDs and label log probabilities |
| M07 dependent templates | prepare.py retains global source ID for every native variant; statistical callback remains unimplemented/pending |
| M08 robust objective | No group-DRO training implemented; no legitimate development evidence |

## Interfaces and static decisions
assets.py resolves metadata to immutable model/data identities, checks pinned upstream Git blobs, collects SHA256 acquisition receipts and never loads remote code. prepare.py validates all four native tasks and writes immutable unit files and coverage. inference.py accepts no oracle labels, uses one actual device, refuses truncation, records observed hardware and every attempt, and resumes only matching manifests. scoring.py calls acquired official BLEnD functions; its separate SAQ parity command executes the original module live on the same predictions. census.py preserves failure and simple-alternative records without inventing affected-mechanism labels or gate episodes.

Static source review corrected an initially expensive per-MCQ-row shard hash: the shard is now hashed once. Actual forward-call and processed-token accounting was added to expose the higher cost of likelihood selection. SAQ census compares the two fixed native prompts, not a fake likelihood method for open answers.

## Material unresolved issues
- CB extraction has no verified official parser parity yet; the mathematical endpoint matches the primary description but scientific receipt remains unqualified.
- Current BLEnD scorer dependencies include resource fetches not version-pinned upstream. Local must resolve them and compare unchanged official code, not infer faithfulness from AST equivalence.
- Native loader schemas are source-inspected, not executed. Unexpected IDs/columns/order/cardinality are hard failures; repairing them requires upstream evidence and a new prepared manifest.
- Single-device bfloat16 feasibility is conditional. No VRAM, time or spend estimate was validated.
- Whole-label continuation boundary must remain prefix-stable for the actual tokenizer. Any mismatch stops that arm.
- Full native MCQ generation is potentially expensive. A truncated queue is incomplete, not full-benchmark evidence.
- The two required model classes belong to different families; within-model arm comparisons are meaningful, cross-size causality is not.
- No trusted clustered statistical callback, novel selected method, training routine or candidate ablation matrix is approved. These cannot be replaced by stored flags or a skeleton.

## Additional source repair: outcome provenance and parity paths
Reviewed against main e81d4d8c3abb724e4a1970a736f082e3f282b9eb. Status remains generated_unexecuted.

- census.py previously authenticated prediction bytes but read mutable outcomes.jsonl without comparing its recorded hash. It now compares both score receipts to actual outcomes, prepared inputs, manifests and task/model/arm identity, and retains outcome hashes in the census summary.
- parity_saq previously changed cwd with relative asset/output/run paths from the runbook. Those paths would then resolve under the scorer cwd. It now resolves all caller paths first and restores cwd/sys.path in finally on success or failure.
- score.json now binds generated CSV artifacts. SAQ parity requires exactly the expected native cell CSV set and hashes, as well as manifest/prepared/outcome bindings and task/model/arm identity.
- Live original imports must originate from the pinned acquired exact_match.py, evaluation_utils.py and utils.py. Their original Git blobs are checked before import; module paths are checked after import. The two original scorer files were re-read at BLEnD 7b9c131719e7fe5f9bed0f8b855532d613cc9f2b; hashes matched the saved lock. Explicit relative Indic resource paths in exact_match.py substantiate the cwd requirement.
- Parity rechecks actual declared resource file hashes. These checks authenticate inputs, not scorer equivalence or research soundness. Package/resource completeness and the live original scorer remain Local obligations.

No import, compile, test or scorer execution was performed. Local must qualify this child source revision before producing evidence. Existing run directories must stay pinned to their old source; do not rewrite old manifests or add CSV hash fields retrospectively. The unchanged scientific boundaries (CB parity, SAQ resources, full native coverage, hardware feasibility, legitimate development/confirmation and no admitted novel methods) still apply.

## 2026-10-09: whole-label memory, probability trace and native source audit

Reviewed original inference/io/CLI/scoring/census and source contracts at main
31814655e85d484144696bf2a24acfbf50abbfc2. This is a baseline evidence-tool repair,
not selected candidate implementation.

- inference.py: whole-label log-softmax now uses exactly P−1...P+K−2 logits,
  predicts all K canonical label tokens and retains prefix-token identity. Full
  prompt logits still exist, but float32 probability intermediates are O(KV).
  Teacher forcing sets use_cache=False and releases the temporary tensors.
- Each actual continuation gets its own context check. No truncation, first-token
  shortcut, length normalization, new precision or test-dependent setting.
- Finite label scores also produce stable normalized label_probabilities.
  The legal-prefix-event semantics is explicit; argmax and tie order retain the
  whole-label rule. These probabilities are not calibrated cultural truth.
- io.py rejects NaN/Infinity when writing canonical/atomic JSON. Error records
  retain string diagnostics rather than exporting non-finite scores as valid.
- likelihood_audit.py and CLI audit-likelihood read two complete native runs,
  require matched model/data/config/hardware/tokenization, and retain every
  per-label/output/cost difference. They supply no benchmark scorer, tolerance
  selection, significance test or gate flag.

Static index review links actual code to the math, native tasks, new audit CLI
and Local acceptance entry. Fresh rereads of BLEnD evaluation_utils.py and
exact_match.py match the locked blobs 68d32aee4a5d1b8886ded1cf9e7647f60bbb9c96 and
bb077f8cb7ede207ae1e5a986ac18625f73a9520. Their original SEM exclusions, first
matched annotation, English fallback and language resources remain unchanged.

Planned Local checks: native full-label score and answer agreement at a
predeclared numerical criterion; complete-run integrity; intended context
failure; non-finite rejection; cost/peak evidence; original scorer qualification.
Hardware/model/bfloat16 feasibility and actual old/new parity are unmeasured.
No project import, compile, test, download, inference, scorer or GPU action ran.

