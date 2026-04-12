# Chapter 8 — Policy Gradients, REINFORCE, Baselines, Actor–Critic, PPO, and SAC

*Rewritten as mastery-oriented teaching notes from the source chapter at the linked repository directory, following the uploaded writing standard.*

## What this chapter is for

This chapter exists because once a reader understands value functions, Bellman equations, and temporal-difference learning, a deeper question becomes unavoidable: why learn a value function first at all? If the real object we ultimately want is a policy, why not optimize the policy directly?

That question is not cosmetic. It opens an entire family of reinforcement-learning methods in which the policy is no longer a side effect of value estimation. It is the thing being parameterized and optimized. But the moment that shift happens, several new difficulties appear at once. What objective is the policy maximizing? How can one differentiate an expectation over random trajectories? Why is REINFORCE unbiased but noisy? Why can a baseline reduce variance without changing the expected gradient? What exactly is a critic doing in actor–critic methods, and where does approximation error enter? Why does PPO clip a probability ratio instead of simply taking a larger gradient step? Why is SAC not just “actor–critic plus entropy,” but a method with a genuinely different objective?

Those questions force this chapter to appear now. Without them, modern policy optimization becomes a bag of named algorithms with no stable conceptual spine. With them, the chapter becomes organized around a small number of precise distinctions: objective versus estimator, exactness versus approximation, variance reduction versus bias introduction, and stabilization of updates versus change of optimization target.

The aim here is not to memorize method names. The aim is to make it impossible to confuse these methods for one another. If the chapter succeeds, the reader will stop seeing REINFORCE, actor–critic, PPO, and SAC as a progression of implementation tricks and will instead see them as different answers to the same structural question: how should one update a parameterized policy using trajectory data?

Before the formal machinery begins, the chapter should freeze one foundational distinction. In value-based control chapters, the main learned object was a predictor of long-run return. In this chapter, the primary learned object is the **policy itself**. The objective is therefore a function of the trajectory law induced by that policy. The parameter $\theta$ matters because it changes action probabilities, those changed action probabilities change the distribution over trajectories, and the objective is an expectation under that $\theta$-dependent law. If the reader loses track of which probability law depends on $\theta$, policy gradients immediately become symbolic rather than conceptual.

---

## 1. Why optimize the policy directly?

### Why this section exists

Earlier material usually introduces reinforcement learning through value-based reasoning. Estimate how good actions are, then derive behavior from those estimates. That route is powerful, but it leaves an important conceptual gap. It makes policy improvement look indirect. The policy improves only because a value estimate has improved. This section exists because many important control problems do not naturally fit that indirect route, and even when they do, there is strong conceptual value in asking whether the policy itself can be treated as the primary optimization object.

The chapter cannot proceed without this idea because every method discussed later assumes that the policy has parameters that can be adjusted directly. If that shift in viewpoint is not made clearly now, later formulas will look like they are optimizing a strange auxiliary object instead of the decision rule itself.

### The object being introduced

The object is a parameterized policy,

$$
\pi_\theta(a \mid s).
$$

This is a conditional distribution over actions given the current state. It answers the question: if the agent is in state $s$, how likely is it to choose action $a$ under parameter setting $\theta$? The policy is now the central object. The state $s$ and action $a$ are the local inputs and outputs. The parameter vector $\theta$ is what the learning algorithm changes. What is fixed during action selection is the current state and current parameter setting. What varies is which action is sampled. Across training, what varies is also the parameter vector itself.

This object allows a new kind of conclusion. Instead of concluding “action $a$ seems best because its estimated value is largest,” we can conclude “adjust $\theta$ so that the policy itself assigns more or less probability to certain actions in certain states.”

### Formal definition

A policy-gradient method parameterizes the policy directly and seeks to optimize an objective such as

$$
J(\theta) = \mathbb{E}_{\tau \sim p_\theta}[G_0(\tau)],
$$

where $\tau$ is a trajectory sampled from the trajectory distribution induced by policy $\pi_\theta$, and $G_0(\tau)$ is the return of that trajectory from the initial time.

### Interpretation paragraph

This definition says that the goal is not to estimate a value table and then extract a policy after the fact. The goal is to choose parameters $\theta$ so that, when the resulting policy interacts with the environment and generates trajectories, the expected return of those trajectories is large. The policy is not derived from the optimization target. It *is* the optimization target.

The first thing the reader should notice is that the objective depends on $\theta$ in an indirect way. The return $G_0(\tau)$ depends on which trajectory occurs, and the probability of each trajectory depends on the policy. So optimization is taking place through the distribution over trajectories. This is the structural fact that drives everything else in the chapter.

### Boundary conditions / assumptions / failure modes

Several assumptions are easy to overlook here.

First, the policy must be parameterized in a differentiable way if one wants to use gradient-based optimization. If the policy is not differentiable in $\theta$, then the main methods in this chapter no longer apply in their usual form.

Second, the expectation is with respect to the trajectory distribution induced by the current policy. This means the data-generating distribution changes as the policy changes. That moving-target character is not a technical footnote. It is one of the defining difficulties of reinforcement learning.

Third, direct policy optimization is not automatically easier than value-based learning. It removes some difficulties and introduces others. In particular, policy-gradient estimators can have very high variance.

A common failure mode is to think that “direct policy optimization” means the environment dynamics no longer matter. They still matter because they determine which trajectories result from a given policy. The change is in what is optimized directly, not in what determines outcomes.

### Fully worked example

Consider a simple two-state episodic task. In state $s_0$, the agent chooses either action $L$ or $R$, after which the episode ends with a reward. Suppose the policy is parameterized by a single scalar $\theta$ through

$$
\pi_\theta(L \mid s_0)=\theta, \qquad \pi_\theta(R \mid s_0)=1-\theta,
$$

with $0 < \theta < 1$.

Assume that action $L$ always gives reward $2$, while action $R$ always gives reward $0$. Since the episode ends immediately after the action, the return is just the immediate reward. There are therefore exactly two possible trajectories:

- trajectory $\tau_L$: choose $L$, receive reward $2$,
- trajectory $\tau_R$: choose $R$, receive reward $0$.

The trajectory probabilities are

$$
p_\theta(\tau_L)=\theta, \qquad p_\theta(\tau_R)=1-\theta.
$$

The objective is

$$
J(\theta)=\mathbb{E}_{\tau \sim p_\theta}[G_0(\tau)]
= p_\theta(\tau_L)\cdot 2 + p_\theta(\tau_R)\cdot 0.
$$

Substitute the probabilities:

$$
J(\theta)=2\theta.
$$

Now interpret this carefully. When $\theta$ increases, the policy assigns more probability to action $L$, the action with better return. Because the environment here is trivial and deterministic, the expected return increases linearly with the probability of taking the better action. The policy itself is the thing being tuned.

What was checked at each step? First, identify the policy as a distribution over actions. Second, identify how that policy determines trajectory probabilities. Third, express expected return using those probabilities. Fourth, interpret how changing $\theta$ changes the policy rather than a separate value estimate.

The general lesson is that direct policy optimization works by changing action probabilities so that the trajectory distribution shifts toward better returns.

### Misconception or counterexample block

**Do not confuse “direct policy optimization” with “ignore values entirely.”**

Policy-gradient methods optimize the policy directly, but many of the strongest methods still use value estimates as supporting tools. Actor–critic methods are the clearest example: the policy is the primary optimization object, yet value estimation still plays a central role in reducing variance and constructing better update signals.

### Connection to later material

This section provides the conceptual starting point for everything that follows. Once the policy becomes the primary object, the next question is how to differentiate the expected return with respect to policy parameters. That leads directly to the score-function derivation and to REINFORCE.

### Retain / Do not confuse

Retain that policy-gradient methods optimize the policy itself, not a value function from which a policy is later extracted. Do not confuse “policy is primary” with “value information becomes irrelevant.”

---

## 2. Trajectory objectives and the score-function route

### Why this section exists

