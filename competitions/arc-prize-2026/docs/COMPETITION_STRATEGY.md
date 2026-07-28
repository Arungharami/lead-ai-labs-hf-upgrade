# ARC Prize 2026 Competition Strategy

**Owner:** Arun Kumar Gharami  
**Lab:** Lead.AI Labs  
**Primary track:** ARC Prize 2026 — ARC-AGI-3  
**Strategy date:** July 28, 2026

## Executive decision

ARC-AGI-3 is the main cash-prize target because it rewards interactive reasoning, agent memory, exploration, and efficient action selection. It also produces unusually strong portfolio evidence even when a prize is not won.

This is a high-difficulty research competition, not dependable income. The project therefore has three success levels:

1. **Minimum success:** a valid, reproducible Kaggle submission with a measurable score.
2. **Professional success:** a strong open-source agent, ablation study, technical report, and public portfolio package.
3. **Prize success:** a milestone or final leaderboard award under the official rules.

## Prize and deadline map

The official 2026 program lists an ARC-AGI-3 prize pool of **$850,000**. It includes a conditional **$700,000 grand prize**, guaranteed top-score awards totaling **$75,000**, and milestone awards totaling **$75,000**.

| Date | Deliverable | Internal objective |
|---|---|---|
| July 28–August 4 | Valid starter submission | End-to-end pipeline and first leaderboard score |
| August 5–18 | Symbolic agent v2 | Stronger perception, memory, and loop avoidance |
| August 19–September 5 | Local VLM policy | Kaggle-offline multimodal reasoning prototype |
| September 6–22 | Ablation and ensemble phase | Select best policy from controlled evidence |
| September 23–30 | Milestone #2 package | Reproducible submission, documentation, release candidate |
| October 1–25 | Final optimization | Robustness, runtime, cross-seed evaluation |
| October 26–November 2 | Final freeze | Final code submission and verification |
| November 3–8 | Paper package | Method, results, limitations, ablations, reproducibility |

Official program dates currently include **September 30, 2026** for Milestone Prize #2, **November 2, 2026** for final competition submissions, **November 8, 2026** for paper submissions, and **December 4, 2026** for results.

## Architecture roadmap

### Lane A — Generic symbolic explorer

Status: **implemented as v1**.

Purpose:

- establish a deterministic and valid baseline;
- learn which actions change a state;
- detect repetition, stagnation, and failed clicks;
- identify likely player, goal, and rare interactive objects;
- preserve legal-action safety.

Planned upgrades:

- object tracking across frames;
- collision and wall inference;
- shortest-path planning over traversable cells;
- action-sequence memory by state abstraction;
- plan repair after unexpected transitions;
- automatic per-game hypothesis summaries.

### Lane B — Vision-language policy

Purpose:

- convert the raw grid into a compact symbolic description and image;
- ask a local, competition-compatible multimodal model for a candidate action;
- maintain a structured reflection memory rather than an ever-growing transcript;
- validate every model action against the legal-action set;
- use deterministic fallback behavior for malformed or uncertain outputs.

Constraints:

- Kaggle accelerated sessions have internet disabled;
- model weights must be attached through approved Kaggle model or dataset sources;
- latency and memory use must be measured before any official submission;
- no external paid API may be assumed in the final notebook.

### Lane C — Program-synthesis and REPL agent

Purpose:

- let a compact code-capable model inspect observations;
- generate short Python analyses or plans inside a controlled local execution loop;
- use tools for connected components, path planning, visual differences, and memory retrieval;
- recover from code errors without crashing the submission.

Safety and reliability controls:

- strict execution timeout;
- no network access;
- approved imports only;
- limited output size;
- exception capture and deterministic fallback;
- full trace logging for reproducibility.

### Lane D — ARC-AGI-2 companion track

ARC-AGI-2 remains valuable for static abstract reasoning and for a research-paper contribution. Work here should reuse shared modules where possible:

- object extraction;
- transformations and symmetries;
- color and topology features;
- program search;
- candidate ranking;
- explainable solution traces.

The companion track must not delay the September 30 ARC-AGI-3 milestone.

## Experiment protocol

Every experiment receives an immutable ID such as `EXP-001` and records:

- Git commit SHA;
- agent version;
- changed hypothesis;
- local game set and random seeds;
- levels completed by game;
- action count and efficiency;
- wall-clock runtime;
- accelerator and memory consumption;
- Kaggle public score when submitted;
- failure patterns;
- decision: keep, modify, or reject.

A feature is promoted only when it improves the aggregate score or clearly fixes a documented failure without creating unacceptable regressions.

## Evaluation metrics

Primary:

- normalized environment score;
- total levels completed;
- number of environments with non-zero progress.

Secondary:

- actions per completed level;
- repeated-state rate;
- no-change action rate;
- resets per environment;
- runtime per action;
- peak RAM and VRAM;
- deterministic replay agreement;
- crash-free completion rate.

## Submission policy

Kaggle currently permits five official submissions per day for the official starter workflow. The team will not spend an official submission unless:

1. unit tests pass;
2. the official local smoke test passes;
3. the full local game run completes without an exception;
4. the generated notebook has internet disabled;
5. no credential or private data is present;
6. the experiment log is updated;
7. the expected improvement is stated before seeing the leaderboard score.

## Lessons from Milestone #1

The public milestone recap indicates that competitive approaches combined several ideas rather than relying on pure random play:

- vision-language reasoning;
- compact reflection or context management;
- legal-action guards;
- click-target heuristics;
- error repair for structured model outputs;
- code execution or a REPL for environment analysis.

The Lead.AI plan adopts these ideas as research directions while preserving an independently implemented baseline and full experiment traceability.

## Key risks and controls

| Risk | Control |
|---|---|
| Overfitting public environments | Evaluate generic abstractions, multiple seeds, and holdout-style perturbations |
| Invalid Kaggle notebook | Build through the official starter and run local verification first |
| Excessive VLM latency | Cache visual summaries, limit reflection calls, benchmark each model |
| Context growth | Store structured findings and short rolling memory |
| Repeated ineffective actions | State-action memory, dead-click tracking, stagnation recovery |
| Secret exposure | Ignore token directories; use local files or Kaggle Secrets only |
| Prize eligibility failure | Read and preserve current competition rules, licensing, and open-source requirements |
| Time lost on speculative ideas | Require an experiment hypothesis, success metric, and stop condition |

## Definition of “best”

The best project is not the largest notebook. It is the strongest reproducible system under the competition constraints:

- correct;
- measurable;
- efficient;
- robust to unknown environments;
- documented well enough for another researcher to reproduce;
- valuable as a research and professional portfolio even without prize money.
