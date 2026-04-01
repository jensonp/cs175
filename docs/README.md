# Docs Site Scaffold

This directory is the static source for GitHub Pages.

Build the actual deployable site with:

```bash
PYTHONPATH=src python3 -m scheduler.docs build --output site
python3 -m http.server --directory site 8000
```

Generated experiment outputs should be written under `artifacts/site/latest/`. The docs builder copies them into `site/generated/latest/` during site assembly.
