# Mathematical inquiry and semantic review
Author-derived analysis; source benchmarks define the endpoints, not the following proofs. Status: read-only mathematical exploration. Eight inquiries, zero admitted novel candidates. No 20→15 selection is claimed. A missing justified candidate is not filled with parameter variants.

## M01 — Exact group loss and independence boundary
Object: Y=(Y1,...,Y4) in {0,1}^4 and action a. Native group loss is L(a,Y)=1−1{a=Y}. Bayes action is argmax_a P(Y=a|x). If the posterior factorizes, P(Y=a|x)=∏j p_j^{a_j}(1−p_j)^{1−a_j}; maximizing the sum of logs separates, giving a_j=1{p_j≥1/2} (ties arbitrary). Thus renaming independent decisions “joint decoding” changes nothing.
Construction: the baseline must compute entire label probabilities, then expose all four outputs at group scoring. Novel joint inference would require justified non-factorizing information.
Prediction/falsifier: an independent joint implementation must exactly agree with marginal MAP, up to ties. A claimed gain without altered information indicates a parser/token-budget/confound.
Simple comparison: direct greedy versus whole-label likelihood. Collision: ordinary Bayes decision theory, not a new method.
Review: exact identity, conditional independence is an assumption, not established cultural mechanism. Operation path B04→B01, condition conditional.

## M02 — Marginal correctness does not identify group correctness
Object: E_j={prediction j correct}, q_j=P(E_j). By union bound,
max(0,∑j q_j−3)≤P(∩j E_j)≤min_j q_j.
The independent product ∏j q_j is only one possible joint distribution. Dependence is unidentifiable from four marginal rates alone.
Construction: preserve full group predictions and estimate observed intersections rather than multiplying row accuracies.
Distinct prediction: matching row accuracy can coexist with differing native Hard accuracy.
Falsifier/boundary: once the complete joint correctness distribution is observed, this ambiguity disappears.
Simple alternative: native grouping, no optimization. Collision: Fréchet/union bounds; established mathematics.
Review: lower bound uses P(∪ E_j^c)≤∑(1−q_j); upper follows intersection inclusion. No fitted correlation or improvement claimed. B06→H02, established.

## M03 — Small row errors have a finite group-loss bound
For deterministic predictions on N native groups, let m_i be incorrect judgments in group i. Then
(1/4)∑i m_i ≤ ∑i 1{m_i>0} ≤ ∑i m_i.
Dividing by N gives r≤R_group≤min(1,4r), where r counts errors over 4N rows.
Construction: report the histogram m_i=0,...,4 alongside the native endpoint.
Prediction: repairing one error in a group with m_i=1 helps the endpoint; repairing one in a group with m_i≥2 does not immediately do so.
Falsifier: a different endpoint or missing rows invalidates the identity, not a numerical “failure” of it.
Simple alternative: group-aware analysis, not extra model calls. Covered: loss decomposition.
Review: inequalities hold pointwise. They do not rank interventions without real outputs. C01→B06, established.

## M04 — Consensus cannot certify truth
Object: repeated model answers A1,...,Ak and semantic agreement score C. If all A_i equal a wrong answer a*, C is maximal while native correctness is zero. No monotone function of agreement alone can certify correctness on an unrestricted answer-generating distribution.
Construction: any future consensus method must compare against single-sample and budget-matched repeated direct inference, retaining high-consensus wrong native episodes.
Prediction: latent consensus improves only under additional, empirically justified error diversity/reliability assumptions.
Falsifier of a restricted method: high-consensus failures surviving the strongest simple alternative.
Simple alternative/functional collision: multilingual self-consistency and medoid self-training already implemented by Cross-Lingual Consensus.
Review: this is a mathematical counterexample, not a fabricated benchmark case. H06→H02, established impossibility under unrestricted distributions.

## M05 — Existential short-answer scoring is not calibrated set prediction
Object: reference alias set R and output candidate text s. If a matcher is monotone under appending text and S(s)=1{∃r∈R:match(r,s)}, then S(s⊕t)≥S(s), even if t contains incorrect cultural claims. Therefore native existential success alone cannot identify precision or all-valid-answer knowledge.
Construction: keep native scoring and raw response lengths; flag output-length dependence for later native-response audit, without creating new labels or replacing the endpoint.
Prediction: longer responses can have higher recall-style scores without a corresponding truth improvement. No such effect has yet been measured.
Falsifier/boundary: non-monotone preprocessing or a precision-sensitive metric invalidates this simplified model. The actual pinned scorer must be checked, not assumed monotone everywhere.
Simple alternative: official short-answer prompt plus fixed token cap.
Collision: established precision/recall distinction.
Review: conditional implication is correct; global monotonicity for every official language branch is unknown. B06→H02, conditional.

