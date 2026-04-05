# Chapter 7 — Policy Gradients, REINFORCE, Baselines, Actor-Critic, PPO, and SAC

## What this chapter establishes

This chapter moves from indirect policy optimization through value functions to direct optimization of a parameterized policy.

By the end, you should know:

- how the policy-gradient theorem is derived in finite horizon,
- why the log probability of a trajectory reduces to a sum of policy log probabilities,
- why reward-to-go is valid,
- why a state-dependent baseline does not change the expected gradient,
- how actor-critic approximates advantage information,
- what PPO clipping is actually doing,
- and how SAC changes the objective by adding entropy.

---

## 1. Parameterized policy and objective

Let \(\pi_\theta(a \mid s)\) be a differentiable stochastic policy with parameter vector \(\theta\).

For a finite-horizon episodic task of horizon \(T\), define the trajectory return

\[
G_0(\tau) = \sum_{t=0}^{T-1}\gamma^t R_{t+1}.
\]

The optimization objective is

\[
J(\theta) = \mathbb{E}_{\tau \sim p_\theta}[G_0(\tau)]
= \sum_\tau p_\theta(\tau)G_0(\tau).
\]

### Why finite horizon is used here

Finite horizon keeps the derivation honest.  
It avoids silently interchanging derivatives, expectations, and infinite sums without justification.

---

## 2. Policy-gradient derivation

Differentiate the objective:

\[
\nabla_\theta J(\theta)
=
\sum_\tau \nabla_\theta p_\theta(\tau) G_0(\tau).
\]

Use the log-derivative identity:

\[
\nabla_\theta p_\theta(\tau)
=
p_\theta(\tau)\nabla_\theta \log p_\theta(\tau).
\]

So

\[
\nabla_\theta J(\theta)
=
\mathbb{E}_{\tau \sim p_\theta}
\left[
\nabla_\theta \log p_\theta(\tau) G_0(\tau)
\right].
\]

### Now expand the trajectory log probability

The trajectory probability factorizes into initial-state, policy, and environment terms.  
Taking logs turns the product into a sum. Only the policy factors depend on \(\theta\), so

\[
\nabla_\theta \log p_\theta(\tau)
=
\sum_{t=0}^{T-1}
\nabla_\theta \log \pi_\theta(A_t \mid S_t).
\]

Substituting gives

\[
\nabla_\theta J(\theta)
=
\mathbb{E}
\left[
\sum_{t=0}^{T-1}
\nabla_\theta \log \pi_\theta(A_t \mid S_t)
\, G_0
\right].
\]

### What this proves

This is already a correct policy-gradient expression.  
No approximation has been used yet.

---

## 3. Why reward-to-go is valid

The previous formula multiplies every score term by the full return \(G_0\).  
But rewards obtained before time \(t\) cannot depend on action \(A_t\), because they were observed earlier.

So when you expand \(G_0\), the past-reward portion contributes zero in expectation when multiplied by

\[
\nabla_\theta \log \pi_\theta(A_t \mid S_t).
\]

What remains is the future-dependent part, namely \(G_t\).  
Therefore the gradient can be written as

\[
\nabla_\theta J(\theta)
=
\mathbb{E}
\left[
\sum_{t=0}^{T-1}
\gamma^t
\nabla_\theta \log \pi_\theta(A_t \mid S_t) G_t
\right].
\]

### What this means

Reward-to-go is not a heuristic convenience.  
It is algebraically justified because rewards that occurred before the action at time \(t\) cannot carry information about that action’s causal effect.

---

## 4. Baseline subtraction

Let \(b(S_t)\) be any function of the state only.  
Consider the term

\[
\mathbb{E}
\left[
\gamma^t \nabla_\theta \log \pi_\theta(A_t \mid S_t)b(S_t)
\right].
\]

Condition on the state \(S_t=s\). Then the inner expectation becomes

\[
\sum_a \pi_\theta(a \mid s)\nabla_\theta \log \pi_\theta(a \mid s)
=
\sum_a \nabla_\theta \pi_\theta(a \mid s).
\]

