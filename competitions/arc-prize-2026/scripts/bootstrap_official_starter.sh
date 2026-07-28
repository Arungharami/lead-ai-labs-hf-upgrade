#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME="$ROOT/.runtime"
STARTER="$RUNTIME/ARC-AGI-3-Kaggle-Starter"
OFFICIAL_REPO="https://github.com/arcprize/ARC-AGI-3-Kaggle-Starter.git"
LOCK_FILE="$ROOT/config/runtime-lock.env"

for command in git python3 mkdir; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Required command not found: $command" >&2
    exit 1
  fi
done

# shellcheck disable=SC1090
source "$LOCK_FILE"

if [[ ! "$OFFICIAL_STARTER_COMMIT" =~ ^[0-9a-f]{40}$ ]]; then
  echo "Invalid OFFICIAL_STARTER_COMMIT in $LOCK_FILE" >&2
  exit 1
fi

mkdir -p "$RUNTIME"

if [[ ! -d "$STARTER/.git" ]]; then
  git clone --no-checkout "$OFFICIAL_REPO" "$STARTER"
fi

git -C "$STARTER" remote set-url origin "$OFFICIAL_REPO"
git -C "$STARTER" fetch --depth 1 origin "$OFFICIAL_STARTER_COMMIT"
git -C "$STARTER" reset --hard "$OFFICIAL_STARTER_COMMIT"

python3 "$ROOT/scripts/configure_official_starter.py"

actual_commit="$(git -C "$STARTER" rev-parse HEAD)"
if [[ "$actual_commit" != "$OFFICIAL_STARTER_COMMIT" ]]; then
  echo "Starter commit mismatch: expected $OFFICIAL_STARTER_COMMIT, got $actual_commit" >&2
  exit 1
fi

echo "Official starter ready at: $STARTER"
echo "Pinned starter commit: $actual_commit"
