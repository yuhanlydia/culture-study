# J01 semantic review and optimization consequences
Status: author-derived read-only review of the unselected J01 discussion preserved at commit 3621288c90cac4c6edd217a57967a5e25d9cf3b5. No solver code or candidate approval.

## Preserved valid results
For p_j,m_jk strictly between zero and one, finite λ≥0, the fixed-marginal feasible polytope contains positive q0. KL(q||q0) is strictly convex on probabilities and the pairwise Bernoulli divergences are convex after their linear moment map; a unique optimizer exists. The KKT exponential family has the stated negative pairwise-gradient term. This is an implicit optimality system, not a one-step closed form.

The optimum is in the relative interior. If a minimizer has a zero state probability, mix it with positive q0 by ε. The zero-coordinate KL directional derivative is −∞. Any moment at an endpoint also has a divergence derivative toward the interior of −∞; finite interior moment terms cannot cancel this. Thus such a boundary point cannot minimize. This justifies using the positive-probability KKT equations here, under the exact stated assumptions.

The Hessian in the interior is
H = diag(1/q_z) + λ A2^T diag(1/[u_r(1−u_r)]) A2,
where A2 maps state probabilities to pair moments. It is positive definite, including on the equality-constraint tangent space. For K=4 there are 16 states, five independent equality rows, and six pairs. A dense equality-constrained Newton step solves a 21×21 KKT system, with arithmetic cost O((2^K+K+1)^3) per iteration plus moment assembly. This dimension count is not a measured runtime or global solver-complexity guarantee.

## Required correction to the single-label statement
The unique distribution on one-hot states with fixed marginal probabilities is q(e_j)=p_j, provided ∑j p_j=1. This leaves no dependence freedom.

It is generally **not** the previously defined independent Bernoulli product q0. That product places mass outside one-hot states and its mass on one-hot states usually does not sum to one. Restricting and normalizing it gives masses proportional to p_j∏_{k≠j}(1−p_k), which generally differ from p_j. If the supplied binary marginals do not sum to one, the one-hot fixed-marginal constraint is infeasible.

Therefore J01's “q=q0” single-label shorthand must mean a newly defined categorical reference, not inheritance of its multilabel product formula. The no-improvement/zero-freedom conclusion survives this correction. BLEnD MC cannot gain a J01 dependence degree of freedom by changing its state domain.

## First-order perturbation exposes the actual intervention
Let q_λ=q0+λδ+O(λ²), and g_jk=logit(p_jp_k)−logit(m_jk), evaluated at λ=0. The equality constraints require ∑zδ(z)=0 and ∑zδ(z)z_j=0.

Linearizing stationarity gives
δ(z)/q0(z) + ∑_{j<k}g_jk z_jz_k + α + ∑jβ_j z_j = 0.
Under independent q0, centered pair products (z_j−p_j)(z_k−p_k) are orthogonal to the constant and every first-order centered variable. Decomposing z_jz_k into centered pair, first-order and constant components therefore yields exactly
δ(z)=−q0(z) h(z),
h(z)=∑_{j<k}g_jk(z_j−p_j)(z_k−p_k).
Its normalization and every marginal derivative vanish, as required. Thus
log q_λ(z)=log q0(z)−λh(z)+O(λ²).
The reweighting changes pairwise dependence, not first-order marginals. This is an author-derived local expansion of an existing projection construct; not a novelty verdict or numerical result.

Prediction: to first order the relative log mass of states a,b changes by −λ[h(a)−h(b)]. If m_jk=p_jp_k, every g_jk=0 and the intervention vanishes exactly for any λ. Pure marginal confidence changes cannot explain this fixed-p construction internally, although the extra elicitation queries still provide extra information and compute.

## MAP margin boundary
Let a0 be the unique mode of q0 and γ=min_{z≠a0}[log q0(a0)−log q0(z)]>0. If max_z|log q_λ(z)−log q0(z)|<γ/2, the mode cannot change: its perturbed log gap is at least γ−2ε>0. A projection can alter dependence without altering any native prediction. Solver convergence or nonzero KL is therefore not evidence of endpoint improvement.

For a stated uniform approximation error δ∞=max_z|P(z)−q(z)|, the excess exact-match risk of q-MAP over P-MAP is at most 2δ∞, by inserting/subtracting q at the two modes. The unknown δ∞ must never be replaced by an assumed calibration guarantee.

