# Chapter 2 — Mathematical Preliminaries

## What this chapter locks in

This chapter installs the probability tools that later chapters use inside Bellman equations, return definitions, and policy-gradient derivations.

The point is not to collect detached formulas.  
The point is to make later derivations readable and checkable.

By the end of this chapter, you should know:

- what expectation checks,
- what conditioning changes and what it does not change,
- how the law of total expectation is used inside recursive RL derivations,
- why discounted return is mathematically well-defined under the usual assumptions,
- how a finite-horizon trajectory law factorizes into local policy and environment factors,
- and how the log-derivative identity turns a derivative of a probability law into an expectation-friendly form.

This chapter is mostly about *what the formulas are actually saying*.

---

## 1. Standing assumptions

Whenever a formula in this chapter needs assumptions, those assumptions should be visible.

### Finite or countable spaces when sums are written

If a formula is written as a sum over states, actions, rewards, or trajectories, then the presentation is assuming a finite or countable space so the sum makes literal sense.

If the space is continuous, the same logic often survives, but:

- sums become integrals,
- probabilities become densities when appropriate,
- and technical conditions need to be checked more carefully.

So the discrete presentation is for clarity, not because the subject only exists in discrete spaces.

### Bounded rewards

Assume there exists a finite constant $R_{\max} \ge 0$ such that

$$
|R_t| \le R_{\max}
$$

almost surely for every relevant time index.

This assumption is especially important when you want infinite discounted sums to stay controlled.

### Discounting in continuing tasks

For continuing tasks, assume

$$
0 \le \gamma < 1.
$$

If $\gamma = 1$ in a genuinely infinite-horizon continuing problem, the return may fail to converge unless extra structure is imposed.

### Finite horizon for trajectory-differentiation arguments

When this chapter differentiates expectations over complete trajectories, assume:

- a finite horizon $T$,
- a differentiable parameterized policy $\pi_\theta$,
- and enough regularity to interchange derivative and summation.

Those assumptions do not appear because we enjoy technical clutter.  
They appear because a derivation only counts if the manipulations are justified.

---

## 2. Random variables and what expectation does

Let $X$ be a discrete random variable taking values in a finite or countable set $\mathcal{X}$.

Then

$$
\mathbb{E}[X] = \sum_{x \in \mathcal{X}} x \, P(X=x),
$$

provided the sum is well-defined.

### What expectation checks

Expectation does **not** ask which value occurs on one sample path.  
Expectation asks for the probability-weighted average across possible values.

So two ingredients always matter:

- the values $x$ that $X$ can take,
- and the weights $P(X=x)$ attached to those values.

If either ingredient is fuzzy, expectation becomes a slogan instead of an object.

### Why RL needs this immediately

Later, a value function will be an expectation of return.  
That means a value function is not a mysterious new species of quantity.  
It is a conditional expectation built from the same rule you see here.

So if expectation itself is unstable, value functions will also feel unstable.

---

## 3. Conditional expectation

If $X$ and $Y$ are random variables, then the conditional expectation of $X$ given $Y=y$ is

$$
\mathbb{E}[X \mid Y=y].
$$

In a discrete setting, this can be written as

$$
\mathbb{E}[X \mid Y=y]
= \sum_x x \, P(X=x \mid Y=y).
$$

### What conditioning changes

Conditioning does **not** change the possible values of $X$.

It changes the probability weights attached to those values after the event $Y=y$ has been specified.

This distinction is basic and critical.

When you condition, you are not inventing a new random variable with new outcomes.  
You are reweighting the same possible values according to the information now being held fixed.

### What conditioning means procedurally

To compute $\mathbb{E}[X \mid Y=y]$:

1. fix the event $Y=y$,
2. re-evaluate the probabilities of the possible values of $X$ under that condition,
3. then average the values of $X$ using those new weights.

### Why RL depends on this

Later, when you see something like

$$
V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t=s],
$$

the important words are not only *expected return*.  
The important words are *expected return conditional on the current state being $s$*.

That conditioning event is the whole point.

---

## 4. The law of total expectation

Suppose you want an expectation of $X$, and another random variable $Y$ divides the world into cases.

Then the law of total expectation says

$$
\mathbb{E}[X] = \sum_y P(Y=y)\,\mathbb{E}[X \mid Y=y].
$$

### What this says

To compute the overall expectation of $X$, you may:

1. split the world into cases indexed by $Y$,
2. compute the expected value of $X$ inside each case,
3. then average those case-specific expectations using the probabilities of the cases.

### Why this matters later

Bellman derivations use this move repeatedly.

A typical Bellman derivation starts with a conditional expectation and then splits according to one more random choice or one more transition outcome:

- next action,
- next state,
- next reward,
- or a joint next-step outcome.

If you can track that split, Bellman equations stop looking like magic and start looking like ordinary probabilistic bookkeeping.

---

## 5. Tower property and nested conditioning

A closely related fact is the tower property.

