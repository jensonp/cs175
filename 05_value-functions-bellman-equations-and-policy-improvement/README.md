# Chapter 4 — Value Functions, Bellman Equations, and Policy Improvement

## What this chapter locks in

This chapter turns the long-run objective into local recursive quantities.

The single biggest risk here is compression.  
A learner often sees the Bellman equations written down correctly without owning the ladder of reasoning that produces them.

This rewrite slows the ladder down.

By the end of this chapter, you should know:

- what $V^\pi$, $Q^\pi$, and $A^\pi$ each mean,
- which equations are definitions and which are derived identities,
- how the Bellman expectation equation is built step by step,
- what a Bellman operator is,
- why contraction matters,
- how optimality equations differ from expectation equations,
- and what the policy-improvement theorem actually proves.

---

## 1. Start with definitions, not with recursions

Fix a policy $\pi$.

### State value

$$
V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t=s].
$$

This is the expected return when the current state is $s$ and policy $\pi$ is followed from now on.

### Action value

$$
Q^\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a].
$$

This is the expected return when the current state is $s$, the current action is forced to be $a$, and policy $\pi$ is followed after that.

### Advantage

$$
A^\pi(s,a) = Q^\pi(s,a) - V^\pi(s).
$$

This measures how much better or worse action $a$ is than the policy’s own average action quality at state $s$.

### First boundary line

These are **definitions**.  
Nothing has been derived yet.

That distinction matters because learners often treat the first displayed equation they see as a theorem.  
Here, the value definitions are just naming the objects.

---

## 2. The relation between $V^\pi$ and $Q^\pi$

Once $S_t=s$ is fixed, the policy chooses the current action according to $\pi(\cdot \mid s)$.

So $V^\pi(s)$ is the policy-weighted average of the corresponding action values:

$$
V^\pi(s) = \sum_a \pi(a \mid s) Q^\pi(s,a).
$$

### What is being checked

At state $s$, different actions lead to different conditional returns.  
The policy assigns probabilities to those actions.  
So the state value is an average over those action-conditioned returns.

### What this proves

$V^\pi(s)$ is not an unrelated object standing next to $Q^\pi(s,a)$.  
It is the current policy’s weighted average over action values at that state.

---

## 3. The algebraic return recursion

Before deriving any Bellman equation, fix the identity

$$
G_t = R_{t+1} + \gamma G_{t+1}.
$$

### What kind of statement this is

This is an algebraic decomposition of the return.

It does **not** yet use the MDP assumption.  
It comes directly from how $G_t$ is defined.

### Why this matters

Later Bellman equations are built by inserting this recursion inside conditional expectations.

So the order is:

1. define return,
2. write the return recursion,
3. then take conditional expectations.

---

## 4. Deriving the Bellman expectation equation for $V^\pi$

Start from the definition

$$
V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t=s].
$$

### Step 1: substitute the return recursion

Replace $G_t$ by $R_{t+1} + \gamma G_{t+1}$:

$$
V^\pi(s) = \mathbb{E}_\pi[R_{t+1} + \gamma G_{t+1} \mid S_t=s].
$$

At this point, the conditioning event is still only $S_t=s$.

### Step 2: split on the current action

Given state $s$, the next policy-controlled random variable is the current action $A_t$.

So condition first on which action is chosen.

The weights for that split are $\pi(a \mid s)$.

### Step 3: split on the next transition outcome

Once state $s$ and action $a$ are fixed, the next random quantities are the next state and next reward.

