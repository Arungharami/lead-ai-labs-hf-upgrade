# Kaggle Execution Runbook

This runbook converts `lead-ai-symbolic-v2` into a private ARC Prize 2026 Kaggle notebook through the pinned official starter.

## Requirements

- Python 3.12
- Git and GNU Make
- Kaggle account
- ARC Prize 2026 competition rules accepted
- private Kaggle API token

```bash
python3.12 --version
git --version
make --version
```

## Enter the project

```bash
cd competitions/arc-prize-2026
python3.12 -m pip install -e '.[dev]'
```

## Repository quality gates

```bash
make ci
```

The current release requires 26 tests, at least 85% branch-aware coverage, lint, formatting, compilation, shell syntax, metadata, agent-contract, and secret checks.

## Build the pinned official runtime

```bash
make setup
```

This checks out the official starter and agent framework revisions recorded in `config/runtime-lock.env`, installs the locked ARC and Kaggle packages, synchronizes the Lead.AI agent and metadata, and runs preflight checks.

Runtime location:

```text
.runtime/ARC-AGI-3-Kaggle-Starter
```

## Store the Kaggle token securely

Use your real token only in the ignored runtime file. The placeholder below intentionally does not resemble a real token.

```bash
mkdir -p .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle
printf '%s' 'YOUR_PRIVATE_KAGGLE_TOKEN' > \
  .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle/access_token
chmod 600 .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle/access_token
```

Validate without displaying it:

```bash
python3.12 scripts/preflight.py --require-token
```

Never place a token in source code, notebook cells, issues, email, chat, or commits.

## Official local verification

Quick smoke test:

```bash
make verify
```

Single-game debugging:

```bash
make play-game GAME=ls20
```

Full public-game run:

```bash
make play
```

Do not submit if the agent crashes, creates invalid actions, hangs, or fails the official smoke test. A zero score with a clean run is a valid baseline and must be recorded honestly.

## Build the private notebook

```bash
make notebook
```

Confirm that the generated notebook:

- contains `MyAgent`;
- produces `submission.parquet`;
- uses kernel ID `arungharami/lead-ai-arc-prize-2026-agent-v2`;
- attaches the ARC competition source;
- is private;
- disables internet;
- uses the locked accelerator;
- contains no credential.

## Push a Kaggle notebook version

```bash
make submit
make status
```

`make submit` pushes a private kernel version. It does not spend an official competition submission by itself.

## Complete the final Kaggle UI step

After the run reports completion:

1. Open the private notebook version on Kaggle.
2. Review output for exceptions, timeouts, memory errors, and early termination.
3. Select **Submit to Competition**.
4. Choose `submission.parquet`.
5. Record experiment ID, Git commit, notebook version, runtime, accelerator, and score in `docs/EXPERIMENT_LOG.md`.

## GitHub Actions option

The `Publish ARC to Kaggle` workflow can publish the public synthetic trace-schema dataset automatically when repository secret `KAGGLE_API_TOKEN` is configured.

A manual workflow run with `publish_competition_kernel=true` can also build and push the private kernel. The final **Submit to Competition** action remains manual.

## Accelerator policy

| Accelerator | Use |
|---|---|
| CPU | symbolic agent, validation, and default release |
| T4 | measured small-model experiments |
| P100 | measured single-GPU memory requirement |
| RTX 6000 | profiled heavy experiments only |

Do not request GPU merely because it is available. The competition host has reported many failed submissions caused by a GPU-dependent notebook being submitted without matching hardware configuration.

## Common failures

### Authentication failure

Regenerate the Kaggle token, replace only the ignored runtime file, enforce mode `600`, and rerun preflight.

### Competition permission failure

Open Kaggle and accept the current competition rules with the same account used by the token.

### Missing dependency or dataset

Return to the pinned starter, rerun `make setup`, and confirm the official competition source is attached.

### Timeout or apparent early completion

Inspect loops, reset behavior, async calls, action limits, and gateway configuration. Do not infer success from a short runtime.

### CUDA out of memory

Reduce model size, token budget, visual history, parallelism, or accelerator demand. Record peak memory before trying another submission.

### Read-only path error

Write generated files only under `/kaggle/working` or `/tmp`, never `/kaggle/input`.

## Release checklist

- [ ] Current rules accepted.
- [ ] `make ci` passes.
- [ ] Runtime-smoke workflow passes.
- [ ] `make verify` passes.
- [ ] Full public-game run is recorded.
- [ ] Best commit and notebook version are pinned.
- [ ] Dataset/model licenses and revisions are recorded.
- [ ] Secret scan passes.
- [ ] Kaggle run output is reviewed.
- [ ] Final competition submission is manually confirmed.
