# Chapter 5 — Value Functions, Bellman Equations, and Policy Improvement

*Rewritten as mastery-oriented teaching notes from the source chapter in the linked repository, following the uploaded writing standard.*

## What this chapter is for

Earlier chapters introduced the return random variable and the probability tools needed to reason about it. That material answered a crucial but incomplete question: what is the long-run quantity we ultimately care about? The answer was the return. But that answer alone is not enough for planning or control. A return is a full-future object. It reaches all the way to the end of the episode or the indefinite future. If we try to reason directly with entire future reward streams at every decision point, the problem stays global, unwieldy, and hard to compute.

This chapter introduces the local objects that make long-run reasoning tractable. The central move is to replace a raw future-sum objective by conditional expectations of that objective. Those conditional expectations are the value functions. Once they exist, the next major discovery is that they satisfy recursive equations. Those recursive equations are the Bellman equations. This is the moment in reinforcement learning where an apparently nonlocal objective becomes a local fixed-point problem.

That conceptual shift is so important that students often absorb the symbols without absorbing the ladder of reasoning that produces them. They see $V^\pi$, $Q^\pi$, Bellman operators, and greedy improvement rules written down correctly, but they do not fully own which statements are definitions, which are algebraic identities, which require the Markov property, and which belong to approximation methods that come later. This chapter slows the ladder down on purpose.

Before the formal sections begin, freeze a four-level ladder that the entire chapter will reuse.

First, a **value definition** names an object such as $V^\pi(s)$ or $Q^\pi(s,a)$ as a conditional expectation of return. At this level, nothing recursive has happened yet.

Second, an **exact Bellman equation** is a true identity satisfied by the genuine value object once the return recursion is inserted into the definition and the Markov structure licenses state-based conditioning.

Third, a **Bellman operator** is a transformation that can be applied to any candidate function, whether or not that function is already the true value function. At this level the question is no longer “what is the value?” but “what does one Bellman-style backup do to an arbitrary guess?”

Fourth, an **algorithmic update rule** is a numerical procedure that uses samples or repeated backups to move an estimate toward a fixed point or control solution. At this level one is no longer stating a property of the exact value object. One is constructing an iterative approximation mechanism.

If these four levels are kept separate, the chapter’s logic is stable. If they are fused, the reader starts treating definitions as updates, operators as theorems, and Bellman identities as if they were already algorithms.

Before the chapter enters the formal sections, it should lock four different levels that will recur throughout.

First, a **value definition** says what quantity is being averaged. For example, $V^\pi(s)$ is an expectation of return under a fixed policy and state condition.

Second, an **exact Bellman identity** says that if the setting is truly Markov in the required sense, then that defined value obeys a particular recursive expectation equation.

Third, a **Bellman operator** is a transformation that can be applied to any candidate function, whether or not that function is already the true value function.

Fourth, an **algorithmic update** is a computational rule that tries to move an estimate toward a Bellman-consistent fixed point.

These are related, but they are not interchangeable. A definition is not yet a recursion. A recursion is not yet an operator on arbitrary guesses. An operator is not yet an algorithm. One of the main jobs of this chapter is to prevent those levels from collapsing into one another.

By the end of the chapter, the reader should be able to explain not only what the value functions are, but why they must be introduced now, what exact problem they solve, how the Bellman expectation equations are derived line by line, why the operator viewpoint matters, what contraction contributes mathematically, how optimality equations differ from evaluation equations, and what the policy-improvement theorem really proves—and just as importantly, what it does not prove.

---

## 1. Why value functions must appear now

### Why this section exists

A return is the right global objective, but it is too large to use directly as the basic unit of reasoning. The agent makes decisions state by state and action by action, not by manipulating an entire future reward sequence all at once. So the chapter needs a way to attach long-run meaning to local decision points. Without that move, there is no clean way to compare states, compare actions within a state, or define what it means for one policy to be better than another from a given situation onward.

This section exists because the chapter cannot proceed from “future cumulative reward matters” to “dynamic programming and improvement are possible” without introducing local long-run quantities. Value functions are exactly those quantities.

### The object being introduced

The object being introduced is a conditional expectation of return. There are several versions of this idea, but they all have the same structure. The underlying random quantity is still the return $G_t$. What changes is the information being held fixed when we average it.

A state-value function fixes the current state and asks for the expected return from there onward under a given policy. An action-value function fixes both the current state and the current action, then asks for the expected return from there onward under that same policy. An advantage function compares those two quantities to measure whether a particular action is better or worse than the policy’s own average action choice at that state.

What is fixed in these objects is the policy and the conditioning information. What varies are all the future random events that remain uncertain after that information is held fixed. The conclusions these objects allow are local judgments about long-run quality.

### Formal definition

Fix a policy $\pi$.

The **state-value function** under policy $\pi$ is

$$
V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t=s].
$$

The **action-value function** under policy $\pi$ is

$$
Q^\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t=s, A_t=a].
$$

The **advantage function** under policy $\pi$ is

$$
A^\pi(s,a) = Q^\pi(s,a) - V^\pi(s).
$$

### Interpretation paragraph

These are definitions, not yet theorems. That boundary matters. The chapter begins here because students often encounter the first displayed value equation as if it were already a recursive law. It is not. At this stage, the equations are naming objects.

The first thing to notice is what kind of quantities these are. They are not immediate rewards. They are not transition probabilities. They are not policies. They are expected *long-run* returns conditioned on present information. The symbol $V^\pi(s)$ means: if the current state is $s$ and policy $\pi$ is followed from now on, what return should we expect on average? The symbol $Q^\pi(s,a)$ means: if the current state is $s$, the current action is forced to be $a$, and then policy $\pi$ is followed thereafter, what return should we expect on average? The advantage $A^\pi(s,a)$ then asks whether action $a$ is above or below the policy’s own average quality at state $s$.

The notation also encodes a subtle but crucial distinction. The superscript $\pi$ identifies which policy is being evaluated. The arguments $(s)$ or $(s,a)$ identify what local information is being held fixed when the expectation is taken. If either of those changes, the quantity changes.

### Boundary conditions, assumptions, and failure modes

Several assumptions are often left unstated when these definitions are first presented. The return $G_t$ must be well-defined under the conditions of the problem. In the discounted continuing setting, that typically means bounded rewards and $0 \le \gamma < 1$. In finite-horizon episodic settings, the horizon itself controls finiteness.

Another important boundary condition is conceptual rather than technical: these definitions do not yet require recursive reasoning, dynamic programming, or Bellman equations. They only require that the return exists and that the conditional expectation is meaningful.

A common failure mode is to treat $V^\pi$ and $Q^\pi$ as interchangeable because both “measure long-run goodness.” They do not condition on the same information, so they are not the same kind of object. Another failure mode is to think the advantage function is an independent primitive. It is not. It is defined from $Q^\pi$ and $V^\pi$.

### Fully worked example

Consider a state $s$ in which policy $\pi$ chooses action $a_1$ with probability $0.7$ and action $a_2$ with probability $0.3$. Suppose that if the agent takes $a_1$ now and then follows $\pi$, the expected return is $5$. If the agent takes $a_2$ now and then follows $\pi$, the expected return is $2$.

The first task is to identify which object each number belongs to. The statement “if the agent takes $a_1$ now and then follows $\pi$, the expected return is $5$” is telling us

$$
Q^\pi(s,a_1)=5.
$$

Likewise,

$$
Q^\pi(s,a_2)=2.
$$

Now ask for the state value $V^\pi(s)$. By definition, this is the expected return when the current state is $s$ and the agent follows policy $\pi$. Since the policy randomizes over the two available actions, the state value is the policy-weighted average of the two action-conditioned returns. So

$$
V^\pi(s)=0.7\cdot 5 + 0.3\cdot 2 = 3.5 + 0.6 = 4.1.
$$

