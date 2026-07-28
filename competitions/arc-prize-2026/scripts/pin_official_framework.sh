#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STARTER="$ROOT/.runtime/ARC-AGI-3-Kaggle-Starter"
FRAMEWORK="$STARTER/vendor/ARC-AGI-3-Agents"
LOCK_FILE="$ROOT/config/runtime-lock.env"

for command in git; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Required command not found: $command" >&2
    exit 1
  fi
done

# shellcheck disable=SC1090
source "$LOCK_FILE"

if [[ ! -d "$FRAMEWORK/.git" ]]; then
  echo "Official agent framework is missing. Run 'make setup' first." >&2
  exit 1
fi

git -C "$FRAMEWORK" fetch --depth 1 origin "$OFFICIAL_AGENTS_COMMIT"
git -C "$FRAMEWORK" reset --hard "$OFFICIAL_AGENTS_COMMIT"
"$STARTER/.venv/bin/python" "$STARTER/scripts/slim_framework.py"

actual_commit="$(git -C "$FRAMEWORK" rev-parse HEAD)"
if [[ "$actual_commit" != "$OFFICIAL_AGENTS_COMMIT" ]]; then
  echo "Agent framework commit mismatch." >&2
  exit 1
fi

echo "Pinned ARC agent framework: $actual_commit"
