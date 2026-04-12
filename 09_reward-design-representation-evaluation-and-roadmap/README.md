# Chapter 9 — Reward Design, Representation, Evaluation, and Roadmap

*Rewritten as mastery-oriented teaching notes from the source chapter at the linked repository directory, following the uploaded writing standard.*

## What this chapter is for

A course in reinforcement learning can become dangerously misleading if it stops at algorithms. It is possible to derive Bellman equations correctly, implement policy optimization correctly, and still produce results that are conceptually wrong because the reward was poorly chosen, the state representation was not actually Markov, or the evaluation protocol did not justify the claim being made. This chapter exists to close that gap.

The topics here are often mislabeled as “practical considerations,” as though they were secondary details added after the real theory is done. That framing is backwards. Reward design determines what objective the agent is truly optimizing. Representation determines what information the learner actually has access to when making predictions and choosing actions. Evaluation determines whether an empirical result counts as evidence at all. If any one of these is mishandled, then even a perfectly implemented algorithm may solve the wrong problem, learn from the wrong inputs, or appear better than it really is.

This chapter therefore stabilizes four distinctions that later work depends on. First, reward, return, and value are different mathematical objects, and confusing them leads to wrong reasoning about what an RL agent is maximizing. Second, reward shaping is not automatically harmless; only particular shaping constructions come with provable invariance guarantees. Third, a compact representation is not automatically a sufficient state representation; aliasing can silently destroy the Markov property. Fourth, evaluation in RL is intrinsically noisy and protocol-sensitive, so a result is only as meaningful as the reporting discipline behind it.

The local hierarchy should be stated once with maximal sharpness. A **reward** is the one-step scalar signal produced by the environment at a particular time. A **return** is an aggregate of future rewards across time from a specified decision point onward. A **value** is an expectation of return under stated conditioning and under the trajectory law induced by a policy and environment. These are not three names for “how good things are.” They answer three different questions: what happened now, what accumulates from now onward, and what expected long-run quantity is associated with a condition such as a state, state-action pair, or policy.

The chapter closes with a roadmap because these issues also define how the subject naturally grows. Once reward specification, state sufficiency, and evaluation discipline are understood, the next questions are no longer “which update rule do I memorize?” but “what problem am I actually solving, with what information, and how do I know the evidence supports the claim?”

---

## 1. Reward, return, and value are different objects

### Why this section exists

Earlier chapters introduce one-step rewards, discounted returns, and value functions, but students frequently blur them together because all three are numerically related to performance. That blur causes serious errors. A statement about an immediate reward can be mistaken for a statement about long-run desirability. A statement about return can be mistaken for a state-based prediction object. A statement about value can be mistaken for something directly observed in the environment. This section must come first because the rest of the chapter depends on knowing exactly which object changes when the reward is redesigned, which object is preserved under shaping, and which object is estimated during evaluation.

### The object being introduced

There are really three objects here, not one.

The **immediate reward** is a one-step signal produced by the environment after an action is taken. It answers the local question: what scalar feedback was produced on this transition?

The **return** is an aggregate of future rewards from some time onward. It answers the temporal question: what total future payoff, usually discounted, is attached to continuing from here?

The **value function** is an expectation of return under specified conditioning and policy assumptions. It answers the predictive question: if the agent is in a given informational situation and then behaves according to a particular policy, what return should it expect on average?

What is fixed differs across the three objects. For reward, the relevant transition is fixed and the observed scalar is produced. For return, the starting time is fixed and future rewards vary along the realized trajectory. For value, the conditioning information and policy are fixed, while the future trajectory remains random.

### Formal definition

The one-step reward observed after action $A_t$ is

$$
R_{t+1}.
$$

The discounted return from time $t$ in the continuing setting is

$$
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}.
$$

A state-action value function under policy $\pi$ is

$$
Q^\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t = s, A_t = a].
$$

A state-value function is similarly

$$
V^\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s].
$$

### Interpretation paragraph

These definitions describe three different stages of abstraction.

Reward is directly generated by the environment on a single transition. It is not an average and not an aggregate. It is the raw one-step feedback.

Return is not observed all at once at time $t$; it is a random variable built from the stream of future rewards that follows time $t$. It summarizes long-run consequences rather than local outcomes.

Value is one level more abstract still. It is not a realized total. It is an expectation of return, conditional on some information such as the present state or state-action pair, and relative to a particular policy. Value is therefore a prediction object. It is what a learner tries to estimate when it learns “how good” a situation is under a policy.

The first thing to notice is that these objects answer different questions. Reward answers what happened now. Return answers what eventually accumulates. Value answers what should be expected on average under stated conditions.

### Boundary conditions / assumptions / failure modes

The return formula shown above is the standard continuing discounted definition. For it to be well-defined in the infinite-horizon setting, one typically assumes bounded rewards and $0 \le \gamma < 1$.

The value function depends on both the policy and the conditioning information. A symbol like $Q^\pi(s,a)$ is meaningless unless one knows what policy $\pi$ is and what return convention is being used.

A common failure mode is to say things like “the reward of a state” when the actual object being discussed is a value estimate. Another is to compare policies based only on immediate rewards when the task is genuinely multi-step and long-horizon.

An especially important boundary case occurs when $\gamma = 0$. Then

$$
G_t = R_{t+1},
$$

so maximizing return collapses to maximizing immediate reward. Outside that degenerate one-step case, reinforcement learning is not simply reward maximization in the local sense.

### Fully worked example

Consider a two-action navigation problem. From state $s$, action $a_1$ yields an immediate reward of $5$ and sends the agent into a trap state that produces rewards of $-10$ forever after. Action $a_2$ yields an immediate reward of $0$ but moves the agent into a corridor that yields rewards of $3$ for many future steps. Let the discount factor be $\gamma = 0.9$.

We now identify the three objects carefully.

First, the **immediate reward** from taking $a_1$ at time $t$ is simply

$$
R_{t+1} = 5.
$$

For $a_2$, it is

$$
R_{t+1} = 0.
$$

If one stopped here, one would conclude that $a_1$ is better because $5 > 0$. But that is only a statement about one-step reward.

Now consider the **return**. If the agent takes $a_1$ and then receives $-10$ forever after, the realized return from time $t$ is

$$
G_t^{(a_1)} = 5 + 0.9(-10) + 0.9^2(-10) + 0.9^3(-10) + \cdots.
$$

Factor the infinite tail:

$$
G_t^{(a_1)} = 5 - 10\sum_{k=1}^{\infty}0.9^k.
$$

Using

$$
\sum_{k=1}^{\infty}0.9^k = \frac{0.9}{1-0.9}=9,
$$

we get

$$
G_t^{(a_1)} = 5 - 10(9) = -85.
$$

