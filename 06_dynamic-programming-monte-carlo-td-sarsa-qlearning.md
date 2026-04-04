# Chapter 5 — Dynamic Programming, Monte Carlo, TD, SARSA, and Q-Learning

## What this chapter establishes

This chapter explains how Bellman equations become learning or planning procedures.

By the end, you should know:

- how dynamic programming uses exact model knowledge,
- how Monte Carlo uses complete sampled returns,
- how temporal-difference learning uses one-step bootstrapping,
- how behavior and target policies differ,
- and exactly where SARSA and Q-learning diverge.

---

## 1. Dynamic programming

For a fixed policy \(\pi\), define iterative policy evaluation by

\[
V_{k+1} = T^\pi V_k.
\]

### What is being updated

- \(V_k\) is the current value estimate after iteration \(k\),
- \(T^\pi\) is the Bellman expectation operator for the known model and policy.

### Why this converges

Because \(T^\pi\) is a \(\gamma\)-contraction, repeated application converges to its unique fixed point, which is \(V^\pi\).

### What assumptions are required

- the model \(P(s',r \mid s,a)\) is known,
- the state and action spaces are finite or otherwise manageable,
- \(0 \le \gamma < 1\) in the continuing discounted setting.

### Value iteration

Similarly,

\[
V_{k+1} = T^*V_k
\]

converges to \(V^*\) under the same contraction logic.

### What dynamic programming is and is not

It is **planning with a known model**.  
It is not a sample-based learning method from raw experience alone.

---

## 2. Monte Carlo estimation

Suppose you follow a policy and wait until the episode terminates.  
For a state \(s\), every visit gives a complete sampled return \(G_t\) following that visit.

An empirical estimator is the average of those observed returns:

\[
\widehat V_N(s) = \frac{1}{N}\sum_{i \in \mathcal{I}(s)} G_t^{(i)},
\]

where \(\mathcal{I}(s)\) indexes the visits to state \(s\).

### What Monte Carlo uses

It uses the **full realized return** after the state is visited.

### What Monte Carlo does not use

It does not bootstrap from the current estimate.  
That is the defining difference from temporal-difference methods.

### Strength and weakness

- strength: the target is directly tied to actual observed long-run outcomes,
- weakness: you must wait until enough future rewards are observed to form the return target.

---

## 3. Temporal-difference learning

Start from the Bellman expectation equation for the value of a state under policy \(\pi\):

\[
V^\pi(S_t) = \mathbb{E}_\pi[R_{t+1} + \gamma V^\pi(S_{t+1}) \mid S_t].
\]

Replace the conditional expectation by the one sampled transition that actually occurred.  
This gives the one-step TD target

\[
Y_t^{\mathrm{TD}} = R_{t+1} + \gamma V(S_{t+1}).
\]

Define the TD error

\[
\delta_t = Y_t^{\mathrm{TD}} - V(S_t)
= R_{t+1} + \gamma V(S_{t+1}) - V(S_t).
\]

Then update by

\[
V(S_t) \leftarrow V(S_t) + \alpha \delta_t.
\]

### What changed relative to the Bellman equation

The Bellman equation is an expectation identity.  
The TD update uses a single observed transition as a noisy estimator of that expectation.

### Why this is called bootstrapping

The target includes the current estimate \(V(S_{t+1})\).  
So the method learns partly from data and partly from its own current predictions.

---

## 4. Monte Carlo versus TD: exact distinction

The clean distinction is the target.

### Monte Carlo target

The target is the complete sampled return \(G_t\).

### TD target

The target is

\[
R_{t+1} + \gamma V(S_{t+1}),
\]

which uses a one-step sample plus a bootstrap term.

### What this means

- Monte Carlo does **not** bootstrap.
- TD **does** bootstrap.

That is the exact distinction.  
Do not blur it with vague statements like “TD is faster” or “Monte Carlo is more accurate.” Those may be context-dependent consequences, not the definition.

---

## 5. Behavior policy and target policy

The behavior policy is the policy that generates the data.  
The target policy is the policy whose value is being estimated or improved.

These can be the same or different.

### Why this distinction matters

On-policy and off-policy methods are classified by this distinction.

- If the same policy both generates the data and appears inside the target, the method is on-policy.
- If the data come from one policy while the target corresponds to another, the method is off-policy.

This is one of the most important checks in RL.

---

## 6. \(\epsilon\)-greedy exploration

Assume a finite action set \(\mathcal{A}\) and a unique greedy action \(a_g(s)\).

Under an \(\epsilon\)-greedy policy:

- with probability \(1-\epsilon\), choose the greedy action,
- with probability \(\epsilon\), choose uniformly among all \(|\mathcal{A}|\) actions.

So the greedy action receives probability

\[
1-\epsilon + \frac{\epsilon}{|\mathcal{A}|},
\]

and every nongreedy action receives

\[
\frac{\epsilon}{|\mathcal{A}|}.
\]

### Exact lower bound

Every action has probability at least

\[
\frac{\epsilon}{|\mathcal{A}|}.
\]

### Why ties matter

If multiple actions are greedy, the exact probability assigned to each greedy action depends on the tie-breaking rule.  
But the lower bound \(\epsilon/|\mathcal{A}|\) still holds when uniform random exploration is used over all actions.

---

## 7. SARSA

Start from the Bellman expectation equation for action value under the current policy \(\pi\):

\[
Q^\pi(s,a)
=
\mathbb{E}_\pi[R_{t+1} + \gamma Q^\pi(S_{t+1}, A_{t+1}) \mid S_t=s, A_t=a].
\]

Replace the conditional expectation by the sampled transition and the sampled next action \(A_{t+1}\).  
This gives the SARSA target

\[
Y_t^{\mathrm{SARSA}}
=
R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}).
\]