If $Z$ is another variable or sigma-field that is coarser than the full information being conditioned on, then nested conditional expectations can often be collapsed in the appropriate order.

In the discrete intuition most readers need first, the idea is simple:

- condition on more information,
- compute an inner expectation,
- then average back out over some of that information.

This is the structural reason recursive equations are legal.

You do not need abstract measure theory to grasp the operational point.  
You do need to understand that expectations can be taken in stages without changing the final quantity when the conditioning is handled correctly.

---

## 6. Return and its indexing

Define the discounted return from time $t$ by

$$
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}.
$$

Every index in this formula is doing work.

### Why the first reward is $R_{t+1}$

At time $t$, the action chosen is $A_t$.  
The first reward caused by that action is observed only after the environment reacts.  
So the first post-decision reward in the return from time $t$ is $R_{t+1}$.

### Why the generic term is $R_{t+k+1}$

When $k=0$, the term is one step after decision time $t$.  
When $k=1$, it is two steps after decision time $t$.  
So the $k$-th future reward is indexed $t+k+1$.

### Why the power on $\gamma$ is $k$

The factor $\gamma^k$ discounts the reward that occurs $k+1$ post-decision steps after time $t$.

If you keep the reward index and the discount exponent aligned in this way, later recursions become transparent.

---

## 7. The return recursion

From the definition of $G_t$ above, you can separate the first reward term from the remaining tail:

$$
G_t
= R_{t+1} + \gamma \sum_{k=0}^{\infty} \gamma^k R_{t+k+2}.
$$

The remaining infinite sum is exactly $G_{t+1}$, so

$$
G_t = R_{t+1} + \gamma G_{t+1}.
$$

### What this proves

This recursion is an **algebraic identity** that follows directly from the definition of return.

It does not yet use the Markov property.  
It does not yet use value functions.  
It does not yet use Bellman theory.

That distinction matters.

The return recursion is always a statement about the return random variable itself.  
Later Bellman equations are statements about conditional expectations of return under additional structural assumptions.

---

## 8. Why discounted return is well-defined

Under bounded rewards and $0 \le \gamma < 1$,

$$
|G_t|
\le \sum_{k=0}^{\infty} \gamma^k |R_{t+k+1}|
\le \sum_{k=0}^{\infty} \gamma^k R_{\max}
= \frac{R_{\max}}{1-\gamma}.
$$

### What is checked first

The first check is absolute magnitude:

- each reward magnitude is at most $R_{\max}$,
- the discount weights form a geometric series,
- and the geometric series converges because $\gamma < 1$.

### What conclusion follows

The discounted return converges absolutely and is uniformly bounded by

$$
\frac{R_{\max}}{1-\gamma}.
$$

### Why this matters

Only after that bound is in place do objects like

$$
V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t=s]
$$

become respectable mathematical quantities under the standing assumptions.

This is a good example of the right order of reasoning:

1. check the random quantity is well-defined,
2. then build expectations of it,
3. then derive recursive identities involving those expectations.

Skipping step 1 is how people manipulate symbols that may not even denote finite quantities.

---

## 9. Episodic finite-horizon return

In a finite-horizon episodic task with terminal time $T$, the return from time $t$ may instead be written as

$$
G_t = \sum_{k=0}^{T-t-1} \gamma^k R_{t+k+1}.
$$

Here the upper limit is finite, so convergence is no longer the issue.  
Instead, the important boundary condition is the last available reward inside the episode.

If the last chosen action is $A_{T-1}$, then the last immediate reward term is $R_T$.

This finite-horizon version is the one that naturally appears in many policy-gradient derivations because the trajectory length is controlled.

---

## 10. Finite-horizon trajectory distributions

Now move from single random variables to whole trajectories.

For a finite-horizon episodic problem with horizon $T$, define a trajectory by

$$
\tau = (s_0, a_0, r_1, s_1, a_1, r_2, \ldots, s_{T-1}, a_{T-1}, r_T, s_T).
$$

Let $\rho(s_0)$ denote the initial-state distribution.

