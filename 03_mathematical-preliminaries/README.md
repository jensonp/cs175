# Chapter 3 — Mathematical Preliminaries

*Rewritten as mastery-oriented teaching notes from the source chapter at the linked repository directory, following the uploaded writing standard.*

## What this chapter is for

Before reinforcement learning can talk about value functions, Bellman equations, trajectory objectives, or policy gradients, it needs a stable language for uncertainty. That language is probability. The purpose of this chapter is not to collect probability formulas as isolated facts. The purpose is to install a small number of mathematical objects so solidly that later derivations stop feeling ceremonial and start feeling inevitable.

### Adversarial reading rule for this chapter

In this chapter, a formula is not yet understood if you can reproduce its symbols but cannot answer three hostile questions. **What is the random object?** **Under which probability law is the expectation taken?** **What is being held fixed when the expression is conditioned or differentiated?** Many later reinforcement-learning mistakes are not algebra mistakes. They are object mistakes: the student averages over the wrong thing, conditions on the wrong sigma-field in informal language, or differentiates with respect to parameters that do not actually appear in the law being used.

There are three recurring questions behind almost everything that follows in reinforcement learning. First, what random quantity are we talking about? Second, with respect to which probability law are we averaging? Third, what information is being held fixed when we condition? If those questions are handled sloppily, later notation becomes unreadable. If they are handled well, value functions become conditional expectations, Bellman equations become repeated applications of expectation identities, and policy-gradient formulas become careful manipulations of trajectory probabilities rather than mysterious tricks.

This chapter therefore does foundational work. It introduces expectation, conditional expectation, and the laws that let expectations be decomposed. It then moves to the return random variable, explains why its indexing is the way it is, and checks the conditions under which infinite discounted return is mathematically meaningful. Finally, it lifts the discussion from single random variables to whole trajectories and shows how trajectory probabilities are written, differentiated, and converted into expectation-friendly forms.

The chapter is written in a discrete finite-or-countable setting whenever sums are shown explicitly. That choice is made for transparency. The ideas themselves are not confined to discrete spaces, but the discrete setting lets the reader see exactly what is being averaged and exactly where each factor in a formula comes from.

One three-way distinction should be fixed before the formal sections begin. Some expressions in this chapter are **notation choices**: they tell you how an already defined object is indexed or written. Some expressions are **probability-structure statements**: they tell you what law governs a random object, such as a return, a conditional distribution, or a trajectory. Some later expressions are **proof tools or transformations**: they do not introduce a new object, but change the form of an expression in a way justified by calculus or expectation identities. These three categories should not be collapsed. Writing $R_{t+1}$ instead of $R_t$ is not the same kind of act as factorizing a trajectory probability, and factorizing a trajectory probability is not the same kind of act as applying the log-derivative identity to that factorized law.

Before the chapter begins its formal sections, lock one three-part distinction that will matter repeatedly later.

First, some expressions in this chapter are **notation choices**. They tell you how an object is indexed or written. Second, some expressions are **probability-structure claims**. They say what random variable exists, what law it is distributed under, or what conditioning event is being held fixed. Third, some expressions are **proof tools**. They are legal manipulations that follow from the previous probability structure once the relevant assumptions hold.

These layers must not be collapsed. A notational convention such as writing $R_{t+1}$ instead of $R_t$ is not merely aesthetic; it reflects the event order from the previous chapter. A conditional expectation is not merely notation; it changes the probability law under which the average is taken. A move such as applying the law of total expectation or differentiating a log-factorized trajectory law is not “just rewriting”; it is a justified transformation that depends on assumptions already being in place. If the reader keeps those three layers separate, the later derivations become much harder to misread.

---

## 1. Standing assumptions

### Why this section exists

A later derivation is only as good as the assumptions that support it. In reinforcement learning, it is extremely easy to write a string of symbols that *looks* like mathematics while quietly relying on unspoken regularity conditions. This section appears first because the chapter cannot responsibly define infinite discounted return, condition on random quantities, or differentiate expectations unless the relevant assumptions are visible from the beginning.

### The object being introduced

The object here is not a single formula but a framework of admissibility. These assumptions specify what kind of spaces we are working on, what boundedness conditions are present, what discounting regime is allowed in continuing tasks, and what regularity is required when a derivative is moved through a sum. What is fixed in this section are the mathematical rules of the game. What varies later are the random variables, trajectories, and policies built inside that framework.

### Formal statement of the standing assumptions

Throughout this chapter, when a formula is written as a sum over states, actions, rewards, or trajectories, assume the relevant space is finite or countable.

When continuing tasks are discussed, assume rewards are bounded almost surely by some constant $R_{\max} \ge 0$:

$$
|R_t| \le R_{\max}
$$

for every relevant time index $t$.

When infinite discounted return is used in a continuing task, assume

$$
0 \le \gamma < 1.
$$

When expectations over finite-horizon trajectories are differentiated with respect to policy parameters $\theta$, assume a finite horizon $T$, a differentiable parameterized policy $\pi_\theta$, and enough regularity to justify interchanging derivative and summation.

### Interpretation

These assumptions are not decorative. Each one blocks a specific failure mode. Countability makes the written sums literal. Bounded rewards prevent a single reward term from exploding. The condition $\gamma < 1$ makes the geometric weights decay, which is what controls the infinite tail of future rewards. Finite horizon and regularity are what make trajectory differentiation legal rather than aspirational.

The important thing to notice is the order of dependence. Later objects such as $G_t$, $V^\pi(s)$, and expected trajectory objectives do not stand on their own. They inherit their legitimacy from assumptions like these.

### Boundary conditions, assumptions, and failure modes

If the state or action space is continuous, sums must be replaced by integrals, and probabilities by densities where appropriate. The logic often survives, but the notation and technical checks change.

If rewards are unbounded, the infinite discounted sum may still converge in some cases, but boundedness can no longer be invoked as a simple global control argument.

If $\gamma = 1$ in a genuinely infinite-horizon continuing task, the return may diverge or fail to be absolutely summable unless additional structure is added, such as finite termination almost surely or stronger integrability conditions.

If one differentiates an expectation over trajectories without checking regularity, the result may be formally suggestive but unjustified. The point is not that every subtle theorem must be re-proved here. The point is that one should know exactly which move requires justification.

### Fully worked example

Consider a continuing task in which rewards satisfy $|R_t| \le 2$ almost surely and the discount factor is $\gamma = 0.9$. The first thing to check is whether the infinite discounted return from time $t$ even has a chance to be controlled:

$$
G_t = \sum_{k=0}^{\infty} 0.9^k R_{t+k+1}.
$$

At each index $k$, the magnitude of the reward term is at most $2$, so the magnitude of the weighted term is at most $2 \cdot 0.9^k$. That gives

$$
|G_t| \le \sum_{k=0}^{\infty} 2 \cdot 0.9^k.
$$

Now the question becomes purely geometric: does the series $\sum_{k=0}^{\infty} 0.9^k$ converge? Yes, because the common ratio is strictly less than $1$. Therefore

$$
|G_t| \le 2 \sum_{k=0}^{\infty} 0.9^k = 2 \cdot \frac{1}{1-0.9} = 20.
$$

The conclusion is not merely numerical. The conclusion is that the return random variable is uniformly bounded by $20$, so taking expectations of it is mathematically respectable under these assumptions.

The general lesson is that before asking what the return *means*, one must first verify that the return is a well-defined random quantity. In future problems, always check: what controls the magnitudes, and what controls the tail?

### Misconception block

**Do not confuse a convenient assumption with an empty assumption.** Bounded rewards and $\gamma<1$ are often presented so routinely that students stop noticing what they do. They are exactly the mechanism that makes the infinite discounted sum manageable in the standard continuing setting.

### Connection to later material

These standing assumptions are used repeatedly in the rest of the chapter. They justify why discounted return can be defined, why expectations of return are meaningful, and why policy-gradient manipulations over finite-horizon trajectory laws can be carried out. Later chapters may weaken or modify these assumptions, but not by ignoring them.

### Retain / Do not confuse

Retain the fact that every later derivation lives inside explicit assumptions. Do not confuse “standard assumptions” with “irrelevant assumptions.” Standard only means common, not optional.

---

## 2. Random variables and what expectation does

