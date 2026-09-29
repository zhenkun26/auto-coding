"""Run repository pytest checks with retained fixtures and no automatic cleanup.

Uses the already installed pytest. This is a test-runner convenience, not a
subprocess sandbox: inspect subprocess behavior separately. All fixture paths
are retained for the user to manage.
"""

from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path


def main() -> int:
    """Run selected pytest arguments (or the whole suite) without disk capture."""
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    sys.dont_write_bytecode = True
    import pytest

    base = Path(os.environ.get("TMPDIR", "/tmp")) / f"auto-coding-tests-{uuid.uuid4().hex}"
    base.mkdir(parents=True)

    class RetainedFixtures:
        @pytest.fixture
        def tmp_path(self) -> Path:
            path = base / uuid.uuid4().hex
            path.mkdir()
            return path

    def reject_cleanup(event: str, args: tuple[object, ...]) -> None:
        if event in {"os.remove", "os.rmdir"}:
            raise RuntimeError(f"filesystem deletion is disabled: {event} {args}")

    sys.addaudithook(reject_cleanup)
    print(f"Retained test artifacts: {base}", flush=True)
    args = sys.argv[1:] or ["tests/", "-q"]
    return int(pytest.main([*args, "--capture=sys", "-p", "no:cacheprovider"], plugins=[RetainedFixtures()]))


if __name__ == "__main__":
    sys.exit(main())