So split on $(S_{t+1}, R_{t+1}) = (s', r)$.

The weights for that split are $P(s', r \mid s, a)$.

### Step 4: recognize the continuation term

After the process reaches next state $s'$, the expected future return under policy $\pi$ is exactly $V^\pi(s')$.

That is the key recognition step.

### Final equation

Putting those steps together gives

$$
V^\pi(s)
=
\sum_a \pi(a \mid s)
\sum_{s',r} P(s', r \mid s,a)
\bigl[r + \gamma V^\pi(s')\bigr].
$$

### What this equation is

This is the Bellman expectation equation for the state value under policy $\pi$.

It is an **exact identity** under the MDP assumptions.

It is not a sampled approximation.

---

## 5. Deriving the Bellman expectation equation for $Q^\pi$

Now start from

$$
Q^\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a].
$$

### Step 1: substitute the return recursion

$$
Q^\pi(s,a) = \mathbb{E}_\pi[R_{t+1} + \gamma G_{t+1} \mid S_t=s, A_t=a].
$$

### Step 2: split on the next transition outcome

Once $s$ and $a$ are fixed, the next stochastic outcome is $(S_{t+1}, R_{t+1})$.

So sum over $(s',r)$ with weights $P(s',r \mid s,a)$.

### Step 3: identify the continuation value

After arriving at next state $s'$, the future is controlled by policy $\pi$, so the continuation value is $V^\pi(s')$.

That gives

$$
Q^\pi(s,a)
=
\sum_{s',r} P(s',r \mid s,a)
\bigl[r + \gamma V^\pi(s')\bigr].
$$

If you then replace $V^\pi(s')$ by its action-value expansion

$$
V^\pi(s') = \sum_{a'} \pi(a' \mid s')Q^\pi(s',a'),
$$

you get

$$
Q^\pi(s,a)
=
\sum_{s',r} P(s',r \mid s,a)
\left[
r + \gamma \sum_{a'} \pi(a' \mid s')Q^\pi(s',a')
\right].
$$

### What this proves

The $Q^\pi$ Bellman equation is also exact.  
It says how the action value at the current pair $(s,a)$ decomposes into:

- immediate reward,
- plus discounted continuation value under the same policy.

---

## 6. Definitions versus exact identities versus approximations

This chapter contains three different kinds of statements, and they must stay separate.

### Definitions

- $V^\pi$,
- $Q^\pi$,
- $A^\pi$.

### Exact identities

- the return recursion,
- the Bellman expectation equations,
- the relation $V^\pi(s) = \sum_a \pi(a \mid s)Q^\pi(s,a)$.

### Approximations

None yet.

The approximations arrive in the next chapter, when exact expectations are replaced by sampled targets.

Keeping this boundary sharp is essential.

---

## 7. Bellman operators

An operator is a mapping that takes one value function and produces another.

### Bellman expectation operator for a fixed policy

$$
(T^\pi V)(s)
=
\sum_a \pi(a \mid s)
\sum_{s',r} P(s',r \mid s,a)\bigl[r + \gamma V(s')\bigr].
$$

### Bellman optimality operator

$$
(T^*V)(s)
=
\max_a
\sum_{s',r} P(s',r \mid s,a)\bigl[r + \gamma V(s')\bigr].
$$

### Why this viewpoint matters

The Bellman equations can now be written as fixed-point equations:

- $V^\pi = T^\pi V^\pi$,
- $V^* = T^*V^*$.

That turns value computation into a fixed-point problem.

---

## 8. Why contraction matters

Under bounded value functions and $0 \le \gamma < 1$, both $T^\pi$ and $T^*$ are $\gamma$-contractions in the supremum norm.

For the policy operator,

$$
\|T^\pi V - T^\pi W\|_\infty \le \gamma \|V-W\|_\infty.
$$

### Why the factor $\gamma$ survives

When you compare $T^\pi V$ and $T^\pi W$, the immediate reward terms cancel.  
The only difference left is in the continuation terms, and each continuation term is multiplied by $\gamma$.

Then three checks matter:

1. $|V(s') - W(s')| \le \|V-W\|_\infty$,
2. transition probabilities sum to $1$,
3. policy probabilities sum to $1$.

So the only multiplicative factor that remains is $\gamma$.

### What this gives you

A contraction has a unique fixed point.  
Repeated application converges to that fixed point.

That is why iterative policy evaluation and value iteration have clean convergence logic in the discounted setting.

---

## 9. Expectation equations versus optimality equations

For a fixed policy, the Bellman equation averages over the continuation action according to that policy.

For optimal control, the continuation action is chosen to maximize value.

### Optimal state-value equation

$$
V^*(s)
=
\max_a
\sum_{s',r} P(s',r \mid s,a)\bigl[r + \gamma V^*(s')\bigr].
$$

### Optimal action-value equation

$$
Q^*(s,a)
=
\sum_{s',r} P(s',r \mid s,a)
\Bigl[r + \gamma \max_{a'} Q^*(s',a')\Bigr].
$$

### The exact difference

- expectation equations evaluate a specified policy,
- optimality equations describe the best achievable continuation.

Do not blur these roles.

---

## 10. Policy improvement

Let $\pi$ be a policy, and define a new policy $\pi'$ that chooses actions greedily with respect to $Q^\pi$.

That means that at each state $s$, the policy $\pi'$ selects an action that maximizes $Q^\pi(s,a)$.

### Why the first step works

You already know that

$$
V^\pi(s) = \sum_a \pi(a \mid s)Q^\pi(s,a).
$$

That is a weighted average of the numbers $Q^\pi(s,a)$.  
A weighted average cannot exceed the maximum of the numbers being averaged.

So

$$
V^\pi(s) \le \max_a Q^\pi(s,a).
$$

If $\pi'$ picks a maximizing action, then its first action is at least as good as the old policy’s average first action.

### What the theorem concludes

The policy-improvement theorem gives

$$
V^{\pi'}(s) \ge V^\pi(s)
\quad\text{for every state } s.
$$

### What it does **not** conclude

It does not say one greedy step makes the policy optimal.  
It says the greedy policy is no worse than the current one.

Repeated evaluation and improvement are what drive control.

---

## 11. Generalized policy iteration

Generalized policy iteration is the repeated interplay between:

- policy evaluation,
- and policy improvement.

These two processes can be exact or approximate, full or partial, interleaved or alternating.

The important point is structural:

1. estimate how good the current policy is,
2. use that estimate to prefer better actions,
3. repeat.

Dynamic programming, TD control, Q-learning, and actor–critic all live inside this broad template.

---

## 12. Common confusions blocked here

### Confusion 1: $V^\pi$ and $Q^\pi$ are interchangeable notations

No.  
They condition on different information.

### Confusion 2: Bellman equations are approximate by nature

Not in this chapter.  
Here they are exact identities under the MDP assumptions.

### Confusion 3: The Bellman operator is just notation fluff

No.  
The operator view is what makes fixed-point and contraction arguments transparent.

### Confusion 4: Policy improvement says greedy means optimal

No.  
It says greedy with respect to the current action-value function is no worse than the current policy.

---

## 13. Mastery check

You understand this chapter if you can answer all of these precisely.

1. Which displayed equations in this chapter are definitions, and which are derived?
2. In the derivation of the Bellman expectation equation for $V^\pi$, what random quantities are being split on, and in what order?
3. What exact recognition step turns the continuation expectation into $V^\pi(s')$?
4. Why does the contraction bound keep the factor $\gamma$?
5. What does the policy-improvement theorem prove, and what does it leave open?

Do not move on until the difference between **definition**, **exact identity**, and **sampled approximation** is stable in your head.