Now compute the advantages:

$$
A^\pi(s,a_1)=Q^\pi(s,a_1)-V^\pi(s)=5-4.1=0.9,
$$

$$
A^\pi(s,a_2)=Q^\pi(s,a_2)-V^\pi(s)=2-4.1=-2.1.
$$

What did each step establish? First, the numbers $5$ and $2$ were identified as action values because they condition on both state and chosen action. Second, the state value was recognized as the policy’s own average over those action values. Third, the advantage values were interpreted as deviations from that policy average. The final interpretation is that, under this policy, action $a_1$ is better than the policy’s average first action at state $s$, while action $a_2$ is worse.

The general lesson is that state value summarizes what happens if the policy chooses as usual, while action value isolates what happens if a particular first action is forced.

### Misconception or counterexample block

**Do not confuse “good state” with “good action.”** A state can have a high value because the policy usually chooses strong actions there, while some particular action in that same state may still be poor. That is exactly why $Q^\pi(s,a)$ and $V^\pi(s)$ are different objects.

**Do not confuse advantage with absolute quality.** A positive advantage means “better than the policy’s average action at this state,” not necessarily “globally excellent” in any absolute sense.

### Connection to later material

These objects will be the target of every major development in the chapter. The Bellman expectation equations will describe them recursively. The operator viewpoint will treat them as fixed points. Optimality equations will describe the best achievable versions of them. Policy improvement will use $Q^\pi$ to build better policies. In other words, this section introduces the actual mathematical entities that the rest of the chapter manipulates.

### Retain / Do not confuse

Retain that $V^\pi$, $Q^\pi$, and $A^\pi$ are definitions built from conditional expectations of return. Do not confuse state value with action value, and do not treat the advantage function as an independent primitive.

---

## 2. The relation between state value and action value

### Why this section exists

Once the definitions are on the table, the next obvious question is whether they are independent or structurally related. They cannot be unrelated, because both are ways of measuring long-run return under the same policy at the same current state. The missing bridge is the random current action chosen by the policy. This section exists to show exactly how the state-value function is assembled from action-value terms.

Without this step, the later policy-improvement argument would feel unmotivated. The theorem relies on understanding $V^\pi(s)$ as an average over the $Q^\pi(s,a)$ values.

### The object being introduced

The object here is not a new value function, but a relation between existing ones. The question it answers is: once the current state $s$ is fixed, how does the randomness of the policy’s current action turn $Q^\pi(s,a)$ values into the state value $V^\pi(s)$?

What is fixed is the state $s$ and the policy $\pi$. What varies is which current action $a$ is sampled from $\pi(\cdot\mid s)$. The conclusion this relation allows is that $V^\pi(s)$ is the policy-weighted average of action values at that state.

### Formal definition

For any state $s$,

$$
V^\pi(s) = \sum_a \pi(a\mid s)Q^\pi(s,a).
$$

### Interpretation paragraph

This equation says that once the state is known, the only remaining policy-controlled uncertainty at the current decision time is which action gets selected. Each possible action $a$ leads to its own conditional expected return $Q^\pi(s,a)$. The policy supplies the weights $\pi(a\mid s)$ telling us how often each of those action-conditioned futures is entered. So the state value is not a mysterious new quantity floating beside $Q^\pi$. It is the policy’s own average over those action values.

The first thing to notice is that this equation is not yet recursive in time. It is only decomposing current-state value across current action choices. Its importance is conceptual: it shows how state value and action value fit together at the same decision point.

### Boundary conditions, assumptions, and failure modes

This equation assumes we are in the usual setting where the policy defines a probability distribution over actions at state $s$. In continuous action spaces, the sum becomes an integral, but the meaning is the same.

A frequent failure mode is to read the equation backward as if the state value uniquely determines all action values. It does not. Many different collections of action values can average to the same state value under a given policy. Another failure mode is to ignore that the weights come from the *current* policy. If the policy changes, the weighted average changes even if the action values did not.

### Fully worked example

Suppose a policy at state $s$ chooses among three actions with probabilities

$$
\pi(a_1\mid s)=0.2, \qquad \pi(a_2\mid s)=0.5, \qquad \pi(a_3\mid s)=0.3.
$$

Suppose the corresponding action values are

$$
Q^\pi(s,a_1)=8, \qquad Q^\pi(s,a_2)=1, \qquad Q^\pi(s,a_3)=4.
$$

We want to compute $V^\pi(s)$ and interpret the result carefully.

Start by identifying the varying object. The current state is fixed as $s$. The action varies according to the policy. For each possible action, $Q^\pi(s,a)$ tells us the expected long-run return conditional on that action being taken now.

Apply the formula:

$$
V^\pi(s)=\sum_a \pi(a\mid s)Q^\pi(s,a)=0.2(8)+0.5(1)+0.3(4).
$$

Now compute each contribution. The first action contributes $1.6$, the second contributes $0.5$, and the third contributes $1.2$. Adding them gives

$$
V^\pi(s)=1.6+0.5+1.2=3.3.
$$

What conclusion does this allow? It tells us that if the agent simply follows policy $\pi$ from state $s$, the expected return is $3.3$. That number reflects not only the quality of the actions but also how often the policy chooses them. Notice that action $a_1$ has the highest action value, but the policy chooses it only $20\%$ of the time. So the state value is pulled downward by the frequent selection of lower-quality actions.

The general lesson is that state value is policy-dependent in two ways at once: through the future behavior of the policy and through its current action mixture.

### Misconception or counterexample block

**Do not say “the value of a state is the max over action values.”** That is false for policy evaluation. Under a fixed policy, the state value is an average over action values according to that policy. The maximization enters only when discussing optimal control, not ordinary evaluation.

### Connection to later material

This relation will later be the first step in policy improvement. Because a weighted average cannot exceed the maximum of the numbers being averaged, the equation immediately suggests why replacing the current action mixture by greedy action choice should help. That intuition becomes a theorem later in the chapter.

### Retain / Do not confuse

Retain that $V^\pi(s)$ is the current policy’s weighted average over $Q^\pi(s,a)$ values. Do not confuse policy evaluation with maximization over actions.

---

## 3. The return recursion comes before the Bellman equations

### Why this section exists

Students often meet the Bellman equations first and then mentally fuse several distinct steps into one. That fusion causes long-term confusion. The recursive structure of value functions does not come from nowhere. It comes from an algebraic fact about the return itself. This section exists to restore the correct order of ideas.

Without this section, the reader is likely to think Bellman equations are mysterious special formulas attached to Markov decision processes rather than the natural result of putting a basic return identity inside conditional expectations.

### The object being introduced

The object here is the recursion satisfied by the return random variable itself. It answers the question: how does the full return from time $t$ decompose into an immediate next reward and the rest of the future?

What is fixed is the definition of the return $G_t$. What varies is how we regroup the terms of its defining sum. The conclusion this identity allows is that the future can be split into “now plus continuation.”

### Formal definition

For discounted return,

$$
G_t = R_{t+1} + \gamma G_{t+1}.
$$

### Interpretation paragraph

This is a plain identity about the return random variable. It says that the return from time $t$ consists of the next reward $R_{t+1}$ plus the return from the next time step onward, discounted once because it lies one step further in the future.

The key thing to notice first is what kind of statement this is not. It is not yet a Bellman equation. It does not yet mention state values, action values, or the Markov property. It is only a decomposition of the return itself, derived from the way $G_t$ is defined.

### Boundary conditions, assumptions, and failure modes

This identity assumes the return is well-defined in the underlying problem class. In discounted continuing tasks, that means the usual conditions that justify the infinite sum. In finite-horizon episodic tasks, it is automatically finite.

A common failure mode is to call this the Bellman equation. That is too early. A Bellman equation arises only after taking conditional expectations and using the problem structure to express the continuation term as a value function.

