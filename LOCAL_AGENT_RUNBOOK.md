# Local agent runbook
Status: generated_unexecuted source/design handoff. It has not been installed, imported, tested, scored or run. Only baseline qualification and evidence repair are ready for Local review; no novel method/G01 is approved.

Read README.md, AGENTS.md, LONG_TERM_TASK.md, research/PROGRESS.md, research/workflow-checkpoint.json, research/sources.lock.json, research/NATIVE_CONTRACTS.md, research/EXPERIMENT_DESIGN.md and rounds/r001/WEB_HANDOFF.md before continuing.

## Host and admission
Local is the controller session, not an agent installed on a GPU server. Actual SSH address/user/port, remote project path, GPU/VRAM/count and time/spend allocation are unknown. Discover the user's real project host and resources through the installed Research Autopilot host/native execution harness; do not copy another project's paths. Use native Conda, not containers/services.

The command blocks below are **inner argv for admitted native harness steps**, not permission to bypass the controller. Read the actual installed workflow-harness, local-execution-harness, gpu-host-runtime and native-evaluation modules. Freeze real plans/budgets with the installed schema; this repository contains no invented admission/grant file.

Controller inspection/plan interface from the actual skill:
```bash
python3 "$SKILL_DIR/scripts/run_harness.py" --inspect-host
python3 "$SKILL_DIR/scripts/run_harness.py" "$PLAN_DRAFT" --root "$PROJECT_DIR" --freeze
python3 "$SKILL_DIR/scripts/run_harness.py" "$FROZEN_PLAN" --root "$PROJECT_DIR"
python3 "$SKILL_DIR/scripts/run_harness.py" "$FROZEN_PLAN" --root "$PROJECT_DIR" --execute --approved-plan-digest "$APPROVED_PLAN_DIGEST"
python3 "$SKILL_DIR/scripts/run_harness.py" "$FROZEN_PLAN" --root "$PROJECT_DIR" --status
```
SKILL_DIR, actual project placement, plan files/digests and budgets come from Local observation/controller admission. Do not guess them. For new candidate boundaries use the actual verify_methods.py with --before code / experiment-design / dispatch / verdict and its real project/batch/candidate arguments from installed help. No validator output exists yet.

## Checkout and environments
User-selected source: https://github.com/yuhanlydia/culture-study, literal main, public. Fast-forward only; one integration writer. Read the actual new head before editing and preserve others' changes. Keep large assets, predictions and credentials out of Git.

On the admitted host, let PROJECT_DIR be the actual checkout and use project-relative locations below; these are new local cache choices, not claimed existing remote paths.
```bash
git clone https://github.com/yuhanlydia/culture-study.git culture-study
cd culture-study
git switch main
git pull --ff-only
conda env create -f environment.yml
conda run -n culture-study python -m pip install -e .
conda run -n culture-study python -m pip freeze
```
The proposed Python 3.10 / Torch 2.5.1 / Transformers 4.46.3 pins support the model architecture interfaces; the solve is not verified. Retain actual solver/install logs and full freeze. Conda is native; no Docker/vLLM service. If the env fails, one bounded compatible repair creates a versioned child environment, never a silent rewrite of the comparison.

The original BLEnD requirements pin Transformers 4.40.1, older than the chosen Llama/Qwen interface requirements. Keep a separate original-scorer environment when needed. Provider SDK dependencies are imports for parity, not authorization to call provider APIs:
```bash
conda create -n blend-official python=3.10 pip openjdk=11 -c conda-forge
conda run -n blend-official python -m pip install -r assets/r001-lang-v2/BLEnD/requirements.txt
conda run -n blend-official python -m pip install pyspark==3.3.1
conda run -n blend-official python -m pip install -e . --no-deps
```
Resolve original undeclared imports (e.g. google-generativeai) from source and pin actual versions if needed. Capture compatibility issues; package-install success does not qualify scorer behavior. The main bridge needs requirements-scorer.txt and every resource below before SAQ.

