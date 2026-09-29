"""Behavioral tests for non-deleting, preflighted distribution updates."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from sync_plugin_skills import RUNTIME_FILES, synchronize


def canonical(root: Path) -> Path:
    files = ["SKILL.md", "references/recovery.md", "references/codex-skills/private.md",
             "verify-evidence/SKILL.md", "setup-auto-coding/SKILL.md", "auto-coding-openspec/SKILL.md"]
    files.extend(f"scripts/{name}" for name in RUNTIME_FILES)
    for name in files:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"source: {name}\n")
    return root


def test_sync_fills_both_channels_and_check_is_read_only(tmp_path: Path) -> None:
    root = canonical(tmp_path)
    assert synchronize(root, check=True)
    assert not (root / "skills").exists()
    assert synchronize(root) == []
    assert synchronize(root, check=True) == []
    assert (root / "skills/auto-coding-openspec/SKILL.md").exists()
    assert not (root / "plugins/auto-coding/skills/auto-coding-openspec").exists()
    assert not (root / "skills/auto-coding/references/codex-skills").exists()
    target = root / "skills/auto-coding/SKILL.md"
    before = target.read_bytes()
    (root / "SKILL.md").write_text("updated\n")
    assert synchronize(root, check=True)
    assert target.read_bytes() == before
    assert synchronize(root) == []
    assert target.read_bytes() == (root / "SKILL.md").read_bytes()


def test_unexpected_content_blocks_all_writes_and_is_preserved(tmp_path: Path) -> None:
    root = canonical(tmp_path)
    assert synchronize(root) == []
    target = root / "plugins/auto-coding/skills/auto-coding/SKILL.md"
    before = target.read_bytes()
    (root / "SKILL.md").write_text("new content\n")
    extra = root / "skills/.local-note"
    extra.write_text("user content\n")
    problems = synchronize(root)
    assert any("unexpected destination" in problem for problem in problems)
    assert target.read_bytes() == before
    assert extra.read_text() == "user content\n"


def test_destination_symlink_cannot_write_outside_bundle(tmp_path: Path) -> None:
    root = canonical(tmp_path / "repo")
    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "skills").symlink_to(outside, target_is_directory=True)
    assert synchronize(root)
    assert list(outside.iterdir()) == []
    assert not (root / "plugins").exists()


def test_nested_symlink_and_directory_file_collision_are_rejected(tmp_path: Path) -> None:
    root = canonical(tmp_path)
    bundle = root / "skills/auto-coding"
    bundle.mkdir(parents=True)
    (bundle / "SKILL.md").mkdir()
    assert synchronize(root)
    assert not (root / "plugins").exists()
    other_root = canonical(tmp_path / "other")
    (other_root / "references/linked.md").symlink_to(other_root / "SKILL.md")
    assert synchronize(other_root)
    assert not (other_root / "skills").exists()