### Fully worked example

Suppose the discount factor is $\gamma=0.9$, and in a particular realized episode the next few rewards are

$$
R_{t+1}=3, \qquad R_{t+2}=4, \qquad R_{t+3}=-1,
$$

with all later rewards equal to $0$.

First compute $G_t$ directly from the definition:

$$
G_t = R_{t+1} + 0.9R_{t+2} + 0.9^2R_{t+3} = 3 + 0.9(4) + 0.81(-1).
$$

That gives

$$
G_t = 3 + 3.6 - 0.81 = 5.79.
$$

Now compute $G_{t+1}$:

$$
G_{t+1} = R_{t+2} + 0.9R_{t+3} = 4 + 0.9(-1) = 3.1.
$$

Insert this into the recursion:

$$
R_{t+1} + 0.9G_{t+1} = 3 + 0.9(3.1) = 3 + 2.79 = 5.79.
$$

The two calculations match. What has been checked? First, the return from time $t$ was computed directly as a future reward sum. Second, the return from time $t+1$ was computed separately. Third, the immediate reward and discounted continuation were recombined. The final interpretation is that the return can always be peeled into one reward plus a smaller copy of the same object one step later.

The general lesson is that recursive structure is already present in the return before any value function is mentioned.

### Misconception or counterexample block

**Do not confuse “recursive” with “Markov.”** The recursion of the return is algebraic and does not require the Markov property. The Markov property matters later when we express continuation expectations using state-based functions.

### Connection to later material

The Bellman expectation equations will be derived by taking conditional expectations of this identity. That is the exact ladder: define return, write the return recursion, then condition on the relevant current information.

### Retain / Do not confuse

Retain that $G_t = R_{t+1} + \gamma G_{t+1}$ is an identity about the return random variable. Do not confuse it with a Bellman equation or with a theorem that already assumes the MDP structure.

---

## 4. Deriving the Bellman expectation equation for the state-value function

### Why this section exists

Now that the state-value function has been defined and the return recursion is in place, the natural next question is whether the state value can be written recursively. That question matters because recursive formulas are what make dynamic programming possible. If the reader cannot see the derivation, later uses of the Bellman equation tend to feel like symbol pushing rather than controlled reasoning.

This section exists to show the derivation slowly enough that every split, every conditioning step, and every recognition move is visible.

### The object being introduced

The object is the Bellman expectation equation for $V^\pi$. It is a recursive identity for the state-value function under a fixed policy. It answers the question: once we know the current state $s$, how can we express the expected return in terms of one-step outcomes and the value of successor states?

What is fixed is the current policy $\pi$ and the current state $s$. What varies are the current action, the next reward, the next state, and all future randomness beyond that. The conclusion this equation allows is that long-run value can be computed from one-step environment dynamics plus continuation value.

### Formal definition

The Bellman expectation equation for the state-value function is

$$
V^\pi(s)=\sum_a \pi(a\mid s) \sum_{s',r} P(s',r\mid s,a)\bigl[r + \gamma V^\pi(s')\bigr].
$$

### Interpretation paragraph

This equation says that the value of a state under policy $\pi$ is obtained by looking one step ahead. First, the policy chooses an action $a$ with probability $\pi(a\mid s)$. Then the environment produces a next state $s'$ and reward $r$ according to $P(s',r\mid s,a)$. The agent receives the immediate reward $r$ and then continues from $s'$, whose expected future return is $V^\pi(s')$. Averaging that one-step-plus-continuation quantity over all possible actions and one-step outcomes gives the current state value.

The reader should notice the meaning of the recursion. A long-run quantity has been turned into a local averaging equation. That is the conceptual heart of the chapter.

### Boundary conditions, assumptions, and failure modes

This equation uses the Markov decision process structure. In particular, once the current state $s$ and action $a$ are fixed, the distribution of the next state and reward is given by $P(s',r\mid s,a)$, and the continuation under policy $\pi$ depends on the future only through the next state $s'$. Without that structure, the state-only recursion would not generally be valid.

Another important boundary line is that the equation is exact under the stated assumptions. It is not a sampled estimate and not an approximation method. Approximation enters later chapters, not here.

A common failure mode is to skip directly from the definition of $V^\pi(s)$ to the final formula, losing sight of which random variables were split on and in what order.

The exact order is worth stating once in full prose. One begins with the definition of return under a fixed current state and fixed policy. Then one decomposes the return into immediate reward plus discounted continuation return. Then one conditions on the first action selected by the policy and on the first next-state/reward outcome generated by the environment. Only after those one-step random quantities have been exposed does one recognize the continuation term as the same value function evaluated at the next state. The Bellman equation is therefore not a clever guess. It is a structured re-expression of the original definition under the Markov factorization already justified earlier.

### Fully worked example

Suppose a state $s$ has two possible actions, $a_1$ and $a_2$, and the policy satisfies

$$
\pi(a_1\mid s)=0.6, \qquad \pi(a_2\mid s)=0.4.
$$

Assume the one-step environment law is as follows.

If action $a_1$ is taken from state $s$:
- with probability $0.5$, the next state is $s_1$ and the reward is $2$;
- with probability $0.5$, the next state is $s_2$ and the reward is $0$.

If action $a_2$ is taken from state $s$:
- with probability $1$, the next state is $s_2$ and the reward is $1$.

Let the discount factor be $\gamma=0.9$, and suppose

$$
V^\pi(s_1)=10, \qquad V^\pi(s_2)=4.
$$

We want to compute $V^\pi(s)$ using the Bellman expectation equation, but we will narrate the reasoning rather than just substituting mechanically.

Start from the meaning of $V^\pi(s)$. It is the expected return from state $s$ under policy $\pi$. By the return recursion, that return is the next reward plus discounted continuation. So the key quantity to average is

$$
R_{t+1} + 0.9V^\pi(S_{t+1}).
$$

Now split by the current action. Under action $a_1$, the expected one-step-plus-continuation value is

$$
0.5[2 + 0.9(10)] + 0.5[0 + 0.9(4)].
$$

Compute the two branches:

$$
2 + 0.9(10)=11,
$$

$$
0 + 0.9(4)=3.6.
$$

So the conditional expectation under action $a_1$ is

$$
0.5(11)+0.5(3.6)=5.5+1.8=7.3.
$$

Now evaluate action $a_2$. Since the next outcome is deterministic in this example, the expected one-step-plus-continuation value is simply

$$
1 + 0.9(4)=4.6.
$$

Now average over the current policy’s action probabilities:

$$
V^\pi(s)=0.6(7.3)+0.4(4.6)=4.38+1.84=6.22.
$$

What did each step establish? First, the continuation structure came from the return recursion. Second, the action split was weighted by the policy. Third, the transition split was weighted by the environment law. Fourth, the continuation after reaching $s'$ was recognized as exactly $V^\pi(s')$. The final interpretation is that the current state value is the policy-weighted average of one-step reward plus discounted successor-state value.

The general lesson is that every Bellman derivation follows the same pattern: substitute the return recursion, split on the next random event(s), and recognize the continuation as a value function.

### Misconception or counterexample block

**Do not say “the Bellman equation predicts the next reward only.”** The next reward is only the first part of the equation. The decisive second part is the discounted continuation value, which carries the entire future through recursion.

**Do not say “this is a computational shortcut only.”** It is first a mathematical identity. Its computational uses come afterward.

### Connection to later material

This state-value Bellman equation will underpin policy evaluation, operator fixed-point analysis, and later iterative algorithms. It is the foundational recursive law for evaluating a fixed policy.

### Retain / Do not confuse

Retain that the Bellman expectation equation for $V^\pi$ is derived by inserting the return recursion inside a conditional expectation and then splitting on action and one-step transition outcome. Do not confuse it with an approximation or with an equation that holds without the MDP assumptions.