## Exact source binding and acquisition
Sources/versions are in research/sources.lock.json. Core inputs:
- CulturalBench: kellycyy/CulturalBench, selected official CSV release at observed revision prefix 996d62a. Full SHA was not exposed by the Web tool. The binder resolves that exact prefix, writes the full immutable SHA, and rejects another version. Expected 1,227 Easy / 4,908 Hard rows. Do not substitute the final paper's 1,696-question denominator.
- BLEnD: nlee0212/BLEnD @ 7b9c131719e7fe5f9bed0f8b855532d613cc9f2b. Every required original question/prompt/annotation/scorer and both v1.1 MCQ shard has an exact Git blob ID. No SemEval directory or third-party HF alias is loaded.
- Llama 1B: meta-llama/Llama-3.2-1B-Instruct, gated. Use already authorized access; do not ask for or print tokens, accept a license on the user's behalf, or replace with 1.5B. Metadata resolution fixes the exact model revision before acquisition.
- Qwen 7B: Qwen/Qwen2.5-7B-Instruct @ a09a35458c702b33eeacc393d103063234e8bc28. Apache-2.0; scale class is 7B, total card parameters 7.61B. No causal size comparison across different families.
- Direct and label-likelihood baselines are this repository's source-reviewed independent implementations. Closest published mechanisms/source commits remain in research/CLOSEST_WORK.md; they are not qualified optional baselines or newly claimed contributions.

Admitted CPU/data-acquisition steps:
```bash
conda run -n culture-study python -m culture_study bind --out bindings-r001-lang-v2.json
conda run -n culture-study python -m culture_study acquire --assets assets/r001-lang-v2 --bindings bindings-r001-lang-v2.json
conda run -n culture-study python -m culture_study validate-assets --assets assets/r001-lang-v2 --bindings bindings-r001-lang-v2.json
conda run -n culture-study python -m culture_study prepare --assets assets/r001-lang-v2 --bindings bindings-r001-lang-v2.json --out prepared/r001-lang-v2
```
The binder performs metadata resolution only. Acquisition is real local download, never performed by Web. Both MCQ shards total about 156 MB before prepared/log expansion; prepared JSONL and prediction storage can be much larger. Observe disk space and permit full coverage only if actual capacity/budget supports it.

Admitted model-acquisition step:
```bash
conda run -n culture-study python -m culture_study acquire --assets assets/r001-lang-v2 --bindings bindings-r001-lang-v2.json --models
conda run -n culture-study python -m culture_study validate-assets --assets assets/r001-lang-v2 --bindings bindings-r001-lang-v2.json
```
The acquisition receipt hashes weights/config/tokenizers and exact model revisions. Cached loaders use assets/r001-lang-v2/models/llama_1b and assets/r001-lang-v2/models/qwen_7b with local_files_only=True and trust_remote_code=False. No automatic network access at model loading.

## Multilingual official scorer acquisition
```bash
conda run -n culture-study python -m pip install -r requirements-scorer.txt
conda run -n culture-study python -m spacy download en_core_web_sm
git clone https://github.com/setiawanirwan/SUSTEM.git assets/scorer/SUSTEM
git -C assets/scorer/SUSTEM checkout --detach a26a64f4236211f77dd141dab7d899ebda1615e2
git clone https://github.com/anoopkunchukuttan/indic_nlp_library.git assets/scorer/indic_nlp_library
git -C assets/scorer/indic_nlp_library checkout --detach 4cead0ae6c78fe9a19a51ef679f586206df9c476
git clone https://github.com/anoopkunchukuttan/indic_nlp_resources.git assets/scorer/indic_nlp_resources
git -C assets/scorer/indic_nlp_resources checkout --detach 5b4ff17c080db4bc4cfc068deaa794aa87562eed
git clone https://github.com/aznlp-disc/stemmer.git assets/scorer/stemmer
git -C assets/scorer/stemmer rev-parse HEAD
```
The Azerbaijani URL is the real official citation, but GitHub metadata redirects were not resolved by the available Web connector. If clone resolves, record its actual owner/commit and detach there before scoring. If it does not, park Azerbaijani SAQ and investigate the original source; do not replace the algorithm or silently omit that culture from a full result.

