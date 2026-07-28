ROOT := $(CURDIR)
PYTHON ?= python3.12
STARTER := $(ROOT)/.runtime/ARC-AGI-3-Kaggle-Starter

.PHONY: help bootstrap configure preflight setup sync test lint format-check \
	shell-check ci verify play play-game notebook submit status clean distclean

help:
	@echo "Lead.AI ARC Prize 2026 commands"
	@echo "  make bootstrap    Pin and configure the official starter"
	@echo "  make setup        Build the pinned local ARC runtime"
	@echo "  make ci           Run all repository quality gates"
	@echo "  make verify       Run the official two-game smoke test"
	@echo "  make play         Run every locally available game"
	@echo "  make submit       Push a private Kaggle notebook version"
	@echo "  make status       Check the latest Kaggle notebook run"

bootstrap:
	bash scripts/bootstrap_official_starter.sh

configure:
	$(PYTHON) scripts/configure_official_starter.py

preflight:
	$(PYTHON) scripts/preflight.py

setup: bootstrap
	@if [ -d "$(STARTER)/vendor/ARC-AGI-3-Agents/.git" ]; then \
		git -C "$(STARTER)/vendor/ARC-AGI-3-Agents" reset --hard; \
	fi
	$(MAKE) -C $(STARTER) setup
	bash scripts/pin_official_framework.sh
	$(PYTHON) scripts/preflight.py

sync: bootstrap
	$(PYTHON) scripts/preflight.py

test:
	$(PYTHON) -m pytest -q --cov=agent --cov-branch --cov-report=term-missing \
		--cov-fail-under=85

lint:
	$(PYTHON) -m ruff check agent tests scripts

format-check:
	$(PYTHON) -m ruff format --check agent tests scripts

shell-check:
	bash -n scripts/bootstrap_official_starter.sh
	bash -n scripts/pin_official_framework.sh

ci: test lint format-check shell-check preflight

verify: sync
	@test -x "$(STARTER)/.venv/bin/python" || \
		(echo "Runtime is not installed. Run 'make setup' first." && exit 1)
	$(MAKE) -C $(STARTER) verify-local

play: sync
	@test -x "$(STARTER)/.venv/bin/python" || \
		(echo "Runtime is not installed. Run 'make setup' first." && exit 1)
	$(MAKE) -C $(STARTER) play-local

play-game: sync
	@test -n "$(GAME)" || (echo "Usage: make play-game GAME=ls20" && exit 1)
	@test -x "$(STARTER)/.venv/bin/python" || \
		(echo "Runtime is not installed. Run 'make setup' first." && exit 1)
	$(MAKE) -C $(STARTER) play-local GAME=$(GAME)

notebook: sync
	@test -x "$(STARTER)/.venv/bin/python" || \
		(echo "Runtime is not installed. Run 'make setup' first." && exit 1)
	$(MAKE) -C $(STARTER) notebook
	$(PYTHON) -m json.tool $(STARTER)/notebooks/submission.ipynb >/dev/null

submit: sync
	$(PYTHON) scripts/preflight.py --require-token
	@test -x "$(STARTER)/.venv/bin/kaggle" || \
		(echo "Runtime is not installed. Run 'make setup' first." && exit 1)
	$(MAKE) -C $(STARTER) submit

status:
	$(PYTHON) scripts/preflight.py --require-token
	@test -x "$(STARTER)/.venv/bin/kaggle" || \
		(echo "Runtime is not installed. Run 'make setup' first." && exit 1)
	$(MAKE) -C $(STARTER) status

clean:
	@if [ -f "$(STARTER)/Makefile" ]; then $(MAKE) -C $(STARTER) clean; fi
	rm -rf .pytest_cache .coverage htmlcov __pycache__ tests/__pycache__ \
		agent/__pycache__ scripts/__pycache__

distclean: clean
	@echo "Removing .runtime, including any local Kaggle token."
	rm -rf .runtime
