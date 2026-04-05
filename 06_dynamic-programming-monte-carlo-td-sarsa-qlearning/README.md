# Chapter 5 — Dynamic Programming, Monte Carlo, TD, SARSA, and Q-Learning

## What this chapter locks in

This chapter explains how Bellman equations turn into actual procedures.

The main risk here is mixing different axes together:

- model known versus unknown,
- exact expectation versus sampled target,
- full return versus bootstrap,
- on-policy versus off-policy,
- sampled next action versus greedy next action.

This rewrite keeps those axes separate on purpose.

---

## 1. Dynamic programming: planning with a known model

Suppose the transition–reward law $P(s',r \mid s,a)$ is known.

Then for a fixed policy $\pi$, iterative policy evaluation applies the Bellman expectation operator repeatedly:

$$
V_{k+1} = T^\pi V_k.
$$

### What is being updated

- $V_k$ is the current estimate after iteration $k$,
- $T^\pi$ uses the known model and the fixed policy to compute the next estimate.

### Why this converges

In the discounted setting, $T^\pi$ is a contraction.  
So repeated application converges to the unique fixed point $V^\pi$.

### What dynamic programming is

It is **planning** with a known model.

### What it is not

It is not learning directly from raw sampled experience alone.

That distinction matters because later chapters move to settings where the model is not known.

---

## 2. Value iteration

If the goal is optimal control rather than evaluation of a fixed policy, use the optimality operator:

$$
V_{k+1} = T^*V_k.
$$

### What changes relative to policy evaluation

The continuation action is no longer averaged under a fixed policy.  
It is chosen by maximization.

### What stays the same

The convergence logic still comes from contraction in the discounted setting.

---

## 3. Monte Carlo estimation

Now move to a setting where you sample experience under a policy and use complete returns from episodes.

Suppose state $s$ is visited at time $t$.  
If you wait until the episode terminates, you can form the realized return $G_t$ following that visit.

A Monte Carlo estimator averages those complete sampled returns.

### What Monte Carlo uses

It uses the **full realized return** after a visit.

### What Monte Carlo does not use

It does **not** bootstrap from the current estimate.

That is the defining distinction.

### Strength

The target is tied directly to realized long-run outcomes.

### Cost

You must wait for enough future rewards to observe the complete return.

---

## 4. Temporal-difference learning

Start from the Bellman expectation equation for a policy:

$$
V^\pi(S_t)
=
\mathbb{E}_\pi[R_{t+1} + \gamma V^\pi(S_{t+1}) \mid S_t].
$$

A one-step TD method replaces the exact conditional expectation by the single transition that actually occurred.

That gives the one-step target

$$
Y_t^{\mathrm{TD}} = R_{t+1} + \gamma V(S_{t+1}).
$$

The corresponding TD error is

$$
\delta_t
=
R_{t+1} + \gamma V(S_{t+1}) - V(S_t).
$$

### What changed relative to the Bellman equation

The Bellman equation is an exact expectation identity.  
The TD target is one noisy sample-based surrogate for that expectation.

### Why this is called bootstrapping

The target depends partly on fresh data, $R_{t+1}$, and partly on the current estimate, $V(S_{t+1})$.

So the method is learning partly from its own present prediction.

---

## 5. The exact Monte Carlo versus TD distinction

This distinction should become automatic.

### Monte Carlo target

The target is the complete sampled return $G_t$.

### TD target

The target is

$$
R_{t+1} + \gamma V(S_{t+1}),
$$

which combines one-step data with a bootstrap term.

### Therefore

- Monte Carlo does **not** bootstrap.
- TD **does** bootstrap.

Do not replace that clean distinction with vague slogans like “TD is faster” or “Monte Carlo is more accurate.”  
Those may be context-dependent consequences, but they are not the definition.

---

## 6. Behavior policy and target policy

These two policies answer different questions.

### Behavior policy

The behavior policy is the policy that generates the data.

### Target policy

The target policy is the policy whose value is being estimated or improved.

### On-policy case

If the same policy both generates the data and appears inside the learning target, the method is on-policy.

### Off-policy case

If the data come from one policy while the target corresponds to another, the method is off-policy.

This distinction is one of the central classification checks in RL.

---

## 7. $\epsilon$-greedy exploration

Assume a finite action set $\mathcal{A}$ and a unique greedy action at state $s$.

An $\epsilon$-greedy policy does the following:

- with probability $1-\epsilon$, choose the greedy action,
- with probability $\epsilon$, choose uniformly among all actions.

### What probability the greedy action receives

The greedy action gets

$$
1-\epsilon + \frac{\epsilon}{|\mathcal{A}|}.
$$

### What probability each non-greedy action receives

Each non-greedy action gets

$$
\frac{\epsilon}{|\mathcal{A}|}.
$$

### What this guarantees

Every action keeps at least some positive probability as long as $\epsilon > 0$.

That matters for exploration.

---

## 8. SARSA

SARSA is an on-policy action-value TD method.

Its one-step target is

$$
R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}),
$$

