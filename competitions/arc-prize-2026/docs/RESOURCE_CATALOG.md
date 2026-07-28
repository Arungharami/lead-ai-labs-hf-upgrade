# ARC-AGI Resource Catalog

Last reviewed: 2026-07-27 (America/Los_Angeles)

This catalog separates official competition assets, community datasets, and candidate models. Verify each repository's license, provenance, and format before use.

## Tier 1 — official competition assets

### Kaggle ARC Prize 2026 — ARC-AGI-3

Use this first for submission compatibility and local public-game validation.

- Competition data includes the official agent framework, Python wheels, and public environment files.
- Frames use integer grids up to 64×64 and values 0–15.
- Games expose a subset of `RESET`, `ACTION1`–`ACTION7`; `ACTION6` requires `(x, y)`.
- The competition evaluates on private games, so public-game memorization is not a valid general solution.
- License displayed by Kaggle: Apache 2.0.

### Official GitHub projects

- `arcprize/ARC-AGI-3-Kaggle-Starter` — canonical local-to-Kaggle packaging workflow.
- `arcprize/ARC-AGI-3-Agents` — agent interface, orchestration, recording, and templates.
- `arcprize/ARC-AGI` — toolkit and wrappers.
- `arcprize/ARCEngine` — frame, action, and game-state definitions.

The repository pins critical official revisions in `config/runtime-lock.env` to prevent silent drift.

## Tier 2 — useful Hugging Face datasets

These are discovery candidates, not automatically trusted training sources.

| Dataset | Best use | Caution |
|---|---|---|
| `arc-agi-community/arc-agi-2` | Static ARC-AGI-2 baseline and evaluation research | Static tasks differ from interactive ARC-AGI-3 |
| `Ardea/arc_agi_v2` | Convenient tabular/HF representation of ARC-AGI-2 | Confirm transformation fidelity and split policy |
| `fredericowieser/arc-agi-3-wm-traces` | Large-scale world-model or transition research | Inspect license, generation method, leakage, and game coverage |
| `magic-sword/arc_agi_3_public_demo_human_testing` | Human/public demonstration analysis | Do not treat public demonstrations as private-test evidence |
| `AgentNativeResearchLab/arc-agi3-*-agent-trajectories` | Per-game trajectory and failure-analysis studies | Many repositories are game-specific and may encourage overfitting |

Recommended workflow:

1. Download one dataset into an isolated adapter directory.
2. Record repository ID, revision, license, row count, game IDs, and generator.
3. Convert into the project trace schema without changing the original.
4. Deduplicate by `(game_id, frame_hash, action, next_frame_hash)`.
5. Keep public-game metrics separate from official Kaggle metrics.

## Tier 3 — candidate models

### ARC-specific repositories

| Model | Potential use | Caution |
|---|---|---|
| `star-ga/naestro-agi3-27b` | Image/text ARC-AGI-3 policy research | Large model; profile Kaggle compatibility and license first |
| `zedgamer/cogniarc-nano-nn` | Lightweight ARC-related experiments | Validate task fit; text classification is not a complete interactive agent |
| `mindware/arc-codet5-660m` | Static ARC program/code generation experiments | Designed for static ARC-style tasks, not direct ARC-AGI-3 control |
| `mindware/arc-codet5-small` | Low-cost static baseline | Same domain mismatch; useful only as an ablation or component |

### General model classes worth benchmarking

- Small vision-language models for frame interpretation.
- Compact text reasoners fed a symbolic grid representation.
- World models trained on public transition traces.
- Hybrid systems where the symbolic agent proposes legal actions and a model ranks them.

Do not select a model only because it is popular. Require:

- a compatible license;
- offline Kaggle execution;
- bounded RAM/VRAM and latency;
- structured action output;
- a deterministic legal-action fallback;
- ablation evidence against `lead-ai-symbolic-v2`.

## Lead.AI original publishable assets

The repository prepares three original artifacts:

1. `lead-ai-labs/arc-agi-3-symbolic-agent` — deterministic symbolic agent code.
2. `lead-ai-labs/arc-agi-3-agent-trace-schema` — synthetic schema examples for experiment logging.
3. `lead-ai-labs/arc-grid-inspector` — interactive grid validator and heuristic inspector.

These assets are intentionally small, auditable, and easy for collaborators to reuse.

## Selection matrix

| Need | Start with |
|---|---|
| Valid Kaggle submission | Official Kaggle starter and this repository's pinned runtime |
| Static ARC pretraining | `arc-agi-community/arc-agi-2` or `Ardea/arc_agi_v2` |
| Interactive transition research | `fredericowieser/arc-agi-3-wm-traces` after audit |
| Per-game failure analysis | AgentNativeResearchLab trajectory repositories |
| Low-cost baseline | `lead-ai-symbolic-v2` |
| Neural candidate ranking | Small licensed offline VLM plus symbolic fallback |
| Public collaboration demo | Lead.AI grid-inspector Space |

## Provenance checklist

Before adding any external artifact to an experiment:

- [ ] Repository ID and immutable revision recorded.
- [ ] License permits intended use and redistribution.
- [ ] Dataset generator and source games documented.
- [ ] Public/private benchmark leakage risk assessed.
- [ ] Schema adapter tested.
- [ ] Train/validation/test separation documented.
- [ ] Model memory, latency, and accelerator measured.
- [ ] Results compared against the same game set and seeds.