### Why this section exists

The next chapters will define value functions as expectations of return. That sounds simple only if expectation itself is already conceptually stable. Many students carry an informal sense that expectation means “average,” but that informal sense is too weak for later derivations. This section exists to pin down exactly what expectation averages over and what information is required to define it.

### The object being introduced

The central object is a random variable $X$. A random variable is a numerical summary assigned to outcomes of an underlying random experiment. What matters here is that $X$ can take different values, and those values are weighted by probabilities. Expectation is the operation that combines the possible values of $X$ with their probabilities to produce a probability-weighted average.

What is fixed in the expectation formula is the probability law of $X$. What varies are the possible values that $X$ can take. The conclusion expectation allows is not “what will happen on a single trial,” but “what average value is implied by the full distribution of possibilities.”

### Formal definition

Let $X$ be a discrete random variable taking values in a finite or countable set $\mathcal{X}$. Then

$$
\mathbb{E}[X] = \sum_{x \in \mathcal{X}} x\,P(X=x),
$$

provided the sum is well-defined.

More generally, for any function $g(X)$ for which the sum exists,

$$
\mathbb{E}[g(X)] = \sum_{x \in \mathcal{X}} g(x)\,P(X=x).
$$

### Interpretation

Expectation is not the value that is “most likely” to happen, and it is not the value that *must* occur. It is the center of mass of the distribution when each possible value is weighted by how likely it is. The formula has two indispensable components: the values themselves and the probability weights attached to those values. Remove either one, and the expectation is no longer determined.

When reading the formula, notice what varies and what does not. The symbol $x$ is the running value in the sum. The probability law $P(X=x)$ supplies the weights. The sum sweeps through every possible value of $X$, multiplies value by weight, and aggregates the result.

### Boundary conditions, assumptions, and failure modes

Expectation may fail to exist if the positive and negative tails are not summable in an appropriate sense. In this chapter, the examples are controlled so that existence is not a problem, but it is important not to internalize the false rule that every random variable automatically has a finite expectation.

Another common failure mode is to treat expectation as if it were defined from observed samples alone. Sample averages can estimate expectations, but the mathematical definition of expectation is with respect to a probability law, not a finite dataset.

### Fully worked example

Suppose an action in a simple environment leads to a one-step reward $X$ taking values $-1$, $0$, and $3$ with probabilities $0.2$, $0.5$, and $0.3$, respectively. We want to compute $\mathbb{E}[X]$.

First identify the object: the random variable is the reward itself. Its possible values are fixed as the set $\{-1,0,3\}$. The varying part in the sum is which of those values is being considered at a given step.

Now apply the definition:

$$
\mathbb{E}[X] = (-1)(0.2) + (0)(0.5) + (3)(0.3).
$$

Compute each contribution separately. The value $-1$ contributes $-0.2$ because it occurs with probability $0.2$. The value $0$ contributes nothing because multiplying by zero removes its term. The value $3$ contributes $0.9$ because it occurs with probability $0.3$.

Adding the contributions gives

$$
\mathbb{E}[X] = -0.2 + 0 + 0.9 = 0.7.
$$

The final interpretation is that the probability-weighted average reward is $0.7$. This does **not** mean the reward will usually equal $0.7$; in fact $0.7$ is not even one of the possible realized rewards. It means that across repeated draws from this distribution, the average reward settles around $0.7$.

The general lesson is that expectation is about the whole distribution, not about a typical single sample. In future problems, always ask: what are the possible values, and what are their weights?

### Misconception block

**Do not confuse expectation with the most probable outcome.** In the example above, the most probable reward is $0$, because it has probability $0.5$. The expectation is $0.7$. Those are different questions. One asks which value occurs most often; the other asks for the probability-weighted average over all values.

### Connection to later material

A value function in reinforcement learning is simply an expectation of a return random variable, often conditioned on state or state-action information. If expectation is understood at this level, then value functions stop feeling like new mystical objects and become familiar probabilistic constructions.

### Retain / Do not confuse

Retain that expectation averages over possible values using probability weights. Do not confuse expectation with a sample average, the most likely value, or a guarantee about a single realization.

---

## 3. Conditional expectation

### Why this section exists

Expectation alone is not enough for reinforcement learning. Value functions are not unconditional averages over every possible future from every possible circumstance. They are averages **given** current information, such as the current state or state-action pair. This section appears now because the moment one asks, “What is the expected return if the agent is currently in state $s$?” conditioning has entered the picture.

### The object being introduced

The object is conditional expectation, written as $\mathbb{E}[X \mid Y=y]$. It is still an expectation of the same random variable $X$, but now computed after holding fixed the information that $Y=y$. What is fixed is the conditioning event. What varies are the possible values of $X$ and their conditional probabilities under that event.

The role of conditional expectation is to update the weighting of possibilities when some information has been revealed. It answers the question: once we know $Y=y$, what is the probability-weighted average value of $X$?

### Formal definition

If $X$ and $Y$ are discrete random variables, then for any value $y$ with $P(Y=y)>0$,

$$
\mathbb{E}[X \mid Y=y] = \sum_x x\,P(X=x \mid Y=y).
$$

More generally, for a function $g(X)$,

$$
\mathbb{E}[g(X) \mid Y=y] = \sum_x g(x)\,P(X=x \mid Y=y).
$$

### Interpretation

Conditioning does not create new possible values of $X$. It changes the probability weights attached to the existing values of $X$ after the event $Y=y$ has been declared true. That distinction is essential. The numerical outcomes available to $X$ are the same kind of outcomes as before. What changes is the distribution because some worlds are no longer compatible with the information being held fixed.

When reading $\mathbb{E}[X \mid Y=y]$, the right way to hear it is: “average the values of $X$, but do so inside the smaller universe in which $Y=y$ has happened.”

### Boundary conditions, assumptions, and failure modes

The conditional expectation given $Y=y$ requires that the event $Y=y$ have positive probability in the discrete setting. If $P(Y=y)=0$, the elementary formula using conditional probabilities is not directly available.

A major failure mode is to think that conditioning changes the definition of the random variable. It does not. Conditioning changes the law under which the same variable is being averaged.

Another failure mode is to forget what is fixed. In $\mathbb{E}[X\mid Y=y]$, the value $y$ is fixed. If one writes $\mathbb{E}[X\mid Y]$, then the result is itself a random variable depending on the realized value of $Y$.

### Fully worked example

Suppose the weather variable $Y$ can be either sunny or rainy, and let the reward variable $X$ represent the payoff from taking an outdoor action. Under sunny weather, the reward is $2$ with probability $0.8$ and $-1$ with probability $0.2$. Under rainy weather, the same reward variable has a different conditional law: it equals $2$ with probability $0.1$ and $-1$ with probability $0.9$. We want to compute $\mathbb E[X\mid Y=\text{sunny}]$ and $\mathbb E[X\mid Y=\text{rainy}]$. The important sentence-level discipline here is that the random variable being averaged never changes; what changes is the law under which it is averaged.

Start with the sunny case. The object being averaged is still $X$, the reward. What changes is that we now restrict attention to the conditional law under sunny weather. The possible values of $X$ remain $2$ and $-1$.

Apply the conditional expectation formula:

$$
\mathbb{E}[X \mid Y=\text{sunny}] = 2(0.8) + (-1)(0.2) = 1.6 - 0.2 = 1.4.
$$

Now do the rainy case:

$$
\mathbb{E}[X \mid Y=\text{rainy}] = 2(0.1) + (-1)(0.9) = 0.2 - 0.9 = -0.7.
$$

The interpretation is direct. The same action has different expected reward depending on the information being held fixed. Nothing about the reward variable itself changed. What changed was the probability law after conditioning on weather.

The general lesson is that conditional expectation is the correct language whenever the question includes phrases like “given the current state,” “given the chosen action,” or “given the observed history.”

### Misconception block

**Do not confuse “conditioning on $Y=y$” with “redefining $X$.”** The values $2$ and $-1$ were possible in both cases. What changed was how much probability mass each value received once weather was specified.

### Connection to later material

This is exactly the structure of value functions. A state-value function is an expectation of return conditional on the present state. An action-value function is an expectation of return conditional on both present state and chosen action. Without stable understanding of conditional expectation, those objects are easily misread.