Now for action $a_2$, suppose the reward stream is $0, 3, 3, 3, \ldots$. Then

$$
G_t^{(a_2)} = 0 + 0.9(3) + 0.9^2(3) + 0.9^3(3) + \cdots.
$$

Factor the tail:

$$
G_t^{(a_2)} = 3\sum_{k=1}^{\infty}0.9^k = 3(9) = 27.
$$

So the return of $a_2$ is far larger even though its immediate reward is smaller.

Finally, the **value** or action-value is the expected return under a specified policy. If these consequences are deterministic, then

$$
Q^\pi(s,a_1) = -85, \qquad Q^\pi(s,a_2) = 27,
$$

for any policy whose future behavior is already built into the described consequences.

The reasoning pattern is what matters. First identify whether you are being asked about a local signal, an accumulated future, or an expectation of that accumulation. Then compute the corresponding object. The general lesson is that a large one-step reward can be a poor choice when long-run consequences are bad.

### Misconception or counterexample block

**Do not confuse reward with value.**

A state or action can have low immediate reward but high value if it leads to strong future outcomes. Conversely, a transition with high immediate reward can have low value if it causes poor long-run consequences.

**This does not mean value is directly observed.**

Reward is observed on a transition. Value is inferred or estimated as an expectation of return.

### Connection to later material

This distinction is foundational for the rest of the chapter. Reward design literally changes the one-step signal. That change propagates into return and therefore into value. Potential-based shaping works by modifying reward in a way that induces a controlled transformation of return and value. Evaluation depends on which of these objects is actually being reported: one-step rewards, episodic returns, or learned value estimates.

### Retain / Do not confuse

Retain that reward is one-step, return aggregates future rewards, and value is an expectation of return. Do not confuse a larger immediate reward with a better long-run decision unless the problem really is one-step.

---

## 2. Potential-based reward shaping

### Why this section exists

Once reward, return, and value have been separated, the natural next question is whether one can alter the reward signal to make learning easier without changing the underlying control problem. This question appears because many RL tasks have sparse or delayed rewards, making credit assignment difficult. Reward shaping is introduced as a possible remedy. But shaping is dangerous unless the modification preserves what “optimal behavior” means. This section therefore introduces the one shaping construction that comes with a clean invariance story.

### The object being introduced

The object is a **shaped reward** constructed from an original reward and a potential function over states. The potential function assigns a scalar score to each state. The shaping term then compares the potential of successive states in a discount-consistent way.

What is fixed is the original MDP, its discount factor $\gamma$, and a chosen potential function $\Phi : \mathcal{S} \to \mathbb{R}$. What varies across transitions is the current state $S_t$ and next state $S_{t+1}$. The question this object answers is: can we modify the local reward signal so that learning receives denser guidance while preserving the set of optimal policies?

### Formal definition

Let the original reward on a transition be $r_t$. Choose a potential function

$$
\Phi : \mathcal{S} \to \mathbb{R}.
$$

Define the shaped reward by

$$
r_t' = r_t + \gamma \Phi(S_{t+1}) - \Phi(S_t).
$$

Equivalently, in random-variable notation one may write

$$
R_{t+1}' = R_{t+1} + \gamma \Phi(S_{t+1}) - \Phi(S_t).
$$

### Interpretation paragraph

The shaping term adds a bonus for moving toward higher-potential states and a penalty for moving away from them, but it does so in a carefully structured way. The coefficient $\gamma$ on the next-state potential is not arbitrary. It aligns the shaping with the same discount convention used in return. This alignment is what later creates the telescoping effect.

The first thing the reader should notice is that the shaping term is not simply “extra reward for good-looking states.” It is a **difference of potentials across successive states**, adjusted by discounting. That structure is exactly what prevents arbitrary distortion of long-run preferences.

### Boundary conditions / assumptions / failure modes

The invariance story depends on standard discounted RL assumptions. In the usual continuing or episodic discounted setting, one assumes the same discount factor is used in both the original return definition and the shaping term.

If the shaping term is chosen arbitrarily rather than as a potential difference, there is generally no guarantee that optimal policies will be preserved. The modified reward may redefine the problem rather than merely accelerate learning.

Another hidden condition is that the shaping function is defined over states in the standard theorem presented here. More general variants exist, but the cleanest form and the one relevant to the course notes is state-based potential shaping.

### Fully worked example

Suppose an agent is navigating toward a goal. Let the discount factor be $\gamma = 0.9$. Choose a simple potential function based on closeness to the goal:

$$
\Phi(s_0)=1, \qquad \Phi(s_1)=4, \qquad \Phi(s_2)=7.
$$

Assume the original rewards along a three-step trajectory are

$$
r_0=0, \qquad r_1=0, \qquad r_2=10,
$$

with visited states

$$
S_0=s_0, \quad S_1=s_1, \quad S_2=s_2, \quad S_3=\text{goal terminal}.
$$

Take the terminal potential to be zero for simplicity:

$$
\Phi(S_3)=0.
$$

We now compute each shaped reward.

For the first transition,

$$
r_0' = r_0 + \gamma\Phi(S_1)-\Phi(S_0)=0 + 0.9(4)-1=3.6-1=2.6.
$$

For the second transition,

$$
r_1' = r_1 + \gamma\Phi(S_2)-\Phi(S_1)=0 + 0.9(7)-4=6.3-4=2.3.
$$

For the third transition,

$$
r_2' = r_2 + \gamma\Phi(S_3)-\Phi(S_2)=10 + 0.9(0)-7=3.
$$

So the shaped reward sequence is

$$
2.6, \quad 2.3, \quad 3.
$$

At first sight this looks like a very different problem: instead of sparse terminal reward, the agent now gets informative intermediate signals. But the important check is not the individual shaped rewards. The important check is the total shaped return.

The original discounted return from time $0$ is

$$
G_0 = 0 + 0.9(0) + 0.9^2(10)=8.1.
$$

The shaped discounted return is

$$
G_0' = 2.6 + 0.9(2.3) + 0.9^2(3).
$$

Compute it:

$$
G_0' = 2.6 + 2.07 + 2.43 = 7.10.
$$

Now compare this to the original return adjusted by the boundary term. Since $\Phi(S_0)=1$,

$$
G_0 - \Phi(S_0)=8.1 - 1 = 7.1.
$$

They match exactly.

The conclusion is that shaping altered the step-by-step feedback dramatically while preserving the trajectory preference structure up to a boundary adjustment that does not depend on the intermediate path in an arbitrary way. The general lesson is that shaping can densify credit assignment without necessarily redefining what counts as a better policy.

### Misconception or counterexample block

**Do not confuse “reward shaping” with “adding any useful bonus.”**

