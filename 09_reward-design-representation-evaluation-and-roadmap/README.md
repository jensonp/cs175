# Chapter 8 — Reward Design, Representation, Evaluation, and Roadmap

## What this chapter establishes

This chapter formalizes issues that are often treated too casually:

- the difference between reward and value,
- the precise effect of potential-based reward shaping,
- how route preferences can change as the living reward changes,
- how evaluation should be reported,
- why representation can induce non-Markov aliasing,
- and where the core material extends next.

---

## 1. Reward versus value

The immediate reward at time \(t+1\) is \(R_{t+1}\).

The action value under policy \(\pi\) is

\[
Q^\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a].
\]

### Exact distinction

- reward is a one-step scalar signal,
- return is the discounted sum of future rewards,
- value is the expectation of return under specified conditioning and policy assumptions.

### Why this matters

A learner is not usually optimizing the immediate reward term in isolation.  
It is optimizing expected long-run return.

Only in the special case \(\gamma=0\) does the problem collapse to pure one-step reward maximization.

---

## 2. Potential-based reward shaping

Let the original reward be \(r_t\).  
Choose any potential function \(\Phi : \mathcal{S} \to \mathbb{R}\).  
Define the shaped reward by

\[
r_t' = r_t + \gamma \Phi(S_{t+1}) - \Phi(S_t).
\]

### What must be checked

To understand the effect on return, compare the original return

\[
G_0 = \sum_{t=0}^{\infty}\gamma^t r_t
\]

with the shaped return

\[
G_0' = \sum_{t=0}^{\infty}\gamma^t r_t'.
\]