### Retain / Do not confuse

Retain that conditioning changes probability weights, not the underlying meaning of the variable being averaged. Do not confuse $\mathbb{E}[X\mid Y=y]$, which is a number for fixed $y$, with $\mathbb{E}[X\mid Y]$, which is a random variable.

---

## 4. The law of total expectation

### Why this section exists

Once conditional expectation is available, the next question is how to move between conditional and unconditional viewpoints. Reinforcement-learning derivations repeatedly split the future according to one more random event: the next action, next state, next reward, or a joint one-step outcome. The chapter cannot proceed to Bellman-style reasoning without the identity that licenses that split.

### The object being introduced

The object is the law of total expectation. It tells us how to recover an overall expectation of $X$ by first conditioning on cases indexed by another random variable $Y$, computing the conditional expectation inside each case, and then averaging those case-specific expectations using the probabilities of the cases.

What is fixed is the partition of the world induced by $Y$. What varies is which case $Y=y$ one is inside. The conclusion this law allows is that an expectation can be computed in stages.

### Formal statement

For discrete random variables $X$ and $Y$,

$$
\mathbb{E}[X] = \sum_y P(Y=y)\,\mathbb{E}[X \mid Y=y],
$$

provided the expectations are well-defined.

### Interpretation

This identity says that to compute the overall expected value of $X$, one may first divide the world into cases using $Y$, then compute the expected value of $X$ inside each case, and finally take the weighted average of those case-level expectations. It is an accounting rule. Nothing mysterious is being created; the same total expectation is being reorganized by cases.

The reader should notice that the weights in the outer sum are the probabilities of the cases themselves, while the inner expectations are the average values of $X$ once each case is fixed.

### Boundary conditions, assumptions, and failure modes

The cases indexed by $Y$ must cover the possibilities in the way the law assumes. In the discrete setting shown here, that means summing over all possible values of $Y$.

A common overgeneralization is to use the law mechanically without checking what variable actually partitions the uncertainty relevant to the calculation. The law is powerful precisely because it lets you choose a useful case split, but not every split simplifies the problem.

### Fully worked example

Return to the weather-reward example, but now suppose

$$
P(Y=\text{sunny}) = 0.6, \qquad P(Y=\text{rainy}) = 0.4.
$$

From the previous section, we already know

$$
\mathbb{E}[X \mid Y=\text{sunny}] = 1.4, \qquad \mathbb{E}[X \mid Y=\text{rainy}] = -0.7.
$$

We now want the unconditional expectation $\mathbb{E}[X]$.

The law of total expectation tells us to average the conditional expectations using the probabilities of the weather cases:

$$
\mathbb{E}[X] = P(Y=\text{sunny})\,\mathbb{E}[X\mid Y=\text{sunny}] + P(Y=\text{rainy})\,\mathbb{E}[X\mid Y=\text{rainy}].
$$

Substitute the known values:

$$
\mathbb{E}[X] = (0.6)(1.4) + (0.4)(-0.7).
$$

Compute each term:

$$
(0.6)(1.4)=0.84, \qquad (0.4)(-0.7)=-0.28.
$$

Add them:

$$
\mathbb{E}[X]=0.84-0.28=0.56.
$$

The interpretation is that the overall expected reward is $0.56$, obtained by combining the good-weather and bad-weather expected rewards according to how often each weather condition occurs.

The general lesson is that if a later RL derivation splits on the next state or next action, it is doing the same structural move. The variable defining the cases may change, but the logic does not.

### Misconception block

**Do not think the law of total expectation introduces approximation.** It is an exact identity, not a heuristic. If used correctly, it gives the same expectation, merely organized by cases.

### Connection to later material

Bellman equations are built from exactly this principle. A conditional expectation of return is split according to what happens at the next step, and the resulting case-wise contributions are recombined. Once you see that, Bellman recursions look like probability bookkeeping rather than inspired guesswork.

### Retain / Do not confuse

Retain that the law of total expectation computes a global expectation by averaging case-specific expectations. Do not confuse the outer weights $P(Y=y)$ with the inner conditional probabilities used inside $\mathbb{E}[X\mid Y=y]$.

---

## 5. Tower property and nested conditioning

### Why this section exists

The law of total expectation shows that expectations can be taken in stages. The next refinement is to understand what happens when conditioning itself is nested. Recursive equations in reinforcement learning often contain expressions where one first conditions on richer information and then averages back to coarser information. This section exists because that staged structure is the mathematical backbone of recursive reasoning.

### The object being introduced

The object is the tower property, also called iterated expectation. It formalizes the idea that when one conditions on detailed information and then averages back to a coarser level of information, the result is the same as conditioning directly on the coarser information.

What is fixed is the hierarchy of information: one level is finer, one is coarser. What varies is which specific information set is being conditioned on at a given stage. The conclusion it allows is that nested expectations can often be collapsed without changing the quantity being computed.

### Formal statement

In discrete intuition, if $Z$ is coarser information than $(Y,Z)$, then

$$
\mathbb{E}[\mathbb{E}[X\mid Y,Z] \mid Z] = \mathbb{E}[X\mid Z].
$$

A particularly common special case is

$$
\mathbb{E}[\mathbb{E}[X\mid Y]] = \mathbb{E}[X].
$$

### Interpretation

The inner expectation computes the average of $X$ using more detailed information. The outer expectation then averages those refined values across the finer distinctions that are not retained at the coarser level. No information is mishandled if the conditioning hierarchy is respected, so the final answer agrees with the direct coarser conditional expectation.

The important thing to notice is that this is not an algebraic cancellation rule for symbols with brackets. It is a rule about information structure.

### Boundary conditions, assumptions, and failure modes

The finer conditioning must actually contain at least as much information as the coarser conditioning. One cannot arbitrarily delete or swap conditioning variables and expect the identity to remain valid.

Another failure mode is to treat the tower property as if it licenses dropping conditioning because it feels inconvenient. The information being averaged out must be averaged out in the correct order.

### Fully worked example

Suppose $Z$ is the current state class of an agent, taking values safe or risky. Inside each class there is a finer variable $Y$ describing an observed signal. Let $X$ be the eventual one-step reward.

Assume that when $Z=\text{safe}$, the signal $Y$ can be green or yellow with probabilities $0.7$ and $0.3$, and

$$
\mathbb{E}[X \mid Y=\text{green}, Z=\text{safe}] = 5,
$$
$$
\mathbb{E}[X \mid Y=\text{yellow}, Z=\text{safe}] = 1.
$$

We want $\mathbb{E}[X \mid Z=\text{safe}]$.

The tower property says that we may first compute the inner conditional expectations at the finer level and then average them using the probabilities of the signal values within the safe class:

$$
\mathbb{E}[X \mid Z=\text{safe}] = \mathbb{E}[\mathbb{E}[X\mid Y,Z] \mid Z=\text{safe}].
$$

So,

$$
\mathbb{E}[X \mid Z=\text{safe}] = (0.7)(5) + (0.3)(1) = 3.5 + 0.3 = 3.8.
$$

What was checked here? First, that $Y$ is finer information inside the already fixed condition $Z=\text{safe}$. Second, that the probabilities $0.7$ and $0.3$ are the conditional probabilities of the finer cases within that coarser class. Third, that the inner expectations are values of the same random variable $X$ under more refined information.

The final interpretation is that the safe-class conditional reward can be obtained by first resolving the signal-level cases and then averaging back. That is exactly how recursive expectations are often computed in RL.

### Misconception block

**Do not confuse the tower property with the claim that conditioning never matters.** Conditioning matters enormously. The tower property says only that if you condition on richer information and then average back correctly, you recover the coarser conditional expectation.

### Connection to later material

This identity is one of the quiet structural reasons Bellman-style recursion is legal. One-step expansions often condition on richer future information and then compress back to state-level or state-action-level quantities.

### Retain / Do not confuse

Retain that nested conditioning is about information levels, not symbol cancellation. Do not confuse “more detailed first, then average back” with arbitrary deletion of conditioning terms.

---

## 6. Return and its indexing

### Why this section exists

