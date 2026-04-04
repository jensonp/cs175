# Reinforcement Learning Foundations - Rewritten Chapter Set

This package is a reconstructed, chapterized rewrite of the source document:

**Source:** `reinforcement-learning-comprehensive.md`

## What is in this package

- `01_audit.md` - audit of the original document
- `02_problem-setup-and-agent-environment-interaction.md`
- `03_mathematical-preliminaries.md`
- `04_states-histories-mdps-and-objective.md`
- `05_value-functions-bellman-equations-and-policy-improvement.md`
- `06_dynamic-programming-monte-carlo-td-sarsa-qlearning.md`
- `07_function-approximation-deadly-triad-and-dqn.md`
- `08_policy-gradients-reinforce-baselines-actor-critic-ppo-sac.md`
- `09_reward-design-representation-evaluation-and-roadmap.md`

## Editorial goals

This rewrite enforces five rules throughout.

1. Every symbol is defined before it is used.
2. Every derivation states what is being conditioned on and why.
3. Every index change states the old and new index limits.
4. Every formula states the assumptions under which it is valid.
5. Optional intuition is separated from the formal argument.

## Recommended reading order

Read Chapters 2 through 5 in order before jumping to Chapters 6 through 8.
Chapter 9 is partly conceptual and can be read after Chapter 5 if needed.

## Conventions used throughout

- Time is discrete: \(t \in \{0,1,2,\ldots\}\).
- The action chosen at time \(t\) is \(A_t\).
- The reward caused by that action is observed **after** the action and is written \(R_{t+1}\).
- When a formula is written as a sum over states or actions, the chapter is assuming finite spaces.
- In continuing tasks, discounted-return results assume \(0 \le \gamma < 1\).
- In finite-horizon episodic tasks, \(\gamma = 1\) may be allowed if the horizon is finite and rewards are bounded.

## What changed relative to the source

The source already had serious mathematical intent and broad topic coverage.
This rewrite mainly improves:

- chapter boundaries
- dependency order
- symbol hygiene
- explanation of what each derivation proves
- explicit handling of assumptions, boundary cases, and common confusions
- separation of formal material from optional intuition
