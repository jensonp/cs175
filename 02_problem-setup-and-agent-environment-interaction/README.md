# Chapter 1 — Problem Setup and Agent-Environment Interaction

## What this chapter establishes

This chapter fixes the most basic objects in reinforcement learning.

By the end of the chapter, you should know exactly:

- what happens first and what happens second at each time step,
- what the random variables \(O_t\), \(A_t\), and \(R_{t+1}\) mean,
- why the reward is indexed by \(t+1\) rather than \(t\),
- what a policy is,
- and what object is being optimized.

Nothing in this chapter requires the Markov property yet.  
That comes later.

---

## 1. Discrete-time interaction

Time is discrete. The time index is

\[
t \in \{0,1,2,\ldots\}.
\]

At each time step, the agent and environment interact in a fixed order.

### The order of events at time \(t\)

1. The environment provides the information available at time \(t\).
2. The agent chooses an action \(A_t\).
3. The environment reacts to that action.
4. The agent then observes the reward \(R_{t+1}\) and the information needed for time \(t+1\).

This order matters.  
The reward belongs to the consequence of the action chosen at time \(t\), so it is written \(R_{t+1}\), not \(R_t\).

### Why the reward index is shifted

The index shift is not cosmetic. It enforces the causal order correctly.

- \(A_t\) is chosen **before** the environment reacts.
- \(R_{t+1}\) is observed **after** the reaction.

So the pair \((A_t, R_{t+1})\) belongs together.  
That is why Bellman recursions later have the form

\[
G_t = R_{t+1} + \gamma G_{t+1}.
\]

If you instead write \(R_t\) for the reward caused by \(A_t\), you blur the event order and create confusion in every later recursion.

---

## 2. Primitive random variables

At the most abstract level, the interaction includes these random variables.

- \(O_t\): the observation available at time \(t\)
- \(A_t\): the action chosen at time \(t\)
- \(R_{t+1}\): the reward observed after action \(A_t\)

At this stage, no state \(S_t\) has been defined yet.  
That is deliberate.

The observation is what the environment reveals.  
A state, when introduced later, will be a representation used for decision making.

---

## 3. What the environment is

The environment is the entire stochastic mechanism that maps past interaction to future observations and rewards.

This statement has two consequences.

### First consequence

The environment is not just a transition table in the narrow MDP sense.  
At the current level of abstraction, it may depend on the whole interaction history.

### Second consequence

We have not yet assumed the Markov property.  
So nothing yet says that the future depends only on a state summary \(S_t\) and action \(A_t\).  
That assumption must be earned later, not smuggled in here.

---

## 4. What the agent is

The agent is the decision rule that maps available information to an action.

That available information may be:

- the current observation,
- a summary of the interaction history,
- the full interaction history,
- or a learned internal representation.

The point of reinforcement learning is to choose or learn that decision rule so that a long-run objective is maximized.

---

## 5. Policies

A policy is the object being optimized.

There are two standard forms.

### Deterministic policy

A deterministic policy maps an information summary \(x\) to a single action:

\[
\pi : x \mapsto a.
\]

If the same \(x\) appears again, the same action is chosen again.

### Stochastic policy

A stochastic policy assigns a probability distribution over actions:

\[
\pi(a \mid x) = P(A_t = a \mid X_t = x).
\]

Here \(X_t\) is a placeholder for whatever information summary the policy is allowed to use.

At this stage, \(X_t\) is intentionally generic.  
Later it may become a state \(S_t\), a history \(H_t\), or a learned representation.

### Why stochastic policies matter

A stochastic policy is not merely a noisy version of a deterministic one. It is useful for three separate reasons.

1. It supports exploration.
2. It is natural in partially observed settings where uncertainty remains after conditioning on the available information.
3. Policy-gradient methods optimize probability distributions directly, so stochastic policies are the native object there.

---

## 6. Notation table

| Symbol | Meaning |
| --- | --- |
| \(O_t\) | observation at time \(t\) |
| \(A_t\) | action chosen at time \(t\) |
| \(R_{t+1}\) | reward observed after action \(A_t\) |
| \(H_t\) | full interaction history available up to time \(t\) |
| \(S_t\) | state representation used for decision making at time \(t\) |
| \(\pi(a \mid s)\) | probability of action \(a\) in state \(s\) under policy \(\pi\) |
| \(\gamma\) | discount factor |
| \(G_t\) | return from time \(t\) onward |
| \(V^\pi(s)\) | state value under policy \(\pi\) |
| \(Q^\pi(s,a)\) | action value under policy \(\pi\) |
| \(A^\pi(s,a)\) | advantage under policy \(\pi\) |

---

## 7. What this chapter does **not** assume

To avoid hidden assumptions, make these absences explicit.

### No Markov assumption yet

We have not yet assumed

\[
P(\text{future} \mid \text{past}, A_t) = P(\text{future} \mid S_t, A_t).
\]

That arrives only after defining history and state carefully.

### No finite-state assumption yet

We have not yet assumed a finite state space or finite action space.  
Those assumptions will be introduced only when needed for finite sums or contraction arguments.

### No value function yet

A policy is defined before value functions are defined.  
That is the correct order.  
A value function is always value **under a policy** or value **under optimal control**.  
So the policy or control problem must exist first.

---

## 8. The optimization problem in plain terms

The reinforcement-learning problem is:

> choose a policy so that the long-run quality of interaction is as large as possible.

That sentence is still informal because the long-run quality has not been written mathematically yet.  
Later chapters make that precise through the return \(G_t\) and the objective \(J(\pi)\).

For now, the important point is this:

- the environment produces outcomes stochastically,
- the policy influences which action is taken,
- and the goal is to optimize the policy, not merely predict rewards.

---

## 9. Common confusions blocked here

### Confusion 1: “observation” and “state” are the same thing

Not necessarily.

- An observation is what is revealed.
- A state is what the agent conditions on.
- A Markov state is a state summary that makes the future independent of the past beyond that summary.

These are three different notions.

### Confusion 2: the reward should be indexed by the same time as the action

That is bad bookkeeping.

The action is chosen at time \(t\).  
The reward resulting from that action is observed after the transition, so it is indexed \(t+1\).

### Confusion 3: a policy must use only the current observation

False.

A policy may depend on any allowed information summary.  
Restricting it to a Markov state is a modeling choice that becomes justified only when the Markov property holds.

---

## 10. Mastery check

You understand this chapter if you can answer all of these without hesitation.

1. Why is the reward written \(R_{t+1}\) instead of \(R_t\)?
2. What is the exact difference between \(O_t\) and \(S_t\)?
3. What has not yet been assumed about the environment?
4. What is the object being optimized in reinforcement learning?
5. What changes when a policy is stochastic instead of deterministic?

If any answer feels vague, fix that before moving on.  
The rest of reinforcement learning depends on these distinctions being clean.
