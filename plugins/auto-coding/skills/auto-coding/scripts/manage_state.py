#!/usr/bin/env python3
"""Atomic single-file state management for auto-coding cross-session recovery.

All writes go through a temp file + os.replace, so a crash never leaves a
torn state file. Standard library only.

Usage:
    manage_state.py init <path> --route <Fast|Standard|High-risk>
    manage_state.py update <path> --set key=value [--set key=value ...]
    manage_state.py read <path>
    manage_state.py clear <path>
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
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
}

INT_FIELDS = {"self_heal_round"}
LIST_FIELDS = {"escape_hatches"}


def iso_now() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_state(path: Path) -> dict:
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
    return state


def write_state(path: Path, state: dict) -> None:
    """Write state atomically via a sibling temp file and rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=path.name + ".", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def coerce(key: str, value: str) -> object:
    """Coerce a --set string value to the field's JSON type."""
    if key in INT_FIELDS:
        try:
            return int(value)
        except ValueError:
            print(f"error: {key} must be an integer, got {value!r}", file=sys.stderr)
            raise SystemExit(2)
    if key in LIST_FIELDS:
        return [item for item in value.split(";") if item]
    return value


def cmd_init(args: argparse.Namespace) -> int:
    """Initialize a fresh state file."""
    path = Path(args.path)
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
    for pair in args.set:
        if "=" not in pair:
            print(f"error: --set expects key=value, got {pair!r}", file=sys.stderr)
            return 2
        key, value = pair.split("=", 1)
        if key not in SCHEMA_FIELDS:
            print(f"error: unknown state field {key!r}", file=sys.stderr)
            return 2
        state[key] = coerce(key, value)
    state["last_update"] = iso_now()
    write_state(path, state)
    print(f"updated {path}: {', '.join(pair.split('=', 1)[0] for pair in args.set)}")
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    """Print the state, plus the resume hint when one is recorded."""
    path = Path(args.path)
    state = read_state(path)
    print(json.dumps(state, indent=2, ensure_ascii=False))
    if state:
        hint = state.get("resume_hint")
        if hint:
            print(f"\nresume_hint: {hint}")
        print(
            "breakpoint: "
            f"{state.get('phase', '?')}/{state.get('current_task', '?')} "
            f"(file: {state.get('current_file', '?')}, "
            f"self-heal round {state.get('self_heal_round', '?')}/3)"
        )
    return 0


def cmd_clear(args: argparse.Namespace) -> int:
    """Mark the run completed by clearing the state to {}."""
    path = Path(args.path)
    write_state(path, {})
    print(f"cleared {path}")
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

    p_clear = sub.add_parser("clear", help="clear the state to {}")
    p_clear.add_argument("path")
    p_clear.set_defaults(func=cmd_clear)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
