"""Unit tests for the atomic state manager ``scripts/manage_state.py``."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import manage_state  # noqa: E402


def init_state(tmp_path: Path, route: str = "Standard") -> Path:
    """Create an initialized state file and return its path."""
    path = tmp_path / "ai_pipeline" / "state.json"
    assert manage_state.main(["init", str(path), "--route", route]) == 0
    return path


def read_json(path: Path) -> dict:
    """Read the state file as JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def test_should_initialize_state_with_route(tmp_path: Path) -> None:
    """Given init, the state file carries the route and zeroed fields."""
    path = init_state(tmp_path, route="High-risk")

    state = read_json(path)

    assert state["route"] == "High-risk"
    assert state["phase"] == "plan"
    assert state["self_heal_round"] == 0
    assert state["escape_hatches"] == []


def test_should_merge_updates_and_refresh_timestamp(tmp_path: Path) -> None:
    """Given update --set pairs, fields merge without dropping prior state."""
    path = init_state(tmp_path)

    exit_code = manage_state.main(
        [
            "update",
            str(path),
            "--set",
            "phase=implement",
            "--set",
            "current_task=T003",
            "--set",
            "self_heal_round=2",
        ]
    )

    assert exit_code == 0
    state = read_json(path)
    assert state["phase"] == "implement"
    assert state["current_task"] == "T003"
    assert state["self_heal_round"] == 2
    assert state["route"] == "Standard"


def test_should_coerce_list_fields_from_semicolon_strings(tmp_path: Path) -> None:
    """Given an escape_hatches update, the value becomes a JSON list."""
    path = init_state(tmp_path)

    manage_state.main(
        ["update", str(path), "--set", "escape_hatches=T001 L0: Any;T004 L1: cast()"]
    )

    assert read_json(path)["escape_hatches"] == ["T001 L0: Any", "T004 L1: cast()"]


def test_should_reject_unknown_fields(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Given an unknown --set key, update exits 2 without writing."""
    path = init_state(tmp_path)

    exit_code = manage_state.main(["update", str(path), "--set", "bogus=1"])

    assert exit_code == 2
    assert "unknown state field" in capsys.readouterr().err


def test_should_refuse_update_on_empty_state(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Given a missing state file, update exits 2 with a hint to init."""
    path = tmp_path / "state.json"

    exit_code = manage_state.main(["update", str(path), "--set", "phase=verify"])

    assert exit_code == 2
    assert "run init first" in capsys.readouterr().err


def test_should_clear_state_to_empty_object(tmp_path: Path) -> None:
    """Given clear, the state file becomes {} and is not deleted."""
    path = init_state(tmp_path)

    assert manage_state.main(["clear", str(path)]) == 0

    assert path.exists()
    assert read_json(path) == {}


def test_should_read_back_breakpoint_summary(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Given a populated state, read prints the breakpoint summary line."""
    path = init_state(tmp_path)
    manage_state.main(
        ["update", str(path), "--set", "current_task=T007", "--set", "current_file=src/a.py"]
    )

    assert manage_state.main(["read", str(path)]) == 0

    out = capsys.readouterr().out
    assert "breakpoint: plan/T007 (file: src/a.py" in out


def test_should_fail_cleanly_on_corrupt_state(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Given a corrupt state file, read exits 1 with a corruption message."""
    path = tmp_path / "state.json"
    path.write_text("{not json", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        manage_state.main(["read", str(path)])

    assert excinfo.value.code == 1
    assert "corrupt state file" in capsys.readouterr().err


def test_should_not_leave_temp_files_after_writes(tmp_path: Path) -> None:
    """Given repeated updates, no temp files remain alongside the state file."""
    path = init_state(tmp_path)
    for round_no in range(3):
        manage_state.main(
            ["update", str(path), "--set", f"self_heal_round={round_no}"]
        )

    leftovers = list(path.parent.glob("*.tmp"))

    assert leftovers == []