where $A_{t+1}$ is the actual next action selected by the current behavior policy.

### What is being sampled

The next action is sampled from the current policy.

### What this means

The target evaluates the continuation induced by the same policy that is generating behavior.

That is why the method is on-policy.

---

## 9. Q-learning

Q-learning uses the target

$$
R_{t+1} + \gamma \max_{a'} Q(S_{t+1}, a').
$$

### What changes relative to SARSA

The next action is no longer the action actually sampled from the current behavior policy.

Instead, the target inserts a greedy maximization over next actions.

### Why this matters

That one substitution changes the role of the target:

- SARSA evaluates the policy actually being followed,
- Q-learning targets the greedy continuation value instead.

This is the exact conceptual fork between them.

---

## 10. The decisive comparison: SARSA versus Q-learning

These methods are often presented as two update rules with almost identical notation.  
That presentation hides the real difference.

### What SARSA checks

At the next state, what action did the current policy actually choose?

### What Q-learning checks

At the next state, what action would maximize the current action-value estimate?

### Consequence

SARSA’s target depends on the behavior policy’s sampled continuation.  
Q-learning’s target depends on a greedy target continuation.

This is why SARSA is on-policy and Q-learning is typically off-policy.

---

## 11. Comparative map of the chapter

It helps to classify each method by the axes it uses.

### Dynamic programming

- model known,
- exact expectation under the model,
- planning rather than direct learning from raw samples.

### Monte Carlo

- model need not be known,
- complete sampled return,
- no bootstrap.

### TD prediction

- model need not be known,
- one-step sampled target,
- bootstrap from current estimate.

### SARSA

- action-value TD control,
- sampled next action from the current policy,
- on-policy.

### Q-learning

- action-value TD control,
- greedy maximization in the target,
- typically off-policy.

When learners confuse methods, it is usually because they have lost track of one of these axes.

---

## 12. Common confusions blocked here

### Confusion 1: Dynamic programming and TD are the same idea

They are related structurally, but not the same.

Dynamic programming uses exact model-based expectations.  
TD uses sampled transitions.

### Confusion 2: Monte Carlo and TD differ because one is “better”

No.  
They differ first in the target they use.

### Confusion 3: SARSA and Q-learning are almost the same because the formulas look similar

No.  
The conceptual fork is exactly at the continuation term.

### Confusion 4: On-policy versus off-policy is about whether exploration is used

No.  
It is about the relation between the policy generating data and the policy appearing inside the target.

---

## 13. Mastery check

You understand this chapter if you can answer all of these precisely.

1. What makes dynamic programming a planning method rather than a sample-based method?
2. What exact target does Monte Carlo use, and what exact target does one-step TD use?
3. What does it mean for a method to bootstrap?
4. What is the difference between a behavior policy and a target policy?
5. At the next state, what does SARSA condition on that Q-learning replaces by a maximization?

If any one of those comparisons is still blurry, tighten it before moving on.  
This chapter is where learners often start mixing names instead of understanding mechanisms.
