# Chapter 2 — Mathematical Preliminaries

## What this chapter establishes

This chapter fixes the probability and convergence facts used later in Bellman equations and policy gradients.

By the end of the chapter, you should know:

- what expectations and conditional expectations mean in the discrete setting,
- how the law of total expectation is used,
- why the discounted return is well-defined under bounded rewards and \(0 \le \gamma < 1\),
- how trajectory probabilities factorize in finite-horizon Markov problems,
- and why the log-derivative identity is enough to derive REINFORCE.

---

## 1. Standing assumptions

Unless a later subsection says otherwise, use these assumptions.

### Assumption 1: finite sums mean finite spaces

Whenever a formula is written as a sum over states or actions, the chapter is assuming a finite state space or action space, or at least a countable space for which the sum is meaningful.

If the space is continuous, the sum must be replaced by an integral and probabilities must be replaced by densities where appropriate.

### Assumption 2: rewards are uniformly bounded

There exists a constant \(R_{\max} \ge 0\) such that

\[
|R_t| \le R_{\max}
\]

almost surely for every time index \(t\).

This assumption is what lets discounted returns stay finite in continuing tasks.

### Assumption 3: discounting for continuing tasks

For continuing tasks, assume

\[
0 \le \gamma < 1.
\]

If \(\gamma = 1\) in a continuing task, then the return can diverge unless extra structure is imposed.  
So the default continuing-task theory here does **not** allow \(\gamma = 1\).

### Assumption 4: finite-horizon policy-gradient derivations

When the text derives policy gradients from sums over trajectories, it assumes:

- a finite horizon \(T\),
- a differentiable policy \(\pi_\theta\),
- and a finite trajectory space or conditions strong enough to justify exchanging derivative and summation.

---

## 2. Expectation

Let \(X\) be a discrete random variable on a finite or countable set \(\mathcal{X}\). Then

\[
\mathbb{E}[X] = \sum_{x \in \mathcal{X}} x \, P(X=x),
\]

provided the sum converges absolutely.

### What this means

Expectation is a weighted average of possible values, where the weights are probabilities.

### Why this matters in RL

Every value function later is an expectation of return under some conditioning event, such as \(S_t = s\) or \((S_t=s, A_t=a)\).

So if expectation is not conceptually stable, value functions will not be stable either.

---

## 3. Conditional expectation

If \(X\) and \(Y\) are discrete random variables, then the conditional expectation of \(X\) given \(Y=y\) is

\[
\mathbb{E}[X \mid Y=y] = \sum_x x \, P(X=x \mid Y=y).
\]

### What this checks

Conditioning changes the probability weights.  
The possible values of \(X\) do not change, but the probability assigned to each value may change once \(Y=y\) is known.

### Why this matters in RL

Bellman equations are conditional expectations.  
For example, \(V^\pi(s)\) is not the unconditional expectation of return. It is the expectation of return **conditional on** the state being \(s\).

That conditioning is the whole point.

---

## 4. Law of total expectation

The law of total expectation says

\[
\mathbb{E}[X] = \sum_y P(Y=y)\mathbb{E}[X \mid Y=y].
\]

### What the identity means

To compute the overall expectation of \(X\), you may:

1. split according to the possible values of \(Y\),
2. compute the expected value of \(X\) inside each case,
3. then average those case-specific expectations using the probabilities of the cases.

### Why this matters in RL

This identity is used constantly in Bellman derivations.  
You condition on the next state, or the next state and reward, and then average over those outcomes.

### What conclusion this licenses

Whenever you see a Bellman expectation equation, the formal move behind it is almost always:

- write an expectation conditional on the current state or state-action,
- condition again on the next transition outcome,
- then average over those outcomes.

---

## 5. Discounted return and why it converges

Define the return from time \(t\) by

\[
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}.
\]

### Why the index starts at \(k=0\)

When \(k=0\), the reward term is \(R_{t+1}\), which is the immediate reward caused by action \(A_t\).

### Why the reward index is \(t+k+1\)

The reward observed one step after time \(t\) is \(R_{t+1}\).  
Two steps after time \(t\) it is \(R_{t+2}\), and so on.  
So the \(k\)-th discounted term must be \(R_{t+k+1}\).

### Why the infinite sum is well-defined

Under bounded rewards and \(0 \le \gamma < 1\),

\[
|G_t|
\le \sum_{k=0}^{\infty} \gamma^k |R_{t+k+1}|
\le \sum_{k=0}^{\infty} \gamma^k R_{\max}
= R_{\max}\sum_{k=0}^{\infty}\gamma^k
= \frac{R_{\max}}{1-\gamma}.
\]

