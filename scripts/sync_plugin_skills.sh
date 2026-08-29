#!/usr/bin/env bash
# Syncs the canonical repo-root skills into the two distribution bundles:
#   1. Codex plugin bundle (plugins/auto-coding/skills/) — auto-coding +
#      verify-evidence + setup-auto-coding.
#   2. skills.sh / `npx skills add zhenkun26/auto-coding` channel (skills/) —
#      all four skills as self-contained, individually pickable directories.
# Single source of truth is the repo root; run this after any change to skill
# content before a release.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_SKILLS="$REPO_ROOT/plugins/auto-coding/skills"
SKILL_DIR="$PLUGIN_SKILLS/auto-coding"
NPM_SKILLS="$REPO_ROOT/skills"

# Guard: only ever clean the generated bundle directories.
if [[ "$PLUGIN_SKILLS" != "$REPO_ROOT/plugins/auto-coding/skills" || "$NPM_SKILLS" != "$REPO_ROOT/skills" ]]; then
  echo "Refusing to clean unexpected path: $PLUGIN_SKILLS / $NPM_SKILLS" >&2
  exit 1
fi

rm -rf "$PLUGIN_SKILLS" "$NPM_SKILLS"
mkdir -p "$SKILL_DIR"

# --- Codex plugin bundle -------------------------------------------------
# Entry skill: single auto-coding skill with on-demand references.
cp "$REPO_ROOT/SKILL.md" "$SKILL_DIR/SKILL.md"
# Local comparative checkouts are research inputs, not distributable skill content.
rsync -a --delete --exclude 'codex-skills/' "$REPO_ROOT/references/" "$SKILL_DIR/references/"

# Standalone companion skills shipped with the plugin. The OpenSpec companion
# (auto-coding-openspec/) is intentionally excluded here: it is installed
# separately, only by repositories that already use OpenSpec.
cp -R "$REPO_ROOT/verify-evidence" "$PLUGIN_SKILLS/verify-evidence"
cp -R "$REPO_ROOT/setup-auto-coding" "$PLUGIN_SKILLS/setup-auto-coding"

# Runtime scripts referenced by the skill (contract checker, state manager,
# project detection, state schema). Repo-level tooling (check_repo.py,
# sync_plugin_skills.sh) is intentionally excluded.
mkdir -p "$SKILL_DIR/scripts"
cp "$REPO_ROOT/scripts/check_python_contracts.py" "$SKILL_DIR/scripts/"
cp "$REPO_ROOT/scripts/manage_state.py" "$SKILL_DIR/scripts/"
cp "$REPO_ROOT/scripts/detect_project.py" "$SKILL_DIR/scripts/"
cp "$REPO_ROOT/scripts/state_schema.json" "$SKILL_DIR/scripts/"

# --- skills.sh channel ---------------------------------------------------
# Every skill becomes a self-contained directory; the installer lets the user
# pick which ones to install and on which agents.
copy_npm_skill() {
  local name="$1"
  mkdir -p "$NPM_SKILLS/$name"
  if [[ -f "$REPO_ROOT/$name/SKILL.md" ]]; then
    cp -R "$REPO_ROOT/$name/." "$NPM_SKILLS/$name/"
  else
    # The root skill: SKILL.md plus references and runtime scripts.
    cp "$REPO_ROOT/SKILL.md" "$NPM_SKILLS/$name/SKILL.md"
    rsync -a --exclude 'codex-skills/' "$REPO_ROOT/references/" "$NPM_SKILLS/$name/references/"
    mkdir -p "$NPM_SKILLS/$name/scripts"
    cp "$REPO_ROOT/scripts/check_python_contracts.py" \
       "$REPO_ROOT/scripts/manage_state.py" \
       "$REPO_ROOT/scripts/detect_project.py" \
       "$REPO_ROOT/scripts/state_schema.json" \
       "$NPM_SKILLS/$name/scripts/"
  fi
}

copy_npm_skill auto-coding
copy_npm_skill verify-evidence
copy_npm_skill setup-auto-coding
copy_npm_skill auto-coding-openspec

echo "Plugin bundle synced to $PLUGIN_SKILLS; skills.sh bundle synced to $NPM_SKILLS"
