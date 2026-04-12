# Chapter 2 — Problem Setup and Agent–Environment Interaction

## Why this chapter exists

Before reinforcement learning can talk about value functions, Bellman equations, optimal control, or policy gradients, it has to answer a more basic question: **what exactly is happening at each time step, and in what order does it happen?** If that question is left vague, later formulas look arbitrary. The reward index starts to feel like a notational trick. Conditional probabilities start to look mystical. Words like *observation*, *history*, and *state* get used as though they were interchangeable, even though they answer different questions.

This chapter fixes that foundation. Its job is not yet to simplify the world into an MDP. Its job is to describe the interaction process in the most general way that is still precise enough to support later theory. That means three things have to be made explicit from the beginning.

First, we must identify the **decision point**: the moment at which the agent chooses an action. Second, we must distinguish the objects that exist before the action from the objects that appear only after the environment reacts. Third, we must avoid granting the word *state* too much power too early. A state representation, if one exists, will later be a summary of the past with a special predictive property. That property has not been assumed yet.

So the point of this chapter is not to compress the problem. It is to describe the interaction contract clearly enough that later compression, when it comes, will be justified rather than hand-waved.

Before the formal sections begin, one local status distinction should be frozen. A **policy** can be defined before a Markov state has been justified, but at that stage it must be read as a rule over whatever information object is actually available at the decision point. Early in the chapter, that object may be the current observation or the full history. Only later, if a state representation is shown to preserve the right predictive information, may the policy be treated as a policy over that state in the exact MDP sense. So the reader should not infer “policy over states” merely from the appearance of action-selection notation. The policy concept comes early. The state-sufficiency license comes later.

---

## 1. Time, decision points, and the order of events

### Why this section exists

The first thing reinforcement learning needs is a precise answer to the question: **when is the agent allowed to act, and what information does it have at that moment?** Without that, it is impossible to tell which quantities are available before the action, which ones are consequences of the action, and why the reward is indexed the way it is. This section exists because every later definition inherits its timing from this one.

### The object being introduced

The key object here is not yet a state or a value function. It is the **decision point at time** <em>t</em>. A decision point is a moment in the interaction process at which the agent is about to choose an action. What is fixed at that moment is the information already revealed from past interaction. What is not yet fixed is the current action <em>A</em><sub>t</sub>, the environment’s response to that action, the next reward, and the next observation.

This object matters because it tells us what can legitimately appear on the right-hand side of a policy definition and what must wait until after the action has been taken.

A local working definition of **policy** is needed here. In this chapter, a policy should be read as a rule that maps whatever information is legitimately available at the decision point into a distribution over actions. At this stage, that information may be an observation, a full history, or some chosen summary of history. What must **not** be assumed yet is that this input already has the stronger status of a Markov state. That stronger claim belongs later.

### Formal definition

Time is discrete:

<p><em>t</em> ∈ {0, 1, 2, ...}.</p>

At each time index <em>t</em>, there is a **decision point**: the moment immediately before the agent chooses action <em>A</em><sub>t</sub>.

The causal order at time <em>t</em> is:

1. The agent arrives at the decision point with information already available from past interaction.
2. The agent chooses action <em>A</em><sub>t</sub>.
3. The environment reacts to that action.
4. The agent then receives the next reward <em>R</em><sub>t+1</sub> and the next observation <em>O</em><sub>t+1</sub> or other post-action information.

### Interpretation

The most important thing to notice is that **time** <em>t</em> **labels the action choice, not the post-action outcome**. The agent acts at time <em>t</em>, and only after that action does the next reward and next observation appear. So the decision point is not “the whole step.” It is specifically the pre-action moment.

This is why the notation later becomes natural rather than annoying. The action at time <em>t</em> is chosen using information available at that time. The reward caused by that action is not yet known at the moment of choice. It belongs to the next post-action outcome.

### Boundary conditions, assumptions, and failure modes

This description assumes discrete decision times. In continuous-time control, the mathematical setup is different, but the same causal discipline still matters: one must still distinguish what is available before the control is applied from what is observed afterward.

A common failure mode is to talk loosely as though “time <em>t</em>” refers simultaneously to the pre-action and post-action situation. That slippage produces index confusion later. If you let the same time index mean both “before the action” and “after the environment’s reaction,” then return definitions and Bellman recursions become hard to parse for no good reason.

Another hidden assumption is that the chapter is describing the interaction from the agent’s perspective. The agent experiences an information stream, chooses actions, and then receives consequences. That is the operational viewpoint the rest of the subject uses.

### Fully worked example

Consider a thermostat controller that chooses between two actions at each minute:
$$
A_t \in \{\text{heat on}, \text{heat off}\}.
$$
At minute $t$, the controller can already read the current measured temperature $O_t$. That reading belongs to the decision point. The controller has it **before** it chooses the action. The next temperature reading $O_{t+1}$ does not yet exist for the controller, because the room has not yet responded to the current action. The reward $R_{t+1}$ also does not yet exist for the controller at the instant of choice, because that reward is meant to summarize the consequences of what is about to be done.

Now follow the order as a causal chain rather than as a checklist.

At the decision point indexed by $t$, the controller knows the current temperature reading $O_t$ and any other previously accumulated information. Using that already available information, it chooses $A_t$, for example “heat on.” Once that choice is made, the environment side of the interaction takes over: the heater affects the room, the room temperature changes according to its thermal dynamics, energy is consumed, and only after those physical consequences occur does the controller receive the next post-action information. That post-action information has two parts. One part is the new observation $O_{t+1}$, the next measured temperature. The other part is the reward $R_{t+1}$, which may combine comfort and energy cost into a single scalar signal.

