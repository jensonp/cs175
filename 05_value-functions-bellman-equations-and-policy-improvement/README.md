# Chapter 4 — Value Functions, Bellman Equations, and Policy Improvement

## What this chapter establishes

This chapter converts the long-run objective into local recursive quantities.

By the end, you should know:

- how \(V^\pi\), \(Q^\pi\), and \(A^\pi\) are defined,
- how Bellman expectation equations are derived,
- what Bellman operators are,
- why contraction matters,
- how optimality equations differ from expectation equations,
- and why greedy improvement is justified.

---

## 1. Value functions and advantage

For a fixed policy \(\pi\), define the state value

\[
V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t=s],
\]

and the action value

\[
Q^\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a].
\]

The advantage is

\[
A^\pi(s,a) = Q^\pi(s,a) - V^\pi(s).
\]

### What each quantity means

- \(V^\pi(s)\): expected return if the current state is \(s\) and the policy \(\pi\) is followed from now on.
- \(Q^\pi(s,a)\): expected return if the current state is \(s\), the current action is forced to be \(a\), and the policy \(\pi\) is followed after that.
- \(A^\pi(s,a)\): how much better or worse action \(a\) is than the policy’s average behavior at state \(s\).

### Important classification

These are **definitions**, not derived formulas.

---

## 2. Relation between \(V^\pi\) and \(Q^\pi\)

Condition on the action chosen by policy \(\pi\) in state \(s\). Then

\[
V^\pi(s) = \sum_a \pi(a \mid s) Q^\pi(s,a).
\]

### Why this is true

Given \(S_t=s\), the next random choice controlled by the policy is \(A_t\).  
The possible action values are \(Q^\pi(s,a)\), and the policy probabilities \(\pi(a \mid s)\) are the weights.

### What this means

\(V^\pi(s)\) is a weighted average of action values under the action distribution used by the policy in that state.

This fact is used repeatedly in policy improvement and Bellman derivations.

---

## 3. Bellman expectation equation for \(V^\pi\)

Start from the definition

\[
V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t=s].
\]

Use the return recursion

\[
G_t = R_{t+1} + \gamma G_{t+1}.
\]

Substitute it into the definition:

\[
V^\pi(s)
=
\mathbb{E}_\pi[R_{t+1} + \gamma G_{t+1} \mid S_t=s].
\]

Now condition on the action \(A_t\), the next state \(S_{t+1}\), and the next reward \(R_{t+1}\).  
That yields

