ROOT := $(CURDIR)
STARTER := $(ROOT)/.runtime/ARC-AGI-3-Kaggle-Starter

.PHONY: bootstrap setup sync test verify play play-game notebook submit status clean

bootstrap:
	bash scripts/bootstrap_official_starter.sh

setup: bootstrap
	$(MAKE) -C $(STARTER) setup

sync:
	@test -d "$(STARTER)" || (echo "Run 'make bootstrap' first." && exit 1)
	cp agent/my_agent.py $(STARTER)/agent/my_agent.py
	cp notebooks/kernel-metadata.json $(STARTER)/notebooks/kernel-metadata.json

# Fast dependency-free tests for the reasoning core.
test:
	python -m pytest -q
	python -m py_compile agent/my_agent.py

verify: sync
	$(MAKE) -C $(STARTER) verify-local

play: sync
	$(MAKE) -C $(STARTER) play-local

play-game: sync
	@test -n "$(GAME)" || (echo "Usage: make play-game GAME=ls20" && exit 1)
	$(MAKE) -C $(STARTER) play-local GAME=$(GAME)

notebook: sync
	$(MAKE) -C $(STARTER) notebook

submit: sync
	$(MAKE) -C $(STARTER) submit

status:
	$(MAKE) -C $(STARTER) status

clean:
	rm -rf .runtime .pytest_cache __pycache__ tests/__pycache__ agent/__pycache__