Once the policy is the optimization object, one immediately encounters a technical obstacle. The objective is an expectation over trajectories generated by the current policy, and the policy parameters affect the objective by changing the trajectory distribution. So the central question becomes: how does one differentiate an expectation whose probability law depends on the parameters being optimized?

This section must appear now because REINFORCE and everything that comes after it depend on exactly one structural move: rewriting the derivative of an expectation over trajectories in a form that can be estimated from sampled episodes.

### The object being introduced

The object is the gradient of the trajectory objective,

$$
\nabla_\theta J(\theta) = \nabla_\theta \mathbb{E}_{\tau \sim p_\theta}[G_0(\tau)].
$$

Here the random object is the whole trajectory $\tau$, not just a single reward or state. The quantity $G_0(\tau)$ is a scalar function of that trajectory. What is fixed is the functional form of return once a trajectory is given. What varies with $\theta$ is the probability with which each trajectory is produced.

This object answers the question: in which direction in parameter space should the policy be nudged so that expected return increases fastest, at least locally?

### Formal definition

Write the objective as

$$
J(\theta) = \sum_\tau p_\theta(\tau) G_0(\tau)
$$

in the finite-horizon discrete setting. Then

$$
\nabla_\theta J(\theta)
= \sum_\tau \nabla_\theta p_\theta(\tau) G_0(\tau).
$$

Using the log-derivative identity,

$$
\nabla_\theta p_\theta(\tau)
= p_\theta(\tau)\, \nabla_\theta \log p_\theta(\tau),
$$

we get

$$
\nabla_\theta J(\theta)
= \sum_\tau p_\theta(\tau) G_0(\tau) \nabla_\theta \log p_\theta(\tau)
= \mathbb{E}_{\tau \sim p_\theta}\big[G_0(\tau)\nabla_\theta \log p_\theta(\tau)\big].
$$

### Interpretation paragraph

This derivation is doing one very important conversion. The derivative originally lands on a trajectory probability, which is awkward to estimate directly from data. The log-derivative identity transforms that derivative into the probability itself times a score term. Once the probability appears explicitly, the whole expression becomes an expectation again.

That is the heart of the score-function route. It turns a gradient of an expectation into an expectation of a gradient-like weight. This is what makes Monte Carlo policy-gradient estimation possible.

The reader should notice the exact role of the score term $\nabla_\theta \log p_\theta(\tau)$. It measures how sensitive the log probability of the trajectory is to the policy parameters. A trajectory with high return contributes to the gradient in the direction that would increase the log-probability of similar trajectories.

### Boundary conditions / assumptions / failure modes

Several hidden assumptions matter.

First, the interchange of derivative and summation needs justification. In finite-horizon discrete problems this is usually straightforward, but one should know that it is an actual mathematical move, not magic.

Second, the log-derivative identity requires that the trajectory probability be positive on the support under consideration.

Third, the expression above is still not operationally convenient until the trajectory score is decomposed into local policy terms. Otherwise the update would require access to the gradient of the whole trajectory probability as a monolithic object.

A common failure mode is to think that this derivation differentiates the return itself. It does not. In the standard score-function derivation, the derivative acts on the probability law over trajectories, while the return is treated as a scalar weight associated with each trajectory.

### Fully worked example

Return to the one-step example from the previous section. The objective was

$$
J(\theta)=2\theta.
$$

Now derive its gradient using the score-function route instead of direct algebra.

There are two trajectories:

- $\tau_L$ with probability $p_\theta(\tau_L)=\theta$ and return $G_0(\tau_L)=2$,
- $\tau_R$ with probability $p_\theta(\tau_R)=1-\theta$ and return $G_0(\tau_R)=0$.

The gradient is

$$
\nabla_\theta J(\theta)
= \sum_\tau p_\theta(\tau)G_0(\tau)\nabla_\theta \log p_\theta(\tau).
$$

Handle each trajectory separately.

For $\tau_L$,

$$
\log p_\theta(\tau_L)=\log \theta,
$$

so

$$
\nabla_\theta \log p_\theta(\tau_L)=\frac{1}{\theta}.
$$

Its contribution is

$$
\theta \cdot 2 \cdot \frac{1}{\theta} = 2.
$$

For $\tau_R$,

$$
\log p_\theta(\tau_R)=\log(1-\theta),
$$

so

$$
\nabla_\theta \log p_\theta(\tau_R)=\frac{-1}{1-\theta}.
$$

Its contribution is

$$
(1-\theta) \cdot 0 \cdot \frac{-1}{1-\theta}=0.
$$

Therefore

$$
\nabla_\theta J(\theta)=2.
$$

This matches the direct derivative of $2\theta$. What was being checked? First, the objective was rewritten as an expectation over trajectories. Second, the score-function identity was applied. Third, each trajectory’s return weighted its score contribution. Fourth, the resulting sum matched the direct gradient.

The general lesson is that the score-function method reconstructs the gradient entirely from trajectory probabilities and returns, without differentiating through the environment’s realized rewards directly.

### Misconception or counterexample block

**Do not confuse “gradient of expected return” with “expected gradient of return.”**

The return of a realized trajectory is a scalar random outcome. In the score-function route, the gradient appears because the *distribution* over trajectories depends on $\theta$, not because the realized scalar return is itself being differentiated step by step through the environment.

### Connection to later material

This is the derivational backbone of REINFORCE. The next step is to exploit the factorization of the trajectory law so that the trajectory score becomes a sum of local policy log-gradients over time.

### Retain / Do not confuse

Retain that the score-function route converts a gradient of an expectation into an expectation involving returns and score terms. Do not confuse the derivative of the trajectory distribution with a derivative of the scalar return itself.

---

## 3. From trajectory score to local policy scores

### Why this section exists

The previous section gives a trajectory-level gradient formula, but it is not yet in a usable form. The term $\nabla_\theta \log p_\theta(\tau)$ still refers to the log-probability of a whole trajectory. This section exists because policy optimization becomes practical only after that global term is decomposed into a sum of local terms attached to decisions made at each time step.

Without this step, the policy gradient would remain conceptually correct but operationally opaque.

### The object being introduced

The object is the factorized trajectory score. A finite-horizon trajectory under a policy has probability

$$
p_\theta(\tau)=\rho(s_0)\prod_{t=0}^{T-1}\pi_\theta(a_t\mid s_t)P(s_{t+1},r_{t+1}\mid s_t,a_t),
$$

where $\rho$ is the initial-state distribution and $P$ is the environment law. What is fixed is the environment and the factored sequential structure. What varies across trajectories are the states, actions, and rewards that actually occur. What varies with $\theta$ are the policy factors.

This object answers the question: where exactly does policy-parameter sensitivity enter the probability of a whole trajectory?

### Formal definition

Taking logs gives

$$
\log p_\theta(\tau)
= \log \rho(s_0)
+ \sum_{t=0}^{T-1}\log \pi_\theta(a_t\mid s_t)
+ \sum_{t=0}^{T-1}\log P(s_{t+1},r_{t+1}\mid s_t,a_t).
$$

If the environment dynamics and initial-state distribution do not depend on $\theta$, then

$$
\nabla_\theta \log p_\theta(\tau)
= \sum_{t=0}^{T-1} \nabla_\theta \log \pi_\theta(a_t\mid s_t).
$$

Substituting this into the trajectory-gradient formula yields

$$
\nabla_\theta J(\theta)
= \mathbb{E}_{\tau \sim p_\theta}\left[G_0(\tau)\sum_{t=0}^{T-1}\nabla_\theta \log \pi_\theta(A_t\mid S_t)\right].
$$

### Interpretation paragraph

This is the decisive structural simplification. The gradient of expected return becomes an expectation of a sum over time, where each term is a local log-policy gradient. The environment still affects which trajectories are seen and what rewards they contain, but under the standard assumption it contributes no direct derivative term because the environment is not parameterized by $\theta$.

