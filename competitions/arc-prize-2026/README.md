# Lead.AI ARC Prize 2026 Agent Lab

[![Competition](https://img.shields.io/badge/Kaggle-ARC--AGI--3-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3)
[![Track](https://img.shields.io/badge/Track-Interactive%20Reasoning-7C3AED)](https://arcprize.org/competitions/2026/arc-agi-3)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Baseline%20Engineering-orange)](#current-status)

A professional, reproducible competition project for **ARC Prize 2026 — ARC-AGI-3**, developed under the Lead.AI Labs portfolio by **Arun Kumar Gharami**.

The project is designed to produce a valid Kaggle submission quickly, then improve it through controlled experiments in perception, memory, exploration, planning, and optional local vision-language-model inference.

> Prize money is possible but not guaranteed. This repository is an engineering and research effort intended to maximize submission quality, reproducibility, and portfolio value.

## Competition target

ARC-AGI-3 evaluates agents in novel interactive environments without natural-language instructions. An agent must inspect changing 64×64 grid observations, infer goals and mechanics, select legal actions, remember discoveries, and complete levels efficiently.

Primary deadlines:

- **September 30, 2026:** Milestone Prize #2
- **November 2, 2026:** Final competition submissions
- **November 8, 2026:** Paper submissions
- **December 4, 2026:** Results announced

## Current status

This first implementation contains:

- a Kaggle-compatible `MyAgent` class;
- deterministic state hashing and reproducible action selection;
- player and target detection for movement-style environments;
- connected-component analysis for click-target discovery;
- novelty-based exploration and loop avoidance;
- online action-value updates from observed screen changes;
- legal-action filtering and robust fallbacks;
- reset and stagnation recovery;
- structured reasoning metadata for every action;
- unit tests for the dependency-free reasoning core;
- an official-starter bootstrap and submission workflow;
- an experiment log and milestone roadmap.

## Repository structure

```text
competitions/arc-prize-2026/
├── README.md
├── Makefile
├── pyproject.toml
├── .gitignore
├── agent/
│   └── my_agent.py
├── notebooks/
│   └── kernel-metadata.json
├── scripts/
│   └── bootstrap_official_starter.sh
├── tests/
│   └── test_agent_core.py
└── docs/
    ├── COMPETITION_STRATEGY.md
    ├── EXPERIMENT_LOG.md
    └── KAGGLE_RUNBOOK.md
```

## Quick start

Requirements: Python 3.12, Git, Make, a Kaggle account, accepted competition rules, and a Kaggle API token.

```bash
cd competitions/arc-prize-2026

# Clone and configure the official ARC Kaggle starter.
make bootstrap

# Put the Kaggle token in the runtime starter, never in Git.
mkdir -p .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle
printf '%s' 'KGAT_your_token_here' > \
  .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle/access_token
chmod 600 .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle/access_token

# Install the official environment.
make setup

# Run local games and smoke tests.
make verify
make play

# Build and push a Kaggle notebook run.
make submit
make status
```

When the Kaggle notebook run is complete, open it on Kaggle and deliberately select **Submit to Competition** using its generated `submission.parquet` output.

## Agent architecture

```text
Observation
   │
   ├── Grid normalization and hashing
   ├── Frame-difference measurement
   ├── Connected-component extraction
   ├── Player/goal estimation
   │
   ▼
Episodic Memory
   ├── Seen-state counts
   ├── Action statistics
   ├── Failed-action memory
   ├── Level-transition tracking
   │
   ▼
Policy
   ├── Goal-directed movement when confidence is high
   ├── Rare-object click exploration when applicable
   ├── Novelty/UCB exploration otherwise
   └── Stagnation recovery and reset
   │
   ▼
GameAction + auditable reasoning metadata
```

## Development principles

1. **Valid submission before sophistication.** Preserve compatibility with the official starter and Kaggle runtime.
2. **Measure every change.** Every feature must have an experiment ID, local score, Kaggle score, runtime, and conclusion.
3. **Avoid public-game overfitting.** Prefer generic perception and memory mechanisms over one-game scripts.
4. **Keep secrets out of Git.** Kaggle and model tokens belong only in ignored local files or Kaggle Secrets.
5. **Open-source readiness.** Prize eligibility requires a reproducible solution and clear documentation.
6. **Use submission quota carefully.** Run local verification before spending one of the daily official submissions.

## Next research upgrades

- action-plan queue with automatic invalid-plan repair;
- dead-click signatures and object-level interaction memory;
- compact reflection memory every 8–12 actions;
- multi-view rendering: raw grid, symbolic map, and cropped regions;
- offline VLM policy using a Kaggle-compatible open model;
- candidate-action generation plus a lightweight arbiter;
- cross-seed evaluation and bootstrap confidence intervals;
- ARC-AGI-2 static-reasoning companion track and paper submission.

## Attribution

The runtime workflow is intentionally built around the official `arcprize/ARC-AGI-3-Kaggle-Starter` and ARC-AGI toolkit. This project adds a Lead.AI research policy, testing, documentation, and experiment-management layer; it does not claim ownership of the ARC benchmark or official starter framework.
