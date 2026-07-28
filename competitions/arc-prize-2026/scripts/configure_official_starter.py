#!/usr/bin/env python3
"""Apply the Lead.AI reproducibility overlay to the official Kaggle starter."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "config" / "runtime-lock.env"
RUNTIME_STARTER = ROOT / ".runtime" / "ARC-AGI-3-Kaggle-Starter"
COMPETITION_SLUG = "arc-prize-2026-arc-agi-3"
KAGGLE_USERNAME = "arungharami"


def read_lock() -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in LOCK_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator or not key or not value:
            raise SystemExit(f"Invalid runtime lock line: {raw_line!r}")
        values[key.strip()] = value.strip()
    required = {
        "OFFICIAL_STARTER_COMMIT",
        "OFFICIAL_AGENTS_COMMIT",
        "ARC_AGI_VERSION",
        "KAGGLE_VERSION",
        "ACCELERATOR",
    }
    missing = sorted(required - values.keys())
    if missing:
        raise SystemExit(f"Missing runtime lock values: {', '.join(missing)}")
    return values


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise SystemExit(f"Could not patch {label}; expected one match, found {count}")
    return updated


def configure_build_script(lock: dict[str, str]) -> None:
    path = RUNTIME_STARTER / "scripts" / "build_notebook.py"
    text = path.read_text(encoding="utf-8")
    accelerator = lock["ACCELERATOR"]
    if accelerator not in {"cpu", "t4", "p100", "rtx6000"}:
        raise SystemExit(f"Unsupported accelerator: {accelerator}")
    text = replace_once(
        text,
        r'^ACCELERATOR = "[^"]+"$',
        f'ACCELERATOR = "{accelerator}"',
        "notebook accelerator",
    )
    path.write_text(text, encoding="utf-8")


def configure_runtime_dependencies(lock: dict[str, str]) -> None:
    path = RUNTIME_STARTER / "Makefile"
    text = path.read_text(encoding="utf-8")
    text = replace_once(
        text,
        r'"arc-agi(?:>=|==)[^"]+"',
        f'"arc-agi=={lock["ARC_AGI_VERSION"]}"',
        "arc-agi version",
    )
    text = replace_once(
        text,
        r'"kaggle(?:>=|==)[^"]+"',
        f'"kaggle=={lock["KAGGLE_VERSION"]}"',
        "Kaggle CLI version",
    )
    path.write_text(text, encoding="utf-8")


def synchronize_project_files(lock: dict[str, str]) -> None:
    shutil.copy2(ROOT / "agent" / "my_agent.py", RUNTIME_STARTER / "agent" / "my_agent.py")

    metadata_path = ROOT / "notebooks" / "kernel-metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    expected_id_prefix = f"{KAGGLE_USERNAME}/"
    if not str(metadata.get("id", "")).startswith(expected_id_prefix):
        raise SystemExit(f"Kaggle kernel id must start with {expected_id_prefix!r}")
    if metadata.get("competition_sources") != [COMPETITION_SLUG]:
        raise SystemExit("Kaggle metadata has the wrong competition source")
    if metadata.get("enable_internet") is not False:
        raise SystemExit("Kaggle notebook internet must remain disabled")

    expected_gpu = lock["ACCELERATOR"] != "cpu"
    if metadata.get("enable_gpu") is not expected_gpu:
        raise SystemExit(
            "Kaggle metadata enable_gpu does not match the locked accelerator"
        )
    shutil.copy2(metadata_path, RUNTIME_STARTER / "notebooks" / "kernel-metadata.json")


def main() -> None:
    if not RUNTIME_STARTER.is_dir():
        raise SystemExit(f"Official starter is missing: {RUNTIME_STARTER}")
    lock = read_lock()
    configure_build_script(lock)
    configure_runtime_dependencies(lock)
    synchronize_project_files(lock)
    print(
        "Configured official starter "
        f"(accelerator={lock['ACCELERATOR']}, "
        f"arc-agi={lock['ARC_AGI_VERSION']}, kaggle={lock['KAGGLE_VERSION']})."
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Configuration failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
