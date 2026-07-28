# ARC Prize Collaboration Guide

The project welcomes focused collaboration through GitHub, Kaggle, and Hugging Face. The objective is reproducible progress, not a large uncoordinated team.

## Recommended four-person team

| Role | Responsibilities | Primary outputs |
|---|---|---|
| Runtime and submission engineer | Official starter compatibility, notebook packaging, memory/time limits, CI | Valid Kaggle kernels and failure-free reruns |
| Symbolic perception and planning engineer | Object tracking, traversability, shortest paths, action semantics | Tested deterministic policy improvements |
| Model and data engineer | Dataset adapters, offline VLM/world-model experiments, licensing | Reproducible model packages and ablations |
| Experiment and research lead | Hypotheses, scorecards, error taxonomy, paper/writeup | Experiment ledger, report, and milestone submission |

Arun Kumar Gharami is the repository owner and integration lead.

## How to contribute

1. Open a GitHub issue describing one falsifiable hypothesis.
2. State the target game set, expected improvement, runtime budget, and failure risks.
3. Work from a feature branch; do not commit tokens, downloaded model weights, or private Kaggle outputs.
4. Add tests and an experiment-log entry with the change.
5. Open a pull request against `main` and include local validation results.

## Good first collaboration tasks

- Build a component tracker that follows objects across frame transitions.
- Learn action semantics from observed displacement rather than fixed action names.
- Create a traversability estimator with uncertainty.
- Add per-game recordings and a failure-taxonomy report.
- Write an adapter for one licensed Hugging Face trajectory dataset.
- Benchmark one small offline model against the same symbolic baseline.
- Improve the grid-inspector Space with trace playback.

## Kaggle team workflow

- Accept the ARC Prize 2026 rules individually.
- Agree on team ownership and prize allocation before merging Kaggle teams.
- Use a private Kaggle team only for official submissions.
- Keep code review and experiment history in GitHub.
- Record every Kaggle notebook version and score in `docs/EXPERIMENT_LOG.md`.
- Never share a Kaggle token; each member uses their own credential.

## Hugging Face collaboration

The preferred organization namespace is `lead-ai-labs`.

Suggested repositories:

- model: `lead-ai-labs/arc-agi-3-symbolic-agent`;
- dataset: `lead-ai-labs/arc-agi-3-agent-trace-schema`;
- Space: `lead-ai-labs/arc-grid-inspector`.

Collaborators may contribute through Hub discussions or pull requests after the repositories are published. Model and dataset revisions used in experiments must be pinned.

## Contribution proposal template

```markdown
### Problem
What measurable failure are you addressing?

### Hypothesis
What specific change should improve which metric?

### Scope
Which files, games, and model/data dependencies are involved?

### Evaluation
What baseline, seeds, runtime, and acceptance criteria will be used?

### Risks
Could this overfit public games, leak data, exceed Kaggle resources, or introduce licensing issues?
```

## Communication cadence

- GitHub issues: design and task ownership.
- Pull requests: implementation review.
- Kaggle discussion/team chat: competition-specific coordination.
- Hugging Face discussions: model, dataset, and Space feedback.
- Weekly summary: best score, failures, experiments promoted/rejected, and next three priorities.

## Collaboration standards

- Evidence over claims.
- One behavioral change per experiment whenever possible.
- No leaderboard score without a commit and notebook version.
- No external dataset without a provenance record.
- No model recommendation without resource profiling.
- No private competition artifacts published publicly.
