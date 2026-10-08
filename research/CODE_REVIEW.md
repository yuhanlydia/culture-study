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
