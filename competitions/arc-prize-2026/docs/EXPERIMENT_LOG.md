# ARC Prize 2026 Experiment Log

Use one row per meaningful agent change. Record the hypothesis **before** submitting to Kaggle.

## Status vocabulary

- `PLANNED` — hypothesis defined, not yet run
- `LOCAL` — tested only in the official local environment
- `SUBMITTED` — official Kaggle submission created
- `PROMOTED` — accepted into the current best agent
- `REJECTED` — failed to improve or introduced unacceptable regressions

## Experiment ledger

| ID | Date | Commit | Agent | Hypothesis | Local result | Kaggle score | Runtime | Status | Decision |
|---|---|---|---|---|---|---|---|---|---|
| EXP-000 | 2026-07-28 | feature branch | Official random baseline | Confirm the full local-to-Kaggle pipeline | Pending official runtime | — | — | PLANNED | Establish baseline |
| EXP-001 | 2026-07-28 | feature branch | `lead-ai-novelty-v1` | Deterministic novelty, visual roles, and failed-action memory should outperform uniform random play | Core tests: 7/7 passed; official game run pending | — | Core only: <1 s | LOCAL | Run official smoke test |
| EXP-002 | TBD | TBD | Object-tracking v2 | Tracking component motion will improve player localization and reduce ineffective moves | — | — | — | PLANNED | — |
| EXP-003 | TBD | TBD | Grid planner v1 | A traversability map and shortest-path planner will improve movement environments | — | — | — | PLANNED | — |
| EXP-004 | TBD | TBD | Reflection memory v1 | Compact structured findings every 10 actions will reduce loops | — | — | — | PLANNED | — |
| EXP-005 | TBD | TBD | Local VLM policy v1 | A small offline multimodal model can choose better candidate actions than the symbolic policy alone | — | — | — | PLANNED | — |
| EXP-006 | TBD | TBD | Hybrid arbiter v1 | Selecting between symbolic and VLM candidates using confidence will improve robustness | — | — | — | PLANNED | — |

## Per-experiment template

Copy this section for each experiment that reaches local evaluation.

```markdown
### EXP-XXX — Descriptive title

- Date:
- Researcher:
- Git commit:
- Parent experiment:
- Agent version:
- Hardware:
- Game set:
- Seeds:

#### Hypothesis

State one falsifiable expected improvement.

#### Change

Describe only what changed from the parent.

#### Success criteria

- Aggregate score:
- Environments improved:
- Maximum tolerated regressions:
- Runtime budget:

#### Results

| Game | Seed | Levels | Score | Actions | Resets | Runtime | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| | | | | | | | |

#### Failure analysis

List loops, invalid actions, dead clicks, crashes, timeouts, and incorrect inferred rules.

#### Decision

`PROMOTE`, `MODIFY`, or `REJECT`, with one paragraph of evidence.
```

## Kaggle submission registry

| Submission date/time | Experiment | Notebook version | Public score | Private/final score | Notes |
|---|---|---|---:|---:|---|
| — | — | — | — | — | No official submission recorded yet |

## Reproducibility checklist

Before marking an experiment `SUBMITTED`:

- [ ] Git commit is pushed.
- [ ] `python -m pytest -q` passes.
- [ ] `make verify` passes.
- [ ] `make play` completes.
- [ ] Agent name/version changed when behavior changed materially.
- [ ] Kaggle notebook metadata is correct.
- [ ] Internet is disabled in the notebook.
- [ ] No tokens, credentials, private data, or local absolute paths are present.
- [ ] Runtime and accelerator are recorded.
- [ ] Hypothesis and expected outcome were written before leaderboard feedback.