A hand-designed bonus for visiting certain states may speed up learning, but it may also change which policies are optimal. The claim of policy preservation is not true for arbitrary reward tweaks.

**This does not mean shaped rewards are fake or irrelevant.**

They can substantially affect learning speed, exploration behavior, and stability. What is preserved under the theorem is the optimal-policy set, not the learning dynamics.

### Connection to later material

Potential-based shaping is one of the cleanest examples in RL of changing local signals while controlling global meaning. It also trains the reader to ask an important question that reappears in representation learning and evaluation: when a modification is made, does it merely help optimization, or does it redefine the problem? That distinction matters in every advanced RL setting.

### Retain / Do not confuse

Retain that potential-based shaping uses a discount-consistent difference of potentials across successive states. Do not confuse theorem-backed shaping with arbitrary reward engineering.

---

## 3. Why the telescoping effect matters

### Why this section exists

The previous section gave the shaping formula, but the central reason it works has not yet been explained in full. Without seeing the telescoping structure, a reader may treat policy preservation as a magical theorem rather than a consequence of algebra. This section exists to expose the mechanism directly.

### The object being introduced

The object is the cumulative contribution of the shaping terms along a trajectory. The question is: when the shaped rewards are summed into a return, what happens to all those potential terms inserted at each step?

What is fixed is a trajectory and the shaping rule

$$
R_{t+1}' = R_{t+1} + \gamma\Phi(S_{t+1}) - \Phi(S_t).
$$

What varies is the time index across the trajectory. The conclusion allowed is that most intermediate potential terms cancel, leaving only boundary terms.

### Formal definition

Using the shaped reward inside the discounted return gives

$$
G_t' = \sum_{k=0}^{\infty} \gamma^k \left(R_{t+k+1} + \gamma\Phi(S_{t+k+1}) - \Phi(S_{t+k})\right).
$$

Split the sum into original return plus shaping contribution:

$$
G_t' = G_t + \sum_{k=0}^{\infty} \gamma^k\left(\gamma\Phi(S_{t+k+1}) - \Phi(S_{t+k})\right).
$$

The shaping part telescopes:

$$
\sum_{k=0}^{\infty} \gamma^k\left(\gamma\Phi(S_{t+k+1}) - \Phi(S_{t+k})\right)
= -\Phi(S_t)
$$

under the standard infinite-horizon bounded-tail assumptions, or more generally equals a boundary difference with the terminal or limiting term made explicit.

### Interpretation paragraph

To understand telescoping, do not start by thinking of advanced theorems. Start by expanding the first few terms. The negative $-\Phi(S_t)$ from one term is followed by a positive discounted copy of the next state’s potential, and the pattern repeats. Each intermediate state potential appears once with a negative sign and once with a positive sign multiplied by exactly the right discount factor to match the overall return weighting. The internal terms cancel. What survives are the endpoints.

This is the reason the shaping is structured as a discounted difference rather than as an arbitrary bonus. It makes the total shaping contribution depend mainly on where the trajectory starts and ends, not on uncontrolled distortions along the way.

### Boundary conditions / assumptions / failure modes

The cancellation is exact in finite-horizon episodic settings when the terminal boundary term is written explicitly. In infinite-horizon settings, one needs the remaining tail term to vanish or converge appropriately. Standard boundedness and discount assumptions are what make that tail manageable.

A common failure mode is to wave at “telescoping” without expanding any terms. That is where understanding gets lost. Another failure mode is to forget that the discounts matter: without the $\gamma$ in front of $\Phi(S_{t+1})$, the cancellation would not line up with the discounted return weights.

### Fully worked example

Work in a finite-horizon episode from time $0$ to time $2$. The shaping contribution to the return is

$$
\sum_{k=0}^{2} \gamma^k\left(\gamma\Phi(S_{k+1}) - \Phi(S_k)\right).
$$

Expand this term by term:

$$
\gamma^0(\gamma\Phi(S_1)-\Phi(S_0))
+ \gamma^1(\gamma\Phi(S_2)-\Phi(S_1))
+ \gamma^2(\gamma\Phi(S_3)-\Phi(S_2)).
$$

Now distribute the powers of $\gamma$:

$$
\gamma\Phi(S_1)-\Phi(S_0)
+ \gamma^2\Phi(S_2)-\gamma\Phi(S_1)
+ \gamma^3\Phi(S_3)-\gamma^2\Phi(S_2).
$$

Now line up like terms:

- $+\gamma\Phi(S_1)$ cancels with $-\gamma\Phi(S_1)$.
- $+\gamma^2\Phi(S_2)$ cancels with $-\gamma^2\Phi(S_2)$.

What remains is

$$
-\Phi(S_0) + \gamma^3\Phi(S_3).
$$

So in the finite-horizon case,

$$
G_0' = G_0 - \Phi(S_0) + \gamma^3\Phi(S_3).
$$

If the terminal potential is chosen to be zero, then

$$
G_0' = G_0 - \Phi(S_0).
$$

Notice what this means. Every intermediate state potential disappeared from the final expression. The shaped return does not accumulate arbitrary path-specific bias from those intermediate states. The general lesson is that the shaping effect is structurally controlled by endpoint information, which is why policy preferences can be preserved.

### Misconception or counterexample block

**Do not say “the potentials cancel” without qualification.**

The intermediate potentials cancel. Boundary terms remain. Those boundary terms are exactly what matter for the invariance argument.

**This does not mean all trajectories get the same shaped return shift.**

The endpoint terms can differ across trajectories if the terminal boundary differs. The precise preservation claim must therefore be stated under the standard theorem conditions, not as a vague slogan.

### Connection to later material

This kind of structured cancellation is a recurring pattern in RL and optimization. It is also a model for how one should reason about theorem-backed engineering changes: identify the algebraic invariant, then check exactly what survives at the boundaries. That habit becomes valuable in eligibility traces, advantage baselines, and other variance-reduction constructions.

### Retain / Do not confuse

Retain that potential-based shaping works because intermediate potential terms telescope in the discounted return. Do not confuse telescoping with total disappearance; the boundary terms are the key survivors.

---

## 4. Why reward design is not cosmetic

### Why this section exists

After seeing a safe shaping construction, the reader might overcorrect and think reward modifications are generally harmless as long as they are intuitively reasonable. This section exists to stop that mistake. In RL, the reward function is not a commentary layered on top of a fixed objective. It is the objective signal that defines what the learner is optimizing.

### The object being introduced

The object is the reward specification itself as part of the task definition. The question it answers is not “how do we score behavior after the fact?” but “what consequences are being incentivized during learning?”