## Review decision and necessary comparisons
J01 remains unselected, mechanism necessity/novelty unknown. It has no native BLEnD SAQ construction, and the one-hot task reduces as above. Its six extra pairwise elicitation queries require an information/compute-matched simpler comparator; 16-state optimization cost alone is not total cost.

ConCoRD's actual nlic/solver.py was re-read at 4f0c7fee44d3d61020c9c4a5a523beba80c4c55d: it converts confidences to weighted clauses, includes relation weights and RC2 inference, with options changing exactly-one behavior. Fixed-marginal distribution projection is a structural comparison to investigate, not enough by itself to declare an advance. LoCo's primary probabilistic/semantic-loss sections were read; the inspected model.py initialization is not a completed loss implementation audit.

Falsifiers: residual native failures resolved by the qualified simple baseline; mode unchanged in consequential cases; miscalibrated pairwise evidence causing loss; high-order structure dominating; budget-matched direct set generation/established logic solver explaining any effect; failure to cover the agreed native endpoints. Do not use the mathematical examples as scientific eval cases.

Next admitted-candidate work requires the sourced parent/census, full distinct mathematical pool/reviews/ranking and actual collision/IPCG. No “J01 code” is delivered before those boundaries.

## Finite change bounds and a marginal-only obstruction (2026-10-08)

These are additional author-derived analytical boundaries, not new candidates,
native examples, executed solver tests or novelty claims. Use the same fixed
p, interior m, finite λ assumptions and multilabel state domain as J01.

Write R(q)=Σ_r d_Ber(u_r(q)||m_r) and R0=R(q0). Optimality against feasible q0 gives

KL(qλ||q0)+λR(qλ) ≤ λR0, hence KL(qλ||q0) ≤ λR0.

With natural logarithms, Pinsker's inequality yields
TV(qλ,q0) ≤ sqrt(λR0/2). For the unique independent mode a0, define
Δ=min_{z≠a0}(q0(a0)−q0(z))>0. A probability coordinate changes by at
most TV, so qλ(a0)−qλ(z) ≥ Δ−2 sqrt(λR0/2).
Thus **λR0 < Δ²/2 guarantees no MAP change**. This is a sufficient,
generally loose condition, not a claim that crossing it guarantees a change.
When R0=0 the original exact independent reduction applies for every λ.
For independent Bernoulli coordinates with no p_j=1/2,
Q=∏_j max(p_j,1−p_j) and
Δ=Q[1−max_j min(p_j,1−p_j)/max(p_j,1−p_j)].
The largest nonmodal probability changes just the coordinate with the largest
minority-to-majority ratio; any further changes multiply by ratios below one.

A stronger λ-independent exclusion is available from marginals alone.
Let a0_j be the majority bit, e_j=min(p_j,1−p_j), E=Σ_j e_j,
and e_max=max_j e_j. Under **any** joint q with those fixed marginals,
the union bound gives q(a0)≥1−E.
For any z≠a0, choose a differing coordinate j; the event Z=z is contained
in {Z_j≠a0_j}, so q(z)≤e_j≤e_max.
Consequently **E+e_max<1 guarantees a0 is the unique MAP for every feasible q**,
including every J01 optimizer, irrespective of pair evidence or λ.
This is only sufficient: a loose lower bound 1−E may be negative and says
nothing outside the stated regime. With K=1 and an interior non-tied p,
the condition reduces to 2e_1<1 and confirms the absence of dependence freedom.
At p_j=1/2 ties require an explicit tie rule; no strict no-change claim follows.

Consequential prediction: no fixed-marginal J01 effect can occur on items
satisfying E+e_max<1 in exact arithmetic. If a future implementation changes
such an answer, first investigate a marginal-constraint violation, option
alignment or MAP extraction error; do not interpret it as cultural knowledge
gain. This check uses only predeclared inference probabilities, no test labels.
Concentrated but incorrect marginals can therefore lock in a wrong answer:
joint projection cannot repair that error while keeping those marginals.
Baseline margin and no-change strata must be retained in future mechanism review.

The constants were checked by the two routes above (objective comparison/TV and
direct event inclusion), without executing scientific code. Both rely on standard
probability inequalities, so these are scope diagnostics, not original theorem
claims. The bounds neither identify true joint probabilities nor map J01 to
BLEnD SEM-B/SEM-W. No pool admission, ranking, solver or experimental approval
changes. Empirical relevance, calibration and item frequencies remain unknown.
