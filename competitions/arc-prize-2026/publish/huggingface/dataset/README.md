---
license: cc-by-4.0
task_categories:
- reinforcement-learning
- other
language:
- en
pretty_name: Lead.AI ARC-AGI-3 Agent Trace Schema
size_categories:
- n<1K
tags:
- arc-agi
- arc-agi-3
- agent-trajectories
- synthetic
- reasoning
- evaluation
- lead-ai
---

# Lead.AI ARC-AGI-3 Agent Trace Schema

This dataset defines a compact, auditable schema for recording ARC-AGI-3 agent transitions and experiment metadata.

## Important provenance statement

The included rows are **synthetic demonstrations** created to validate the schema and publishing workflow. They are not official competition games, private evaluation data, human demonstrations, or claims of achieved performance.

No official ARC environment file is redistributed in this package.

## Intended use

- validate trace-processing code;
- teach collaborators the expected experiment format;
- build dashboards and playback tools;
- test data adapters before importing a separately licensed trajectory dataset;
- standardize failure analysis across symbolic and neural agents.

## Columns

| Column | Description |
|---|---|
| `trace_id` | Unique synthetic trace identifier |
| `game_id` | Demonstration game label; synthetic rows use `demo-*` |
| `episode_id` | Episode identifier |
| `step` | Zero-based action step |
| `state_hash` | Stable anonymized state signature |
| `available_actions` | Pipe-separated legal action names |
| `chosen_action` | Selected action |
| `x`, `y` | Optional coordinate for complex actions |
| `levels_completed` | Levels completed at the observation |
| `changed_cells` | Number of changed grid cells after the action |
| `reward` | Experiment-local diagnostic reward |
| `policy` | Agent policy/version |
| `outcome` | Transition label such as `changed`, `no_change`, or `level_gain` |
| `source` | Provenance category |
| `is_synthetic` | Always `true` for the published sample |
| `notes` | Human-readable explanation |

## Loading

```python
from datasets import load_dataset

ds = load_dataset("lead-ai-labs/arc-agi-3-agent-trace-schema")
print(ds["train"].features)
```

## Using external traces

External ARC trajectory repositories must not be silently mixed into this dataset. Create a documented adapter that records:

- source repository and immutable revision;
- license;
- generator/model;
- included game IDs;
- frame encoding;
- action encoding;
- deduplication method;
- train/validation/test policy;
- known leakage or public-game overfitting risks.

## Limitations

The sample is intentionally tiny and synthetic. It cannot train or evaluate a competitive ARC agent. It exists to make collaboration, logging, and tooling consistent.

## Repository

Source, schema governance, and publishing workflows are maintained at:

`Arungharami/lead-ai-labs-hf-upgrade/competitions/arc-prize-2026`
