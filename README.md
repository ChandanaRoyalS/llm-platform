# llm-platform

A LoRA-fine-tuned open model that extracts findings from home-inspection reports, served with
vLLM on infrastructure provisioned with Terraform and Helm, driven by a LangGraph agent that
turns a report into a graded, page-cited findings summary and answers cross-report questions
through read-only SQL, observed in Langfuse, with a Next.js review UI. All data is public
sample inspection reports.

Built in six weeks, seven phases, eight gates: `docs/GATES.md` is the record of which gates
have passed and the evidence for each. The results table lands here at G6.

## Status

| Gate | Due | Status |
|---|---|---|
| G0 | 18 Oct 2026 | Not declared |
| G1 | 18 Oct 2026 | Not declared |
| G2 | 25 Oct 2026 | Not declared |
| G3 | 1 Nov 2026 | Not declared |
| G4 | 8 Nov 2026 | Not declared |
| G5 | 15 Nov 2026 | Not declared |
| G6 | 22 Nov 2026 | Not declared |
| G7 | 22 Nov 2026 | Not declared |

## Quickstart

Prerequisites: [uv](https://docs.astral.sh/uv/), Docker with Compose v2, `make`.

```sh
uv sync --all-groups   # Python 3.12 environment
make check             # ruff, ruff format --check, mypy --strict, pytest (80% coverage floor)
make up                # Postgres 16 + pgvector on :5432, Langfuse on :3000, schema applied
make test-stack        # the connectivity tests against the running stack
make down
```

`make ingest`, `make demo`, `make infra-up` and `make infra-down` are stubs until the phase
that implements each (5, 6, 4, 4).

## Layout

```
src/llm_platform/   schema.py (extraction schema, ADR-0001), config.py, stack.py
ingest/schema.sql   reports + findings tables, applied by `make up`
docs/               GATES.md, LOG.md, CHANGES.md, adr/
tests/              unit tests; tests/test_stack_live.py behind the `stack` marker
```

## How this was built

Every decision is a one-page ADR in `docs/adr/`. One log line per day in `docs/LOG.md`.
Scope changes only through `docs/CHANGES.md`. Commits are authored solely by the owner.