Retain SUSTEM's SundaRootWordVer20220216.txt and source/license. Its current pinned implementation resolves its lexicon relative to the module. Original scorer import still expects a SUSTEM package parent on PYTHONPATH. For Azerbaijani, inspect the actual module's word.txt/suffix.txt resolution and put exact copied/hash-verified lexicons in the observed original scorer cwd. Inspect before choosing cwd.

Spanish and Amharic use Spark NLP 5.3.3 / PySpark 3.3.1 pretrained lemma/es and lemma/am. Greek uses official CLTK grc assets. These pretrained resource versions are not pinned by the original source. Native scorer startup may fetch them; make this an explicit admitted setup step, capture URLs/cache paths/revisions and SHA256 of every resource, then replay offline where supported. Do not report full SAQ if a resource is missing. Korean needs Java/Okt assets; English uses the actual spaCy model version; other language libraries must retain the source-pinned versions and their resource files.

Create scorer-dependencies.json from configs/scorer-dependencies.template.json with status=locally_bound, **actual absolute local paths**, installed package/source versions and exhaustive resource file hashes. Set resolved_git_revisions using the four directory-key names. Each pretrained_assets value must contain its observed version and a nonempty files list, all listed in resource_files with SHA256. Null template entries are blockers. This is an input inventory, not a scientific PASS or dispatch grant. Original code expects indic_nlp_library and indic_nlp_resources in its cwd; use the observed native layout or verified symlinks and record them. Both environments must read the identical lexicons/pretrained assets for parity.

## Native preparation acceptance
prepared/r001-lang-v2/coverage.json must show both original CB sets with matching group IDs, exactly four Hard rows per group, original 500 shared BLEnD templates, all 16 cultures, all available English/local cells, both official SAQ prompts, both complete v1.1 MCQ shards and every native MCQID without duplicates. Inspect actual MCQ rows/counts; never substitute the original paper's historical MCQ count.

Any schema/ID/order mismatch stops preparation. Preserve the failing log/partial directory, inspect the pinned native file, make an evidence-supported child adapter and use a new prepared directory. Do not edit data/labels or waive cardinality assertions to make the run pass.

## Complete inference, scoring and logs
All 14 inference runs from research/EXPERIMENT_DESIGN.md must be dispatched sequentially in the actual admitted GPU queue. Exact argv for each categorical cell, replacing MODEL with llama_1b or qwen_7b, TASK with cb_easy/cb_hard/blend_mcq, ARM with direct/label_likelihood and DEVICE with the actual allocated single device:
```bash
conda run -n culture-study python -m culture_study run --assets assets/r001-lang-v2 --bindings bindings-r001-lang-v2.json --prepared prepared/r001-lang-v2 --model "$MODEL" --task "$TASK" --arm "$ARM" --device "$DEVICE" --out "runs/r001-lang-v2/$MODEL/$TASK/$ARM"
conda run -n culture-study python -m culture_study score --assets assets/r001-lang-v2 --prepared prepared/r001-lang-v2 --run "runs/r001-lang-v2/$MODEL/$TASK/$ARM" --out "runs/r001-lang-v2/$MODEL/$TASK/$ARM-score"
```
These named substitutions enumerate exactly 12 categorical runs, not optional cherry-picked choices. No assumed cuda:0/GPU host is recorded as an observed resource.

