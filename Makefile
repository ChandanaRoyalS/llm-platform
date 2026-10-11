.PHONY: help install lint format type test test-stack check up down wait-langfuse schema ingest demo infra-up infra-down

help:
	@grep -E '^[a-z][a-z0-9-]*:' Makefile | sed 's/:.*//' | tr '\n' ' '; echo

install:
	uv sync --all-groups

lint:
	uv run ruff check src tests
	uv run ruff format --check src tests

format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

type:
	uv run mypy

test:
	uv run pytest

# Runs only after `make up`: connects to Postgres+pgvector and Langfuse (T0.3).
test-stack:
	uv run pytest -m stack -o addopts=-q

check: lint type test
	@echo "all checks passed"

# `--wait` blocks until every healthcheck passes, so the schema step below never races
# initdb on a fresh volume. The schema is idempotent (IF NOT EXISTS), so `make up` is safe
# to run on a machine that has run it before.
up:
	docker compose up -d --wait
	$(MAKE) wait-langfuse
	$(MAKE) schema

# Langfuse's image has no wget/curl for a container healthcheck, so readiness is polled from the host.
wait-langfuse:
	@echo waiting for Langfuse...; for i in $$(seq 1 60); do curl -fsS http://localhost:3000/api/public/health >/dev/null 2>&1 && echo Langfuse healthy && exit 0; sleep 3; done; echo Langfuse did not become healthy; docker compose logs langfuse-web --tail 20; exit 1

# Idempotent (IF NOT EXISTS), so `make up` is safe on a machine that has run it before.
schema:
	docker compose exec -T db psql -v ON_ERROR_STOP=1 -U llm -d llm_platform < ingest/schema.sql

down:
	docker compose down


# ---- stubs: each target is implemented in the phase named, and not before ----

ingest:
	@echo "make ingest: implemented in Phase 5 (T5.1)"; exit 1

demo:
	@echo "make demo: implemented in Phase 6 (T6.7)"; exit 1

infra-up:
	@echo "make infra-up: implemented in Phase 4 (T4.4)"; exit 1

infra-down:
	@echo "make infra-down: implemented in Phase 4 (T4.4)"; exit 1
