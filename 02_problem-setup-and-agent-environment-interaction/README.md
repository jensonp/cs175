# Chapter 2 — Problem Setup and Agent–Environment Interaction

## What this chapter locks in

This chapter fixes the *interaction contract* of reinforcement learning before any Markov model is introduced.

If this chapter is vague, later chapters become harder than they need to be for three separate reasons.

First, the reward index starts looking arbitrary instead of causal.  
Second, conditioning statements later in Bellman equations start looking magical instead of routine.  
Third, learners start using words like *observation*, *history*, and *state* as if they were interchangeable.

The purpose of this chapter is to prevent that.

By the end of the chapter, you should be able to say precisely:

- what exists at the decision point at time $t$,
- what happens before and after action $A_t$,
- why the reward is written $R_{t+1}$,
- what the difference is between an observation, a history, and a state summary,
- what information a policy is allowed to act on,
- what the most general pre-Markov environment law looks like,
- and what object reinforcement learning is actually trying to optimize.

Nothing in this chapter assumes the Markov property.  
Nothing in this chapter assumes a finite state space.  
Nothing in this chapter assumes that the current observation is enough.

---

## 1. Time and the decision point

Time is discrete:

$$
t \in \{0,1,2,\ldots\}.
$$

At each index $t$, there is a **decision point**.  
A decision point is the moment just before the agent chooses action $A_t$.

That phrase matters because it tells you what information is available *before* the action and what information only appears *after* the environment reacts.

For this chapter, keep the following picture in mind.

At the decision point indexed by $t$:

- some information from the past interaction is already available,
- the agent uses allowed information to choose action $A_t$,
- the environment reacts,
- then a new reward and new post-action information are produced.

The entire subject sits on top of that order.

---

## 2. The order of events at time $t$

The causal order is:

1. The agent reaches the decision point at time $t$ with some available information.
2. The agent chooses action $A_t$.
3. The environment reacts to that action.
4. The agent then receives the immediate consequence of that reaction:
   - reward $R_{t+1}$,
   - and whatever new observation or information becomes available for the next decision point.

So the first post-action outcome tied to $A_t$ is indexed by $t+1$, not by $t$.

This is not cosmetic bookkeeping.

It tells you two things at once:

- **which action caused the reward**, and
- **when the reward becomes observable**.

If you ignore that order, later recursions may still be memorized, but they stop feeling inevitable.

---

## 3. Why the reward is written $R_{t+1}$

The reward caused by action $A_t$ is observed only after the environment reacts to that action.

So the reward belongs to the next post-action outcome, and the correct symbol is

$$
R_{t+1}.
$$

It is not written $R_t$ because the reward is not available at the instant *before* action $A_t$ is chosen.

This is exactly why the return later starts from

$$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots
$$

and exactly why the recursion later takes the form

$$
G_t = R_{t+1} + \gamma G_{t+1}.
$$

The first term of return from time $t$ is the first reward that happens *after* the decision made at time $t$.

That is the whole reason for the shift.

---

## 4. The primitive interaction objects

At the most general level, the interaction involves the following primitive random variables.

### Observation

$$
O_t
$$

This is information revealed by the environment and available at the decision point indexed by $t$.

An observation may be rich enough to identify the underlying situation exactly.  
It may also be partial, noisy, delayed, aliased, or incomplete.

So an observation is **not automatically a state** and is **not automatically Markov**.

### Action

$$
A_t
$$

This is the action chosen by the agent at decision time $t$.

### Reward

$$
R_{t+1}
$$

This is the immediate scalar consequence observed after the environment reacts to action $A_t$.

At this stage, those are the only objects you need to regard as primitive.

---

## 5. History comes before state

Before introducing any state notion, you need the most complete record that is available in principle at the current decision point.

A standard history at time $t$ is

$$
H_t = (O_0, A_0, R_1, O_1, A_1, R_2, \ldots, O_t).
$$

The exact formatting varies a little across books and implementations, but the structural point is always the same:

- $H_t$ contains the interaction up to the current decision point,
- $H_t$ is available *before* action $A_t$ is chosen,
- and any later state representation must be built from information available in that history.

This order matters:

1. define the interaction process,
2. define the history,
3. define a summary of history,
4. then ask whether that summary is Markov.

If you skip history and jump straight to “state,” the word *state* starts doing work it has not earned.

---

## 6. Observation, history, and policy input are different objects

Three distinct questions are floating around already, and they should not be collapsed.

### Observation $O_t$

This answers: **what is directly revealed now?**

It is the current environmental output at the decision point.

### History $H_t$

This answers: **what interaction record is available in principle up to now?**

It contains accumulated past information up to the current decision point.

### Policy input $X_t$

This answers: **what information is the policy actually allowed to condition on?**

The policy does not have to use the full history.  
It might use

- the current observation only,
- the full history,
- a hand-designed summary of history,
- or a learned representation constructed from past interaction.

So $X_t$ is a general placeholder for the information summary the policy uses.

Later, one especially important case will be when the policy input is a state summary $S_t = f(H_t)$.

But that has not been assumed yet.

---

## 7. The most general environment law before any Markov assumption

At this point, the environment should be understood in the most general way.

It is the stochastic mechanism that maps the current decision context and current action to the next outcome.

Before any Markov restriction is imposed, the next outcome may depend on the **entire history**, not just on a compressed state variable.

A generic one-step law is therefore of the form

$$
P(O_{t+1}, R_{t+1} \mid H_t, A_t).
$$

Read that slowly.

It says:

- fix the current full history $H_t$,
- fix the action $A_t$,
- then the environment induces a conditional distribution over the next observation and next reward.

This is the correct pre-Markov object.

Why this matters:

