# Chapter 7 — Function Approximation, the Deadly Triad, and DQN

*Rewritten as mastery-oriented teaching notes from the source chapter at the linked repository directory, following the uploaded writing standard.*

## What this chapter is for

Up to this point, reinforcement learning is easiest to understand in a tabular world. In a tabular method, a value function is literally a table: one location for each state, or one location for each state-action pair. That world is ideal for learning the logic of Bellman equations, bootstrapping, temporal-difference learning, and control. But it is not the world in which modern reinforcement learning usually operates. Realistic problems have too many states to enumerate, too few repeated visits to each individual state, observations that are high-dimensional or continuous, and structure that cannot be exploited if every state is treated as unrelated to every other state.

This chapter explains what changes when the value function is no longer stored exactly in a table. The crucial shift is not merely that a neural network appears. The deeper shift is that the object being learned becomes a **parameterized function**. The learner no longer updates one isolated entry at a time. Instead, it updates shared parameters, and those shared parameters affect predictions at many inputs simultaneously. That single fact changes the entire learning problem.

Once function approximation is introduced, several ideas that were relatively safe in the tabular setting become much more delicate. Bootstrapping can propagate approximation errors. Off-policy data can emphasize parts of the state-action space in a way that conflicts with the target being learned. Shared parameters can make a local update have broad, unintended consequences elsewhere. The interaction of these effects is what later becomes known as the **deadly triad**.

That phrase should be unpacked as an interaction claim, not left as a slogan. The three components are: function approximation, which couples updates across inputs through shared parameters; bootstrapping, which uses current estimates inside future targets; and off-policy learning, which allows the data distribution to differ from the target policy’s induced distribution. Each component alone is already intelligible. The structural instability pressure appears when all three operate together, because target construction, distribution mismatch, and cross-input interference can reinforce one another rather than cancel.

A fully causal reading helps here. Function approximation means one update changes many predictions at once because parameters are shared. Bootstrapping means today’s target is built partly from those mutable predictions rather than from fully realized future outcomes. Off-policy learning means the states and actions most frequently updated need not match the states and actions emphasized by the target policy whose values are being approximated. Put together, these three facts create a feedback loop: prediction errors enter targets, those targets drive shared-parameter updates, and those updates are taken under a distribution that may emphasize the wrong parts of the space for the target being pursued. The deadly triad is therefore not a slogan about three scary words. It is a claim about one coupled error-amplification pathway.

This chapter therefore has a double job. First, it must explain function approximation in a way that makes clear what problem it solves and what new risks it creates. Second, it must explain Deep Q-Networks (DQN) not as “Q-learning plus a neural net,” which is too shallow, but as a carefully stabilized approximate control method built in response to those risks.

If the chapter succeeds, you should finish with five stable insights. First, you should know exactly why tabular methods stop scaling. Second, you should understand why approximation turns value learning into a regression-like problem, but not an ordinary supervised learning problem with fixed labels. Third, you should see why the deadly triad is a structural instability pattern rather than a slogan. Fourth, you should be able to read every term in the DQN target and explain why it is there. Fifth, you should understand why target networks, replay buffers, and representation choices are not implementation decorations but part of the mathematical and algorithmic story.

---

## 1. Why tabular methods stop scaling

### Why this section exists

Earlier chapters can afford to treat a value function as a table because that setting makes the logic of reinforcement learning transparent. But the moment one asks whether the same methods could be used in large games, robotics, control, or vision-based environments, a gap opens immediately. A table requires separate storage and repeated learning for each distinct state or state-action pair. If the relevant space is too large, too sparse, or continuous, that approach breaks. This section exists because the chapter cannot motivate function approximation unless the limits of the tabular world are stated clearly.

### The object being introduced

The object being introduced here is the contrast between a **tabular value function** and a **parameterized approximator**. A tabular value function is a lookup object: give it a state or state-action pair and it returns the stored number associated with exactly that entry. A parameterized approximator, by contrast, is a function with shared parameters. It takes an input and produces a predicted value through a rule controlled by parameters $w$.

The question this contrast answers is: what kind of object should replace a table when exact enumeration is impossible or wasteful? What is fixed is the learning goal—we still want to estimate something like a state value or action value. What varies is the representation used to store and update that estimate. The conclusion this section allows is that scaling forces a change in representation, and that change is conceptually significant.

A second bridge is needed before the chapter moves on. Once the value function becomes parameterized, the learner still writes down something that looks like prediction fitting, but the meaning of the target changes. In ordinary supervised learning, one often imagines a dataset of inputs paired with fixed labels. In approximate reinforcement learning, the target is often assembled from rewards plus estimated continuation values. So the chapter should lock this distinction early: approximate RL may have a regression-shaped loss, but it does not automatically have fixed-label supervision.

### Formal definition

A tabular state-value function stores one number per state:

$$
V(s).
$$

A tabular action-value function stores one number per state-action pair:

$$
Q(s,a).
$$

With function approximation, these are replaced by parameterized predictors such as

$$
\widehat V(s; w)
\qquad \text{or} \qquad
\widehat Q(s,a; w),
$$

where $w$ is a parameter vector.

### Interpretation paragraph

The notation $\widehat V(s;w)$ should be read carefully. The input $s$ is the state whose value is being predicted. The parameter vector $w$ is not a changing variable inside the prediction in the same sense as $s$; it is the collection of weights that determine the shape of the predictor. When learning happens, what is being adjusted is usually $w$, not the state itself. The hat on $\widehat V$ or $\widehat Q$ signals that we are no longer talking about the exact value function. We are talking about an estimate.

The first thing to notice is that a table and a parameterized approximator answer the same kind of question—what is the value associated with this input?—but they do so in very different ways. A table memorizes entries independently. A parameterized model shares structure across inputs through common parameters.

### Boundary conditions / assumptions / failure modes

Tabular methods do not “fail” in a logical sense whenever the state space is large. They fail in a practical and statistical sense. There may be too many entries to store, too few visits to estimate each entry reliably, or states that differ only superficially but must nevertheless be treated as unrelated by a pure table.

Function approximation does not automatically solve the problem. It introduces an inductive bias: the model assumes that different states or state-action pairs can be related through shared parameters. That assumption can be beneficial when similar inputs really should have similar values. It can be harmful when the chosen representation aliases distinct situations together or forces an inappropriate notion of similarity.

A common overgeneralization is to say that function approximation is needed only for continuous spaces. That is false. It is also useful in very large but discrete spaces, because the real issue is not only continuity but scale, sparsity, and generalization.

### Fully worked example

Consider an environment in which the state is the position of an agent on a $1000 \times 1000$ grid. Even before actions are included, there are already

$$
1000 \cdot 1000 = 10^6
$$

possible positions. Suppose there are four actions in every nonterminal state. Then a tabular action-value method would in principle require roughly

$$
4 \cdot 10^6
$$

separate entries.

Now ask what learning from experience looks like. Suppose the agent visits one particular state-action pair $(s,a)$ and receives an update. In a tabular scheme, that update changes only the entry for that exact pair. All other entries remain unchanged. If the agent has never visited a neighboring state that is intuitively similar, the table has no way to transfer what was learned at $(s,a)$ to that neighboring state.

Now imagine instead that we use a parameterized approximator $\widehat Q(s,a;w)$ whose input features include the agent’s coordinates and action identity. If one transition produces a gradient step on $w$, then the value prediction at the observed $(s,a)$ changes, but so can the predictions at nearby coordinates or related actions, because all are produced from the same parameter vector.

What was checked here? First, the combinatorial scale of the tabular object was made explicit. Second, the locality of tabular updates was identified. Third, the parameter-sharing nature of approximation was contrasted with that locality. The conclusion is not that approximation is automatically better. The conclusion is that approximation changes the learning problem from isolated memorization to structured generalization.

The general lesson is that as soon as the relevant space becomes too large to cover densely, the main question is no longer “how do I update this exact entry?” but “how do I learn a function that generalizes from sparse experience?” That is the entry point to approximation-based RL.

### Misconception or counterexample block

**Do not confuse function approximation with “a bigger table.”**

A bigger table is still a table. Each entry remains independent. Function approximation is different because its parameters are shared across inputs. That means an update at one input affects others. The coupling created by shared parameters is the central conceptual shift.

### Connection to later material

Everything that follows in this chapter depends on this representation change. Once updates affect many inputs at once, stability becomes more delicate, and the distinction between “the data distribution” and “the target being learned” becomes more consequential. Later sections on the deadly triad and DQN are best understood as responses to the consequences of parameter sharing.

