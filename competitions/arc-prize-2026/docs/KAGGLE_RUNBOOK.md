# Kaggle Execution Runbook

This runbook converts the repository agent into a valid ARC Prize 2026 Kaggle notebook using the official starter project.

## 1. One-time requirements

- Python 3.12
- Git
- Make
- Kaggle account
- ARC Prize 2026 rules accepted on Kaggle
- Kaggle API token generated from Kaggle Settings

Verify tools:

```bash
python3.12 --version
git --version
make --version
```

## 2. Enter the project

```bash
cd competitions/arc-prize-2026
```

## 3. Bootstrap the official starter

```bash
make bootstrap
```

This clones the official repository into:

```text
.runtime/ARC-AGI-3-Kaggle-Starter
```

The runtime directory is ignored by Git. The bootstrap also copies the Lead.AI agent and Arun's Kaggle notebook metadata into the starter.

## 4. Add the Kaggle token securely

```bash
mkdir -p .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle
printf '%s' 'KGAT_REPLACE_WITH_YOUR_TOKEN' > \
  .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle/access_token
chmod 600 .runtime/ARC-AGI-3-Kaggle-Starter/.kaggle/access_token
```

Never paste the token into source code, a notebook cell, an issue, or a commit.

## 5. Install the official environment

```bash
make setup
```

The official starter creates its Python 3.12 environment, installs the ARC packages and Kaggle CLI, and prepares the agent framework.

## 6. Run repository tests

```bash
python3.12 -m pip install -e '.[dev]'
make test
```

Expected result for the current baseline:

```text
7 passed
```

## 7. Run official ARC verification

Fast smoke test:

```bash
make verify
```

Full local run:

```bash
make play
```

Single-game debugging:

```bash
make play-game GAME=ls20
```

Do not proceed to an official submission if the agent crashes, creates invalid actions, or fails the official smoke test.

## 8. Build the generated notebook locally

```bash
make notebook
```

Inspect the generated notebook under the official runtime. Confirm:

- the notebook imports successfully;
- `MyAgent` is present;
- the Kaggle username is `arungharami`;
- the competition source is `arc-prize-2026-arc-agi-3`;
- internet is disabled;
- no token appears in notebook source or output;
- the intended accelerator is selected.

## 9. Push a Kaggle notebook run

```bash
make submit
make status
```

`make submit` uploads and runs the generated notebook. It does not complete the final competition submission by itself.

## 10. Complete the deliberate Kaggle submission step

After `make status` reports completion:

1. Open the generated notebook version on Kaggle.
2. Review the run output for exceptions or timeouts.
3. Select **Submit to Competition**.
4. Choose the generated `submission.parquet` output.
5. Record the notebook version, experiment ID, timestamp, and score in `docs/EXPERIMENT_LOG.md`.

The official starter documentation states that five official competition submissions are available per day. Treat each one as an experiment, not a guess.

## 11. Accelerator policy

Start with the default T4 setting only after the CPU-compatible baseline is valid. Use larger accelerators only when a measured model requires them.

| Accelerator | Intended use |
|---|---|
| CPU | symbolic policies and pipeline validation |
| T4 | small local models and normal iteration |
| P100 | single-GPU memory needs |
| RTX 6000 | heavy ARC-AGI-3 model experiments after profiling |

All accelerated Kaggle sessions are expected to run without internet. Attach required open model weights through supported Kaggle sources and preserve license information.

## 12. Failure recovery

### Python 3.12 not found

Install Python 3.12 and rerun `make setup`.

### Kaggle 401 or unauthorized error

Generate a fresh Kaggle API token, replace the local ignored token file, and rerun. Do not commit the token.

### Metadata error

Verify `notebooks/kernel-metadata.json` contains:

```text
arungharami/lead-ai-arc-prize-2026-agent-v1
```

Then rerun `make submit`.

### Local environment cannot download a game initially

Confirm internet access for the first local setup. After environment assets are cached, local play can continue offline.

### Local score is zero

A valid zero score means the pipeline is working but the policy has not solved a level. Record the result as a baseline; do not misrepresent it as success.

### Submission times out or runs out of memory

Reduce model size, context, visual history, reflection frequency, or accelerator requirements. Record peak memory and latency before resubmitting.

## 13. Release checklist

Before the September milestone or November final submission:

- [ ] Current competition rules re-read and accepted.
- [ ] Best commit tagged.
- [ ] Tests and official local verification pass.
- [ ] Full game run recorded.
- [ ] Experiment table complete.
- [ ] Model and dataset licenses documented.
- [ ] Reproduction commands tested from a clean clone.
- [ ] Secrets audit complete.
- [ ] Open-source package and technical report prepared.
- [ ] Kaggle submission manually confirmed.