Reinforcement learning is centered on future cumulative reward. The object that represents that cumulative future is the return. Students often memorize its formula while remaining uncertain about why the first reward is indexed $R_{t+1}$ instead of $R_t$, why the discount exponent starts at zero, or what exactly the summation index is tracking. This section exists to make every index in the return formula intelligible.

### The object being introduced

The object is the discounted return from time $t$, denoted $G_t$. It is a random variable built from future rewards. What is fixed is the starting decision time $t$. What varies are the future step offsets $k=0,1,2,\dots$. The role of $G_t$ is to summarize the entire future reward stream beginning immediately *after* the decision at time $t$.

The indexing here is not arbitrary. The return from time $t$ starts with $R_{t+1}$ because Chapter 2 already fixed the event order: the decision at time $t$ chooses $A_t$, and only after the environment reacts does the next reward become available. So the return notation is carrying causal structure forward, not inventing a fresh convention inside probability notation.

### Formal definition

For a continuing task,

$$
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}.
$$

### Interpretation

The formula begins with $R_{t+1}$ because at time $t$ the agent chooses action $A_t$, and the first reward resulting from that choice is observed only after the environment transitions. So the return from time $t$ starts with the next reward, not the current index reward.

The summation index $k$ measures how far into the future the reward lies relative to time $t$. When $k=0$, the term is the first post-decision reward $R_{t+1}$. When $k=1$, it is the second post-decision reward $R_{t+2}$. The exponent on $\gamma$ is also $k$, because the reward that is $k+1$ steps after the decision time receives exactly $k$ rounds of discounting relative to the first post-decision reward.

### Boundary conditions, assumptions, and failure modes

The infinite sum only makes sense under conditions such as bounded rewards and $0 \le \gamma <1$ in the standard continuing setting. Those conditions are not repeated in every line of notation, but they are what make the object legitimate.

A common failure mode is index drift: writing the reward term and discount exponent out of sync. Another is to think $R_t$ belongs in $G_t$ by default. In the standard post-decision convention, it does not.

### Fully worked example

Suppose $\gamma = 0.5$ and a particular realized future reward sequence from time $t$ onward is

$$
R_{t+1}=4, \quad R_{t+2}=-2, \quad R_{t+3}=6, \quad R_{t+4}=0,
$$

and all later rewards are zero. Then

$$
G_t = \sum_{k=0}^{\infty} 0.5^k R_{t+k+1}
$$

reduces in this realization to

$$
G_t = 0.5^0 R_{t+1} + 0.5^1 R_{t+2} + 0.5^2 R_{t+3} + 0.5^3 R_{t+4}.
$$

Substitute the reward values:

$$
G_t = 1\cdot 4 + 0.5(-2) + 0.25(6) + 0.125(0).
$$

Now compute the discounted contribution of each realized reward in order. The first post-decision reward is multiplied by $1$ and therefore contributes $4$. The second reward is multiplied by $0.5$ and therefore contributes $-1$. The third reward is multiplied by $0.25$ and therefore contributes $1.5$. The fourth reward is multiplied by $0.125$ and therefore contributes $0$. Writing the contributions in prose matters because it keeps the alignment visible: the reward subscript identifies which future reward is being used, and the discount exponent records how far into the future that reward lies relative to time $t$.

Therefore

$$
G_t = 4 - 1 + 1.5 + 0 = 4.5.
$$

What did each index mean? The reward subscript identified which future reward was being included. The exponent on $0.5$ tracked how many steps into the future that reward lay relative to time $t$. Because those two bookkeeping devices remained aligned, the expression was easy to interpret.

The general lesson is that the return formula is not arbitrary notation. It is carefully indexed to reflect the temporal structure of act, then transition, then reward.

### Misconception block

**Do not confuse the time index $t$ with the summation index $k$.** The time index $t$ fixes the starting decision point. The index $k$ runs through future offsets from that point.

### Connection to later material

The return random variable is the raw object whose conditional expectations become value functions. If the reader is not fully clear on what $G_t$ contains and how it is indexed, later Bellman equations will feel harder than they are.

### Retain / Do not confuse

Retain that $G_t$ starts with $R_{t+1}$, because the action at time $t$ yields reward only after the next transition. Do not confuse the future-offset index $k$ with the base time index $t$.

---

## 7. The return recursion

### Why this section exists

Once return has been defined, the next natural question is whether it admits a recursive form. Recursive structure is the entry point to Bellman-style reasoning, but the reader must first separate what is a plain algebraic fact about return from what later becomes a conditional expectation identity. This section exists to establish that distinction cleanly.

### The object being introduced

The object is the one-step recursion satisfied by the return random variable itself. The question it answers is: how is the full future return from time $t$ related to the immediate next reward and the remaining future return from time $t+1$?

What is fixed is the definition of $G_t$. What varies is the way the infinite sum is regrouped. The conclusion this section allows is that return can be decomposed into an immediate term plus a discounted tail.

### Formal statement

Starting from

$$
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1},
$$

one obtains

$$
G_t = R_{t+1} + \gamma G_{t+1}.
$$

### Interpretation

This formula says that the return from time $t$ is made of two parts: the first reward received after acting at time $t$, and then the entire return from the next decision time onward, discounted once because it lies one step further into the future.

The important thing to notice first is what this formula is **not**. It is not yet a Bellman equation. It is not yet about expectations. It is simply an identity satisfied by the return random variable because of how the sum defining it is arranged.

### Boundary conditions, assumptions, and failure modes

The recursion presumes the return itself is well-defined. In continuing settings, that takes us back to the standing assumptions that control the infinite series.

A frequent failure mode is to refer to this identity as “the Bellman equation.” That is too early. Bellman equations arise when one takes conditional expectations of return and adds appropriate structural assumptions, usually Markovian ones.

### Fully worked example

Take the realized reward sequence from the previous section with $\gamma=0.5$:

$$
R_{t+1}=4, \quad R_{t+2}=-2, \quad R_{t+3}=6, \quad R_{t+4}=0,
$$

and later rewards zero.

We already computed

$$
G_t = 4.5.
$$

Now compute $G_{t+1}$ from its own definition:

$$
G_{t+1} = \sum_{k=0}^{\infty} 0.5^k R_{t+1+k+1} = R_{t+2} + 0.5R_{t+3} + 0.25R_{t+4} + \cdots.
$$

Substitute the realized rewards:

$$
G_{t+1} = -2 + 0.5(6) + 0.25(0) = -2 + 3 = 1.
$$

Now check the recursion:

$$
R_{t+1} + \gamma G_{t+1} = 4 + 0.5(1) = 4.5.
$$

This matches the direct computation of $G_t$. What was checked at each step? First, the definition of $G_{t+1}$ was applied with the time index shifted by one. Second, the same realized reward sequence was used. Third, the immediate next reward $R_{t+1}$ was separated from the tail and the tail was recognized as exactly the discounted next return.

The general lesson is that recursive structure here is not imported from a theorem; it is already present in the definition of return.

### Misconception block

**Do not confuse an identity about return with a recursive equation about value.**

$$
G_t = R_{t+1} + \gamma G_{t+1}
$$

holds at the level of the random variable itself. A Bellman equation concerns quantities like $V^\pi(s)=\mathbb{E}_\pi[G_t\mid S_t=s]$.

### Connection to later material

Later, this identity will be inserted inside conditional expectations. That is how one reaches recursive formulas for value functions. But the conceptual order matters: first the identity for $G_t$, then expectations of that identity under appropriate conditioning.

### Retain / Do not confuse

Retain that the return recursion is an algebraic decomposition of the return random variable. Do not confuse it with a Bellman equation or with any claim requiring the Markov property.

---

## 8. Why discounted return is well-defined

### Why this section exists

It is common in applied work to manipulate return formulas as if convergence were automatic. That is dangerous. Before one conditions on return, optimizes expected return, or differentiates objectives built from return, one must first confirm that the return random variable is mathematically meaningful. This section exists to do that check explicitly.

### The object being introduced

The object is not a new random variable but a boundedness argument for the already defined discounted return. The question is whether the infinite series defining $G_t$ converges and whether its magnitude is controlled uniformly.

What is fixed is the return definition and the standing assumptions $|R_t|\le R_{\max}$ and $0\le \gamma<1$. What varies is the future index $k$ in the tail. The conclusion allowed is that the entire return is absolutely convergent and bounded.