### Retain / Do not confuse

Retain that tabular methods stop scaling because they require separate learning for separate entries and cannot generalize across unseen or rare inputs. Do not confuse “using a model” with “simply storing more values.” The key new fact is shared parameters.

---

## 2. Function approximation turns value learning into a regression problem

### Why this section exists

Once the value function is parameterized, the next question is how learning should be framed mathematically. In a table, an update rule can be written directly in terms of entry replacement or incremental averaging. With a parameterized predictor, learning looks more like fitting a function to targets. This section exists because the chapter needs to make that change in viewpoint explicit. Without it, later loss functions and gradient updates would appear out of nowhere.

### The object being introduced

The object introduced here is a prediction error objective for a value approximator. The approximator produces a prediction such as $\widehat Q(S_t,A_t;w)$. A target quantity $Y_t$ is constructed from data and, in many RL algorithms, from current or delayed value estimates. The role of learning is then to make the prediction match the target as well as possible.

What is fixed at a given training step is the observed sample $(S_t,A_t,\ldots)$ and the target construction for that step. What varies is the parameter vector $w$ that controls the predictor. The question this object answers is: how should we measure the error of the current value estimate on the observed sample? The conclusion it allows is that approximate value learning can be cast as minimizing a regression-style loss.

### Formal definition

A common per-sample squared prediction loss is

$$
\mathcal L_t(w) = \bigl(Y_t - \widehat Q(S_t,A_t;w)\bigr)^2.
$$

A local term should be fixed here because later chapters and implementations rely on it. A **semi-gradient update** is an update in which the target is treated as fixed for the purpose of differentiating the loss at the current step, even if that target was itself constructed from learned predictions and may be recomputed later. This is the standard move in many approximate RL algorithms. It matters because it keeps the update simple, but it also means the optimization is not identical to full differentiation through every dependency inside the target.

More generally, one can consider expected losses such as

$$
\mathbb E\bigl[(Y_t - \widehat Q(S_t,A_t;w))^2\bigr],
$$

where the expectation is taken with respect to the training distribution over samples.

### Interpretation paragraph

This loss has the same surface form as ordinary supervised learning: target minus prediction, squared. But one must be careful not to import all the intuitions of standard supervised learning without inspection. In ordinary regression, the labels are typically treated as fixed truths supplied by a dataset. In reinforcement learning, the target $Y_t$ is often constructed from rewards plus estimated future values. That means the target may itself depend on a value function estimate.

The important thing to notice first is that the role of the approximator is not to recover some direct oracle-provided ground-truth label at each state-action pair. Instead, it is trying to fit targets assembled from experience, and those targets may involve bootstrapping. The resulting optimization problem therefore has a regression appearance but a more delicate structure.

### Boundary conditions / assumptions / failure modes

The squared loss is not mandatory. Other losses are possible. But squared error is standard because it is simple, differentiable, and directly penalizes mismatches between target and prediction.

A major hidden assumption in interpreting the loss is whether the target is treated as fixed during differentiation. In many practical RL algorithms, the answer is yes for the current update step, even if the target is recomputed later. That is what leads to **semi-gradient** methods, discussed later.

A major failure mode is to say, “Approximate value learning is just supervised learning.” That is too crude. The target distribution is induced by the interaction process, and the targets themselves may depend on current predictions. This matters because moving targets and self-referential targets create instability that fixed-label regression does not usually face.

The clean way to state the distinction is this. In ordinary supervised learning, the target label is usually treated as externally given for the current update. In approximate RL, the loss may have the same surface form, but the target often depends on the learner’s own current or recently frozen predictions, on a behavior-generated data distribution, and on a bootstrapped continuation rule. So the loss is regression-shaped, but its target-generation process is endogenous to the learning system. That is exactly why importing standard supervised-learning intuitions without inspection can be dangerous.

### Fully worked example

Suppose at some time step we observe the transition

$$
(S_t,A_t,R_{t+1},S_{t+1}) = (s_1, a_2, 3, s_2).
$$

Assume that the current approximator predicts

$$
\widehat Q(s_1,a_2;w)=4.5.
$$

Suppose the target rule for the current method produces

$$
Y_t = 5.2.
$$

Then the per-sample loss is

$$
\mathcal L_t(w) = (5.2 - 4.5)^2 = 0.7^2 = 0.49.
$$

So far this looks like an ordinary squared-error calculation. But now inspect where the target came from. Suppose that target was built as

$$
Y_t = R_{t+1} + \gamma \max_{a'} \widehat Q(S_{t+1},a';w^-),
$$

with $\gamma=0.9$ and target-network estimate

$$
\max_{a'} \widehat Q(s_2,a';w^-)=\frac{2.2}{0.9}=2.444\ldots
$$

so that the total target equals roughly $3+2.2=5.2$.

Now the important reasoning step appears. The target is not a human-provided truth label for $(s_1,a_2)$. It is a reward-plus-estimated-continuation quantity built partly from another value estimate at the next state. The loss therefore measures disagreement between one prediction and a target that itself depends on a learned value function.

What conclusion does each step allow? The direct arithmetic shows how the loss is computed. The target decomposition shows why the regression framing is only partial. The final interpretation is that approximate RL uses regression machinery, but the targets are endogenous to the learning system.

The general lesson is that when you see a squared value loss in RL, you should immediately ask two questions. First, what exactly is the target? Second, which parts of that target are fixed during the current update and which parts are outputs of learned models?

### Misconception or counterexample block

**Do not confuse “regression form” with “ordinary supervised learning.”**

The expression

$$
(Y_t - \widehat Q(S_t,A_t;w))^2
$$

has the shape of a regression loss, but the semantics of $Y_t$ are different when the target is bootstrapped or depends on learned predictors. That difference is not cosmetic. It is one of the central reasons approximate RL can be unstable.

### Connection to later material

This regression viewpoint prepares the ground for DQN. DQN will define a specific target $Y_t^{\mathrm{DQN}}$ and then fit an online action-value network to that target. The difficulty, and later the design of target networks and replay buffers, comes from the fact that those targets are not fixed labels from a static dataset.

### Retain / Do not confuse

Retain that function approximation turns value estimation into fitting predictions to targets. Do not confuse the presence of a squared loss with the presence of stable fixed labels.

---

## 3. Shared parameters and the new coupling of updates

### Why this section exists

The last section explained why value learning with approximation looks like regression. But that still does not fully explain why approximation changes the dynamics so dramatically. The decisive fact is parameter sharing. In a table, an update is local to one entry. In a parameterized model, one update can alter predictions far away from the sampled input. This section exists because the deadly triad cannot be understood unless this coupling is made explicit.

### The object being introduced

The object introduced here is the idea of **cross-input coupling through shared parameters**. The approximator $\widehat Q(s,a;w)$ uses the same parameter vector $w$ for all inputs. Therefore, when $w$ is updated using one sample, predictions at many other state-action pairs may change as a side effect.

What is fixed is the functional form of the approximator and the fact that all predictions are generated from the same parameters. What varies is the specific input used to generate the current gradient update. The conclusion this object allows is that approximation creates generalization, but also interference.

### Formal definition

There is no single formula that defines coupling more fundamentally than the approximator itself:

$$
\widehat Q(s,a;w).
$$

The key fact is that for two different inputs $(s,a)$ and $(s',a')$, both predictions depend on the same $w$. After an update

$$
w \leftarrow w + \Delta w,
$$

both

$$
\widehat Q(s,a;w)
\qquad \text{and} \qquad
\widehat Q(s',a';w)
$$

may change.

### Interpretation paragraph

This is what parameter sharing means operationally. The model is not storing one independent number for each input. It is storing a compact parameterization whose outputs are linked. That linkage is what allows generalization from sparse experience: learning something about one part of the space can improve predictions elsewhere. But it is also what allows destructive interference: improving the fit on one sample can worsen the fit on another.

The first thing to notice is that approximation does not merely reduce memory usage. It introduces a geometry of prediction space in which changes propagate through shared structure.

### Boundary conditions / assumptions / failure modes

The strength and pattern of coupling depend on the representation and model class. Some approximators, such as local basis-function methods, may produce relatively local generalization. Deep networks may produce much broader and harder-to-predict coupling.

A common hidden assumption is that “similar inputs should have similar values.” That may be reasonable or disastrous depending on whether the representation exposes the right notion of similarity. If the state representation hides distinctions that matter for return, then the approximator is forced to share where it should separate.

