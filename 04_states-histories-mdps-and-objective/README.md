# Chapter 4 — States, Histories, MDPs, and the Objective

*Rewritten as mastery-oriented teaching notes from the source chapter, following the uploaded writing standard.*

## What this chapter is for

The previous chapter built the probabilistic language needed to speak precisely about return, conditional expectation, and trajectory-level objectives. But that language alone does not yet explain why reinforcement learning can often be written in such compact recursive form. A return random variable can always be defined. An expectation of return can always be written. What still remains unclear is why those expectations can often be indexed by a *state* rather than by the entire past.

That gap is the reason this chapter must exist. Reinforcement learning literature often moves very quickly from interaction to states, from states to MDPs, and from MDPs to Bellman equations, as if each step were automatic. It is not automatic. There is a conceptual chain that must be respected.

First there is the actual interaction process between agent and environment. From that process there is a complete record of what has happened so far. That record is the history. Then there may be a summary of that history used for decision making. Only after that summary is tested for the relevant sufficiency property does it deserve to support exact MDP-style recursion. If that order is skipped, students can repeat the symbols of dynamic programming while silently losing track of what justifies them.

The most important local warning for this chapter is the following: a representation map is not yet a sufficiency theorem. If a chapter writes something like $S_t = f(H_t)$, that statement means only that some summary has been defined from history. It does **not** yet mean that the summary preserves all the predictive information required for exact state-based recursion. The whole burden of the Markov test later in the chapter is to decide whether that stronger claim is actually true. This warning should be kept explicit because many later RL texts silently move from “we have a representation” to “we have a state” without paying that conceptual cost.

A second warning should be attached immediately to that one. Passing the Markov test does not mean “the state contains every conceivable fact about the world.” It means something narrower and more useful: for the purposes of one-step prediction and control under the chapter’s setup, conditioning on the current state and current action is as informative as conditioning on the whole history and current action. The license gained is therefore exact **state-based local recursion**, not omniscience. That is the exact amount of simplification the chapter is trying to earn.

This chapter therefore separates four things that are often blurred together:

- the full decision-relevant history,
- a representation built from that history,
- the Markov property as a conditional sufficiency statement,
- and the objective that is actually being optimized.

That separation is one of the conceptual load-bearing walls of the subject. Without it, “state” becomes an informal label for whatever the model currently sees, “MDP” becomes a default assumption rather than an earned structural simplification, and Bellman equations start to look universal even in settings where they are only approximate.

By the end of this chapter, the reader should be able to answer all of the following without vagueness. What exactly does history contain at a decision point? In what sense is a state representation merely a function of history? What does the Markov property actually compare? What changes once a representation is Markov? What does the performance objective optimize? And why does Bellman structure depend not just on having a summary, but on having the *right kind* of summary?

---

## 1. History comes first

### Why this section exists

Before the chapter can discuss state, it has to make precise what state is supposed to summarize. The subject cannot responsibly ask whether a representation is sufficient if it never names the full information record relative to which sufficiency is judged. This is the first gap that must be repaired. Many confusions about state arise because the full past is treated as background rather than as an explicit mathematical object.

### The object being introduced

The object here is the **history** at decision time $t$, usually denoted $H_t$. It is the complete decision-relevant record of interaction available *before* action $A_t$ is chosen. What is fixed is the current decision index $t$. What varies across realizations is the particular sequence of observations, actions, and rewards that has occurred up to that time. The role of $H_t$ is foundational: it is the maximal past information record available to the agent at the current decision point.

This object answers a basic question: if the agent is about to choose its next action, what information from the past is, in principle, available to condition on? The history provides that reference object. Later summaries and state representations are judged against it.

### Formal definition

A common form for the history at time $t$ is

$$
H_t = (O_0, A_0, R_1, O_1, A_1, R_2, \ldots, O_t).
$$

### Interpretation

This notation says that at decision time $t$, the agent has access to the initial observation $O_0$, all earlier chosen actions, all rewards received after those actions, and the current observation $O_t$. The action $A_t$ is **not** yet inside $H_t$ because the history is defined at the moment just before that action is chosen.

That timing matters. The history is not an arbitrary record of “everything eventually observed.” It is the information available at the decision boundary. That is why the current observation appears, but the current action does not.

The reader should also notice that the exact symbols are not the deepest point. Some sources include states instead of observations, some write histories in slightly different indexing conventions, and some bundle rewards differently. What does not vary is the structural role: history is the fullest available pre-action record.

### Boundary conditions, assumptions, and failure modes

The exact contents of the history depend on what the agent can actually observe. In fully observed settings, one may write states explicitly. In partially observed settings, the history may be built from observations rather than hidden environment states.

A common failure mode is to treat history as “whatever the model stored internally.” That is too narrow. The history is the conceptual full record available from interaction, not merely the compressed representation the model happened to keep.

Another failure mode is to define history after the current action rather than before it. That destroys the clean decision-time interpretation and makes later conditioning statements harder to read.

### Fully worked example

Suppose an agent interacts with an environment over several time steps. At time $0$, it receives observation $O_0 = \text{red light}$. It chooses action $A_0 = \text{wait}$. The environment returns reward $R_1 = 0$ and new observation $O_1 = \text{green light}$. Then the agent chooses action $A_1 = \text{go}$. The environment returns reward $R_2 = 5$ and new observation $O_2 = \text{intersection cleared}$.

What is the history at decision time $t=2$, just before action $A_2$ is chosen?

By definition,

$$
H_2 = (O_0, A_0, R_1, O_1, A_1, R_2, O_2).
$$

Now substitute the realized values:

$$
H_2 = (\text{red light}, \text{wait}, 0, \text{green light}, \text{go}, 5, \text{intersection cleared}).
$$

What has been checked here? First, the time index $t=2$ means the history must include all interaction up to the current observation $O_2$. Second, the history stops before action $A_2$ because the agent has not yet chosen it. Third, every included object is genuinely available at that decision point.

The final interpretation is that this history is the full pre-action information record. Any later state representation used at time $2$ must be a function of this history, not of some future information and not of some invented object detached from the interaction record.

The general lesson is that history is the reference object against which compression, representation, and sufficiency are judged. In future problems, always ask: what is the full information record available at the moment the next action must be selected?

### Misconception block

**Do not confuse history with the current observation.** The current observation is one component of history, often the last one. History is the whole pre-decision interaction record up to that point.

### Connection to later material

Later sections will define state as a function of history and then ask whether that function preserves the information needed for one-step prediction and control. None of that can be stated precisely unless history is first made explicit.

### Retain / Do not confuse

Retain that history is the full available record at the current decision point. Do not confuse it with a single observation, with the agent’s internal memory, or with a post-action record.

---

## 2. A state representation is a function of history

### Why this section exists

Once the full information record has been named, the next question is how reinforcement learning reduces that record to something more manageable. The full history grows with time and is often too large or too awkward to use directly. The chapter therefore needs a general language for summaries built from history before it can ask whether such summaries are sufficient.

### The object being introduced

