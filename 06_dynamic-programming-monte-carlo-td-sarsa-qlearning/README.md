# Chapter 6 — Dynamic Programming, Monte Carlo, TD, SARSA, and Q-Learning

*Rewritten as mastery-oriented teaching notes from the source chapter in the linked repository, following the uploaded writing standard.*

## What this chapter is for

The previous chapters introduce value functions and Bellman equations as mathematical objects. That is necessary, but it leaves an obvious unresolved question: how do those equations become actual procedures that estimate values or improve policies? A Bellman equation by itself is not yet an algorithm. It tells us what is true at the solution. This chapter is about the family of methods that try to reach that solution, and it is written to prevent the most common kind of confusion in reinforcement learning: mixing together methods that look similar in notation while differing in exactly one decisive mechanism.

There are several axes that students often blur together. Does the method assume the transition-reward model is known, or does it learn directly from sampled experience? Does it use an exact expectation under the model, or a sampled target from one observed transition or one complete episode? Does the target use the full realized return, or does it bootstrap from the current estimate? If the method updates action values, is the continuation determined by the same policy that generated the data, or by a different policy inserted into the target? This chapter keeps those axes separate on purpose, because each method in the chapter is best understood not by memorizing a formula, but by identifying exactly where it lands on each of those dimensions.

To make that promise operational, the chapter should fix one reusable classification order now. For every method introduced later, ask the same six questions in the same sequence. First, does the method assume a known model, or does it learn from sampled experience? Second, is its target an exact expectation or a sampled quantity? Third, does it use a complete realized return or a bootstrap estimate of continuation? Fourth, if action values are being updated, what policy determines the continuation inside the target? Fifth, what object is actually being updated: a state value, an action value, or a policy-improvement surrogate built from one of those? Sixth, what is the method trying to compute exactly, and what is it using only as an intermediate estimate? Once these six questions are fixed, the later methods stop looking like a bag of formulas and start looking like structured variations on a common template.

The chapter is organized around a progression. Dynamic programming comes first because it solves Bellman equations when the environment model is known. Monte Carlo comes next because it removes the need for a model, but pays for that by waiting for complete returns. Temporal-difference learning then appears as the compromise: it also learns from raw experience, but it replaces full returns with a one-step bootstrap target. Finally, SARSA and Q-learning specialize the temporal-difference idea to action values and control, with the distinction between them resting entirely on what they do at the next state.

That difference should be stated in the sharpest possible way. In SARSA, the next action inside the target is the action that the behavior policy actually takes, so the continuation term is policy-following. In Q-learning, the next action inside the target is the maximizing action under the current estimate, whether or not the behavior policy actually took it, so the continuation term is policy-replacing. The difference is not cosmetic. It determines whether the target is evaluating the behavior actually experienced or imposing a more aggressive control choice inside the bootstrap.

If this chapter works, the reader should stop seeing these methods as a bag of famous names and start seeing them as clean answers to a precise design question: **given what information is available, what target can we construct for learning value?**

---

## 1. The organizing map of the chapter

### Why this section exists

Before defining any individual method, the reader needs a conceptual map. Otherwise each new algorithm looks like a disconnected formula and the chapter becomes a vocabulary test instead of a lesson. This section exists because the later methods are easiest to distinguish once the right comparison axes are visible from the beginning.

### The object being introduced

The object here is not yet a single algorithm. It is a classification frame. The frame answers the question: when a value-learning method is proposed, what are the few decisive checks that tell us what kind of method it is? What is fixed in this section are the comparison axes themselves. What varies later is where each method lands on those axes.

### Formal definition

The main axes of comparison in this chapter are the following.

