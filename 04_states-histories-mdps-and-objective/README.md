# Chapter 3 — States, Histories, MDPs, and the Objective

## What this chapter establishes

This chapter answers three central questions.

1. What information does the agent actually have?
2. When is a state representation good enough to support Markov analysis?
3. What is the exact optimization objective?

By the end, you should know the difference between a history, a representation, a Markov state, an MDP, a return recursion, and the performance objective \(J(\pi)\).

---

## 1. Full interaction history

The complete interaction history available up to time \(t\) is

\[
H_t = (O_0, A_0, R_1, O_1, A_1, R_2, \ldots, O_t).
\]

### What is included and what is not

- It includes all observations up to time \(t\).
- It includes all past actions up to time \(t-1\).
- It includes all rewards up to time \(t\), which are indexed \(R_1,\ldots,R_t\).
- It does **not** include \(A_t\), because at the instant the history is available, action \(A_t\) has not yet been chosen.

That boundary matters.

---

## 2. State representations

A state representation is any mapping

\[
S_t = f(H_t).
\]

At this point, that is all a state is: a summary of the history.

### What this does **not** imply

This definition does **not** yet imply that \(S_t\) is Markov.  
A state representation can throw away information needed for future prediction.

So “state” in the broad representation sense and “Markov state” are not automatically the same thing.

### Why compress the history at all

The full history grows with time.  
A fixed-size representation is computationally manageable and often necessary for learning.

But compression is only safe if it preserves the information needed for the control problem.

---

## 3. The Markov property

The representation \(S_t\) is Markov if, once \(S_t\) and \(A_t\) are known, the earlier history adds no further predictive information about the next state and reward.

Formally,

\[
P(S_{t+1}, R_{t+1} \mid H_t, A_t)
=
P(S_{t+1}, R_{t+1} \mid S_t, A_t).
\]

### What this equality means

The left side conditions on the whole history and the current action.  
The right side conditions only on the current state summary and the current action.

If these are equal for all relevant histories and actions, then the state summary retains everything about the past that matters for one-step prediction of the controlled future.

### What conclusion this licenses

Once the Markov property holds, future analysis can be written in terms of \(S_t\) and \(A_t\) without loss.

That is what makes Bellman equations possible in the familiar finite-dimensional form.

---

## 4. Markov decision process definition

An MDP is the tuple

\[
(\mathcal{S}, \mathcal{A}, P, \rho, \gamma),
\]

where

- \(\mathcal{S}\) is the state space,
- \(\mathcal{A}\) is the action space,
- \(P(s', r \mid s, a)\) is the transition-reward law,
- \(\rho\) is the initial-state distribution,
- \(\gamma\) is the discount factor.

### What the transition-reward law means

For each current state-action pair \((s,a)\), the term

\[
P(s', r \mid s,a)
\]

gives the probability of moving to next state \(s'\) and receiving reward \(r\).

This notation keeps reward and transition together.  
That is often cleaner than separating the dynamics and expected reward prematurely.

### Optional derived quantity: expected immediate reward

If you want a separate expected reward function, define

\[
\bar r(s,a) = \sum_{s',r} r \, P(s', r \mid s,a).
\]

This is an expected one-step reward, not a long-run value.

---

## 5. Episodic versus continuing tasks

### Episodic task

An episodic task ends after a finite random number of steps.

There is a terminal condition, and once termination occurs, the episode stops.

### Continuing task

A continuing task has no built-in terminal time.

In that case, discounted returns are typically used with \(0 \le \gamma < 1\) so that the return stays finite under bounded rewards.

### Why this distinction matters

The same Bellman-style reasoning appears in both settings, but the boundary conditions differ:

- episodic tasks can sometimes allow \(\gamma = 1\),
- continuing tasks generally require discounting or another device to keep the objective well-defined.

---

## 6. Return recursion

The discounted return from time \(t\) is

\[
G_t = \sum_{k=0}^{\infty}\gamma^k R_{t+k+1}.
\]

Now derive the one-step recursion carefully.

Start by separating the first term, which is the \(k=0\) term:

\[
G_t = R_{t+1} + \sum_{k=1}^{\infty}\gamma^k R_{t+k+1}.
\]

Now change the index by setting

\[
j = k-1.
\]

### Why that change is valid

- when \(k=1\), the new index is \(j=0\),
- as \(k \to \infty\), the new index also tends to infinity.

So the remaining sum becomes

\[
\sum_{k=1}^{\infty}\gamma^k R_{t+k+1}
=
\sum_{j=0}^{\infty}\gamma^{j+1} R_{t+j+2}.
\]

Factor out one power of \(\gamma\):

\[
\sum_{j=0}^{\infty}\gamma^{j+1} R_{t+j+2}
=
\gamma \sum_{j=0}^{\infty}\gamma^j R_{t+j+2}.
\]

But the remaining series is exactly \(G_{t+1}\). Therefore

\[
G_t = R_{t+1} + \gamma G_{t+1}.
\]

### What conclusion this licenses

This recursion is exact.  
It is not a Bellman equation yet.  
It is just an identity about the return itself.

Bellman equations arise only after taking conditional expectations of this identity.

---

## 7. The objective

For a policy \(\pi\), define the performance objective

\[
J(\pi) = \mathbb{E}_\pi[G_0].
\]

### What the notation \(\mathbb{E}_\pi\) means

The expectation is taken under the probability law induced jointly by:

- the initial-state distribution \(\rho\),
- the environment transition-reward law \(P\),
- and the policy \(\pi\).

### What is being optimized

The control problem is

\[
\pi^* \in \arg\max_\pi J(\pi).
\]

So the objective is not to maximize immediate reward greedily at each step.  
It is to maximize the expected return from the start of interaction.

### If a maximizer does not exist

More generally one can write \(\sup_\pi J(\pi)\).  
But in the finite discounted setting emphasized here, optimal policies exist.

---

## 8. Why the state concept matters for the objective

A policy can, in principle, condition on the full history.  
So why insist on Markov states?

Because once the representation is Markov, long-horizon control can be analyzed locally through recursive objects:

- state values,
- action values,
- Bellman operators,
- dynamic programming,
- and temporal-difference targets.

Without a Markov representation, those local recursions may no longer be valid in the simple state-based form.

---

## 9. Common confusions blocked here

### Confusion 1: a state is whatever the observation happens to be

No.

The observation may be incomplete.  
A state representation can include memory or latent features derived from the history.

### Confusion 2: any compression of history is safe

False.

A compression is only safe for Markov analysis if it preserves the predictive information needed so that the future depends on the past only through the compressed state and current action.

### Confusion 3: the return recursion is already a Bellman equation

No.

\[
G_t = R_{t+1} + \gamma G_{t+1}
\]

is an identity about a random variable.  
A Bellman equation appears only after conditioning and taking expectations.

### Confusion 4: maximizing expected return is the same as maximizing each immediate reward

Only if the future does not matter, which is the degenerate case \(\gamma=0\).  
In general, a short-term sacrifice can increase long-run return.

---

## 10. Mastery check

You understand this chapter if you can explain all of these precisely.

1. What is included in \(H_t\), and why is \(A_t\) not part of it?
2. What is the difference between a general state representation and a Markov state?
3. What does \(P(s', r \mid s,a)\) encode?
4. Why is the return recursion exact before any expectation is taken?
5. What random mechanisms are included inside \(\mathbb{E}_\pi\) when defining \(J(\pi)\)?

If any answer is still hand-wavy, fix it now.  
Every later derivation depends on this chapter.
