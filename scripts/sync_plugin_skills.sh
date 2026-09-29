#!/usr/bin/env bash
# Compatibility entrypoint; Python implements non-deleting sync and --check.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$REPO_ROOT/scripts/sync_plugin_skills.py" "$@"
