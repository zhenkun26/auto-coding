"""Unit tests for the read-only project detector ``scripts/detect_project.py``."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import detect_project


def write(path: Path, content: str = "") -> Path:
    """Write a file to a temp path, creating parents as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_should_detect_python_template(tmp_path: Path) -> None:
    """Given pyproject.toml and src/, the python template is detected."""
    write(tmp_path / "pyproject.toml", "[tool.mypy]\n")

    assert detect_project.detect_templates(tmp_path) == ["python"]


def test_should_detect_typescript_template(tmp_path: Path) -> None:
    """Given package.json and tsconfig.json, the typescript template is detected."""
    write(tmp_path / "package.json", "{}")
    write(tmp_path / "tsconfig.json", "{}")

    assert detect_project.detect_templates(tmp_path) == ["typescript"]


def test_should_report_greenfield_without_sources(tmp_path: Path) -> None:
    """Given an empty src/ directory, the codebase state is greenfield."""
    (tmp_path / "src").mkdir()

    state = detect_project.detect_codebase_state(tmp_path)

    assert state["state"] == "greenfield"
    assert state["source_files"] == 0


def test_should_report_brownfield_with_sources(tmp_path: Path) -> None:
    """Given source files under src/, the codebase state is brownfield."""
    write(tmp_path / "src" / "services" / "auth.py", "x = 1\n")
    write(tmp_path / "src" / "app.py", "y = 2\n")

    state = detect_project.detect_codebase_state(tmp_path)

    assert state["state"] == "brownfield"
    assert state["source_files"] == 2


def test_should_detect_openspec_and_ci(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Given openspec and CI markers, main reports them in the JSON output."""
    write(tmp_path / "openspec" / "config.yaml", "schema: spec-driven\n")
    write(tmp_path / ".github" / "workflows" / "ci.yml", "name: CI\n")
    write(tmp_path / "pyproject.toml", "[tool.ruff]\n")

    exit_code = detect_project.main([str(tmp_path)])

    assert exit_code == 0
    report = json.loads(capsys.readouterr().out)
    assert report["openspec"] is True
    assert report["ci"] == [".github/workflows"]
    assert report["configs"]["ruff"] is True
    assert report["configs"]["mypy"] is False


def test_should_fail_cleanly_on_missing_directory(capsys: pytest.CaptureFixture) -> None:
    """Given a nonexistent root, main exits 2 with an error message."""
    exit_code = detect_project.main(["/nonexistent-path-for-auto-coding-test"])

    assert exit_code == 2
    assert "not a directory" in capsys.readouterr().err


def test_should_report_all_source_roots_when_multiple_exist(tmp_path: Path) -> None:
    """Given src/ and cmd/ side by side, both roots are reported."""
    write(tmp_path / "src" / "app.py", "x = 1\n")
    write(tmp_path / "src" / "lib.py", "y = 2\n")
    write(tmp_path / "cmd" / "main.go", "package main\n")

    state = detect_project.detect_codebase_state(tmp_path)

    assert state["source_roots"] == ["src", "cmd"]
    assert state["source_root"] == "src"  # most source files wins
    assert state["source_files"] == 3
    assert state["state"] == "brownfield"


def test_should_not_treat_empty_tests_dir_as_pytest_configured(tmp_path: Path) -> None:
    """Given an empty tests/ directory, pytest is not reported as configured."""
    (tmp_path / "tests").mkdir()

    assert detect_project.detect_configs(tmp_path)["pytest"] is False


def test_should_treat_tests_dir_with_test_files_as_pytest_configured(tmp_path: Path) -> None:
    """Given tests/ containing test modules, pytest is reported as configured."""
    write(tmp_path / "tests" / "test_app.py", "def test_ok(): pass\n")

    assert detect_project.detect_configs(tmp_path)["pytest"] is True


def test_should_detect_pytest_declared_in_pyproject_dependencies(tmp_path: Path) -> None:
    """Given pytest in pyproject dependencies, it is reported as configured."""
    write(
        tmp_path / "pyproject.toml",
        '[project]\ndependencies = ["pytest>=8"]\n',
    )

    assert detect_project.detect_configs(tmp_path)["pytest"] is True
