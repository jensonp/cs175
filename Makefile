PYTHON ?= python3
PYTHONPATH ?= src

.PHONY: lint test smoke docs format

lint:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ruff check .
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ruff format --check .

format:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m ruff format .

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m pytest

smoke:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m scheduler.cli smoke --seed 0

docs:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m scheduler.docs build --output site