The first thing to notice is that the policy gradient is now explicitly a sum of contributions from the policy’s own choices. That is why policy-gradient estimators can be built from sampled trajectories without differentiating through environment dynamics.

### Boundary conditions / assumptions / failure modes

The critical assumption is that the environment transition-reward law and the initial-state distribution do not depend on $\theta$. If they do, their derivatives remain and must be included.

Another subtle point is that the expression shown above still attaches the full trajectory return $G_0$ to every time-step score term. This is correct, but it is not yet the most efficient or interpretable form. Later, one refines the weighting so that the score at time $t$ is paired with the return from time $t$ onward.

A common failure mode is to say “the environment disappears from the gradient.” That is false. The environment disappears from the *direct derivative term* under the assumption above, but it still determines the state visitation distribution and reward outcomes that appear inside the expectation.

### Fully worked example

Consider a horizon-$2$ episode with trajectory

$$
\tau=(s_0,a_0,r_1,s_1,a_1,r_2,s_2).
$$

Suppose the probability factorization is

$$
p_\theta(\tau)=\rho(s_0)\pi_\theta(a_0\mid s_0)P(s_1,r_1\mid s_0,a_0)\pi_\theta(a_1\mid s_1)P(s_2,r_2\mid s_1,a_1).
$$

Take logs:

$$
\log p_\theta(\tau)=\log \rho(s_0)+\log \pi_\theta(a_0\mid s_0)+\log P(s_1,r_1\mid s_0,a_0)+\log \pi_\theta(a_1\mid s_1)+\log P(s_2,r_2\mid s_1,a_1).
$$

Now differentiate with respect to $\theta$. Under the assumption that $\rho$ and $P$ do not depend on $\theta$, the derivative of the first, third, and fifth terms is zero. Therefore

$$
\nabla_\theta \log p_\theta(\tau)
=\nabla_\theta \log \pi_\theta(a_0\mid s_0)+\nabla_\theta \log \pi_\theta(a_1\mid s_1).
$$

What was checked at each step? First, the trajectory probability was written as a product of local terms. Second, the log turned that product into a sum. Third, only those terms containing $\theta$ survived differentiation. Fourth, the global trajectory score became a sum of local policy scores.

The general lesson is that policy gradients are local in their derivatives but global in their expectations. Local action-log-probability sensitivities are weighted by returns generated over whole trajectories.

### Misconception or counterexample block

**Do not confuse local derivative structure with local credit assignment.**

Even though the derivative decomposes into per-time-step log-policy terms, the problem of deciding which action deserves credit for later rewards is not automatically solved. That is why the choice of return-like weighting matters so much.

### Connection to later material

This decomposition makes REINFORCE possible. It also lays the groundwork for baselines, advantages, and critic-based estimators, all of which can be understood as different choices of how to weight these local score terms.

### Retain / Do not confuse

Retain that the trajectory score decomposes into a sum of log-policy gradients over time when only the policy depends on $\theta$. Do not confuse “environment contributes no derivative term” with “environment plays no role in the expectation.”

---

## 4. REINFORCE

### Why this section exists

Once the trajectory gradient has been decomposed into local policy score terms, the first full policy-gradient estimator comes into view. This section exists because REINFORCE is the canonical starting point for Monte Carlo policy-gradient learning. It is the simplest clean estimator that shows what direct policy optimization looks like before variance reduction and critic approximation are introduced.

The chapter cannot move to baselines or actor–critic methods responsibly until the reader understands what exact estimator those later methods are modifying.

### The object being introduced

The object is the REINFORCE gradient estimator. It is a stochastic estimator of the gradient of expected return. For each sampled trajectory, it adds up policy score terms weighted by returns. What is fixed is the sampled trajectory and the current policy parameters during the update. What varies are the actions sampled, the rewards obtained, and therefore the returns that weight the update.

This estimator answers the question: given sampled episodes, how can one form an unbiased estimate of the policy gradient using only trajectory data?

### Formal definition

A common finite-horizon REINFORCE-style gradient contribution is

$$
\sum_{t=0}^{T-1} \gamma^t \nabla_\theta \log \pi_\theta(A_t \mid S_t) G_t
$$

inside an expectation, where $G_t$ is the return from time $t$ onward.

Equivalently, one often writes the policy gradient in the form

$$
\nabla_\theta J(\theta)
= \mathbb{E}_\pi\left[\sum_{t=0}^{T-1} \nabla_\theta \log \pi_\theta(A_t\mid S_t) G_t\right],
$$

with conventions differing slightly depending on where discounting is placed.

### Interpretation paragraph

REINFORCE says: for each time step in a sampled trajectory, take the gradient of the log-probability of the action that was actually chosen, and weight that gradient by how good the future turned out to be from that point onward. If the future return is large, move parameters in a direction that makes that action more likely in similar circumstances. If the future return is poor, move in the opposite direction.

The first thing to notice is that REINFORCE uses *sampled return* as the learning signal. It does not estimate a value function first. It takes the full Monte Carlo outcome as the weight attached to the policy score.

### Boundary conditions / assumptions / failure modes

REINFORCE is unbiased under the standard assumptions behind the score-function derivation, but unbiased does not mean low-noise. In fact, its main weakness is high variance. The sampled return can fluctuate dramatically across trajectories, especially in long-horizon or sparse-reward problems.

Another point that must be kept straight is that the estimator gives credit to an action using a return from the action’s time onward, not a reward that necessarily arrived immediately. This is appropriate but makes credit assignment difficult in long horizons.

A common failure mode is to think that REINFORCE is primitive and therefore conceptually unimportant. In reality, many later methods are best understood as controlled modifications of REINFORCE rather than wholly separate inventions.

### Fully worked example

Consider a one-state episodic task with two time steps. At each time $t \in \{0,1\}$, the agent chooses action $A_t \in \{L,R\}$. Suppose the policy is Bernoulli with parameter $\theta$ through

$$
\pi_\theta(L\mid s)=\theta, \qquad \pi_\theta(R\mid s)=1-\theta.
$$

Assume a sampled episode produced the following:

- at time $0$, the agent chose $L$,
- reward $R_1=1$,
- at time $1$, the agent chose $R$,
- reward $R_2=3$,
- discount factor $\gamma=1$.

Then the returns are

$$
G_0 = R_1 + R_2 = 4,
$$
$$
G_1 = R_2 = 3.
$$

Now write the sampled REINFORCE contribution:

$$
\nabla_\theta \log \pi_\theta(L\mid s) G_0 + \nabla_\theta \log \pi_\theta(R\mid s) G_1.
$$

For the chosen action $L$,

$$
\log \pi_\theta(L\mid s)=\log \theta,
$$
so

$$
\nabla_\theta \log \pi_\theta(L\mid s)=\frac{1}{\theta}.
$$

For the chosen action $R$,

$$
\log \pi_\theta(R\mid s)=\log(1-\theta),
$$
so

$$
\nabla_\theta \log \pi_\theta(R\mid s)=\frac{-1}{1-\theta}.
$$

Therefore the sampled gradient contribution is

$$
\frac{4}{\theta} - \frac{3}{1-\theta}.
$$

Suppose $\theta=0.5$. Then the contribution becomes

$$
\frac{4}{0.5} - \frac{3}{0.5} = 8 - 6 = 2.
$$

Interpret this carefully. The first action received strong positive reinforcement because it was followed by high total future return. The second action’s contribution was negative because it was action $R$, whose log-gradient points in the direction of reducing $\theta$, and it was weighted by a positive return. Whether the overall update increases or decreases $\theta$ depends on the combination of both time-step contributions.

The general lesson is that REINFORCE updates sum time-local sensitivity terms weighted by future outcomes. Each term asks: how should we change the parameters to make the sampled action more or less likely, given how the future unfolded from that point?

### Misconception or counterexample block

**Do not read REINFORCE as “repeat actions that produced reward immediately.”**

The relevant signal is not just the next reward. It is the return from that time onward. An action may deserve positive reinforcement because it set up large rewards much later.