Now ask what the sequence licenses. Because $O_t$ is present before the action, it is legitimate for the policy to condition on $O_t$. Because $O_{t+1}$ and $R_{t+1}$ are produced only after the action and the environment’s response, they are not legitimate inputs to the choice of $A_t$. That is the exact reason the first reward tied to action $A_t$ is written as $R_{t+1}$ rather than $R_t$. The index is not decorative. It marks the first consequence that becomes visible only after the action’s effect begins.

The general lesson is that the action time marks the decision, while the next reward and next observation mark the earliest visible consequences of that decision.

### Misconception block

**Do not confuse “the time step” with “the agent’s information at the decision point.”**  
A time step often informally includes both acting and observing consequences. But the policy is defined only at the pre-action moment. That is the moment whose available information matters.

**Do not think the order is a bookkeeping choice.**  
It is a causal choice. The notation is encoding which quantities are known before the action and which ones are produced after the action.

### Connection to later material

Everything later depends on this timing. The return from time <em>t</em> begins with the first reward observed after choosing <em>A</em><sub>t</sub>. Conditional expectations in Bellman equations are conditioned on variables available at the decision point. Policy definitions only take as input information available before the action. So this section is not preliminary decoration; it is the clock that the rest of the theory runs on.

### Retain / Do not confuse

Retain:

- Time <em>t</em> labels the **decision point** and the chosen action <em>A</em><sub>t</sub>.
- The environment reacts **after** <em>A</em><sub>t</sub>.
- The first reward tied to <em>A</em><sub>t</sub> is <em>R</em><sub>t+1</sub>.

Do not confuse:

- pre-action information with post-action outcomes,
- “same step” in informal speech with “same index” in formal notation.

---

## 2. Observation, action, and reward: the primitive interaction objects

### Why this section exists

Once the event order is fixed, we need names for the basic random variables that participate in the interaction. This section exists because later objects—history, state summaries, policies, return, and value functions—are all built out of these primitive ingredients. If these primitives are not interpreted correctly, later derived objects will inherit the confusion.

### The object being introduced

There are three primitive objects at this stage:

- the **observation** <em>O</em><sub>t</sub>,
- the **action** <em>A</em><sub>t</sub>,
- the **reward** <em>R</em><sub>t+1</sub>.

Each answers a different question. The observation tells us what information is currently revealed. The action records what the agent chooses to do. The reward records the immediate scalar consequence that becomes available after the environment reacts.

What is fixed and what varies matters here. At the decision point indexed by <em>t</em>, <em>O</em><sub>t</sub> may already be known, <em>A</em><sub>t</sub> has not yet been chosen, and <em>R</em><sub>t+1</sub> has not yet been observed.

### Formal definitions

The primitive variables are:

<p><em>O</em><sub>t</sub> = observation available at decision time <em>t</em>,</p>

<p><em>A</em><sub>t</sub> = action chosen by the agent at time <em>t</em>,</p>

<p><em>R</em><sub>t+1</sub> = reward observed after the environment reacts to <em>A</em><sub>t</sub>.</p>

### Interpretation

The word *observation* should be read carefully. An observation is not automatically a complete description of the world. It is simply what the environment reveals to the agent at that moment. It may be complete, partial, noisy, delayed, aliased, or filtered. That is why the chapter uses <em>O</em><sub>t</sub> rather than immediately writing down a state variable and pretending the problem is already Markov.

The action <em>A</em><sub>t</sub> is the agent’s current intervention. The reward <em>R</em><sub>t+1</sub> is a scalar feedback signal, but it is not the whole future objective. It is only the immediate consequence now visible after the action has had its first effect.

### Boundary conditions, assumptions, and failure modes

A hidden but important assumption is that reward is scalar. That is standard in RL, but it does not mean the underlying problem is truly one-dimensional. It means the environment or modeling setup has compressed the immediate feedback into a single number.

A major failure mode is to over-interpret the observation. Students often begin using *observation* and *state* as synonyms. That is unsafe. An observation is what is seen now. A state, later, will be a representation used for prediction and control, and a **Markov** state will have a specific sufficiency property. Those are stronger claims.

Another common failure mode is to treat the immediate reward as “the thing being optimized.” It is not. The reward is the local signal; the policy will later be judged by long-run return.

A second local distinction should be made explicit here. A one-step reward is part of the interaction stream. A policy criterion is a long-run object built from that stream. So even in this early chapter, the reward should be read as the immediate post-action signal, not as the full standard by which a policy is judged. That later criterion will be an expectation of return. The reason to say this now is preventive: many later confusions begin when a reader silently upgrades “the reward I just observed” into “the objective the policy is optimizing.” The latter is downstream of the former, not identical to it.

### Fully worked example

Imagine a robot navigating a building. At each decision point, its camera image is the observation <em>O</em><sub>t</sub>. It chooses an action <em>A</em><sub>t</sub> from

<p>{forward, left, right, stop}.</p>

After the move, the environment returns a reward:

- +10 if the robot reaches the goal,
- -1 for taking a normal step,
- -20 if it collides.

Now ask what each object means.

At time <em>t</em>, the camera image <em>O</em><sub>t</sub> is available. That image may not reveal the full floor plan, whether a hallway loops back, or whether an unseen obstacle lies around the corner. So <em>O</em><sub>t</sub> is information, but not necessarily a complete world description.

The robot then chooses <em>A</em><sub>t</sub>. Suppose it chooses “forward.”

Only after that move does the robot find out what happened. If it collides, the collision penalty is part of <em>R</em><sub>t+1</sub>. If it reaches the goal, the goal reward is part of <em>R</em><sub>t+1</sub>. If neither happens, it may receive -1. It also gets a new image <em>O</em><sub>t+1</sub>.

What this example teaches is not merely that the symbols are different, but that they occupy different causal positions. The camera image $O_t$ is already present when the robot is deciding, so it is legitimate policy input. The action $A_t$ is the intervention chosen on the basis of that currently available information. The reward $R_{t+1}$ is neither a second observation nor a long-run objective; it is the first scalar consequence that becomes visible only after the environment has responded to the chosen action. The example therefore stabilizes three distinctions at once: observation is an information object, action is a decision object, and reward is a post-action feedback object.