- it is the unrestricted one-step law,
- it makes clear that the past may matter through more than the current observation,
- and it gives you the exact object that later chapters will simplify when a Markov state representation is introduced.

That is the missing bridge many learners never get shown explicitly.

---

## 8. What the agent is

At this level of abstraction, the agent is the decision rule that maps allowed information to actions.

The agent is not the environment.  
The agent is not the reward process.  
The agent is not the value function.

The agent is the mechanism that selects actions from available information.

That information might be rich or poor, exact or approximate, current or accumulated.  
The only question for now is what information the policy is allowed to use.

---

## 9. Policies

A **policy** is the object being optimized.

### Deterministic policy

A deterministic policy maps an allowed information summary $x$ to a single action:

$$
\pi : x \mapsto a.
$$

### Stochastic policy

A stochastic policy assigns probabilities to actions:

$$
\pi(a \mid x) = P(A_t = a \mid X_t = x).
$$

This notation is intentionally written with $x$ rather than with $s$.

That is because, at this stage, we have *not* yet established that the policy input is a Markov state.

### Why stochastic policies matter

A stochastic policy is not merely a deterministic policy with accidental noise.

Stochasticity matters because:

- exploration may require positive probability on multiple actions,
- the available information may leave genuine residual uncertainty,
- and later policy-gradient methods optimize distributions over actions directly.

So stochastic policies are part of the subject itself, not an afterthought.

---

## 10. What reinforcement learning is optimizing

At an informal level, reinforcement learning is trying to choose a policy whose long-run interaction with the environment is good.

The environment responds stochastically.  
The policy influences which actions are taken.  
The downstream rewards depend on the interaction of both.

So the thing being optimized is **the policy**, not the next reward in isolation and not the environment dynamics.

The exact mathematical objective will be written later using return and expectations, but the logical structure is already fixed:

- policies generate actions,
- actions influence future trajectories,
- trajectories generate rewards,
- and the goal is to choose the policy with better long-run consequences.

---

## 11. Episodic and continuing tasks

This chapter does not yet need the full objective machinery, but it should mark the two main task types.

### Episodic tasks

Interaction is divided into episodes.  
An episode starts from some initial condition and eventually terminates.

At termination, there is no further action choice inside that episode.

### Continuing tasks

Interaction does not naturally terminate.  
The process keeps unfolding across decision times.

Later chapters will specify how return is defined in each case.  
For now, the important point is that the interaction contract from earlier sections applies in both settings.

The event order does not change just because the task type changes.

---

## 12. Terminal points and index limits

In episodic tasks, there is a last decision time within an episode.

Suppose the final action in an episode is chosen at time $T-1$.

Then:

- the last chosen action is $A_{T-1}$,
- the final immediate reward tied to that action is $R_T$,
- and after termination there is no next within-episode action $A_T$.

This detail matters because later recursions often treat terminal continuation terms specially.

So even before value functions appear, it is useful to be clear about the index boundary.

---

## 13. What has **not** been assumed yet

This chapter is intentionally narrow.  
Several things are still missing on purpose.

### No Markov assumption

We have **not** assumed that some current summary makes the future independent of the rest of the past.

### No state variable has been granted special status

A state summary may later be introduced, but no summary has yet been declared sufficient.

### No finite-state or finite-action assumption

Nothing here requires finite spaces.

### No value function yet

Value functions are expectations of return under a policy or under optimal control.  
They come later because the interaction process has to be specified first.

### No Bellman equation yet

The return recursion is not even defined formally yet, so Bellman structure would be premature here.

These omissions are not weaknesses.  
They are scope control.

---

## 14. Common confusions this chapter should block

### Confusion 1: observation and state are the same thing

Not necessarily.

An observation is what is directly revealed now.  
A state will later be a summary used for decision making.  
A Markov state will later be a summary with a particular predictive sufficiency property.

Those are different layers.

### Confusion 2: the reward should share the action’s time index

No.

The action is chosen at time $t$.  
The reward caused by that action is observed after the transition, so it is indexed by $t+1$.

### Confusion 3: the environment already has MDP form

Not yet.

At this chapter’s level of generality, the one-step law may depend on the whole history:

$$
P(O_{t+1}, R_{t+1} \mid H_t, A_t).
$$

### Confusion 4: the policy must use only the current observation

False.

The policy may use any allowed information summary $X_t$.

### Confusion 5: “state” is whatever name we give the current representation

Also false.

A summary does not become Markov because we call it a state.  
That is a later property that has to be checked.

---

## 15. What this chapter allows you to conclude

After this chapter, you are allowed to say all of the following.

1. At time $t$, the agent acts *before* the next reward is observed.
2. The reward tied to action $A_t$ is correctly written $R_{t+1}$.
3. A history $H_t$ is available conceptually before any state summary is defined.
4. The policy acts on some allowed information summary $X_t$.
5. The general pre-Markov environment law can depend on the full history and current action.
6. Reinforcement learning is optimizing a policy, not merely reacting greedily to the next scalar signal.

If any one of those feels fuzzy, you are not ready to compress the problem into an MDP yet.

---

## 16. Mastery check

You understand this chapter if you can answer each question cleanly.

1. What information is available at the decision point indexed by $t$?
2. Why is the reward caused by action $A_t$ written $R_{t+1}$?
3. What is the difference between an observation $O_t$ and a history $H_t$?
4. What does the generic one-step law $P(O_{t+1}, R_{t+1} \mid H_t, A_t)$ say?
5. What is the difference between the policy input $X_t$ and a future state representation $S_t$?
6. What exactly has **not** yet been assumed in this chapter?

If you cannot answer those without drifting into vague language, do not move on.  
Every later chapter will lean on these distinctions.