### Connection to later material

REINFORCE is the reference point for the rest of the chapter. Baselines will modify its weight to reduce variance without changing the expected gradient. Actor–critic methods will replace exact returns with lower-variance estimates built from a critic. PPO will constrain update size. SAC will modify the objective itself.

### Retain / Do not confuse

Retain that REINFORCE is an unbiased Monte Carlo policy-gradient estimator built from log-policy gradients weighted by returns. Do not confuse unbiasedness with practicality in high-variance settings.

---

## 5. Baselines and the zero-mean argument

### Why this section exists

REINFORCE is conceptually clean, but its variance can be severe. The immediate next question is therefore not whether REINFORCE is mathematically correct. It is how to reduce variance without changing the expected gradient being estimated. This section exists to answer that question through the introduction of baselines.

The chapter cannot proceed to advantage-based reasoning or actor–critic methods without this section because the baseline trick is the first major example of improving estimator quality while preserving the target gradient in expectation.

### The object being introduced

The object is a baseline function, typically a state-dependent scalar $b(S_t)$ subtracted from the return-like weight in the policy update. At time $t$, the update weight becomes

$$
G_t - b(S_t).
$$

What is fixed at that time step is the current state $S_t$ when conditioning is applied. What varies is the sampled action and the future trajectory. The baseline answers the question: can we center the return-like signal around a reference level so that the update fluctuates less, while still estimating the same expected gradient?

### Formal definition

A baseline-adjusted policy-gradient term has the form

$$
\nabla_\theta \log \pi_\theta(A_t\mid S_t)\big(G_t - b(S_t)\big).
$$

The key identity is

$$
\mathbb{E}_\pi\big[\nabla_\theta \log \pi_\theta(A_t\mid S_t)b(S_t)\big]=0,
$$

provided the baseline depends only on the state and not on the sampled action in a way that breaks the argument.

The proof should also be heard in words, not just in symbols. At a given state $S_t=s$, a state-only baseline $b(s)$ is fixed with respect to the action randomness generated by the policy at that moment. The only part still varying under the policy expectation is which action $A_t$ is sampled. When one averages $\nabla_\theta \log \pi_\theta(A_t\mid s)$ over actions drawn from $\pi_\theta(\cdot\mid s)$, the result is zero. Multiplying that zero-mean score term by a quantity that depends only on the state preserves zero. That is why the baseline can shift the weighting of sampled updates in a variance-reducing way without changing the expected gradient itself. The argument is not that baselines are “small” or “approximately harmless.” The argument is that their expected score contribution is exactly zero under the stated condition.

### Interpretation paragraph

The idea is simple but subtle. A state-only baseline shifts the return weight by an amount that is the same for every action considered at that state. Because the policy score term has conditional expectation zero under the policy, subtracting such a state-only reference does not change the expected gradient. It only changes the variance of the sampled estimator.

The first thing to notice is that the baseline is not meant to change which objective is being optimized. Its role is variance control, not objective redesign.

### Boundary conditions / assumptions / failure modes

The central assumption is that the baseline must not depend on the sampled action in a way that survives conditioning on the current state. If the baseline depends on the action, the zero-mean argument can fail and the expected gradient may change.

Another subtle point is that a baseline can reduce variance, but not every baseline reduces it equally well. Some choices are much better than others. A poor baseline can have little effect.

A common failure mode is to think that any term can be subtracted from the update if it seems convenient. That is false. The zero-mean argument is precise. The subtraction must preserve the expected gradient.

### Fully worked example

Let us prove the zero-mean argument carefully in the discrete case.

We want to analyze

$$
\mathbb{E}_\pi\big[\nabla_\theta \log \pi_\theta(A_t\mid S_t)b(S_t)\big].
$$

Condition on the current state $S_t=s$. Since $b(S_t)$ becomes the fixed scalar $b(s)$ under this conditioning,

$$
\mathbb{E}_\pi\big[\nabla_\theta \log \pi_\theta(A_t\mid S_t)b(S_t) \mid S_t=s\big]
= b(s)\, \mathbb{E}_\pi\big[\nabla_\theta \log \pi_\theta(A_t\mid s) \mid S_t=s\big].
$$

Now expand the conditional expectation over actions:

$$
\mathbb{E}_\pi\big[\nabla_\theta \log \pi_\theta(A_t\mid s) \mid S_t=s\big]
= \sum_a \pi_\theta(a\mid s)\nabla_\theta \log \pi_\theta(a\mid s).
$$

Use the identity $\nabla_\theta \log \pi = \frac{1}{\pi}\nabla_\theta \pi$ wherever $\pi>0$:

$$
\sum_a \pi_\theta(a\mid s)\nabla_\theta \log \pi_\theta(a\mid s)
= \sum_a \nabla_\theta \pi_\theta(a\mid s).
$$

Since probabilities over actions sum to $1$ for every state,

$$
\sum_a \pi_\theta(a\mid s)=1.
$$

Differentiate both sides with respect to $\theta$:

$$
\sum_a \nabla_\theta \pi_\theta(a\mid s)=\nabla_\theta 1 = 0.
$$

Therefore

$$
\mathbb{E}_\pi\big[\nabla_\theta \log \pi_\theta(A_t\mid S_t)b(S_t) \mid S_t=s\big]=b(s)\cdot 0 = 0.
$$

Now average over the state distribution. The result remains zero:

$$
\mathbb{E}_\pi\big[\nabla_\theta \log \pi_\theta(A_t\mid S_t)b(S_t)\big]=0.
$$

What did each step accomplish? Conditioning on state made the baseline fixed. Expanding over actions exposed the policy normalization identity. Differentiating the fact that action probabilities sum to one yielded the zero-mean result.

The conclusion is exact: a state-only baseline can be subtracted without changing the expected policy gradient.

### Misconception or counterexample block

**Do not confuse “baseline reduces variance” with “baseline is harmless no matter how chosen.”**

A state-only baseline preserves the expected gradient. An action-dependent baseline can change the gradient unless special correction terms are included. The safe statement is precise, not vague.

### Connection to later material

This section leads directly to the advantage viewpoint. Once the baseline is chosen to represent typical continuation from a state, the update weight becomes a measure of whether the sampled action performed better or worse than expected. That is the conceptual content of advantage.

### Retain / Do not confuse

Retain that a state-only baseline changes estimator variance without changing the expected gradient. Do not confuse “subtract a helpful reference level” with “subtract any convenient learned signal.”

---

## 6. The advantage viewpoint

### Why this section exists

Baselines explain how to center the update signal, but they do not yet explain what the centered signal means. Once one subtracts a state-level reference, the natural interpretation is no longer “how good was the future overall?” but “how good was the sampled action relative to what is typical from this state?” This section exists because that comparison is the conceptual heart of policy-gradient credit assignment.

### The object being introduced

The object is the advantage,

$$
A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s).
$$

This is a relative measure. It answers the question: starting from state $s$, was action $a$ better or worse than the policy’s average continuation from that state? What is fixed is the state and action. What varies is how much better or worse that action is than the policy’s own baseline expectation.

This object allows a stronger conclusion than raw return does. It allows us to separate “the state was favorable” from “the chosen action was favorable relative to the alternatives under the current policy.”

### Formal definition

The state value and action value under policy $\pi$ are

$$
V^\pi(s)=\mathbb{E}_\pi[G_t \mid S_t=s],
$$

$$
Q^\pi(s,a)=\mathbb{E}_\pi[G_t \mid S_t=s, A_t=a].
$$

The advantage is then

$$
A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s).
$$

In Monte Carlo form, using a baseline $V^\pi(S_t)$, the sample quantity

$$
G_t - V^\pi(S_t)
$$

acts like an advantage-style weight.

### Interpretation paragraph

Advantage is a comparison quantity. A large return by itself does not tell the full story. Perhaps every action from the current state would have led to a large return because the state was exceptionally favorable. In that case, reinforcing the sampled action strongly may be misleading. Advantage corrects that by asking whether the chosen action outperformed the policy’s typical expectation for that state.

