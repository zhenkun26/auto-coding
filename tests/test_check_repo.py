"""Unit tests for the repository mechanical checks in ``scripts/check_repo.py``."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_repo


def write(path: Path, content: str) -> Path:
    """Write a file to a temp path, creating parents as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def write_toolchain_routes(root: Path) -> None:
    """Create the minimal routed references required by the repository checker."""
    links: list[str] = []
    for template, _manifests in check_repo.TEMPLATES:
        relative = f"references/toolchain-{template}.md"
        write(root / relative, f"# {template}\n")
        links.append(f"[{template}]({relative})")
    write(
        root / "SKILL.md",
        "---\nname: demo\nlicense: MIT\n---\n" + "\n".join(links) + "\n",
    )


def test_should_find_broken_relative_links(tmp_path: Path) -> None:
    """Given a markdown file referencing a missing file, the check reports it."""
    write(tmp_path / "docs" / "page.md", "[missing](missing-file.md)\n")

    problems = check_repo.check_relative_links(tmp_path)

    assert len(problems) == 1
    assert "missing-file.md" in problems[0]


def test_should_pass_when_all_links_resolve(tmp_path: Path) -> None:
    """Given a markdown file with valid links, no problems are reported."""
    write(tmp_path / "docs" / "page.md", "[ok](target.md)\n")
    write(tmp_path / "docs" / "target.md", "target\n")

    problems = check_repo.check_relative_links(tmp_path)

    assert problems == []


def test_should_flag_skill_without_license_or_frontmatter(tmp_path: Path) -> None:
    """Given SKILL.md files missing MIT frontmatter, they are flagged without crashing."""
    write(tmp_path / "skills" / "no-license" / "SKILL.md", "---\nname: no-license\n---\nbody\n")
    write(tmp_path / "skills" / "no-frontmatter" / "SKILL.md", "just body, no frontmatter\n")

    problems = check_repo.check_skill_licenses(tmp_path)

    assert any("no-license" in problem for problem in problems)
    assert any("no-frontmatter" in problem for problem in problems)


def test_should_honor_exact_vendor_mit_override(tmp_path: Path) -> None:
    """A user-approved comparative checkout is exempt without weakening other paths."""
    write(tmp_path / "references" / "codex-skills" / "demo" / "SKILL.md", "no frontmatter\n")
    write(tmp_path / "references" / "other-vendor" / "demo" / "SKILL.md", "no frontmatter\n")

    problems = check_repo.check_skill_licenses(tmp_path)

    assert not any("codex-skills" in problem for problem in problems)
    assert any("other-vendor" in problem for problem in problems)


def test_should_report_readme_heading_mismatch(tmp_path: Path) -> None:
    """Given READMEs with different heading structures, the check reports it."""
    write(tmp_path / "README.md", "# Title\n## One\n## Two\n")
    write(tmp_path / "README-EN.md", "# Title\n## One\n")

    problems = check_repo.check_readme_heading_structure(tmp_path)

    assert len(problems) == 1


def test_should_report_missing_detected_toolchain_route(tmp_path: Path) -> None:
    """Given an incomplete route map, the missing detected toolchain is reported."""
    write(tmp_path / "SKILL.md", "---\nname: demo\nlicense: MIT\n---\n")

    problems = check_repo.check_toolchain_routes(tmp_path)

    assert any("go" in problem for problem in problems)


def test_should_pass_when_all_detected_toolchains_are_routed(tmp_path: Path) -> None:
    """Given one reference and route per detector template, no gap is reported."""
    write_toolchain_routes(tmp_path)

    assert check_repo.check_toolchain_routes(tmp_path) == []


def test_should_not_crash_on_non_utf8_markdown(tmp_path: Path) -> None:
    """Given a non-UTF-8 markdown file, the link check warns instead of crashing."""
    write(tmp_path / "docs" / "target.md", "target\n")
    binary = tmp_path / "docs" / "binary.md"
    binary.write_bytes(b"\xff\xfe\x00bad\xff")

    problems = check_repo.check_relative_links(tmp_path)

    assert problems == []


def test_should_return_empty_string_for_unreadable_file(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Given a missing file, read_text_safely returns '' and warns on stderr."""
    content = check_repo.read_text_safely(tmp_path / "missing.md")
    captured = capsys.readouterr()

    assert content == ""
    assert "cannot read" in captured.err


def test_should_return_zero_when_repo_is_clean(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Given a clean repo layout, main exits zero."""
    write(tmp_path / "README.md", "# Title\n## One\n")
    write(tmp_path / "README-EN.md", "# Title\n## One\n")
    write_toolchain_routes(tmp_path)
    monkeypatch.setattr(check_repo, "REPO_ROOT", tmp_path)

    assert check_repo.main() == 0


def test_should_return_nonzero_when_link_is_broken(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Given a broken relative link, main exits nonzero."""
    write(tmp_path / "README.md", "# Title\n## One\n")
    write(tmp_path / "README-EN.md", "# Title\n## One\n")
    write(tmp_path / "docs" / "page.md", "[missing](gone.md)\n")
    write_toolchain_routes(tmp_path)
    monkeypatch.setattr(check_repo, "REPO_ROOT", tmp_path)

    assert check_repo.main() == 1