### Misconception block

**Observation is not automatically state.**  
A blurry camera frame can be an observation. It need not contain enough information to predict the future on its own.

**Reward is not probability, not value, and not the total objective.**  
It is an immediate scalar consequence. Later we will aggregate rewards across time to define return.

### Connection to later material

History will be built from observations, actions, and rewards. State summaries will later be functions of history. Return will be a sum of future rewards starting from <em>R</em><sub>t+1</sub>. Value functions will take expectations of that return. So these primitive variables are the atoms from which the rest of the chapter and later theory are assembled.

### Retain / Do not confuse

Retain:

- <em>O</em><sub>t</sub>: what is revealed now.
- <em>A</em><sub>t</sub>: what the agent chooses now.
- <em>R</em><sub>t+1</sub>: the immediate scalar consequence observed after the action’s effect begins.

Do not confuse:

- observation with a guaranteed Markov state,
- immediate reward with long-run objective.

---

## 3. History comes before state

### Why this section exists

If we do not yet assume the current observation is enough, then what is the most complete decision-relevant record available in principle at time <em>t</em>? That question forces the notion of **history**. This section exists because one cannot responsibly introduce a state summary until one first identifies the larger object that is being summarized.

### The object being introduced

The object is the **history** <em>H</em><sub>t</sub>. It is the accumulated interaction record up to the current decision point. What is fixed when discussing <em>H</em><sub>t</sub> is the sequence of observations, actions, and rewards that have already occurred. What varies across possible trajectories is which particular sequence occurred.

The role of history is conceptual: it is the most information-rich object available before the next action is chosen. Later representations—memory states, features, recurrent hidden states, learned embeddings, or classical MDP states—must all be understood as summaries or functions of this underlying record.

### Formal definition

A standard history at time <em>t</em> is

<p><em>H</em><sub>t</sub> = (<em>O</em><sub>0</sub>, <em>A</em><sub>0</sub>, <em>R</em><sub>1</sub>, <em>O</em><sub>1</sub>, <em>A</em><sub>1</sub>, <em>R</em><sub>2</sub>, ..., <em>O</em><sub>t</sub>).</p>

This history contains everything observed up to the decision point at which <em>A</em><sub>t</sub> is about to be chosen.

### Interpretation

The structure of <em>H</em><sub>t</sub> matters. It ends with <em>O</em><sub>t</sub>, not with <em>A</em><sub>t</sub>, because <em>A</em><sub>t</sub> has not yet been chosen. The history is therefore a **pre-action object**. It records what the agent could in principle know before deciding what to do now.

A helpful way to read the definition is this: history is not “the past” in a vague sense. It is the exact decision-time record available for conditioning. That is why it comes before any notion of state. A state summary, if introduced later, should be a function of information available in <em>H</em><sub>t</sub>, not a magical external label that appears without justification.

### Boundary conditions, assumptions, and failure modes

Different texts format history slightly differently. Some include an initial reward convention, some package post-action observation and reward together, and some use states instead of observations once Markov structure has been assumed. Those formatting choices do not change the conceptual role of history.

A common failure mode is to jump directly from “current observation” to “current state” without checking whether the observation actually contains enough information. Another failure mode is subtler: some learners call any internal memory vector a *state* and assume that settles the matter. It does not. A memory vector is at most a candidate summary of history. Whether it has the required predictive sufficiency is a separate question.

### Fully worked example

Consider a maze with two visually identical intersections. At both intersections, the robot’s current observation is the same: a picture showing one corridor to the left and one corridor to the right. So

<p><em>O</em><sub>t</sub> = “left-right intersection”</p>

in both places.

But suppose the optimal action differs between the two intersections because one of them was reached by coming from the entrance and the other by coming from a loop. If the robot turns left in the first case, it gets closer to the goal; if it turns left in the second case, it goes into a dead end.

Now check what each object is telling us.

- The current observation <em>O</em><sub>t</sub> is the same in both situations.
- The histories <em>H</em><sub>t</sub> are different, because the past sequences of turns and observations differ.
- Therefore the correct action can depend on the history even when the current observation does not distinguish the cases.

What conclusion does this allow?

It shows that the observation alone need not be sufficient for decision making. So any valid state representation for control, if one exists, may need to summarize more than the current observation.

The general pattern is important. Whenever two different pasts lead to the same current observation but require different actions or imply different future distributions, the current observation is not enough.

### Misconception block

**Do not confuse history with “everything that ever happened in the universe.”**  
History here means the interaction record available from the agent–environment process up to the current decision point.

**Do not confuse a summary of history with the history itself.**  
A summary may discard information. That is precisely why one later has to ask whether the discarded information matters.

### Connection to later material

This section prepares the ground for state representations, partial observability, belief states, recurrent policies, and the Markov property. The later question “is this representation a Markov state?” only makes sense after history has been identified as the fuller object being summarized.

### Retain / Do not confuse

Retain:

- History <em>H</em><sub>t</sub> is the full interaction record available before choosing <em>A</em><sub>t</sub>.
- It ends at <em>O</em><sub>t</sub>, not at <em>A</em><sub>t</sub>.
- State, later, must be understood relative to history.

Do not confuse:

- same observation with same history,
- having a summary with having a sufficient summary.

---

## 4. Observation, history, policy input, and state summary are different objects

### Why this section exists

Once history has been introduced, another question appears immediately: **what information is the policy actually allowed to use?** The answer need not be “the full history.” This section exists to separate four commonly collapsed notions: the currently revealed observation, the full interaction history, the information summary the policy conditions on, and a later state representation with special predictive properties.

### The object being introduced

The new object is the **policy input** <em>X</em><sub>t</sub>. It is whatever information summary the policy actually uses at the decision point. What is fixed is the available information from past interaction. What varies is how much of that information the policy is permitted to keep or process.