Because policy probabilities sum to one,

\[
\sum_a \pi_\theta(a \mid s) = 1
\quad \Longrightarrow \quad
\sum_a \nabla_\theta \pi_\theta(a \mid s)=0.
\]

So the baseline term has zero expectation.

Therefore

\[
\nabla_\theta J(\theta)
=
\mathbb{E}
\left[
\sum_{t=0}^{T-1}
\gamma^t
\nabla_\theta \log \pi_\theta(A_t \mid S_t)
\left(G_t - b(S_t)\right)
\right].
\]

### What this proves

Subtracting a state-dependent baseline does not change the expected gradient.  
It can, however, reduce variance.

### Important boundary condition

The baseline must not depend on the sampled action in a way that breaks the zero-expectation argument.  
A state-only baseline is safe.

---

## 5. Advantage and actor-critic

If the baseline is chosen as the state value \(V^\pi(S_t)\), then

\[
G_t - V^\pi(S_t)
\]

is an advantage-style quantity.  
More formally, the exact policy-gradient contribution at time \(t\) involves

\[
\gamma^t \nabla_\theta \log \pi_\theta(A_t \mid S_t) A^\pi(S_t,A_t).
\]

But the true advantage is usually unknown, so actor-critic methods replace it with an estimator \(\widehat A_t\).

Then the stochastic actor update direction is

\[
\widehat g_t(\theta)
=
\gamma^t \nabla_\theta \log \pi_\theta(A_t \mid S_t)\widehat A_t.
\]

### What must be checked for unbiasedness

If

\[
\mathbb{E}[\widehat A_t \mid S_t, A_t]
=
A^\pi(S_t,A_t),
\]

then the expected update matches the exact policy-gradient contribution at that time step.

### Common one-step choice

A widely used choice is the TD residual

\[
\delta_t = R_{t+1} + \gamma V_w(S_{t+1}) - V_w(S_t).
\]

### Important honesty condition

If the critic \(V_w\) is approximate, then \(\delta_t\) need not be an unbiased estimate of the true advantage.  
So the actor update may become biased, even though variance may improve.

That tradeoff must be stated explicitly.

---

## 6. Critic update and semi-gradient issue

A critic may be trained by a Bellman-style regression target.  
Using a frozen target parameter vector \(w^-\), define

\[
Y_t^V(w^-)
=
R_{t+1} + \gamma V_{w^-}(S_{t+1}).
\]

Then define the critic loss

\[
L_V(w; w^-)
=
\frac{1}{2}
\mathbb{E}
\left[
\left(Y_t^V(w^-) - V_w(S_t)\right)^2
\right].
\]

### Why the frozen target matters again

While differentiating with respect to \(w\), the target depends on \(w^-\), not on the same variable \(w\).  
So the target is treated as constant during differentiation.

This gives

\[
\nabla_w L_V(w;w^-)
=
\mathbb{E}
\left[
\left(V_w(S_t)-Y_t^V(w^-)\right)\nabla_w V_w(S_t)
\right].
\]

### Semi-gradient boundary condition

If one sets \(w^- = w\) inside the target but still suppresses the derivative through \(V_w(S_{t+1})\), one gets the standard semi-gradient TD form.

That is not the full gradient of the naive “same-parameter-on-both-sides” objective.  
This distinction must stay explicit.

---

## 7. PPO

Suppose the data were collected by an older policy \(\pi_{\theta_{\mathrm{old}}}\).  
Define the probability ratio

\[
r_t(\theta)
=
\frac{\pi_\theta(A_t \mid S_t)}
{\pi_{\theta_{\mathrm{old}}}(A_t \mid S_t)}.
\]

Let \(\hat A_t\) be an advantage estimate treated as constant during the update.

The unclipped surrogate is

\[
L^{\mathrm{PG}}(\theta)
=
\mathbb{E}[r_t(\theta)\hat A_t].
\]

### What the ratio means

If \(r_t(\theta) > 1\), the new policy assigns more probability to the sampled action than the old policy did.  
If \(r_t(\theta) < 1\), it assigns less.

