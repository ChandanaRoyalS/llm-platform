# Gates

Execution plan rule 1: *"Gates are hard. A phase is done when its gate passes from a fresh
clone and the evidence is written in docs/GATES.md."* This file is that record.

A gate is **declared** only when its condition has been observed, from a clean clone, with
the evidence written down here. "Not declared" does not mean failed — it means nobody has
checked, or a known blocker stands in the way. Work cut under rule 6 (buffer day used) is
recorded in the gate's section too, never carried forward.

Conditions below are transcribed from *LLM Platform Execution Plan v2 — Inspection Reports*,
"Gate conditions and evidence". That document is authoritative; verify wording against it
before relying on it.

| Gate | Due | Condition | Status |
|---|---|---|---|
| G0 | 18 Oct | `make check` green (ruff, mypy --strict, pytest) on the skeleton; `make up` brings up Postgres+pgvector and Langfuse; CI runs on push | Not declared |
| G1 | 18 Oct | 300+ labelled cases from 60+ reports, split by report, test split hashed; kappa ≥ 0.75 on system and severity for the hand-corrected 20%; EVAL_SPEC.md and SEVERITY_RUBRIC.md committed before any model run | Not declared |
| G2 | 25 Oct | Final adapter beats base by ≥ MDE on macro field F1, CI of paired delta excludes zero, JSON validity ≥ 98%; W&B linked; adapter on HF Hub with model card | Not declared |
| G3 | 1 Nov | vLLM serves the AWQ model from our Docker image; Locust p50/p95, TTFT, tokens/s at 1/8/32 users for fp16 and AWQ; AWQ-vs-fp16 delta with CI | Not declared |
| G4 | 8 Nov | `make infra-up` creates VPC/EKS/node groups/S3/ECR from nothing; same chart deploys on kind and EKS, helm test green on both; `make infra-down` leaves nothing billable (Cost Explorer next day) | Not declared |
| G5 | 15 Nov | 20 held-out reports summarized with 100% citation grounding and severity agreement ≥ G2 test F1 minus 3 pp; 30 held-out SQL questions ≥ 80% result-set match; thread survives restart; ADR-0008 | Not declared |
| G6 | 22 Nov | Every turn in Langfuse with cost; UI streams over SSE with findings, thumbnails and SQL; promptfoo and Ragas agree with the in-house harness within its CI | Not declared |
| G7 | 22 Nov | README with results-at-a-glance, 4-minute video, v0.1 tag, GHCR images, model card linked, `make demo` reproducible | Not declared |

Early-ship point: with G3 declared the train-and-serve story is complete. If interviews
start, v0.1 is tagged there and Phases 4–6 ship as v0.2 (change control, case 3).

## G0 — not declared

Full condition: *"make check green (ruff, mypy --strict, pytest) on the skeleton; make up
brings up Postgres+pgvector and Langfuse; CI runs on push."*

Evidence required: CI link, test count. To be filled in from a fresh clone on a clean
machine or container.

- `make check` — _pending_
- `make up` — _pending_
- CI run on push — _pending_