1. **Model known vs model unknown**
   - Known model: the method can compute expectations using $P(s',r \mid s,a)$.
   - Unknown model: the method learns from sampled experience instead.

2. **Exact expectation vs sampled target**
   - Exact expectation: the update target is computed by averaging under the known model.
   - Sampled target: the update target is built from realized transitions or realized episodes.

3. **Full return vs bootstrap**
   - Full return: the target uses the realized cumulative future reward.
   - Bootstrap: the target uses the current estimate of a later value as part of the target.

4. **On-policy vs off-policy**
   - On-policy: the policy generating data is the same policy whose continuation appears in the target.
   - Off-policy: the policy generating data and the policy inside the learning target differ.

These axes should now be read as a fixed inspection order rather than as a chapter-specific list. When a new method appears, do not begin by memorizing its equation. Begin by interrogating it in sequence.

First ask where its target comes from: from a known model or from sampled experience. Then ask what kind of target it is: an exact expectation, a sampled return, or a sampled bootstrap target. Then ask whether the continuation inside that target comes from the same policy that generated the data or from a different policy inserted for control. Then ask what object the update is actually trying to improve: a state value, an action value, or a policy-improvement mechanism built on top of one of those. Only after those questions are stable should the reader worry about the exact algebraic form of the update.

This inspection order matters because many RL methods look similar at the symbol level while differing in exactly one decisive mechanism. The symbols become much easier to parse once the method has been classified before it is memorized.

### Interpretation paragraph

This map does not replace the methods. It tells us what to ask when any method appears. The first thing to notice is that these axes are logically different. A method can be sample-based and still be on-policy or off-policy. A method can be sample-based and either bootstrap or avoid bootstrapping. A method can use exact expectations only if a model is known. If the reader keeps those checks separate, the chapter becomes much easier to understand.

### Boundary conditions / assumptions / failure modes

The biggest failure mode is to collapse these dimensions into vague impressions such as “Monte Carlo is episodic,” “TD is faster,” or “Q-learning is greedy.” Those phrases are not fully wrong, but they are too weak to be classification rules. Another failure mode is to assume that methods differing by one symbol are conceptually close. In reinforcement learning, a change in one continuation term can change the policy interpretation of the whole method.

### Fully worked example

Suppose someone proposes the following update target for a value estimate at time $t$:

$$
Y_t = R_{t+1} + \gamma V(S_{t+1}).
$$

How do we classify it?

First, ask whether this target requires the full transition-reward law $P(s',r \mid s,a)$. It does not. The target is constructed from the realized one-step outcome that actually occurred: the observed reward $R_{t+1}$ and the observed next state $S_{t+1}$. So this is not a model-based exact-expectation method. It is sample-based.

Second, ask whether the target uses a full realized return or bootstraps. The term $V(S_{t+1})$ is not a realized future return. It is the method’s own current estimate of future value at the next state. So this target bootstraps.

Third, ask whether this is a state-value or action-value update. It is written in terms of $V$, so it is a state-value target.

Fourth, ask whether on-policy versus off-policy even arises here. In this bare state-value target, the policy dependence would be determined by how data are generated and which value function is meant. The formula alone is not enough to answer that classification. That observation matters: sometimes one needs the surrounding learning setup, not just the algebraic target.

The general lesson is that classification is not guesswork. It is a sequence of explicit checks. In future problems, ask: what information is used to build the target, and what role does the current estimate play inside it?

### Misconception or counterexample block

**Do not confuse “sample-based” with “Monte Carlo.”** A one-step TD target is sample-based too. The real distinction is whether the sample target is the *full return* or a *bootstrap target*.

### Connection to later material

This classification frame will be reused throughout the chapter. It is especially important when comparing SARSA and Q-learning, because those methods are often mistaken for nearly identical updates when in fact they differ on the decisive on-policy/off-policy axis.

### Retain / Do not confuse

Retain that the central axes are: model vs no model, expectation vs sample, full return vs bootstrap, and on-policy vs off-policy. Do not confuse these axes with one another or replace them with vague slogans.

---

## 2. Dynamic programming: planning with a known model

### Why this section exists

Bellman equations tell us what the value function of a policy must satisfy. But an equation describing the correct answer is not yet a computational procedure. The first setting in which Bellman equations turn into direct algorithms is the model-known setting. This section must appear first because it shows the cleanest route from Bellman equations to computation: if the environment law is known, the expectation inside the Bellman equation can be evaluated exactly.

### The object being introduced

The object is dynamic programming for policy evaluation. It is a planning method, not a direct learning method from raw experience. It answers the question: if the policy $\pi$ is fixed and the transition-reward law is known, how can we compute the corresponding value function $V^\pi$? What is fixed is the policy and the environment model. What varies from iteration to iteration is the current approximate value function. The conclusion this method allows is convergence to the exact value function of the fixed policy under the discounted assumptions.

### Formal definition

For a fixed policy $\pi$, define the Bellman expectation operator

$$
(T^\pi V)(s) = \sum_a \pi(a\mid s) \sum_{s',r} P(s',r\mid s,a)\,[r + \gamma V(s')].
$$

Iterative policy evaluation applies this operator repeatedly:

$$
V_{k+1} = T^\pi V_k.
$$

Equivalently, state by state,

$$
V_{k+1}(s) = \sum_a \pi(a\mid s) \sum_{s',r} P(s',r\mid s,a)\,[r + \gamma V_k(s')].
$$

### Interpretation paragraph

This update says the following. Start with a current guess $V_k$ for the value of each state. For each state $s$, imagine following the fixed policy $\pi$. Under the known model, average over all actions the policy may choose, then average over all next-state and reward outcomes the environment may produce. The quantity inside the brackets, $r + \gamma V_k(s')$, is the one-step reward plus the discounted continuation value according to the current guess. The operator $T^\pi$ takes the current guess and produces a new guess by enforcing one step of Bellman consistency exactly.

The first thing to notice is what is *not* happening. No trajectory is being sampled. No random transition is being observed. The update is computed by summing over possibilities under the model. That is why dynamic programming is planning rather than direct sample-based learning.

### Boundary conditions / assumptions / failure modes

The discounted convergence guarantee relies on standard assumptions such as bounded rewards and $0 \le \gamma < 1$. In that setting, $T^\pi$ is a contraction mapping in the sup norm, and therefore repeated application converges to the unique fixed point $V^\pi$.

A common failure mode is to say “dynamic programming uses Bellman equations” as though that distinguished it from TD learning. TD learning also comes from Bellman equations structurally. The real distinction is that dynamic programming computes the Bellman update by exact expectation under a known model, whereas TD replaces that expectation with sampled experience.

### Fully worked example

Consider a tiny MDP with two states, $s_1$ and $s_2$, and one action available in each state, so the policy is trivial. Suppose the environment model is known exactly. From $s_1$, the system moves deterministically to $s_2$ and delivers reward $2$. From $s_2$, it stays in $s_2$ and delivers reward $1$. Let the discount factor be $\gamma=0.5$. Because the model is known, every dynamic-programming backup can evaluate the full expected continuation exactly rather than estimating it from sample experience.

We start with initial guess

$$
V_0(s_1)=0, \qquad V_0(s_2)=0.
$$

Now apply iterative policy evaluation.

For state $s_1$,

$$
V_1(s_1)=2 + 0.5\,V_0(s_2)=2 + 0.5(0)=2.
$$

What was checked here? Since the next state and reward are deterministic, the expectation is trivial. The immediate reward is $2$, and the continuation value according to the current estimate is $V_0(s_2)=0$.

For state $s_2$,

$$
V_1(s_2)=1 + 0.5\,V_0(s_2)=1 + 0.5(0)=1.
$$

Now do the second iteration.

For $s_1$,

$$
V_2(s_1)=2 + 0.5\,V_1(s_2)=2 + 0.5(1)=2.5.
$$

For $s_2$,

$$
V_2(s_2)=1 + 0.5\,V_1(s_2)=1 + 0.5(1)=1.5.
$$

Third iteration:

$$
V_3(s_1)=2 + 0.5(1.5)=2.75,
$$
$$
V_3(s_2)=1 + 0.5(1.5)=1.75.
$$

A pattern is emerging. The values keep moving toward Bellman consistency. In fact, solving the fixed-point equations directly gives

$$
V^\pi(s_2)=1 + 0.5V^\pi(s_2),
$$
so

$$
V^\pi(s_2)=2.
$$

Then

$$
V^\pi(s_1)=2 + 0.5V^\pi(s_2)=2 + 1 = 3.
$$

The iterates are clearly approaching $(3,2)$. The general lesson is that dynamic programming repeatedly pushes a current estimate through one exact Bellman backup using the known model.

### Misconception or counterexample block

**Do not confuse “exact expectation” with “closed-form solution.”** Dynamic programming may still require iteration. The update is exact in the sense that the expectation under the model is computed exactly at each step, not that the final answer appears in one algebraic move.

### Connection to later material

Dynamic programming is the reference point for later methods. Monte Carlo and TD methods can be understood as ways of approximating or replacing the Bellman backup when the model is not known or exact expectation is too expensive.

### Retain / Do not confuse

Retain that dynamic programming is planning with a known model and exact Bellman backups. Do not confuse it with direct learning from sampled experience.

---

## 3. Why dynamic programming converges in the discounted setting

### Why this section exists

The update rule for iterative policy evaluation is clear, but without a reason for convergence it would remain a plausible heuristic rather than a justified method. This section appears now because the reader should understand why repeated Bellman backups do not wander arbitrarily in the discounted case.

### The object being introduced

The object is the contraction property of the Bellman expectation operator $T^\pi$. It answers the question: why does repeatedly applying $T^\pi$ bring value estimates closer to $V^\pi$? What is fixed is the policy and discount factor. What varies are the candidate value functions to which the operator is applied. The conclusion allowed is uniqueness of the fixed point and geometric convergence to it.

### Formal definition

For the sup norm $\|V-W\|_\infty = \max_s |V(s)-W(s)|$, the Bellman expectation operator satisfies

$$
\|T^\pi V - T^\pi W\|_\infty \le \gamma \|V-W\|_\infty
$$

when $0 \le \gamma < 1$.

### Interpretation paragraph

This inequality says that after one Bellman expectation backup, the largest coordinate-wise difference between two value functions shrinks by at least the factor $\gamma$. Because $\gamma$ is strictly less than $1$ in the discounted setting, repeated application keeps shrinking discrepancies. That is exactly the mechanism behind convergence.

The first thing to notice is what the operator shrinks: not necessarily the values themselves, but the *distance between competing guesses*. This is why the fixed point becomes unique. Two different fixed points would have zero distance shrinkage only if their distance were already zero.

### Boundary conditions / assumptions / failure modes

The contraction proof depends crucially on $\gamma<1$. If $\gamma=1$ in a continuing undiscounted setting, this argument does not go through. Additional structure would be needed.

A common failure mode is to think contraction means the value function entries themselves must numerically decrease. That is false. Some entries may increase across iterations. What contracts is the distance between two estimates after both are passed through the operator.

### Fully worked example

Return to the two-state example with $\gamma=0.5$. Let

$$
V(s_1)=10,\quad V(s_2)=4,
$$
$$
W(s_1)=6,\quad W(s_2)=0.
$$

Then

$$
\|V-W\|_\infty = \max\{|10-6|,|4-0|\}=4.
$$

Now apply the Bellman expectation operator.

Because the environment is deterministic with

$$
T^\pi X(s_1)=2+0.5X(s_2), \qquad T^\pi X(s_2)=1+0.5X(s_2),
$$

we get

$$
T^\pi V(s_1)=2+0.5(4)=4,
$$
$$
T^\pi V(s_2)=1+0.5(4)=3,
$$
$$
T^\pi W(s_1)=2+0.5(0)=2,
$$
$$
T^\pi W(s_2)=1+0.5(0)=1.
$$

So

$$
\|T^\pi V - T^\pi W\|_\infty = \max\{|4-2|,|3-1|\}=2.
$$

That is exactly $0.5 \cdot 4$, which matches the contraction factor $\gamma=0.5$.

The general lesson is that Bellman expectation updates damp discrepancies because future differences are discounted.

### Misconception or counterexample block

**Do not interpret contraction as “the algorithm becomes less random.”** This is a deterministic operator statement about distances between value functions under the discounted Bellman map.

### Connection to later material

Contraction reasoning also underlies value iteration with the optimality operator in the discounted case. More broadly, it is the cleanest explanation of why Bellman-based updates are numerically stable in the model-known setting.

### Retain / Do not confuse

Retain that $T^\pi$ shrinks sup-norm distances by the factor $\gamma$. Do not confuse shrinking differences with monotone decrease of each value entry.

---

## 4. Value iteration: from prediction to optimal control

### Why this section exists

Policy evaluation computes the value of a fixed policy, but reinforcement learning is usually about control: finding a good or optimal policy. The chapter cannot stop at policy evaluation because that would answer only “how good is this policy?” and not “how should the agent act?” This section introduces the control-side dynamic-programming update.

### The object being introduced

The object is the Bellman optimality operator and the corresponding value-iteration procedure. It answers the question: if the model is known and the goal is optimal control, how can we update a value estimate toward the optimal value function $V^*$? What is fixed is the environment model. What varies is the current value estimate and, implicitly, the action chosen by maximization at each backup. The conclusion allowed is convergence to the optimal value function in the discounted setting.

### Formal definition

The Bellman optimality operator is

$$
(T^*V)(s) = \max_a \sum_{s',r} P(s',r\mid s,a)\,[r + \gamma V(s')].
$$

Value iteration applies this operator repeatedly:

$$
V_{k+1} = T^*V_k.
$$

State by state,

$$
V_{k+1}(s) = \max_a \sum_{s',r} P(s',r\mid s,a)\,[r + \gamma V_k(s')].
$$

### Interpretation paragraph

Compared with policy evaluation, one part changes and one part stays the same. What stays the same is the Bellman-backup logic: the next estimate is built from one-step reward plus discounted continuation value. What changes is how actions are handled. In policy evaluation, actions are averaged using a fixed policy $\pi$. In value iteration, the continuation action is selected by maximization. The update therefore no longer asks, “what happens if the agent follows this given policy?” It asks, “what is the best achievable one-step choice plus continuation according to the current value estimate?”

### Boundary conditions / assumptions / failure modes

In the discounted setting, $T^*$ is also a contraction under the sup norm, so repeated application converges to the unique fixed point $V^*$. But one should not confuse the value-update rule with a final policy by itself. The greedy policy with respect to the converged value function must still be extracted.

Another failure mode is to think value iteration literally tests all long-run policies directly. It does not. It repeatedly performs local maximization inside Bellman backups, and the contraction property makes those local updates sufficient for convergence to the optimal value function.

### Fully worked example

Consider an MDP with one state $s$ and two actions, $a_1$ and $a_2$. Suppose action $a_1$ yields reward $1$ and returns to state $s$, while action $a_2$ yields reward $3$ and also returns to state $s$. Let $\gamma=0.5$. The Bellman optimality update therefore compares two one-step continuation expressions that differ only in their immediate reward, because the continuation state is the same in both cases. The example is valuable only if that comparison is read as a local maximization embedded inside a recursive value update, not merely as two numbers being placed beside each other.

Then the Bellman optimality update is

$$
V_{k+1}(s)=\max\{1+0.5V_k(s),\; 3+0.5V_k(s)\}.
$$

The maximization clearly chooses the second term, so

$$
V_{k+1}(s)=3+0.5V_k(s).
$$

Start from $V_0(s)=0$.

Then

$$
V_1(s)=3,
$$
$$
V_2(s)=3+0.5(3)=4.5,
$$
$$
V_3(s)=3+0.5(4.5)=5.25.
$$

At the fixed point,

$$
V^*(s)=3+0.5V^*(s),
$$
so

$$
V^*(s)=6.
$$

The greedy action is always $a_2$. What was the key check at each iteration? Not merely what the continuation value is, but which action produces the larger one-step-plus-continuation quantity. The general pattern is that value iteration alternates between evaluating continuation via the current estimate and improving action choice via local maximization.

### Misconception or counterexample block

**Do not confuse value iteration with “evaluate then improve” as separate explicit phases.** That description fits policy iteration more directly. Value iteration folds improvement into every backup through the maximization.

### Connection to later material

Q-learning will later look like a sample-based counterpart to this control logic. The max term in the Q-learning target is the sample-based descendant of the Bellman optimality maximization.

### Retain / Do not confuse

Retain that value iteration replaces policy averaging with maximization inside the Bellman backup. Do not confuse it with fixed-policy evaluation.

---

## 5. Monte Carlo prediction: learning from complete returns

### Why this section exists

Dynamic programming depends on a known model. Once the model is unavailable, the agent must learn from actual experience. The most direct sample-based idea is to wait until the future is revealed and then use the realized return itself as the learning target. This section appears now because it is the cleanest model-free replacement for exact Bellman expectations.

### The object being introduced

The object is Monte Carlo value estimation for a policy. It answers the question: if we sample episodes under a policy and do not know the model, how can we estimate the value of a visited state? What is fixed is the policy generating the episodes and the definition of return. What varies are the realized returns following different visits. The conclusion allowed is an empirical estimate of expected return based on complete episodes.

### Formal definition

Suppose state $s$ is visited at time $t$ in an episode generated under policy $\pi$. The Monte Carlo target for that visit is the realized return

$$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots.
$$

A Monte Carlo estimate of $V^\pi(s)$ can be formed by averaging such returns across visits to $s$.

In an incremental form,

$$
V(s) \leftarrow V(s) + \alpha \bigl(G_t - V(s)\bigr).
$$

### Interpretation paragraph

Monte Carlo uses the most literal possible target for value: after visiting a state, follow the rest of the episode, collect the realized future rewards, form the complete return, and use that return to update the estimate. There is no bootstrap term. There is no substitution of an estimated continuation value. The target is entirely made from realized rewards that actually occurred.

The first thing to notice is the price of this purity. Because the target is the full return, the method must wait until enough future rewards have been observed. In episodic tasks, that means waiting until the episode ends. Monte Carlo is therefore conceptually simple but temporally delayed.

### Boundary conditions / assumptions / failure modes

Monte Carlo prediction is most natural in episodic settings because the complete return is then available after the episode terminates. In continuing tasks one needs additional devices, such as truncation or regenerative episodes, to construct practical Monte Carlo targets.

A common failure mode is to say “Monte Carlo is unbiased, so it is always better.” That overgeneralizes. Monte Carlo avoids bootstrap bias in its target, but the full return can have high variance and delayed availability. The correct definition is not “better,” but “uses the complete sampled return and does not bootstrap.”

### Fully worked example

Suppose under policy $\pi$ an episode contains the following rewards after visiting state $s$ at time $t$:

$$
R_{t+1}=2, \qquad R_{t+2}=-1, \qquad R_{t+3}=4,
$$

and then the episode ends. Let $\gamma=0.5$.

The Monte Carlo target is the realized return from that visit:

$$
G_t = 2 + 0.5(-1) + 0.5^2(4).
$$

Compute term by term:

- immediate reward contribution: $2$,
- second reward contribution: $-0.5$,
- third reward contribution: $1$.

So

$$
G_t = 2 - 0.5 + 1 = 2.5.
$$

Suppose the current estimate is $V(s)=1.7$ and the step size is $\alpha=0.2$. Then the incremental Monte Carlo update is

$$
V(s) \leftarrow 1.7 + 0.2(2.5-1.7).
$$

The prediction error here is $0.8$, so the update becomes

$$
V(s) \leftarrow 1.7 + 0.16 = 1.86.
$$

What was checked? First, identify the visit whose value is being estimated. Second, form the complete return from that visit using all later realized rewards. Third, compare that full return to the current estimate. Fourth, move the estimate partway toward the target.

The general lesson is that Monte Carlo waits for the future to finish unfolding and then uses the observed outcome directly.

### Misconception or counterexample block

**Do not confuse the full sampled return with an expectation.** A single Monte Carlo target $G_t$ is one realized sample of future return, not the true value $V^\pi(s)$ itself. Its usefulness comes from averaging across visits or repeated incremental updates.

### Connection to later material

Monte Carlo provides the non-bootstrap side of the Monte Carlo versus TD comparison. That distinction will become central when the chapter introduces temporal-difference learning.

### Retain / Do not confuse

Retain that Monte Carlo uses the complete realized return after a visit and does not bootstrap. Do not confuse one sampled return with the expected value function itself.

---

## 6. First-visit and every-visit Monte Carlo

### Why this section exists

Once Monte Carlo is introduced, an immediate practical detail appears: if a state is visited multiple times in the same episode, how should those visits be counted? This section exists because many learners hear “average returns from visits to the state” and do not realize that there are two standard conventions.

### The object being introduced

The objects are first-visit and every-visit Monte Carlo. They answer the question: within a single episode, do we use only the first occurrence of a state or every occurrence of that state when forming updates? What is fixed is the policy and the episodic return structure. What varies is how repeated visits inside one episode are counted.

### Formal definition

- **First-visit Monte Carlo:** update using the return following only the first visit to state $s$ in each episode.
- **Every-visit Monte Carlo:** update using the return following every visit to state $s$ in each episode.

### Interpretation paragraph

Both conventions are legitimate Monte Carlo methods because both use complete sampled returns and do not bootstrap. The difference lies only in how repeated within-episode occurrences are counted. First-visit Monte Carlo reduces dependence among updates from the same episode by using only the first occurrence. Every-visit Monte Carlo extracts more data from each episode by using all occurrences.

### Boundary conditions / assumptions / failure modes

One should not overstate the distinction. Both methods are still Monte Carlo because they share the defining property of using full returns. Another failure mode is to think first-visit means the first time the state is ever seen across the whole training run. It means the first visit within an episode.

### Fully worked example

Suppose one episode visits state $s$ twice. Let the reward sequence after the first visit be

$$
R_{t+1}=1, \; R_{t+2}=2, \; R_{t+3}=0,
$$

and suppose the second visit occurs at time $t+1$, so its return begins one step later.

Let $\gamma=1$ for simplicity in this episodic example. Then the return from the first visit is

$$
G_t = 1+2+0 = 3.
$$

The return from the second visit is

$$
G_{t+1}=2+0=2.
$$

Under first-visit Monte Carlo, this episode contributes only the target $3$ for state $s$.

Under every-visit Monte Carlo, this episode contributes both targets $3$ and $2$ for state $s$.

The general lesson is that the defining Monte Carlo feature is unchanged. The variation lies in which visits are counted when repeated occurrences appear inside one episode.

### Misconception or counterexample block

**Do not confuse “every visit” with “average the rewards inside one visit.”** Every-visit Monte Carlo means use the return following each distinct visit event.

### Connection to later material

This distinction is not the conceptual center of the chapter, but understanding it helps prevent the mistaken impression that Monte Carlo is a single rigid algorithm rather than a family of full-return estimators.

### Retain / Do not confuse

Retain that first-visit and every-visit Monte Carlo differ only in how repeated state occurrences inside an episode are counted. Do not confuse that with the bootstrap distinction.

---

## 7. Temporal-difference learning: learning from one-step samples plus bootstrap

### Why this section exists

Monte Carlo frees us from needing the model, but it pays by waiting for complete returns. The next obvious question is whether we can start learning immediately after one transition instead of waiting until the end of the episode. This section exists because temporal-difference learning is exactly that move: it replaces the full return by a one-step target that already includes an estimate of the future.

### The object being introduced

The object is one-step temporal-difference prediction, often called TD(0). It answers the question: how can we update a state-value estimate after just one observed transition under a policy? What is fixed is the policy whose value is being predicted. What varies are the observed one-step transition and the current value estimate used for bootstrapping. The conclusion allowed is an online sample-based update that does not require waiting for the episode to finish.

### Formal definition

The Bellman expectation equation for a policy is

$$
V^\pi(S_t) = \mathbb{E}_\pi\bigl[R_{t+1} + \gamma V^\pi(S_{t+1}) \mid S_t\bigr].
$$

A one-step TD target replaces the exact expectation by the realized one-step sample:

$$
Y_t^{\mathrm{TD}} = R_{t+1} + \gamma V(S_{t+1}).
$$

The TD error is

$$
\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t).
$$

The incremental update is

$$
V(S_t) \leftarrow V(S_t) + \alpha \delta_t.
$$

### Interpretation paragraph

This update uses two kinds of information. The first term, $R_{t+1}$, is fresh data from the environment. The second term, $V(S_{t+1})$, is not newly observed long-run outcome data. It is the learner’s own current estimate of future value at the next state. That is exactly why TD is called a bootstrap method: it learns partly from its own current prediction.

The first thing to notice is what has been traded away. Relative to Monte Carlo, TD gives up the complete realized future. In return, it gets immediacy. The update can be performed after a single transition.

The trade can be stated more mechanically. Monte Carlo waits until later so that its target contains realized continuation instead of estimated continuation. TD refuses to wait; it inserts the learner’s current continuation estimate immediately. That single replacement changes three things at once. It allows online updates after one transition. It introduces self-reference because the target depends on a current estimate. And it changes the error profile from purely return-sampling noise to a mixture of sampling noise and bootstrap error. When the reader asks what TD “is,” this replacement is the right answer.

### Boundary conditions / assumptions / failure modes

For terminal next states, the continuation term is conventionally treated as zero, so the target becomes just the terminal reward. This boundary condition matters in episodic tasks.

A common failure mode is to describe TD as “using the Bellman equation directly.” That is too loose. The Bellman equation is an exact conditional expectation identity. TD uses one realized sample as a noisy surrogate for that expectation.

### Fully worked example

Suppose at time $t$ the agent is in state $S_t=s$, takes an action according to the policy, receives reward

$$
R_{t+1}=3,
$$

and lands in next state $S_{t+1}=s'$. Let

$$
V(s)=2.0, \qquad V(s')=4.0, \qquad \gamma=0.5, \qquad \alpha=0.1.
$$

The TD target is

$$
Y_t^{\mathrm{TD}} = 3 + 0.5(4.0)=3+2=5.
$$

The TD error is then

$$
\delta_t = 5 - 2.0 = 3.0.
$$

So the updated value estimate becomes

$$
V(s) \leftarrow 2.0 + 0.1(3.0)=2.3.
$$

What happened conceptually? The state $s$ had current estimated value $2.0$. One observed transition suggested a one-step-plus-continuation target of $5$. Because the target exceeded the current estimate, the value was nudged upward.

Now compare that with what Monte Carlo would require. Monte Carlo would wait for the full future reward stream after time $t$ to finish. TD acted immediately after one transition. The general lesson is that TD converts Bellman structure into online learning by replacing expectation with a sample and future return with a bootstrap estimate.

### Misconception or counterexample block

**Do not say “TD uses observed future rewards.”** One-step TD uses only the immediate observed reward and an estimated continuation value. It does not observe the full future trajectory before updating.

### Connection to later material

SARSA and Q-learning are action-value control methods built from this same one-step temporal-difference structure. Understanding TD prediction first makes those control methods much easier to interpret.

### Retain / Do not confuse

Retain that one-step TD uses a sampled one-step reward plus a bootstrap continuation estimate. Do not confuse the Bellman expectation identity with the TD target built from one realized transition.

---

## 8. The exact Monte Carlo versus TD distinction

### Why this section exists

Students often remember that Monte Carlo waits longer and TD updates sooner, but those are consequences, not the core distinction. This section exists because the defining difference between Monte Carlo and TD should become automatic and verbalizable without hesitation.

### The object being introduced

The object is the direct conceptual comparison between two target constructions. It answers the question: what exactly differs between Monte Carlo and one-step TD at the level of the learning target? What is fixed is the same prediction task under a policy. What varies is only the form of the target.

### Formal definition

- **Monte Carlo target:**

$$
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots
$$

- **One-step TD target:**

$$
R_{t+1} + \gamma V(S_{t+1}).
$$

### Interpretation paragraph

Monte Carlo uses the complete sampled return that actually happened after the visit. TD uses one step of realized experience and then substitutes the learner’s current estimate for the rest. That is the distinction. Everything else follows from it. Because Monte Carlo uses the full return, it does not bootstrap and must wait for later rewards. Because TD uses a bootstrap estimate, it can update immediately and is using its own current value function as part of the target.

### Boundary conditions / assumptions / failure modes

One should resist replacing this clean distinction with broad claims like “TD is lower variance” or “Monte Carlo is more accurate.” Those can be useful tendencies in some settings, but they are not the definitions. The chapter needs the definitional distinction first; comparative statistical properties come later and depend on context.

### Fully worked example

Suppose after visiting state $s$ at time $t$, the future realized rewards are

$$
R_{t+1}=1, \qquad R_{t+2}=2, \qquad R_{t+3}=4,
$$

with $\gamma=0.5$. Also suppose the next-state estimate used by TD is

$$
V(S_{t+1}) = 5.
$$

Then the Monte Carlo target is

$$
G_t = 1 + 0.5(2) + 0.5^2(4)=1+1+1=3.
$$

The one-step TD target is

$$
1 + 0.5(5)=3.5.
$$

These are not the same number. That is not a mistake. The methods are targeting the same underlying value in expectation under suitable conditions, but on a particular sample they use different learning targets.

What did each method check? Monte Carlo checked the full realized future. TD checked only the first realized reward and then consulted the current value estimate for the continuation. The general lesson is that the Monte Carlo versus TD distinction is a target distinction.

### Misconception or counterexample block

**Do not say “TD is just an approximation to Monte Carlo.”** That wording hides the structural role of bootstrapping. TD is a different target construction motivated by Bellman recursion, not merely a truncated Monte Carlo return.

### Connection to later material

This distinction is the key to understanding why SARSA and Q-learning remain TD methods even though they operate on action values. Their targets also combine sampled one-step experience with bootstrap continuation terms.

### Retain / Do not confuse

Retain that Monte Carlo uses the full realized return and TD uses one-step reward plus bootstrap. Do not confuse consequences of that distinction with the distinction itself.

---

## 9. What bootstrapping really means

### Why this section exists

The word “bootstrapping” is used constantly in reinforcement learning, but often only as a slogan. Without a precise meaning, the reader cannot correctly classify TD methods or understand why they differ from Monte Carlo methods. This section exists to turn the term from jargon into a usable concept.

### The object being introduced

The object is the notion of a bootstrap target. It answers the question: when do we say a learning update is bootstrapping? What is fixed is the learning problem. What varies is whether the target depends purely on realized data or partly on the current learned estimate. The conclusion it allows is a crisp classification of methods.

### Formal definition

A target is **bootstrapped** if it depends in part on the learner’s current estimate of a future quantity.

For example,

$$
R_{t+1} + \gamma V(S_{t+1})
$$

is a bootstrap target because it includes the estimate $V(S_{t+1})$.

The Monte Carlo target

$$
G_t
$$

is not bootstrap because it is made entirely from realized rewards.

### Interpretation paragraph

To bootstrap is to support learning of one prediction using another current prediction. The word is appropriate because the method is, in a limited sense, pulling itself forward using its own present estimate. That is neither magical nor automatically bad. It is a structural design choice. Bootstrapping makes earlier updates possible, but it also means the target depends on a quantity that may itself still be inaccurate.

### Boundary conditions / assumptions / failure modes

The key failure mode is to define bootstrapping in terms of speed or efficiency. A method is not bootstrap because it is “faster.” It is bootstrap because its target includes current learned estimates. Another failure mode is to think any use of a value estimate anywhere in an algorithm counts as bootstrapping. The issue is specifically whether the **target** for the update includes the current estimate of a future quantity.

### Fully worked example

Consider two possible targets after observing transition $(S_t,R_{t+1},S_{t+1})$.

Target A:

$$
Y_A = R_{t+1} + \gamma V(S_{t+1}).
$$

Target B:

$$
Y_B = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3}.
$$

Assume the later rewards in target B are actually observed before the update is made.

Now classify them.

For target A, the continuation is given by $V(S_{t+1})$, which is not observed outcome data. It is the learner’s current estimate. Therefore target A bootstraps.

For target B, every term is a realized reward. The target uses no current learned estimate of the future. Therefore target B does not bootstrap.

The general lesson is simple but important: ask whether the continuation comes from observed future rewards or from the current estimate.

### Misconception or counterexample block

**Do not confuse bootstrapping with using a discount factor.** Both Monte Carlo and TD targets can include discounting. Discounting and bootstrapping are different concepts.

### Connection to later material

Once action-value methods are introduced, the same check will reappear. SARSA bootstraps with $Q(S_{t+1},A_{t+1})$, while Q-learning bootstraps with $\max_{a'}Q(S_{t+1},a')$.

### Retain / Do not confuse

Retain that bootstrapping means the target includes the learner’s current estimate of a future quantity. Do not confuse bootstrapping with discounting, speed, or general cleverness.

---

## 10. Behavior policy and target policy

### Why this section exists

The chapter is about to move from state-value prediction to action-value control. At that point, one policy may generate the data while another policy is implicitly being evaluated or improved by the update target. Without a clean distinction between those two roles, on-policy and off-policy methods become permanently confusing. This section must appear before SARSA and Q-learning because the difference between them lives exactly here.

### The object being introduced

The objects are the behavior policy and the target policy. They answer two different questions. The behavior policy answers: **which actions actually generate the data?** The target policy answers: **which policy’s continuation value is the update trying to estimate or improve?** What is fixed is the learning setup. What varies is whether those two roles are played by the same policy or different ones.

### Formal definition

- **Behavior policy:** the policy that generates the observed trajectories or transitions.
- **Target policy:** the policy whose value is being estimated or toward which learning is directed.

A method is

- **on-policy** if behavior policy and target policy are the same,
- **off-policy** if they differ.

### Interpretation paragraph

This distinction is about roles, not about which policy is “better.” The behavior policy determines what data appear in the replay of experience. The target policy determines what continuation the update is actually trying to represent. In some algorithms those roles coincide. In others, the learner explores using one policy but updates toward the value of another.

One more axis should be made explicit here. Two methods can share the same one-step sampled transition structure and still differ in what object they update. A state-value predictor, an action-value predictor, and a control rule derived from those predictors are not interchangeable objects. That difference matters because the continuation term, the improvement step, and the final output of the algorithm all depend on what kind of object is being estimated.

The first thing to notice is that “on-policy versus off-policy” is not a statement about whether the agent explores. Exploration can occur in either case. The question is whether the target uses the same policy that generated the action choices in the data.

### Boundary conditions / assumptions / failure modes

A common failure mode is to think that off-policy means “the method is greedy” or “the method uses random behavior.” Neither is the definition. Another is to think that if the update contains an $\epsilon$-greedy behavior rule, the method must be on-policy. That is only true if the learning target also uses that same $\epsilon$-greedy continuation.

### Fully worked example

Suppose an agent uses an $\epsilon$-greedy policy to act in the environment, so the next action is occasionally exploratory. This is the behavior policy.

Now consider two possible action-value targets after observing transition to next state $S_{t+1}$.

Target 1:

$$
R_{t+1} + \gamma Q(S_{t+1},A_{t+1}),
$$

where $A_{t+1}$ is the actual next action sampled from that same $\epsilon$-greedy behavior policy.

Target 2:

$$
R_{t+1} + \gamma \max_{a'}Q(S_{t+1},a').
$$

In Target 1, the continuation action is the one the behavior policy actually selected. Therefore the target policy is the same as the behavior policy. This is on-policy.

In Target 2, the continuation action is not the one actually sampled by the behavior policy. Instead, the target inserts the greedy maximizing action. Therefore the target policy differs from the behavior policy whenever the behavior policy explores. This is off-policy.

The general lesson is that to classify a method, one must inspect the continuation term in the target, not merely the policy used to act.

### Misconception or counterexample block

**Do not confuse “the policy used in the environment” with “the policy appearing inside the target.”** They can be the same, but they need not be.

### Connection to later material

This distinction is the decisive conceptual fork between SARSA and Q-learning. The formulas differ in one continuation term, and that one difference determines the policy classification of the whole method.

### Retain / Do not confuse

Retain that the behavior policy generates data and the target policy defines what continuation the update is learning about. Do not confuse on-policy/off-policy with exploration versus exploitation.

---

## 11. $\epsilon$-greedy exploration

### Why this section exists

Action-value control methods need exploration. If the agent always picks the current greedy action, many state-action pairs may never be tried, and the learned action values can remain uninformed. This section exists because SARSA and Q-learning are commonly implemented with $\epsilon$-greedy behavior, and the reader should understand exactly what that means probabilistically.

### The object being introduced

The object is the $\epsilon$-greedy policy over a finite action set. It answers the question: how can we mostly follow the current greedy action while still assigning nonzero probability to other actions? What is fixed is the current action-value estimate and the finite action set $\mathcal A$. What varies is which action is chosen on a given decision step. The conclusion it allows is persistent exploration with a simple probability structure.

### Formal definition

Assume a finite action set $\mathcal A$ and, for simplicity, a unique greedy action in state $s$. An $\epsilon$-greedy policy chooses

- the greedy action with probability $1-\epsilon$ plus its share of the exploration mass,
- each action uniformly when the exploration branch is taken.

Therefore the greedy action receives probability

$$
1-\epsilon + \frac{\epsilon}{|\mathcal A|},
$$

and each non-greedy action receives probability

$$
\frac{\epsilon}{|\mathcal A|}.
$$

### Interpretation paragraph

The policy mixes two mechanisms. Most of the time, with probability $1-\epsilon$, it behaves greedily. The rest of the time, with probability $\epsilon$, it ignores greediness and chooses uniformly over all actions. Because the uniform branch includes the greedy action too, the greedy action’s total probability is not merely $1-\epsilon$, but $1-\epsilon + \epsilon/|\mathcal A|$.

The first thing to notice is the guarantee this creates: every action has positive probability as long as $\epsilon>0$. That is the basic exploration property.

### Boundary conditions / assumptions / failure modes

The formulas above assume a unique greedy action. If there are ties, the probability assignment among greedy actions depends on the tie-breaking convention.

A common failure mode is to say that the greedy action gets probability $1-\epsilon$. That misses the fact that the exploratory branch can also pick the greedy action.

### Fully worked example

Suppose the action set has four actions:

$$
|\mathcal A|=4,
$$

and $\epsilon=0.2$. Assume there is one unique greedy action.

Then the probability of the greedy action is

$$
1-0.2 + \frac{0.2}{4} = 0.8 + 0.05 = 0.85.
$$

Each non-greedy action gets

$$
\frac{0.2}{4}=0.05.
$$

Check that the probabilities sum to one:

$$
0.85 + 3(0.05)=0.85+0.15=1.
$$

Now interpret. On average, the policy behaves greedily 85% of the time and assigns 5% probability to each alternative. That means the greedy action dominates but no action is completely excluded.

The general lesson is that $\epsilon$-greedy creates a controlled balance between exploitation and guaranteed exploration.

### Misconception or counterexample block

**Do not confuse “random with probability $\epsilon$” with “non-greedy with probability $\epsilon$.”** Under standard $\epsilon$-greedy, the exploratory branch samples uniformly from *all* actions, including the greedy one.

### Connection to later material

In SARSA, the actual next action sampled from an $\epsilon$-greedy policy enters directly into the target. In Q-learning, the agent may behave $\epsilon$-greedily, but the target still uses a greedy maximization instead of the sampled continuation.

### Retain / Do not confuse

Retain that under standard $\epsilon$-greedy, the greedy action gets $1-\epsilon + \epsilon/|\mathcal A|$. Do not confuse that with $1-\epsilon$.

---

## 12. SARSA: on-policy action-value temporal-difference control

### Why this section exists

State-value prediction is not enough for control because control requires comparing actions, not just states. Once action values are introduced, the temporal-difference idea can be used to learn directly from transitions while simultaneously improving behavior. SARSA appears first among the control methods because it preserves the on-policy logic in the cleanest way.

### The object being introduced

The object is the SARSA update, named from the transition tuple $(S_t,A_t,R_{t+1},S_{t+1},A_{t+1})$. It answers the question: how do we update an action-value estimate using one observed transition when the continuation is determined by the same policy currently generating behavior? What is fixed is the current behavior policy, typically something exploratory such as $\epsilon$-greedy with respect to $Q$. What varies are the sampled transition and the sampled next action from that same policy. The conclusion allowed is on-policy action-value learning.

### Formal definition

The one-step SARSA target is

$$
Y_t^{\mathrm{SARSA}} = R_{t+1} + \gamma Q(S_{t+1},A_{t+1}),
$$

where $A_{t+1}$ is the actual next action selected by the current behavior policy.

The update is

$$
Q(S_t,A_t) \leftarrow Q(S_t,A_t) + \alpha \Bigl(R_{t+1} + \gamma Q(S_{t+1},A_{t+1}) - Q(S_t,A_t)\Bigr).
$$

### Interpretation paragraph

SARSA is a TD method for action values. Like TD prediction, it uses one observed reward and a bootstrap continuation term. But unlike state-value TD, the continuation is action-sensitive: it uses the value of the specific next action that the current policy actually selected. That single fact is the reason SARSA is on-policy. The target evaluates continuation under the same policy that is generating the experience.

The first thing to notice is that the next action is sampled, not optimized over. SARSA asks: **given the policy I am actually following, what continuation did I commit myself to at the next state?**

### Boundary conditions / assumptions / failure modes

If $S_{t+1}$ is terminal, the continuation term is conventionally set to zero.

A major failure mode is to describe SARSA as “Q-learning with exploration.” That is inaccurate. SARSA’s defining feature is not merely that the behavior is exploratory. It is that the target uses the action actually sampled from the behavior policy.

### Fully worked example

Suppose at time $t$ the agent is in state $s$, takes action $a$, receives reward

$$
R_{t+1}=2,
$$

and reaches next state $s'$. The current policy at $s'$ is $\epsilon$-greedy and, on this particular transition, it actually selects action $a'$. Suppose

$$
Q(s,a)=1.5,
$$
$$
Q(s',a')=4.0,
$$
$$
\gamma=0.5,
$$
$$
\alpha=0.1.
$$

Then the SARSA target is

$$
2 + 0.5(4.0)=2+2=4.
$$

The temporal-difference error is

$$
4 - 1.5 = 2.5.
$$

So the updated action-value estimate becomes

$$
Q(s,a) \leftarrow 1.5 + 0.1(2.5)=1.75.
$$

Now interpret the meaning of this update. The method is not saying “the best possible continuation from $s'$ is worth $4.0$.” It is saying “under the policy actually being followed, the sampled continuation action was $a'$, whose current estimated value is $4.0$.” That is why SARSA learns the value of the behavior policy itself.

The general lesson is that SARSA’s continuation term is policy-realistic: it follows the policy’s actual next move, including exploratory behavior.

### Misconception or counterexample block

**Do not confuse “the next action available” with “the next action actually sampled.”** SARSA uses the action that the current policy really selected at the next state.

### Connection to later material

SARSA will form one side of the decisive comparison with Q-learning. That comparison is the cleanest place to test whether the reader truly understands on-policy versus off-policy control.

### Retain / Do not confuse

Retain that SARSA is an on-policy action-value TD method whose target uses the actual sampled next action. Do not confuse it with a greedy-max target.

---

## 13. Q-learning: greedy target control from sampled transitions

### Why this section exists

Once SARSA is understood, the natural next question is what happens if the continuation term stops following the sampled behavior policy and instead uses the best-looking next action according to the current estimates. This section exists because that single substitution creates Q-learning, one of the central control algorithms in reinforcement learning.

### The object being introduced

The object is the Q-learning update. It answers the question: how can we update an action-value estimate from one observed transition while targeting the greedy continuation value rather than the behavior policy’s sampled continuation? What is fixed is the observed transition and current action-value estimate. What varies is the maximizing next action inside the target. The conclusion allowed is a control method that typically learns off-policy.

### Formal definition

The Q-learning target is

$$
Y_t^{\mathrm{Q}} = R_{t+1} + \gamma \max_{a'} Q(S_{t+1},a').
$$

The update is

$$
Q(S_t,A_t) \leftarrow Q(S_t,A_t) + \alpha \Bigl(R_{t+1} + \gamma \max_{a'}Q(S_{t+1},a') - Q(S_t,A_t)\Bigr).
$$

### Interpretation paragraph

Q-learning is still a one-step TD method. It still uses the observed immediate reward and still bootstraps from current estimates. But the continuation is no longer the value of the action the behavior policy actually selected. Instead, it is the value of the greedy next action under the current action-value table. In other words, the target asks: **if I were to continue optimally according to my current estimates from the next state onward, what target would that imply?**

The first thing to notice is that the next action in the target is *inserted by maximization*, not observed in the data. That is the conceptual break from SARSA.

### Boundary conditions / assumptions / failure modes

If the next state is terminal, the continuation term is taken as zero.

A common failure mode is to say Q-learning is on-policy because the agent may behave $\epsilon$-greedily with respect to the same $Q$ function. That is not enough. If the target uses $\max_{a'}Q(S_{t+1},a')$ while behavior sometimes chooses exploratory actions, then behavior and target policies differ, which makes the method off-policy in the usual setting.

### Fully worked example

Suppose the agent observes the same transition as in the SARSA example: it is currently updating the pair $(s,a)$, it receives reward $R_{t+1}=2$, and the transition lands in next state $s'$. The important difference is not the sampled transition itself. The difference lies in what happens next in the target. Q-learning does not ask which action was actually chosen from $s'$. It asks which action currently has the largest estimated value at $s'$, and it uses that greedy continuation in the target whether or not behavior will actually follow it.

Assume the current action values at $s'$ are

$$
Q(s',a_1)=4.0, \qquad Q(s',a_2)=3.2,
$$

and suppose the actual next action selected by the behavior policy happened to be $a_2$ because of exploration. Also let

$$
Q(s,a)=1.5,
$$
$$
\gamma=0.5,
$$
$$
\alpha=0.1.
$$

The Q-learning target is not based on the sampled next action $a_2$. It is based on the maximizing next action value:

$$
\max_{a'}Q(s',a')=4.0.
$$

So the target is

$$
2 + 0.5(4.0)=4.
$$

The TD error is

$$
4 - 1.5 = 2.5,
$$

and the update becomes

$$
Q(s,a) \leftarrow 1.5 + 0.1(2.5)=1.75.
$$

Now change the example slightly to make the contrast sharper. Suppose instead the sampled exploratory action had low value,

$$
Q(s',a_2)=0.5,
$$

while the greedy action still had value $4.0$.

Then SARSA would use target

$$
2 + 0.5(0.5)=2.25,
$$

because it follows the actual sampled continuation. Q-learning would still use

$$
2 + 0.5(4.0)=4,
$$

because it ignores the sampled exploratory action and inserts the greedy continuation instead.

The general lesson is that Q-learning learns toward the greedy continuation value even when the data were generated by exploratory behavior.

### Misconception or counterexample block

**Do not say “Q-learning uses the next action.”** It uses the maximizing next action value, which need not match the action actually taken in the sampled behavior trajectory.

### Connection to later material

Q-learning is often interpreted as the model-free sample-based descendant of the Bellman optimality backup. The max term in its target is the clearest sign of that lineage.

### Retain / Do not confuse

Retain that Q-learning bootstraps from the greedy next-state action value. Do not confuse the maximizing action in the target with the action actually sampled by behavior.

---

## 14. The decisive comparison: SARSA versus Q-learning

### Why this section exists

These two methods are often presented side by side with nearly identical formulas, and that presentation causes many learners to focus on the surface similarity instead of the one decisive difference. This section exists to force the contrast into the open.

### The object being introduced

The object is the exact conceptual fork between SARSA and Q-learning. It answers the question: at the next state, what continuation does each method use in its target? What is fixed is the same observed transition into the next state. What varies is only the continuation term. The conclusion this comparison allows is a precise explanation of why SARSA is on-policy and Q-learning is typically off-policy.

### Formal definition

SARSA target:

$$
R_{t+1} + \gamma Q(S_{t+1},A_{t+1}).
$$

Q-learning target:

$$
R_{t+1} + \gamma \max_{a'} Q(S_{t+1},a').
$$

### Interpretation paragraph

At the next state, SARSA asks: **which action did the current policy actually choose?** Q-learning asks: **which action would maximize the current action-value estimate?** That is the whole fork. Everything else follows. Because SARSA follows the actual next action chosen by the current policy, its target is policy-consistent with behavior. Because Q-learning overwrites the next action with a greedy maximization, its target generally differs from exploratory behavior.

### Boundary conditions / assumptions / failure modes

One should not let the near-identical algebra hide the conceptual difference. The methods are not merely cosmetic variants. A change from sampled continuation to greedy continuation changes what policy the update is learning about.

A common failure mode is to classify methods based on whether the agent is exploring during data collection. That is not sufficient. Both SARSA and Q-learning can be run with exploratory behavior. The classification depends on the target continuation, not merely the data-collection behavior.

### Fully worked example

Suppose the next state is $s'$ and the current action values there are

$$
Q(s',\text{safe})=5, \qquad Q(s',\text{risky})=1.
$$

Assume the behavior policy is $\epsilon$-greedy and, on this particular transition, because of exploration it actually selects the risky action at $s'$. Also suppose the observed immediate reward is

$$
R_{t+1}=0,
$$

and let $\gamma=1$ for simplicity.

Now compute the two targets.

For SARSA, the actual next action sampled by the policy was risky, so

$$
Y^{\mathrm{SARSA}} = 0 + Q(s',\text{risky}) = 1.
$$

For Q-learning, the target uses the greedy continuation regardless of the exploratory sampled action, so

$$
Y^{\mathrm{Q}} = 0 + \max\{5,1\}=5.
$$

These are radically different targets from the same transition.

What does that mean? SARSA is learning the value of continuing under the current exploratory policy, so it accounts for the fact that risky exploratory actions really can happen. Q-learning is learning toward the greedy continuation value, so it acts as if the best next action will be chosen from $s'$ onward.

The general lesson is that the entire policy interpretation of the method is determined by what happens at the continuation term.

### Misconception or counterexample block

**Do not conclude from similar update syntax that the methods behave similarly.** Their policy semantics differ exactly where the continuation is chosen.

### Connection to later material

This comparison becomes especially important when reasoning about risky domains or exploration-sensitive behavior. On-policy methods learn the consequences of the exploratory behavior they actually execute, while off-policy greedy-target methods learn toward a different continuation policy.

### Retain / Do not confuse

Retain that SARSA uses the actual sampled next action and Q-learning uses the greedy maximizing next action. Do not confuse sampled continuation with greedy continuation.

---

## 15. Why Q-learning is typically off-policy and SARSA is on-policy

### Why this section exists

The previous section compared the targets directly. This section exists to formalize the policy classification that follows from that comparison, because “typically off-policy” for Q-learning and “on-policy” for SARSA are often memorized as labels without being justified.

### The object being introduced

The object is the policy classification argument. It answers the question: why does the SARSA target align with the behavior policy while the Q-learning target usually does not? What is fixed is the observed data stream generated by some behavior policy. What varies is the policy represented inside the continuation term of the target.

### Formal definition

- SARSA is **on-policy** because its target uses $A_{t+1}$, the next action actually sampled from the current behavior policy.
- Q-learning is **typically off-policy** because its target uses

$$
\max_{a'}Q(S_{t+1},a'),
$$

which corresponds to greedy continuation even when the behavior policy explores.

### Interpretation paragraph

In SARSA, there is no mismatch between data-generation policy and target continuation. The update asks about the value of the continuation action the current policy actually selected. In Q-learning, if behavior is exploratory, then the policy generating data is not the greedy policy represented by the max term inside the target. The method is therefore using one policy to collect experience and another policy to define the continuation it learns toward.

### Boundary conditions / assumptions / failure modes

The word “typically” matters for Q-learning. If behavior happened to be exactly greedy at all times and matched the target policy, then behavior and target policies would coincide. But in practical learning, Q-learning is often paired with exploratory behavior, and then the mismatch appears.

A failure mode is to think that because Q-learning may update the same table used for behavior selection, it must be on-policy. Sharing parameters or tables does not determine the classification. The policy inside the target does.

### Fully worked example

Suppose behavior is $\epsilon$-greedy with $\epsilon=0.1$ over two actions in state $s'$. Then behavior chooses the greedy action with high probability but not with probability $1$. In particular, there is still some positive probability of choosing the non-greedy action.

If the update target is SARSA,

$$
R_{t+1} + \gamma Q(S_{t+1},A_{t+1}),
$$

then whatever action the behavior policy selected at $s'$, that is the continuation used inside the target. The target therefore tracks the value of the same exploratory policy.

If the update target is Q-learning,

$$
R_{t+1} + \gamma \max_{a'}Q(S_{t+1},a'),
$$

then the target always assumes the greedy continuation, even on those transitions where the behavior policy actually took the non-greedy exploratory action. This mismatch is exactly what off-policy means.

The general lesson is that on-policy/off-policy classification is determined by comparing two roles: who generated the data, and who appears inside the target.

### Misconception or counterexample block

**Do not define off-policy as “using old data” or “using replay.”** Those may appear in some off-policy systems, but off-policy itself means the behavior policy and target policy differ.

### Connection to later material

This policy-role distinction becomes foundational in more advanced RL, including importance sampling, experience replay, actor-critic variants, and offline RL. The chapter’s simple examples are the right place to build the concept correctly.

### Retain / Do not confuse

Retain that policy classification comes from comparing the data-generating policy to the policy implicit in the target continuation. Do not confuse shared parameters with shared policy role.

---

## 16. The method family map

### Why this section exists

By this point the chapter has introduced several methods that can feel similar because they all revolve around value functions and Bellman-style targets. This section exists to compress the full comparison into one conceptual map after the detailed explanations are already in place.

### The object being introduced

The object is a comparative method map. It answers the question: where does each method sit on the chapter’s organizing axes? What is fixed is the set of comparison axes introduced at the beginning. What varies is the method being classified.

### Formal definition

The chapter’s method family can be summarized as a structured comparison rather than as a slogan list.

Dynamic programming assumes the transition-reward model is available and therefore computes Bellman-style expectations exactly under that model. Its distinguishing feature is not merely that it is “iterative,” but that the expectation inside the backup is evaluated from known dynamics rather than estimated from samples.

Monte Carlo prediction removes model access and instead waits until a full sampled return is available. Its target is therefore an actually realized return, not a bootstrap estimate. That is why it is model-free and non-bootstrap at the same time.

One-step temporal-difference prediction also removes model access, but it does not wait for the full future to unfold. It uses one sampled transition and then bootstraps from the current value estimate of the next situation. Its identity therefore comes from combining sample-based learning with a bootstrap target.

SARSA inherits the one-step TD control structure but uses the next action actually sampled from the current behavior/target policy inside the continuation term. That is why it is on-policy: the same policy that generates the continuation action is the policy whose action values are being learned.

Q-learning keeps the sampled-transition-plus-bootstrap structure but replaces the actually sampled continuation action by a maximizing action inside the target. That is why its target policy can differ from the behavior policy, which is the conceptual core of its usual off-policy classification.

### Interpretation paragraph

This family map should now be read as a classification by mechanisms, not as a list to memorize. Dynamic programming is defined by exact model-based expectation. Monte Carlo is defined by full-return sampled targets. TD prediction is defined by one-step sample targets plus bootstrap. SARSA and Q-learning both sit inside the TD-control family, but they divide according to what policy appears in the continuation term. The point of the map is not that these methods lie on one simple line. The point is that different comparison axes answer different questions: where the target comes from, whether continuation is bootstrapped, what policy the continuation corresponds to, and what object is being updated.

### Boundary conditions / assumptions / failure modes

A common failure mode is to compress the whole map into “DP, MC, TD, SARSA, Q-learning” as a list of names without understanding what each one changes relative to the previous method. The names matter much less than the mechanism each name stands for.

### Fully worked example

Suppose someone gives the following update target:

$$
R_{t+1} + \gamma \max_{a'}Q(S_{t+1},a').
$$

Classify it systematically.

- It uses an observed one-step reward and next state, not an exact expectation under a model. Therefore it is sample-based, not dynamic programming.
- It does not use the complete realized return, because the continuation is given by a current estimate. Therefore it bootstraps and is not Monte Carlo.
- It is written in terms of $Q$, so it is an action-value method rather than a state-value method.
- The continuation uses a maximization rather than the sampled next action, so it is the Q-learning side of the action-value TD family.
- If behavior is exploratory, then behavior and target policies differ, so it is typically off-policy.

The general lesson is that the family map can be used actively as a classification tool, not just passively as a summary.

### Misconception or counterexample block

**Do not treat the family map as a historical sequence only.** It is primarily a structural comparison of targets, models, and policy roles.

### Connection to later material

Being able to locate a method on this map is the beginning of deeper RL literacy. Later algorithms are often hybrids or extensions of these families, and understanding them depends on recognizing which parts are inherited from which ancestors.

### Retain / Do not confuse

Retain the classification map as a set of mechanism checks. Do not confuse a method’s family identity with its reputation or popularity.

---

## 17. Common confusions this chapter is designed to block

### Why this section exists

This chapter introduces several methods that are easy to blur together, especially because all of them involve values, rewards, and Bellman-style expressions. This section exists to force the recurring confusions into explicit view.

### The object being introduced

The object is a misconception audit. It answers the question: where do learners most often misclassify the methods in this chapter? What is fixed is the core method definitions. What varies are the wrong simplifications learners often impose on them.

### Formal definition

Here are the major confusions the chapter is designed to prevent.

1. **Dynamic programming and TD are the same thing.**
2. **Monte Carlo and TD differ because one is “better.”**
3. **SARSA and Q-learning are almost identical because the formulas look similar.**
4. **On-policy versus off-policy is about whether exploration occurs.**
5. **$\epsilon$-greedy gives the greedy action probability $1-\epsilon$.**

### Interpretation paragraph

Each confusion results from focusing on the wrong feature. Dynamic programming and TD are related by Bellman structure, but they differ in whether expectation is computed exactly under a model or replaced by samples. Monte Carlo and TD differ in the target, not in a global quality ranking. SARSA and Q-learning look similar symbolically, but their continuation terms encode different target policies. On-policy and off-policy are policy-role distinctions, not exploration/no-exploration distinctions. And $\epsilon$-greedy probability must account for the exploratory branch selecting the greedy action as well.

### Boundary conditions / assumptions / failure modes

The chapter’s recurring failure mode is lexical learning: memorizing method names while leaving the mechanism blurry. If that happens, similar-looking formulas will be confused repeatedly. The cure is always the same: identify the target, identify whether it bootstraps, identify where the next action comes from, and identify whether a model is assumed.

### Fully worked example

Suppose a learner says: “Q-learning is on-policy because the agent acts $\epsilon$-greedily using the same $Q$ values it updates.”

Why is this wrong?

First, inspect the behavior policy. Yes, it may be $\epsilon$-greedy with respect to the current $Q$ values.

Second, inspect the target policy inside the update. The Q-learning target is

$$
R_{t+1} + \gamma \max_{a'}Q(S_{t+1},a').
$$

This target assumes greedy continuation, not $\epsilon$-greedy continuation.

Third, compare the two roles. If behavior sometimes takes non-greedy exploratory actions but the target always uses greedy continuation, behavior and target policies differ.

Therefore the method is typically off-policy.

The general lesson is that classification must be done by role comparison, not by noticing that the same parameter table is involved in both acting and learning.

### Misconception or counterexample block

**Do not confuse formula similarity with conceptual similarity.** In RL, one altered continuation term can change the learning target’s policy meaning entirely.

### Connection to later material

These misconception checks matter beyond this chapter. Many advanced RL methods are best understood by asking the same questions in more elaborate settings.

### Retain / Do not confuse

Retain that most confusion in this topic comes from looking at surface notation instead of target construction and policy role. Do not confuse symbolic resemblance with identical learning semantics.

---

## 18. What this chapter now entitles you to do

### Why this section exists

A chapter on algorithms should end by clarifying what understanding has been earned. Without that, the reader may remember formulas but not know what reasoning moves are now legitimate. This section exists to mark that transition explicitly.

### The object being introduced

The object is a capabilities summary. It answers the question: after mastering this chapter, what can the reader now classify, explain, and derive correctly? What is fixed is the material already covered. What varies is the kind of reasoning the reader is now prepared to carry out.

### Formal definition

After this chapter, the reader should be able to do all of the following.

1. Explain why dynamic programming is planning with a known model rather than direct learning from sampled experience.
2. Write the Bellman expectation and optimality backups underlying iterative policy evaluation and value iteration.
3. Distinguish Monte Carlo from TD by the exact form of the learning target.
4. Explain precisely what bootstrapping means.
5. Distinguish behavior policy from target policy.
6. Compute $\epsilon$-greedy action probabilities correctly.
7. Explain why SARSA is on-policy.
8. Explain why Q-learning is typically off-policy.

### Interpretation paragraph

These are not merely facts to recite. They are structural distinctions that make later reinforcement-learning material readable. If the reader can classify a new value-learning method by inspecting its target construction, model assumptions, and policy roles, then the chapter has achieved its purpose.

### Boundary conditions / assumptions / failure modes

A major failure mode is to think one understands the chapter because the names feel familiar. Familiarity is not mastery. The real test is whether one can explain each method’s mechanism in words, not just reproduce its equation.

### Fully worked example

Suppose a new method is proposed with target

$$
R_{t+1} + \gamma \sum_a \pi(a\mid S_{t+1})Q(S_{t+1},a).
$$

What can you now say immediately?

First, it is sample-based because it uses the observed one-step reward and next state rather than exact expectation under the model.

Second, it bootstraps because the continuation is given by the current action-value estimate $Q$.

Third, it is an action-value TD method because the target is built from $Q$ values.

Fourth, the continuation is averaged under a policy $\pi$ rather than maximized or sampled as a particular realized action. That already tells you this method differs structurally from both SARSA and Q-learning, even before you know its name.

The general lesson is that this chapter equips the reader to analyze new methods mechanistically.

### Misconception or counterexample block

**Do not conclude that a chapter is mastered because its canonical five names are recognizable.** Mastery means being able to parse new targets and classify them correctly.

### Connection to later material

Later chapters on multi-step methods, eligibility traces, function approximation, actor-critic methods, and off-policy correction all build directly on the distinctions established here.

### Retain / Do not confuse

Retain that the chapter’s real achievement is a classification and interpretation toolkit. Do not confuse name recognition with mechanism-level understanding.

---

## 19. Mastery check

A serious reader should be able to answer the following questions in complete sentences, with all relevant variables and assumptions made explicit.

1. What makes dynamic programming a planning method rather than a direct sample-based learning method?
2. In iterative policy evaluation, what exactly is being averaged, and under what distribution is that averaging performed?
3. In value iteration, what changes relative to policy evaluation and what stays the same?
4. What exact target does Monte Carlo use after a visit to a state, and why is that target not a bootstrap target?
5. What exact target does one-step TD use, and why is that target called a bootstrap target?
6. What is the difference between a behavior policy and a target policy?
7. Under standard $\epsilon$-greedy with a unique greedy action, what probability does the greedy action receive, and why is it not merely $1-\epsilon$?
8. In SARSA, what determines the continuation term in the target?
9. In Q-learning, what replaces SARSA’s continuation term, and why does that replacement matter conceptually?
10. Why is SARSA on-policy while Q-learning is typically off-policy?

If any one of these answers still feels blurry, the right move is to revisit the relevant section and identify exactly which axis is being mixed up. That is the point where understanding usually breaks.
