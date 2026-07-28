# ARC Prize Multi-Platform Publishing

This directory is the source of truth for publishing the Lead.AI ARC Prize 2026 project across GitHub, Hugging Face, and Kaggle.

## Publication targets

| Platform | Target | Purpose |
|---|---|---|
| GitHub | `Arungharami/lead-ai-labs-hf-upgrade` | Source code, CI, issues, experiments, and releases |
| Hugging Face model | `lead-ai-labs/arc-agi-3-symbolic-agent` | Versioned symbolic-agent code and model card |
| Hugging Face dataset | `lead-ai-labs/arc-agi-3-agent-trace-schema` | Original synthetic trace schema and sample rows |
| Hugging Face Space | `lead-ai-labs/arc-grid-inspector` | Interactive grid validation and heuristic inspection |
| Kaggle dataset | `arungharami/lead-ai-arc-agent-trace-schema` | Easy-to-find public dataset package |
| Kaggle competition kernel | `arungharami/lead-ai-arc-prize-2026-agent-v2` | Private ARC-AGI-3 competition notebook |

## Truthful publication policy

- The agent repository contains code, not pretrained neural weights.
- The trace-schema dataset contains synthetic demonstration rows only.
- No official hidden ARC game, private competition output, token, or personal data is redistributed.
- No Kaggle score is reported until an official submission is completed and logged.
- External datasets and models are linked in `docs/RESOURCE_CATALOG.md`; they are not silently copied or merged.
- Every published artifact must identify its Git commit and license.

## One-click GitHub Actions

Two manual workflows are included:

- **Publish ARC to Hugging Face** — requires repository secret `HF_TOKEN`.
- **Publish ARC to Kaggle** — requires repository secret `KAGGLE_API_TOKEN` and accepted competition rules.

Open the repository's **Actions** tab, choose the workflow, and use **Run workflow**. Secrets are never printed or committed.

## Local Hugging Face publishing

```bash
export HF_TOKEN='your_write_token'
python -m pip install -U huggingface_hub
hf auth whoami

hf repos create lead-ai-labs/arc-agi-3-symbolic-agent --type model --exist-ok
hf repos create lead-ai-labs/arc-agi-3-agent-trace-schema --type dataset --exist-ok
hf repos create lead-ai-labs/arc-grid-inspector --type space --space-sdk gradio --exist-ok
```

The GitHub workflow assembles the correct files and uploads them. Local users may follow the same staging layout documented in the workflow.

## Local Kaggle publishing

```bash
export KAGGLE_API_TOKEN='your_private_token'
python -m pip install -U 'kaggle>=2.2'

kaggle datasets create -p publish/kaggle/dataset
```

For later versions:

```bash
kaggle datasets version \
  -p publish/kaggle/dataset \
  -m 'Update ARC agent trace schema and documentation'
```

The private competition kernel is built from `agent/my_agent.py` using the pinned official starter:

```bash
make setup
make ci
make verify
make submit
make status
```

The final **Submit to Competition** action remains a deliberate manual step on Kaggle.

## Release checklist

- [ ] GitHub quality and runtime-smoke workflows pass.
- [ ] Model, dataset, and Space cards contain the current commit.
- [ ] Dataset rows are marked synthetic and schema-validated.
- [ ] No secret or generated private output appears in the diff.
- [ ] Hugging Face repositories render correctly.
- [ ] Kaggle dataset status is public and metadata is correct.
- [ ] Competition notebook completes without exceptions.
- [ ] Official scores are entered in `docs/EXPERIMENT_LOG.md` only after verification.
