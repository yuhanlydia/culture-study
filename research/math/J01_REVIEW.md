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