For each of the two model keys:
```bash
conda run -n culture-study python -m culture_study run --assets assets/r001-lang-v2 --bindings bindings-r001-lang-v2.json --prepared prepared/r001-lang-v2 --model "$MODEL" --task blend_saq --arm direct --device "$DEVICE" --out "runs/r001-lang-v2/$MODEL/blend_saq/direct"
conda run -n culture-study python -m culture_study score --assets assets/r001-lang-v2 --prepared prepared/r001-lang-v2 --run "runs/r001-lang-v2/$MODEL/blend_saq/direct" --dependencies scorer-dependencies.json --out "runs/r001-lang-v2/$MODEL/blend_saq/direct-score"
conda run -n blend-official python -m culture_study parity-saq --assets assets/r001-lang-v2 --prepared prepared/r001-lang-v2 --run "runs/r001-lang-v2/$MODEL/blend_saq/direct" --bridge-scores "runs/r001-lang-v2/$MODEL/blend_saq/direct-score" --dependencies scorer-dependencies.json --out "runs/r001-lang-v2/$MODEL/blend_saq/parity"
```
Original scorer imports must succeed in the separate environment before this live comparison; the exact functions, exclusions, normalization, first-match order, aliases and same native predictions are checked. A parity exception means no qualification. CB requires a real official/verified faithful extraction comparison, still unresolved; do not treat the source-defined group grader as fully qualified.

Run logs: manifest.json (model/input/code/hardware), predictions.jsonl (raw output, strict/native parser, token scores, native IDs, timings, forward calls, observed memory, every attempt), complete.json (full coverage/completion only). Score logs: score.json, outcomes.jsonl, official stdout log and SAQ per-cell CSVs. None of these receipt filenames proves validity without checking contents.

Census for each categorical model/task:
```bash
conda run -n culture-study python -m culture_study census --prepared prepared/r001-lang-v2 --direct-run "runs/r001-lang-v2/$MODEL/$TASK/direct" --alternative-run "runs/r001-lang-v2/$MODEL/$TASK/label_likelihood" --direct-score "runs/r001-lang-v2/$MODEL/$TASK/direct-score" --alternative-score "runs/r001-lang-v2/$MODEL/$TASK/label_likelihood-score" --out "runs/r001-lang-v2/$MODEL/$TASK/census"
```
SAQ fixed native prompt diagnosis:
```bash
conda run -n culture-study python -m culture_study census --prepared prepared/r001-lang-v2 --direct-run "runs/r001-lang-v2/$MODEL/blend_saq/direct" --alternative-run "runs/r001-lang-v2/$MODEL/blend_saq/direct" --direct-score "runs/r001-lang-v2/$MODEL/blend_saq/direct-score" --alternative-score "runs/r001-lang-v2/$MODEL/blend_saq/direct-score" --out "runs/r001-lang-v2/$MODEL/blend_saq/census"
```
SAQ internally compares inst-4 against pers-3; it never compares a record to itself. It is a diagnosis, not an oracle selector or substitute endpoint. residuals.jsonl keeps evidence records and null mechanism fields. Source review must classify the actual failure and strongest alternatives before producing Natural Gate 0 observations; do not fill nulls automatically.

## Finite repair and acceptance
At most two retained attempts per model unit. At most two bounded environment/source repair attempts within the actual cumulative admitted budget. An OOM, context overflow, failed tokenizer boundary, missing dependency or parity mismatch stops the affected run; park it if the bound is reached. Continue only independent admitted cells. Do not install a service, allocate paid GPUs or revise precision/tuning based on test score.

Resume only the identical source/input/model/hardware/settings manifest. Preserve a malformed JSONL tail and repair from recorded valid-prefix evidence before rechecking; never silently discard it. Any result-affecting source/asset change requires a child run and requalification, not rewriting old receipts.

Local prelude acceptance requires complete immutable acquisition/preparation manifests, original native denominators, all requested model/task/arm outputs within actual resources, actual scorer qualification, errors/negative evidence retained and a reviewed residual census. Quantitative effect claims additionally require an applicable trusted clustered statistical callback; that callback is not delivered or admitted yet.

Then restore the canonical workflow using the actual installed artifact schemas. Freeze a sourced Parent Problem and value thresholds; require Natural Gate 0, substantive math pool and per-card review/ranking, current collision/IPCG before candidate code. No development split was established here. No test fitting/tuning/retrieval labels. Legitimate development and fresh native confirmation, complete candidate G01/controls, E04 and independent confirmation are unresolved prerequisites.

Deliver small source/provenance/status changes to literal main by expected-head or normal fast-forward, read exact commit paths/contents, and exclude credentials, large data/model weights and private skill source. HF output remains unspecified. A checkpoint upload/new destination is a separate unresolved decision only if it becomes necessary.

