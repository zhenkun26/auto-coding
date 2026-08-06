# syntax=docker/dockerfile:1

########################################
# Builder: install test dependencies only
########################################
FROM python:3.12-alpine AS builder

WORKDIR /build

# Build cache for pip: accelerates CI/CD rebuilds.
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir pytest && \
    pip uninstall -y setuptools wheel 2>/dev/null || true

# Strip bytecode caches in the builder so the copy into the runner is lean.
RUN find /usr/local/lib/python3.12/site-packages -type d -name __pycache__ -prune -exec rm -rf {} + && \
    find /usr/local/lib/python3.12/site-packages -type f -name '*.pyc' -delete

########################################
# Runner: minimal image, non-root, HEALTHCHECK
########################################
FROM python:3.12-alpine AS runner

# Create a non-root user with a fixed uid (matches runAsUser in /deploy).
RUN addgroup -S -g 10001 app && adduser -S -G app -u 10001 app

WORKDIR /app

# Copy only the runtime/test dependencies from the builder (bytecode already stripped).
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy the repository (see .dockerignore for exclusions).
COPY --chown=app:app . .
COPY --chmod=0755 scripts/docker-entrypoint.sh /app/docker-entrypoint.sh

USER app

EXPOSE 8000

# Serves the docs mirror (MODE=serve). The validation mode exits after checks.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8000/ >/dev/null 2>&1 || exit 1

ENV MODE=validate
ENTRYPOINT ["/app/docker-entrypoint.sh"]