## M06 — Decoder channels can imitate knowledge differences
Object: latent intended label Z and emitted text O, with extraction e(O). Observed score P(e(O)=Y)=∑z P(Z=z)P(e(O)=Y|Z=z). A changed channel/extractor can change observed accuracy at fixed latent Z. Z is unobserved, so no unique knowledge/channel decomposition follows from accuracy alone.
Construction: log raw greedy output, strict extracted label and complete-label likelihood action on the same native inputs. Keep parsers frozen.
Prediction: format errors repaired by likelihood are evidence of an inexpensive interface remedy, not evidence that knowledge was learned.
Falsifier: residual native losses when both emission/extraction succeed weaken a pure-format explanation.
Simple alternative: constrained likelihood, standard decoding. Not a novel mechanism.
Review: law of total probability exact; latent intention interpretation is not identifiable. B05→H02, established.

## M07 — Repeated distractors create pseudoreplication
Let d_{iv} be paired outcome differences for template i, variant v. Treating all rows independent uses Var(mean) as if covariances vanished. Actually Var(∑_{iv}d_{iv})=∑Var(d_{iv})+2∑Cov(d_{iv},d_{jw}). Shared-question/country/translation effects can make omitted covariances positive.
Construction: resample complete global template clusters, preserving countries, variants, languages and both prompts, and recompute the frozen macro/micro estimand.
Prediction: naive row intervals may be narrower than cluster intervals; not guaranteed for every covariance law.
Falsifier/boundary: zero cross-row covariance under a justified sampling model makes the naive computation adequate.
Simple alternative: clustered paired analysis; existing statistics.
Review: exact variance expansion; independence across templates still requires scrutiny (CB near-duplicates may violate it). B04→C01, established.

## M08 — Worst-culture optimization needs legitimate development evidence
Object: culture losses L_c(θ), worst-group risk max_c L_c. Epigraph form minimizes t subject to L_c≤t. Lagrangian t+∑c λ_c(L_c−t), λ_c≥0, has finite infimum over unrestricted t only if ∑cλ_c=1; hence dual adversarial weights lie on the simplex. This is ordinary group DRO, not a novel cultural method.
Construction: a future robust objective would require non-test culture loss estimates, trainable interfaces and fair average/worst-group comparisons.
Prediction: changes target high-loss groups and can trade off overall accuracy; multilingual transfer may regress local performance.
Falsifier: no legitimate development data, unstable group estimates, or a simple fixed-weight alternative resolving the failure prevents admission.
Simple alternative: fixed macro weighting/no training. Collision: established group DRO; dedicated primary-source audit still pending.
Review: algebra valid; strong duality requires appropriate convexity/feasibility and is not asserted for neural networks. D01→D02, conditional.

## Full inquiry disposition
| Order | Inquiry | Mathematical review | New-candidate disposition |
|---|---|---|---|
| 1 | M01 | Exact under stated factorization | Comparator/negative boundary |
| 2 | M02 | Exact bounds | Measurement requirement |
| 3 | M03 | Exact pointwise inequalities | Diagnosis requirement |
| 4 | M06 | Exact mixture; non-identifiable latent interpretation | Simple comparator |
| 5 | M07 | Exact variance expansion | Statistical design |
| 6 | M04 | Exact counterexample | Covered mechanism; reject unrestricted truth claim |
| 7 | M05 | Conditional monotonicity | Native audit lead |
| 8 | M08 | Exact epigraph algebra; conditional dual interpretation | Covered objective, prerequisites missing |

This is a usefulness order for the baseline audit, not a top-15 candidate ranking. Qualified novel pool=0; target deficit=20; selected novel methods=0; top-15 deficit=15. No claim that these eight notes establish originality, necessity, Natural Gate 0, IPCG or ACL-level contribution.

Next derivation must be anchored to real small-model failures remaining after qualified simple alternatives. It may deepen a substantive mathematical route or produce no_new_idea_needed; it must not backfill formulas around prematurely written candidate code.
