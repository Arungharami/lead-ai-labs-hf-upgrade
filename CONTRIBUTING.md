# Contributing

Useful contributions to **lead-ai-labs-hf-upgrade** include:

- Reproduce the controlled benchmark with the documented seed and split.
- Review a deterministic benchmark case and its expected outcome.
- Check artifact schema or checksum validation without publishing a release.

## Reporting a problem

Check existing issues first. Include the source commit or branch, environment, minimal steps, expected behavior, actual behavior, and a redacted error. State whether you used real data, an educational fixture, or exported results. Keep credentials and personal records out of public reports.

## Proposing a change

Choose one bounded task. Describe the intended behavior and how it will be checked before a large implementation. Use a focused branch and draft pull request; link any existing issue. Record exactly which checks ran, including failures and unavailable checks. Do not report a full suite as passed after running only a subset.

## Relevant local checks

These are focused checks, not a replacement for the full project workflow in the README.

```bash
pytest
```

## Project evidence and boundaries

Preserve synthetic-data labeling, the untouched test partition, validation-only threshold selection, and release checksums. Publishing model or dataset assets is separate from contributing code.

[Project overview and setup](README.md) · [Issues](https://github.com/Arungharami/lead-ai-labs-hf-upgrade/issues) · [Author's portfolio](https://arungharami.info)
