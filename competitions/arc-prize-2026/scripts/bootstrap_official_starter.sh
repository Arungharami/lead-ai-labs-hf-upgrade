#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME="$ROOT/.runtime"
STARTER="$RUNTIME/ARC-AGI-3-Kaggle-Starter"
OFFICIAL_REPO="https://github.com/arcprize/ARC-AGI-3-Kaggle-Starter.git"

for command in git cp mkdir; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Required command not found: $command" >&2
    exit 1
  fi
done

mkdir -p "$RUNTIME"

if [[ ! -d "$STARTER/.git" ]]; then
  git clone --depth 1 "$OFFICIAL_REPO" "$STARTER"
else
  git -C "$STARTER" pull --ff-only
fi

cp "$ROOT/agent/my_agent.py" "$STARTER/agent/my_agent.py"
cp "$ROOT/notebooks/kernel-metadata.json" "$STARTER/notebooks/kernel-metadata.json"

echo "Official starter ready at: $STARTER"
echo "Lead.AI agent and Kaggle metadata are synchronized."
