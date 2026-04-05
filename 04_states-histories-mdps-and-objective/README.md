# Chapter 3 — States, Histories, MDPs, and the Objective

## What this chapter locks in

This chapter separates four ideas that are often blurred together:

- history,
- state representation,
- Markov sufficiency,
- and the objective being optimized.

This separation is one of the conceptual firewalls of the whole subject.

If the learner does not clearly distinguish “a summary of the past” from “a summary that is sufficient in the Markov sense,” then Bellman equations, dynamic programming, and even policy definitions can still be repeated mechanically while not being fully understood.

The purpose of this chapter is to make that confusion hard to maintain.

By the end of the chapter, you should be able to state:

- what history contains at a decision point,
- how a state representation is built from history,
- what exact conditional law the Markov property compares,
- what an MDP is once a Markov state has been established,
- what the objective is maximizing,
- and why Bellman structure depends on Markov sufficiency rather than merely on having some convenient summary.

---

## 1. Start with the most complete decision-relevant record

At the decision point indexed by $t$, the fullest conceptual record available from past interaction is the history

$$
H_t = (O_0, A_0, R_1, O_1, A_1, R_2, \ldots, O_t).
$$

The exact notation can vary across sources, but the structural point does not vary:

- $H_t$ is available before action $A_t$ is chosen,
- $H_t$ records the interaction up to the current decision point,
- and any later state representation must be a function of information available in $H_t$.

This is the right order:

1. interaction process,
2. history,
3. summary of history,
4. test of whether that summary is Markov.

History comes first because it is the reference object against which sufficiency is tested.

If you never name the full information record, you cannot state precisely what information a summary may have discarded.

---

## 2. State representation as a function of history

A state representation is some mapping

$$
S_t = f(H_t).
$$

This equation is doing one simple but important job.

It says that a state representation is **derived from the available past**.  
It is not a mystical entity that appears independently of the interaction record.

### What this means

A state representation may be:

- exact or approximate,
- high-dimensional or low-dimensional,
- hand-designed or learned,
- lossless or lossy.

None of those adjectives, by themselves, answer the Markov question.

At this stage, the equation $S_t = f(H_t)$ means only:

- the agent conditions on a summary,
- that summary is built from history,
- and the summary may retain some information while discarding other information.

That is all.

---

## 3. Summary does not yet mean sufficient

The word *state* is often used too casually.

If you call a representation a state, you have not yet proved anything about prediction or control.

You have only named a summary that the agent plans to use.

So the correct conceptual distinction is:

- **summary** means “some function of history,”
- **Markov state** means “a summary that passes a particular conditional sufficiency test.”

This is the exact fork where many misunderstandings begin.

A compact representation can be useful and still fail to be Markov.  
A learned embedding can work well in practice and still fail to be Markov.  
A human-interpretable feature vector can feel sensible and still fail to be Markov.

The word you use for the summary is irrelevant.  
The conditional law is what decides the matter.

---

## 4. The unrestricted one-step law

From Chapter 1, before imposing any Markov restriction, the next-step outcome may depend on the full history and current action:

$$
P(O_{t+1}, R_{t+1} \mid H_t, A_t).
$$

That is the unrestricted one-step description of the interaction at the level of observable outputs.

If you later introduce a state representation $S_t=f(H_t)$, the central question becomes:

does conditioning on $S_t$ preserve all the information from history that is needed for one-step prediction and control?

That is exactly what the Markov test checks.

---

## 5. What the Markov property actually says

A state representation $S_t$ is Markov if, once $S_t$ and the current action $A_t$ are known, the conditional law of the next-step outcome no longer depends on the rest of the past.

A common formal expression is

$$
P(S_{t+1}, R_{t+1} \mid H_t, A_t)
=
P(S_{t+1}, R_{t+1} \mid S_t, A_t).
$$

Read this in the right order.

On the left side, the conditioning keeps the **full history** and the current action.  
On the right side, the conditioning keeps only the **state summary** and the current action.

The Markov claim says those two conditional laws are the same.

### What is being checked

You are checking whether, after fixing the summary $S_t$ and action $A_t$, there is any predictive information left in the earlier history for the next-step outcome.