Define the error

\[
\delta_t^{\mathrm{SARSA}}
=
R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t,A_t).
\]

Update by

\[
Q(S_t,A_t)
\leftarrow
Q(S_t,A_t) + \alpha \delta_t^{\mathrm{SARSA}}.
\]

### Why SARSA is on-policy

The target uses the action \(A_{t+1}\) actually sampled from the current behavior policy.  
So the target is evaluating the same policy that is generating the data.

---

## 8. Q-learning

Start from the Bellman optimality equation for action value:

\[
Q^*(s,a)
=
\mathbb{E}[R_{t+1} + \gamma \max_{a'}Q^*(S_{t+1},a') \mid S_t=s, A_t=a].
\]

Replace the conditional expectation by the sampled transition.  
This gives the Q-learning target

\[
Y_t^{\mathrm{QL}}
=
R_{t+1} + \gamma \max_{a'} Q(S_{t+1},a').
\]

Define the error

\[
\delta_t^{\mathrm{QL}}
=
R_{t+1} + \gamma \max_{a'}Q(S_{t+1},a') - Q(S_t,A_t).
\]

Update by

\[
Q(S_t,A_t)
\leftarrow
Q(S_t,A_t) + \alpha \delta_t^{\mathrm{QL}}.
\]

### Why Q-learning is off-policy

The next action used in the target is not the action actually sampled by the behavior policy.  
The target uses the maximizing action instead.

So the behavior policy may explore, but the target corresponds to the greedy policy implied by the current value estimate.

---

## 9. Exact comparison: SARSA versus Q-learning

The difference is entirely localized in the target.

### SARSA target

\[
R_{t+1} + \gamma Q(S_{t+1}, A_{t+1})
\]

The next action \(A_{t+1}\) is the one actually sampled.

### Q-learning target

\[
R_{t+1} + \gamma \max_{a'} Q(S_{t+1},a')
\]

The next action is replaced by the maximizing action, whether or not that action was sampled.

### What this means operationally

- SARSA learns the value of the policy actually being followed.
- Q-learning learns toward the greedy policy implied by current estimates, while data may come from an exploratory behavior policy.

That is the precise distinction.  
Do not replace it with vague intuition.

---

## 10. Common confusions blocked here

### Confusion 1: dynamic programming and TD are the same because both use Bellman equations

No.

- Dynamic programming uses the exact model and computes expectations directly.
- TD uses sampled transitions and stochastic approximation.

### Confusion 2: Monte Carlo is just TD with a bigger horizon

No.

The essential difference is not horizon length.  
It is whether the target bootstraps from a current estimate.

### Confusion 3: on-policy means “the policy currently stored in memory”

No.

The correct check is whether the policy used inside the target is the same as the policy that generated the data.

### Confusion 4: Q-learning is greedy only when behavior is greedy

False.

Q-learning can behave exploratorily and still be off-policy because the target itself is greedy.

---

## 11. Mastery check

You understand this chapter if you can answer all of these precisely.

1. What assumption lets policy evaluation by \(V_{k+1}=T^\pi V_k\) converge?
2. What makes Monte Carlo “not bootstrapped”?
3. In TD learning, what part of the target comes from data and what part comes from the current estimate?
4. Why is SARSA on-policy?
5. Why is Q-learning off-policy even when data are collected using exploration?

If any answer sounds casual rather than exact, review before moving on.