The role of <em>X</em><sub>t</sub> is to make policy definitions precise without prematurely assuming the input is a Markov state.

### Formal definition

We distinguish the following objects:

- **Observation**:  
  <p><em>O</em><sub>t</sub> = the information directly revealed at decision time <em>t</em>.</p>

- **History**:  
  <p><em>H</em><sub>t</sub> = (<em>O</em><sub>0</sub>, <em>A</em><sub>0</sub>, <em>R</em><sub>1</sub>, <em>O</em><sub>1</sub>, <em>A</em><sub>1</sub>, <em>R</em><sub>2</sub>, ..., <em>O</em><sub>t</sub>).</p>

- **Policy input**:  
  <p><em>X</em><sub>t</sub> = the information summary on which the policy conditions at time <em>t</em>.</p>

A later state representation may be written as

<p><em>S</em><sub>t</sub> = <em>f</em>(<em>H</em><sub>t</sub>),</p>

but at this stage no special sufficiency property has yet been assumed for <em>S</em><sub>t</sub>.

### Interpretation

These objects answer different questions.

- <em>O</em><sub>t</sub>: What is directly seen now?
- <em>H</em><sub>t</sub>: What full interaction record is available in principle now?
- <em>X</em><sub>t</sub>: What information is the policy actually allowed to use now?
- <em>S</em><sub>t</sub>: A candidate summary of history that may later be tested for the Markov property.

The key point is that <em>X</em><sub>t</sub> is a neutral symbol. It lets us define policies in a general way. Sometimes <em>X</em><sub>t</sub> = <em>O</em><sub>t</sub>. Sometimes <em>X</em><sub>t</sub> = <em>H</em><sub>t</sub>. Sometimes <em>X</em><sub>t</sub> is a compressed memory vector or engineered feature map. Using <em>x</em> rather than <em>s</em> in policy notation prevents us from smuggling in the Markov assumption by notation alone.

### Boundary conditions, assumptions, and failure modes

There is an important hidden distinction between **available information** and **used information**. The full history may exist conceptually even if the implemented policy discards most of it. If the policy is memoryless, then <em>X</em><sub>t</sub> may equal <em>O</em><sub>t</sub> even though <em>H</em><sub>t</sub> is much richer.

A common failure mode is to say “the policy uses the state” before the word *state* has been earned. Another is to assume that because a neural network maintains a hidden vector, that vector is automatically sufficient. It may be useful; it is not automatically Markov.

### Fully worked example

Return to the maze with visually identical intersections.

Suppose we compare three policies.

**Policy 1: observation-only policy.**  
It conditions only on the current image:

<p><em>X</em><sub>t</sub> = <em>O</em><sub>t</sub>.</p>

Because both intersections look the same, this policy must choose the same action distribution in both cases.

**Policy 2: history-based policy.**  
It conditions on the full interaction record:

<p><em>X</em><sub>t</sub> = <em>H</em><sub>t</sub>.</p>

Now the policy can distinguish which intersection it is at by using earlier turns and observations.

**Policy 3: summarized-memory policy.**  
It uses a hand-designed memory bit that records whether the robot last turned left or right:

<p><em>X</em><sub>t</sub> = memory summary extracted from <em>H</em><sub>t</sub>.</p>

This summary is smaller than the full history but may still be enough for the task if that one bit captures the distinction that matters.

This example shows three different asymmetries that are easy to blur if one moves too quickly. First, identical current observations do not force identical histories; the same visible situation can be reached through materially different pasts. Second, once the full history is available, the policy still need not condition on all of it. The policy may deliberately compress the history into a smaller memory summary if that is enough for its own decision rule. Third, the usefulness of such a summary does not yet prove Markov sufficiency. A summary can improve decision making relative to the raw observation while still failing the stronger test required for Bellman-style state reasoning later.

The general lesson is that policy input is a design choice or learned representation choice. State, in the stronger sense used later, is a property claim about predictive sufficiency.

### Misconception block

**Do not confuse “what exists” with “what the policy conditions on.”**  
The history may exist even if the policy ignores it.

**Do not confuse “policy input” with “Markov state.”**  
Every Markov state can serve as policy input, but not every policy input deserves to be called a Markov state.

### Connection to later material

This distinction is essential for understanding partially observable RL, belief states, recurrent policies, feature learning, and the Markov property. It also matters for proofs. Later Bellman-style recursions become simple only when the policy input has the right sufficiency property. Until then, the safe general input symbol is <em>X</em><sub>t</sub>, not <em>S</em><sub>t</sub>.

### Retain / Do not confuse

Retain:

- <em>O</em><sub>t</sub>: current revealed information.
- <em>H</em><sub>t</sub>: full available record.
- <em>X</em><sub>t</sub>: actual policy input.
- <em>S</em><sub>t</sub>: possible later state summary.

Do not confuse:

- policy input with history,
- policy input with a Markov state,
- observation with the whole decision context.

---

## 5. The most general environment law before any Markov assumption

### Why this section exists

Once we know what information exists at the decision point and what action is taken there, we can ask the next structural question: **what object describes how the environment produces the next outcome?** Before any Markov simplification, the answer cannot be a transition law that depends only on a current state, because no such state has yet been justified. This section exists to write down the correct unrestricted one-step law.

### The object being introduced

The key object is the conditional distribution

<p><em>P</em>(<em>O</em><sub>t+1</sub>, <em>R</em><sub>t+1</sub> | <em>H</em><sub>t</sub>, <em>A</em><sub>t</sub>).</p>

This is the most general one-step environment law at the current level of abstraction. What is fixed when reading it are the current history <em>H</em><sub>t</sub> and the chosen action <em>A</em><sub>t</sub>. What varies are the possible next observation–reward outcomes <span>(<em>O</em><sub>t+1</sub>, <em>R</em><sub>t+1</sub>)</span>.