If the answer is yes, the summary is not Markov.  
If the answer is no, the summary is Markov.

### What is not being checked

You are not checking whether the summary is intuitive.  
You are not checking whether it is low-dimensional.  
You are not checking whether it seems useful on observed data.  
You are checking a conditional sufficiency statement.

That is the whole test.

---

## 6. The decision boundary: summary versus Markov state

This section is the conceptual center of the chapter.

### Case 1: a summary that is **not** Markov

Suppose two different histories $h$ and $\tilde h$ both map to the same summary value $s$:

$$
f(h) = f(\tilde h) = s.
$$

Now fix an action $a$.

If the conditional law of the next-step outcome differs across those two histories even though the summary and action are the same, then the summary has thrown away prediction-relevant information.

Formally, if

$$
P(S_{t+1}, R_{t+1} \mid H_t=h, A_t=a)
\neq
P(S_{t+1}, R_{t+1} \mid H_t=\tilde h, A_t=a),
$$

then the common summary value $s$ is not sufficient, and the representation is not Markov.

### Case 2: a summary that **is** Markov

If for every action $a$, any two histories mapping to the same $s$ induce the same next-step conditional law, then the summary has preserved exactly the one-step predictive information needed.

In that case, the representation is Markov.

### Why this boundary matters

Bellman equations, dynamic programming, and standard value-function recursions all assume that the current state and action are sufficient to describe the next-step law.

If that sufficiency fails, the usual MDP equations are no longer exact descriptions of the original process.

That does not mean the summary is useless.  
It means the MDP language becomes an approximation.

---

## 7. From Markov state to MDP

Once a representation has passed the Markov test, the process can be described locally in terms of state and action.

In the finite-state, finite-action presentation, an MDP is specified by:

- a state space $\mathcal{S}$,
- an action space $\mathcal{A}$,
- a one-step transition-reward law
  $$
  P(s', r \mid s, a),
  $$
- and an initial-state distribution.

### What changes once you have an MDP

Before the Markov property, the next-step law might need the entire history.  
After the Markov property, the next-step law can be described using only:

- current state $s$,
- current action $a$,
- next state $s'$,
- next reward $r$.

That local structure is what makes the later recursion machinery possible.

### Why this simplification is powerful

The past does not disappear from reality.  
It is compressed into a summary that has been shown sufficient for one-step prediction and control.

That is why MDP theory works.  
It is not ignoring the past arbitrarily.  
It is using a representation that already carries what the past contributes for the next step.

---

## 8. Policies after Markov sufficiency

Before Markov sufficiency was established, the policy input had to be written generically as $X_t$.

Now, once $S_t$ is accepted as a Markov state, a policy can naturally be written as

$$
\pi(a \mid s) = P(A_t=a \mid S_t=s).
$$

### Why this notation is legitimate now

It is legitimate now because the state summary has already been granted the relevant role for one-step predictive control.

That is the logical order:

1. define the summary,
2. test Markov sufficiency,
3. then write state-based policy notation.

Using $\pi(a \mid s)$ before that point is often harmless as shorthand, but conceptually it skips a key justification.

---

## 9. Return and the objective

The return in a continuing discounted setting is

$$
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1},
$$

under the standard bounded-reward and $0 \le \gamma < 1$ assumptions from the previous chapter.

The broad optimization goal is to choose a policy that makes expected return large.

A standard objective is

$$
J(\pi) = \mathbb{E}_\pi[G_0],
$$

where the expectation is taken under the trajectory distribution induced by the policy and the environment, starting from the relevant initial distribution.

### What this objective does **not** say

It does not say “maximize the next reward,” except in degenerate special cases such as $\gamma=0$.

It says that the policy is judged by the long-run consequences of the trajectories it induces.

That is why RL can rationally choose a locally bad action when that action improves downstream outcomes.

---

## 10. State value and action value as conditional expectations

Once the objective and state notion are in place, two central objects can be named.

### State value

$$
V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t=s].
$$

This is the expected return starting from state $s$ when actions are selected according to policy $\pi$.

### Action value

$$
Q^\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a].
$$

This is the expected return starting from state $s$, forcing the current action to be $a$, and then following policy $\pi$ thereafter.

