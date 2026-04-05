# Chapter 6 — Function Approximation, the Deadly Triad, and DQN

## What this chapter establishes

This chapter explains what changes when value functions are no longer stored in tables.

By the end, you should know:

- how a parameterized value function turns learning into regression,
- why the deadly triad is a real stability issue,
- how DQN defines its target and loss,
- why frozen target networks matter,
- what replay changes,
- and why representation choice is part of the RL problem rather than a mere implementation detail.

---

## 1. Why tabular methods stop scaling

A tabular method stores a separate value for each state or state-action pair.

That works only when the relevant space can be explicitly enumerated.  
If the state-action space is too large, too sparse, or continuous, a table becomes impractical.

So we replace the table with a parameterized function, such as

\[
\widehat V(\cdot; w)
\quad \text{or} \quad
\widehat Q(\cdot,\cdot; w),
\]

where \(w \in \mathbb{R}^d\) is the parameter vector.

---

## 2. Learning as regression

Given a target random variable \(Y\), define the squared-error objective under a data distribution \(\nu\):

\[
L(w)
=
\mathbb{E}_{(S,A,Y)\sim \nu}
\left[
(Y - \widehat Q(S,A;w))^2
\right].
\]

For a finite batch of size \(B\), the empirical loss is

\[
\widehat L_B(w)
=
\frac{1}{B}\sum_{i=1}^B
\left(Y_i - \widehat Q(S_i,A_i;w)\right)^2.
\]

### What this means

The approximator is trying to predict target values from input pairs \((S,A)\).

### Exact gradient of the empirical loss

If the target values \(Y_i\) are treated as constants with respect to \(w\), then

\[
\nabla_w \widehat L_B(w)
=
\frac{1}{B}\sum_{i=1}^B
2\left(\widehat Q(S_i,A_i;w)-Y_i\right)
\nabla_w \widehat Q(S_i,A_i;w).
\]

### Important classification

This is the exact gradient of the stated batch loss **only when the targets are treated as fixed with respect to \(w\)** during differentiation.

That caveat matters later.

---

## 3. The deadly triad

The deadly triad is the simultaneous presence of:

1. function approximation,
2. bootstrapping,
3. off-policy learning.

### Why these three together are dangerous

Each one alone may be manageable.  
Together, they can produce instability or divergence because:

- function approximation causes updates at one input to affect predictions at many other inputs,
- bootstrapping makes targets depend on current predictions,
- off-policy learning means the data distribution need not match the target policy’s occupancy distribution.

### What conclusion you are allowed to draw

The deadly triad is a **risk structure**, not a theorem that every such method must diverge.

It means instability becomes possible and must be controlled.

---

## 4. DQN target

DQN keeps the Q-learning idea but replaces the table by a neural approximator \(Q(\cdot,\cdot; w)\).

For a sampled transition \((S_t, A_t, R_{t+1}, S_{t+1}, \zeta_t)\), where \(\zeta_t \in \{0,1\}\) indicates whether the transition is terminal, define

\[
Y_t^{\mathrm{DQN}}
=
R_{t+1}
+
\gamma(1-\zeta_t)\max_{a'}Q(S_{t+1},a'; w^-).
\]

Here \(w^-\) is a frozen target-network parameter vector.

### What each term checks

- \(R_{t+1}\): the immediate observed reward
- \((1-\zeta_t)\): whether future continuation should be included
- \(\max_{a'}Q(S_{t+1},a'; w^-)\): greedy continuation value evaluated by the frozen target network
- \(\gamma\): discounting of the continuation term

### Terminal transition boundary condition

If \(\zeta_t = 1\), then the transition ends the episode and the future contribution is forced to zero:

\[
Y_t^{\mathrm{DQN}} = R_{t+1}.
\]

If \(\zeta_t = 0\), the usual continuation term remains.

---

## 5. DQN loss

At training stage \(t\), under replay distribution \(\nu_t\), define

