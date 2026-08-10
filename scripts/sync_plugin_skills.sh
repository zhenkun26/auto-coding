#!/usr/bin/env bash
# Syncs the canonical repo-root skill into the Codex plugin bundle
# (plugins/auto-coding/skills/auto-coding). Single source of truth is the
# repo root; run this after any change to skill content before a release.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_SKILLS="$REPO_ROOT/plugins/auto-coding/skills"
SKILL_DIR="$PLUGIN_SKILLS/auto-coding"

# Guard: only ever clean the generated plugin skills directory.
if [[ "$PLUGIN_SKILLS" != "$REPO_ROOT/plugins/auto-coding/skills" ]]; then
  echo "Refusing to clean unexpected path: $PLUGIN_SKILLS" >&2
  exit 1
fi

rm -rf "$PLUGIN_SKILLS"
mkdir -p "$SKILL_DIR"

# Entry skill: single auto-coding skill with on-demand references.
cp "$REPO_ROOT/SKILL.md" "$SKILL_DIR/SKILL.md"
# Local comparative checkouts are research inputs, not distributable skill content.
rsync -a --delete --exclude 'codex-skills/' "$REPO_ROOT/references/" "$SKILL_DIR/references/"

# Runtime scripts referenced by the skill (contract checker, state manager,
# project detection, state schema). Repo-level tooling (check_repo.py,
# sync_plugin_skills.sh) is intentionally excluded.
mkdir -p "$SKILL_DIR/scripts"
cp "$REPO_ROOT/scripts/check_python_contracts.py" "$SKILL_DIR/scripts/"
cp "$REPO_ROOT/scripts/manage_state.py" "$SKILL_DIR/scripts/"
cp "$REPO_ROOT/scripts/detect_project.py" "$SKILL_DIR/scripts/"
cp "$REPO_ROOT/scripts/state_schema.json" "$SKILL_DIR/scripts/"

echo "Plugin skills synced to $SKILL_DIR"