The first thing to notice is that $V^\pi(s)$ is state-level context, while $Q^\pi(s,a)$ is state-and-action-specific context. Their difference isolates action quality relative to the state’s average continuation.

### Boundary conditions / assumptions / failure modes

The exact advantage depends on the true value functions of the current policy. In practice these are usually unknown and must be estimated.

Another subtlety is that a sample quantity like $G_t-V^\pi(S_t)$ is not equal to the exact advantage on every trajectory. It is a noisy estimator whose expectation given $(S_t,A_t)$ aligns with the action-value difference structure.

A common failure mode is to think advantage means “how good the action was in absolute terms.” That is not right. Advantage is inherently relative to a baseline state value.

### Fully worked example

Suppose that from state $s$, the current policy chooses between actions $a_1$ and $a_2$ with probabilities

$$
\pi(a_1\mid s)=0.75, \qquad \pi(a_2\mid s)=0.25.
$$

Assume the action values are

$$
Q^\pi(s,a_1)=10, \qquad Q^\pi(s,a_2)=4.
$$

First compute the state value under the current policy:

$$
V^\pi(s)=\sum_a \pi(a\mid s)Q^\pi(s,a)=0.75(10)+0.25(4)=7.5+1=8.5.
$$

Now compute the advantages:

$$
A^\pi(s,a_1)=10-8.5=1.5,
$$

$$
A^\pi(s,a_2)=4-8.5=-4.5.
$$

Interpret this carefully. Action $a_1$ is not merely good in absolute terms. It is better than the policy’s typical continuation from $s$ by $1.5$. Action $a_2$ is worse than the policy’s typical continuation by $4.5$. That negative value does not mean the return from $a_2$ must be negative in absolute terms. It means it is bad relative to what the state usually offers under the current policy.

The general lesson is that advantage separates action quality from state quality. That makes it especially suitable for weighting policy updates.

### Misconception or counterexample block

**Do not confuse value with advantage.**

A state can have high value while a particular action in that state has negative advantage. This simply means the state is generally promising, but the sampled action was worse than the policy’s typical continuation.

### Connection to later material

Advantage is the conceptual link between baselines and actor–critic methods. Once one wants lower-variance policy updates, it becomes natural to learn a value-based quantity that approximates this relative signal. That learned approximation is exactly where the critic enters.

### Retain / Do not confuse

Retain that advantage measures action quality relative to the state’s typical continuation. Do not confuse “high return” with “positive advantage”; those are different claims.

---

## 7. Actor–critic methods

### Why this section exists

REINFORCE uses Monte Carlo returns and is unbiased, but often too noisy. Baselines help, but in many problems one wants a lower-variance, more frequently updated signal than full returns provide. This section exists because actor–critic methods solve that problem by combining direct policy optimization with learned value information.

The chapter cannot move to PPO or SAC without actor–critic because both are best understood against this actor–critic template.

### The object being introduced

The object is a two-part learning architecture:

- the **actor**, which parameterizes and updates the policy,
- the **critic**, which estimates value information used to construct improved policy-update weights.

The actor answers the question “how should action probabilities change?” The critic answers the question “how good was the sampled action or state relative to expectation?” What is fixed at any update moment is the sampled state, action, reward, and current parameter settings of actor and critic. What varies are the learned estimates and the sampled transitions.

This architecture allows a different conclusion than REINFORCE alone. Instead of weighting policy scores with noisy full returns, one can weight them with learned estimates such as value targets, temporal-difference errors, or advantage estimates.

### Formal definition

A generic actor update has the form

$$
\nabla_\theta \log \pi_\theta(A_t\mid S_t)\, \widehat A_t,
$$

where $\widehat A_t$ is some critic-provided estimate of an advantage-like quantity.

A common critic target is based on temporal-difference structure, for example the one-step TD error

$$
\delta_t = R_{t+1} + \gamma V_w(S_{t+1}) - V_w(S_t),
$$

where $V_w$ is the critic’s parameterized value estimate.

### Interpretation paragraph

Actor–critic methods divide labor. The actor is responsible for changing the policy. The critic is responsible for evaluating what happened strongly enough to guide that change with lower variance than raw Monte Carlo returns would provide.

The first thing to notice is that the critic is not a side project. It exists to supply the actor with a better learning signal. But the price of this improvement is that the actor update is now only as trustworthy as the critic’s estimate. This is where the central bias–variance tradeoff enters.

### Boundary conditions / assumptions / failure modes

The critic’s estimate is rarely exact in practice. Function approximation, bootstrapping, limited data, and nonstationarity can all introduce error. As soon as the actor update uses an imperfect estimated advantage in place of the exact one, the update direction can be biased relative to the exact policy gradient.

This is not a minor detail. It is one of the defining tradeoffs of actor–critic methods: lower variance at the cost of possible bias.

A common failure mode is to say “actor–critic gives the same gradient as REINFORCE, just faster.” That is not generally true. Some actor–critic constructions preserve certain theoretical identities under exact critics, but practical algorithms almost always involve approximation.

### Fully worked example

Suppose a sampled transition at time $t$ is

$$
S_t=s, \quad A_t=a, \quad R_{t+1}=2, \quad S_{t+1}=s'.
$$

Assume the discount factor is $\gamma=0.9$. The critic currently estimates