\[
L_t(w; w^-)
=
\mathbb{E}_{(S,A,R,S',\zeta)\sim \nu_t}
\left[
\left(
R + \gamma(1-\zeta)\max_{a'}Q(S',a';w^-) - Q(S,A;w)
\right)^2
\right].
\]

### Why the frozen target matters

During optimization with respect to the online parameters \(w\), the target depends on \(w^-\), not on the same vector \(w\) currently being updated.

That means the right-hand side is a well-defined regression target during the update window in which \(w^-\) is held fixed.

### What problem this avoids

If the same parameters were used on both sides and differentiated through naively, the target would move at the same time as the prediction, which can destabilize optimization.

The frozen target reduces that moving-target problem.

---

## 6. Replay distribution

A replay buffer stores transitions collected over time.  
If the buffer at time \(t\) is

\[
\mathcal{B}_t = \{(S_i,A_i,R_i,S'_i,\zeta_i)\}_{i=1}^{N_t},
\]

and transitions are sampled uniformly, then the empirical training distribution is uniform over those \(N_t\) stored transitions.

### Why replay helps

Replay changes the temporal structure of training data.

Instead of training only on the most recent, highly correlated transitions, the learner trains on a more mixed sample from recent history.

This has two main effects.

1. It reduces short-range correlation in updates.
2. It allows reuse of past experience.

### What replay does **not** do by itself

Replay does not make the method on-policy.  
DQN remains a value-based off-policy method.

---

## 7. Computational cost of the target

For a batch of size \(B\) and a discrete action set of size \(|\mathcal{A}|\), evaluating the target requires checking the next-state action values across all candidate next actions.

So the per-batch target-evaluation cost is

\[
O(B|\mathcal{A}|).
\]

### Why this cost appears

For each of the \(B\) next states, you must evaluate the approximator on every candidate action inside the maximization.

### Boundary condition

If the action space is continuous, that discrete maximization is no longer directly available.  
Then DQN in its standard discrete-action form no longer applies without modification.

---

## 8. Representation and state encoding

A representation maps raw observations or histories into the input space used by the function approximator.

This is not merely a formatting decision.  
It changes the effective learning problem.

### Example: neighborhood encoding

If a gridworld representation records four neighboring binary terrain indicators, then each neighbor has \(2\) possibilities and there are \(4\) positions, so the total number of local patterns is

\[
2^4 = 16.
\]

If exactly one neighboring cell may instead contain a goal marker and the remaining three cells remain binary terrain cells, then the count changes because:

1. the goal can occupy any one of \(4\) positions,
2. once that position is fixed, the remaining \(3\) cells each have \(2\) possibilities.

So the goal-containing case contributes

\[
4 \cdot 2^3 = 32
\]

patterns, and the total count becomes

\[
16 + 32 = 48.
\]

### Why this matters

Representation size and representation adequacy are separate questions.

A compact representation may still be non-Markov.  
A large representation may still omit key hidden variables.  
The count of representable inputs does not by itself certify that the encoding is sufficient.

---

## 9. Common confusions blocked here

### Confusion 1: once you use a neural network, RL becomes ordinary supervised learning

No.

The loss may look like regression, but the targets are generated by Bellman-style bootstrapping and the data distribution depends on the interaction policy.

### Confusion 2: the deadly triad means any off-policy deep RL method must fail

False.

It names a source of instability, not a universal impossibility theorem.

### Confusion 3: target networks are just an optimization trick with no conceptual role

Wrong.

Their conceptual role is to freeze the target while differentiating with respect to the online parameters.

### Confusion 4: representation only affects speed, not correctness

False.

A poor encoding can destroy the Markov property or hide critical variables, changing what can be learned at all.

---

## 10. Mastery check

You understand this chapter if you can explain all of these exactly.

1. What turns value learning with approximation into a regression problem?
2. Why is the “frozen” part of a target network important?
3. Which three ingredients form the deadly triad?
4. Why does terminal handling multiply the future term by \(1-\zeta_t\)?
5. Why can a compact state encoding still be inadequate?

Do not move on if any answer is merely intuitive rather than exact.