This object answers the question: **given everything the process has revealed so far and the action chosen now, what distribution does the environment induce over the next immediate outcome?**

### Formal definition

Before any Markov assumption, a generic one-step environment law is

<p><em>P</em>(<em>O</em><sub>t+1</sub>, <em>R</em><sub>t+1</sub> | <em>H</em><sub>t</sub>, <em>A</em><sub>t</sub>).</p>

### Interpretation

Read the formula in the right order.

First, hold fixed a particular history <em>H</em><sub>t</sub> = <em>h</em>. This means you are fixing the entire interaction record up to the current decision point. Next, hold fixed an action <em>A</em><sub>t</sub> = <em>a</em>. Once those are fixed, the environment defines a probability distribution over what comes next: the next observation and the next reward.

The first thing to notice is that the law conditions on **history**, not merely on the current observation. That is deliberate. It expresses the most general possibility that the future can depend on aspects of the past that are not captured by what is currently observed.

The second thing to notice is that reward and next observation appear together. This is useful because both are immediate consequences of the same environment reaction to <em>A</em><sub>t</sub>.

### Boundary conditions, assumptions, and failure modes

The formula does **not** assume a Markov state exists. It does **not** assume finite observation or action spaces. It does **not** require that the current observation be sufficient.

A common overgeneralization is to replace the law too early by something like

<p><em>P</em>(<em>O</em><sub>t+1</sub>, <em>R</em><sub>t+1</sub> | <em>O</em><sub>t</sub>, <em>A</em><sub>t</sub>).</p>

That replacement is only valid if the current observation is actually sufficient. Many problems do not satisfy that.

A second failure mode is to think that once we define some summary <em>S</em><sub>t</sub> = <em>f</em>(<em>H</em><sub>t</sub>), the environment law automatically reduces to

<p><em>P</em>(<em>O</em><sub>t+1</sub>, <em>R</em><sub>t+1</sub> | <em>S</em><sub>t</sub>, <em>A</em><sub>t</sub>).</p>

That is not automatic either. It becomes valid only if <em>S</em><sub>t</sub> retains exactly the predictive information needed for the next-step distribution.

### Fully worked example

Suppose a machine has a hidden internal mode, either Mode 0 or Mode 1. The agent never observes the mode directly. The current observation <em>O</em><sub>t</sub> is always the same display light, so the current observation contains no information about the mode.

The action set is

<p><em>A</em><sub>t</sub> ∈ {toggle, stay}.</p>

The environment works as follows:

- If the agent chooses **toggle**, the hidden mode flips.
- If the agent chooses **stay**, the hidden mode remains the same.
- The next reward is +1 if the hidden mode after the action is Mode 1, and 0 otherwise.
- The next observation is again the same uninformative display light.

Now examine two different histories that end in the same current observation.

- In history <em>h</em>, the agent has toggled an odd number of times.
- In history <em>h′</em>, the agent has toggled an even number of times.

Suppose the initial hidden mode was Mode 0. Then these two histories imply different current hidden modes, even though the current observation is identical.

Now choose the action <em>A</em><sub>t</sub> = stay.

Given history <em>h</em>, staying keeps the system in Mode 1, so

<p><em>P</em>(<em>R</em><sub>t+1</sub> = 1 | <em>H</em><sub>t</sub> = <em>h</em>, <em>A</em><sub>t</sub> = stay) = 1.</p>

Given history <em>h′</em>, staying keeps the system in Mode 0, so

<p><em>P</em>(<em>R</em><sub>t+1</sub> = 1 | <em>H</em><sub>t</sub> = <em>h′</em>, <em>A</em><sub>t</sub> = stay) = 0.</p>

What was checked here?

- We checked that the current observation is the same under both histories.
- We checked that the hidden mode differs because the past action sequence differs.
- We then fixed the same current action in both cases.
- The resulting next-reward distributions were different.

What conclusion does that allow?

It proves that the next outcome distribution cannot, in general, be written as a function of the current observation alone. The history matters. So the correct unrestricted one-step law is indeed conditioned on <em>H</em><sub>t</sub> and <em>A</em><sub>t</sub>.

The general lesson is this: whenever two different histories lead to the same current observation but induce different future distributions under the same current action, the observation is not Markov.

### Misconception block

**This does not mean the environment must literally store the full history.**  
The formula is not a statement about internal implementation. It is a statement about the predictive object that is guaranteed to be valid before any compression is justified.

**Do not confuse “we can define a summary” with “the summary is sufficient.”**  
A compression is easy to write. Predictive sufficiency is the hard part.

### Connection to later material

This formula is the bridge to Markov models. Later, if we can find a representation <em>S</em><sub>t</sub> = <em>f</em>(<em>H</em><sub>t</sub>) such that the future depends on the past only through <em>S</em><sub>t</sub>, then the law simplifies. That is exactly what makes MDPs and Bellman equations possible. But the simplification is meaningful only because we first wrote down the unrestricted object honestly.

### Retain / Do not confuse

Retain:

- The correct pre-Markov one-step law is  
  <p><em>P</em>(<em>O</em><sub>t+1</sub>, <em>R</em><sub>t+1</sub> | <em>H</em><sub>t</sub>, <em>A</em><sub>t</sub>).</p>
- It conditions on the full history because the current observation need not be sufficient.

Do not confuse:

- current observation with full predictive context,
- a chosen summary with a justified Markov representation.

---

## 6. The agent and the policy

### Why this section exists

Once the interaction law is clear, we can isolate the agent’s role. The agent is not the whole trajectory, not the reward process, and not the environment dynamics. The agent contributes a particular object: a **policy**. This section exists because reinforcement learning optimizes policies, and that claim only becomes precise once we say what a policy maps from and what it maps to.

### The object being introduced

