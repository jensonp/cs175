# CS175 Research Project Scaffold

This repository is now structured as a theory-forward research codebase for a CS175 project on confidence-aware, learning-augmented online scheduling for cloud-style workloads.

## What This Repo Contains

- `src/scheduler/`: core package for workloads, policies, simulation, metrics, corruption, docs build, and CLI entrypoints
- `tests/`: unit, invariant, regression, and smoke-oriented tests
- `experiments/`: runnable experiment entrypoints and config placeholders
- `docs/`: static GitHub Pages site scaffold
- `.github/`: CI, Pages deploy, release automation, templates, and ownership rules
- `scripts/`: local helper scripts for docs builds and smoke runs

## Quick Start

Preferred with `uv`:

```bash
uv sync --dev
uv run ruff check .
uv run pytest
uv run python -m scheduler.cli smoke --seed 0
uv run python -m scheduler.docs build --output site
```

Fallback without `uv`:

```bash
python3 -m pip install -e . pytest ruff
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m scheduler.cli smoke --seed 0
PYTHONPATH=src python3 -m scheduler.docs build --output site
```

## Development Workflow

- Create short-lived branches such as `feat/<issue>-name` or `infra/<issue>-name`
- Land one coherent issue per PR
- Require one reviewer and passing CI before merging to `main`
- Commit at meaningful checkpoints: scaffold, logic, tests, docs/results updates
- Tag course milestones as releases:
  - `v0.1-proposal`
  - `v0.2-progress`
  - `v0.3-presentation`
  - `v1.0-final`

## Core Commands

```bash
make lint
make test
make smoke
make docs
```

If `make` is unavailable, the same commands are wired through the Python modules above.

## GitHub Settings Still Required

Some settings cannot be enforced from the repository alone. After pushing this scaffold to GitHub, enable:

- branch protection on `main`
- required checks: `lint`, `tests`, `smoke`, `docs-build`
- squash merge only
- GitHub Pages from Actions

## Legacy Course Materials

The earlier lecture-reconstruction materials are still preserved:

- `markdown/lecture02/reinforcement-learning-comprehensive.md`
- `output/lecture02/reinforcement-learning-comprehensive.html`
- `reinforcement-learning-comprehensive.pdf`
- `markdown/rl-resources/reinforcement-learning-resources-expanded.md`
- `output/rl-resources/reinforcement-learning-resources-expanded.html`
- `reinforcement-learning-resources-expanded.pdf`

These remain useful background references for the reinforcement-learning and planning portions of the course.