### Formal statement

Under bounded rewards and $0 \le \gamma < 1$,

$$
|G_t| \le \sum_{k=0}^{\infty} \gamma^k |R_{t+k+1}| \le \sum_{k=0}^{\infty} \gamma^k R_{\max} = \frac{R_{\max}}{1-\gamma}.
$$

### Interpretation

The proof works by checking magnitude before sign. The absolute value of each reward is no larger than $R_{\max}$. Therefore each discounted term has magnitude at most $\gamma^k R_{\max}$. The series of these upper bounds is geometric and converges because $\gamma<1$. Since the original series is dominated by a convergent geometric series, the return is absolutely convergent and uniformly bounded.

The first thing the reader should notice is the order of reasoning. One does not begin by taking expectation. One first verifies that the random quantity whose expectation is to be taken is itself well-defined.

### Boundary conditions, assumptions, and failure modes

If $\gamma=1$ in a continuing task, the geometric bound becomes useless because the series $\sum_{k=0}^{\infty} 1$ diverges. If rewards are unbounded, the simple domination argument also fails.

This does not mean all such problems are hopeless. It means that these particular sufficient conditions are no longer available, and new structure would be needed.

### Fully worked example

Suppose $R_{\max}=5$ and $\gamma=0.8$. We want to know whether the infinite discounted return is controlled.

Start from the definition:

$$
G_t = \sum_{k=0}^{\infty} 0.8^k R_{t+k+1}.
$$

Take absolute values term by term using the triangle inequality:

$$
|G_t| \le \sum_{k=0}^{\infty} 0.8^k |R_{t+k+1}|.
$$

Now apply the bounded reward assumption, which says each $|R_{t+k+1}|$ is at most $5$:

$$
|G_t| \le \sum_{k=0}^{\infty} 0.8^k \cdot 5 = 5\sum_{k=0}^{\infty} 0.8^k.
$$

The remaining sum is geometric with ratio $0.8$, so

$$
\sum_{k=0}^{\infty} 0.8^k = \frac{1}{1-0.8} = 5.
$$

Therefore

$$
|G_t| \le 5 \cdot 5 = 25.
$$

The conclusion is stronger than mere convergence. The return is bounded by $25$ in absolute value for every sample path consistent with the assumptions. That makes expressions such as

$$
V^\pi(s)=\mathbb{E}_\pi[G_t\mid S_t=s]
$$

well-behaved under the standing assumptions.

The general lesson is that a controlled infinite sum is obtained by pairing bounded term magnitudes with decaying weights.

### Misconception block

**Do not confuse a sufficient condition with a definition.** Discounted return is *defined* by its series. The boundedness argument shows one convenient set of conditions under which the definition yields a legitimate finite quantity.

### Connection to later material

This section justifies why return-based value functions and objectives are not merely formal symbols in the continuing setting. It also models the correct mathematical habit: first ensure the object exists, then manipulate it.

### Retain / Do not confuse

Retain that bounded rewards plus $\gamma<1$ make the infinite discounted return absolutely convergent and uniformly bounded. Do not confuse “usually finite in practice” with “proved finite under stated assumptions.”

---

## 9. Episodic finite-horizon return

### Why this section exists

Not every reinforcement-learning problem is continuing. Many important derivations, especially in policy gradient methods, are easiest to state on finite-horizon episodes. In that setting, the key issue is no longer convergence of an infinite series but careful handling of the terminal index. This section exists to adapt the return concept to episodic tasks.

### The object being introduced

The object is the finite-horizon return from time $t$ in an episode ending at time $T$. What is fixed is the current time $t$ and the terminal time $T$. What varies is the future offset $k$ only until the episode ends. The question it answers is: what discounted cumulative reward remains between now and termination?

### Formal definition

In a finite-horizon episodic task with terminal time $T$,

$$
G_t = \sum_{k=0}^{T-t-1} \gamma^k R_{t+k+1}.
$$

### Interpretation

The upper limit $T-t-1$ ensures that the final included reward is $R_T$. If the last chosen action occurs at time $T-1$, then the reward produced by that final action is observed at time $T$, so it is the last immediate reward in the episode. The finite upper limit is therefore not arbitrary; it encodes the boundary of the episode exactly.

### Boundary conditions, assumptions, and failure modes

Because the sum has finitely many terms, convergence is no longer the main issue. The main issue is indexing correctly at the terminal boundary. A frequent mistake is to include too many or too few reward terms by mishandling the upper limit.

### Fully worked example

Suppose an episode has terminal time $T=4$, current time is $t=1$, and $\gamma=0.9$. Then the finite-horizon return is

$$
G_1 = \sum_{k=0}^{4-1-1} 0.9^k R_{1+k+1} = \sum_{k=0}^{2} 0.9^k R_{k+2}.
$$

So the finite-horizon sum contains exactly three terms. When $k=0$, the contribution is $0.9^0R_2$, which is the first reward observed after time $1$. When $k=1$, the contribution is $0.9^1R_3$, the next reward one step farther into the future. When $k=2$, the contribution is $0.9^2R_4$, the final reward generated by the last available action before termination. There are no further terms because $R_4$ is already the reward associated with the final decision time $T-1=3$.

If the realized rewards are $R_2=3$, $R_3=-1$, and $R_4=2$, then

$$
G_1 = 1\cdot 3 + 0.9(-1) + 0.9^2(2) = 3 - 0.9 + 1.62 = 3.72.
$$

The logic of the indexing is what matters most. The formula is not saying “sum until it seems natural to stop.” It is saying “include every post-decision reward from time $t+1$ through the terminal reward at time $T$, and stop exactly there.”

The general lesson is that finite-horizon formulas demand exact boundary awareness.

### Misconception block

**Do not confuse terminal time with the index of the last action.** If the last action is chosen at time $T-1$, then the last immediate reward is observed at time $T$.

### Connection to later material

Finite-horizon returns are the natural payoff objects when trajectory-based objectives are written over complete episodes. They are especially common in policy-gradient derivations, where one sums over complete trajectories of controlled length.

### Retain / Do not confuse

Retain that the last included reward in a horizon-$T$ episode is $R_T$. Do not confuse “finite horizon” with “ignore indexing details”; finite horizon removes convergence issues, not bookkeeping issues.

---

## 10. Finite-horizon trajectory distributions

### Why this section exists

So far the chapter has discussed scalar random variables such as rewards and returns. Policy-gradient methods, however, reason about complete trajectories. To differentiate expected return over entire episodes, one must know what the probability of a whole trajectory is. This section exists to make that probability law explicit.

### The object being introduced