What is fixed is the transition structure of the environment, unless one is redefining that as well. What varies is the scalar reward assigned to transitions, events, or outcomes. The conclusion allowed is that changing reward generally changes optimal behavior unless a specific invariance theorem applies.

### Formal definition

There is no single new formula here beyond the general RL setup: the reward function is the mapping that determines the distribution of the one-step reward variable, often as part of

$$
P(s',r \mid s,a).
$$

When the reward function is altered, the induced return

$$
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}
$$

changes as well, and therefore so do the value functions defined as expectations of that return.

### Interpretation paragraph

A reward function encodes preferences over trajectories by assigning local signals whose accumulated effect determines return. This means reward design is a way of specifying the control problem itself. Add a step penalty, and you bias toward shorter routes. Add a survival bonus, and you encourage delaying termination. Add a large terminal bonus, and you may encourage risky strategies that pursue rare but high-payoff endings.

The first thing to notice is that changing reward is not merely making the learner “care more clearly” about the same thing. Very often it changes what the learner should rationally prefer.

### Boundary conditions / assumptions / failure modes

The main exception is when the reward modification belongs to a family with a proven invariance property, such as potential-based shaping under the standard assumptions. Outside such special constructions, a reward change should be treated as a problem-definition change.

A common failure mode is to add “helpful” intermediate rewards while still claiming to solve the original task. That claim is only justified if one proves or cites an invariance result. Another is to confuse human interpretability of the reward with fidelity to the intended objective.

### Fully worked example

Suppose an agent must choose between two routes to a goal.

- **Route A** reaches the goal in 2 steps and yields terminal reward $10$.
- **Route B** reaches the goal in 4 steps and yields terminal reward $10$.

Assume discounting is $\gamma = 1$ for simplicity in this finite-horizon example, and consider two reward designs.

#### Reward design 1: terminal reward only

The reward is zero on nonterminal steps and $10$ on reaching the goal.

Then the total return for each route is simply

$$
G^{(A)} = 10, \qquad G^{(B)} = 10.
$$

Under this reward design, the agent is indifferent between the routes.

#### Reward design 2: terminal reward plus living penalty

Now add a living penalty of $-1$ at each nonterminal step, while keeping terminal reward $10$.

Route A has one nonterminal transition before reaching the goal on the second step, so its return is

$$
G^{(A)} = -1 + 10 = 9.
$$

Route B has three nonterminal transitions before reaching the goal on the fourth step, so its return is

$$
G^{(B)} = -1 + (-1) + (-1) + 10 = 7.
$$

Now Route A is preferred.

What changed? The environment dynamics did not change. The goal did not change. The terminal reward did not change. Only the reward specification changed. Yet the preference ordering over policies changed materially.

The general lesson is that reward design shapes the optimization landscape directly. When you change reward, always ask which trajectory tradeoffs you are changing: speed, safety, path length, risk exposure, or delayed payoff.

### Misconception or counterexample block

**Do not say “the task is the same, we just changed the reward a little.”**

If the induced return ordering over policies changes, then from the standpoint of optimization the task has changed.

**This does not mean reward design is illegitimate.**

It means it is powerful and should be treated with the seriousness of problem specification, not as a cosmetic tuning layer.

### Connection to later material

Reward misspecification is one of the main reasons real RL systems fail to exhibit intended behavior. This section therefore connects directly to alignment, offline evaluation, inverse RL, preference learning, and safe RL. The theme is always the same: optimization will faithfully pursue the objective you encoded, not the one you vaguely intended.

### Retain / Do not confuse

Retain that reward design usually changes the control objective. Do not confuse “easier to learn from” with “equivalent to the original task” unless a preservation theorem applies.

---

## 5. Representation and non-Markov aliasing

### Why this section exists

Up to this point, much of RL theory is written as if the agent’s state is a sufficient summary of the future. But in practice, one often feeds the learner an observation, feature vector, compressed state, or learned embedding rather than the full latent state. This section must appear now because reward design alone does not determine learning success. Even with a correct reward, learning can fail if the representation given to the agent destroys the predictive sufficiency that the Markov property requires.

### The object being introduced

The object is a **representation** of the underlying situation, together with the phenomenon of **aliasing**. A representation maps latent situations to a smaller observable or encoded object. Aliasing occurs when two distinct latent situations map to the same representation even though they imply different future reward or transition laws under the same action.

What is fixed is the representation map and the action under consideration. What varies are the latent situations that may collapse to the same observed representation. The question this object answers is: does the representation preserve enough information for Markov prediction and control?

### Formal definition

A representation is Markov-sufficient if, for any represented state $x$ and action $a$, the future transition-reward law depends only on $x$ and $a$, not on additional hidden distinctions among latent histories or latent states that map to $x$.

Aliasing occurs when there exist two latent situations $z$ and $z'$ such that