### Why the conditioning matters

These are not generic averages over the whole process.

They are conditional expectations under specific current information.

The precise conditioning event is what turns return into a state-based or state-action-based quantity.

---

## 11. Why Bellman structure cares about Markov sufficiency

The algebraic return recursion

$$
G_t = R_{t+1} + \gamma G_{t+1}
$$

always holds from the definition of return.

But a state-based Bellman equation needs more than that identity.

To move from the return recursion to a recursive equation in terms of $V^\pi(s)$ or $Q^\pi(s,a)$, you need the law of the next-step outcome to be determined by the current state and action rather than by hidden leftovers from the past.

So there are two distinct layers.

### Layer 1: algebraic recursion

This is always true:

$$
G_t = R_{t+1} + \gamma G_{t+1}.
$$

### Layer 2: state-based Bellman recursion

This is a conditional expectation statement that becomes exact under the MDP assumptions.

That distinction is essential.

The Bellman equation is not merely the return recursion with prettier notation.  
It is the return recursion *plus* the right conditioning structure.

---

## 12. Partial observation and non-Markov summaries

The current observation alone may fail to be Markov.

That happens when the current observation does not retain enough information from the past to determine the next-step law together with the current action.

In such cases:

- the observation may still be useful,
- a learned representation may still perform well,
- but the exact MDP equations for the original process no longer apply if you condition only on the observation.

This is the conceptual reason partially observable problems are harder.  
The difficulty is not simply “less data.”  
The difficulty is that a compressed or current view may fail the sufficiency test.

---

## 13. Learned representations and practical approximation

A learned latent representation may be closer to Markov than raw observation, but the name *latent state* does not prove the point.

The same question still has to be asked:

after conditioning on the learned representation and the current action, is there predictive information left in the earlier history for the next-step outcome?

If yes, then the representation is not exactly Markov.

This is not an insult to the representation.  
It is simply a statement about what kind of equations are exact and what kind are approximate.

That distinction becomes very important later when people apply MDP-based update rules in settings where the true process is only approximately Markov from the learner’s chosen representation.

---

## 14. Common confusions this chapter should block

### Confusion 1: a state is whatever the agent currently sees

Not necessarily.

What the agent currently sees is an observation.  
A state is a summary used for decision making.  
A Markov state is a summary with a specific conditional sufficiency property.

### Confusion 2: if a summary works well in practice, it must be Markov

No.

Practical usefulness and exact Markov sufficiency are different questions.

### Confusion 3: MDPs are the conceptual starting point of reinforcement learning

No.

The interaction process and history come first.  
The MDP is a structural simplification earned by the Markov property.

### Confusion 4: Bellman equations are automatically valid whenever someone writes down a feature vector

False.

State-based Bellman structure is exact when the relevant Markov assumptions hold.

### Confusion 5: the objective is immediate reward maximization

Usually false.

The objective is expected return, which values downstream consequences.

---

## 15. What this chapter allows you to conclude

After this chapter, you are allowed to say all of the following.

1. History is the reference object from which a state representation is built.
2. A state representation is a function of history and may be lossy.
3. The Markov property is a conditional sufficiency statement comparing the full-history one-step law with the state-based one-step law.
4. Once a representation is Markov, the process can be described as an MDP with local transition-reward dynamics.
5. State-based policies and state-based value functions become legitimate because the relevant conditioning structure has been justified.
6. Bellman equations require more than the algebraic return recursion; they require the right Markov structure.

If those statements feel solid, the next chapters can safely build recursive value theory on top of them.

---

## 16. Mastery check

You understand this chapter if you can answer these questions precisely.

1. Why must history be defined before state?
2. What does the equation $S_t = f(H_t)$ mean, and what does it *not* mean?
3. In the Markov condition, what information is being compared on the left side and the right side of the conditional law?
4. How can a useful summary still fail to be Markov?
5. What new local description becomes available once the representation is Markov?
6. Why is the algebraic return recursion not enough by itself to justify a Bellman equation?
7. What does the performance objective judge: immediate reward or long-run expected return?

If any answer comes out vague, fix it now.  
This is the chapter that separates genuine understanding from symbolic imitation.