### Clipped objective

PPO replaces the unclipped objective by a clipped one that, case by case, prevents the objective from rewarding excessive probability-ratio changes beyond a chosen window \([1-\epsilon,\,1+\epsilon]\).

### What clipping is doing conceptually

- If \(\hat A_t > 0\), increasing the probability of the sampled action is helpful, but only up to the clipping threshold.
- If \(\hat A_t < 0\), decreasing the probability is helpful, but again only up to the clipping threshold.

So clipping limits how much the objective can improve merely by pushing the ratio farther in the already-helpful direction.

### What conclusion this licenses

PPO is not “taking the policy gradient and then clipping gradients.”  
The clipping is applied to the **surrogate objective through the probability ratio**, which changes the optimization landscape itself.

That distinction matters.

---

## 8. Soft Actor-Critic

SAC modifies the objective by adding an entropy bonus.

Let \(\alpha_{\mathrm{ent}} > 0\) be the entropy coefficient.  
Define the soft return

\[
G_0^{\mathrm{soft}}
=
\sum_{t=0}^{\infty}
\gamma^t
\left(
R_{t+1} + \alpha_{\mathrm{ent}}\mathcal{H}(\pi(\cdot \mid S_t))
\right).
\]

The corresponding objective is

\[
J_{\mathrm{soft}}(\pi)
=
\mathbb{E}_\pi[G_0^{\mathrm{soft}}].
\]

### Soft value relations

Define

\[
Q^\pi_{\mathrm{soft}}(s,a)
=
\mathbb{E}_\pi
\left[
R_{t+1} + \gamma V^\pi_{\mathrm{soft}}(S_{t+1})
\mid S_t=s, A_t=a
\right],
\]

and

\[
V^\pi_{\mathrm{soft}}(s)
=
\mathbb{E}_{A \sim \pi(\cdot \mid s)}
\left[
Q^\pi_{\mathrm{soft}}(s,A) - \alpha_{\mathrm{ent}}\log \pi(A \mid s)
\right].
\]

### Why the minus sign appears inside the expectation

Entropy is

\[
\mathcal{H}(\pi(\cdot \mid s))
=
-
\mathbb{E}_{A \sim \pi(\cdot \mid s)}
[\log \pi(A \mid s)].
\]

So maximizing reward plus entropy becomes equivalent to maximizing a critic term minus \(\alpha_{\mathrm{ent}}\log \pi\) inside the state-wise expectation.

### Conceptual meaning

SAC does not maximize reward alone.  
It maximizes reward plus a preference for stochastic policies with higher entropy.

---

## 9. Common confusions blocked here

### Confusion 1: policy gradients require differentiating the environment dynamics

Not in the standard derivation here.  
The environment terms vanish from \(\nabla_\theta \log p_\theta(\tau)\) because they do not depend on \(\theta\).

### Confusion 2: reward-to-go is a biased approximation

No.  
In this finite-horizon derivation, it is algebraically justified.

### Confusion 3: any baseline is safe

No.  
The zero-expectation proof relies on the baseline being state-dependent in the required way.

### Confusion 4: actor-critic updates are always exact gradients

False.

The actor update is exact only under the corresponding expectation statement with the true advantage.  
A learned critic can introduce bias.

### Confusion 5: PPO clipping directly clips parameter updates

No.  
It clips the probability-ratio contribution inside the surrogate objective.

---

## 10. Mastery check

You understand this chapter if you can explain all of these precisely.

1. Why does \(\nabla_\theta \log p_\theta(\tau)\) reduce to a sum over policy log-probability gradients?
2. Why can \(G_0\) be replaced by reward-to-go \(G_t\) in the time-\(t\) term?
3. Why does a state-dependent baseline have zero expected contribution?
4. Under what condition is an actor-critic update unbiased relative to the exact advantage term?
5. What exactly is being clipped in PPO?
6. What changes in SAC relative to ordinary reward maximization?

If any answer is not exact, revisit the section before moving on.
