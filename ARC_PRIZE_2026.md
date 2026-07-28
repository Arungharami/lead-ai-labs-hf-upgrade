# Lead.AI ARC Prize 2026 — Start Here

This page is the fastest route to every ARC Prize asset in the repository.

## Core project

- [Production agent lab](competitions/arc-prize-2026/README.md)
- [Symbolic agent source](competitions/arc-prize-2026/agent/my_agent.py)
- [Production readiness](competitions/arc-prize-2026/docs/PRODUCTION_READINESS.md)
- [Security policy](competitions/arc-prize-2026/SECURITY.md)
- [Experiment log](competitions/arc-prize-2026/docs/EXPERIMENT_LOG.md)

## Publish and collaborate

- [Multi-platform publishing guide](competitions/arc-prize-2026/PUBLISHING.md)
- [Current dataset and model catalog](competitions/arc-prize-2026/docs/RESOURCE_CATALOG.md)
- [Collaboration guide](competitions/arc-prize-2026/docs/COLLABORATION.md)
- [Kaggle runbook](competitions/arc-prize-2026/docs/KAGGLE_RUNBOOK.md)

## Prepared public artifacts

### Hugging Face

- symbolic-agent model card: `lead-ai-labs/arc-agi-3-symbolic-agent`;
- trace-schema dataset: `lead-ai-labs/arc-agi-3-agent-trace-schema`;
- interactive Space: `lead-ai-labs/arc-grid-inspector`.

Source packages are under `competitions/arc-prize-2026/publish/huggingface/`.

### Kaggle

- public trace-schema dataset: `arungharami/lead-ai-arc-agent-trace-schema`;
- private competition kernel: `arungharami/lead-ai-arc-prize-2026-agent-v2`.

Source packages are under `competitions/arc-prize-2026/publish/kaggle/` and `competitions/arc-prize-2026/notebooks/`.

## Automated workflows

- `ARC Prize 2026 Quality Gates`
- `ARC Prize 2026 Runtime Smoke`
- `ARC Multi-Platform Publication Checks`
- `Publish ARC to Hugging Face`
- `Publish ARC to Kaggle`

Publishing workflows use protected GitHub environments and repository secrets. No token belongs in source code or chat.

## Current truth

- GitHub source and hardening are published.
- Public Hugging Face and Kaggle packages are prepared and validated.
- External platforms update automatically after the required repository secrets are available.
- An official leaderboard score remains pending an account-authorized Kaggle run and the final manual **Submit to Competition** action.
