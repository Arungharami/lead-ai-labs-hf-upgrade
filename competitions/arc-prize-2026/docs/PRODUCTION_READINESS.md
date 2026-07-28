# Production Readiness

## Readiness status

| Control | Status | Evidence |
|---|---|---|
| Agent contract | Ready | `MyAgent`, `is_done`, and `choose_action` validated by AST preflight |
| Python syntax | Ready | compile gate in local and GitHub CI |
| Unit behavior | Ready | 26 deterministic tests |
| Coverage | Ready | 85% minimum gate; current local result approximately 90% |
| Legal actions | Ready | integer, string, dictionary, and enum normalization |
| Complex coordinates | Ready | clamped to `0..63` |
| Full reset | Ready | learned state cleared on `full_reset` |
| Death recovery | Ready | episode reset with retained global values |
| Loop recovery | Ready | state-action failures and stagnation reset |
| Path planning | Ready | four-neighbor shortest path around wall colors |
| Secret controls | Ready | ignored runtime, scan, token format and permission checks |
| Reproducible starter | Ready | exact official starter commit |
| Reproducible framework | Ready | exact official agent-framework commit |
| Critical packages | Ready | exact ARC toolkit and Kaggle CLI versions |
| Kaggle metadata | Ready | private, internet disabled, correct competition source |
| Notebook build | Ready | scheduled and pull-request runtime smoke workflow |
| Official local game run | Account/machine dependent | requires installed runtime and environment downloads |
| Kaggle notebook execution | Account dependent | requires private Kaggle token |
| Competition submission | User action required | requires accepted rules and Kaggle UI confirmation |
| Leaderboard performance | Unknown until measured | no score should be claimed before submission |

## Definition of complete

The repository is engineering-complete for a first official baseline when all
automated gates pass and the following externally authorized actions are done:

1. competition rules accepted;
2. Kaggle token installed locally;
3. `make setup` completed;
4. `make verify` completed;
5. `make play` completed;
6. `make submit` completed;
7. notebook execution reviewed;
8. `submission.parquet` manually submitted;
9. score recorded in the experiment ledger.

## Non-negotiable release gates

```bash
python3.12 -m pip install -e '.[dev]'
make ci
make setup
make notebook
make verify
```

A release must not be called successful when any command fails.

## Performance gates for future agents

A new policy must be compared against the same game set and runtime budget.
Record:

- total score;
- levels completed;
- actions per completed level;
- reset count;
- repeated-state rate;
- unchanged-frame rate;
- invalid-action count;
- exception count;
- wall-clock runtime;
- peak RAM and VRAM;
- fallback frequency.

No policy is promoted solely because of one public leaderboard result.

## Known limits

The symbolic v2 agent uses documented visual color cues and generic exploration.
It does not yet contain a learned world model, a vision-language model, or
game-specific solved programs. It is a robust, reproducible baseline rather
than a claim of state-of-the-art ARC performance.

External services can change after this release. The weekly runtime smoke
workflow is designed to detect incompatibilities with the locked build path.