The object is the **policy**. A policy is a decision rule that takes the allowed information summary at the decision point and produces an action or a distribution over actions. What is fixed is the policy input <em>X</em><sub>t</sub>. What varies is the resulting action choice.

The policy answers the question: **given the information the agent is allowed to use now, how does it choose what to do?**

### Formal definitions

A deterministic policy is a mapping

<p><em>π</em>: <em>x</em> ↦ <em>a</em>.</p>

A stochastic policy is a conditional distribution over actions:

<p><em>π</em>(<em>a</em> | <em>x</em>) = <em>P</em>(<em>A</em><sub>t</sub> = <em>a</em> | <em>X</em><sub>t</sub> = <em>x</em>).</p>

The notation uses <em>x</em>, not <em>s</em>, because we have not yet established that the policy input is a Markov state.

### Interpretation

The deterministic policy says: once the information summary equals <em>x</em>, the action is fixed. The stochastic policy says: once the information summary equals <em>x</em>, the agent randomizes according to a distribution over possible actions.

The important thing to notice first is that a policy is defined relative to its **input object**. If the input is poor, the best achievable policy may still perform poorly. If the input is rich enough, the policy may exploit longer-range structure.

The second thing to notice is that stochasticity is not an implementation accident. It is a legitimate modeling object. A stochastic policy is itself the thing being optimized in many RL methods.

### Boundary conditions, assumptions, and failure modes

A hidden assumption is that the policy only depends on information available at the decision point. It cannot depend on future rewards or future observations.

A common failure mode is to write <em>π</em>(<em>a</em> | <em>s</em>) too early and thereby smuggle in a state assumption. Another is to think that stochastic policies are just deterministic policies with added nuisance noise. That is false in general. Randomization can be essential for exploration, for symmetry breaking, for mixed strategies, or because uncertainty remains after conditioning on available information.

### Fully worked example

Consider a two-armed bandit with actions

<p><em>A</em><sub>t</sub> ∈ {left arm, right arm}.</p>

Since bandits have no evolving observation in the usual simple setup, let the policy input be trivial:

<p><em>X</em><sub>t</sub> = <em>x</em><sub>0</sub></p>

for every <em>t</em>.

Now compare two policies.

**Deterministic policy**

<p><em>π</em>(left arm | <em>x</em><sub>0</sub>) = 1.</p>

This policy always chooses the left arm.

**Stochastic policy**

<p><em>π</em>(left arm | <em>x</em><sub>0</sub>) = 0.7,</p>
<p><em>π</em>(right arm | <em>x</em><sub>0</sub>) = 0.3.</p>

This policy randomizes.

What is being checked here?

- We fix the available information summary <em>x</em><sub>0</sub>.
- We ask how the policy transforms that input into action choice.
- In the deterministic case, the action is fixed.
- In the stochastic case, the action is distributed.

What conclusion does this allow?

It shows that the policy object need not choose a single action pointwise. It can encode a distribution over actions at the same information input.

Now interpret why that matters. Suppose the left arm is believed better but the right arm is still uncertain. A stochastic policy can assign positive probability to both arms, allowing continued exploration. A purely deterministic policy cannot do that unless its input changes.

The general lesson is that the policy is the controllable object. The environment law is not under the agent’s control; the policy is.

### Misconception block

**Reinforcement learning is not optimizing the next action in isolation.**  
It is choosing a policy whose repeated action choices produce better long-run consequences.

**A stochastic policy is not merely “a deterministic policy plus mistakes.”**  
The randomness can be deliberate, structural, and essential.

### Connection to later material

Policy evaluation, policy improvement, actor methods, policy gradients, entropy regularization, and exploration strategies all build directly on this section. The distinction between deterministic and stochastic policies will matter not only conceptually but algorithmically.

### Retain / Do not confuse

Retain:

- The agent is the decision rule.
- A policy maps allowed information to actions or action probabilities.
- Using <em>x</em> instead of <em>s</em> avoids assuming the input is already a Markov state.

Do not confuse:

- agent with environment,
- policy with reward function,
- stochastic policy with accidental noise.

---

## 7. What reinforcement learning is optimizing

### Why this section exists

Once the policy has been defined, we can say what RL is trying to improve. Without this section, a student may mistakenly think the goal is to maximize immediate reward at each step. That is not the general objective. This section exists to identify the policy—not the next reward, not the environment dynamics—as the object of optimization.

### The object being introduced

The relevant object is the **long-run performance of a policy**. The policy shapes the sequence of actions. Those actions influence the trajectory of future observations and rewards. So the quality of a policy cannot be judged by one reward in isolation; it must be judged by the return its induced trajectories tend to produce.

### Formal definition

For an episodic task ending at time <em>T</em>, the return from decision time <em>t</em> is

<p><em>G</em><sub>t</sub> = <em>R</em><sub>t+1</sub> + <em>R</em><sub>t+2</sub> + ... + <em>R</em><sub>T</sub>.</p>

For a continuing task, a discounted return is commonly used:

<p><em>G</em><sub>t</sub> = <em>R</em><sub>t+1</sub> + <em>γ</em><em>R</em><sub>t+2</sub> + <em>γ</em><sup>2</sup><em>R</em><sub>t+3</sub> + ..., with 0 ≤ <em>γ</em> &lt; 1.</p>

Reinforcement learning seeks a policy <em>π</em> that makes the expected return large.

That sentence should be read with full structural precision. The policy is not being judged by one reward in isolation, and it is not being judged by a static score attached to an action label. It is being judged through the trajectory law that it induces jointly with the environment. In other words, a policy changes action probabilities; those changed action probabilities alter which histories and future observations occur; those altered histories change which rewards are later seen; and the return aggregates those rewards across time. The policy-level criterion therefore lives at the level of induced trajectories, not at the level of one isolated step.

### Interpretation