The object here is a **state representation** $S_t$. At this stage, the chapter is not yet claiming that the representation is Markov, sufficient, minimal, or exact. It is introducing only the idea of a summary derived from the available past.

What is fixed is the current time index $t$ and the mapping from histories to representation values. What varies is the realized history $H_t$, and therefore the realized representation value $S_t$. The question this object answers is: what summary of the past will the agent condition on when making decisions or predictions?

### Formal definition

A state representation is some mapping

$$
S_t = f(H_t).
$$

### Adversarial misconception block: representation map is not a certificate of sufficiency

A dangerous but plausible move is to say: "because \(S_t=f(H_t)\), I have now defined the state." What you have certainly defined is a **representation**. What you have **not** yet obtained for free is the stronger predictive claim needed for MDP reasoning. The map \(f\) tells you how histories are collapsed. It does not tell you whether the collapse preserves the conditional law needed for one-step prediction and control.

The hostile test is to imagine two distinct histories \(h_t\) and \(\tilde h_t\) that produce the same summary value \(s\). If those two histories induce different conditional laws for the next reward or next summary under the same action, then the representation is a summary but not a Markov state for the purposes of the later theory. So the chapter's order matters: first define the map, then test the property. Never reverse those two steps in your reasoning.

### Interpretation

This equation is simple, but it does important conceptual work. It says that a state representation is not an independent primitive floating outside the interaction process. It is derived from history. The map $f$ may preserve a great deal of information or discard much of it. It may be hand-designed or learned. It may be exact, approximate, interpretable, opaque, low-dimensional, high-dimensional, deterministic, or stochastic after enrichment of notation. None of those adjectives yet answers the central sufficiency question.

At this point, all the equation means is that the agent uses a summary of the past rather than the full past itself. That is the only claim currently licensed.

### Boundary conditions, assumptions, and failure modes

The map $f$ may be identity, in which case $S_t$ is effectively the full history itself. It may also be highly compressive, such as keeping only the current observation, a finite window of past observations, a learned hidden vector, or domain-specific features.

A common failure mode is to treat the word “state” as already meaning “good enough for dynamic programming.” At this stage, it does not. It means only “some function of history used as a summary.”

Another failure mode is to think that lower dimension or practical usefulness automatically implies sufficiency. It does not. Compression is a design choice. Sufficiency is a conditional-law property that must still be checked.

### Fully worked example

Suppose an agent plays a simple game in which the full history at time $t$ is

$$
H_t = (O_0, A_0, R_1, O_1, \ldots, O_t).
$$

Now imagine three candidate state representations.

1. **Full-history representation:**
   $$
   S_t^{(1)} = H_t.
   $$
   This keeps everything.

2. **Current-observation representation:**
   $$
   S_t^{(2)} = O_t.
   $$
   This keeps only the current observation and discards the rest.

3. **Feature summary representation:**
   $$
   S_t^{(3)} = (O_t, \text{running reward total up to time } t).
   $$
   This keeps the current observation plus one aggregate quantity from the past.

What do these examples show? First, each is a valid state representation because each is a function of history. Second, they differ in how much information they retain. Third, at this point none has earned the title “Markov” merely by being named.

The reasoning check here is structural, not yet probabilistic. We are checking only whether the proposed representation is built from information available in the history. Each one is. That makes each a legitimate candidate summary.

The general lesson is that “state representation” is a broad category. Many summaries qualify. The harder question—answered later—is whether a chosen summary preserves the information that matters for next-step prediction and control.

### Misconception block

**Do not confuse “state representation” with “Markov state.”** Every Markov state is a representation, but not every representation is Markov.

### Connection to later material

The next step in the chapter is to test whether a chosen summary preserves the information needed for exact one-step dynamics. That is where the Markov property enters and where the distinction between merely using a summary and having an exact MDP becomes critical.

### Retain / Do not confuse

Retain that a state representation is any summary derived from history. Do not confuse this with a proof of sufficiency, with a claim of optimality, or with the Markov property.

---

## 3. Summary is not the same thing as sufficiency

### Why this section exists

The previous section introduced state representation in the broadest sense. That broadness is useful, but also dangerous. Many learners start referring to any convenient summary as “the state,” and then silently inherit conclusions that only hold for Markov states. This section exists to block that shortcut before it becomes habitual.

### The object being introduced

The object here is a distinction rather than a new formula: the distinction between a **summary of history** and a **sufficient summary in the Markov sense**. The role of this distinction is diagnostic. It prevents us from granting exact recursive structure too early.

What is fixed is a chosen summary map $f$. What varies is whether that map actually preserves the predictive information needed for the next step. The question it answers is: when does a summary merely compress the past, and when does it compress the past without losing what matters for one-step prediction and control?

### Formal definition

At this stage the formal point is purely classificatory:

- **Summary:** any function of history, $S_t=f(H_t)$.
- **Markov state:** a summary that passes the Markov conditional sufficiency test introduced later.

### Interpretation

This distinction says that naming a representation does not prove what the representation can support. A compact embedding, a feature vector, a recurrent hidden state, or the current observation may all be useful summaries. But usefulness and exact sufficiency are different questions.

The first thing to notice is that the chapter is not dismissing non-Markov summaries. A summary can be practically valuable even if it fails the exact Markov test. The point is more disciplined: the mathematics you are allowed to apply depends on what has actually been established.

### Boundary conditions, assumptions, and failure modes

The phrase “the state” is often used informally in engineering discussions for whatever representation a system uses. That informal practice is not always harmful, but it becomes harmful the moment one begins using exact MDP equations without checking whether the representation really supports them.

A common failure mode is this chain of reasoning:

1. The representation is compact and works well empirically.
2. Therefore it must be the state.
3. Therefore Bellman equations written in terms of it must be exact.

Every step after the first requires additional justification.

### Fully worked example

Imagine a card game in which the observation $O_t$ shows only the dealer’s visible card, but the future outcome also depends on the sequence of the player’s earlier hidden draws. Consider the summary

$$
S_t = O_t.
$$

This is certainly a function of history. So it is a valid summary. But does it preserve all information from the past needed to predict the next-step outcome together with the current action?

Not necessarily. Two different histories may lead to the same visible dealer card while differing in the player’s hidden total. If those two histories produce different next-step outcome laws under the same chosen action, then $S_t=O_t$ has discarded prediction-relevant information.

What has been checked here? First, that the representation qualifies as a summary because it is derived from history. Second, that this qualification alone says nothing about whether next-step laws are preserved. Third, that one must compare conditional laws, not superficial convenience, to decide whether the representation is Markov.

The general lesson is that there is a real conceptual boundary between “some compression of the past” and “a compression that preserves exactly the right conditional law.” That boundary is what the Markov property will formalize.

### Misconception block

**Do not confuse “works well” with “is exact.”** A summary can support good performance and still fail to be Markov. Practical adequacy and exact structural sufficiency are not the same claim.

### Connection to later material

Later chapters will derive recursive value equations, dynamic programming updates, and policy evaluation formulas that are exact in MDPs. This section explains why those results cannot be transferred mechanically to every learned or hand-designed representation.

