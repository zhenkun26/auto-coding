#!/usr/bin/env python3
"""Atomic single-file state management for auto-coding cross-session recovery.

All writes go through a temp file + os.replace. Failed writes retain the
temporary file for recovery; completion preserves the record. Single writer,
standard library only. Recorded evidence is not independently verified here.

Usage:
    manage_state.py init <path> --route <Fast|Standard|High-risk>
    manage_state.py update <path> --set key=value [--set key=value ...]
    manage_state.py read <path>
    manage_state.py complete <path> --summary <verified-outcome>
    manage_state.py clear <path> --summary <verified-outcome>  # deprecated alias
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_FIELDS = {
    "route",
    "phase",
    "current_task",
    "current_file",
    "self_heal_round",
    "escape_hatches",
    "started_at",
    "last_update",
    "resume_hint",
    "status",
    "objective",
    "boundary",
    "plan_ref",
    "completed",
    "remaining",
    "blockers",
    "evidence",
    "completion_summary",
}

INT_FIELDS = {"self_heal_round"}
LIST_FIELDS = {"escape_hatches", "completed", "remaining", "blockers", "evidence"}
ENUM_FIELDS = {
    "route": {"Fast", "Standard", "High-risk"},
    "phase": {"plan", "implement", "verify", "handoff"},
    "status": {"active", "blocked", "completed"},
}


def validate_state(state: dict[str, object]) -> str | None:
    """Validate field types, including legacy records without delivery fields."""
    for key, value in state.items():
        if key not in SCHEMA_FIELDS:
            return f"unknown state field {key!r}"
        if key in LIST_FIELDS:
            if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
                return f"{key} must be an array of nonempty strings"
        elif key in INT_FIELDS:
            if type(value) is not int or value < 0:
                return f"{key} must be a nonnegative integer"
        elif not isinstance(value, str):
            return f"{key} must be a string"
        elif key in ENUM_FIELDS and value not in ENUM_FIELDS[key]:
            return f"invalid {key}: {value!r}"
    if state and any(key not in state for key in ("route", "phase", "last_update")):
        return "state requires route, phase, and last_update"
    return None


def iso_now() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_state(path: Path) -> dict[str, object]:
    """Return the state dict, or {} when the file is absent or empty."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return {}
    try:
        state = json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"error: corrupt state file {path}: {exc}", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(state, dict):
        print(f"error: state file {path} is not a JSON object", file=sys.stderr)
        raise SystemExit(1)
    problem = validate_state(state)
    if problem:
        print(f"error: invalid state file {path}: {problem}", file=sys.stderr)
        raise SystemExit(1)
    return state


