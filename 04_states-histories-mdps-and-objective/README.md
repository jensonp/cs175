# Chapter 3 — States, Histories, MDPs, and the Objective

## What this chapter locks in

This chapter separates four ideas that learners often blur together:

- history,
- state representation,
- Markov sufficiency,
- and the objective being optimized.

This is one of the most important chapters in the whole sequence.  
If the distinction between “a summary” and “a Markov summary” is not firm, the rest of reinforcement learning can become symbolic theater.

---

## 1. Start with history, not with state

At time $t$, a history $H_t$ records the interaction information available up to the current decision point.

A typical form is

$$
H_t = (O_0, A_0, R_1, O_1, A_1, R_2, \ldots, O_t).
$$

The exact notation can vary, but the structural point does not:

- history is the most complete decision-relevant record you are carrying,
- and any state representation you define later is built from that history.

So the correct logical order is:

1. define interaction,
2. define history,
3. define a state representation as a function of history,
4. then test whether that state representation is Markov.

---

## 2. A state representation is a function of history

A state representation is some summary

$$
S_t = f(H_t).
$$

That summary may be hand-designed, learned, compact, lossy, exact, or approximate.

### What this means

The name “state” does not yet guarantee anything about predictive sufficiency.

It only says:

- the agent is conditioning on this summary,
- and this summary is derived from the available past.

A summary can be useful while still failing to be Markov.

---

## 3. What the Markov property actually says

The Markov property is a statement about conditional laws.

A state representation $S_t$ is Markov if, once $S_t$ and the current action $A_t$ are known, the conditional distribution of the next-step outcome no longer depends on the rest of the past.

In plain language:

> after conditioning on the current state summary and current action, there is no remaining predictive information in the earlier history for the next transition outcome.

A common formal expression is:

$$
P(S_{t+1}, R_{t+1} \mid H_t, A_t)
=
P(S_{t+1}, R_{t+1} \mid S_t, A_t).
$$

### What is being checked

You are checking whether the summary has kept exactly the information needed for one-step prediction and control.

### What is **not** being checked

You are not checking whether the summary is intuitive.  
You are not checking whether it is low-dimensional.  
You are not checking whether it “feels like the state.”

The test is predictive sufficiency under conditioning.

---

## 4. The key decision boundary: summary versus Markov state

This is the most important fork in the chapter.

### A summary that is not Markov

Suppose two different histories produce the same representation $S_t=s$, but those histories imply different conditional laws for $(S_{t+1}, R_{t+1})$ once action $A_t=a$ is fixed.

Then $S_t$ is **not** Markov.

### A summary that is Markov

If any two histories that map to the same $S_t=s$ induce the same conditional law for the next-step outcome under each action, then the summary is Markov.

### Why this distinction matters

Bellman equations, policy evaluation, and dynamic programming all rely on the current state being sufficient for future prediction in this precise conditional sense.

If the representation is not Markov, those equations are no longer exact descriptions of the original process.

---

## 5. From Markov state to MDP

Once a state representation is Markov, you can describe the environment using Markov transition laws.

In the finite-state and finite-action setting, an MDP is specified by:

- a state space $\mathcal{S}$,
- an action space $\mathcal{A}$,
- a transition–reward law $P(s', r \mid s, a)$,
- and usually an initial-state distribution.

### What this means

The future one-step law is now described locally:

- current state $s$,
- current action $a$,
- next state $s'$,
- next reward $r$.

The past no longer needs to be carried explicitly once the current state is known.

### Why that helps

This local structure is what makes Bellman recursions possible.

---

## 6. Policies in an MDP

Once states are Markov, a policy is usually written as a mapping from current state to action probabilities:

$$
\pi(a \mid s) = P(A_t=a \mid S_t=s).
$$

### Why this is legitimate now

Earlier, you were not allowed to assume the current summary was enough.  
Now, under the Markov property, conditioning on $S_t$ is sufficient for one-step predictive control.

That is why MDP theory speaks naturally in terms of state-based policies.

---

## 7. Return and the objective

The return from time $t$ is

$$
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}
$$

in a continuing discounted setting, under the usual boundedness and discount assumptions.

The broad optimization goal is to choose a policy that makes expected return large.

A common episodic objective is an expectation from the initial distribution, such as

$$
J(\pi) = \mathbb{E}_\pi[G_0].
$$

### What this objective checks

The objective is not “maximize the next reward” unless $\gamma = 0$.  
It is about the long-run consequences of the policy.

That is exactly why reinforcement learning can rationally choose a locally bad action that improves downstream outcomes.

---

## 8. Why the Markov property matters for Bellman structure

Bellman equations depend on a recursive decomposition of return:

$$
G_t = R_{t+1} + \gamma G_{t+1}.
$$

That recursion always holds as an algebraic identity.  
But turning it into a **state-based** recursive equation requires more.

It requires that, once you condition on $S_t=s$ and take an action $a$, the law of the next-step outcome be determined by $s$ and $a$, not by hidden leftovers from the past.

So there are two layers:

1. the return recursion is always algebraically true,
2. the Bellman equation in terms of state value is true under the MDP assumptions.

This distinction matters.

---

## 9. Boundary conditions

### Partial observation

If the current observation does not preserve enough information from the past, then the observation alone may fail to be Markov.

### Learned representations

A learned latent representation may or may not be Markov.  
Calling it an “embedding” does not answer the sufficiency question.

### Non-Markov summaries

A non-Markov summary can still be useful for learning in practice.  
But when you use exact MDP language with it, you are making an approximation.

---

## 10. Common confusions blocked here

### Confusion 1: A state is whatever the agent currently sees

Not necessarily.  
What the agent sees is an observation.  
A state is a summary used for decision making.  
A Markov state is a summary with a specific conditional sufficiency property.

### Confusion 2: If a summary works well, it must be Markov

No.  
Practical usefulness and exact Markov sufficiency are different questions.

### Confusion 3: MDPs are the starting point of the subject

Not conceptually.  
The interaction process comes first.  
The MDP description is a later structural simplification earned by the Markov property.

### Confusion 4: The objective is immediate reward maximization

Usually false.  
The objective is expected return, which includes future rewards through discounting or finite-horizon accumulation.

---

## 11. Mastery check

You understand this chapter if you can answer all of these without drifting into vague language.

1. Why must history be defined before state?
2. What does the equation $S_t = f(H_t)$ mean conceptually?
3. What exact conditional-independence statement is being tested by the Markov property?
4. What is the difference between a useful summary and a Markov state?
5. Why does Bellman theory care about Markov sufficiency?

If you cannot answer these cleanly, pause here.  
This chapter is the conceptual firewall for everything that follows.
