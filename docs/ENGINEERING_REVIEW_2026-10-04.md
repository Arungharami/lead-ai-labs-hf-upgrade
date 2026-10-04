# Engineering review — October 4, 2026

## Scope

Source review of `src/lead_ai_bench/data.py`, training/model-selection/evaluation helpers, tests and project packaging. This review addresses a bounded correctness issue; it does not certify the entire application, rerun all research experiments, or establish production readiness.

## Finding and repair

Deduplication happened before excluding transaction IDs, so identical model inputs with different IDs survived and could cross split boundaries. Fractional targets were cast to integers before binary validation.

Validate binary labels before casting; deduplicate on the exact numeric feature contract after ID exclusion; reject identical features carrying conflicting labels; enforce class support after deduplication.

## Verification

`PYTHONPATH=src python -m unittest discover -s tests -p test_data_contract_regressions.py -v` — 4 tests passed using the installed pandas/numpy runtime. The complete pinned scikit-learn training workflow was not rerun locally.

All changed Python files were syntax-compiled. Package installation from this workspace is blocked, so full dependency-backed suites and production builds are not described as passed. GitHub checks on the pull request provide the remaining integration validation.

## Next implementation work

Retrain candidate artifacts through the existing quality and checksum gates before any new release. Add provenance-preserving adapters for representative authorized real data and assess calibration/drift there. Synthetic benchmark scores remain demonstration evidence.

## Evidence boundary

No raw benchmark data, measured research results, corpus approval records, model releases or production deployments were changed. Any affected scientific output must be re-executed and linked to the accepted source commit before updating manuscript claims.
