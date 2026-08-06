#!/usr/bin/env bash
# Syncs the canonical repo-root skills into the Codex plugin bundle
# (plugins/auto-coding/skills). Single source of truth is the repo root;
# run this after any change to skill content before cutting a release.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_SKILLS="$REPO_ROOT/plugins/auto-coding/skills"

# Guard: only ever clean the generated plugin skills directory.
if [[ "$PLUGIN_SKILLS" != "$REPO_ROOT/plugins/auto-coding/skills" ]]; then
  echo "Refusing to clean unexpected path: $PLUGIN_SKILLS" >&2
  exit 1
fi

rm -rf "$PLUGIN_SKILLS"
mkdir -p "$PLUGIN_SKILLS"

# Entry skill: auto-coding (top-level SKILL.md).
mkdir -p "$PLUGIN_SKILLS/auto-coding"
cp "$REPO_ROOT/SKILL.md" "$PLUGIN_SKILLS/auto-coding/SKILL.md"

# Component skills and reference resources.
rsync -a --delete "$REPO_ROOT/grill-me/" "$PLUGIN_SKILLS/grill-me/"
rsync -a --delete "$REPO_ROOT/pipeline/" "$PLUGIN_SKILLS/pipeline/"
rsync -a --delete "$REPO_ROOT/ponytail_code/" "$PLUGIN_SKILLS/ponytail/"
rsync -a --delete "$REPO_ROOT/adaptive/" "$PLUGIN_SKILLS/adaptive/"
rsync -a --delete "$REPO_ROOT/self_verify/" "$PLUGIN_SKILLS/self_verify/"

# OpenSpec skills (one directory per skill).
for skill_dir in "$REPO_ROOT"/openspec/skills/*/; do
  name="$(basename "$skill_dir")"
  rsync -a --delete "$skill_dir" "$PLUGIN_SKILLS/$name/"
done

# Reference resources (adaptive, self_verify) need SKILL.md wrappers so Codex
# skill discovery accepts every directory under skills/. The canonical content
# stays in ADAPTIVE.md / SELF_VERIFY.md; these wrappers only point to it.
cat > "$PLUGIN_SKILLS/adaptive/SKILL.md" <<'EOF'
---
name: adaptive
license: MIT
description: Toolchain adaptation rules referenced by the pipeline skill. Read ADAPTIVE.md for the verification strategy routing and non-degradable baseline.
---

# Adaptive — Toolchain adaptation reference

Reference resource bundled with auto-coding. The pipeline skill reads
`ADAPTIVE.md` in this directory to decide verification strategy, degradation
rules, and scale protection.
EOF

cat > "$PLUGIN_SKILLS/self_verify/SKILL.md" <<'EOF'
---
name: self-verify
license: MIT
description: Three-layer code self-check protocol (L0/L1/L2) referenced by the pipeline skill. Read SELF_VERIFY.md for the authoritative protocol.
---

# Self-Verify — Three-layer self-check reference

Reference resource bundled with auto-coding. The pipeline skill reads
`SELF_VERIFY.md` in this directory for the L0/L1/L2 self-check protocol.
EOF

echo "Plugin skills synced to $PLUGIN_SKILLS"
