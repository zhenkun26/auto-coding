"""Deterministic assertions on adversarial fixture scenarios.

These tests pin down the failure modes this repository's own tooling must
never silently pass — see ``tests/fixtures/adversarial/README.md`` for the
trap catalog. They verify the *mechanisms* (detectors, checkers, state
manager), not prompt-level agent compliance, which remains a documented
validation boundary.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "adversarial"

sys.path.insert(0, str(SCRIPTS_DIR))

import detect_project


def run_contract_checker(fixture: str) -> subprocess.CompletedProcess[str]:
    """Run the contract checker CLI against one fixture directory."""
    fixture_dir = FIXTURES / fixture
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "check_python_contracts.py"),
            "--spec",
            str(fixture_dir / "spec.md"),
            "--source",
            str(fixture_dir / "src"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_trap_contract_mismatch_must_fail_with_missing_and_param_count() -> None:
    """Spec defines 3 contracts, code implements 1: the checker must not pass."""
    result = run_contract_checker("contract_mismatch")

    assert result.returncode == 1
    assert "MISSING: function 'audit_log'" in result.stdout
    assert "PARAM_COUNT: 'PaymentService.refund'" in result.stdout
    assert "OK: method 'PaymentService.authorize'" in result.stdout


def test_trap_missing_return_annotations_must_not_false_pass() -> None:
    """Signatures without return annotations must fail, never silently pass."""
    result = run_contract_checker("false_pass_return_types")

    assert result.returncode == 1
    assert result.stdout.count("RETURN_TYPE_MISSING:") == 2
    assert "PASSED (0)" not in result.stdout


def test_trap_prose_signatures_must_be_ignored() -> None:
    """Signature-looking prose outside fences must not be treated as contracts."""
    result = run_contract_checker("prose_trap")

    assert result.returncode == 0
    assert "All 1 contracts structurally verified." in result.stdout
    assert "validate" not in result.stdout
    assert "render" not in result.stdout


def test_control_valid_project_must_pass() -> None:
    """A fully spec-compliant fixture must pass — guards over-strict regressions."""
    result = run_contract_checker("valid_project")

    assert result.returncode == 0
    assert "All 3 contracts structurally verified." in result.stdout


def test_trap_empty_tests_dir_is_not_pytest_configured() -> None:
    """An empty tests/ directory must not be reported as pytest configured."""
    configs = detect_project.detect_configs(FIXTURES / "stale_tests_dir")

    assert configs["pytest"] is False


def test_trap_multiple_source_roots_are_all_reported() -> None:
    """src + cmd layouts must report every root, primary = most source files."""
    state = detect_project.detect_codebase_state(FIXTURES / "multi_source_root")

    assert state["source_roots"] == ["src", "cmd"]
    assert state["source_root"] == "src"
    assert state["source_files"] == 3
    assert state["state"] == "brownfield"


def test_trap_corrupt_state_must_fail_loudly() -> None:
    """A torn state file must exit 1 with a corruption error, not crash or pass."""
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "manage_state.py"),
            "read",
            str(FIXTURES / "corrupt_state" / "state.json"),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "corrupt state file" in result.stderr


def test_detect_project_json_report_on_fixture_is_parseable() -> None:
    """The detector's JSON contract stays stable on a fixture project."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "detect_project.py"), str(FIXTURES / "multi_source_root")],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report["codebase"]["source_roots"] == ["src", "cmd"]
    assert set(report) >= {"root", "templates", "ci", "openspec", "git", "codebase", "tools", "configs"}