---

## 5. Deriving the Bellman expectation equation for the action-value function

### Why this section exists

The state-value Bellman equation evaluates a policy starting from a state. But control problems require comparing particular actions within a state. That means the chapter also needs a recursive equation for $Q^\pi(s,a)$. Without it, action-based improvement rules would lack a principled foundation.

This section exists because the state-value recursion alone does not tell us how the long-run value of a specific state-action pair decomposes into immediate reward and continuation.

### The object being introduced

The object is the Bellman expectation equation for the action-value function. It answers the question: once the current state $s$ and current action $a$ are fixed, how does the expected return decompose into one-step environment outcomes and continuation under the same policy?

What is fixed is the pair $(s,a)$ and policy $\pi$. What varies are the next reward, the next state, the next action chosen by the policy at that next state, and everything after that. The conclusion it allows is a recursive local equation for action values.

### Formal definition

The Bellman expectation equation for the action-value function is

$$
Q^\pi(s,a)=\sum_{s',r} P(s',r\mid s,a)\bigl[r + \gamma V^\pi(s')\bigr].
$$

Using the relation between state value and action value, this can also be written as

$$
Q^\pi(s,a)=\sum_{s',r} P(s',r\mid s,a)\left[r + \gamma \sum_{a'} \pi(a'\mid s')Q^\pi(s',a')\right].
$$

### Interpretation paragraph

The logic here is slightly different from the state-value case. Because the current action is already fixed as $a$, there is no current action average at the first step. The immediate next uncertainty begins with the one-step transition outcome $(s',r)$. After that outcome is realized, the policy takes over again from the next state $s'$, so the continuation is measured by $V^\pi(s')$. If desired, that continuation value can be expanded into a policy average over next-step action values.

The first thing to notice is the role split between the two displayed forms. The first form expresses the action value through successor-state values. The second keeps everything in terms of $Q^\pi$. Both are exact; they simply emphasize different structural viewpoints.

### Boundary conditions, assumptions, and failure modes

As before, the equation relies on the MDP structure and on the return being well-defined. It also relies on the idea that after the forced first action, the same policy $\pi$ governs future action choices.

A common failure mode is to read the second form as if the maximization of future action values were already present. It is not. The continuation still averages over future actions according to $\pi$. Maximization belongs to optimality equations, not policy evaluation equations.

### Fully worked example

Suppose the current state-action pair is $(s,a)$, and the environment has the following one-step law. With probability $0.3$, the next state is $s_1$ and the immediate reward is $5$. With probability $0.7$, the next state is $s_2$ and the immediate reward is $-1$. Let $\gamma=0.8$, and suppose the continuation values under policy $\pi$ are already known. The point of writing the law in prose is that the Bellman expectation is not “looking up a formula.” It is averaging the continuation expression over the exact next-state and reward law generated by the present state-action pair.

Let $\gamma=0.8$, and suppose the state values under policy $\pi$ are

$$
V^\pi(s_1)=6, \qquad V^\pi(s_2)=3.
$$

We want to compute $Q^\pi(s,a)$.

Because the first action is fixed, the only first-step randomness is in the environment outcome. The Bellman expectation equation therefore tells us to average the quantity

$$
r + 0.8V^\pi(s')
$$

over the possible next outcomes.

For the first branch, the contribution is

$$
5 + 0.8(6)=5+4.8=9.8.
$$

For the second branch, the contribution is

$$
-1 + 0.8(3)=-1+2.4=1.4.
$$

Now weight by the transition probabilities:

$$
Q^\pi(s,a)=0.3(9.8)+0.7(1.4)=2.94+0.98=3.92.
$$

That is the expected return from taking action $a$ now in state $s$ and then following policy $\pi$. The reasoning checked three things in order: which part of the uncertainty remains after conditioning on $(s,a)$, what the one-step-plus-continuation quantity is on each branch, and how those branches are weighted.

Now suppose additionally that at state $s_1$, policy $\pi$ chooses actions $b_1$ and $b_2$ with probabilities $0.25$ and $0.75$, and the corresponding action values are $Q^\pi(s_1,b_1)=10$ and $Q^\pi(s_1,b_2)=14$. Then

$$
V^\pi(s_1)=0.25(10)+0.75(14)=2.5+10.5=13.
$$

This illustrates how the continuation value in the first Bellman form can be unfolded into policy-weighted action values in the second form.

The general lesson is that fixing the current action removes one layer of policy averaging at the first step, but future steps are still controlled by the same policy.

### Misconception or counterexample block

**Do not confuse “current action fixed” with “all future actions fixed.”** In $Q^\pi(s,a)$, only the first action is forced. After that, the process follows policy $\pi$, so future actions remain random according to that policy.

### Connection to later material

This equation is the bridge from policy evaluation to policy improvement. To improve a policy, one must compare the $Q^\pi(s,a)$ values of available actions and prefer the better ones. That idea becomes formal later in the chapter.

### Retain / Do not confuse

Retain that the Bellman equation for $Q^\pi$ fixes the current action, averages over the next environment outcome, and then continues under the same policy. Do not confuse policy evaluation with future-action maximization.

---

## 6. Definitions, exact identities, and approximations must stay separate

### Why this section exists

A surprisingly large fraction of confusion in reinforcement learning comes from mixing different logical types of statements together. Readers often move through a chapter with several displayed equations and never stabilize which ones are definitions, which ones are exact consequences of those definitions, and which ones come from estimation or approximation schemes. That instability causes downstream misunderstandings about what is guaranteed and what is only approximate.

This section exists to draw a sharp boundary line.

### The object being introduced

The object here is not a new formula but a classification scheme for formulas. The question it answers is: what kind of statement is each important equation in this chapter?

What is fixed is the list of equations already introduced. What varies is their logical role. The conclusion this classification allows is disciplined reasoning: one knows what can be used as a definition, what requires proof, and what belongs to later approximate algorithms.

### Formal definition

In this chapter, three logical categories must be kept separate. The **definitions** introduce the objects $V^\pi$, $Q^\pi$, and $A^\pi$ by stipulating what those symbols mean. The **exact identities** are then mathematical consequences of those definitions together with the assumptions of the setting; this category includes the return recursion, the relation $V^\pi(s)=\sum_a\pi(a\mid s)Q^\pi(s,a)$, and the Bellman expectation equations. **Approximations** do not yet belong to the chapter’s core logic. They arrive later, when exact expectations are replaced by sampled targets or function approximation. Writing the categories in prose rather than as a list makes the logical dependency explicit: definitions come first, exact identities depend on them, and approximations are later substitutes for exact quantities rather than part of the foundational proof structure.

### Interpretation paragraph

A definition introduces a new object by stipulating what the notation means. It is not true or false; it is adopted. An exact identity is a mathematical consequence of definitions plus the assumptions of the setting. It can be proved and then used. An approximation is neither of those: it is a substitute for an exact quantity, usually introduced for computational or statistical reasons.

The first thing the reader should notice is that confusion between these categories produces very different errors. Mistaking a definition for a theorem makes one forget what the object means. Mistaking an identity for an approximation makes one understate what is exact. Mistaking an approximation for an identity makes one overclaim correctness.

### Adversarial checkpoint: the theorem object is not the code object

At this point a strong but still unsafe reader may say: "I understand the Bellman operator, so my update code is just the theorem in incremental form." That is not yet justified. The theorem-level object is an exact map on functions under stated assumptions about the model and return. The code-level object is often a sampled, partial, asynchronous, or approximate update using only one transition or minibatch at a time. Those two objects are related, but they are not identical.

The hostile question is: **which object is your convergence claim about?** If the claim is about a fixed point of an exact operator, then you must name the operator and its assumptions. If the claim is about a learning rule applied to sampled data, then you must also account for noise, step sizes, coverage, approximation, and data dependence. Saying "Bellman" is not enough to bridge that gap.

### Boundary conditions, assumptions, and failure modes

The exact identities remain exact only under the assumptions under which they were derived, especially the MDP structure and well-defined return. Approximations may later be extremely useful, but they do not inherit the status of exact identities merely because they resemble them algebraically.

A common failure mode is to say something like “the Bellman equation is a target used in learning.” That is incomplete and often misleading. First it is an exact recursive identity. Only later are sampled or approximate Bellman-style targets constructed from it.

### Fully worked example

Consider the three equations

$$
Q^\pi(s,a)=\mathbb{E}_\pi[G_t\mid S_t=s,A_t=a],
$$

$$
G_t=R_{t+1}+\gamma G_{t+1},
$$

and

$$
Q^\pi(s,a)=r + \gamma \max_{a'} Q(s',a').
$$

We now classify them carefully.

The first equation is a definition. It tells us what the notation $Q^\pi(s,a)$ means.

The second equation is an exact identity about the return random variable. It follows from the definition of discounted return.

The third equation, as written with specific realized $r$ and $s'$, is not generally an exact identity for the true action-value function. It resembles a one-step target used in control algorithms. Without expectation over next outcomes and without clarifying whether $Q$ is exact or approximate, it is not of the same logical type as the first two equations.

What conclusion does this classification allow? It prevents the reader from silently moving between levels of exactness. The general lesson is that before asking whether an equation is useful, one must ask what kind of statement it is.

### Misconception or counterexample block

**Do not confuse “used in a learning update” with “only approximate by nature.”** Some exact identities later inspire approximate update rules. The practical use of an equation in learning does not determine its logical status.

### Connection to later material

This distinction becomes even more important in temporal-difference learning, Monte Carlo estimation, and function approximation. Those chapters inherit exact identities from this chapter, then deliberately replace inaccessible expectations by estimates. If the boundary is not sharp now, those later chapters become much harder to reason about correctly.

### Retain / Do not confuse

Retain that definitions name objects, exact identities relate them rigorously, and approximations come later. Do not blur these categories when reading or using Bellman-style formulas.

---

## 7. The Bellman operator viewpoint

### Why this section exists

The Bellman equations already provide recursive formulas, so why introduce operators at all? Because recursion alone does not yet highlight the underlying mathematical structure. The operator viewpoint turns value computation into a fixed-point problem. That re-description is not cosmetic. It is what makes contraction arguments, uniqueness results, and iterative solution methods transparent.

This section exists because dynamic programming is fundamentally about repeatedly applying a transformation to a candidate value function until the fixed point is reached. The operator notation packages that transformation as an object in its own right.

### The object being introduced

The object is an operator: a mapping that takes one value function as input and produces another value function as output. For a fixed policy $\pi$, the Bellman expectation operator takes a candidate function $V$ and produces a new function whose value at each state is the expected one-step reward plus discounted continuation using $V$ as the continuation estimate. The Bellman optimality operator does the same except it uses the best action rather than averaging under a fixed policy.

What is fixed is the environment model and either the policy or the optimal-control criterion. What varies is the candidate value function on which the operator acts. The conclusions operators allow are fixed-point statements and convergence arguments.

### Formal definition

The **Bellman expectation operator** for a fixed policy $\pi$ is

$$
(T^\pi V)(s)=\sum_a \pi(a\mid s) \sum_{s',r} P(s',r\mid s,a)\bigl[r + \gamma V(s')\bigr].
$$

The **Bellman optimality operator** is

$$
(T^*V)(s)=\max_a \sum_{s',r} P(s',r\mid s,a)\bigl[r + \gamma V(s')\bigr].
$$

The Bellman equations can then be written as fixed-point equations:

$$
V^\pi = T^\pi V^\pi,
$$

$$
V^* = T^* V^*.
$$

### Interpretation paragraph

The operator $T^\pi$ does not assume its input function $V$ is already correct. It simply says: if you hand me any candidate continuation-value function $V$, I will produce the one-step lookahead value obtained by combining immediate reward with discounted continuation according to $V$. The true policy value function $V^\pi$ is exactly the function that remains unchanged under this transformation. That is what it means to be a fixed point.

The same logic applies to $T^*$, except that instead of averaging over the next action according to a policy, the operator chooses the best action at each state. The first thing to notice is that “Bellman equation” and “fixed-point equation” are two views of the same structure.

### Boundary conditions, assumptions, and failure modes

The operator viewpoint assumes the same underlying discounted MDP framework used earlier. The fixed-point claims are meaningful only because the value functions exist and the operators are well-defined on the class of candidate functions under consideration.

A common failure mode is to think the operator is merely shorthand for a long formula. It is more than notation. It changes the level of abstraction so that one can talk about repeated application, contraction, uniqueness, and convergence.

Another failure mode is to confuse the policy operator $T^\pi$ with the optimality operator $T^*$. The first evaluates a specified policy; the second encodes the best possible one-step choice with continuation.

### Fully worked example

Consider an MDP with two states, $s_1$ and $s_2$, and a fixed policy $\pi$ that chooses a single action in each state deterministically. Suppose the one-step structure is as follows:

- From $s_1$, the next reward is always $2$ and the next state is always $s_2$.
- From $s_2$, the next reward is always $1$ and the next state is always $s_2$.

Let $\gamma=0.5$. We will apply $T^\pi$ to a candidate value function $V$ satisfying

$$
V(s_1)=10, \qquad V(s_2)=4.
$$

Compute $(T^\pi V)(s_1)$. There is no action randomness and no transition randomness in this example, so the formula becomes

$$
(T^\pi V)(s_1)=2 + 0.5V(s_2)=2+0.5(4)=4.
$$

Now compute $(T^\pi V)(s_2)$:

$$
(T^\pi V)(s_2)=1 + 0.5V(s_2)=1+0.5(4)=3.
$$

So the operator maps the candidate function $V$ to the new function with values

$$
(T^\pi V)(s_1)=4, \qquad (T^\pi V)(s_2)=3.
$$

What has this example shown? First, the operator takes a whole function as input, not a single scalar. Second, it performs a one-step lookahead using that candidate continuation function. Third, unless the input function was already the correct fixed point, the output differs from the input. The general lesson is that the Bellman operator describes the transformation whose fixed point is the desired value function.

### Misconception or counterexample block

**Do not confuse “apply the Bellman operator once” with “solve for the value function.”** One application generally produces a better-informed one-step lookahead value, but only the fixed point gives the exact value function.

A short status reminder belongs here. Applying the Bellman operator once is an operation on a **candidate function**. Writing the Bellman expectation equation for $V^\pi$ is a statement about the **true value function**. Those are related because the true value is a fixed point of the operator, but they are not the same statement. The operator view is what later turns a theorem about exact values into an iterative route toward those values.

### Connection to later material

This operator viewpoint is the doorway to contraction theory, iterative policy evaluation, value iteration, and many approximate methods. It is also one of the cleanest examples in reinforcement learning of how an optimization or evaluation problem can be reframed as finding a fixed point of a map.

### Retain / Do not confuse

Retain that Bellman operators map candidate value functions to one-step lookahead value functions, and the true values are fixed points of those operators. Do not confuse operator notation with mere cosmetic abbreviation.

---

## 8. Why contraction matters

### Why this section exists

The operator viewpoint becomes mathematically powerful only when we know something about how the operator behaves. A fixed-point equation alone does not guarantee uniqueness or convergence of iterative application. Contraction is the property that supplies both. This section exists because it explains why dynamic programming methods in discounted problems have such clean convergence logic.

Without contraction, iterative application of Bellman operators would be a hopeful procedure. With contraction, it becomes a principled one.

### The object being introduced

The object is the contraction property of Bellman operators in the supremum norm. It answers the question: if two candidate value functions differ, how much can one application of the Bellman operator enlarge or shrink that difference?

What is fixed is the discounted setting and the norm used to measure function differences. What varies are the two candidate functions being compared. The conclusion it allows is that the operator pulls functions closer together by at least a factor of $\gamma$.

### Formal definition

Under bounded value functions and $0\le \gamma <1$,

$$
\|T^\pi V - T^\pi W\|_\infty \le \gamma \|V-W\|_\infty.
$$

Likewise, the optimality operator also satisfies

$$
\|T^*V - T^*W\|_\infty \le \gamma \|V-W\|_\infty.
$$

### Interpretation paragraph

The supremum norm $\|V-W\|_\infty$ is the largest absolute difference between the two functions across all states. The contraction inequality says that after one Bellman update, the maximum discrepancy between the transformed functions is at most $\gamma$ times the old maximum discrepancy. Since $\gamma<1$, repeated application shrinks differences geometrically.

The first thing to notice is why the factor is exactly $\gamma$. The immediate reward terms cancel when differences are taken. The only surviving difference is in the continuation terms, and every continuation term is multiplied by $\gamma$. Probabilities average those continuation differences but do not amplify them beyond their maximum.

### Boundary conditions, assumptions, and failure modes

The discounted condition $\gamma<1$ is essential for contraction in this form. If $\gamma=1$, the argument no longer yields a strict contraction factor. Additional structure would then be needed to recover comparable guarantees.

The argument also depends on working with bounded value functions in the supremum norm. Different settings may require different spaces or norms.

A common failure mode is to think contraction means the operator moves each value estimate monotonically toward truth. That is not what the inequality says. It says the distance between any two functions shrinks under the operator, which implies uniqueness and convergence of iteration, not necessarily monotone componentwise movement.

### Fully worked example

Consider the same deterministic two-state system from the previous section with $\gamma=0.5$, and compare two candidate value functions:

$$
V(s_1)=10, \qquad V(s_2)=4,
$$

$$
W(s_1)=6, \qquad W(s_2)=8.
$$

First compute their supremum-norm distance:

$$
|V(s_1)-W(s_1)|=|10-6|=4,
$$

$$
|V(s_2)-W(s_2)|=|4-8|=4.
$$

So

$$
\|V-W\|_\infty=4.
$$

Now apply the Bellman operator from the earlier example. We already know that for any candidate function $X$,

$$
(T^\pi X)(s_1)=2+0.5X(s_2), \qquad (T^\pi X)(s_2)=1+0.5X(s_2).
$$

Apply it to $V$:

$$
(T^\pi V)(s_1)=2+0.5(4)=4,
$$

$$
(T^\pi V)(s_2)=1+0.5(4)=3.
$$

Apply it to $W$:

$$
(T^\pi W)(s_1)=2+0.5(8)=6,
$$

$$
(T^\pi W)(s_2)=1+0.5(8)=5.
$$

Now compare the transformed functions:

$$
|(T^\pi V)(s_1)-(T^\pi W)(s_1)|=|4-6|=2,
$$

$$
|(T^\pi V)(s_2)-(T^\pi W)(s_2)|=|3-5|=2.
$$

Therefore

$$
\|T^\pi V - T^\pi W\|_\infty=2.
$$

And since $\gamma\|V-W\|_\infty = 0.5 \cdot 4 = 2$, the contraction bound holds exactly in this example.

What general pattern does this illustrate? The difference between the two transformed functions comes only from the continuation estimate, and that continuation difference is scaled by the discount factor. The reward terms do not contribute to the difference because they are the same in both operator applications.

### Misconception or counterexample block

**Do not confuse “reward is large” with “operator difference is large.”** When comparing $T^\pi V$ and $T^\pi W$, identical reward terms cancel. The difference is controlled by continuation disagreement, not reward magnitude itself.

### Connection to later material

Contraction is what justifies iterative policy evaluation and value iteration. It gives a unique fixed point and explains why repeated Bellman updates converge geometrically in the discounted setting. This same style of reasoning appears broadly in optimization and numerical analysis wherever fixed-point iterations are used.

### Retain / Do not confuse

Retain that Bellman operators are $\gamma$-contractions in the discounted setting, which yields uniqueness of fixed points and convergence of iteration. Do not confuse contraction with monotone improvement of each individual component at every step.

---

## 9. Expectation equations versus optimality equations

### Why this section exists

So far the chapter has evaluated a fixed policy. But the control problem asks a different question: not “how good is this policy?” but “what is the best return achievable from here?” The formulas for those two tasks look similar enough that students often blur them. This section exists to force a clean distinction.

Without this distinction, the reader will misread evaluation equations as if they were already solving control, or misread optimality equations as if they were still averaging under a specified policy.

### The object being introduced

The object is the optimal value function and the Bellman optimality equations. These equations answer the question: if the agent were to act optimally from each point onward, what recursive equations would the best achievable values satisfy?

What is fixed is the environment and the criterion of optimal continuation. What varies are the candidate actions available at each state. The conclusion these equations allow is a recursive characterization of the best achievable long-run value.

### Formal definition

The optimal state-value equation is

$$
V^*(s)=\max_a \sum_{s',r} P(s',r\mid s,a)\bigl[r + \gamma V^*(s')\bigr].
$$

The optimal action-value equation is

$$
Q^*(s,a)=\sum_{s',r} P(s',r\mid s,a)\Bigl[r + \gamma \max_{a'}Q^*(s',a')\Bigr].
$$

### Interpretation paragraph

These equations differ from the policy-evaluation equations in one decisive way. Under a fixed policy, future actions are averaged according to that policy. Under optimal control, future actions are chosen to maximize value. So the role played earlier by the expectation over policy action probabilities is replaced by a maximization.

The first thing to notice is that the two equation families solve different problems. Bellman expectation equations describe the consequences of committing to a specified policy. Bellman optimality equations describe the best consequences achievable when future choices are made optimally.

### Boundary conditions, assumptions, and failure modes

These equations are again exact under the discounted MDP assumptions. However, the move from expectation to maximization changes both the interpretation and the computational challenge. The optimality operator is nonlinear because of the max, even if the expectation operator for a fixed policy is linear in the candidate function.

A frequent failure mode is to think that one can replace the policy average by a max at any time without changing the problem. That would silently turn policy evaluation into control. The distinction must remain sharp.

### Fully worked example

Suppose a state $s$ has two actions. Under action $a_1$, the next reward is $2$ and the next state is always $s_1$. Under action $a_2$, the next reward is $0$ and the next state is always $s_2$. Let $\gamma=0.9$, and suppose the optimal state values of the successor states are already known to be

$$
V^*(s_1)=7, \qquad V^*(s_2)=10.
$$

We want to compute $V^*(s)$.

For action $a_1$, the one-step-plus-optimal-continuation quantity is

$$
2 + 0.9(7)=2+6.3=8.3.
$$

For action $a_2$, the quantity is

$$
0 + 0.9(10)=9.
$$

Now apply the maximization:

$$
V^*(s)=\max\{8.3, 9\}=9.
$$

What does this mean? It means the optimal value of state $s$ is obtained by taking action $a_2$ now and then continuing optimally thereafter. Notice that under a fixed policy that sometimes chooses $a_1$, the state value could be lower than $9$. The optimality equation is not averaging over a policy’s behavior; it is selecting the best continuation.

The general lesson is that expectation equations and optimality equations have similar shapes but fundamentally different roles: one describes a chosen policy, the other describes the best attainable behavior.

### Misconception or counterexample block

**Do not confuse “greedy with respect to current estimates” with “already optimal.”** The optimality equation describes the true optimal values. A greedy choice based on imperfect estimates may be useful algorithmically, but it does not magically make the estimates optimal.

### Connection to later material

The distinction between expectation and optimality equations is central to value iteration, Q-learning, and many control methods. More broadly, it is an instance of a pervasive distinction in decision theory: evaluating a given decision rule versus solving for the best rule.

### Retain / Do not confuse

Retain that Bellman expectation equations evaluate a fixed policy, while Bellman optimality equations describe best achievable continuation through maximization. Do not blur averaging under a policy with maximizing over actions.

---

## 10. The policy-improvement theorem

### Why this section exists

The chapter has now developed the machinery to evaluate a policy and to describe optimality. But there is still a missing bridge: how does one move from one policy to a better one? The policy-improvement theorem supplies that bridge. It formalizes the intuitive idea that if one knows which actions look better under the current policy’s action-value function, then preferring those actions should not make things worse.

This section exists because reinforcement learning is not only about evaluating policies. It is about improving them. The theorem is the first rigorous statement explaining why greedy preference based on $Q^\pi$ is a sensible improvement step.

### The object being introduced

The object is a theorem comparing two policies: a current policy $\pi$ and a new policy $\pi'$ that chooses greedily with respect to $Q^\pi$. It answers the question: if the new policy picks actions that maximize the old policy’s action-value function, what can be guaranteed about the new policy’s state values?

What is fixed is the old policy’s action-value function. What varies is which maximizing action the new policy selects in each state. The conclusion allowed is a statewise no-worse guarantee.

### Formal definition

Suppose policy $\pi'$ is greedy with respect to $Q^\pi$, meaning that for each state $s$, it chooses an action in

$$
\arg\max_a Q^\pi(s,a).
$$

Then the policy-improvement theorem states that

$$
V^{\pi'}(s) \ge V^\pi(s) \qquad \text{for every state } s.
$$

The theorem should be read with the right strength. It proves a **comparison statement**: if a new policy is chosen greedily with respect to the old policy’s action values, then the new policy is at least as good as the old one in the value sense guaranteed by the theorem’s assumptions. What it does **not** prove all by itself is that one greedy step solves the whole control problem in arbitrary approximate settings, or that any empirical improvement heuristic inherits the same guarantee. The theorem is exact, but it is exact under the same clean MDP assumptions that made the Bellman identities exact.

It proves a **statewise monotone improvement guarantee** under the exact assumptions of the theorem. It does not prove that the improved policy is globally optimal after one step unless the old action values already coincide with the optimal ones. It also does not by itself say how $Q^\pi$ was obtained, whether it is exact or approximate, or whether a sample-based learning algorithm using noisy estimates will preserve the same guarantee. Those later algorithmic questions are downstream. The theorem itself is exact, but its scope is exact too.

### Interpretation paragraph

The theorem says that if you start from a policy $\pi$, evaluate it, and then build a new policy that always takes an action that looks best according to $Q^\pi$, the new policy cannot be worse than the old one at any state. This is a powerful monotonicity result. It does not claim immediate optimality. It claims safe improvement.

The first thing to notice is where the theorem begins. It begins with the relation

$$
V^\pi(s)=\sum_a \pi(a\mid s)Q^\pi(s,a).
$$

That expression is a weighted average of the numbers $Q^\pi(s,a)$. A weighted average cannot exceed the maximum of the numbers being averaged. So at the current decision point, the greedy action chosen by $\pi'$ is at least as good as the old policy’s average first action. The theorem then extends that one-step insight to all future decisions by applying the same logic recursively.

### Plausible wrong answer block: what greedy improvement does and does not give

A common overstatement is: "take the greedy policy with respect to $Q^\pi$, and now you have solved the control problem." The exact policy-improvement theorem proves something narrower. It compares the original policy $\pi$ with a policy that is greedy with respect to the relevant value function under the theorem's assumptions. The conclusion is an **improvement or non-degradation statement**, not an automatic proof that the greedy policy is globally optimal after one step in every approximate setting.

Why does this matter? Because in practical algorithms the value estimates are often noisy or approximate. Greedification with respect to an imperfect estimate can still be useful, but the theorem's exact guarantee lives at the level of the exact object it names. The theorem is powerful. It is not a blank permission slip to overclaim what approximate code is doing.

### Boundary conditions, assumptions, and failure modes

The theorem assumes exact evaluation of $Q^\pi$ in the underlying MDP setting. In approximate settings, greedy improvement based on imperfect value estimates may fail to be monotone without additional conditions.

Another important boundary line is that the theorem does not say the greedy policy is optimal after one step. It says only that it is no worse than the current policy. Equality can occur; strict improvement is not guaranteed everywhere.

A common failure mode is to assume that if one greedy step helps, then greedy behavior with respect to any rough estimate must also help. That is not what the exact theorem says.

### Fully worked example

Suppose at some state $s$, the current policy $\pi$ chooses among three actions with probabilities

$$
\pi(a_1\mid s)=0.5, \qquad \pi(a_2\mid s)=0.3, \qquad \pi(a_3\mid s)=0.2,
$$

and suppose

$$
Q^\pi(s,a_1)=4, \qquad Q^\pi(s,a_2)=7, \qquad Q^\pi(s,a_3)=1.
$$

First compute the current state value using the policy average:

$$
V^\pi(s)=0.5(4)+0.3(7)+0.2(1)=2+2.1+0.2=4.3.
$$

Now identify the greedy action with respect to $Q^\pi$. The maximum action value is $7$, achieved by $a_2$. So a greedy improved policy $\pi'$ would choose $a_2$ at state $s$.

At the first decision step, this means the new policy’s chosen action has value

$$
Q^\pi(s,a_2)=7,
$$

which is greater than the old policy’s average first-step value $4.3$. This verifies the initial inequality

$$
V^\pi(s) \le \max_a Q^\pi(s,a).
$$

Why does this matter for the full theorem rather than just the first action? Because once the new policy reaches the next state, it again chooses actions that are at least as good relative to the old policy’s action values. Repeating that logic over future time steps yields the statewise improvement guarantee.

The general lesson is that policy improvement starts from a simple numerical fact about averages and maxima, then extends it recursively through the dynamics.

### Misconception or counterexample block

**Do not confuse “greedy with respect to $Q^\pi$” with “greedy with respect to $Q^{\pi'}$.”** The theorem compares a new policy to the old one using the old policy’s action-value function as the reference object. That distinction matters in the proof logic.

**Do not say “one greedy step makes the policy optimal.”** It may improve the policy, but repeated evaluation and improvement are what drive convergence toward optimality.

### Connection to later material

The policy-improvement theorem is the core logical engine behind policy iteration and many control algorithms. More broadly, it illustrates a common pattern in optimization: evaluate the current object, construct a locally improved object using the evaluation, then repeat.

### Retain / Do not confuse

Retain that a policy greedy with respect to $Q^\pi$ is guaranteed to be no worse than $\pi$ state by state under the exact theorem. Do not confuse monotone improvement with one-step optimality.

---

## 11. Generalized policy iteration

### Why this section exists

The chapter has now developed two complementary processes: policy evaluation and policy improvement. In actual reinforcement learning and dynamic programming, these processes are rarely isolated permanently. They interact. Generalized policy iteration is the name for that interaction. This section exists to show the larger structural pattern into which policy evaluation and policy improvement fit.

Without this structural view, individual algorithms can look unrelated even when they are built from the same basic alternating logic.

### The object being introduced

The object is not one particular algorithm but a template: repeatedly estimate how good the current policy is, then use that estimate to make the policy better, then repeat. The evaluation step can be exact or approximate, full or partial. The improvement step can also be exact or approximate, greedy or softly greedy. What matters is the coupling.

What is fixed is the high-level loop. What varies are the specific computational choices inside the evaluation and improvement subroutines. The conclusion this concept allows is a unified view of many seemingly different control algorithms.

### Formal definition

Generalized policy iteration consists of repeated interaction between:

1. **Policy evaluation**: estimate or compute the value of the current policy.
2. **Policy improvement**: use those value estimates to choose better actions or a better policy.

### Interpretation paragraph

The central idea is structural rather than procedural detail. Evaluation answers, “How good is the policy I currently have?” Improvement answers, “Given what I now know, how should I change the policy?” In generalized policy iteration, these two questions are not answered once each. They are answered over and over, often interleaved.

The first thing to notice is that the two processes need not wait for each other to finish completely. Classical policy iteration performs near-complete evaluation before improvement. Value iteration blends the two more tightly. Actor–critic methods also fit the same high-level pattern, although the computational form is different. The concept is broad because the structural interplay, not the exact implementation, is what matters.

### Boundary conditions, assumptions, and failure modes

The guarantees of particular generalized policy iteration schemes depend on the accuracy of evaluation, the form of improvement, and the assumptions of the problem class. The broad concept itself does not imply that every approximate version converges under all conditions.

A common failure mode is to think generalized policy iteration is a single algorithm with one precise schedule. It is better understood as a family resemblance across algorithms built from the same evaluation-improvement feedback loop.

### Fully worked example

Suppose an agent starts with a policy $\pi_0$ in a small MDP. After exact evaluation, it computes the state-action values $Q^{\pi_0}$ and constructs a greedy improved policy $\pi_1$. That is the first evaluation-improvement cycle.

Now suppose the agent evaluates $\pi_1$ only partially rather than to full exactness, obtaining an estimate that is good enough to identify clearly better actions in several states. It then updates to another policy $\pi_2$ using those partial values. This still fits the generalized policy iteration template because the structural pattern remains the same: value information is being used to alter the policy, and the altered policy changes the value information needed next.

What the reader should see in this example is that the stopping point of evaluation may change without changing the structural loop itself. The current policy is assessed strongly enough to say something action-relevant about its behavior. That assessment is then used to prefer better actions. Once the policy changes, a new evaluation problem is created, because the value information needed next is now tied to the new policy rather than the old one. The invariant is therefore not “evaluate to completion.” The invariant is the alternation: value information shapes policy, and changed policy creates the next value problem.

The general lesson is that many RL control algorithms are variations on this same alternating structure.

### Misconception or counterexample block

**Do not confuse generalized policy iteration with classical policy iteration.** Classical policy iteration is one specific member of the family. Generalized policy iteration is the broader template that includes many exact and approximate control methods.

### Connection to later material

This concept will help organize later chapters on temporal-difference control, Q-learning, actor–critic methods, and approximate dynamic programming. When algorithms start to look different on the surface, generalized policy iteration reveals the common skeleton underneath.

### Retain / Do not confuse

Retain that generalized policy iteration is the repeated interplay between evaluation and improvement, not one single fixed algorithm. Do not confuse the broad structural template with one particular implementation schedule.

---

## 12. Common confusions this chapter is designed to block

### Why this section exists

This section is a consolidation device, not a repair device. The earlier sections should already have made the core distinctions intelligible. The purpose here is to stabilize them by placing the most easily blurred pairs side by side one last time.

### Confusion 1: $V^\pi$ and $Q^\pi$ are just different notations for the same thing

No. They condition on different information. $V^\pi(s)$ conditions on the current state and lets the policy choose the action. $Q^\pi(s,a)$ conditions on both the current state and a forced current action.

### Confusion 2: the first recursive equation you see is automatically a Bellman equation

No. The return recursion

$$
G_t=R_{t+1}+\gamma G_{t+1}
$$

is an identity about return itself. Bellman equations arise after placing that identity inside conditional expectations and using the MDP structure.

### Confusion 3: Bellman equations are approximate by nature

Not in this chapter. Here they are exact identities under the MDP assumptions. Approximate Bellman-style targets appear later when expectations are replaced by sampled or approximate quantities.

### Confusion 4: the Bellman operator is just notation fluff

No. The operator viewpoint reveals the fixed-point structure and makes contraction and convergence arguments possible in a transparent way.

### Confusion 5: policy improvement means greediness instantly yields optimality

No. The theorem gives a no-worse guarantee relative to the current policy under exact evaluation. It does not say one greedy step reaches optimality.

### Retain / Do not confuse

Retain that most major errors in this chapter come from collapsing distinctions that must remain separate. Do not confuse similar-looking formulas that answer different questions.

---

## 13. What this chapter now entitles you to do

### Why this section exists

A good chapter should end by clarifying what new mathematical moves the reader is now licensed to make. This is not mere summary. It is a statement of capability. The reader should leave not only with formulas remembered, but with a clear sense of which reasoning steps are now justified.

### What you can now conclude

After mastering this chapter, you should be able to do the following with full control.

First, you can define state value, action value, and advantage as conditional expectations of return and interpret precisely what information is fixed in each.

Second, you can explain why the state value is the policy-weighted average of action values at a state.

Third, you can derive Bellman expectation equations by starting from the return recursion, then conditioning and splitting on the next random variables in the correct order.

Fourth, you can distinguish evaluation equations from optimality equations and identify exactly where averaging is replaced by maximization.

Fifth, you can treat Bellman equations as fixed-point equations of Bellman operators and understand why contraction implies unique fixed points and convergence of iteration in discounted settings.

Sixth, you can state and interpret the policy-improvement theorem without overstating it.

Seventh, you can recognize generalized policy iteration as the broad evaluation-improvement structure behind many control algorithms.

### Connection to later material

These capabilities are the foundation for dynamic programming algorithms, temporal-difference learning, value iteration, Q-learning, actor–critic methods, and approximate control. More abstractly, they train the habit of seeing a long-run decision problem as a recursive fixed-point problem.

### Retain / Do not confuse

Retain that the point of the chapter is not to memorize Bellman equations in isolation, but to understand the chain of reasoning that makes them exact, interpretable, and useful. Do not move on while the difference between definition, exact identity, and approximation remains blurry.

---

### Recover-the-reasoning checkpoint

Be able to explain the following chain in complete sentences.

The return identity is a statement about one random variable. A Bellman expectation equation is obtained when a value function is defined as a conditional expectation of that return under suitable Markov structure and policy conditioning. A Bellman operator is a map that takes a candidate function and returns a new function by applying the right-hand side of the Bellman equation. An algorithmic update is a computational procedure that tries, exactly or approximately, to move a representation toward a fixed point of such a relation.

If you answer an exam question about any one of those four levels using the language of another, you may sound advanced while still being wrong.

## 14. Mastery check

A serious reader should be able to answer each of the following in full sentences, with the relevant assumptions and distinctions made explicit.

1. What exactly is fixed in $V^\pi(s)$, and what exactly is fixed in $Q^\pi(s,a)$?
2. Why is $V^\pi(s)$ an average over action values rather than a maximum over them under a fixed policy?
3. In the derivation of the Bellman expectation equation for $V^\pi$, what is substituted first, and what random quantities are then split on, in what order?
4. What exact recognition step turns the continuation term into $V^\pi(s')$?
5. Why is the return recursion not yet a Bellman equation?
6. What does the Bellman operator do to a candidate value function, and what does it mean for the true value function to be a fixed point?
7. Why does the contraction inequality keep the factor $\gamma$ and not something larger?
8. What is the exact conceptual difference between evaluating a fixed policy and solving for the optimal value function?
9. What does the policy-improvement theorem prove, and what does it leave open?
10. How does generalized policy iteration unify policy iteration, value iteration, and later approximate control methods at the structural level?

If any answer feels fuzzy, the best next step is not speed. It is repair. This chapter is one of the main load-bearing chapters in reinforcement learning. Later algorithms make much more sense when these objects and distinctions are stable.