The first thing to notice is that return starts with <em>R</em><sub>t+1</sub>, not <em>R</em><sub>t</sub>. That is now forced by the event order established earlier. The second thing to notice is that the policy is evaluated through the trajectories it induces. The environment responds stochastically, so performance is usually framed in expectation.

This is the right place to see why “maximize immediate reward” can be wrong. An action with smaller immediate reward may lead to better future states, better information, or better future reward opportunities. Return captures that delayed-consequence structure.

### Boundary conditions, assumptions, and failure modes

Discounted return assumes 0 ≤ <em>γ</em> &lt; 1 so that distant future rewards are geometrically down-weighted and the infinite series is controlled. In episodic tasks, discounting may or may not be used, but termination already bounds the sum.

A common failure mode is to interpret <em>γ</em> merely as a numerical trick. It does control convergence in continuing tasks, but conceptually it also determines how much future reward matters relative to immediate reward.

Another failure mode is to equate reward with return. Reward is a one-step scalar signal. Return is an aggregate across future time.

### Fully worked example

Suppose an agent at time $t$ has two available choices. One choice gives an immediate reward of $R_{t+1}=5$ but leads to poor future outcomes, so the subsequent rewards are $R_{t+2}=0$ and $R_{t+3}=0$. The other choice gives only $R_{t+1}=1$ immediately, but changes the later trajectory so that $R_{t+2}=4$ and $R_{t+3}=4$. If the task is episodic and ends at time $t+3$, then the first choice produces
$$
G_t = 5 + 0 + 0 = 5,
$$
while the second produces
$$
G_t = 1 + 4 + 4 = 9.
$$
The point is not merely that one sum is larger. The example shows why immediate reward and return answer different questions. Immediate reward tells you what became visible right after the action. Return tells you what that action set in motion across the rest of the episode. A reader who remembers only the local reward will prefer the first action. A reader who tracks the return correctly will see that the second action is better for the objective actually being optimized.

If instead the task were continuing with discount factor <em>γ</em> = 0.5, then:

For Action A,

<p><em>G</em><sub>t</sub> = 5 + 0.5·0 + 0.5<sup>2</sup>·0 = 5.</p>

For Action B,

<p><em>G</em><sub>t</sub> = 1 + 0.5·4 + 0.5<sup>2</sup>·4 = 1 + 2 + 1 = 4.</p>

Now the ranking reverses.

What does that teach?

It shows that the objective depends on the return definition, and the return definition encodes how future consequences are weighted. The invariant lesson is that RL evaluates policies through multi-step consequences, not only through the next reward.

### Misconception block

**Reward is not return.**  
Reward is one immediate signal. Return is an aggregate of future rewards.

**A policy is not judged by isolated moves.**  
It is judged by the trajectories it tends to generate under the environment law.

### Connection to later material

Value functions will soon be defined as expected return conditioned on information at the decision point. Bellman equations will express recursive structure in those expectations. None of that makes sense unless the chapter has already fixed what return is aggregating and why it begins with <em>R</em><sub>t+1</sub>.

### Retain / Do not confuse

Retain:

- RL optimizes a policy through expected return.
- Return starts at <em>R</em><sub>t+1</sub> because that is the first reward after the decision at time <em>t</em>.
- Immediate reward and long-run desirability can differ.

Do not confuse:

- reward with return,
- greedy one-step improvement with optimal long-run control.

---

## 8. Episodic tasks, continuing tasks, and terminal index limits

### Why this section exists

Once return is mentioned, the chapter must also clarify what happens when interaction ends or does not end. This section exists because index boundaries matter. If the final decision time and final reward index are not handled carefully, later recursions involving terminal states become confusing.

### The object being introduced

The key distinction is between **episodic** and **continuing** tasks.

In an episodic task, interaction begins from an initial condition and terminates after a finite number of within-episode decisions. In a continuing task, there is no natural terminal point; the interaction goes on indefinitely.

### Formal definitions

An **episodic task** is one in which interaction is divided into episodes that terminate.

A **continuing task** is one in which interaction does not naturally terminate.

If an episode’s final action is chosen at time <em>T</em> - 1, then:

- the last chosen action is <em>A</em><sub>T-1</sub>,
- the final immediate reward tied to that action is <em>R</em><sub>T</sub>,
- there is no within-episode action <em>A</em><sub>T</sub>.

### Interpretation

The index <em>T</em> does not label a final action in that description. It labels the reward that arrives **after** the final action <em>A</em><sub>T-1</sub>. This is the same timing discipline as before, applied at the boundary.

The main thing to notice is that termination removes future continuation from that episode. So later recursions often treat terminal continuation terms as zero or absent, not because something mysterious happened, but because there is no further within-episode decision beyond that boundary.

### Boundary conditions, assumptions, and failure modes

A common mistake is to assume that if the final reward is <em>R</em><sub>T</sub>, then there must also be an action <em>A</em><sub>T</sub> inside the same episode. Not so. The final reward is the consequence of <em>A</em><sub>T-1</sub>.

Another mistake is to think the event order changes in continuing tasks. It does not. The same pre-action and post-action distinction remains. The only difference is whether a terminal boundary exists.

### Fully worked example

Suppose an episode lasts exactly three decisions, at times 0, 1, 2. Then the final action index is

<p><em>T</em> - 1 = 2,</p>

so

<p><em>T</em> = 3.</p>

The sequence is:

- At time 0, choose <em>A</em><sub>0</sub>, then observe <em>R</em><sub>1</sub> and <em>O</em><sub>1</sub>.
- At time 1, choose <em>A</em><sub>1</sub>, then observe <em>R</em><sub>2</sub> and <em>O</em><sub>2</sub>.
- At time 2, choose <em>A</em><sub>2</sub>, then observe <em>R</em><sub>3</sub> and termination.

Now check the boundary carefully.

- <em>A</em><sub>2</sub> is the last action.
- <em>R</em><sub>3</sub> is the last reward caused by that action.
- There is no next within-episode action <em>A</em><sub>3</sub>.