### Retain / Do not confuse

Retain that summary means compression of history, while Markov state means compression that preserves the relevant one-step conditional law. Do not confuse usefulness, low dimension, or intuition with sufficiency.

---

## 4. The unrestricted one-step law

### Why this section exists

Before one can state the Markov property, one must know what the unrestricted process looks like *before* any Markov restriction is imposed. Otherwise the Markov condition sounds like a free-floating slogan rather than a comparison between two concrete conditional laws. This section exists to name the full-history one-step law that Markov sufficiency will later simplify.

### The object being introduced

The object is the full-history one-step conditional law for the next-step outcome. In the observable formulation used here, that outcome consists of the next observation and reward. What is fixed is the present history $H_t$ and current action $A_t$. What varies is the next-step pair $(O_{t+1}, R_{t+1})$ or, after a state representation is adopted, the next-state reward pair.

The question this object answers is: without assuming any state sufficiency, what information may the next-step distribution depend on?

### Formal definition

Before imposing the Markov restriction, a generic one-step law may be written as

$$
P(O_{t+1}, R_{t+1} \mid H_t, A_t).
$$

### Interpretation

This formula says that the next observation-reward outcome can, in principle, depend on the entire available history and the current action. It makes no claim that only the current observation is enough, and no claim that some compressed state representation is enough. It is the most honest one-step description available before sufficiency is established.

The reader should notice what is fixed and what is varying. The conditioning side keeps the full past and the current action fixed. The random object on the left is the next-step outcome. This is the correct baseline from which simplifications must be earned.

### Boundary conditions, assumptions, and failure modes

This law may describe a partially observed process, a non-Markov observable process, or a process for which the full underlying environment state is hidden from the agent. It is intentionally general.

