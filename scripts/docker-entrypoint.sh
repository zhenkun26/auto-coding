#!/bin/sh
# auto-coding container entrypoint.
#
# Modes:
#   validate (default): run the unit tests and repository checks, then exit.
#   serve:              serve the repository as a read-only docs mirror on :8000.
set -eu

if [ "${MODE:-validate}" = "serve" ]; then
  echo "[auto-coding] serving docs mirror on :${PORT:-8000}"
  exec python -m http.server "${PORT:-8000}" --directory /app
fi

echo "[auto-coding] validating..."
python -m pytest /app/tests/ -q
python /app/scripts/check_repo.py
echo "[auto-coding] validation passed"