The object is a trajectory $\tau$ and its probability under a policy and environment. A trajectory is a whole time-ordered sequence of states, actions, rewards, and terminal state information across an episode. What is fixed is the horizon $T$, the initial-state distribution $\rho$, the policy $\pi$, and the environment transition-reward law $P(s',r\mid s,a)$. What varies is the particular realized sequence making up $\tau$.

The role of the trajectory distribution is to tell us how likely each complete episode is. That is the probability law with respect to which expected performance over episodes is computed.

### Formal definition

For a finite-horizon episodic problem with horizon $T$, define

$$
\tau = (s_0,a_0,r_1,s_1,a_1,r_2,\ldots,s_{T-1},a_{T-1},r_T,s_T).
$$

If $\rho(s_0)$ is the initial-state distribution, $\pi(a_t\mid s_t)$ is the policy, and $P(s_{t+1},r_{t+1}\mid s_t,a_t)$ is the environment law, then

$$
p_\pi(\tau) = \rho(s_0)\prod_{t=0}^{T-1} \pi(a_t\mid s_t)\,P(s_{t+1},r_{t+1}\mid s_t,a_t).
$$

### Interpretation

This factorization says that a full trajectory probability is built by multiplying local contributions across time. The initial distribution picks the starting state. At each time step, the policy contributes the probability of the chosen action given the current state, and the environment contributes the probability of producing the next state-reward pair given the current state and action.

At this point the chapter should say explicitly what kind of statement this is. The factorization is not yet a gradient formula and not yet a policy-optimization result. It is first a **probability-structure statement**: once the horizon, initial distribution, policy, and one-step environment law are fixed, the probability of a complete trajectory is the product of those local terms across time. Only after that law has been written down and the parameter dependence has been identified does the later log-derivative move become licensed. In other words, the trajectory law comes first; the gradient manipulation is downstream of it.

### "This does not imply" paragraph for score-function reasoning

The log-derivative identity does **not** say that every term in a trajectory factorization contributes a policy-gradient term. It says something narrower: if an expectation is taken under a trajectory law $p_\theta(\tau)$, then
$$
\nabla_\theta p_\theta(\tau)=p_\theta(\tau)\nabla_\theta \log p_\theta(\tau)
$$
for those $\tau$ in the support of the law where the derivative is well-defined. The next adversarial question is therefore: **which factors inside $p_\theta(\tau)$ actually depend on $\theta$?** If the environment transition law and reward law are not parameterized by $\theta$, they do not create policy-gradient terms merely because they appear in the factorization. A student who forgets that point can carry the right identity into the wrong differentiation target.

It is worth stating the dependency in the strongest possible form. The trajectory factorization is a statement about **what probability law is being averaged over**. By itself, it does not yet produce any gradient estimator and does not yet justify replacing a derivative by a sampled score-weighted return. The later log-derivative identity is a separate calculus step that acts on that already specified law. So the logical order is: first define the trajectory distribution; then identify where the parameters enter; then use calculus to rewrite derivatives of that law into an expectation-friendly form. If these three stages are blurred, later policy-gradient derivations can look like a single magical trick rather than a chain of legitimate steps.

The formula has the shape of a chain rule specialized to the sequential structure of the RL interaction. The reader should notice that the global trajectory law is not an opaque monolith. It is assembled from interpretable local mechanisms.

### Boundary conditions, assumptions, and failure modes

This factorization depends on the assumed generative structure of the episodic process: initial state distribution, then repeated alternation of policy choice and environment response. If the environment or policy has additional hidden dependence on full history beyond what is captured in the stated law, then the factorization must be modified accordingly.

Another failure mode is to forget what each factor conditions on. The policy factor depends on current state. The environment factor depends on current state and chosen action. Mixing those roles obscures the meaning of the product.

### Fully worked example

Consider a horizon-$2$ episode. Let the initial state distribution satisfy

$$
\rho(s_0=a)=0.6, \qquad \rho(s_0=b)=0.4.
$$

Suppose the realized trajectory is

$$
\tau = (a,\,L,\,1,\,b,\,R,\,2,\,a).
$$

This means the episode starts in state $a$, the first action is $L$, the first reward is $1$, the next state is $b$, the second action is $R$, the second reward is $2$, and the terminal state is $a$.

Assume the policy and environment probabilities are

$$
\pi(L\mid a)=0.7,
$$
$$
P(b,1\mid a,L)=0.5,
$$
$$
\pi(R\mid b)=0.4,
$$
$$
P(a,2\mid b,R)=0.25.
$$

Now compute the trajectory probability by multiplying the initial factor and the local step factors:

$$
p_\pi(\tau)=\rho(a)\,\pi(L\mid a)\,P(b,1\mid a,L)\,\pi(R\mid b)\,P(a,2\mid b,R).
$$

Substitute the numbers:

$$
p_\pi(\tau)=0.6 \cdot 0.7 \cdot 0.5 \cdot 0.4 \cdot 0.25.
$$

Multiply step by step:

$$
0.6\cdot 0.7=0.42,
$$
$$
0.42\cdot 0.5=0.21,
$$
$$
0.21\cdot 0.4=0.084,
$$
$$
0.084\cdot 0.25=0.021.
$$

So the probability of this exact trajectory is

$$
p_\pi(\tau)=0.021.
$$

Each multiplication step had a meaning. The first fixed the starting state. The second accounted for the first action choice. The third accounted for the environment’s first response. The fourth accounted for the second action choice. The fifth accounted for the environment’s final response. The general lesson is that a trajectory law is built locally, one time index at a time.

### Misconception block

**Do not confuse a trajectory with a single state sequence.** In this chapter, a trajectory includes states, actions, and rewards. The reward terms matter because performance objectives and environment laws depend on them.

### Connection to later material

Expected performance over episodes is an expectation with respect to this trajectory law. Policy gradients work by differentiating that expectation. The ability to factor the trajectory law into local terms is exactly what later makes the derivative manageable.

### Retain / Do not confuse

Retain that a full trajectory probability is the product of initial, policy, and environment factors across time. Do not confuse what the policy controls with what the environment controls.

---

## 11. Expectations over trajectories

### Why this section exists

Once trajectories have probabilities, the next step is to average functions of trajectories. This is the bridge from probability laws over episodes to optimization objectives in reinforcement learning. Without this section, expected return over full episodes would remain implicit and therefore harder to manipulate.

### The object being introduced

The object is the expectation of a trajectory-dependent function $f(\tau)$. The random object is no longer a scalar like a reward; it is a whole trajectory. What is fixed is the trajectory law $p_\pi(\tau)$. What varies is the particular trajectory $\tau$ being summed over. The conclusion this object allows is that any episode-level quantity can be averaged just like an ordinary random variable, once trajectories are recognized as the underlying outcomes.

### Formal definition

For any function $f(\tau)$ of the full trajectory,

$$
\mathbb{E}_\pi[f(\tau)] = \sum_\tau p_\pi(\tau)\,f(\tau)
$$

in the finite-horizon discrete setting.

### Interpretation

This is the same expectation rule seen earlier. The only thing that changed is the object being averaged. Earlier, the sum ran over possible values of a scalar random variable. Now the sum runs over possible complete trajectories. The structure is identical: value times probability, aggregated over all possibilities.

The first thing to notice is that “trajectory expectation” is not a new kind of expectation. It is the same expectation idea applied to a richer random object.

### Boundary conditions, assumptions, and failure modes

In large or continuous problems, the sum over all trajectories is not computationally realistic to enumerate explicitly. But the conceptual definition remains important, even when one later estimates the expectation by sampling.

A common confusion is to think $f(\tau)$ must be return itself. It can be any trajectory functional: total reward, discounted return, number of visits to a state, a gradient contribution, or something else entirely.

### Fully worked example

Return to the horizon-$2$ setting, but now suppose there are exactly two possible trajectories under the policy:

$$
\tau_1, \qquad \tau_2,
$$

with probabilities

$$
p_\pi(\tau_1)=0.3, \qquad p_\pi(\tau_2)=0.7.
$$

Let $f(\tau)$ be total undiscounted return over the episode, and suppose

$$
f(\tau_1)=5, \qquad f(\tau_2)=1.
$$

Then by definition,

$$
\mathbb{E}_\pi[f(\tau)] = \sum_\tau p_\pi(\tau)f(\tau) = 0.3(5)+0.7(1).
$$

Compute the two contributions:

$$
0.3(5)=1.5, \qquad 0.7(1)=0.7.
$$

Add them:

$$
\mathbb{E}_\pi[f(\tau)] = 2.2.
$$

What was checked? First, identify the random object: not a reward, but a whole trajectory. Second, identify the value attached to each trajectory through the function $f$. Third, weight each value by the trajectory’s probability. The general lesson is that once a problem is written at the trajectory level, the expectation machinery remains unchanged.

### Misconception block

**Do not confuse “expectation over trajectories” with “sum of state values.”** The expectation is over complete trajectories as atomic outcomes in the random experiment, even if the function being averaged is built from state or reward terms inside those trajectories.

### Connection to later material

Expected episodic return, objective functions for policy optimization, and Monte Carlo estimators are all built on this trajectory expectation viewpoint. It is the conceptual doorway to policy gradient methods.

### Retain / Do not confuse

Retain that expectations over trajectories obey the same value-times-probability logic as ordinary expectations. Do not confuse the complexity of the object being averaged with any change in the definition of expectation itself.

---

## 12. Differentiating an expectation over trajectories

### Why this section exists

Optimization enters reinforcement learning when the policy depends on parameters and one wants to change those parameters to improve expected return. The first formal obstacle is differentiation of an expectation whose underlying probability law depends on the parameters. This section exists to identify that obstacle cleanly before solving it.

### The object being introduced

The object is the derivative of an expectation with respect to policy parameters $\theta$. Suppose the policy induces a trajectory law $p_\theta(\tau)$ and we care about

$$
\sum_\tau p_\theta(\tau)f(\tau).
$$

What is fixed is the trajectory functional $f(\tau)$, assumed not to depend explicitly on $\theta$ in this section. What varies with $\theta$ is the trajectory probability law. The question is how to differentiate the expected objective without losing interpretability.

### Formal statement

Under the finite-horizon regularity assumptions,

$$
\nabla_\theta \sum_\tau p_\theta(\tau)f(\tau) = \sum_\tau \nabla_\theta p_\theta(\tau)f(\tau).
$$

### Interpretation

This step says the derivative may be moved inside the sum, provided the regularity conditions justify doing so. But notice what it does **not** solve. We still face derivatives of probabilities, which are awkward objects to work with directly. So this section should be understood as a reduction of the problem, not its final solution.

The reader should notice the exact source of parameter dependence. Under the present assumption, $f(\tau)$ is fixed as a function of the trajectory itself. The policy parameters affect only how likely each trajectory is.

### Boundary conditions, assumptions, and failure modes

The interchange of derivative and summation is not automatically valid in every setting. This chapter assumes a finite horizon and enough regularity for the move to be legal.

Another failure mode is to forget the assumption that $f(\tau)$ does not explicitly depend on $\theta$. If it does, then an additional derivative term appears by the product rule.

### Fully worked example

Suppose there are two trajectories, $\tau_1$ and $\tau_2$, with

$$
p_\theta(\tau_1)=\theta, \qquad p_\theta(\tau_2)=1-\theta,
$$

for $0<\theta<1$. Let

$$
f(\tau_1)=4, \qquad f(\tau_2)=1.
$$

The expected objective is

$$
J(\theta)=\sum_\tau p_\theta(\tau)f(\tau)=4\theta + 1(1-\theta)=4\theta +1-\theta = 1+3\theta.
$$

Differentiating directly gives

$$
\frac{d}{d\theta}J(\theta)=3.
$$

Now verify the section’s identity by differentiating inside the sum:

$$
\sum_\tau \frac{d}{d\theta}p_\theta(\tau)f(\tau)=\frac{d}{d\theta}(\theta)\cdot 4 + \frac{d}{d\theta}(1-\theta)\cdot 1 = 1\cdot 4 + (-1)\cdot 1 = 3.
$$

The two routes agree. What did each step check? First, the objective was written as an expectation over trajectories. Second, the parameter dependence was located in the trajectory probabilities. Third, differentiation was carried out either before or after summation, giving the same answer because the regularity assumptions held in this finite example.

The general lesson is that parameterized expectations are differentiated by tracking how the distribution changes.

### Misconception block

**Do not confuse “differentiate an expectation” with “differentiate the realized return of one trajectory.”** Optimization acts on the probability law over trajectories, not on a single sampled episode viewed in isolation.

### Connection to later material

This section sets up the exact bottleneck that the log-derivative identity will resolve. Once derivatives of probabilities are converted into probabilities times score terms, the whole expression becomes an expectation again.

### Retain / Do not confuse

Retain that parameter dependence enters through the trajectory law when $f(\tau)$ itself is parameter-free. Do not confuse moving the derivative inside the sum with having solved the gradient problem completely.

---

## 13. The log-derivative identity

### Why this section exists

The previous section reduced the gradient problem to derivatives of trajectory probabilities. Those derivatives are not convenient to estimate from sampled trajectories. This section exists because the log-derivative identity converts those derivatives into a form that reintroduces the probability law itself, which is exactly what an expectation needs.

### The object being introduced

The object is the identity relating $\nabla_\theta p_\theta(\tau)$ to $\nabla_\theta \log p_\theta(\tau)$. The role of this identity is transformational: it turns a derivative of a probability into the probability multiplied by a score term.

What is fixed is the trajectory probability function. What varies is the parameter $\theta$. The conclusion enabled by this identity is that gradient expressions can be rewritten as expectations rather than raw derivatives of probabilities.

### Formal definition

Whenever $p_\theta(\tau) > 0$,

$$
\nabla_\theta \log p_\theta(\tau) = \frac{1}{p_\theta(\tau)}\nabla_\theta p_\theta(\tau).
$$

Rearranging,

$$
\nabla_\theta p_\theta(\tau) = p_\theta(\tau)\,\nabla_\theta \log p_\theta(\tau).
$$

This identity is easy to misuse if its scope is not stated. By itself, it is an algebraic identity about differentiable positive functions. In this chapter, it becomes useful because the object to which it is applied is a **factorized trajectory probability law**. Once that law is factorized and once the parameter $\theta$ is assumed to enter only through the policy, the log turns products into sums and the derivative terms associated with the environment disappear. So the later policy-gradient interpretation depends on two distinct things: the general log-derivative identity and the specific parameter-dependence structure of the RL trajectory law.

### Interpretation

This identity is simple calculus, but its effect is profound. The derivative of the log probability measures the local sensitivity of the log-likelihood of the trajectory to the policy parameters. Multiplying by the probability recovers the derivative of the probability itself. The crucial advantage is structural: once a factor of $p_\theta(\tau)$ appears explicitly, it can sit inside a sum as the weighting term of an expectation.

A useful boundary statement belongs here. The log-derivative identity does **not** say that optimization is finished, and it does **not** say that one sampled trajectory reveals the true gradient. What it gives is a change of algebraic form: a derivative of a probability law becomes that same law multiplied by a score term. That matters because expectations are taken with respect to the law itself. The identity therefore licenses a later estimator construction. It does not by itself choose the weighting signal, prove low variance, or eliminate the need for assumptions about where the parameter dependence lives.

The first thing to notice is that the log is not introduced for aesthetic reasons. It is introduced because differentiating a log converts multiplicative structure into additive structure and makes expectations possible.

### Boundary conditions, assumptions, and failure modes

The expression $\log p_\theta(\tau)$ and the ratio formula require $p_\theta(\tau)>0$ for the trajectory under discussion. In practice, gradient formulas are interpreted on the support of the policy-induced trajectory distribution.

A common overstatement is to treat the identity itself as the policy-gradient theorem. It is not. It is a tool used inside the theorem’s derivation.

### Fully worked example

Suppose a trajectory probability is

$$
p_\theta(\tau)=\theta^2
$$

for a particular trajectory and parameter range $\theta>0$. We want to verify the identity.

First compute the derivative directly:

$$
\frac{d}{d\theta}p_\theta(\tau)=\frac{d}{d\theta}(\theta^2)=2\theta.
$$

Now compute the score term. Since

$$
\log p_\theta(\tau)=\log(\theta^2)=2\log \theta,
$$

we have

$$
\frac{d}{d\theta}\log p_\theta(\tau)=\frac{2}{\theta}.
$$

Multiply by the probability itself:

$$
p_\theta(\tau)\frac{d}{d\theta}\log p_\theta(\tau)=\theta^2 \cdot \frac{2}{\theta}=2\theta.
$$

This matches the direct derivative. What was checked? First, positivity of $p_\theta(\tau)$ so that the log is defined. Second, direct differentiation of the probability. Third, differentiation of the log probability. Fourth, multiplication by the original probability to recover the same result.

The general lesson is not the algebra itself. The lesson is that the derivative of a probability can be rewritten in a form compatible with expectation notation.

### Misconception block

**Do not confuse “score” with “probability.”** The quantity $\nabla_\theta \log p_\theta(\tau)$ is a sensitivity measure, not a probability weight. It only becomes part of an expectation when multiplied by $p_\theta(\tau)$ inside the sum.

### Connection to later material

This identity is the structural hinge of policy-gradient derivations. It is what allows a gradient of expected return to be rewritten as an expectation of return multiplied by score terms.

### Retain / Do not confuse

Retain that the log-derivative identity converts derivatives of probabilities into probability-weighted score terms. Do not confuse that identity with the full policy-gradient theorem.

---

## 14. Why the score decomposes over time

### Why this section exists

The log-derivative identity gives an expectation-friendly form, but one more simplification is needed. A trajectory probability is a product over time, and direct differentiation of that product is still cumbersome unless its logarithm breaks into a sum of local terms. This section exists to show exactly why that decomposition occurs and exactly which terms survive differentiation.

### The object being introduced

The object is the trajectory score

$$
\nabla_\theta \log p_\theta(\tau).
$$

What is fixed is the factorized trajectory law. What varies with time are the local policy and environment factors. The role of the decomposition is to replace one global trajectory sensitivity with a sum of local sensitivities along the trajectory.

### Formal statement

From the factorized trajectory law,

$$
\log p_\theta(\tau)=\log \rho(s_0)+\sum_{t=0}^{T-1}\log \pi_\theta(a_t\mid s_t)+\sum_{t=0}^{T-1}\log P(s_{t+1},r_{t+1}\mid s_t,a_t).
$$

If the environment dynamics and initial-state distribution do not depend on $\theta$, then differentiating gives

$$
\nabla_\theta \log p_\theta(\tau)=\sum_{t=0}^{T-1}\nabla_\theta \log \pi_\theta(a_t\mid s_t).
$$

### Interpretation

Taking the logarithm turns the product of local factors into a sum. Differentiation of the sum is then termwise. If the parameter $\theta$ lives only inside the policy, then the terms coming from the initial-state distribution and environment dynamics vanish under differentiation. What remains is a sum over time of local policy score terms.

The reader should notice what this means conceptually: the gradient information accumulates along the trajectory only through decisions made by the policy. The environment contributes to which trajectories are seen, but under the stated assumption it does not contribute direct parameter derivatives.

### Boundary conditions, assumptions, and failure modes

This derivation assumes the environment law and initial-state distribution do not depend on $\theta$. If they do depend on $\theta$, their derivative terms remain and must be included.

Another failure mode is to forget that the decomposition is a property of the **log** of the factorized trajectory law. Without the log, the product form is harder to differentiate and interpret.

### Fully worked example

Consider a horizon-$2$ trajectory under a parameterized policy. Suppose

$$
p_\theta(\tau)=\rho(s_0)\,\pi_\theta(a_0\mid s_0)\,P(s_1,r_1\mid s_0,a_0)\,\pi_\theta(a_1\mid s_1)\,P(s_2,r_2\mid s_1,a_1),
$$

and assume $\rho$ and $P$ do not depend on $\theta$.

Take logs:

$$
\log p_\theta(\tau)=\log \rho(s_0)+\log \pi_\theta(a_0\mid s_0)+\log P(s_1,r_1\mid s_0,a_0)+\log \pi_\theta(a_1\mid s_1)+\log P(s_2,r_2\mid s_1,a_1).
$$

Differentiate term by term. The derivative of $\log \rho(s_0)$ is zero because $\rho$ does not depend on $\theta$. The derivatives of the two environment log terms are also zero for the same reason. The only surviving terms are

$$
\nabla_\theta \log p_\theta(\tau)=\nabla_\theta \log \pi_\theta(a_0\mid s_0)+\nabla_\theta \log \pi_\theta(a_1\mid s_1).
$$

What did each step check? First, the product structure of the trajectory law. Second, that taking logs converted the product to a sum. Third, that the location of parameter dependence was confined to the policy factors. Fourth, that differentiation therefore produced a time-sum of policy scores only.

The general lesson is that local control decisions contribute additively to the trajectory score when viewed through the log of the trajectory law.

### Misconception block

**Do not say “the environment disappears.”** The environment does not disappear from the trajectory distribution itself. It disappears only from the derivative **if** it carries no dependence on the policy parameters.

### Connection to later material

This decomposition is what turns policy-gradient formulas into sums of local log-policy gradients along sampled trajectories. It is the step that makes trajectory-level optimization computationally and conceptually tractable.

### Retain / Do not confuse

Retain that the trajectory score decomposes into a sum of log-policy gradients over time when only the policy depends on $\theta$. Do not confuse “no derivative contribution” with “no probabilistic role.”

---

## 15. Common confusions this chapter is designed to block

### Why this section exists

A chapter on preliminaries succeeds not only when it introduces correct concepts, but also when it blocks recurring wrong ones. The same small confusions reappear in many later derivations and make advanced material feel harder than it is. This section gathers the most dangerous misunderstandings in one place.

### Confusion 1: expectation is the same as averaging observed samples

Expectation is defined from a probability law. A sample average is an estimator built from realized data. They are related, but they are not the same object. The distinction matters because reinforcement learning often alternates between theoretical expectations and empirical estimates.

### Confusion 2: conditioning changes the values a random variable can take

Usually the important change is not the set of numerical values but the weights placed on those values after information is fixed. Conditioning reweights possibilities. It does not magically redefine the random variable into a different kind of object.

### Confusion 3: the return recursion is already a Bellman equation

The identity

$$
G_t = R_{t+1} + \gamma G_{t+1}
$$

is a statement about the return random variable. A Bellman equation is a recursive statement about conditional expectations of return, usually at the level of state values or action values and typically under Markov assumptions.

### Confusion 4: bounded rewards and $\gamma<1$ are cosmetic assumptions

They are substantive. In the standard continuing setup, they are exactly what gives a clean bound on discounted return.

### Confusion 5: the log-derivative identity by itself is the policy-gradient theorem

It is not. It is one tool in the derivation. The policy-gradient theorem also relies on the trajectory-law setup, differentiation of expectations, and decomposition of the trajectory score.

### Retain / Do not confuse

Retain that these distinctions are not linguistic niceties. They are correctness conditions for later reasoning.

---

### Oral-exam checkpoint: notation versus probability structure versus proof tool

Be able to answer the following without writing down a memorized slogan.

When you write $G_t = R_{t+1} + \gamma G_{t+1}$, you are stating an **algebraic identity** about one random variable defined from a reward sequence. When you write an expectation of return conditioned on a state or history, you are adding a **probability structure**: now the question becomes which random object is being averaged and under what law. When you later use factorized trajectory distributions or the log-derivative identity, you are invoking a **proof tool** that manipulates the chosen probability law. Those are three different levels. If you cannot say which level a given line belongs to, you are still at risk of using the right symbol in the wrong argument.

## 16. What this chapter now entitles you to do

### Why this section exists

A good foundational chapter should end by clarifying what the reader is now licensed to use responsibly. The purpose of this section is not summary for summary’s sake. It is to mark the transition from preliminary concepts to valid mathematical moves in later chapters.

### What you can now conclude

After mastering the material above, you are allowed to do the following without handwaving.

First, you may treat value functions as conditional expectations of return, provided the conditioning variable and the probability law are explicit.

Second, you may split expectations into next-step cases using the law of total expectation and interpret the result as exact probabilistic bookkeeping rather than approximation.

Third, you may use the return recursion as a plain identity about the return random variable and then place it inside expectations when moving toward Bellman equations.

Fourth, you may state clear sufficient conditions under which the infinite discounted return is well-defined.

Fifth, you may write the probability of a finite-horizon trajectory as a product of local initial-state, policy, and environment factors.

Sixth, you may understand how derivatives of expected trajectory functionals become expectation-friendly after the log-derivative identity and score decomposition are applied.

### Connection to later material

This is enough infrastructure for the next major conceptual step: understanding when current state information is sufficient for prediction and control, and why recursive value equations can be written in compact state-based form.

### Retain / Do not confuse

Retain that the point of preliminaries is to license later reasoning, not to accumulate detached formulas. Do not confuse familiarity with notation for mastery of what the notation permits.

---

## 17. Mastery check

A serious reader should be able to answer the following questions in complete sentences, with the relevant variables and assumptions made explicit.

1. What exactly is expectation averaging over, and what are the two ingredients required to define it?
2. When you condition on an event such as $Y=y$, what changes and what stays the same?
3. In a Bellman-style derivation, what does the law of total expectation let you do, and why is that move exact?
4. Why does the return from time $t$ begin with $R_{t+1}$ rather than $R_t$ in the standard convention?
5. Under what assumptions is infinite discounted return bounded, and what does the bound look like?
6. In a factorized finite-horizon trajectory law, which factors come from the policy and which come from the environment at each time index?
7. Why does the log-derivative identity help convert a derivative of expected return into a form that can again be read as an expectation?
8. Under what assumption do the environment terms vanish from the derivative of the log trajectory probability?

If any one of these answers feels vague, the right move is not to press ahead. The right move is to repair the gap now. Later chapters build directly on these ideas, and weak understanding here compounds quickly.