A common failure mode is to start with $P(s',r\mid s,a)$ as if that were automatically the right law. That notation already assumes a state representation and already assumes the relevant Markov locality. This section reminds the reader that such notation is a later achievement, not the starting point.

### Fully worked example

Suppose an agent observes traffic signals, but the hidden environment also depends on how long the signal has already been in its current phase. Two histories may have the same current visible light, say green, but differ in how recently that green phase began.

At time $t$, consider two concrete histories. In history $h$, the light has been green for a long time. In history $\tilde h$, the light has only just turned green. The current visible observation is therefore the same in both cases, but the hidden phase age differs. Now fix the current action at $a=\text{go cautiously}$. Because the latent phase age affects what is likely to happen next, the next-step law can still differ across these two histories even though the current observation matches. This is exactly the kind of case in which a compact present observation fails to license Markov reasoning.

So even if the current observation is the same in both cases, one may have

$$
P(O_{t+1},R_{t+1}\mid H_t=h, A_t=a) \neq P(O_{t+1},R_{t+1}\mid H_t=\tilde h, A_t=a).
$$

What was checked? First, the next-step law was conditioned on the *full* history and action. Second, two different histories with the same apparent current observation were compared. Third, the example showed that earlier past information can remain relevant unless a proper sufficient summary is used.

The general lesson is that the unrestricted one-step law is allowed to depend on the full past. That is exactly why a sufficiency test is needed before moving to MDP notation.

### Misconception block

**Do not assume the next step is determined by the current observation alone.** That may be true in some problems, but it is not the default starting point.

### Connection to later material

The Markov property will now be stated as the claim that a chosen summary preserves exactly this one-step law. That comparison is the mathematical heart of the chapter.

That wording should be made even sharper. The Markov claim is not merely that the summary is convenient, compact, or useful for control. It is that once the current summary $S_t$ and action $A_t$ are fixed, the conditional distribution of the next-step outcome no longer depends on which full history produced that summary. The constrained object is therefore a **distributional law**, not a qualitative feeling that “the summary seems informative enough.” This is why the chapter must keep comparing summaries back to histories instead of treating representation quality as a purely informal matter.

### Retain / Do not confuse

Retain that the unrestricted one-step law conditions on full history and current action. Do not confuse this general law with the already-simplified MDP law $P(s',r\mid s,a)$.

---

## 5. What the Markov property actually says

### Why this section exists

Now that both history and summary have been defined, the chapter can state the decisive test. Without this test, “state” remains just a name. The chapter cannot proceed to MDP structure, state-based policies, or Bellman equations until it makes explicit what it means for a summary to preserve the right predictive information.

### The object being introduced

The object is the **Markov property** of a state representation $S_t$. Its role is not cosmetic. It determines whether conditioning on the current summary and current action is as informative for the next-step law as conditioning on the entire past and current action.

What is fixed is a candidate representation $S_t=f(H_t)$ and the current action $A_t$. What varies is the next-step outcome. The question it answers is: once the current summary and action are known, does any additional information in the earlier history still change the next-step conditional law?

### Formal definition

A state representation $S_t$ is Markov if

$$
P(S_{t+1}, R_{t+1} \mid H_t, A_t) = P(S_{t+1}, R_{t+1} \mid S_t, A_t).
$$

### What the Markov property is actually claiming

The Markov property is not the vague statement that the current state "contains all relevant information." In these notes it should be read more sharply: once \(S_t\) and \(A_t\) are fixed, the conditional law of the next relevant one-step outcome does not depend on the fuller past history. That is a statement about **conditional distributions**, not about introspective completeness or human notions of relevance.

This sharper reading matters because it blocks a common oral-exam failure. A student says the right words but cannot say what object the property constrains. The property constrains the law of the next-step variables used by the model, such as the next state and reward. It does not say that the representation is psychologically complete, physically complete, or useful for every possible future statistic. It says something narrower and more usable: it licenses a local one-step description.

### What the Markov property now licenses

Once the Markov condition holds for the chosen representation, a new compression becomes legal. Future one-step laws may be written in terms of the current state and action alone, rather than in terms of the entire history. That means the learner may define state-indexed reward and transition descriptions, state-conditioned value functions, and Bellman-style recursive equations without silently dropping information that still matters. This is the exact reason the Markov property is load-bearing. It does not merely rename the summary as a “state.” It changes what forms of reasoning are now exact.

Just as important is what it does **not** license automatically. It does not guarantee that the representation is minimal. It does not guarantee that learning with function approximation will be easy. It does not guarantee that the policy class can exploit the representation well. The license is exactness of the local probabilistic reduction, not a blanket promise of practical tractability.

### Interpretation

This equality compares two conditional laws for the same next-step random object. On the left, the conditioning keeps the full available history and the current action. On the right, the conditioning keeps only the summary value and the current action. The Markov claim says those two laws are the same.

Read this in the correct order. It does **not** say that the history has vanished from reality. It says that once the summary $S_t$ is fixed, the history contributes no further information *for predicting the next state-reward outcome given the current action*. That is a conditional sufficiency claim.

The first thing the reader should notice is what is being compared: not feature quality, not interpretability, not practical convenience, but equality of conditional laws.

### Boundary conditions, assumptions, and failure modes

The equality must be understood as holding for the relevant histories and action choices in the process under study. In measure-theoretic settings one states the condition carefully with respect to almost-sure equivalence, but the conceptual content remains the same.

A common failure mode is to misread the Markov property as saying the future is independent of the past. That is not the right statement. The correct statement is that the future is independent of the earlier past *conditional on the current Markov state and action*.

Another failure mode is to think that one-step sufficiency is trivial because a representation predicts the immediate next reward well on average. The formal claim is stricter: it concerns the full conditional law, not a single prediction score.

### Fully worked example

Suppose an environment keeps track of whether a machine is overheating, but the observation only shows a warning light that can be yellow or red. Let the history contain past sensor patterns. Consider two histories $h$ and $\tilde h$ that both lead to the same summary value $S_t = \text{yellow}$.

Now fix action $a = \text{continue operating}$. Assume that under history $h$, the hidden overheating process has been worsening, while under $\tilde h$ it has been stable. Then the next-step outcome law may differ:

$$
P(S_{t+1}, R_{t+1} \mid H_t=h, A_t=a) \neq P(S_{t+1}, R_{t+1} \mid H_t=\tilde h, A_t=a).
$$

Because both histories share the same summary value $S_t=\text{yellow}$ and the same action $a$, but induce different next-step laws, the summary “current warning color only” is **not** Markov.

Now imagine a richer representation that includes both current warning color and recent temperature trend. Suppose that for any two histories mapping to the same richer representation, the next-step law under each fixed action matches. Then this richer representation *is* Markov.

What was checked at each step? First, identify two histories that map to the same summary value. Second, fix the current action so that action is not the source of difference. Third, compare the conditional law of the next-step outcome. If the laws differ, the summary has discarded prediction-relevant information. If they match for all such cases, the summary passes the sufficiency test.

The general lesson is that the Markov property is about whether the summary preserves the right conditional law, not about whether the summary looks sensible.

### Misconception block

**Do not confuse “future depends only on the state” with “the past no longer matters.”** The past matters because it helped produce the state. The Markov claim is that the past has been compressed into the current state in a way that is sufficient for the next-step law.

### Connection to later material

Everything that follows in standard MDP theory rests on this property. State-based transition laws, value functions indexed by state, Bellman equations, dynamic programming, and many policy optimization formulas depend on the idea that the current state-action pair contains the relevant local predictive information.

### Retain / Do not confuse

Retain that the Markov property is equality of full-history and state-based next-step conditional laws. Do not confuse it with convenience, intuition, or unconditional independence from the past.

---

## 6. The decisive test: summary versus Markov state

### Why this section exists

The previous section stated the Markov condition abstractly. This section exists to make the testing logic operational. Students often understand the formula symbolically but still struggle to see what one would actually compare in practice. The chapter therefore now turns the formal definition into a concrete decision boundary.

### The object being introduced

The object here is the testing pattern for deciding whether a summary is Markov. The role of the test is to identify whether the summary has merged histories that should not have been merged.

What is fixed is a summary value $s$ and an action $a$. What varies are the different histories that map to the same summary value. The question this object answers is: if two histories look identical through the lens of the chosen summary, do they still imply the same next-step law under each fixed action?

### Formal definition

Suppose two histories $h$ and $\tilde h$ satisfy

$$
f(h)=f(\tilde h)=s.
$$

Then the summary is not Markov if for some action $a$,

$$
P(S_{t+1},R_{t+1}\mid H_t=h, A_t=a)
\neq
P(S_{t+1},R_{t+1}\mid H_t=\tilde h, A_t=a).
$$

Conversely, if for every action $a$, any two histories mapping to the same $s$ induce the same next-step conditional law, then the summary is Markov.

### Interpretation

This is the most concrete way to understand the Markov condition. A summary groups many histories into the same representation value. The question is whether those grouped histories are genuinely equivalent for one-step prediction and control. If the answer is yes, the grouping is safe. If the answer is no, the summary has thrown away information that still matters.

The first thing to notice is that the problem is not that compression occurred. Compression is expected. The problem is *bad compression*: histories that should remain distinguishable for next-step dynamics have been merged into one summary value.

### Boundary conditions, assumptions, and failure modes

The comparison must be action-specific. A summary might appear adequate under one action but fail under another. The Markov test concerns the next-step law conditioned on both summary and current action.

Another failure mode is to test only expected reward and ignore the rest of the next-step law. A representation may preserve mean reward while still changing the distribution of next states or the broader reward distribution.

### Fully worked example

Consider a simple navigation task in which the current observation shows only the agent’s position in a hallway, but not whether the floor is slippery. The true future dynamics depend on both position and slipperiness, and slipperiness depends on earlier weather events stored in history.

Let two histories $h$ and $\tilde h$ both lead to the same visible position, so the summary is

$$
S_t = \text{current visible position} = s.
$$

Suppose the chosen action is $a = \text{move right}$.

- Under history $h$, the floor is dry, so moving right succeeds with probability $0.9$ and slips back with probability $0.1$.
- Under history $\tilde h$, the floor is wet, so moving right succeeds with probability $0.4$ and slips back with probability $0.6$.

Then the next-step laws differ even though $f(h)=f(\tilde h)=s$ and the action is the same. Therefore the visible-position summary is not Markov.

Now imagine a richer summary that includes both position and a slipperiness indicator inferred from recent observations. If every pair of histories mapping to the same richer summary induces identical next-step laws under each action, then that richer representation is Markov.

What was checked? First, histories were grouped by the chosen summary. Second, one action was held fixed. Third, the next-step distribution was compared across histories inside that group. The differing laws exposed missing information in the summary.

The general lesson is that the Markov question is always: among histories collapsed to the same summary value, did we accidentally merge cases with different controlled next-step dynamics?

### Misconception block

**Do not say “the summary is almost Markov, so the test is passed.”** The exact Markov question has an exact answer. “Almost Markov” can be useful in practice, but it means approximation, not exact sufficiency.

### Connection to later material

This test is the conceptual hinge for deciding whether later MDP-based equations are exact or approximate. Once that distinction is ignored, it becomes very easy to misuse Bellman updates outside the regime that justifies them.

### Retain / Do not confuse

Retain that a summary is Markov when histories that map to the same summary value are genuinely equivalent for next-step controlled dynamics. Do not confuse compression with safe compression.

---

## 7. From Markov state to MDP

### Why this section exists

Once a representation passes the Markov test, the chapter can finally introduce the local description that makes MDP theory possible. This section exists because the move from “history-based process” to “state-action local process” is one of the major structural simplifications in reinforcement learning, and the reader should see exactly what has been earned.

### The object being introduced

The object is a **Markov decision process** described in terms of state, action, one-step transition-reward law, and initial distribution. Its role is to provide a local model of controlled dynamics once a state representation has been shown sufficient.

What is fixed is the state space, action space, initial distribution, and one-step law. What varies over time are the realized states, actions, rewards, and state transitions. The question this object answers is: once the state is Markov, how can the process be described without continually referring back to the entire history?

### Formal definition

In the finite-state, finite-action presentation, an MDP is specified by four ingredients taken together. First, there is a state space $\mathcal S$, the set of possible Markov states in which the process may currently stand. Second, there is an action space $\mathcal A$, the set of actions that may be chosen. Third, there is a one-step transition-reward law
$$
P(s',r\mid s,a),
$$
which tells us the conditional distribution of the next state and reward once the current state and action have been fixed. Fourth, there is an initial-state distribution, which determines how the process starts before any action has been chosen.

### Interpretation

This description says that once the current state $s$ and action $a$ are fixed, the next state $s'$ and reward $r$ are governed by a local one-step law that no longer needs the rest of the past as explicit input. That is the essential economy of the MDP representation.

The reader should notice what has changed from the unrestricted one-step law. Previously, the next-step outcome could depend on the whole history. Now, because the state has been shown Markov, the whole relevant influence of the past has been compressed into the current state.

This does not mean the past was unimportant. It means the past has already done its work by producing the current sufficient state.

### Boundary conditions, assumptions, and failure modes

This local MDP description is exact only if the state representation used is truly Markov. If the summary is non-Markov, then writing $P(s',r\mid s,a)$ may still be a useful approximation, but it is no longer an exact description of the original process.

A common failure mode is to present MDPs as the conceptual starting point of RL. They are not the starting point in the logic of this chapter. Interaction and history come first. The MDP arises only after the correct state representation has been justified.

### Fully worked example

Suppose a robot operates in a warehouse. The full history includes past sensor readings and actions. Engineers propose the state representation

$$
S_t = (\text{current location}, \text{battery level}, \text{cargo status}).
$$

After analysis, they determine that once this state and the chosen action are fixed, the next state-reward law does not depend on any earlier history. The representation is therefore Markov.

Once the representation has been justified as Markov, a local MDP description becomes available. The state space $\mathcal S$ is the set of all location-battery-cargo triples. The action space $\mathcal A$ contains whatever decisions are available at those states, such as move, pick up, drop off, or recharge. The one-step law $P(s',r\mid s,a)$ then describes, for each present triple and chosen action, how likely the robot is to land in each next triple and receive each reward. The initial-state distribution completes the specification by describing where and with what battery and cargo status the robot begins. The conceptual gain is that full-history dynamics have been replaced by local state-action dynamics without losing predictive correctness.

The general lesson is that the MDP is a compact local description earned by Markov sufficiency, not a license to forget that the process originally unfolded over histories.

### Misconception block

**Do not say “the past disappears in an MDP.”** The past is not erased. It is compressed into the current state in a way that preserves the relevant one-step controlled law.

### Connection to later material

Once the process is represented as an MDP, state-based value functions, Bellman equations, dynamic programming, policy evaluation, and control algorithms become exact descriptions under the model assumptions.

### Retain / Do not confuse

Retain that an MDP is a local controlled process description available after a Markov state representation has been established. Do not confuse this with the claim that any summary automatically induces an exact MDP.

---

## 8. Why state-based policy notation becomes legitimate

### Why this section exists

Now that a Markov state has been established and the process can be described as an MDP, the chapter can revisit policy notation. Earlier, before state sufficiency was justified, a policy had to be treated as depending on whatever input representation the agent actually used. This section exists to explain why the familiar notation $\pi(a\mid s)$ becomes conceptually justified only after the state representation has earned its role.

### The object being introduced

The object is a **state-based policy**. Its role is to describe how actions are chosen given the current Markov state rather than the full history. What is fixed is the current state value $s$. What varies is the action $a$. The question it answers is: once the current state is known, how does the agent randomize or choose among actions?

### Formal definition

Once $S_t$ is accepted as a Markov state, a policy may be written as

$$
\pi(a\mid s)=P(A_t=a\mid S_t=s).
$$

### Interpretation

This notation says that the agent’s action-selection rule can be indexed by the current state summary rather than by the entire history. The mathematical content is that the policy conditions only on the state value available at the current decision point.

The important logical order is this:

1. define the history,
2. define a summary of history,
3. test whether the summary is Markov,
4. then treat state-based conditioning as the correct local language.

It is not that one is forbidden to write $\pi(a\mid s)$ earlier as shorthand. The point is conceptual honesty. Before the state representation is justified, the notation may hide an unproved sufficiency assumption.

### Boundary conditions, assumptions, and failure modes

If the representation used by the agent is not Markov, then a state-based policy may still be the actual controller employed by the agent, but the exact structural guarantees of MDP analysis may fail for the original process.

A common failure mode is to think that the definition of a policy as $\pi(a\mid s)$ itself proves the process is Markov. It does not. Policy notation is about how the agent chooses actions. Markov sufficiency is about whether the state-action pair determines the next-step law.

### Fully worked example

Suppose a thermostat controller uses the current state representation

$$
S_t = (\text{room temperature}, \text{heater status}).
$$

If this representation has been shown Markov for the control problem, then the policy may be written as

$$
\pi(\text{turn heater on}\mid s), \qquad \pi(\text{turn heater off}\mid s).
$$

What does this mean concretely? Fix a specific state value, say

$$
s = (18^\circ\text{C}, \text{off}).
$$

Then $\pi(\text{turn heater on}\mid s)$ is the probability that the policy selects “turn heater on” when the current Markov state is exactly this temperature-status pair.

What has been checked? First, the object being conditioned on is the current state, not the full history. Second, the policy describes a distribution over actions at that fixed state. Third, the notation is legitimate because the representation has already been granted state status in the Markov sense.

The general lesson is that state-based policies are not just notation convenience. They rely on a justified state representation.

### Misconception block

**Do not confuse “the agent uses a state vector” with “the environment is exactly modeled as an MDP from that vector.”** The former is an architectural choice. The latter is a structural claim requiring justification.

### Connection to later material

State-based policy notation will be used throughout policy evaluation, control, and policy gradient methods. This section explains why that notation carries more than cosmetic meaning in the MDP setting.

### Retain / Do not confuse

Retain that $\pi(a\mid s)$ becomes fully justified after the state summary has passed the Markov test. Do not confuse policy notation with proof of Markov sufficiency.

---

## 9. Return and the performance objective

### Why this section exists

The chapter has now established the structural setting in which decision making is described. The next question is what the agent is trying to optimize. Without a clear objective, the rest of reinforcement learning would be a collection of transition models and value formulas with no declared purpose. This section exists to reconnect state and MDP structure to the long-run optimization target.

### The object being introduced

The objects here are the return random variable and the performance objective. The return summarizes future reward from a decision point onward. The objective evaluates a policy by the expected return it induces under the environment dynamics and initial distribution.

What is fixed is the policy and the induced trajectory law when the objective is evaluated. What varies are the realized trajectories and therefore the realized returns. The question this object answers is: what quantity does reinforcement learning actually try to make large?

### Formal definition

In the continuing discounted setting,

$$
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1},
$$

under the standard assumptions of bounded rewards and $0\le \gamma < 1$.

A standard performance objective is

$$
J(\pi)=\mathbb E_\pi[G_0].
$$

### Interpretation

The return $G_t$ is the discounted cumulative future reward from time $t$ onward. The objective $J(\pi)$ is the expected value of that return when the system starts from the relevant initial distribution and then evolves under policy $\pi$ and the environment.

The reader should notice what this objective is *not*. It is not “maximize the immediate next reward,” except in degenerate special cases such as $\gamma=0$. The objective judges policies by the long-run consequences of the trajectories they generate.

That is the conceptual reason reinforcement learning may rationally choose an action with poor immediate payoff if that action improves downstream outcomes enough.

### Boundary conditions, assumptions, and failure modes

The discounted infinite-horizon definition assumes the same standing conditions as in the previous chapter: bounded rewards and discount factor strictly below $1$ in continuing tasks.

A common failure mode is to interpret the objective as if the agent greedily maximizes $R_{t+1}$ at each step. That is generally false. The objective concerns expected return, not merely immediate reward.

Another failure mode is to forget the distribution under which the expectation is taken. The expectation is under the trajectory law induced jointly by the policy and environment, starting from the initial distribution.

### Fully worked example

Suppose an agent has two possible policies in a small environment.

- Policy $\pi_1$ chooses a risky action that yields immediate reward $5$ but usually leads to poor future states.
- Policy $\pi_2$ chooses a cautious action that yields immediate reward $1$ but usually leads to high-reward future states.

Assume the discounted expected returns are

$$
J(\pi_1)=\mathbb E_{\pi_1}[G_0]=6,
$$
$$
J(\pi_2)=\mathbb E_{\pi_2}[G_0]=12.
$$

What conclusion does the objective license? Even though $\pi_1$ gets the better immediate reward at the first step, the objective prefers $\pi_2$ because its expected long-run discounted return is larger.

What was checked? First, each policy was evaluated by expected return, not by first-step reward. Second, the comparison was made at the policy level. Third, the larger objective value determined the preferred policy.

The general lesson is that reinforcement learning optimizes long-run consequences as encoded by return. Immediate reward matters only as one term inside that larger quantity.

### Misconception block

**Do not confuse “reward signal” with “objective function.”** The reward at one time step is a local signal. The objective is a function of the whole return distribution induced by the policy.

### Connection to later material

Value functions, Bellman equations, and policy optimization methods are all devices for evaluating or improving this objective. If the objective is misunderstood, the purpose of those later constructions is also misunderstood.

### Retain / Do not confuse

Retain that RL typically optimizes expected return, not immediate reward alone. Do not confuse the per-step reward with the policy-level performance criterion.

---

## 10. State value and action value as conditional expectations

### Why this section exists

The chapter has introduced the objective globally at the policy level. The next step is to localize that objective around particular current situations. This section exists because reinforcement learning needs quantities that answer questions such as: how good is it to be in this state, and how good is it to take this action in this state? Those questions are answered by conditional expectations of return.

### The object being introduced

The objects are the **state-value function** and the **action-value function** for a policy $\pi$. Their role is to evaluate long-run expected return under specific current information.

What is fixed in $V^\pi(s)$ is the current state value $s$ and the policy $\pi$. What varies are the future trajectories that can unfold from that state under the policy. In $Q^\pi(s,a)$, both the current state $s$ and current action $a$ are fixed, while the subsequent future under policy $\pi$ varies.

These objects answer two different questions:

- If I am currently in state $s$ and follow policy $\pi$, what return should I expect?
- If I am currently in state $s$, force action $a$ now, and then follow policy $\pi$, what return should I expect?

### Formal definition

The state-value function is

$$
V^\pi(s)=\mathbb E_\pi[G_t\mid S_t=s].
$$

The action-value function is

$$
Q^\pi(s,a)=\mathbb E_\pi[G_t\mid S_t=s, A_t=a].
$$

### Interpretation

These are conditional expectations of the same return random variable, but under different conditioning information. The value function $V^\pi(s)$ averages over futures starting from state $s$ when actions are drawn according to policy $\pi$. The function $Q^\pi(s,a)$ conditions one level more specifically by fixing the current action as well.

The key thing to notice first is that value functions are not mystical objects. They are conditional expectations. Their meaning comes directly from the probabilistic machinery built in the previous chapter.

### Boundary conditions, assumptions, and failure modes

These quantities are most naturally interpreted in the MDP setting, where conditioning on current state and action gives the right local predictive structure. If the chosen representation is not Markov, then state-based value functions may still be defined formally, but the familiar exact recursive equations may fail for the underlying process.

A common failure mode is to forget what remains fixed after conditioning. In $V^\pi(s)$, the state is fixed, but the current action is not fixed; it is sampled according to the policy. In $Q^\pi(s,a)$, both state and current action are fixed.

### Fully worked example

Suppose a robot is in state $s=\text{charging station}$ under policy $\pi$. From this state, the policy chooses action “wait” with probability $0.7$ and “leave station” with probability $0.3$.

Assume

$$
Q^\pi(s,\text{wait}) = 10,
$$
$$
Q^\pi(s,\text{leave station}) = 4.
$$

Then what is $V^\pi(s)$?

Because $V^\pi(s)$ averages over the policy’s action choices at state $s$,

$$
V^\pi(s) = \sum_a \pi(a\mid s)Q^\pi(s,a).
$$

So here,

$$
V^\pi(s)=0.7(10)+0.3(4)=7+1.2=8.2.
$$

What was checked? First, the state was fixed. Second, because state value does not fix the current action, the policy distribution over actions at that state had to be used. Third, the action-value terms were combined under those probabilities.

The final interpretation is that $8.2$ is the expected return from being at the charging station under policy $\pi$, averaging over the policy’s present action choice. The numbers $10$ and $4$ remain more specific: they are returns conditional on each particular current action.

The general lesson is that $Q^\pi$ is more fine-grained than $V^\pi$, and $V^\pi$ can often be recovered by averaging $Q^\pi$ under the policy.

### Misconception block

**Do not confuse $V^\pi(s)$ with the best possible return from state $s$.** It is the return under the specific policy $\pi$. Optimal value functions are different objects introduced only after optimization over policies.

### Connection to later material

These two functions will become central in Bellman equations, policy evaluation, improvement, temporal-difference learning, and policy gradient baselines. Understanding them now as conditional expectations prevents later formulas from seeming arbitrary.

### Retain / Do not confuse

Retain that $V^\pi(s)$ and $Q^\pi(s,a)$ are conditional expectations of return under policy $\pi$. Do not confuse policy-specific value with optimal value, and do not confuse fixing the state with fixing both state and action.

---

## 11. Why Bellman structure requires more than the return recursion

### Why this section exists

The previous chapter introduced the algebraic identity

$$
G_t = R_{t+1} + \gamma G_{t+1}.
$$

A local distinction is needed here to prevent a later category error. Any return random variable can be decomposed algebraically into an immediate reward term plus a discounted continuation return. That statement is true before any Markov assumption is made, because it is only a decomposition of a sum. What it does **not** yet give you is a Bellman equation indexed only by state. Bellman-style state recursion requires an additional step: the future distribution must depend on the past only through a state variable that is Markov in the relevant sense. So the reader should separate two claims. The first is a generic algebraic identity for returns. The second is an exact state-based expectation identity. The first does not automatically license the second.

That identity is always true whenever return is defined. But many students then slide too quickly into believing that Bellman equations are automatic. This section exists to stop that slide. Bellman equations require not just return recursion, but the right conditioning structure.

### The object being introduced

The object here is the distinction between two layers:

1. the algebraic recursion of the return random variable,
2. the state-based recursive equations for value functions.

What is fixed is the return identity itself. What varies is whether the conditioning information is sufficient to turn that identity into a closed recursion in terms of state or state-action value functions. The question it answers is: why does a Bellman equation require a Markov state, not merely a definition of return?

### Formal definition

The algebraic return recursion is

$$
G_t = R_{t+1} + \gamma G_{t+1}.
$$

A Bellman-style state-value equation under MDP assumptions takes the form

$$
V^\pi(s) = \mathbb E_\pi[R_{t+1} + \gamma V^\pi(S_{t+1}) \mid S_t=s].
$$

### Interpretation

The first equation is an identity about the return random variable. It does not say anything about sufficiency of state. It merely regroups the discounted sum.

The second equation is a conditional expectation statement expressed purely in terms of the current state and the next state under the policy. To arrive at it, one must be able to condition on the current state and know that the next-step law is governed by the state-action pair rather than hidden leftovers from the earlier history.

The first thing to notice is that the Bellman equation is not just the return recursion with prettier symbols. It is the return recursion **plus** the Markov structure that closes the recursion at the state level.

### "This does not imply" paragraph for Bellman licensing

The identity
\[
G_t = R_{t+1} + \gamma G_{t+1}
\]
does **not** by itself produce a Bellman equation. It only says how one return random variable decomposes into an immediate reward and a shifted return random variable. A Bellman equation requires an additional closure step: the continuation term must be expressible as a value of the same type under conditioning information that is sufficient for the next-step law. That closure step is exactly where the Markov property and the chosen value-function definition do real work. If you skip that logic and jump directly from algebraic recursion to Bellman form, you are using familiar notation without its license.

### Boundary conditions, assumptions, and failure modes

If the representation is non-Markov, then conditioning on the current summary may leave out information needed to characterize the next-step law exactly. In that case, a state-based Bellman equation written for the summary may be only approximate.

A common failure mode is to write down Bellman equations whenever a feature vector exists. A feature vector is not the same thing as a sufficient state.

### Fully worked example

Suppose $S_t$ is a true Markov state. Then

$$
V^\pi(s)=\mathbb E_\pi[G_t\mid S_t=s].
$$

Use the return recursion inside the expectation:

$$
V^\pi(s)=\mathbb E_\pi[R_{t+1}+\gamma G_{t+1}\mid S_t=s].
$$

Now apply linearity of expectation:

$$
V^\pi(s)=\mathbb E_\pi[R_{t+1}\mid S_t=s] + \gamma \mathbb E_\pi[G_{t+1}\mid S_t=s].
$$

At this point, to replace the second term with an expectation involving $V^\pi(S_{t+1})$, we need the future to be conditionally structured through the Markov state. Under the MDP assumptions, one may write the state-based recursive form

$$
V^\pi(s)=\mathbb E_\pi[R_{t+1}+\gamma V^\pi(S_{t+1})\mid S_t=s].
$$

What was used at each step?

- The first step used the definition of state value.
- The second step inserted the algebraic return recursion.
- The third step used linearity of expectation.
- The final step required the Markov conditioning structure that lets future return from the next time step be summarized through $S_{t+1}$.

The general lesson is that the Bellman equation is a probabilistic recursion justified by both return algebra and Markov sufficiency.

### Misconception block

**Do not confuse “return is recursive” with “state values are recursively closed.”** The first is always true. The second requires the right state structure.

### Connection to later material

This distinction is essential for dynamic programming, policy evaluation, value iteration, Q-learning, and actor-critic methods. Many algorithms inherit their validity from Bellman structure, so knowing exactly when that structure is exact matters.

### Retain / Do not confuse

Retain that Bellman equations require more than the return recursion; they require the state representation to support the relevant Markov conditioning. Do not confuse algebraic decomposition with state-based closure.

---

## 12. Partial observation and why non-Markov summaries are hard

### Why this section exists

The chapter has so far explained what happens when a summary is Markov. It now needs to explain why many realistic problems are harder: the current observation may fail to retain enough information from the past. This section exists to connect the abstract sufficiency discussion to partial observability and to show why non-Markov summaries make exact MDP reasoning break.

### The object being introduced

The object is the case where the agent conditions on a representation that is not Markov, often the current observation alone. Its role is explanatory: it shows what kind of structural difficulty appears when the available representation fails the sufficiency test.

What is fixed is the chosen summary, such as the current observation. What varies are the histories that can produce the same summary while implying different next-step laws. The question it answers is: why are partially observed problems more difficult than fully observed Markov ones?

### Formal definition

If the current observation $O_t$ alone is used as the summary,

$$
S_t = O_t,
$$

then this representation is non-Markov whenever there exist histories $h,\tilde h$ and an action $a$ such that

$$
P(O_{t+1},R_{t+1}\mid H_t=h,A_t=a)
\neq
P(O_{t+1},R_{t+1}\mid H_t=\tilde h,A_t=a)
$$

while both histories yield the same current observation.

### Interpretation

The problem is not merely “less data.” The problem is that the chosen summary does not fully preserve the information from the past that still matters for controlled prediction. So the future cannot be locally described exactly using that summary alone.

The first thing to notice is that current observation and state are not synonymous. In a fully observed Markov problem they may coincide. In partially observed problems they often do not.

### Boundary conditions, assumptions, and failure modes

A non-Markov summary can still be useful, and policies based on it can still perform well. Approximate methods may still succeed. The failure is not necessarily practical failure. The failure is that exact MDP equations no longer describe the original process when conditioned only on that summary.

A common failure mode is to call every partially observed problem an MDP over observations. That is a convenient approximation only when explicitly treated as such.

### Fully worked example

Suppose an autonomous agent sees only whether a room appears bright or dark. Unknown to the agent, brightness depends both on current light level and whether sunglasses are currently on its camera lens. The observation is just

$$
O_t \in \{\text{bright}, \text{dark}\}.
$$

Two histories may both yield $O_t=\text{dark}$:

- in one history the room is actually dark,
- in another history the room is bright but the camera lens is obscured.

Fix the action $a = \text{increase lighting}$. The next-step outcome law may differ across these two histories because the effect of increasing lighting depends on the hidden cause of darkness.

Therefore the current observation alone is not Markov. What was checked? First, different histories led to the same observation. Second, the same action was fixed. Third, the next-step law differed. That is exactly the pattern of non-Markovity.

The general lesson is that partial observation creates difficulty because the current view may fail to preserve what the past still implies about hidden conditions relevant to the future.

### Misconception block

**Do not confuse partial observability with sensor noise alone.** The deeper issue is insufficiency of the chosen representation for the controlled next-step law.

### Connection to later material

This section prepares the ground for later discussions of memory, belief states, recurrent models, and approximate state construction. Those tools exist precisely because current observation often fails to be Markov.

### Retain / Do not confuse

Retain that partial observation is hard because current observation may fail the Markov sufficiency test. Do not confuse “observation available now” with “sufficient state for exact recursion.”

---

## 13. Learned representations and approximate Markovity

### Why this section exists

Modern reinforcement learning often relies on learned latent representations rather than hand-designed state summaries. That makes it tempting to assume that once a neural representation is called a “latent state,” the theoretical state machinery automatically applies. This section exists to prevent that leap.

### The object being introduced

The object is a **learned representation** used as a candidate state summary. Its role is practical: it compresses high-dimensional history or observation streams into a vector convenient for prediction and control. The question is whether that representation is exactly Markov, approximately Markov, or neither.

What is fixed is the learned mapping from histories or observations to latent vectors. What varies are the histories that may produce the same or similar latent code. The question it answers is: what can and cannot be concluded merely from the fact that a representation was learned and works well?

### Formal definition

A learned latent representation might be written abstractly as

$$
Z_t = f_\phi(H_t)
$$

or, in architectures with limited memory, as a learned summary of an observation stream. It is exactly Markov only if it passes the same conditional sufficiency test as any other candidate state representation.

### Interpretation

The name “latent state” does not settle the mathematics. It is only a label unless the representation preserves the relevant one-step conditional law. A learned representation may be highly useful, dramatically better than raw observation, and still fail exact Markov sufficiency.

That is not a criticism of the representation. It is a statement about what level of exactness later equations should be interpreted as having.

### Boundary conditions, assumptions, and failure modes

A representation may be approximately Markov in the sense that it preserves most predictive information relevant to control, even if not all of it. Approximate Markovity is often enough for effective algorithms. But approximation should be named honestly.

A common failure mode is to move from empirical success to exact structural claims. Good control performance is evidence of usefulness, not proof of exact sufficiency.

### Fully worked example

Suppose a recurrent agent processes an observation stream from a driving simulator and produces a latent vector $Z_t$. The vector is then used for action selection and value prediction.

Empirically, the agent performs well. But does that prove $Z_t$ is Markov?

No. To establish exact Markovity, one would need to check that for any two histories producing the same latent vector and for every current action, the next-step state-reward law is identical. In practice, such exact verification is rarely available.

What can be concluded instead is narrower and more honest. If a learned representation $Z_t$ supports strong empirical control, then it has shown itself to be a useful summary for the tasks and distributions encountered during training and evaluation. That is a practical success claim. It is not yet an exact structural claim. The exact structural claim would require the same test as before: for every pair of histories mapped to the same $Z_t$, and for every current action, the induced next-step law would have to agree. If that exact equality is unavailable, then the chapter should describe the learned representation as an approximate or task-useful state summary rather than as an already-certified Markov state. The conceptual discipline remains unchanged: learning the representation changes how the summary is obtained, but it does not weaken the criterion for exact sufficiency.

### Misconception block

**Do not confuse “latent” with “sufficient.”** Hidden representations can be powerful and still fail to preserve all next-step predictive information.

### Connection to later material

This distinction matters later when MDP-based updates are applied in partially observed or approximate-state settings. It clarifies when the theory is exact and when it is serving as a modeling approximation.

### Retain / Do not confuse

Retain that learned representations are candidate states, not automatically certified Markov states. Do not confuse empirical effectiveness with proof of exact sufficiency.

---

## 14. Common confusions this chapter is designed to block

### Why this section exists

By this point the chapter has introduced history, summary, Markov sufficiency, MDP structure, policy notation, return objectives, and value functions. The topic is conceptually dense, and the same few confusions repeatedly corrupt later understanding. This section gathers them explicitly so they become harder to carry forward unnoticed.

### Confusion 1: a state is whatever the agent currently sees

Not necessarily. What the agent currently sees is an observation. A state representation is a summary used for decision making. A Markov state is a summary that satisfies the relevant conditional sufficiency property.

### Confusion 2: if a summary is compact or useful, it must be Markov

No. Compactness and practical usefulness are different properties from exact one-step sufficiency.

### Confusion 3: MDPs are the starting point of reinforcement learning

No. The interaction process and its histories come first. An MDP is a local structural description available after the right state representation has been justified.

### Confusion 4: Bellman equations follow from the return recursion alone

False. The return recursion is always true, but state-based Bellman structure requires the current representation to support the correct Markov conditioning.

### Confusion 5: the objective is immediate reward maximization

Usually false. Standard RL objectives are based on expected return, which values downstream consequences, not only the next reward.

### Retain / Do not confuse

Retain that most misuse of MDP language comes from collapsing distinctions the chapter has worked hard to keep separate. Do not confuse observation with state, compression with sufficiency, recursion of return with Bellman recursion, or local reward with policy objective.

---

## 15. What this chapter now licenses you to say

### Why this section exists

A foundational chapter should end not only with definitions, but with a clear statement of what the reader is now entitled to conclude. This section marks the transition from introductory distinction-making to stable usable understanding.

### What you can now conclude

After mastering this chapter, you may now say all of the following precisely.

First, history is the reference object from which any state representation must be built.

Second, a state representation is a function of history and may be lossy.

Third, the Markov property is a conditional sufficiency statement comparing the full-history one-step law to the state-based one-step law.

Fourth, once a representation is Markov, the process can be described locally as an MDP using a transition-reward law of the form

$$
P(s',r\mid s,a).
$$

Fifth, state-based policies and value functions become conceptually legitimate because the conditioning structure has been justified.

Sixth, Bellman equations require more than the return recursion; they require the relevant Markov state-action sufficiency.

Seventh, non-Markov summaries may still be useful, but MDP equations written in terms of them should be interpreted as approximate rather than exact descriptions of the original process.

### Connection to later material

These conclusions are the platform on which recursive value theory, dynamic programming, policy improvement, and many RL algorithms will be built. If these distinctions are secure now, later chapters can move quickly without becoming conceptually fragile.

### Retain / Do not confuse

Retain that the real achievement of this chapter is not learning the word MDP. It is learning the chain of justification that makes MDP reasoning valid.

---

## 16. Mastery check

A serious reader should be able to answer each of the following in complete sentences, making clear what is fixed, what is varying, and what conclusion the relevant definition allows.

1. Why must history be defined before state?
2. What does the equation $S_t=f(H_t)$ assert, and what does it not assert?
3. In the Markov condition, what information is retained on the left side and what information is retained on the right side?
4. How can two different histories expose that a summary is not Markov?
5. What local description becomes available once a representation is Markov?
6. Why is the algebraic return recursion not enough by itself to justify a Bellman equation?
7. What exactly does the standard objective optimize: immediate reward or long-run expected return?
8. Why can a learned representation be useful without being exactly Markov?

If any answer still feels fuzzy, that fuzziness should be repaired now, not later. This chapter is one of the places where symbolic familiarity can easily masquerade as real understanding. The whole point of the chapter is to make that masquerade harder to maintain.