$$
V_w(s)=5, \qquad V_w(s')=4.
$$

Compute the one-step TD error:

$$
\delta_t = R_{t+1} + \gamma V_w(S_{t+1}) - V_w(S_t)
= 2 + 0.9(4) - 5.
$$

Calculate:

$$
0.9(4)=3.6,
$$
so

$$
\delta_t = 2 + 3.6 - 5 = 0.6.
$$

Now interpret that number. The critic had assigned value $5$ to the current state. After observing the reward and the estimated continuation value of the next state, the realized one-step backed-up target is $5.6$. So the outcome was slightly better than the critic expected, by $0.6$.

An actor–critic update may therefore use

$$
\nabla_\theta \log \pi_\theta(a\mid s) \cdot 0.6.
$$

This says: increase the probability of the sampled action in proportion to how much better the observed transition looked than the critic had predicted.

What was checked at each step? First, the critic’s current estimates were identified. Second, a bootstrapped target was formed using reward plus discounted next-state value. Third, the difference between target and current estimate produced a signed learning signal. Fourth, that signal was used to weight the actor’s log-policy gradient.

The general lesson is that actor–critic replaces high-variance full-return weighting with a more local learned estimate of improvement.

### Misconception or counterexample block

**Do not confuse “critic estimates values” with “critic decides the policy.”**

In actor–critic, the critic guides the actor, but the actor is still the object being optimized directly. The critic supplies information; it is not the policy itself.

### Connection to later material

Actor–critic is the architectural template underlying many modern algorithms. PPO uses actor–critic-style advantage estimates while constraining update size. SAC uses actor and critic components too, but under a maximum-entropy objective rather than plain expected-return optimization.

### Retain / Do not confuse

Retain that actor–critic combines direct policy updates with value-based guidance from a critic. Do not confuse lower variance with guaranteed exactness; critic approximation can bias the actor update.

---

## 8. Bias–variance tradeoffs in policy optimization

### Why this section exists

By this point the chapter has introduced unbiased but noisy Monte Carlo updates and lower-variance but potentially biased critic-based updates. This section exists to make that tradeoff explicit, because many later confusions come from discussing algorithms without stating which part of the method is buying variance reduction and which part is paying for it with approximation.

### The object being introduced

The object is not a new algorithm but a comparison principle. The relevant quantities are estimator variance and estimator bias. Variance measures how much the update fluctuates across samples. Bias measures systematic deviation of the expected update direction from the exact target gradient. What is fixed is the target policy gradient one would ideally like to estimate. What varies is the estimator used to approximate it.

This object answers the question: what is gained and what is risked when moving from REINFORCE to baselines, then from baselines to critic-estimated advantages?

### Formal definition

At a high level:

- REINFORCE with full returns is unbiased under the usual assumptions.
- A valid state-only baseline preserves unbiasedness and can reduce variance.
- Replacing exact return-based or exact advantage-based weights with critic-estimated quantities can reduce variance further, but may introduce bias if the critic is imperfect.

### Interpretation paragraph

This distinction is one of the most important in the whole chapter. If an algorithm changes the expected gradient itself, then it is not merely a variance-reduction method. It is changing the estimator’s target or introducing approximation into the update. Some of the most successful methods in practice deliberately accept such bias because the variance reduction and optimization stability gains are worth it.

The first thing to notice is that variance and bias do not move in lockstep. One can reduce variance without introducing bias using a valid baseline. But stronger variance reduction often comes from using learned approximations, and those approximations can tilt the update direction.

### Boundary conditions / assumptions / failure modes

Bias is not always fatal. In practical reinforcement learning, a biased but stable and data-efficient method may outperform a theoretically cleaner unbiased method. The key is to know that a tradeoff is being made.

A common failure mode is to equate “uses a critic” with “therefore more correct.” Often the critic exists precisely because exact return-based estimation is too noisy, not because the critic makes the update exact.

### Fully worked example

Compare two ways of updating a policy after a sampled state-action pair:

1. Use the Monte Carlo return $G_t$ as the weight.
2. Use an approximate critic-based estimate $\widehat A_t$ as the weight.

Suppose that for a particular state-action situation, the true expected advantage is $2$, but sampled Monte Carlo returns fluctuate wildly, say between $-5$ and $9$ across episodes. A critic, after training, might output values near $1.8$, $2.1$, or $2.3$ instead.

The first estimator has large spread. If we used it repeatedly, the average might still converge to the correct target, but each individual update could point in very different directions or magnitudes. The second estimator has much smaller spread, so optimization may proceed more steadily. But if the critic systematically underestimates by $0.2$, then the expected update is no longer exactly the same as the exact target update.

What changed and what stayed invariant? The actor still uses a log-policy gradient term. What changed is the weight attached to that term. By changing the weight, we changed the statistical properties of the estimator.

The general lesson is that policy-optimization methods are often best compared by asking what quantity weights the policy score, and how trustworthy that quantity is.

### Misconception or counterexample block

**Do not confuse “unbiased” with “best for learning.”**

An unbiased estimator can be so noisy that it is practically unusable in difficult environments. The right comparison is not philosophical purity. It is optimization behavior under finite data and approximation.

### Connection to later material

This tradeoff sits underneath PPO and SAC as well. PPO introduces additional approximation through a clipped surrogate objective in exchange for better stability. SAC changes the objective itself to trade reward maximization against entropy.

### Retain / Do not confuse

Retain that estimator design in policy optimization is largely a question of where variance is reduced and where bias or approximation is introduced. Do not confuse theoretical exactness with practical superiority.

---

## 9. PPO and why clipping appears

### Why this section exists

Once actor–critic methods are on the table, one more difficulty becomes unavoidable. Even with a reasonable advantage estimate, a large policy update can move the policy too far in one step. Then data collected under the old policy may become a poor basis for improving the new one. This section exists because PPO is fundamentally about controlling update size so that policy optimization remains locally trustworthy.

### The object being introduced

The object is the probability ratio between the new and old policy for the sampled action,

$$
r_t(\theta)=\frac{\pi_\theta(A_t\mid S_t)}{\pi_{\theta_{\text{old}}}(A_t\mid S_t)}.
$$

What is fixed during a PPO update is the batch of sampled states, actions, and estimated advantages collected under the old policy. What varies is the candidate new parameter vector $\theta$. The ratio answers the question: how much has the new policy changed the probability of the action that was actually sampled under the old policy?

This object allows PPO to evaluate a candidate update not only by whether it improves the surrogate objective, but by whether it does so using a policy ratio that remains close enough to one to trust the old data.

### Formal definition

A standard PPO clipped surrogate objective is

$$
L^{\text{clip}}(\theta)
= \mathbb{E}\left[\min\Big(r_t(\theta)\widehat A_t,\; \operatorname{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\widehat A_t\Big)\right].
$$

A local distinction is needed here. PPO’s clipped objective is a **training surrogate**, not the literal original expected-return objective of the environment. Its job is to constrain how aggressively the new policy can move relative to the old policy along sampled directions suggested by the advantage estimates. So the clip should be read as a conservative update-shaping device. It modifies the optimization landscape used for training in order to reduce destructive large updates. That is different in kind from SAC, where the underlying objective itself is changed by adding entropy.

### Interpretation paragraph

This objective compares two quantities for each sampled time step. The first is the usual ratio-weighted surrogate term $r_t(\theta)\widehat A_t$. The second uses a clipped ratio that cannot move outside the interval $[1-\epsilon,1+\epsilon]$. By taking the minimum of the unclipped and clipped terms, PPO prevents the optimizer from claiming too much objective improvement from policy changes that push the ratio too far away from one.

The first thing the reader should notice is that PPO is not saying large policy changes are impossible. It is saying that the objective being optimized will stop rewarding them beyond a certain point, at least in the clipped surrogate. This makes the update more conservative.

### Boundary conditions / assumptions / failure modes

PPO clipping is a stabilizing approximation, not a proof of monotonic policy improvement in general practice. It is designed to keep updates more local, but it does not magically certify safety.

Another subtle point is that the surrogate objective is evaluated on data collected under the old policy. If the new policy becomes too different, those samples become a less trustworthy basis for estimating improvement. PPO addresses this through conservative updates, not by removing the underlying issue.

A common failure mode is to describe PPO as “policy gradient plus clipping because clipping works.” That misses the essential point: clipping is there to control how much the policy ratio can influence the update using old-policy data.

### Fully worked example

Suppose at a sampled time step we have estimated advantage

$$
\widehat A_t = 2,
$$

a clip parameter $\epsilon = 0.2$, and a candidate new policy produces ratio

$$
r_t(\theta)=1.5.
$$

First compute the unclipped term:

$$
r_t(\theta)\widehat A_t = 1.5 \cdot 2 = 3.
$$

Now clip the ratio into the interval $[0.8,1.2]$:

$$
\operatorname{clip}(1.5,0.8,1.2)=1.2.
$$

So the clipped term is

$$
1.2 \cdot 2 = 2.4.
$$

PPO takes the minimum of these two because the advantage is positive:

$$
\min(3,2.4)=2.4.
$$

Interpretation: the new policy increased the probability of the sampled positively advantageous action by too much relative to the trust region implied by the clip range. PPO therefore refuses to count the full apparent gain of $3$ and instead only credits $2.4$ in the objective.

Now consider a negative advantage, say

$$
\widehat A_t=-2,
$$
with the same ratio $1.5$. Then the unclipped term is

$$
1.5(-2)=-3,
$$

and the clipped term is

$$
1.2(-2)=-2.4.
$$

Taking the minimum now yields

$$
\min(-3,-2.4)=-3.
$$

This reflects the asymmetry introduced by the sign of the advantage. The objective is constructed so that large harmful ratio movements are not mistakenly favored.

The general lesson is that PPO’s clipping operates through the policy ratio and the sign of the advantage, shaping how aggressively old data can justify a policy change.

### Misconception or counterexample block

**Do not confuse PPO clipping with exact trust-region optimization.**

Clipping is a practical surrogate mechanism for conservative updates. It is not the same as solving an exact constrained optimization problem with full guarantees.

### Connection to later material

PPO is one of the dominant practical actor-style methods because it combines critic-based advantage estimation with a mechanism for update conservatism. Understanding PPO also prepares the reader to recognize a broader design pattern: do not ask only what gradient is being estimated; ask how far the policy is allowed to move per update.

### Retain / Do not confuse

Retain that PPO uses a policy ratio and clipping to keep updates more local when using old-policy data. Do not confuse clipping with a proof of guaranteed safe improvement.

---

## 10. Entropy and why stochasticity may be rewarded

### Why this section exists

Policy optimization naturally tends to increase the probability of actions that appear favorable. But if this happens too aggressively, the policy can collapse prematurely into nearly deterministic behavior before it has learned enough about the environment. This section exists because many actor-style methods include entropy not as decoration, but as an explicit control on premature collapse and brittle exploration.

### The object being introduced

The object is the policy entropy at a state,

$$
\mathcal H(\pi(\cdot\mid s)) = -\sum_a \pi(a\mid s)\log \pi(a\mid s)
$$

in the discrete setting. This is a measure of how spread out the action distribution is. What is fixed is the state. What varies are the action probabilities assigned by the policy. The object answers the question: how uncertain or distributed is the policy’s action selection at this state?

### Formal definition

An entropy-regularized objective may take the form

$$
J_{\text{ent}}(\theta)=J(\theta)+\alpha\, \mathbb{E}[\mathcal H(\pi_\theta(\cdot\mid S_t))],
$$

where $\alpha \ge 0$ controls the weight of the entropy term.

### Interpretation paragraph

Entropy rewards stochasticity. If the policy places all probability mass on one action, entropy is low. If it remains more spread across actions, entropy is higher. By adding entropy to the objective, one is explicitly saying that policy quality is not only about expected return. It is also, to some degree controlled by $\alpha$, about maintaining diversity in the action distribution.

The first thing to notice is that entropy is not automatically beneficial in unlimited quantity. A policy that remains completely random forever may have high entropy and poor reward. Entropy is a control knob, not an unconditional good.

### Boundary conditions / assumptions / failure modes

The usefulness of entropy regularization depends on the task and on the coefficient $\alpha$. Too little entropy pressure and the policy may collapse too early. Too much and the policy may remain too diffuse to exploit what it has learned.

Another subtle point is that entropy changes the optimization objective. It is not merely a variance-reduction trick like a baseline. This distinction is crucial.

A common failure mode is to treat entropy as if it were merely a heuristic to “encourage exploration.” That is directionally true, but incomplete. Entropy is an explicit objective term with a precise mathematical effect on what the policy is being asked to maximize.

### Fully worked example

Consider a state with two actions. Compare two policies:

1. $\pi_1(a_1\mid s)=1, \pi_1(a_2\mid s)=0$,
2. $\pi_2(a_1\mid s)=0.5, \pi_2(a_2\mid s)=0.5$.

Compute entropy for each.

For the deterministic policy,

$$
\mathcal H(\pi_1)=-(1\cdot \log 1 + 0\cdot \log 0).
$$

Using the standard convention that $0\log 0=0$, and since $\log 1=0$,

$$
\mathcal H(\pi_1)=0.
$$

For the uniform binary policy,

$$
\mathcal H(\pi_2)=-(0.5\log 0.5 + 0.5\log 0.5)= -\log 0.5.
$$

Since $\log 0.5<0$, this is positive. So the uniform policy has higher entropy.

Interpretation: the deterministic policy has no uncertainty in action choice, while the uniform policy is maximally spread among the two actions. If an entropy bonus is added to the objective, the uniform policy receives an extra reward-like incentive relative to the deterministic one.

The general lesson is that entropy explicitly values distributional spread in the policy. Whether that is beneficial depends on how it interacts with the return objective.

### Misconception or counterexample block

**Do not confuse entropy with randomness for its own sake.**

Entropy matters only relative to an optimization objective that balances it against return. A high-entropy policy is not automatically desirable unless the objective says it is.

### Connection to later material

This section prepares the reader for SAC, where entropy is not a side bonus tacked onto a return-maximization problem, but part of the central objective structure.

### Retain / Do not confuse

Retain that entropy rewards policy spread and can delay premature collapse. Do not confuse entropy regularization with a baseline; entropy changes the objective itself.

---

## 11. Soft Actor–Critic (SAC) and objective change

### Why this section exists

After PPO, a reader might think the remaining design space is mainly about better estimators or more stable updates. SAC forces a deeper distinction. It shows that one can change not only the estimator or stabilization mechanism, but the objective being optimized. This section exists because SAC is best understood not as “another actor–critic variant,” but as a method built around maximum-entropy reinforcement learning.

### The object being introduced

The object is a maximum-entropy objective, which balances expected return with policy entropy. Instead of asking the policy only to obtain large reward, the objective also rewards stochasticity. What is fixed is the tradeoff coefficient or temperature that balances reward and entropy. What varies are the policy parameters that determine both expected returns and action-distribution entropy.

This object answers a different question than plain policy gradient. It asks: how should the policy behave if we value both reward and sustained stochasticity?

### Formal definition

A soft objective can be written schematically as

$$
J_{\text{soft}}(\pi)=\mathbb{E}\left[\sum_{t} \gamma^t\big(R_{t+1} + \alpha \mathcal H(\pi(\cdot\mid S_t))\big)\right],
$$

where $\alpha$ controls the importance of entropy relative to reward.

### Interpretation paragraph

This objective changes the target itself. The policy is no longer trying merely to maximize expected reward. It is trying to maximize reward while remaining stochastic according to the entropy weighting. That means the best policy under the soft objective need not be the same as the best policy under plain expected-return optimization.

The first thing to notice is that this is a conceptual difference from PPO or from adding a baseline. Baselines do not change what gradient is being estimated in expectation. Clipping constrains how aggressively a surrogate objective can be improved. SAC changes what counts as improvement in the first place.

### Boundary conditions / assumptions / failure modes

The temperature parameter $\alpha$ matters enormously. If it is too small, the method approaches ordinary reward-focused optimization. If it is too large, the policy may prioritize entropy too strongly and underexploit high-reward actions.

Another subtle point is that SAC uses actor–critic machinery, but that does not make it “the same algorithm family as PPO with different code.” The critic in SAC is serving a soft objective structure, and the policy update reflects that structure.

A common failure mode is to say “SAC is just actor–critic plus entropy.” That understates the point. Entropy is not merely a side regularizer in the background. It is built into the optimization target.

### Fully worked example

Suppose a one-state problem has two available stationary policies.

- Policy $\pi_A$ is deterministic and always yields reward $5$ with zero entropy.
- Policy $\pi_B$ is stochastic and yields expected reward $4.4$ with entropy $1.0$.

Let the soft-objective coefficient be $\alpha=1$ and consider one-step evaluation for simplicity.

For $\pi_A$, the soft objective value is

$$
5 + 1\cdot 0 = 5.
$$

For $\pi_B$, the soft objective value is

$$
4.4 + 1\cdot 1.0 = 5.4.
$$

Under ordinary expected-return optimization, $\pi_A$ would be preferred because $5 > 4.4$. Under the soft objective, $\pi_B$ is preferred because its lower reward is compensated by higher entropy.

What changed and what stayed the same? The environment rewards did not change. The policies did not change. What changed was the objective used to evaluate them.

This is the exact boundary line the chapter must keep explicit. PPO mainly changes how policy updates are **stabilized** while still aiming at a reward-centered objective through a surrogate. SAC changes what the policy is **for** by optimizing a maximum-entropy objective in which entropy is part of the target itself. If those two categories are blurred, modern policy methods collapse into one generic “actor–critic family” and the chapter loses its strongest organizing distinction.

The general lesson is that SAC can choose policies that would not be optimal under plain reward maximization because the optimization target is different.

### Misconception or counterexample block

**Do not confuse “same architecture” with “same objective.”**

Two methods may both have actors and critics while optimizing fundamentally different targets. Architecture alone does not determine the conceptual category of the method.

### Connection to later material

SAC is a central example of a broader lesson: in reinforcement learning, one must always ask not only how an update is estimated, but what objective that update is trying to optimize. That habit is essential well beyond this chapter.

### Retain / Do not confuse

Retain that SAC changes the optimization target by incorporating entropy directly into the objective. Do not confuse “uses actor and critic components” with “is just another standard actor–critic method.”

---

## 12. The boundary questions that organize the whole chapter

### Why this section exists

Modern policy-optimization methods are often learned as a sequence of names. That is exactly the wrong way to retain them. This section exists to give a stable set of diagnostic questions that separate these methods along the dimensions that actually matter. Without these questions, the chapter collapses into method memorization.

### The object being introduced

The object is a conceptual checklist for analyzing any policy-optimization algorithm. It is not a formula but an ordering of questions. What is fixed is the intention to compare methods structurally rather than by name. What varies is which algorithm is being examined.

This checklist answers the question: if I encounter a new policy-optimization method, what should I inspect first to understand what it really is?

### Formal definition

Whenever reading a policy-optimization method, ask these questions in order:

1. **What objective is being optimized?**
   Is it plain expected return, a clipped surrogate objective, or a maximum-entropy objective?

2. **What estimator drives the actor update?**
   Is it based on full returns, baseline-adjusted returns, critic-estimated advantages, or something else?

3. **What remains exact and what is approximate?**
   Is the update unbiased in principle, or is bias introduced by critic approximation, clipping, bootstrapping, or target freezing?

4. **What quantity is treated as fixed during differentiation?**
   Are some targets or old-policy quantities treated as constants while optimizing current parameters?

### Interpretation paragraph

This checklist prevents superficial comparison. Two algorithms may both involve log-policy gradients and yet differ fundamentally because one uses a Monte Carlo return while another uses a critic-based approximation. Two algorithms may both use actors and critics, yet differ because one optimizes expected return and the other optimizes a soft entropy-regularized objective. Two algorithms may both use advantage estimates, yet differ because one trusts them inside a plain surrogate while another clips the policy ratio.

The first thing to notice is that these questions are ordered. If one starts with implementation details before identifying the objective, the comparison often becomes confused.

### Boundary conditions / assumptions / failure modes

A common failure mode is to compare algorithms by architecture alone. “This one has an actor and critic, so it is like that other one.” That is too shallow. Another is to compare only by performance lore, such as “PPO is stable” or “SAC explores well,” without identifying what structural design choice produces that behavior.

### Fully worked example

Apply the checklist to four methods discussed in this chapter.

**REINFORCE**

- Objective: plain expected return.
- Estimator: Monte Carlo returns weighting log-policy gradients.
- Exactness: unbiased under standard assumptions.
- Fixed quantities during differentiation: the sampled trajectory return acts as the scalar weight; the gradient arises from policy probabilities.

**Baseline-adjusted REINFORCE**

- Objective: still plain expected return.
- Estimator: returns centered by a state-only baseline.
- Exactness: same expected gradient as REINFORCE if the baseline is valid.
- Fixed quantities during differentiation: the state-only baseline is treated as a fixed scalar under conditioning on the state.

**PPO**

- Objective: clipped surrogate objective.
- Estimator: advantage estimates, usually critic-based, multiplied by policy ratios.
- Exactness: introduces approximation through clipping and estimated advantages.
- Fixed quantities during differentiation: old-policy probabilities are treated as reference values in the ratio.

**SAC**

- Objective: maximum-entropy objective.
- Estimator: actor–critic style updates aligned with the soft objective.
- Exactness: depends on approximation quality, bootstrapping, and implementation details.
- Fixed quantities during differentiation: depends on the specific update, but the key conceptual feature is that entropy enters the target itself.

The general lesson is that the checklist forces you to identify the algorithm’s deepest commitments before worrying about implementation details.

### Misconception or counterexample block

**Do not classify methods only by whether they have a critic.**

A critic is a component. It is not the defining conceptual feature of the objective, the estimator, or the update-stability mechanism.

### Connection to later material

This checklist is useful well beyond the present chapter. It is a durable method for reading reinforcement-learning papers, comparing algorithms, and diagnosing why two methods that look similar in code may behave differently in theory and practice.

### Retain / Do not confuse

Retain the four boundary questions: objective, estimator, approximation source, and fixed quantities during differentiation. Do not confuse algorithm names with algorithm structure.

---

## 13. Common confusions this chapter is meant to prevent

### Why this section exists

A mastery-level chapter should not merely introduce correct formulas. It should also block the false equivalences that make later reasoning unstable. This section gathers the confusions that most often cause policy optimization to feel like a blur.

### Confusion 1: REINFORCE, actor–critic, PPO, and SAC are the same algorithm with small implementation differences

They are not. They differ in objective, estimator, bias–variance profile, and stabilization mechanism. Some preserve the plain expected-return target, some constrain update size through a clipped surrogate, and some change the target through entropy.

### Confusion 2: A baseline changes what gradient is being estimated

A valid state-only baseline does not change the expected policy gradient. Its role is variance reduction. This is an exact statement under the usual assumptions.

### Confusion 3: Actor–critic gives the exact policy gradient but faster

Not necessarily. If the critic is approximate, the actor’s update direction can be biased relative to the exact gradient.

### Confusion 4: PPO clipping proves monotonic safe improvement

No. PPO clipping is a conservative surrogate mechanism designed to reduce instability when using old-policy data. It is not a universal proof of safe improvement in practical settings.

### Confusion 5: SAC is just PPO with entropy added on top

No. SAC is built around a different objective structure. Entropy is part of the target being optimized, not merely an optional decoration.

### Retain / Do not confuse

Retain that modern policy optimization is organized by structural choices, not by superficial naming. Do not confuse variance reduction, objective change, and update-size control with one another.

---

## 14. What this chapter now licenses you to do

### Why this section exists

A foundational chapter is successful only if it changes what the reader can now do correctly. This final section exists to mark those new abilities explicitly, because policy optimization becomes much easier once the reader knows which distinctions to enforce automatically.

### What you should now be able to do

You should now be able to do the following without handwaving.

First, you should be able to explain why policy-gradient methods optimize a different primary object than value-based methods.

Second, you should be able to derive the score-function route conceptually: objective as expectation over trajectories, derivative landing on trajectory probabilities, log-derivative conversion, then decomposition into local policy score terms.

Third, you should be able to explain exactly why a state-only baseline leaves the expected gradient unchanged, and exactly what assumption that argument depends on.

Fourth, you should be able to interpret advantage as relative action quality rather than raw return.

Fifth, you should be able to explain what the critic contributes in actor–critic methods and where bias can enter.

Sixth, you should be able to explain why PPO cares about the policy ratio and what clipping is trying to control.

Seventh, you should be able to state what makes SAC conceptually different: not just its architecture, but its objective.

### Connection to later material

These abilities matter beyond named algorithms. They let you read policy-optimization methods structurally, diagnose what an estimator is really doing, and see where a method’s performance gains are likely coming from: from objective design, estimator choice, approximation, or update control.

### Retain / Do not confuse

Retain that the chapter’s lasting value lies in the distinctions it installs: policy versus value as primary object, return versus advantage, variance reduction versus bias introduction, conservative surrogate optimization versus true objective change. Do not move on if those distinctions still blur together.

---

## 15. Mastery check

A serious reader should be able to answer each of the following in complete sentences, with the relevant variables and assumptions made explicit.

1. Why does direct policy optimization treat the policy as a different primary object than value-based control does?
2. In the score-function derivation, what exact role does the log-derivative identity play?
3. Why does a state-only baseline have zero expected contribution to the policy gradient?
4. What does advantage measure that raw return does not?
5. What exactly does the critic provide in actor–critic methods, and why can that introduce bias?
6. What problem is the PPO ratio-and-clipping mechanism trying to control?
7. Why is entropy regularization not the same kind of modification as a baseline?
8. In what sense does SAC change the optimization target rather than merely stabilizing the estimator?

If any of those questions still produce vague answers, that is not a sign to rush forward. It is a sign that the conceptual boundaries of policy optimization need one more pass. This chapter is where modern reinforcement-learning control either becomes coherent or collapses into a list of algorithm names.
