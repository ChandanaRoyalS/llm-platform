# Log

One line per working day (execution plan rule 9): date · shipped · slipped · dollars spent.
Running total in the last column. The Sunday-evening weekly check (three questions) goes at
the end of that week's block.

GPU hourly price, checked the Sunday before Phase 2: _not yet checked_.

| Date | Shipped | Slipped | $ today | $ total |
|---|---|---|---|---|
| 2026-10-10 | T0.1 (ahead of the Monday start): repo on GitHub, uv, ruff, mypy --strict, pytest with 80% floor, pre-commit, Makefile with stubs, CI green on main. T0.2: GATES/LOG/CHANGES, ADR template, ADR-0001. T0.3: docker-compose (pgvector on :5433, Langfuse v4 on :3000), make up/down/test-stack, connectivity tests, CI stack job | CI stack job removed until T0.3 (hashFiles is not valid in a job-level if; two red runs). T0.3 cost ~40 min on three things: Langfuse rejects LANGFUSE_INIT_USER_EMAIL without a dotted domain; its image has no wget, so the web healthcheck moved to a curl loop in `make up`; db moved to host port 5433 because another project's Postgres owns 5432 | 0 | 0 |

## Ideas for v0.3

Not changes (change control, "explicitly not changes"). Parked here and nowhere else.

- _none yet_