def write_state(path: Path, state: dict[str, object]) -> None:
    """Write state atomically via a sibling temp file and rename."""
    if path.is_symlink():
        raise OSError(f"refusing to replace symlink: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=path.name + ".", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        print(f"error: failed write; retained recovery file: {tmp_name}", file=sys.stderr)
        raise


def coerce(key: str, value: str) -> object:
    """Coerce a --set string value to the field's JSON type.

    List fields accept either a JSON array literal (preferred — items may
    contain any character, including ``;``) or a legacy ``;``-separated
    string. The ``;`` form is kept for backward compatibility but splits on
    every semicolon, so items must not contain one.
    """
    if key in INT_FIELDS:
        try:
            return int(value)
        except ValueError:
            print(f"error: {key} must be an integer, got {value!r}", file=sys.stderr)
            raise SystemExit(2)
    if key in LIST_FIELDS:
        stripped = value.strip()
        if stripped.startswith("["):
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError as exc:
                print(f"error: {key} JSON array is invalid: {exc}", file=sys.stderr)
                raise SystemExit(2)
            if not isinstance(parsed, list) or not all(
                isinstance(item, str) for item in parsed
            ):
                print(f"error: {key} must be a JSON array of strings", file=sys.stderr)
                raise SystemExit(2)
            return parsed
        return [item for item in value.split(";") if item]
    return value


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize a fresh state file."""
    path = Path(args.path)
    if path.exists() or path.is_symlink():
        print(f"error: {path} already exists; read it or choose a new task path", file=sys.stderr)
        return 2
    state = {
        "route": args.route,
        "phase": "plan",
        "current_task": "",
        "current_file": "",
        "self_heal_round": 0,
        "escape_hatches": [],
        "started_at": iso_now(),
        "last_update": iso_now(),
        "resume_hint": "",
        "status": "active",
        "objective": "",
        "boundary": "",
        "plan_ref": "",
        "completed": [],
        "remaining": [],
        "blockers": [],
        "evidence": [],
    }
    write_state(path, state)
    print(f"initialized {path} (route={args.route})")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """Merge --set key=value pairs into the state file."""
    path = Path(args.path)
    state = read_state(path)
    if not state:
        print(f"error: {path} is empty; run init first", file=sys.stderr)
        return 2
    if state.get("status") == "completed":
        print("error: completed records are retained; start a new task path", file=sys.stderr)
        return 2
    for pair in args.set:
        if "=" not in pair:
            print(f"error: --set expects key=value, got {pair!r}", file=sys.stderr)
            return 2
        key, value = pair.split("=", 1)
        if key not in SCHEMA_FIELDS:
            print(f"error: unknown state field {key!r}", file=sys.stderr)
            return 2
        if key == "completion_summary" or (key == "status" and value == "completed"):
            print("error: use complete --summary to finish a task", file=sys.stderr)
            return 2
        state[key] = coerce(key, value)
    state["last_update"] = iso_now()
    problem = validate_state(state)
    if problem:
        print(f"error: {problem}", file=sys.stderr)
        return 2
    write_state(path, state)
    print(f"updated {path}: {', '.join(pair.split('=', 1)[0] for pair in args.set)}")
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    """Print the state, plus the resume hint when one is recorded."""
    path = Path(args.path)
    state = read_state(path)
    print(json.dumps(state, indent=2, ensure_ascii=False))
    if state:
        print(f"status: {state.get('status', 'active (legacy)')}")
        hint = state.get("resume_hint")
        if hint:
            print(f"\nresume_hint: {hint}")
        print(
            "breakpoint: "
            f"{state.get('phase', '?')}/{state.get('current_task', '?')} "
            f"(file: {state.get('current_file', '?')}, "
            f"repair round {state.get('self_heal_round', '?')})"
        )
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    """Preserve a structurally complete record, without certifying its claims."""
    path = Path(args.path)
    state = read_state(path)
    if not state:
        print("error: no task record to complete", file=sys.stderr)
        return 2
    if state.get("status") == "completed":
        print("error: task already completed; retained record is unchanged", file=sys.stderr)
        return 2
    if not args.summary or not args.summary.strip():
        print("error: completion requires --summary; clear no longer erases state", file=sys.stderr)
        return 2
    if any(state.get(key) != [] for key in ("remaining", "blockers")) or state.get("status") == "blocked":
        print("error: completion requires explicit empty remaining and blockers lists, and an unblocked status", file=sys.stderr)
        return 2
    for key in ("objective", "boundary", "completed", "evidence"):
        value = state.get(key)
        if not value or (isinstance(value, str) and not value.strip()):
            print(f"error: completion requires recorded {key}", file=sys.stderr)
            return 2
    state.update(status="completed", phase="handoff", completion_summary=args.summary, last_update=iso_now())
    write_state(path, state)
    print(f"completed {path}; recorded evidence still requires semantic acceptance")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch to the subcommand."""
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="initialize a state file")
    p_init.add_argument("path")
    p_init.add_argument(
        "--route", required=True, choices=["Fast", "Standard", "High-risk"]
    )
    p_init.set_defaults(func=cmd_init)

    p_update = sub.add_parser("update", help="merge fields into the state file")
    p_update.add_argument("path")
    p_update.add_argument("--set", action="append", required=True, metavar="key=value")
    p_update.set_defaults(func=cmd_update)

    p_read = sub.add_parser("read", help="print the state and resume hint")
    p_read.add_argument("path")
    p_read.set_defaults(func=cmd_read)

    for name in ("complete", "clear"):
        help_text = "complete and preserve the record" if name == "complete" else "deprecated alias for complete"
        p_complete = sub.add_parser(name, help=help_text)
        p_complete.add_argument("path")
        p_complete.add_argument("--summary")
        p_complete.set_defaults(func=cmd_complete)

    args = parser.parse_args(argv)
    func: Callable[[argparse.Namespace], int] = args.func
    return func(args)


if __name__ == "__main__":
    sys.exit(main())