## Child source acceptance: parity and census provenance
This repair is generated_unexecuted. Use the delivered child revision for new
runs; preserve any run already pinned to older code. Source changes alter
source_digest, so do not point new scoring at an old inference manifest or edit
old receipts to pass. Existing scientific results, if any, must be reviewed at
their original revision.

Before dispatch, inspect research/CODE_REVIEW.md and the additional bounds in
research/math/J01_REVIEW.md. Local qualification must check the actual runbook's
relative-path parity command, exact native per-cell CSV coverage and hashes,
score/run task-model-arm identity, and outcomes/manifest/prepared hash checks.
The original module import and all declared resources must remain pinned.
parity_saq restores cwd and sys.path on either outcome; retained partial
destinations require a new attempt directory. A parity failure or missing old
score_artifacts field is not solved by adding a flag or editing a receipt.

These are planned checks, not completed tests. Use real acquired native assets
and retained outputs through the admitted harness; no invented scientific cases.
Keep all old logs and bounded repair rules. Return acquisition/prepared manifests,
complete raw predictions, scored outcomes, live native parity output, census
receipts and every failure with exact code/model/data/resource revisions.

## Likelihood memory repair and native source audit

Read [research/implementation/README.md](research/implementation/README.md) and
[research/experiments/ACL_PROTOCOL.md](research/experiments/ACL_PROTOCOL.md) at the
receipt's exact commit. Source remains generated_unexecuted.

The repaired whole-label arm converts only continuation prediction positions to
float32, releases temporary logits each label, disables an unused teacher-forcing
KV cache, checks the actual full continuation context, rejects non-finite log
probabilities, and retains normalized legal-label probabilities. Direct decoding,
complete native coverage, model precision and the whole-label argmax are unchanged
by the intended construction. Actual numeric equivalence and memory are pending.

Source digest includes all project Python files, including the new audit module.
Use new immutable child run/score directories for this revision. An older
manifest cannot be resumed or scored with the current checkout; keep its pinned
checkout and all receipts. Do not retrofit label_probabilities into old records.

Before comparison, bind ACL_PREPARED_DIR, ACL_OLD_LIKELIHOOD_RUN,
ACL_NEW_LIKELIHOOD_RUN and ACL_LIKELIHOOD_AUDIT_DIR to actual absolute paths.
Both input runs must be complete on the same native task, prepared data, model
files, config and hardware. Numerical acceptance criteria must be justified and
declared before observing their differences. The implemented inner argv is:

~~~bash
conda run -n culture-study python -m culture_study audit-likelihood \
  --prepared "$ACL_PREPARED_DIR" \
  --left-run "$ACL_OLD_LIKELIHOOD_RUN" \
  --right-run "$ACL_NEW_LIKELIHOOD_RUN" \
  --out "$ACL_LIKELIHOOD_AUDIT_DIR"
~~~

The command runs only as an admitted CPU inspection task under the existing
native harness, with actual time/RAM/disk limits. It does not load a model,
generate outputs, score a benchmark or certify a tolerance. Inspect audit.json
and the full comparisons.jsonl for every canonical label and native unit.
Return both manifests/completion/prediction hashes and source digests, per-label
delta, raw/strict/final answer changes, actual calls/tokens/memory/timing.

An incomplete old run, tokenization or hardware mismatch, non-finite value,
unexplained output change or numerical mismatch leaves acceptance pending.
Retain the error and bounded repair history. Requalify affected native behavior
through the actual original scorer; the audit is software evidence, not a
scientific performance endpoint. Continue independent qualified cells only.

The 14-run baseline census still uses the original two datasets and complete
coverage. J01/LOCAL02/PARETO03 have no callable solver and must not be dispatched.



## Native language-column repair