So the series converges absolutely and \(G_t\) is uniformly bounded.

### What conclusion this licenses

Once this bound is established, value functions such as \(V^\pi(s)=\mathbb{E}[G_t \mid S_t=s]\) are at least well-defined under the standing assumptions.

Without this step, later Bellman derivations would be manipulating an object that might not even exist.

---

## 6. Trajectory distributions in a finite-horizon Markov model

For a finite-horizon episodic task with horizon \(T\), define the trajectory

\[
\tau = (s_0, a_0, r_1, s_1, a_1, r_2, \ldots, s_{T-1}, a_{T-1}, r_T, s_T).
\]

Let \(\rho(s_0)\) be the initial-state distribution.  
If the policy is \(\pi\) and the environment law is \(P(s',r \mid s,a)\), then

\[
p_\pi(\tau)
=
\rho(s_0)\prod_{t=0}^{T-1}
\pi(a_t \mid s_t)
P(s_{t+1}, r_{t+1} \mid s_t, a_t).
\]

### What this factorization checks

At each time \(t\), exactly two stochastic choices matter:

1. the policy chooses \(a_t\) from \(s_t\),
2. the environment produces \((s_{t+1}, r_{t+1})\) from \((s_t, a_t)\).

Multiplying those factors across time gives the trajectory probability.

### Why this matters

Policy-gradient derivations differentiate expectations over trajectories.  
That is only manageable once the trajectory probability is written as a product of factors.

---

## 7. Gradients of expectations and the log-derivative identity

Suppose \(f(\tau)\) does not depend on the parameter vector \(\theta\). Then

\[
\nabla_\theta \sum_\tau p_\theta(\tau) f(\tau)
=
\sum_\tau \nabla_\theta p_\theta(\tau) f(\tau),
\]

under the finite-horizon, finite-sum assumptions.

Now use the identity

\[
\nabla_\theta \log p_\theta(\tau)
=
\frac{1}{p_\theta(\tau)} \nabla_\theta p_\theta(\tau),
\]

which can be rearranged as

\[
\nabla_\theta p_\theta(\tau)
=
p_\theta(\tau)\nabla_\theta \log p_\theta(\tau).
\]

### Why this identity matters

It converts derivatives of probabilities into probabilities multiplied by derivatives of log probabilities.  
That is exactly what turns a derivative of an expectation into an expectation of a score term.

### What conclusion this licenses

This is the algebraic core of REINFORCE.  
You do not need deeper calculus machinery to understand the basic policy-gradient derivation once this identity is available.

---

## 8. Boundary conditions that must stay explicit

### Case 1: \(\gamma = 1\) in continuing tasks

Do not assume the return is finite.  
It may diverge.

### Case 2: unbounded rewards

The geometric weighting alone does not automatically rescue the return if rewards can grow too quickly.

### Case 3: continuous state or action spaces

Finite sums must be replaced by integrals.  
The conceptual structure is the same, but the notation changes.

### Case 4: infinite-horizon policy gradients

You need stronger technical conditions to justify interchanging limits, differentiation, and expectation.  
This chapter avoids that complication by using finite-horizon derivations when differentiating over trajectories.

---

## 9. Common confusions blocked here

### Confusion 1: expectation and conditional expectation are basically the same

No.

- \(\mathbb{E}[X]\) averages over all uncertainty.
- \(\mathbb{E}[X \mid Y=y]\) averages only over the uncertainty left after conditioning on \(Y=y\).

Bellman equations are conditional statements, not unconditional ones.

### Confusion 2: discounting is only a preference convention

Discounting can encode preference, but in this chapter it is also doing mathematical work: it helps ensure the return is finite.

### Confusion 3: a trajectory probability is just a product of policy probabilities

False.  
It includes the initial-state probability and the environment transition-reward probabilities too.

---

## 10. Mastery check

You understand this chapter if you can explain all of these cleanly.

1. Why does bounded reward plus \(0 \le \gamma < 1\) imply the return is finite?
2. When using the law of total expectation in RL, what random variable are you usually conditioning on?
3. In the trajectory factorization, which terms come from the policy and which come from the environment?
4. Why is the log-derivative identity useful in policy gradients?
5. Under what condition is it unsafe to use the infinite discounted-return formula without further justification?

If any answer is fuzzy, stop there.  
The rest of the theory depends on these preliminaries.
