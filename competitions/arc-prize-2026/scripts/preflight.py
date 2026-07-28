#!/usr/bin/env python3
"""Offline production checks for the ARC Prize workspace."""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".runtime" / "ARC-AGI-3-Kaggle-Starter"
LOCK_PATH = ROOT / "config" / "runtime-lock.env"
METADATA_PATH = ROOT / "notebooks" / "kernel-metadata.json"
AGENT_PATH = ROOT / "agent" / "my_agent.py"
TOKEN_PATH = RUNTIME / ".kaggle" / "access_token"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TOKEN_RE = re.compile(r"KGAT_[A-Za-z0-9_-]{20,}")
ALLOWED_AGENT_IMPORTS = {
    "__future__",
    "collections",
    "hashlib",
    "math",
    "random",
    "typing",
    "arcengine",
    "agents",
}


def read_lock() -> dict[str, str]:
    lock: dict[str, str] = {}
    for raw_line in LOCK_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator:
            raise AssertionError(f"Invalid lock line: {raw_line!r}")
        lock[key.strip()] = value.strip()
    return lock


def check_python() -> None:
    assert sys.version_info >= (3, 12), "Python 3.12 or newer is required"


def check_lock(lock: dict[str, str]) -> None:
    required = {
        "OFFICIAL_STARTER_COMMIT",
        "OFFICIAL_AGENTS_COMMIT",
        "ARC_AGI_VERSION",
        "KAGGLE_VERSION",
        "ACCELERATOR",
    }
    assert required <= lock.keys(), f"Missing lock keys: {sorted(required - lock.keys())}"
    assert SHA_RE.fullmatch(lock["OFFICIAL_STARTER_COMMIT"])
    assert SHA_RE.fullmatch(lock["OFFICIAL_AGENTS_COMMIT"])
    assert lock["ACCELERATOR"] in {"cpu", "t4", "p100", "rtx6000"}
    assert re.fullmatch(r"\d+\.\d+\.\d+", lock["ARC_AGI_VERSION"])
    assert re.fullmatch(r"\d+\.\d+\.\d+", lock["KAGGLE_VERSION"])


def check_metadata(lock: dict[str, str]) -> None:
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    assert metadata["id"].startswith("arungharami/")
    assert metadata["code_file"] == "submission.ipynb"
    assert metadata["language"] == "python"
    assert metadata["kernel_type"] == "notebook"
    assert metadata["is_private"] is True
    assert metadata["enable_internet"] is False
    assert metadata["enable_tpu"] is False
    assert metadata["competition_sources"] == ["arc-prize-2026-arc-agi-3"]
    assert metadata["enable_gpu"] == (lock["ACCELERATOR"] != "cpu")


def check_agent_contract() -> None:
    source = AGENT_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(AGENT_PATH))
    imports: set[str] = set()
    my_agent: ast.ClassDef | None = None

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])
        elif isinstance(node, ast.ClassDef) and node.name == "MyAgent":
            my_agent = node

    unexpected = sorted(imports - ALLOWED_AGENT_IMPORTS)
    assert not unexpected, f"Unexpected agent imports: {unexpected}"
    assert my_agent is not None, "MyAgent class is missing"
    methods = {
        node.name
        for node in my_agent.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    assert {"is_done", "choose_action"} <= methods
    compile(source, str(AGENT_PATH), "exec")


def check_no_secrets() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".runtime" in path.parts or ".git" in path.parts:
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".zip", ".ipynb"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        match = TOKEN_RE.search(text)
        assert match is None, f"Possible Kaggle token found in {path}"


def git_head(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        text=True,
    ).strip()


def check_runtime(lock: dict[str, str]) -> None:
    if not RUNTIME.exists():
        return
    assert (RUNTIME / ".git").is_dir()
    assert git_head(RUNTIME) == lock["OFFICIAL_STARTER_COMMIT"]
    assert (RUNTIME / "agent" / "my_agent.py").read_bytes() == AGENT_PATH.read_bytes()
    runtime_metadata = json.loads(
        (RUNTIME / "notebooks" / "kernel-metadata.json").read_text(encoding="utf-8")
    )
    project_metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    assert runtime_metadata == project_metadata

    framework = RUNTIME / "vendor" / "ARC-AGI-3-Agents"
    if framework.exists():
        assert git_head(framework) == lock["OFFICIAL_AGENTS_COMMIT"]


def check_token(require_token: bool) -> None:
    if not TOKEN_PATH.exists():
        assert not require_token, f"Kaggle token is required at {TOKEN_PATH}"
        return
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()
    assert TOKEN_RE.fullmatch(token), "Kaggle token format is invalid"
    if os.name != "nt":
        mode = stat.S_IMODE(TOKEN_PATH.stat().st_mode)
        assert mode & 0o077 == 0, "Kaggle token permissions must be 600 or stricter"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-token", action="store_true")
    args = parser.parse_args()

    lock = read_lock()
    checks = [
        ("Python", check_python),
        ("Runtime lock", lambda: check_lock(lock)),
        ("Kaggle metadata", lambda: check_metadata(lock)),
        ("Agent contract", check_agent_contract),
        ("Secret scan", check_no_secrets),
        ("Runtime synchronization", lambda: check_runtime(lock)),
        ("Kaggle credential", lambda: check_token(args.require_token)),
    ]

    failures: list[str] = []
    for name, check in checks:
        try:
            check()
        except (AssertionError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
            failures.append(f"{name}: {exc}")
            print(f"[FAIL] {name}: {exc}")
        else:
            print(f"[PASS] {name}")

    if failures:
        raise SystemExit(1)
    print("Production preflight passed.")


if __name__ == "__main__":
    main()