Read [research/model/NATIVE_EVIDENCE_CONTRACT.md](research/model/NATIVE_EVIDENCE_CONTRACT.md),
[research/sources/NATIVE_VIEW_AUDIT.json](research/sources/NATIVE_VIEW_AUDIT.json), and the current
research/sources.lock.json before setup. This is a generated_unexecuted input child.
The old Question-English / Translation-local assumption reverses the actual read release content for 14 cultures.
Question/prompt columns now have separate source-locked meanings. Full 500-row/culture qualification is pending.

The active command blocks above now use child identities:
bindings-r001-lang-v2.json, assets/r001-lang-v2, prepared/r001-lang-v2 and runs/r001-lang-v2.
They are proposed project-relative paths, not observed remote directories.
If any already exists, reconcile its exact source/lock/config identity. Do not overwrite it;
bind another explicit child identity consistently through the existing CLI.
Preserve bindings.json, assets/acquisition.json, prepared/r001 and all older runs/receipts.
The new source_lock digest requires a new bind and acquisition receipt.
This is not a license to rerun/erase completed attempts.

Ordered inner argv after actual host/harness admission:
~~~bash
conda run -n culture-study python -m culture_study bind --out bindings-r001-lang-v2.json
conda run -n culture-study python -m culture_study acquire --assets assets/r001-lang-v2 --bindings bindings-r001-lang-v2.json
conda run -n culture-study python -m culture_study validate-assets --assets assets/r001-lang-v2 --bindings bindings-r001-lang-v2.json
conda run -n culture-study python -m culture_study prepare --assets assets/r001-lang-v2 --bindings bindings-r001-lang-v2.json --out prepared/r001-lang-v2
~~~

Preserve existing verified files/caches. Local may reuse unchanged source/model files by copying or linking
them into the child asset layout only after verifying the exact upstream revision/blob/content identity.
The existing acquire skips present source files then checks their pinned Git blob and size;
model acquisition can use the valid HF cache. It writes a **new** child acquisition.json.
Do not copy an old receipt as proof of child acquisition. Use the same legal model revisions for a repaired
comparison. If the binder's Llama revision differs from an existing immutable model binding, park the affected
comparison and make a source-reviewed child model pin; do not switch models silently or edit the old receipt.
If there is no prior binding, record the newly resolved revision prospectively.

Required source/input acceptance before model dispatch:
- coverage must retain 1227 CB questions/4908 Hard rows, both native MCQ shards, 16 original BLEnD cultures,
  500 shared IDs, 30 SAQ language cells, two official prompt IDs and 30000 SAQ units per model.
- SAQ coverage includes input_contract_id=blend_original_7b9c131_columns_v2 and the complete mapping.
  Every SAQ unit source records question_column, prompt_column and input_contract_id.
- For all 14 non-English cultures, English questions come from Translation with English prompt templates;
  local questions come from Question with translated templates. US/UK retain Question and only one English cell.
  Inspect actual native texts/IDs across the complete prepared files, including culture references and
  label-blind question/prompt composition. Headers or script characters alone are insufficient language proof.
- Record input audit/source hashes and all exceptions. Unresolved malformed/mixed-language/ID/scorer behavior
  parks the affected claims; no source-label repair, homemade eval cases, silent row omission or test tuning.
- Requalify official scorer dependencies and live parity at this revision on actual native outputs.
  A source fix does not produce parity. Perform the exact 14-run sequence and collection above only when
  actual resources and the native harness permit complete coverage.

Retain raw per-ID predictions, language/prompt score cells, original score artifacts, costs,
census and failures, with new source/input identities. Never recertify older mislabeled-language
runs by renaming a language field. If older runs are later found, review them separately as
historical/source-defect evidence, not as child performance or confirmation.

The old/new whole-label memory audit needs identical prepared inputs and is a separate qualification.
It cannot compare the differently conditioned SAQ input child as a numerical equivalence test.
No J01/LOCAL02/PARETO03 solver or candidate G01 is admitted.
Bounded repair remains at most two attempts within actual cumulative limits;
source/input/scorer or resource failure preserves the failed attempt and parks its descendants.
Return a coherent small evidence packet to this same repo/main with exact tested commit,
raw/per-ID/scorer/parity/census locators and actual host/budget gaps.

