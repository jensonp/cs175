# CS175 Lesson Rewrite Pack — Mastery-Focused Edition

This repository is organized so GitHub renders each chapter folder automatically.
The mastery-focused rewrite currently covers Chapters 2 through 9, and the original audit is preserved as a separate reference chapter.

## Chapter map

- [01_audit/](01_audit/) - audit of the original document and what needed improvement
- [02_problem-setup-and-agent-environment-interaction/](02_problem-setup-and-agent-environment-interaction/) - start here
- [03_mathematical-preliminaries/](03_mathematical-preliminaries/)
- [04_states-histories-mdps-and-objective/](04_states-histories-mdps-and-objective/)
- [05_value-functions-bellman-equations-and-policy-improvement/](05_value-functions-bellman-equations-and-policy-improvement/)
- [06_dynamic-programming-monte-carlo-td-sarsa-qlearning/](06_dynamic-programming-monte-carlo-td-sarsa-qlearning/)
- [07_function-approximation-deadly-triad-and-dqn/](07_function-approximation-deadly-triad-and-dqn/)
- [08_policy-gradients-reinforce-baselines-actor-critic-ppo-sac/](08_policy-gradients-reinforce-baselines-actor-critic-ppo-sac/)
- [09_reward-design-representation-evaluation-and-roadmap/](09_reward-design-representation-evaluation-and-roadmap/)

## What changed

The original sequence already had a strong mathematical spine. These rewrites preserve that seriousness, but slow down the points where learners usually lose the thread:

- every major object is defined before it is used,
- each derivation says what is being conditioned on,
- each recursive step says what random quantity is being split on,
- assumptions and boundary conditions are attached to the formulas that need them,
- exact identities are separated from sampled estimators,
- common confusion points are called out at the moment they first matter,
- each chapter ends with a mastery check that tests whether the key distinctions are actually stable.

## Reading order

Read the chapters in order. The dependency chain matters.

1. [02_problem-setup-and-agent-environment-interaction/](02_problem-setup-and-agent-environment-interaction/)
2. [03_mathematical-preliminaries/](03_mathematical-preliminaries/)
3. [04_states-histories-mdps-and-objective/](04_states-histories-mdps-and-objective/)
4. [05_value-functions-bellman-equations-and-policy-improvement/](05_value-functions-bellman-equations-and-policy-improvement/)
5. [06_dynamic-programming-monte-carlo-td-sarsa-qlearning/](06_dynamic-programming-monte-carlo-td-sarsa-qlearning/)
6. [07_function-approximation-deadly-triad-and-dqn/](07_function-approximation-deadly-triad-and-dqn/)
7. [08_policy-gradients-reinforce-baselines-actor-critic-ppo-sac/](08_policy-gradients-reinforce-baselines-actor-critic-ppo-sac/)
8. [09_reward-design-representation-evaluation-and-roadmap/](09_reward-design-representation-evaluation-and-roadmap/)

Read [01_audit/](01_audit/) separately if you want the critique of the original source and the rationale for the rewrite.

## Conventions used throughout

- Time is discrete, with index $t \in \{0,1,2,\ldots\}$.
- The action chosen at time $t$ is $A_t$.
- The reward caused by that action is observed after the transition and is written $R_{t+1}$.
- A value function is always an expectation of return under stated conditioning.
- Sums over states or actions assume finite or countable spaces unless the text explicitly switches to integrals.
- For continuing discounted tasks, the default assumption is $0 \le \gamma < 1$ and bounded rewards.
- For finite-horizon episodic tasks, some formulas may allow $\gamma = 1$ if the horizon is finite and rewards are bounded.

## File contents

Each chapter is still a single `README.md` inside its folder so it renders cleanly on GitHub.