\[
V^\pi(s)
=
\sum_a \pi(a \mid s)
\sum_{s',r}
P(s',r \mid s,a)
\left[r + \gamma V^\pi(s')\right].
\]

### What operations were used

1. substitute the return recursion,
2. condition on the current action,
3. condition on the next state and reward,
4. recognize that the continuation value from next state \(s'\) is \(V^\pi(s')\).

### What conclusion this licenses

This is the Bellman expectation equation for state value.  
It is an exact identity, not a sampled approximation.

---

## 4. Bellman expectation equation for \(Q^\pi\)

Start from

\[
Q^\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a].
\]

Again substitute the return recursion:

\[
Q^\pi(s,a)
=
\mathbb{E}_\pi[R_{t+1} + \gamma G_{t+1} \mid S_t=s, A_t=a].
\]

Now condition on the next state and reward:

\[
Q^\pi(s,a)
=
\sum_{s',r}
P(s',r \mid s,a)
\left[
r + \gamma \mathbb{E}_\pi[G_{t+1} \mid S_{t+1}=s']
\right].
\]

The continuation expectation from next state \(s'\) is \(V^\pi(s')\), or equivalently

\[
V^\pi(s') = \sum_{a'}\pi(a' \mid s')Q^\pi(s',a').
\]

So

\[
Q^\pi(s,a)
=
\sum_{s',r}
P(s',r \mid s,a)
\left[
r + \gamma \sum_{a'} \pi(a' \mid s')Q^\pi(s',a')
\right].
\]

### What conclusion this licenses

This is the Bellman expectation equation for action value.

Again, it is exact.

---

## 5. Bellman operators

Define the Bellman expectation operator for a fixed policy \(\pi\):

\[
(T^\pi V)(s)
=
\sum_a \pi(a \mid s)
\sum_{s',r}
P(s',r \mid s,a)\left[r + \gamma V(s')\right].
\]

Define the Bellman optimality operator

\[
(T^* V)(s)
=
\max_a
\sum_{s',r}
P(s',r \mid s,a)\left[r + \gamma V(s')\right].
\]

### Why operators are useful

The Bellman equations can now be written as fixed-point equations:

- \(V^\pi = T^\pi V^\pi\)
- \(V^* = T^* V^*\)

This turns the control problem into a fixed-point problem.

---

## 6. Contraction property

Under bounded value functions and \(0 \le \gamma < 1\), both \(T^\pi\) and \(T^*\) are \(\gamma\)-contractions in the supremum norm.

That means

\[
\|T^\pi V - T^\pi W\|_\infty \le \gamma \|V-W\|_\infty,
\]

and similarly for \(T^*\).

### Why the proof works

For \(T^\pi\), the difference between \((T^\pi V)(s)\) and \((T^\pi W)(s)\) is a weighted average of terms of the form \(\gamma(V(s')-W(s'))\).

Three checks matter.

1. The absolute difference \(|V(s')-W(s')|\) is bounded above by \(\|V-W\|_\infty\).
2. The transition probabilities sum to \(1\) for each \((s,a)\).
3. The policy probabilities sum to \(1\) for each \(s\).

So the only surviving multiplicative factor is \(\gamma\).

### What conclusion this licenses

A contraction has a unique fixed point, and repeated application converges to that fixed point.  
That is why policy evaluation and value iteration work in the discounted finite-state setting.

---

## 7. Optimality equations

Define optimal value functions by

\[
V^*(s) = \max_\pi V^\pi(s),
\qquad
Q^*(s,a) = \max_\pi Q^\pi(s,a).
\]

Then

\[
V^*(s)
=
\max_a
\sum_{s',r}
P(s',r \mid s,a)
\left[r + \gamma V^*(s')\right],
\]

and

\[
Q^*(s,a)
=
\sum_{s',r}
P(s',r \mid s,a)
\left[r + \gamma \max_{a'}Q^*(s',a')\right].
\]

### Why these differ from the expectation equations

In the expectation equations, the continuation action is averaged under a fixed policy \(\pi\).  
In the optimality equations, the continuation action is chosen to maximize long-run value.

So the expectation equations are about evaluation of a given policy.  
The optimality equations are about the best achievable continuation.

---

## 8. Policy improvement theorem

Let \(\pi\) be a policy, and define a greedy policy \(\pi'\) by selecting an action that maximizes \(Q^\pi(s,a)\) at each state \(s\).

Then

\[
V^{\pi'}(s) \ge V^\pi(s)
\quad \text{for every state } s.
\]

### Why the first step works

Because

\[
V^\pi(s) = \sum_a \pi(a \mid s)Q^\pi(s,a),
\]

the value \(V^\pi(s)\) is a weighted average of the numbers \(Q^\pi(s,a)\).  
A weighted average cannot exceed the maximum of the numbers being averaged.

So

\[
V^\pi(s) \le \max_a Q^\pi(s,a) = Q^\pi(s,\pi'(s)).
\]

### Why that is enough

Once the greedy action is at least as good as the old policy’s average action at each state, repeated Bellman application under \(\pi'\) pushes the value no lower, and contraction plus monotonicity yields

\[
V^{\pi'} \ge V^\pi.
\]

### What conclusion this licenses

Greedy improvement with respect to the current action-value function is justified.  
It is not a heuristic guess.

---

## 9. Generalized policy iteration

Generalized policy iteration means alternating between two coupled processes:

1. **policy evaluation** — estimate how good the current policy is,
2. **policy improvement** — change the policy to prefer better actions.

These two processes need not finish completely before the other begins.  
They may be exact or approximate, synchronous or interleaved.

### Why this concept matters

Dynamic programming, Monte Carlo control, TD control, SARSA, Q-learning, and actor-critic methods all fit this template, even though their update rules differ.

The structural backbone is the same:

- evaluate,
- improve,
- repeat.

---

## 10. Common confusions blocked here

### Confusion 1: \(V^\pi\) and \(Q^\pi\) are different notations for the same thing

False.

- \(V^\pi(s)\) conditions only on the state.
- \(Q^\pi(s,a)\) conditions on both state and current action.

### Confusion 2: a Bellman equation is an approximation

Not here.  
The Bellman expectation and optimality equations are exact under the MDP assumptions.

### Confusion 3: contraction is just a technical curiosity

No.  
Contraction is the reason the Bellman fixed point is unique and iterative application converges.

### Confusion 4: policy improvement says a greedy step gives the optimal policy immediately

No.  
It says the greedy policy is no worse than the old one. Repeated improvement is what moves you toward optimality.

---

## 11. Mastery check

You understand this chapter if you can explain all of these cleanly.

1. Why is \(V^\pi(s)\) a weighted average of \(Q^\pi(s,a)\)?
2. In the Bellman expectation equation for \(V^\pi\), what random variables are summed over and why?
3. What is the difference between \(T^\pi\) and \(T^*\)?
4. Why does the factor \(\gamma\) appear in the contraction bound?
5. What does the policy improvement theorem prove, and what does it not prove?

These are foundational.  
Do not move on until each answer is precise.
