# Experiments

This directory is reserved for experiment entrypoints, configs, and milestone-specific runs.

Use the smoke command for a minimal end-to-end validation:

```bash
python3 -m scheduler.cli smoke --seed 0
```

Later experiments can store configs here while writing run outputs to `artifacts/runs/<run_id>/`.