$$
\phi(z) = \phi(z') = x,
$$

but for some action $a$,

$$
P(\text{future} \mid z,a) \neq P(\text{future} \mid z',a).
$$

In particular, one may already see the violation at the one-step level if either

$$
P(S_{t+1},R_{t+1} \mid z,a) \neq P(S_{t+1},R_{t+1} \mid z',a).
$$

### Interpretation paragraph

A Markov representation is one that tells the learner everything it needs, at least for prediction and control under the model class being assumed. Aliasing means the learner is being shown one input symbol for multiple genuinely different predictive situations. The learner is then asked to assign one value estimate or one action choice to circumstances that should be treated differently.

The first thing to notice is that compactness and sufficiency are different properties. A small representation may be desirable computationally, but if it merges situations that matter for future evolution, it is not a valid state representation for Markov RL reasoning.

### Boundary conditions / assumptions / failure modes

A representation can be useful without being perfectly Markov, but then the clean MDP theory no longer applies exactly. One must be honest about the approximation.

A common failure mode is to say “the representation works well empirically, so it is Markov enough” without checking the task’s predictive requirements. Another is to focus only on immediate reward aliasing while ignoring transition aliasing. A representation can preserve immediate rewards yet still fail because future dynamics differ.

### Fully worked example

Consider a partially observed corridor task. The latent world has two states, $z_L$ and $z_R$, that look identical to the agent: both produce the same observation

$$
\phi(z_L)=\phi(z_R)=x.
$$

Suppose the available actions are Left and Right.

- In latent state $z_L$, taking action Right reaches the goal with reward $+5$ and terminates.
- In latent state $z_R$, taking action Right falls into a pit with reward $-5$ and terminates.

From the represented state $x$, the agent cannot distinguish whether it is really in $z_L$ or $z_R$.

Now check the Markov condition. If the representation were Markov-sufficient, then conditioning on $x$ and the chosen action should determine the relevant future law. But here, under the same represented state $x$ and same action Right, the next-step reward law depends on which latent situation actually holds:

$$
P(R_{t+1}=5 \mid z_L, \text{Right}) = 1,
$$

while

$$
P(R_{t+1}=-5 \mid z_R, \text{Right}) = 1.
$$

So the one-step transition-reward law is not determined by $x$ alone. The representation aliases two different predictive states.

What does this do to value learning? If the learner must assign a single action-value $Q(x,\text{Right})$, it will average over the hidden cases according to their frequencies. If the hidden cases occur equally often, it may learn something near zero. But zero is not a faithful description of either true latent state: in one case the correct action is extremely good, in the other it is extremely bad.

The general lesson is that when one representation is forced to stand in for multiple future-incompatible situations, value estimates and policies become compromised in a mathematically predictable way. In future problems, always ask whether the current input is sufficient to determine the future law relevant to decision making.

### Misconception or counterexample block

**Do not confuse observation with state.**

An observation is what the agent sees. A state in the Markov sense is an information summary sufficient for predicting the future under actions. Those are not automatically the same object.

**This does not mean every compressed representation is bad.**

Compression is good when it preserves decision-relevant predictive structure. The problem is not compactness itself; the problem is losing information that matters.

### Connection to later material

This section points directly toward partial observability, belief states, recurrent policies, predictive state representations, and representation learning for control. It also clarifies why some function approximation failures in RL are not merely optimization failures but information failures.

### Retain / Do not confuse

Retain that aliasing occurs when different latent predictive situations collapse to the same representation. Do not confuse a compact encoding with a Markov-sufficient state.

---

## 6. Evaluation methodology and why multiple seeds matter

### Why this section exists

Even if reward and representation are correct, one still needs evidence that an algorithm works. In RL, that evidence is unusually fragile because training is stochastic, environments may be stochastic, and performance can vary sharply from run to run. This section exists because many invalid empirical claims come from reporting a single strong run, a single cherry-picked curve, or a protocol with too many hidden degrees of freedom.

### The object being introduced

The object is an evaluation protocol over repeated runs. Suppose an algorithm is trained multiple times under independently randomized conditions and produces evaluation returns

$$
X_1, X_2, \ldots, X_N.
$$

These are random outcomes of the training-and-evaluation procedure, not fixed constants known in advance. What is fixed is the algorithm, environment, budget, and reporting protocol. What varies across runs are the random seeds and all stochastic consequences they induce. The question this object answers is: what performance should we report, and how do we quantify variability across runs?

### Formal definition

Given returns from $N$ independent runs,

$$
X_1, X_2, \ldots, X_N,
$$

the sample mean is

$$
\widehat\mu_N = \frac{1}{N}\sum_{i=1}^N X_i.
$$

One may also report sample variance, standard deviation, confidence intervals, interquartile range, or other uncertainty summaries, depending on the protocol.

### Interpretation paragraph

The sample mean is an estimate of average performance across the randomness of the experimental procedure. It is not the performance of a particular run, and it is not a guarantee of what will happen on the next run. Multiple seeds matter because the question is rarely “can this algorithm sometimes work?” The real question is “what performance does this method typically deliver under the stated protocol?”

The first thing to notice is that stochasticity enters at many levels: parameter initialization, minibatch order, exploration randomness, simulator randomness, environment randomness, and sometimes even nondeterminism in hardware or implementation details. A single run cannot distinguish a robust method from a lucky one.

### Boundary conditions / assumptions / failure modes

The simple interpretation of $\widehat\mu_N$ assumes the runs are meaningfully comparable and produced under the same protocol except for the intended randomization. If the training budget, reward scale, evaluation frequency, or environment version changes across runs, then averaging them is not clean evidence.

A common failure mode is to report the best seed rather than the distribution across seeds. Another is to average training rewards rather than evaluation returns without making that distinction explicit. Yet another is to report a mean with no spread measure, making it impossible to assess stability.

### Fully worked example

Suppose an RL algorithm is trained under five independent random seeds and evaluated at the end of training. The final evaluation returns are

$$
X_1 = 120, \quad X_2 = 80, \quad X_3 = 140, \quad X_4 = 60, \quad X_5 = 100.
$$

We first identify the object: these are not five environment rewards from one episode. They are five end-of-training evaluation outcomes from five independent runs of the full training procedure.

Now compute the sample mean:

$$
\widehat\mu_5 = \frac{1}{5}(120+80+140+60+100).
$$

Add the returns:

$$
120+80+140+60+100 = 500.
$$

Divide by $5$:

$$
\widehat\mu_5 = 100.
$$

So the average reported performance is $100$.

Now compare this to what a single run would have implied. If one had reported only the third seed, the claim might have been “the method gets 140.” If one had reported only the fourth seed, the claim might have been “the method gets 60.” Neither statement fairly represents the typical behavior of the method under the given stochastic protocol.

The spread is also substantial. The results range from $60$ to $140$, which already signals nontrivial instability. Even without computing a full uncertainty interval, one can see that “average performance is 100” tells only part of the story; the method’s reliability is also an empirical property that needs reporting.

The general lesson is that repeated seeds do not merely make a plot look more professional. They reveal whether a method is consistently good, erratic, brittle, or occasionally excellent but unreliable.

### Misconception or counterexample block

**Do not confuse “one good run exists” with “the method is good.”**

Existence of a lucky run shows possibility, not reliability.

**This does not mean the sample mean alone is enough.**

A mean without a measure of spread can hide severe instability. Two methods with the same mean can differ radically in reliability.

### Connection to later material

Evaluation methodology becomes even more important in offline RL, model-based RL, large-scale benchmarking, and hyperparameter-sensitive deep RL. As problems become harder and pipelines more complex, protocol clarity becomes part of the scientific contribution rather than a bureaucratic appendix.

### Retain / Do not confuse

Retain that multiple seeds are necessary because RL outcomes can vary materially across runs. Do not confuse a single strong run with credible evidence about a method’s typical performance.

---

## 7. What a credible evaluation report must specify

### Why this section exists

The previous section explained why repeated evaluation is necessary. The next gap is that even multiple seeds are not enough if the protocol itself is underspecified. A result cannot be interpreted if the reader does not know what was trained, on what inputs, under which reward, for how long, and how performance was measured. This section exists to make explicit what information must be reported for an RL result to be scientifically interpretable.

### The object being introduced

The object is a **reporting protocol**: the list of experimental ingredients that must be fixed and disclosed so the reported result has meaning. What is fixed are the environment, task, representation, training budget, and evaluation conditions. What varies across seeds should be only the intended random sources, not hidden experimental choices.

### Formal definition

A credible evaluation report should specify at least the following:

1. the environment and task definition,
2. the reward specification,
3. the observation or state representation,
4. the training budget,
5. the evaluation policy,
6. the number of seeds,
7. the summary statistic across seeds,
8. a measure of spread or uncertainty,
9. and ablations or controlled comparisons that isolate major components.

### Interpretation paragraph

Each item on this list answers a different ambiguity.

The environment and task define what problem was solved. The reward specification defines the actual objective. The representation tells us what information the learner had. The training budget determines whether a method is sample efficient or simply overtrained. The evaluation policy clarifies whether one reports greedy behavior, stochastic behavior, or something else. The number of seeds and summary statistics tell us whether the result is typical. The uncertainty measure tells us how stable it is. Ablations tell us which ingredients actually matter.

The first thing to notice is that missing any one of these can invalidate comparisons. For example, if two methods are compared under different training budgets or different evaluation policies, the resulting numbers no longer answer the intended question cleanly.

### Boundary conditions / assumptions / failure modes

Different subfields may add further requirements, such as reporting hyperparameter search procedures, validation protocols, or environment versions. The list above is therefore a minimum, not an upper bound.

A common failure mode is selective transparency: detailed architecture description but vague reward definition, or many seeds but no statement of the evaluation policy, or strong averages but no uncertainty bars. Another is to bury critical protocol choices in appendices while foregrounding performance numbers that cannot be interpreted without them.

### Fully worked example

Suppose a paper claims: “Our method achieves average return 250 on Task X.” On its own, this claim is too underspecified to evaluate.

We now check what must be asked, one item at a time.

First, **what is Task X?** Is it a standard benchmark version, a modified simulator, or a custom environment? Without this, the number 250 floats without reference.

Second, **what reward was used?** If the reward included shaping terms or penalties absent from the standard task, then the result may not be comparable to prior work.

Third, **what did the agent observe?** If the method used privileged state information while the baseline used raw observations, the comparison is confounded.

Fourth, **what was the training budget?** An algorithm that reaches 250 only after ten times more experience than its baseline is solving a different practical problem than one that reaches 250 efficiently.

Fifth, **what evaluation policy produced the 250?** Was it the mean return under a stochastic exploration policy, or the performance of a deterministic greedy policy derived from the learned model?

Sixth and seventh, **over how many seeds and with what summary statistic?** A mean of 250 over ten seeds is a different claim from a best-seed performance of 250.

Eighth, **what uncertainty was reported?** If the mean is 250 with very high variance, the practical story differs from a tightly concentrated result.

Ninth, **what ablations were run?** If the method includes a new loss, a new architecture, and a new replay scheme, then without ablations one cannot tell which component actually contributed.

The final interpretation is that “average return 250” is not a self-contained scientific result. It becomes meaningful only when embedded inside a disciplined reporting protocol.

This point should be made even stricter. The evaluation protocol is not an appendix to the claim. It is part of the claim’s meaning. A reported return number without environment specification, reward definition, observation regime, seed protocol, evaluation policy, and ablation structure is not a fully formed empirical statement waiting only for cosmetic details. It is an incomplete statement whose evidential content cannot yet be determined.

That sentence can be made even stricter. A reported return number is not a self-contained fact waiting for contextual decoration. It is a statistic produced under a task definition, a reward specification, an observation regime, a training budget, an evaluation policy, and a seed protocol. Change those, and the meaning of the number changes. So in reinforcement learning, the empirical claim is not “the score was 250” with protocol attached later. The real claim is “under this fully specified experimental contract, the method produced this distribution of outcomes.” The protocol is part of the proposition.

The general lesson is that evaluation numbers are never self-explanatory. They derive meaning from the experimental contract around them.

### Misconception or counterexample block

**Do not confuse “a number is reported” with “evidence is reported.”**

A number without protocol context is often closer to advertising than to science.

**This does not mean every report must be maximalist.**

It means the key conditions that determine interpretability must be explicit.

### Connection to later material

Protocol discipline becomes even more central when comparing offline RL datasets, sim-to-real setups, preference-based objectives, or large-scale representation-learning systems. In all such settings, hidden protocol differences can dominate the apparent algorithmic effect.

### Retain / Do not confuse

Retain that credible evaluation is a protocol, not just a score. Do not confuse a headline number with a well-defined scientific claim.

---

### Reasoning synthesis: from reward design to credible evidence

At this point the chapter should make its larger logic explicit. Reward design determines what local signal the learner is pushed to optimize. Representation determines what information the learner is actually allowed to use when making predictions and decisions. Evaluation determines whether the resulting empirical evidence can support the claim being made. These are not three disconnected “practical topics.” They are three different places where the meaning of the learning problem can drift. A bad reward can redefine the problem. A bad representation can hide the information required for exact control reasoning. A bad evaluation protocol can make even a correct implementation look more convincing or less convincing than it should. The chapter’s unifying lesson is that reinforcement learning failures often come from mismatched meaning before they come from wrong algebra.

## 8. What an ablation is and what it is not

### Why this section exists

Ablation studies are frequently cited as evidence that a particular design component matters. But in practice, many so-called ablations change several things at once, making the conclusion logically unsupported. This section exists because evaluation is not only about repeating runs; it is also about isolating causal contribution within a system of interacting design choices.

### The object being introduced

The object is an **ablation**: a controlled comparison between a full system and a modified version in which one component is removed or changed while the rest of the protocol is kept fixed. What is fixed is everything not under test: environment, reward, budget, architecture, optimizer, and evaluation protocol. What varies is the single component being ablated.

The question an ablation answers is: what performance difference is attributable to this component under this controlled setup?

### Formal definition

An ablation is a controlled experiment in which one designated component is altered while the rest of the experimental pipeline is held fixed.

### Interpretation paragraph

The logic is simple but strict. If multiple ingredients change simultaneously, then any performance change cannot be attributed cleanly to one of them. A valid ablation is therefore not merely “we made a variant.” It is “we changed exactly the component whose contribution we are trying to isolate, while keeping the rest constant enough that the comparison is interpretable.”

The first thing to notice is that ablation is a causal-isolation idea, not a naming convention.

### Boundary conditions / assumptions / failure modes

In some systems, holding everything else exactly fixed may create mismatches or instability because components interact. When that happens, the researcher must explain the compromise honestly. But the burden remains: the closer the comparison is to single-component isolation, the stronger the inference.

A common failure mode is to remove one component and then retune several hyperparameters, change the network, and alter the optimizer “for fairness.” At that point the comparison is no longer a clean ablation of the original component.

### Fully worked example

Suppose a full RL method contains three major ingredients:

1. prioritized replay,
2. a target network,
3. an auxiliary consistency loss.

The full system is trained under a fixed environment, reward, network, optimizer, training budget, and evaluation protocol.

Now imagine two proposed comparisons.

#### Comparison A

Remove only the auxiliary consistency loss. Keep replay, target network, architecture, learning rate, budget, and evaluation procedure unchanged.

This is a clean ablation of the auxiliary consistency loss. If performance drops, the reader can reasonably attribute the change to the removal of that component, subject to the usual statistical uncertainty.

#### Comparison B

Remove the auxiliary loss, shrink the network for speed, reduce the replay buffer, and change the learning rate because the system became unstable.

This is not a clean ablation. Even if performance changes a lot, the result does not isolate the contribution of the auxiliary loss. The network, replay behavior, and optimization regime also changed.

The reasoning pattern to retain is the following. First, identify the component whose causal contribution is being tested. Second, check what else changed. Third, ask whether the resulting comparison still supports the causal claim being made. If not, it is a variant comparison, not an ablation in the strong sense.

### Misconception or counterexample block

**Do not confuse “component removed” with “component isolated.”**

A component may be removed in a study that also changes many other things. That does not make the study a clean ablation.

**This does not mean variant studies are useless.**

They can still be informative. They just support weaker claims than a controlled ablation does.

### Connection to later material

As RL systems become more modular—combining replay, exploration bonuses, representation losses, model components, and planning heads—the ability to isolate contributions becomes crucial. Ablation logic is therefore central not just to evaluation, but to scientific understanding of complex learning systems.

### Retain / Do not confuse

Retain that a true ablation isolates one component while the rest of the protocol stays fixed. Do not confuse a broad variant comparison with a clean causal isolation study.

---

## 9. Boundary conditions in living-reward and route analyses

### Why this section exists

Reward design becomes especially tangible in route-planning examples, grid worlds, and navigation problems where a living reward or step penalty changes path preference. These examples are often taught informally, but they are valuable precisely because they make the effect of reward design mathematically explicit. This section exists to connect the abstract warning about reward design to a concrete family of analyses.

### The object being introduced

The object is a comparison between candidate trajectories that differ in length, risk, or terminal payoff under a reward scheme that includes living reward or per-step cost. What is fixed is the environment’s route structure and the candidate policies being compared. What varies is the living reward parameter. The question is: how does changing the one-step reward shift which route has higher return?

### Formal definition

Suppose route $A$ has return $G^{(A)}$ and route $B$ has return $G^{(B)}$. Under a living reward $c$ added at each step, the total return of each route changes according to how many times that reward is accumulated. In a simple undiscounted finite setting, if route $A$ takes $n_A$ steps before terminal payoff $T_A$, then

$$
G^{(A)} = n_A c + T_A,
$$

with an analogous expression for route $B$.

### Interpretation paragraph

The point is not that living reward is special. The point is that once reward is part of return, the number of steps matters directly. A longer path accumulates the living reward more times. So if the living reward is negative, longer paths are penalized more heavily. If the living reward is positive, longer paths may become preferable, even if they delay termination.

The first thing to notice is that route preference is not determined by stepwise reasoning in isolation. It is determined by the total return comparison.

### Boundary conditions / assumptions / failure modes

The exact threshold at which one route becomes preferable depends on discounting, terminal rewards, and whether stochastic outcomes are involved. In discounted settings, later living rewards count less, so the dependence on path length is weighted rather than purely additive.

A common failure mode is to reason verbally—“a more negative living reward encourages faster completion”—without actually computing the threshold where the preference flips. In serious analysis, that threshold should be derived.

### Fully worked example

Consider two deterministic routes to a goal with discount factor $\gamma = 1$ for simplicity.

- Route A reaches the goal in 2 steps with terminal reward $8$.
- Route B reaches the goal in 4 steps with terminal reward $12$.

Let the living reward be $c$ per nonterminal step.

Now write the returns explicitly.

Route A has one nonterminal step before the terminal step, so

$$
G^{(A)} = c + 8.
$$

Route B has three nonterminal steps before the terminal step, so

$$
G^{(B)} = 3c + 12.
$$

We now compare routes by solving

$$
G^{(A)} > G^{(B)}.
$$

Substitute the formulas:

$$
c + 8 > 3c + 12.
$$

Rearrange:

$$
8 - 12 > 3c - c,
$$

so

$$
-4 > 2c,
$$

which gives

$$
c < -2.
$$

Now interpret the threshold.

- If the living reward is less than $-2$, Route A is preferred because the extra steps of Route B are too costly.
- If the living reward is greater than $-2$, Route B is preferred because its larger terminal reward outweighs the additional step costs.
- If $c=-2$, the routes are tied.

This is a clean mathematical demonstration that changing living reward changes the optimal policy region. Nothing philosophical is happening here. The return definition is doing exactly what it says.

The general lesson is that whenever a reward parameter is adjusted, route preferences can shift in threshold-like ways. In future tasks, the right move is to compute those thresholds explicitly rather than rely on vague intuition.

### Misconception or counterexample block

**Do not confuse “living reward encourages speed” with a universal law.**

A negative living reward tends to favor shorter paths, but the actual preference depends on terminal rewards, discounting, and risk structure.

**This does not mean reward design is arbitrary.**

It means the effect of reward design is mathematically analyzable and should be analyzed.

### Connection to later material

This style of threshold analysis appears in grid worlds, shortest-path tasks, risk-sensitive RL, and reward-parameter sweeps used in benchmarking. It also provides a useful mental model for how small reward changes can move policy boundaries in a systematic way.

### Retain / Do not confuse

Retain that living rewards affect route preference through accumulated return, not through rhetoric about “encouraging” behavior. Do not confuse a directional intuition with a full return comparison.

---

## 10. Roadmap: where the subject naturally goes next

### Why this section exists

A chapter like this can feel less algorithmic than earlier material, so it is important to make clear that these topics are not a detour. They are the conceptual ground that later extensions rely on. This section exists to show how the current chapter feeds directly into deeper RL topics.

### The object being introduced

The object is not a new theorem but a map of conceptual dependencies. What is fixed is the understanding built in this chapter: reward semantics, representation sufficiency, and evaluation discipline. What varies are the next directions one might pursue once that foundation is stable.

### Formal definition

Natural next topics after this chapter include:

- eligibility traces and multi-step methods,
- partial observability and belief-state ideas,
- deeper treatment of offline RL,
- model-based RL,
- and representation learning for control.

### Interpretation paragraph

Each of these directions depends on the distinctions developed here.

Eligibility traces and multi-step methods still optimize returns, so reward and return semantics remain central.

Partial observability and belief-state methods arise precisely because raw observations may not be Markov, which is the problem highlighted by aliasing.

Offline RL makes evaluation even more delicate because the data distribution is fixed and online correction is limited.

Model-based RL depends on predicting transition-reward structure accurately, which in turn depends on having suitable state representations.

Representation learning for control explicitly tackles the problem that compact encodings must preserve decision-relevant predictive content.

The first thing to notice is that this chapter is not about tidying up loose ends. It is about preventing later methods from resting on blurry assumptions.

### Boundary conditions / assumptions / failure modes

A failure mode at this stage is to treat later methods as independent toolkits. They are not. Their success depends on how well the foundational objects are specified. Another failure mode is to think that stronger algorithms compensate automatically for poor reward design or non-Markov representations. Often they do not.

### Fully worked example

Take partial observability as a concrete follow-on topic. Suppose a student asks why belief states are introduced in a later chapter. The answer can now be built step by step.

First, earlier MDP theory assumes current state is a sufficient summary for future prediction and control.

Second, this chapter showed that a compact observation may alias multiple latent predictive situations.

Third, if that aliasing breaks the Markov property, then value learning on raw observations becomes conceptually mismatched to the true decision problem.

Fourth, a belief state is introduced as a richer information object that summarizes uncertainty over latent states using the observation history.

The conclusion is that belief states are not an optional complication. They are the mathematically motivated response to the failure mode identified here.

This example illustrates the general lesson of the roadmap: later topics are answers to the exact foundational gaps stabilized in this chapter.

### Misconception or counterexample block

**Do not think “foundation chapters” are separate from advanced material.**

In RL, advanced methods often exist precisely because foundational assumptions fail in realistic settings.

### Connection to later material

This section is itself a connection to later material: it tells the reader what conceptual pressures produce the next wave of methods.

### Retain / Do not confuse

Retain that later RL topics grow out of the reward, representation, and evaluation issues stabilized here. Do not confuse conceptual foundations with optional background.

---

## 11. Common confusions blocked by this chapter

### Why this section exists

Mastery requires not only knowing the right distinctions but also recognizing the recurring wrong ones. The confusions listed here are dangerous because they look superficially reasonable and recur in both coursework and research discussions.

### The object being introduced

The object here is a collection of conceptual error patterns. Each one is a place where a reader may use the right words but connect them incorrectly.

### Formal definition

The major confusions blocked here are:

1. reward and value are the same thing,
2. reward shaping is always harmless,
3. a compact representation is automatically a good state,
4. one strong run is enough to evaluate an RL method,
5. any changed-component comparison is an ablation.

### Interpretation paragraph

These are not mere vocabulary mistakes. Each one collapses a distinction the chapter worked to build. If reward and value are blurred, one misreads the optimization target. If shaping is assumed harmless, one silently changes the task while claiming not to. If compactness is mistaken for sufficiency, one overlooks aliasing. If a single run is treated as evidence, one mistakes luck for reliability. If any variant study is called an ablation, one overclaims causal understanding.

### Boundary conditions / assumptions / failure modes

The mistake pattern to watch for is rhetorical compression. In casual speech, people often skip distinctions because the context feels obvious. In mathematical reasoning and experimental claims, those skipped distinctions are exactly where errors enter.

### Fully worked example

Suppose someone says: “We improved the agent by adding a dense reward and a new encoder, and the average return on one seed went up, so the shaping and representation both worked.”

This single sentence contains several conceptual failures.

First, adding a dense reward may have changed the objective unless the shaping was theorem-backed.

Second, a new encoder may have improved or worsened Markov sufficiency; compactness alone does not settle that question.

Third, one seed is not enough evidence to claim robust improvement.

Fourth, because two major components changed at once, the result does not isolate whether the reward change or representation change caused the gain.

The final interpretation is that the statement sounds plausible because it uses standard RL vocabulary, but conceptually it is too loose to support the claimed conclusion.

### Misconception or counterexample block

**Do not confuse fluent RL language with disciplined RL reasoning.**

A sentence can sound expert while still collapsing critical distinctions.

### Connection to later material

The ability to detect these confusions becomes even more important in advanced papers, large benchmark studies, and interdisciplinary applications where terminology is reused loosely.

### Retain / Do not confuse

Retain the chapter’s key distinctions and use them as diagnostic tools. Do not confuse terminological familiarity with conceptual mastery.

---

## 12. What this chapter entitles you to say precisely

### Why this section exists

The chapter should end not with a vague sense of importance but with a clear understanding of what the reader is now licensed to claim, derive, and critique responsibly. This section exists to turn the preceding material into usable intellectual commitments.

### The object being introduced

The object is a set of disciplined conclusions that follow from the chapter. What is fixed is the conceptual groundwork built across the previous sections. What varies is the context in which the reader will apply it later.

### Formal definition

After mastering this chapter, the reader should be able to make several precise claims and defend them in full sentences.

The first is that reward, return, and value are different mathematical objects with different roles in reinforcement learning. A one-step reward is not yet a long-run objective, and a value is not merely a reward with more notation attached to it.

The second is that potential-based shaping can preserve optimal-policy structure because its contribution to discounted return telescopes into boundary terms rather than accumulating arbitrary pathwise distortion through the interior of the trajectory.

The third is that ordinary reward modifications outside a theorem-backed invariance family usually redefine the task rather than merely speeding up learning on the same task.

The fourth is that a representation can be compact and still fail to be Markov, because aliasing can force distinct latent situations into the same visible input.

The fifth is that an evaluation claim becomes interpretable only when the protocol that gives the number meaning is made explicit: seeds, budgets, policy at evaluation time, reward specification, environment variant, and ablations are part of the scientific content, not ornamental reporting.

The sixth is that clean ablation logic requires isolating one causal change at a time while holding the rest of the system fixed enough that attribution remains possible.

---

## 13. Mastery check

You understand this chapter at the intended level if you can answer the following without collapsing any distinctions.

1. What is the exact difference between reward, return, and value, and what question does each object answer?
2. Why can potential-based shaping preserve optimal policies even though it changes one-step rewards?
3. When the shaping terms telescope, which terms cancel and which boundary terms remain?
4. Why does changing a living reward or step penalty generally change the optimization problem rather than merely make it easier to learn?
5. What does representation aliasing mean, and why does it threaten the Markov property?
6. Why is a compact observation not automatically a valid state representation for MDP-based reasoning?
7. Why are multiple random seeds necessary for credible evaluation in RL?
8. What information must a useful evaluation report specify so that a reported score can be interpreted?
9. What makes a comparison a clean ablation rather than a loose variant study?
10. If several things change at once—reward, representation, training budget, and architecture—what kinds of claims become unjustified?

If any of these answers still come out as slogans rather than structured explanations, that is the right signal to revisit the relevant section. This chapter is not about memorizing terms. It is about learning how to tell when an RL formulation or RL result actually means what it claims to mean.
