---
license: mit
library_name: custom
pipeline_tag: reinforcement-learning
tags:
- arc-agi
- arc-agi-3
- symbolic-ai
- planning
- agent
- reasoning
- kaggle
- lead-ai
---

# Lead.AI ARC-AGI-3 Symbolic Agent

`lead-ai-symbolic-v2` is a deterministic, code-based agent for ARC Prize 2026 — ARC-AGI-3. It is published as an auditable agent artifact rather than a pretrained neural-weight checkpoint.

## What is included

- self-contained `MyAgent` implementation;
- frame validation and stable state hashing;
- legal-action normalization;
- connected-component visual analysis;
- player/goal estimation;
- shortest-path planning with uncertainty-aware fallback;
- novelty/UCB exploration;
- state-specific failed-action and dead-click memory;
- stagnation and reset recovery;
- JSON-serializable reasoning metadata;
- pinned official runtime revision information.

## Intended use

- reproducible ARC-AGI-3 baseline experiments;
- candidate-action generation for hybrid symbolic/neural systems;
- failure analysis and action-trace generation;
- education and research on interactive reasoning agents.

## Not intended for

- claims of general intelligence;
- use as a pretrained neural model;
- private-game memorization or benchmark leakage;
- reporting an official score before a verified Kaggle submission;
- safety-critical or autonomous real-world decisions.

## Evaluation status

Repository quality gates include unit, contract, notebook, security, formatting, and pinned-runtime checks. Official Kaggle scores are intentionally omitted until they are produced by a verified competition submission and recorded with a Git commit and notebook version.

## Reproduction

```bash
git clone https://github.com/Arungharami/lead-ai-labs-hf-upgrade.git
cd lead-ai-labs-hf-upgrade/competitions/arc-prize-2026
python3.12 -m pip install -e '.[dev]'
make ci
make setup
make verify
```

The final Kaggle kernel uses the official ARC starter and an internet-disabled runtime.

## Files published with this card

- `my_agent.py` — competition agent source;
- `runtime-lock.env` — pinned official revisions;
- `PRODUCTION_READINESS.md` — release evidence and remaining account-dependent steps.

## Limitations

The policy uses color, component, transition, and path heuristics. Novel games may use different visual semantics, hidden state, delayed effects, or action meanings. The deterministic fallback favors reliability and auditability over broad learned world knowledge.

## Collaboration

Contributions are coordinated in the GitHub repository through issues and pull requests. See `docs/COLLABORATION.md` for team roles, experiment standards, and provenance requirements.

## Attribution

Developed by Arun Kumar Gharami / Lead.AI Labs. ARC benchmark assets and official frameworks remain the property of their respective authors and are used under their published licenses.