If the policy is $\pi$ and the one-step environment law is $P(s', r \mid s, a)$, then the trajectory probability is

$$
p_\pi(\tau)
=
\rho(s_0)
\prod_{t=0}^{T-1}
\pi(a_t \mid s_t)\,
P(s_{t+1}, r_{t+1} \mid s_t, a_t).
$$

### What is checked at each time index

At each time $t$ in the product:

- the policy contributes the factor for choosing $a_t$ given $s_t$,
- the environment contributes the factor for producing $(s_{t+1}, r_{t+1})$ given $(s_t, a_t)$.

The full trajectory law is obtained by multiplying these local factors across time.

### Why this factorization matters

Later policy-gradient derivations work with expectations over complete trajectories.  
Those expectations become manageable only after the law of the trajectory has been decomposed into factors that correspond to the local mechanics of the process.

Without that factorization, “differentiate the expected return” is too opaque to handle.

---

## 11. Expectations over trajectories

If $f(\tau)$ is any function of the full trajectory, then under the finite-horizon discrete setup,

$$
\mathbb{E}_{\pi}[f(\tau)]
=
\sum_{\tau} p_\pi(\tau)\, f(\tau).
$$

This is the same expectation rule as before.  
The only thing that changed is the random object:

- earlier it was a scalar random variable,
- now it is a whole trajectory.

So the conceptual structure is identical: values of $\tau$ are weighted by their probabilities.

Later, when the function is total return or discounted return, the expectation becomes the performance objective.

---

## 12. Differentiating an expectation over trajectories

Suppose the policy is parameterized by $\theta$, and suppose $f(\tau)$ does not depend explicitly on $\theta$.

Under the finite-horizon regularity assumptions,

$$
\nabla_\theta \sum_\tau p_\theta(\tau) f(\tau)
=
\sum_\tau \nabla_\theta p_\theta(\tau) f(\tau).
$$

This step still leaves the hard part unresolved:

how do you differentiate $p_\theta(\tau)$ in a useful way?

That is where the log-derivative identity enters.

---

## 13. The log-derivative identity

The identity is

$$
\nabla_\theta \log p_\theta(\tau)
=
\frac{1}{p_\theta(\tau)} \nabla_\theta p_\theta(\tau),
$$

whenever $p_\theta(\tau) > 0$.

Rearranging gives

$$
\nabla_\theta p_\theta(\tau)
=
p_\theta(\tau)\, \nabla_\theta \log p_\theta(\tau).
$$

### What this changes

This converts a derivative of a probability into two factors:

- the probability itself,
- multiplied by a derivative of a log probability.

That matters because the probability factor can be folded back into an expectation.

So the derivation can move from

- “differentiate a probability law directly,”

to

- “take an expectation involving a score term.”

That is the central structural move behind policy-gradient formulas.

---

## 14. Why the score decomposes over time

From the factorized trajectory law,

$$
\log p_\theta(\tau)
=
\log \rho(s_0)
+
\sum_{t=0}^{T-1} \log \pi_\theta(a_t \mid s_t)
+
\sum_{t=0}^{T-1} \log P(s_{t+1}, r_{t+1} \mid s_t, a_t).
$$

If the environment dynamics do not depend on $\theta$, then differentiating with respect to $\theta$ removes every term except the policy terms:

$$
\nabla_\theta \log p_\theta(\tau)
=
\sum_{t=0}^{T-1} \nabla_\theta \log \pi_\theta(a_t \mid s_t).
$$

### What this licenses later

This is what allows policy-gradient derivations to express the gradient of performance in terms of policy log-probabilities along the trajectory, rather than derivatives of the environment law.

That is not a lucky trick.  
It is a direct consequence of factorization plus the assumption that the policy parameters do not control the environment dynamics.

---

## 15. Common confusions this chapter should block

### Confusion 1: expectation is the same as averaging observed samples

Not exactly.

Empirical sample averages estimate expectations.  
They are not the definition of expectation itself.

### Confusion 2: conditioning changes the values a random variable can take

No.

Conditioning changes the probability weights attached to those values.

### Confusion 3: the return recursion is already a Bellman equation

No.

$$
G_t = R_{t+1} + \gamma G_{t+1}
$$

is an identity about return.  
A Bellman equation is a recursive statement about conditional expectations of return, usually under Markov assumptions.

### Confusion 4: bounded rewards and $\gamma<1$ are decorative assumptions

No.

They are exactly what makes the infinite discounted return controlled in the standard continuing setup.

### Confusion 5: the log-derivative identity is a policy-gradient theorem by itself

Also no.

It is a mathematical tool that makes the theorem derivation possible.  
It is one step in the chain, not the whole chain.

---

## 16. What this chapter allows you to conclude

After this chapter, you are allowed to do all of the following responsibly.

1. Treat a value function as an expectation of return under explicit conditioning.
2. Split expectations according to next-step cases using the law of total expectation.
3. Use the return recursion as a clean algebraic identity.
4. State sufficient conditions under which the infinite discounted return is well-defined.
5. Write the probability of a finite-horizon trajectory as a product of local policy and environment terms.
6. Understand how derivatives of expected trajectory functionals become expectations involving policy log-probability gradients.

That is enough mathematical infrastructure for the next chapter to ask a sharper question:

when is a summary of history sufficient for one-step prediction and control?

---

## 17. Mastery check

You understand this chapter if you can answer each question without handwaving.

1. What does expectation average over?
2. What changes when you condition on an event such as $Y=y$?
3. What exactly does the law of total expectation let you do in a Bellman derivation?
4. Why is the return from time $t$ indexed with rewards $R_{t+1}, R_{t+2}, \ldots$?
5. Under what assumptions is the infinite discounted return bounded?
6. In the trajectory factorization, what factor is contributed by the policy and what factor is contributed by the environment at each time index?
7. Why does the log-derivative identity help convert a derivative of expected return into an expectation-friendly form?

If any answer is shaky, stop here and fix it.  
The next chapter depends on these facts being stable.
