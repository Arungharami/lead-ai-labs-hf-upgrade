# Lead.AI ARC Prize 2026 Production Agent Lab

[![Competition](https://img.shields.io/badge/Kaggle-ARC--AGI--3-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-3)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Agent](https://img.shields.io/badge/Agent-lead--ai--symbolic--v2-7C3AED)](agent/my_agent.py)
[![Status](https://img.shields.io/badge/Status-Submission%20Ready-16A34A)](docs/PRODUCTION_READINESS.md)

A reproducible ARC Prize 2026 — ARC-AGI-3 competition workspace developed by
**Arun Kumar Gharami / Lead.AI Labs**.

The repository provides a deterministic symbolic reasoning agent, a pinned copy
of the official Kaggle starter, pinned critical runtime versions, local and
integration tests, secret checks, notebook validation, experiment governance,
and GitHub Actions quality gates.

> No software project can truthfully guarantee a perfect leaderboard result or
> zero defects in every future external environment. This project instead uses
> explicit version locks, automated tests, official-runtime smoke checks, and
> controlled release gates to make failures detectable and reproducible.

## Current release

| Item | Value |
|---|---|
| Agent | `lead-ai-symbolic-v2` |
| Kernel | `arungharami/lead-ai-arc-prize-2026-agent-v2` |
| Accelerator | CPU |
| Python | 3.12+ |
| Unit tests | 26 |
| Coverage gate | 85% minimum |
| Official starter | pinned in `config/runtime-lock.env` |
| ARC toolkit | `0.9.9` |
| Kaggle CLI | `2.2.3` |
| Internet in Kaggle | disabled |
| Official leaderboard score | pending account-authorized submission |

## What is implemented

### Agent intelligence

- strict frame normalization and malformed-grid rejection;
- collision-resistant state signatures with row-boundary encoding;
- four-connected component extraction;
- player and goal color-role estimation;
- shortest-path movement around detected wall cells;
- fallback goal-vector movement;
- rare-object and goal-component click exploration;
- legal-action normalization;
- state-specific failed-action memory;
- dead-click memory;
- online action-value updates;
- deterministic exploration by game identifier;
- full-reset, death, level-transition, and stagnation recovery;
- complex-action coordinate enforcement within the ARC `0..63` contract;
- compact JSON-serializable action reasoning.

### Engineering controls

- pinned official starter and agent-framework commits;
- pinned critical `arc-agi` and Kaggle CLI versions;
- CPU-first notebook configuration;
- private, internet-disabled Kaggle metadata;
- offline production preflight;
- source and generated-notebook secret scanning;
- unit and branch coverage gates;
- lint, formatting, compilation, and shell syntax checks;
- official-runtime notebook-build smoke workflow;
- experiment and submission registry;
- release and incident-response checklists.

## Repository structure

```text
competitions/arc-prize-2026/
├── README.md
├── SECURITY.md
├── Makefile
├── pyproject.toml
├── config/
│   └── runtime-lock.env
├── agent/
│   └── my_agent.py
├── notebooks/
│   └── kernel-metadata.json
├── scripts/
│   ├── bootstrap_official_starter.sh
│   ├── configure_official_starter.py
│   ├── pin_official_framework.sh
│   └── preflight.py
├── tests/
│   └── test_agent_core.py
└── docs/
    ├── COMPETITION_STRATEGY.md
    ├── EXPERIMENT_LOG.md
    ├── KAGGLE_RUNBOOK.md
    └── PRODUCTION_READINESS.md
```

## Quick start

Use Linux, macOS, or Windows through WSL/Git Bash with Python 3.12, Git, and
GNU Make.

```bash
cd competitions/arc-prize-2026

python3.12 -m pip install -e '.[dev]'
make ci
make setup
make notebook
```

`make setup` performs the following:

1. checks out the exact official starter commit;
2. applies the locked CPU and dependency configuration;
3. copies the Lead.AI agent and Kaggle metadata;
4. installs the official runtime;
5. pins the official agent framework;
6. runs the production preflight.

## Secure Kaggle authentication

Accept the competition rules through the Kaggle website, then save the token
only inside the ignored runtime directory:

```bash
mkdir -p .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle

printf '%s' 'YOUR_PRIVATE_KAGGLE_TOKEN' > \
  .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle/access_token

chmod 600 \
  .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle/access_token
```

Validate the credential without displaying it:

```bash
python3.12 scripts/preflight.py --require-token
```

Never paste the token into ChatGPT, source code, a notebook, an issue, an email,
or a commit.

## Local evaluation

```bash
make verify
make play-game GAME=ls20
make play
```

A zero local score is still a valid engineering baseline when the pipeline
finishes without invalid actions or crashes. Record it honestly in
`docs/EXPERIMENT_LOG.md`.

## Kaggle notebook submission

```bash
make notebook
make submit
make status
```

After the Kaggle notebook run completes:

1. open the notebook version on Kaggle;
2. inspect the execution output;
3. select **Submit to Competition**;
4. select `submission.parquet`;
5. record the experiment ID, commit SHA, notebook version, runtime, and score.

The repository cannot perform the final account-authorized Kaggle UI action or
accept competition rules on the user's behalf.

## Quality commands

| Command | Purpose |
|---|---|
| `make preflight` | Validate configuration, metadata, agent contract, secrets, and runtime sync |
| `make test` | Run 26 tests with branch-aware coverage |
| `make lint` | Run Ruff lint rules |
| `make format-check` | Verify deterministic formatting |
| `make shell-check` | Validate shell script syntax |
| `make ci` | Run all repository quality gates |
| `make bootstrap` | Restore and configure the pinned official starter |
| `make setup` | Install and pin the complete official runtime |
| `make notebook` | Build and validate the Kaggle notebook |
| `make verify` | Run the official quick game smoke test |
| `make play` | Run all locally available games |
| `make clean` | Remove generated outputs while preserving the runtime token |
| `make distclean` | Remove the entire runtime, including the local token |

## Release policy

A candidate is not promoted unless:

- `make ci` passes;
- the official runtime smoke workflow passes;
- `make verify` passes locally;
- a full game run completes without crashes;
- the experiment hypothesis was written before leaderboard feedback;
- the exact commit and notebook version are recorded;
- no secret or private data is present;
- the Kaggle submission is manually verified.

See [Production Readiness](docs/PRODUCTION_READINESS.md),
[Kaggle Runbook](docs/KAGGLE_RUNBOOK.md), and
[Experiment Log](docs/EXPERIMENT_LOG.md).

## Attribution and licensing

The runtime integration is based on the official ARC Prize starter and agent
framework. The Lead.AI code adds a symbolic policy, planning, testing,
reproducibility, security, and experiment-management layer. The benchmark,
competition, official starter, and official runtime remain the property of
their respective maintainers.