Substitute the definition of \(r_t'\):

\[
G_0'
=
G_0
+
\sum_{t=0}^{\infty}\gamma^{t+1}\Phi(S_{t+1})
-
\sum_{t=0}^{\infty}\gamma^t\Phi(S_t).
\]

Now rewrite the first extra sum with index \(j=t+1\). Then

\[
\sum_{t=0}^{\infty}\gamma^{t+1}\Phi(S_{t+1})
=
\sum_{j=1}^{\infty}\gamma^j \Phi(S_j).
\]

Split the second extra sum into its \(t=0\) term plus the rest:

\[
\sum_{t=0}^{\infty}\gamma^t\Phi(S_t)
=
\Phi(S_0) + \sum_{t=1}^{\infty}\gamma^t\Phi(S_t).
\]

The two infinite tails cancel, leaving

\[
G_0' = G_0 - \Phi(S_0).
\]

### What conclusion this licenses

Potential-based shaping changes the return only by a start-state-dependent constant.  
So for a fixed start state, relative action preferences and optimal policies are preserved.

### What is **not** guaranteed

A shaping term that is not of potential-based form does not automatically preserve optimal policies.

That point must stay sharp.

---

## 3. Route thresholds in gridworld-style problems

Suppose there are two candidate routes, indexed by \(i \in \{1,2\}\).

- route \(i\) lasts \(T_i\) nonterminal steps,
- it ends with terminal reward \(R_i\),
- and each nonterminal step contributes living reward \(r\).

Then the return of route \(i\) is

\[
G_i(r)
=
\sum_{t=0}^{T_i-1}\gamma^t r + \gamma^{T_i}R_i.
\]

### If \(\gamma \neq 1\)

The finite geometric sum is

\[
\sum_{t=0}^{T_i-1}\gamma^t
=
\frac{1-\gamma^{T_i}}{1-\gamma}.
\]

So

\[
G_i(r)
=
r\frac{1-\gamma^{T_i}}{1-\gamma}
+
\gamma^{T_i}R_i.
\]

To find the threshold where the two routes tie, solve

\[
G_1(r) = G_2(r).
\]

That yields the living-reward value at which the preferred route changes.

### If \(\gamma = 1\) and the horizon is finite

Then the geometric-sum formula above is not the correct form because its denominator becomes zero.  
Instead use the finite-horizon undiscounted sum directly:

\[
G_i(r) = T_i r + R_i.
\]

Setting the two routes equal gives

\[
T_1 r + R_1 = T_2 r + R_2,
\]

so if \(T_1 \ne T_2\),

\[
r = \frac{R_2 - R_1}{T_1 - T_2}.
\]

### Why this section matters

It shows concretely that changing a living reward can change the preferred policy region.  
Reward design is not a cosmetic choice.

---

## 4. Evaluation methodology

Suppose an algorithm is run with \(N\) independent random seeds, producing evaluation returns

\[
X_1, X_2, \ldots, X_N.
\]

The sample mean is

\[
\widehat \mu_N = \frac{1}{N}\sum_{i=1}^N X_i.
\]

### Why multiple seeds matter

RL outcomes can vary substantially across random initializations, environment stochasticity, and exploration trajectories.  
A single run is not enough evidence.

### What a good evaluation report should specify

At minimum, report:

1. the environment and task definition,
2. the reward definition,
3. the state or observation representation,
4. the number of training steps or episodes,
5. the evaluation policy used,
6. the number of random seeds,
7. the statistic reported across seeds,
8. any confidence intervals or dispersion summaries,
9. ablations that isolate major design components.

### What an ablation is

An ablation is a controlled comparison where one component is removed or changed while the rest of the protocol is kept fixed.

If many things change at once, the result is no longer a clean ablation.

---

## 5. Representation counts and non-Markov aliasing

A representation may be compact and still fail to be Markov.

### What aliasing means

Aliasing occurs when two different underlying histories or latent states map to the same representation, even though they imply different future transition or reward distributions.

Then the learner cannot distinguish situations that require different decisions.

### Why this matters

Once aliasing occurs, state-based Bellman reasoning written on that representation may no longer describe the true controlled process correctly.

That is not just a data-efficiency issue.  
It is a modeling issue.

### Example intuition

A visual observation might look identical whether or not a key was already collected in the past.  
If future transitions depend on that hidden fact, the raw observation is not Markov.

---

## 6. Roadmap beyond the core

The core material supports several nearby extensions.

### Model-based RL

Instead of being given the transition law \(P\), the learner estimates or plans with a model.

### Partial observability

When observations are not Markov, one can work with belief states, recurrent memory, or other history-dependent representations.

### Multi-step returns and eligibility traces

These interpolate between one-step TD and full-return Monte Carlo.

### Continuous-control actor-critic methods

These adapt the policy-gradient and critic ideas to continuous action spaces.

### Offline RL

Learning is performed from a fixed dataset rather than continued interaction, which sharpens distribution-shift issues.

### Distributional RL and risk-sensitive RL

These change what is being predicted or optimized beyond expected return alone.

### Why this roadmap belongs here

These topics extend the same formal backbone rather than replacing it.  
The objects remain:

- policies,
- returns,
- value functions,
- state representations,
- and optimization objectives.

---

## 7. Common confusions blocked here

### Confusion 1: reward shaping just makes learning faster and cannot change the problem

False in general.

Only specific shaping forms, such as potential-based shaping, preserve optimal policies in the standard sense.

### Confusion 2: reward and value differ only informally

No.

Reward is immediate.  
Value is an expectation of long-run return.

### Confusion 3: evaluation with one strong run is acceptable evidence

Not in any serious experimental standard.  
Variation across seeds and design choices must be reported.

### Confusion 4: a small representation is bad and a large representation is good

Neither is true on its own.

The real question is whether the representation preserves the information needed for prediction and control.

---

## 8. Mastery check

You understand this chapter if you can explain all of these exactly.

1. Why does potential-based shaping preserve policy ordering up to a start-state constant?
2. Why must the \(\gamma=1\) route-threshold case be handled separately?
3. What makes an ablation “clean”?
4. What is non-Markov aliasing?
5. Why can evaluation not rely on a single random seed?

This chapter is where the theory connects to design discipline.  
Treat it with the same rigor as the earlier derivations.
