# Lead.AI ARC Agent Trace Schema

A small, original schema package for logging and validating ARC-AGI-3 agent transitions.

## Data provenance

Every included row is synthetic and marked `is_synthetic=true`. The package does not redistribute official ARC games, private competition traces, human data, or unverified leaderboard results.

## Use cases

- develop trace parsers and dashboards;
- standardize symbolic and neural agent experiments;
- test playback and failure-analysis tools;
- document adapters for separately licensed trajectory datasets;
- support collaboration around a shared row-level format.

## Not suitable for

- training a competitive model by itself;
- estimating ARC-AGI-3 benchmark performance;
- replacing official Kaggle competition data;
- claiming level completions or scores.

## Core fields

`game_id`, `episode_id`, `step`, `state_hash`, `available_actions`, `chosen_action`, optional coordinates, `levels_completed`, `changed_cells`, diagnostic `reward`, policy version, outcome, source, and notes.

## Source project

The schema, symbolic agent, CI, publishing workflows, and collaboration guide are maintained in:

`Arungharami/lead-ai-labs-hf-upgrade/competitions/arc-prize-2026`

## License

CC BY 4.0 for the original synthetic rows and documentation. External ARC assets are not included.