What conclusion does this allow?

It fixes the exact endpoint of the return:

<p><em>G</em><sub>2</sub> = <em>R</em><sub>3</sub>.</p>

There is no further term because the episode has ended.

The general lesson is that terminal indexing is not special new notation. It is simply the same action-then-consequence order carried all the way to the end of an episode.

### Misconception block

**Do not think termination breaks the indexing scheme.**  
It confirms it. The final reward still arrives after the final action.

### Connection to later material

Terminal conditions matter in dynamic programming, Monte Carlo estimation, bootstrapping, and Bellman recursions. Clear endpoint indexing prevents later confusion about why terminal continuation terms disappear.

### Retain / Do not confuse

Retain:

- Episodic tasks terminate; continuing tasks do not.
- If the last action is <em>A</em><sub>T-1</sub>, the final reward is <em>R</em><sub>T</sub>.
- There is no within-episode <em>A</em><sub>T</sub> after termination.

Do not confuse:

- final reward index with final action index,
- episodic termination with a change in causal order.

---

## 9. What has not been assumed yet

### Why this section exists

A chapter can be misunderstood not only by what it says, but by what readers mistakenly think it has already granted. This section exists to mark the limits of the current setup. Those limits matter because later chapters will add strong structure, and that added structure should be recognized as a real assumption rather than something that was present all along.

### The object being introduced

The object here is not a new mathematical variable but a set of **scope boundaries**. These boundaries tell us which simplifications are not yet licensed.

### Formal statements

At this stage, the chapter has **not** assumed:

1. the Markov property,
2. that the current observation is sufficient,
3. that a special state variable has already been justified,
4. finite state or action spaces,
5. value functions,
6. Bellman equations.

### Interpretation

These omissions are not weaknesses. They are deliberate discipline. The chapter is constructing the most general interaction frame first. Later chapters will become more powerful precisely because they will add new assumptions on top of something already clear.

### Boundary conditions and failure modes

The main failure mode is premature compression. If a learner starts writing <em>P</em>(<em>s</em>′, <em>r</em> | <em>s</em>, <em>a</em>) before showing where <em>s</em> came from and why it is sufficient, they are skipping the most important logical bridge in the subject.

Another failure mode is to think that because many introductory examples use small finite MDPs, the general theory starts there. It does not. The interaction process comes first; finite MDP structure is a later special case.

### Misconception block

**A summary does not become Markov because we name it “state.”**  
The Markov property is not a naming convention. It is a conditional-independence-style sufficiency claim that must be justified.

### Connection to later material

This section tells you what the next chapters will actually contribute. When a state representation and Markov transition law appear later, you will know that something substantive has been added, not merely re-labeled.

### Retain / Do not confuse

Retain:

- No Markov assumption yet.
- No privileged state variable yet.
- No Bellman machinery yet.

Do not confuse:

- early notation convenience with proven structural sufficiency.

---

## 10. Final synthesis: what this chapter now licenses

The chapter has done a specific job. It has fixed the timing of interaction, identified the primitive variables, defined history before state, separated policy input from observation and history, and written the correct pre-Markov one-step environment law.

As a result, you are now entitled to make the following claims precisely.

At decision time <em>t</em>, the agent acts **before** the next reward is observed. The reward tied to <em>A</em><sub>t</sub> is therefore correctly written <em>R</em><sub>t+1</sub>. The most complete available record before choosing <em>A</em><sub>t</sub> is the history

<p><em>H</em><sub>t</sub> = (<em>O</em><sub>0</sub>, <em>A</em><sub>0</sub>, <em>R</em><sub>1</sub>, <em>O</em><sub>1</sub>, <em>A</em><sub>1</sub>, <em>R</em><sub>2</sub>, ..., <em>O</em><sub>t</sub>).</p>

A policy need not use the full history; it may condition on some allowed information summary <em>X</em><sub>t</sub>. Before any Markov assumption, the correct one-step environment law is

<p><em>P</em>(<em>O</em><sub>t+1</sub>, <em>R</em><sub>t+1</sub> | <em>H</em><sub>t</sub>, <em>A</em><sub>t</sub>).</p>

And reinforcement learning is not merely responding to immediate scalar feedback. It is choosing a policy whose repeated interaction with the environment leads to better long-run return.

That is the platform on which later chapters will stand. When the subject later introduces states, returns, value functions, and Bellman recursions, those objects will no longer feel like isolated formulas. They will read as consequences of an interaction process whose timing and information structure are already under control.

---

## Mastery check

You should be able to answer each of the following in complete sentences, not by slogan.

1. What exactly is available at the decision point indexed by <em>t</em>, and what is not yet available?
2. Why is the reward caused by <em>A</em><sub>t</sub> written <em>R</em><sub>t+1</sub> rather than <em>R</em><sub>t</sub>?
3. What is the difference between the current observation <em>O</em><sub>t</sub>, the full history <em>H</em><sub>t</sub>, and the policy input <em>X</em><sub>t</sub>?
4. Why is  
   <p><em>P</em>(<em>O</em><sub>t+1</sub>, <em>R</em><sub>t+1</sub> | <em>H</em><sub>t</sub>, <em>A</em><sub>t</sub>)</p>
   the correct pre-Markov one-step law?
5. In what sense is a state representation a summary of history, and why is naming a summary “state” not enough to make it Markov?
6. Why is reinforcement learning said to optimize a policy rather than the next reward in isolation?
7. If an episode’s final action is <em>A</em><sub>T-1</sub>, why is the final immediate reward <em>R</em><sub>T</sub>, and why is there no within-episode action <em>A</em><sub>T</sub>?

If any of those answers still feels vague, the right move is not to rush onward. It is to return to the causal order of the interaction process and rebuild the chapter from there. That order is the spine of the subject.