### Fully worked example

Suppose the approximator is linear in features:

$$
\widehat Q(s,a;w)=w^\top x(s,a),
$$

where $x(s,a)$ is a feature vector. Consider two inputs $(s_1,a_1)$ and $(s_2,a_2)$ with feature vectors

$$
x(s_1,a_1) = \begin{bmatrix}1 \\ 1\end{bmatrix},
\qquad
x(s_2,a_2) = \begin{bmatrix}1 \\ 0\end{bmatrix},
$$

and current parameters

$$
w = \begin{bmatrix}2 \\ -1\end{bmatrix}.
$$

Then the predictions are

$$
\widehat Q(s_1,a_1;w)=2 + (-1)=1,
$$

and

$$
\widehat Q(s_2,a_2;w)=2.
$$

Now suppose a training step updates the parameters to

$$
w' = \begin{bmatrix}2.5 \\ -0.8\end{bmatrix}.
$$

This update may have been generated entirely from the sample $(s_1,a_1)$, but let us inspect its broader effect.

The updated prediction at the sampled input is

$$
\widehat Q(s_1,a_1;w') = 2.5 + (-0.8)=1.7.
$$

The updated prediction at the other input is

$$
\widehat Q(s_2,a_2;w')=2.5.
$$

So even though $(s_2,a_2)$ was not observed during this update, its prediction changed from $2$ to $2.5$ because the first feature component is shared across both inputs.

What was checked? First, the shared dependence on $w$ was made explicit through the feature map. Second, an update generated from one sample was applied. Third, the effect on another input was computed directly. The conclusion is that function approximation couples learning across inputs by design.

The general lesson is that later when an algorithm becomes unstable, one must not imagine the error as trapped in one state-action pair. Shared parameters can move that error through the representation.

### Misconception or counterexample block

**Do not confuse generalization with guaranteed improvement elsewhere.**

Parameter sharing means one update can influence many predictions. It does **not** mean that the influence will be beneficial. Generalization and interference are two sides of the same mechanism.

### Connection to later material

The deadly triad becomes genuinely dangerous only because of this coupling. If approximation were not shared, bootstrapping errors would not spread through the state space in the same way, and off-policy mismatch would have weaker cross-state consequences.

### Retain / Do not confuse

Retain that shared parameters create both generalization and interference. Do not confuse “nonlocal update effect” with “better learning.” The same mechanism can help or harm.

---

## 4. Bootstrapping under approximation

### Why this section exists

Earlier chapters introduced bootstrapping as a core reinforcement-learning idea: instead of waiting for complete returns, a learner can update current predictions using estimates of future predictions. In the tabular world, this often works well. But once function approximation is introduced, bootstrapping takes on a new character. This section exists because the chapter needs to explain why a previously useful idea becomes more dangerous in the presence of approximation.

### The object being introduced

The object being introduced is a **bootstrapped target**. Instead of defining a target solely from observed rewards or full returns, the learner uses current or delayed value estimates to approximate future value. A generic one-step action-value target has the shape

$$
Y_t = R_{t+1} + \gamma \times \text{estimated continuation}.
$$

What is fixed is the observed transition and the target construction rule. What varies is the value estimate used for the continuation term. The question this object answers is: how can we update current values without waiting for the entire future to be observed? The conclusion it allows is faster and more sample-efficient learning, but at the cost of self-referential targets.

### Formal definition

A generic bootstrapped one-step target for action-value learning can be written as

$$
Y_t = R_{t+1} + \gamma \widehat U_{t+1},
$$

where $\widehat U_{t+1}$ is an estimate of future value constructed from current or delayed predictions.

For example, in Q-learning style control the continuation estimate often takes the form

$$
\max_{a'} \widehat Q(S_{t+1},a';\cdot).
$$

### Interpretation paragraph

Bootstrapping means that the learner is using part of its own current belief structure to define the target it is trying to fit. This is efficient because the learner does not need to wait until the end of an episode to propagate information backward. But it also means that errors in current estimates can enter future targets. Under function approximation, where many inputs are coupled, such errors can be propagated and amplified in more complex ways.

The first thing to notice is that the target is partly empirical and partly estimated. The reward term comes from observed experience. The continuation term comes from the model’s current estimate of the future.

### Adversarial misconception block: why the supervised-learning analogy is dangerous if left unqualified

It is helpful to notice the superficial resemblance to supervised learning: there is an input, a prediction, a target-like quantity, and a squared-error loss. But a hostile reading asks what makes the target trustworthy. In ordinary supervised learning, the label is usually treated as an externally given outcome for the current example. In approximate reinforcement learning, the target often contains the system's own current or recent estimate of future value. That difference is not cosmetic. It means that changing the predictor can change future targets, so the learning problem is partly self-referential.

This is why the supervised analogy is useful only up to a boundary. It helps explain the optimization shape. It does not justify importing all the stability intuitions of fixed-label regression.

### Boundary conditions / assumptions / failure modes

Bootstrapping is not “bad” in itself. It is one of the central reasons temporal-difference methods are efficient. The important issue is that bootstrapping creates feedback: current predictions influence future targets.

In the presence of approximation, that feedback may be destabilizing if the continuation term is inaccurate, if errors spread through shared parameters, or if the data distribution does not align with the target policy’s relevant states.

A common overgeneralization is to say that Monte Carlo methods are always safer because they use returns rather than bootstrapped targets. They avoid one particular source of self-reference, but they introduce their own issues such as higher variance and weaker temporal credit propagation. The point here is not that bootstrapping is wrong. The point is that under approximation it must be handled with respect.

### Fully worked example

Suppose the learner observes

$$
R_{t+1}=1,
qquad
\gamma = 0.9,
$$

and current continuation estimates at the next state are

$$
\widehat Q(S_{t+1},a_1)=4,
\qquad
\widehat Q(S_{t+1},a_2)=2.
$$

Then a Q-learning style one-step target would be

$$
Y_t = 1 + 0.9 \max\{4,2\} = 1 + 0.9 \cdot 4 = 4.6.
$$

Now imagine that the true best continuation value at $S_{t+1}$ should really have been $2.5$, but the model currently overestimates it as $4$. Then the target is inflated by

$$
0.9(4-2.5)=1.35.
$$

That means the current state-action prediction is being pushed upward using a continuation estimate that is already too large.

Under a table, the damage of that inflated target may remain more local. Under function approximation, the inflated update changes shared parameters. Those parameter changes can then alter predictions at many other inputs, including future continuation estimates used in later targets.

What was checked? First, the target was computed numerically. Second, the effect of a misestimated continuation value was isolated. Third, the structural consequence under approximation was identified: the target error need not remain local.

The general lesson is that bootstrapping introduces a feedback channel from current prediction errors into future learning targets. With shared parameters, that feedback can propagate across the space rather than staying where it began.

### Misconception or counterexample block

**Do not interpret a bootstrapped target as an observed truth.**

The reward term is observed. The continuation term is estimated. A bootstrapped target is therefore partly data and partly current model belief. That is exactly why it can accelerate learning and exactly why it can destabilize learning.

### Connection to later material

Bootstrapping is the second corner of the deadly triad. DQN retains bootstrapping because it is too valuable to discard, but it adds mechanisms intended to soften the instability that bootstrapping can cause when combined with approximation.

### Retain / Do not confuse

Retain that bootstrapping uses learned estimates inside targets. Do not confuse “target” with “ground truth label.” In approximate RL, targets often contain predictions.

---

## 5. Off-policy learning and distribution mismatch

### Why this section exists

The next ingredient in the deadly triad is off-policy learning. Earlier chapters likely introduced the distinction between learning from the same policy that generates data and learning about a different policy than the behavior policy. That distinction becomes much sharper under approximation because the distribution of training samples now matters for which parts of the function are fit well. This section exists because the chapter cannot explain the triad without clarifying what off-policy means at the level of data distribution.

### The object being introduced

The object introduced here is the distinction between a **behavior distribution** and the distribution relevant to the **target policy or target operator**. The behavior policy generates the observed transitions used for learning. The target of learning may correspond to a different policy or to a greedy control operator.

What is fixed is the observed dataset or stream of sampled transitions. What varies is the policy or value target that the algorithm is effectively trying to learn about. The question this object answers is: what changes when the states and actions emphasized by the data are not the same as the states and actions most relevant to the target? The conclusion it allows is that approximation will be shaped by the data distribution, which may or may not align with the target’s needs.

### Formal definition

A learning method is **on-policy** if the data distribution is generated by the same policy whose value structure is being estimated or improved.

It is **off-policy** if the data distribution is generated by a behavior policy different from the policy implicit in the target or learning objective.

In Q-learning-style control, the target often uses a greedy continuation term such as

$$
\max_{a'} \widehat Q(S_{t+1},a'),
$$

regardless of which action was actually selected by the behavior policy.

### Interpretation paragraph

The key issue is not merely that two policy names differ. The key issue is that learning with function approximation is weighted by the data that are actually seen. If the dataset emphasizes some regions heavily and others only rarely, the approximator will usually fit those regions unevenly. When the target depends on a different policy structure than the behavior distribution, the learner may be asked to fit values well in exactly those areas the data undersample or sample in a skewed way.

The first thing to notice is that off-policy learning is partly a question about **distributional emphasis**. Which states and actions are visited often? Which are rarely constrained by data? Approximation makes these questions central because the fitted function is only as good as the training signal shaping it.

### Boundary conditions / assumptions / failure modes

Off-policy does not automatically imply instability. In fact, off-policy learning is extremely useful because it allows reuse of old experience, learning from exploratory behavior while improving a greedier policy, and training from logged data.

The important failure mode is to ignore the interaction between off-policy data and function approximation. If the data distribution poorly covers the regions most important to the target, then errors can persist or even worsen in those regions, especially when bootstrapping feeds those errors back into later targets.

A common confusion is to think that replay buffers make a method on-policy because they reuse experience from the same agent. That is false. Replay changes sample reuse and correlation structure; it does not erase the distinction between the behavior distribution and the target policy structure.

### Fully worked example

Suppose an agent has two possible actions in each state, left and right. The behavior policy is exploratory and chooses left with probability $0.9$ and right with probability $0.1$ in a broad region of the state space. However, the learning target is greedy control, which is increasingly interested in the right action because that action leads to high long-run reward.

Now consider what the approximator experiences during training. Most samples in that region involve the left action. The fitted function therefore receives much denser error information about $Q(s,\text{left})$ than about $Q(s,\text{right})$.

Suppose in a particular next state $s'$ the model currently overestimates

$$
\widehat Q(s',\text{right}) = 10
$$

when the true desirable value should be closer to $6$, while the left-action estimate is accurate at $2$. A Q-learning style target at predecessor states uses

$$
\max\{\widehat Q(s',\text{left}), \widehat Q(s',\text{right})\} = 10.
$$

So predecessor targets are computed using the overestimated right-action value, even though the data reaching $s'$ may have come mostly from left-action behavior and may rarely provide corrective evidence about right-action estimates.

What is being checked here? First, the behavior distribution places much more weight on left than right. Second, the target construction uses a greedy operator that cares about the maximally valued continuation, which is right in this example. Third, the approximator receives sparse correction for the very action dominating the target. The conclusion is that off-policy mismatch can let errors in poorly constrained parts of the value function influence many updates.

The general lesson is that under approximation, what matters is not only what target you want to learn, but whether your data distribution actually constrains the relevant parts of the function well enough to support that target.

### Misconception or counterexample block

**Do not confuse off-policy with “using old data.”**

Using old data may or may not be off-policy depending on what policy generated that data and what policy the target corresponds to. Off-policy is about a mismatch between behavior distribution and target policy structure, not merely about data age.

### Connection to later material

Off-policy learning is the third corner of the deadly triad. DQN is off-policy in exactly this structural sense: it learns from replayed transitions generated under exploratory behavior while fitting a greedy control target based on maximization at the next state.

### Retain / Do not confuse

Retain that off-policy means learning from a data distribution different from the policy structure implicit in the target. Do not confuse replay, logged data, or stale data with the definition of off-policy itself.

---

## 6. The deadly triad

### Why this section exists

At this point the chapter has introduced the three components separately: function approximation, bootstrapping, and off-policy learning. But the deadly triad is not a mere list of three bad words. The point of the triad is that these ingredients interact. This section exists because students often understand each piece individually but fail to see why the combination creates a distinctive stability risk.

### The object being introduced

The object introduced here is the **deadly triad** itself: the simultaneous presence of function approximation, bootstrapping, and off-policy learning. It is not a theorem saying divergence must occur in every such method. It is a structural warning about a class of feedback loops that can make learning unstable.

What is fixed is the presence of all three ingredients in the same method. What varies is the environment, representation, optimization scheme, and algorithmic stabilizers. The question this object answers is: why do methods that look like natural extensions of tabular RL become fragile in the approximate setting? The conclusion it allows is not fatalism, but informed caution.

### Formal definition

The deadly triad consists of:

1. **Function approximation**: value estimates are represented by a parameterized function such as $\widehat Q(s,a;w)$ rather than independent table entries.
2. **Bootstrapping**: targets depend on current or delayed value estimates, for example through terms like $\gamma \max_{a'} \widehat Q(S_{t+1},a';\cdot)$.
3. **Off-policy learning**: the data distribution differs from the policy or target operator implicit in the update target.

### Interpretation paragraph

Why is this combination dangerous? Function approximation means errors do not stay local; they can spread through shared parameters. Bootstrapping means current errors can re-enter later targets, so they can feed themselves forward. Off-policy learning means the parts of the function that dominate the target need not be the parts best constrained by the data. Put together, these ingredients create a setting in which inaccurate predictions can be propagated, amplified, and insufficiently corrected.

The first thing to notice is that the danger is an interaction pattern. Approximation alone is not the problem. Bootstrapping alone is not the problem. Off-policy learning alone is not the problem. The risk emerges when all three act on one another.

### Boundary conditions / assumptions / failure modes

The phrase “deadly triad” can tempt people into two opposite mistakes. One mistake is to dismiss it as exaggeration because some modern methods work well in practice. The other mistake is to interpret it as a proof that any approximate off-policy bootstrapping method must diverge. Both are wrong.

The triad identifies a region of algorithm design where instability is structurally plausible. Whether a given method actually diverges depends on many details: representation choice, optimization dynamics, target lag, data coverage, step sizes, architecture, normalization, clipping, and more.

A common overgeneralization is to think the triad matters only for deep networks. It matters more generally for approximate value learning whenever these three ingredients coexist.

### Fully worked example

Consider a simplified chain of reasoning rather than a single arithmetic computation. Suppose the learner currently overestimates the value of a certain action in a next state $s'$. Denote this overestimate by

$$
\widehat Q(s',a^*;w) > Q^*(s',a^*).
$$

Now follow the three ingredients in order.

**Step 1: Bootstrapping.** A predecessor transition into $s'$ uses a target of the form

$$
Y = R + \gamma \max_{a'} \widehat Q(s',a';w^-).
$$

Because the continuation estimate is too large, the predecessor target is also too large.

**Step 2: Function approximation.** The predecessor update changes shared parameters. Those parameter changes alter not only the predecessor prediction but many other predictions, including possibly values at states that resemble the predecessor or share important features.

**Step 3: Off-policy learning.** Suppose the behavior data undersample the very regions where the overestimated continuation values live. Then the learner may receive insufficient direct correction in those regions, even while those same values continue to dominate greedy targets through the max operator.

Now ask what conclusion each step allows. The first step shows that target error is created from current prediction error. The second step shows that the resulting update can affect many parts of the function, not just one. The third step shows that data need not strongly constrain the parts of the function that most influence greedy targets. Combined, this creates the possibility that error will not shrink cleanly and may instead spread or reinforce itself.

The general lesson is that the deadly triad is a feedback-system diagnosis. It identifies a set of couplings through which approximate value learning can become unstable.

### Misconception or counterexample block

**Do not say “the deadly triad means these methods never work.”**

That is false. Many successful RL systems use all three ingredients. The correct interpretation is that this combination needs deliberate stabilization. The triad explains why those stabilizers are necessary in the first place.

### Connection to later material

DQN is the first major algorithm in this chapter that should be read against the background of the deadly triad. Target networks and replay buffers are not accidental engineering choices. They are attempts to make this risky combination workable.

### Retain / Do not confuse

Retain that the deadly triad is the interaction of approximation, bootstrapping, and off-policy learning. Do not confuse “risk structure” with “guaranteed failure” or with “mere folklore.”

---

### "This does not imply" paragraph for the deadly triad

The deadly triad does **not** say that the presence of function approximation, bootstrapping, and off-policy learning guarantees divergence in every case. Its point is more adversarial and more useful: when all three are active, the system contains a mechanism by which approximation error, target drift, and distribution mismatch can reinforce one another rather than cancel. That is an instability pressure claim, not a universal impossibility theorem.

Why make this explicit? Because a student who treats the triad as a slogan will either overpanic or underthink. The mature reading is: when these three ingredients coexist, one should demand a stability story rather than assuming tabular intuitions transfer unchanged.

## 7. DQN as approximate Q-learning

### Why this section exists

The chapter has now developed the conceptual need for stabilization. The next question is what a concrete algorithm looks like once tabular Q-learning is moved into the function-approximation setting. DQN is the canonical answer historically and pedagogically. This section exists because the reader now has enough conceptual background to understand DQN not as magic, but as a particular approximate control scheme built from familiar ingredients.

### The object being introduced

The object introduced here is the DQN update target. DQN uses a neural network to approximate the action-value function and retains the greedy one-step target structure of Q-learning. However, it evaluates the continuation term using a separate, frozen set of target parameters.

What is fixed for a sampled update is one observed transition and the current target-network parameters. What varies is the online parameter vector being optimized to fit the target. The question this object answers is: what target should a neural action-value network chase on a sampled transition if we want Q-learning style control with some stabilization? The conclusion it allows is a usable update rule for approximate greedy control.

### Formal definition

For a sampled transition

$$
(S_t, A_t, R_{t+1}, S_{t+1}, \zeta_t),
$$

where $\zeta_t \in \{0,1\}$ indicates whether the transition is terminal, the DQN target is

$$
Y_t^{\mathrm{DQN}} = R_{t+1} + \gamma (1-\zeta_t) \max_{a'} Q(S_{t+1}, a'; w^-).
$$

The online network prediction being fit is

$$
Q(S_t,A_t;w),
$$

where $w$ denotes the online parameters and $w^-$ denotes the frozen target-network parameters.

### Interpretation paragraph

This formula should be read term by term, not as a block to memorize. The observed reward $R_{t+1}$ is the immediate empirical part of the target. The factor $(1-\zeta_t)$ is a terminal mask: it decides whether future continuation should be included at all. If the transition ends the episode, then no future value should be added. The greedy continuation term

$$
\max_{a'} Q(S_{t+1},a';w^-)
$$

asks which next action currently looks best according to the target network. The discount factor $\gamma$ scales that continuation according to temporal distance.

The first thing to notice is that DQN keeps the control logic of Q-learning. It still uses a max over next-state actions. What changes is how the value function is represented and how the continuation estimate is stabilized.

### Boundary conditions / assumptions / failure modes

The terminal mask is not optional. If the next state is terminal, the continuation term must be excluded; otherwise the algorithm would incorrectly add value beyond episode end.

The target is still bootstrapped and still off-policy in the sense discussed earlier. DQN does not escape the deadly triad by deleting those ingredients. It instead tries to control their interaction.

To make that sentence operational, identify the interaction pressure one device at a time. Replay reduces the short-range correlation of successive updates and changes how often particular transitions are reused. Target networks slow the motion of the bootstrap target so that the predictor is not fitting a target generated by its own immediately changing parameters. Neither device turns the problem back into tabular learning or fixed-label supervised learning. Each one only weakens one link in the feedback loop described above.

That sentence should be made more operational. Replay buffers address one part of the problem by reducing short-range temporal correlation and improving data reuse across updates. Target networks address another part by slowing the movement of the bootstrap target so the predictor is not chasing a target generated by its own immediately changing parameters. Neither device eliminates approximation, bootstrapping, or off-policy learning. Each one instead reduces how violently those ingredients interact over short training windows.

A common hidden assumption is that the max operator always provides a good control target. In practice, the max can also amplify overestimation bias, which motivates later variants such as Double DQN. That issue is beyond the main purpose of this chapter, but it is worth noticing that even the target structure itself can create additional approximation difficulties.

### Fully worked example

Suppose a sampled transition is

$$
(S_t,A_t,R_{t+1},S_{t+1},\zeta_t) = (s_1,a_2,2,s_2,0),
$$

and the discount factor is

$$
\gamma = 0.95.
$$

Assume the target network gives the following next-state action values:

$$
Q(s_2,a_1;w^-)=5,
\qquad
Q(s_2,a_2;w^-)=3.5,
\qquad
Q(s_2,a_3;w^-)=4.2.
$$

We want to compute the DQN target.

First identify the continuation action value. The max over actions is

$$
\max_{a'} Q(s_2,a';w^-)=5.
$$

Because $\zeta_t=0$, the transition is nonterminal, so the terminal mask is

$$
1-\zeta_t = 1.
$$

Now apply the target formula:

$$
Y_t^{\mathrm{DQN}} = 2 + 0.95 \cdot 1 \cdot 5 = 2 + 4.75 = 6.75.
$$

Now change only one fact: suppose instead that the sampled transition is terminal, so $\zeta_t=1$. Then the continuation must vanish:

$$
Y_t^{\mathrm{DQN}} = 2 + 0.95 \cdot 0 \cdot 5 = 2.
$$

What was checked at each step? First, the immediate reward was identified. Second, the maximal continuation estimate was computed from the target network. Third, the terminal flag was used to decide whether continuation should be allowed. Fourth, the terms were combined into the final target. The conclusion is that the DQN target is a one-step greedy bootstrap target with explicit terminal handling.

The general lesson is that every DQN target should be parsed in the same order: immediate reward, terminal status, greedy next-state estimate, discounting, final sum.

### Misconception or counterexample block

**Do not confuse the online and target networks.**

The prediction being updated during the current step is usually

$$
Q(S_t,A_t;w).
$$

The continuation estimate inside the target is usually computed with

$$
Q(S_{t+1},a';w^-).
$$

Those are different parameter sets playing different roles.

### Connection to later material

This target is the heart of DQN. The next sections explain why the target network is frozen, why replay is used, and why the resulting gradient has a semi-gradient interpretation. Those details matter because without them the approximate Q-learning target can become too unstable to train reliably.

### Retain / Do not confuse

Retain that DQN keeps the Q-learning max target but evaluates continuation with frozen target parameters and masks terminal transitions explicitly. Do not confuse the sampled online prediction with the target-network continuation estimate.

---

## 8. Why the target network is frozen

### Why this section exists

The DQN target introduced above contains a second parameter vector $w^-$. That is not a superficial notation choice. It is one of the algorithm’s main stabilization devices. This section exists because the reader should understand not only that the target network is frozen, but exactly what problem freezing addresses.

### The object being introduced

The object is the **target network**, a copy of the action-value network whose parameters are held fixed for a period while the online network is updated. The target network defines the continuation part of the DQN target. The online network is the one being optimized.

What is fixed during a block of updates is $w^-$. What varies update by update is the online parameter vector $w$. The question this object answers is: how can we reduce instability caused by the target changing at the same moment the predictor is trying to chase it? The conclusion it allows is a slower-moving target.

### Formal definition

During online updates, DQN uses the target

$$
Y_t^{\mathrm{DQN}} = R_{t+1} + \gamma (1-\zeta_t) \max_{a'} Q(S_{t+1}, a'; w^-),
$$

while fitting the online network prediction

$$
Q(S_t,A_t;w).
$$

The target parameters $w^-$ are updated only periodically or through a slower update rule, rather than at every gradient step.

### Interpretation paragraph

If the same rapidly changing parameter vector were used both to define the target and to define the prediction being fit, then the learner would be chasing a target that moves exactly when the predictor moves. This is a difficult optimization geometry. The learner is not just trying to fit a target; it is trying to fit a target that can shift immediately as a consequence of the very parameters being updated.

Freezing $w^-$ does not make the target permanent. It makes the target **temporarily more stationary**. The first thing to notice is that this is a timescale separation device. The online network moves at the step-by-step learning timescale. The target network moves at a slower timescale.

### Boundary conditions / assumptions / failure modes

Freezing the target network does not solve all stability problems. The target is still bootstrapped and still based on learned predictions. It is simply less volatile than it would be if it were tied exactly to the online parameters.

A common overstatement is that the target network makes DQN “supervised learning.” That is false. The targets remain bootstrapped and periodically refreshed from learned value estimates. Freezing only slows target drift.

Another failure mode is to think the target network is needed for correctness in some exact mathematical sense. In reality, it is a stabilization heuristic with a clear conceptual rationale, not a theorem that the algorithm cannot be defined without it.

### Fully worked example

Suppose that at training step 1 the target-network continuation estimate at a certain next state is

$$
\max_{a'}Q(S_{t+1},a';w^-)=4.
$$

With reward $R_{t+1}=1$ and $\gamma=0.9$, the target is

$$
Y_1 = 1 + 0.9\cdot 4 = 4.6.
$$

Now suppose the online network is updated aggressively and, if it were also used as the target network immediately, the continuation estimate for the same next state would jump to $6$ at the very next step. Then the corresponding target would become

$$
Y_2 = 1 + 0.9\cdot 6 = 6.4.
$$

So from one step to the next, the value being chased would jump from $4.6$ to $6.4$, even if the underlying environment evidence about that transition had not changed at all. The learner is now trying to fit a moving objective whose own movement is partly caused by the learner’s previous update.

If instead the target network remains frozen, then for several online updates the continuation estimate stays at $4$, so the target remains $4.6$ for that state while the online network tries to move toward it. Only later, when the target network is refreshed, does the continuation estimate change.

What was checked? First, the target’s dependence on continuation estimates was made explicit. Second, the effect of letting those continuation estimates change immediately with the online network was computed. Third, the stabilizing effect of holding them fixed temporarily was described. The conclusion is that freezing reduces the speed of target drift.

The general lesson is that whenever a model is learning from targets generated by another learned model, one should ask whether those two objects need to move on different timescales.

### Misconception or counterexample block

**Do not say “the target network is just a copy for convenience.”**

Its purpose is algorithmic. It slows target movement. That is not convenience; that is stabilization.

### Connection to later material

Target-network lag is a recurring design idea in deep RL. Later methods generalize the same intuition in different forms. The key principle is that if a target is built from learned estimates, separating the target’s update timescale from the online learner’s update timescale can make optimization more stable.

### Retain / Do not confuse

Retain that the target network exists to slow target drift. Do not confuse a slowly moving target with a truly fixed supervised label.

---

## 9. Replay buffers and why DQN reuses experience

### Why this section exists

DQN is not defined only by its target network. A second major ingredient is experience replay. Students sometimes remember replay as a memory trick, but that is too shallow. Replay changes the statistical character of the training data and makes better use of collected transitions. This section exists because those changes are central to why DQN became workable.

### The object being introduced

The object introduced here is the **replay buffer**, a storage mechanism that collects past transitions and later samples mini-batches from them for training. Instead of updating only on the most recent transition, the learner trains on a distribution induced by stored experience.

What is fixed is the stored collection of transitions at a given moment. What varies is which sampled batch is drawn from that collection for the current update. The question this object answers is: why should an RL learner break the tight temporal coupling between data collection and parameter updates? The conclusion it allows is reduced short-range correlation and improved sample reuse.

### Formal definition

A replay buffer stores transitions of the form

$$
(S_t,A_t,R_{t+1},S_{t+1},\zeta_t).
$$

Training updates sample transitions or mini-batches from the buffer and use them to construct DQN targets and losses such as

$$
\bigl(Y_t^{\mathrm{DQN}} - Q(S_t,A_t;w)\bigr)^2.
$$

### Interpretation paragraph

In online interaction, consecutive transitions are often highly correlated. If the learner updated directly and only on those transitions in strict temporal order, then the gradient signal could be dominated by narrow, locally repetitive slices of experience. Replay partially breaks that sequence by mixing transitions from different times. This makes the training batches look less like a short correlated trajectory fragment and more like draws from a broader empirical distribution.

Replay also improves sample efficiency. A single transition is expensive to collect in RL because it comes from interaction. Reusing it in multiple updates extracts more learning signal from the same experience.

The first thing to notice is that replay changes the training distribution. It is not just storage; it is a way of reshaping how experience is presented to the optimizer.

### Boundary conditions / assumptions / failure modes

Replay does not remove off-policy structure. In fact, replay often intensifies it in the sense that updates are performed on transitions generated under older behavior policies as well as recent ones. The method is still off-policy if the target is based on a different policy structure than the behavior that generated the data.

Replay also does not guarantee a good coverage distribution. A replay buffer may still overrepresent some regions and underrepresent others, depending on how data were collected.

A common misconception is that replay makes data “independent.” That is too strong. It reduces short-range temporal correlation and mixes samples, but the resulting samples are not magically independent in a strict probabilistic sense.

### Fully worked example

Imagine an agent currently stuck for many consecutive steps in a narrow corridor of the environment. If learning used only the most recent transition each time, then the next several updates would all be dominated by highly similar corridor transitions. The optimizer would repeatedly see nearly the same local configuration, producing gradients with strong correlation.

Now suppose the replay buffer contains transitions from many earlier phases of interaction: some from the corridor, some from open regions, some near rewards, and some near terminal failure states. A mini-batch sampled from this buffer might contain one corridor transition, two open-region transitions, one near-reward transition, and one terminal transition.

What changes mathematically? The current update is now computed from a more diverse empirical sample. The loss is no longer shaped entirely by the immediate temporal neighborhood of the current state trajectory. This can reduce oscillatory learning driven by short-run correlations and can improve sample reuse because older informative transitions are not discarded after one use.

What was checked? First, the correlated online setting was identified. Second, the replay-induced mixture of experiences was contrasted with that setting. Third, the training implication was stated: gradient updates are driven by a broader empirical distribution. The conclusion is that replay changes optimization conditions in ways that can improve stability and efficiency.

The general lesson is that in approximate RL, **how** data are presented to the optimizer matters almost as much as which target formula is used.

### Misconception or counterexample block

**Do not confuse replay with on-policy learning.**

Replay can mix experiences from many behavior policies and many time periods. It helps with sample reuse and correlation reduction. It does not make the target policy equal to the behavior policy.

### Connection to later material

Replay is one of the major design patterns inherited by many deep RL methods. Later variants modify how transitions are prioritized or sampled, but the basic idea remains: break short-range correlations and reuse costly interaction data.

### Retain / Do not confuse

Retain that replay reduces short-range temporal correlation and improves sample reuse. Do not confuse “mixed batches” with “independent data” or with “on-policy learning.”

---

## 10. The semi-gradient character of DQN updates

### Why this section exists

By now the chapter has defined the DQN target and explained the roles of target networks and replay. But one mathematical subtlety remains: when the loss is differentiated, which quantities are treated as fixed and which are differentiated through? This question matters because the target itself is built from learned value estimates. This section exists because later RL methods will rely heavily on this distinction, and DQN is a good place to learn it clearly.

### The object being introduced

The object introduced here is the **semi-gradient** nature of the DQN update. The online network prediction $Q(S_t,A_t;w)$ depends on the online parameters $w$, and that dependence is differentiated. The target

$$
Y_t^{\mathrm{DQN}} = R_{t+1} + \gamma (1-\zeta_t) \max_{a'} Q(S_{t+1},a';w^-)
$$

is treated as fixed with respect to $w$ during the current update because it depends on the frozen target parameters $w^-$, not on the current online parameters being optimized.

What is fixed is the target for the current sampled update. What varies is the online parameter vector $w$. The question this object answers is: what gradient is actually being taken when DQN minimizes its per-sample loss? The conclusion it allows is that DQN performs a regression-style gradient step toward a temporarily fixed target.

### Formal definition

A typical DQN loss on a sampled transition is

$$
\mathcal L_t(w) = \bigl(Y_t^{\mathrm{DQN}} - Q(S_t,A_t;w)\bigr)^2,
$$

with

$$
Y_t^{\mathrm{DQN}} = R_{t+1} + \gamma (1-\zeta_t) \max_{a'} Q(S_{t+1},a';w^-).
$$

During differentiation with respect to $w$, the target is treated as fixed, so

$$
\nabla_w \mathcal L_t(w)
$$

acts only through the prediction term $Q(S_t,A_t;w)$.

### Interpretation paragraph

The phrase “semi-gradient” means we are not differentiating through every pathway by which the eventual learning signal depends on learnable quantities. Instead, for the current update, we freeze the target side and take the gradient only of the online prediction. This is mathematically simpler and algorithmically more stable than trying to chase a fully moving target through all dependencies.

The first thing to notice is that this is not a trivial bookkeeping detail. In RL, one should always ask: which object is being optimized, and which parts of the update are being treated as external input for the present step? DQN’s answer is: the target is treated as given, the online prediction is differentiated.

### Implementation-failure warning: what "freeze the target" means operationally

A common project bug is to say "we use a semi-gradient loss" while still letting gradients flow through the target computation graph. The phrase "treat the target as fixed" is not metaphorical. It is an operational instruction about differentiation. During the current update, the target side is used as a numeric reference value. The gradient is taken only with respect to how the current prediction changes with the online parameters.

If code accidentally differentiates through the target path, then the implemented update is no longer the one the chapter is analyzing. That mistake matters because the conceptual point of the semi-gradient description is precisely to separate the role of the prediction path from the role of the target path during one update.

### Boundary conditions / assumptions / failure modes

Because DQN uses a frozen target network, the semi-gradient interpretation is especially clean: the target depends on $w^-$, not $w$, during the update block. In algorithms where target and prediction share parameters more directly, this distinction can become less clean or more subtle.

A common misconception is that semi-gradient means the update is approximate in a careless sense. It does involve ignoring certain possible derivative pathways, but it is also a deliberate design choice aligned with the target-network separation.

Another failure mode is to overlook that the loss being minimized is not the same as direct optimization of true control performance. It is a surrogate fitting objective built from bootstrapped targets.

### Fully worked example

Suppose for one sampled transition the DQN target is computed as

$$
Y_t^{\mathrm{DQN}} = 7.
$$

Assume the online network currently predicts

$$
Q(S_t,A_t;w)=5.
$$

Then the loss is

$$
\mathcal L_t(w) = (7-5)^2 = 4.
$$

Now ask what the gradient should respond to. Since the target value $7$ was computed from the frozen target network and sampled reward, it is treated as fixed during this update. The gradient therefore aims to move the online prediction upward toward $7$.

If, by contrast, one mistakenly imagined differentiating through a target that was itself changing with $w$, the interpretation would become much more tangled. A change in $w$ would alter both the prediction and the target simultaneously, making the optimization geometry harder to control.

What was checked? First, the target and prediction roles were separated. Second, the loss was computed numerically. Third, the differentiation pathway was identified: only the online prediction contributes derivative terms with respect to $w$. The conclusion is that DQN performs a semi-gradient fit to a temporarily fixed target.

The general lesson is that in approximate RL, the phrase “the model predicts a target” always invites a second question: is the target treated as fixed or is the gradient allowed to flow through it?

### Misconception or counterexample block

**Do not confuse the target being learned from with the quantity being differentiated through.**

The target influences the loss value. That does not mean its internal computation is differentiated with respect to the online parameters in the current DQN update.

### Connection to later material

This distinction becomes even more important in actor–critic methods and other modern algorithms where multiple networks interact. The habit of asking “what is fixed, what varies, and what is the gradient actually flowing through?” is one of the most useful habits this chapter can build.

### Retain / Do not confuse

Retain that DQN performs a semi-gradient update: differentiate the online prediction, not the frozen target. Do not confuse “appears inside the loss” with “is differentiated through.”

---

## 11. Representation is part of the RL problem

### Why this section exists

Students sometimes finish a first pass through DQN believing that architecture choice and state representation are implementation details external to the core RL problem. That is too shallow. Function approximation only works relative to the representation it receives. If the representation discards distinctions that matter for future return, no amount of clever loss design can fully repair the damage. This section exists because the chapter must end the approximation discussion at the right conceptual depth: representation is part of what makes value learning possible or impossible.

### The object being introduced

The object introduced here is the **state or observation representation** supplied to the approximator. The approximator does not observe “reality itself.” It receives a vector, tensor, feature map, or other encoded object. That representation determines what distinctions the model can express and what kinds of generalization it will impose.

What is fixed is the representation map used to encode the agent’s input. What varies are the latent situations in the environment that may or may not be distinguishable under that representation. The question this object answers is: when can an approximate value function even represent the value distinctions the task requires? The conclusion it allows is that representation quality is not secondary to RL; it is a core part of the problem definition.

### Formal definition

If the approximator receives a representation $\phi(s)$ rather than raw state $s$, then value prediction may take a form such as

$$
\widehat V(s;w) = f(\phi(s);w)
\qquad \text{or} \qquad
\widehat Q(s,a;w) = g(\phi(s),a;w).
$$

If two distinct underlying situations $s_1$ and $s_2$ satisfy

$$
\phi(s_1)=\phi(s_2),
$$

then the approximator receives them as the same input representation.

### Interpretation paragraph

If distinct latent situations are mapped to the same representation while requiring different values, the approximator is being asked to assign incompatible targets to the same input. This is often called **aliasing**. No matter how powerful the optimization procedure is, it cannot fit two different correct values to one identical input unless extra distinguishing information is provided.

The first thing to notice is that representation determines not only computational convenience but also the **space of representable value functions**. If the right distinctions are not visible in the input, the value function cannot be learned correctly in the intended sense.

### Boundary conditions / assumptions / failure modes

A representation need not be perfect to be useful. Approximate representations can still support strong performance. But severe aliasing can create irreducible prediction conflict.

A common hidden assumption is that larger networks solve representation problems automatically. They do not. Model capacity helps only relative to the information made available. If two distinct situations are encoded identically, capacity cannot separate them.

Another failure mode is to blame optimization whenever training seems unstable. Sometimes the problem is representational: the learner is trying to fit incompatible targets to indistinguishable inputs.

### Fully worked example

Suppose an environment has two latent states, $s_1$ and $s_2$. In $s_1$, taking action wait leads with high probability to a large future reward, so the correct action value is roughly

$$
Q(s_1,\text{wait}) \approx 8.
$$

In $s_2$, taking the same action leads to failure, so

$$
Q(s_2,\text{wait}) \approx -3.
$$

Now suppose the chosen representation map hides the latent distinction and sends both states to the same encoded input:

$$
\phi(s_1)=\phi(s_2)=z.
$$

Then the approximator receives identical input for both cases and must produce

$$
\widehat Q(z,\text{wait};w)
$$

for each. But one target is around $8$ and the other around $-3$. The learner is therefore being asked to fit incompatible labels to the same encoded example.

What can happen during training? If the dataset contains both situations, the approximator may settle somewhere in between, perhaps near an average value depending on training distribution and loss weighting. But that compromise is not the correct value for either latent state.

What was checked? First, two distinct latent states with distinct correct values were specified. Second, the representation collapse was made explicit. Third, the impossibility of exact fit under that representation was derived. The conclusion is that some value-learning failures are representational, not merely algorithmic.

The general lesson is that when approximate RL struggles, one should ask not only whether the update rule is correct, but whether the representation preserves the distinctions on which correct value assignment depends.

### Misconception or counterexample block

**Do not say “representation is just feature engineering.”**

Representation determines what function can in principle be learned. It is not a cosmetic preprocessing stage. It is part of the modeling assumptions of the RL system.

### Connection to later material

As RL progresses into deep networks, partial observability, recurrent models, and learned encoders, this point becomes even more important. Representation learning is not merely upstream of RL; it is intertwined with whether value learning and control can be coherent.

### Retain / Do not confuse

Retain that representation determines what distinctions the approximator can express. Do not confuse optimization failure with representational impossibility.

---

## 12. Reading DQN as a stabilized but still risky system

### Why this section exists

By this point the chapter has introduced all the main pieces: approximation, regression-style fitting, shared-parameter coupling, bootstrapping, off-policy mismatch, the deadly triad, the DQN target, target networks, replay, semi-gradients, and representation. What remains is to synthesize these ideas into a single mental model. This section exists because a student who knows the formulas but cannot tell the full story of why DQN is designed the way it is does not yet understand the chapter deeply.

### The object being introduced

The object here is not a new formula but a coherent system-level interpretation of DQN. DQN should be viewed as a method that keeps the control logic of Q-learning while adding specific devices to manage the instability created by the deadly triad.

What is fixed is the overall goal of approximate greedy control. What varies are the design choices used to make that goal trainable in practice. The conclusion this section allows is that DQN is best understood as a compromise: it preserves powerful but risky ingredients and adds mechanisms to make them more manageable.

### Formal definition

At the system level, DQN combines several roles that have to be read together rather than as an inventory. It maintains an online action-value approximator $Q(s,a;w)$, the network whose parameters are actually being updated. It also maintains a target network $Q(s,a;w^-)$, whose slower-moving parameters are used only to construct continuation targets. Training data arrive not as a fresh on-policy stream but as replayed transitions $(S_t,A_t,R_{t+1},S_{t+1},\zeta_t)$ stored from earlier behavior. For each sampled transition, the target is
$$
Y_t^{\mathrm{DQN}} = R_{t+1} + \gamma (1-\zeta_t)\max_{a'}Q(S_{t+1},a';w^-),
$$
and the online network is then fit to that target by a semi-gradient update. Written in prose, the structure becomes easier to reconstruct: replay supplies the data, the target network supplies the continuation estimate, the terminal mask enforces episodic boundary correctness, and the online network is the object actually differentiated.

### Interpretation paragraph

Read as a whole, DQN says the following. We still want a greedy one-step control target because Q-learning style control is attractive. We cannot store values in a table, so we use a shared-parameter approximator. Because shared parameters, bootstrapped targets, and off-policy data create instability risk, we slow target drift with a frozen target network and make optimization statistically easier with replayed training batches. Even then, the method is not magically safe. It is stabilized, not purified.

The first thing to notice is that each DQN component is a response to a different instability pressure, and the pressures are not interchangeable. Shared-parameter approximation is what makes large problems representable at all, but it also makes each update nonlocal. The target network slows how quickly the continuation estimate moves, so the learner is not chasing a value target that changes at the same rate as the predictor. Replay changes the statistical structure of training by reusing past transitions and weakening short-range correlation in the update stream. The terminal mask enforces the boundary condition that no further continuation value should be added after an absorbing transition. Semi-gradient fitting specifies which object is treated as fixed and which is differentiated during the update. Representation then sits underneath all of these choices: if the input collapses distinctions that matter for return, none of the stabilizers can recover information that the representation never preserved.

### Boundary conditions / assumptions / failure modes

DQN still inherits limitations. It can overestimate through the max operator. It can still struggle under poor representation, sparse coverage, or difficult optimization geometry. It is often more suited to discrete-action settings than continuous-action control without further modification.

A common failure mode in understanding is to see DQN as the final answer to approximate RL. It is historically important and conceptually central, but it is also a first major stabilized deep value-learning method, not the end of the subject.

### Fully worked example

Consider the complete life of one replayed DQN update on a nonterminal sampled transition.

1. A transition

$$
(s,a,r,s',\zeta=0)
$$

is drawn from replay.

2. The target network evaluates the next state and returns action values such as

$$
Q(s',a_1;w^-)=1.2,
\quad Q(s',a_2;w^-)=4.7,
\quad Q(s',a_3;w^-)=3.9.
$$

3. The greedy continuation estimate is the maximum, namely $4.7$.

4. With reward $r=2$ and discount $\gamma=0.9$, the target becomes

$$
Y = 2 + 0.9 \cdot 4.7 = 6.23.
$$

5. The online network currently predicts

$$
Q(s,a;w)=5.5.
$$

6. The sample loss is

$$
(6.23-5.5)^2.
$$

7. A gradient step adjusts $w$ so that the online prediction at $(s,a)$ moves toward $6.23$.

8. Because the model uses shared parameters, that same step may also alter predictions elsewhere.

9. The target network is not changed by this step, so the continuation estimate stays temporarily fixed for future updates until the target network is refreshed.

10. Because the transition came from replay, it may have been collected under an earlier exploratory policy rather than the agent’s current behavior, so the update remains off-policy.

What does each step illustrate? Steps 1 and 10 show replay and off-policy data. Steps 2 through 4 show bootstrapped target construction. Step 5 shows the online prediction being fit. Step 7 shows the semi-gradient update. Step 8 reminds us that approximation creates nonlocal parameter effects. Step 9 explains why target freezing matters. The final interpretation is that every DQN update is a small controlled encounter with the deadly triad, moderated by stabilizing design choices.

The general lesson is that DQN should be read as a system whose pieces are motivated by pressures, not as a formula bundle to memorize.

### Misconception or counterexample block

**Do not reduce DQN to “Q-learning with a neural net.”**

That phrase hides the actual conceptual work of the algorithm. The important part is not only that the value function is neural. The important part is that once approximation is introduced, target lag, replay, and update interpretation become central.

### Connection to later material

Understanding DQN at this system level prepares you for later improvements and variants. You will be able to recognize what later methods are trying to repair: overestimation bias, sample inefficiency, poor exploration, unstable targets, weak representations, and more.

### Retain / Do not confuse

Retain that DQN is a stabilized approximate control method, not merely a neural implementation of tabular Q-learning. Do not confuse having stabilizers with eliminating the deadly triad entirely.

---

## 13. Common confusions this chapter is designed to block

### Why this section exists

A chapter on approximation and DQN can leave behind persistent misunderstandings if it only states formulas. This section exists to gather the confusions most likely to sabotage later learning.

### Confusion 1: function approximation is just a storage trick

No. It changes the learning dynamics because parameters are shared across inputs. This creates both generalization and interference.

### Confusion 2: the deadly triad means modern RL is impossible

No. The triad identifies a structural instability risk. Many practical methods work by introducing stabilizing choices while retaining the useful ingredients.

### Confusion 3: a DQN target is just an observed label

No. It is partly observed reward and partly estimated future value. It is a bootstrapped target, not a ground-truth label in the ordinary supervised sense.

### Confusion 4: replay makes the method on-policy

No. Replay changes how data are sampled and reused. It does not collapse the distinction between behavior distribution and target policy structure.

### Confusion 5: the target network is only an implementation convenience

No. Its purpose is to slow target drift so the learner is not chasing a target that moves as quickly as the predictor itself.

### Confusion 6: bigger networks solve bad representations automatically

No. Capacity cannot recover distinctions that the input representation fails to expose.

### Retain / Do not confuse

Retain that most major difficulties in deep value learning come from interactions among representation, target construction, data distribution, and optimization. Do not confuse one component’s role with another’s.

---

## 14. What this chapter now entitles you to do

### Why this section exists

A strong chapter should end by clarifying what the reader is now justified in saying and using. The goal here is to mark what this material has made available for later reasoning.

### What you can now conclude

After mastering this chapter, you are entitled to do the following responsibly.

First, you can explain exactly why tabular value methods stop scaling and why approximation introduces shared-parameter coupling.

Second, you can read a value-learning loss as a regression-style fitting objective while immediately checking whether the target is fixed, bootstrapped, delayed, or self-referential.

Third, you can state the deadly triad precisely and explain why its danger lies in interaction rather than in any one ingredient by itself.

Fourth, you can parse every term of the DQN target and say what it checks: immediate reward, terminal status, greedy continuation, discounting, and target-network evaluation.

Fifth, you can explain why target networks and replay are stabilizing devices rather than optional implementation details.

Sixth, you can identify the semi-gradient character of DQN updates and explicitly state which parameters define the prediction being differentiated and which define the target being treated as fixed.

Seventh, you can explain why representation quality is part of the RL problem and not merely a preprocessing choice.

### Connection to later material

These are exactly the tools needed for later chapters on improved value-learning methods, actor–critic systems, overestimation corrections, and learned representations. Once you understand DQN in this principled way, later algorithms become intelligible modifications of known pressures rather than disconnected inventions.

### Retain / Do not confuse

Retain that this chapter is the transition from exact tabular logic to modern approximate RL. Do not confuse familiarity with DQN notation for mastery of why the algorithm has the form it does.

---

## 15. Mastery check

A serious reader should be able to answer the following questions in complete sentences, with the relevant variables and assumptions made explicit.

1. Why do tabular methods fail not only in continuous spaces, but also in large sparse discrete spaces?
2. What changes conceptually when a value function becomes parameterized instead of tabular?
3. In what sense does approximate value learning resemble regression, and in what sense is it unlike ordinary supervised learning?
4. Why can bootstrapping become more dangerous once shared parameters are present?
5. What exactly is the distribution mismatch issue in off-policy learning under approximation?
6. Why is the deadly triad an interaction claim rather than a statement about any one component alone?
7. In the DQN target, what does each term mean, and what boundary condition does the terminal mask enforce?
8. Which parameters define the prediction being updated, and which parameters define the target during a DQN step?
9. What problem does the target network address, and what does it *not* solve?
10. What statistical and optimization changes does replay introduce?
11. Why is DQN called semi-gradient in spirit?
12. How can a bad representation make correct value prediction impossible even with a powerful approximator?

If those answers are not stable, slow down here. This chapter is where reinforcement learning stops being a world of independent table entries and becomes a world of interacting learned functions. If that transition is not conceptually secure, later deep RL methods will feel like disconnected tricks rather than principled responses to real mathematical pressures.
