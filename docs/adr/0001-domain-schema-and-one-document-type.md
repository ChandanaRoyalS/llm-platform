# ADR-0001: Domain, extraction schema, and why one document type

- **Status:** accepted
- **Date:** 2026-10-12
- **Phase:** 0

## Context

The project exists to prove a full fine-tuning lifecycle — data, pre-registered evaluation,
QLoRA SFT and DPO, quantized serving, cloud infrastructure, an agent on top — in six weeks
and about $180. The domain has to give the fine-tune something to win at: a task where a
7–8B instruct model is measurably wrong zero-shot, where labels can be produced and checked
without a domain expert on call, and where every input is public.

Home-inspection reports fit all three. Inspection companies and inspection-software vendors
(HomeGauge, Spectora, Inspector Nexus) publish sample reports, and Texas's TREC form gives
a fixed structure (system sections with D/I/NI/NP checkboxes) to a large share of them.
The reports are long, repetitive and full of boilerplate, so the hard part of extraction is
not reading English but deciding what a *finding* is: separating an observed defect from a
recommendation and from standard disclaimer text, naming the building system, and grading
severity against a rubric the report itself does not state.

Alternatives considered and set aside: a realtor-facing task on MLS listing data (no public
corpus at the needed size), and a second document type alongside inspection reports (doubles
the labelling and evaluation cost without adding a new kind of evidence to the resume line).

## Decision

**Domain.** Home-inspection reports only, from public sample reports; no data from any
client or pilot user; nothing identifying a property is stored (`reports` carries
address-free metadata only).

**Extraction unit.** One *finding*: a span of report text (a TREC system section, or a
heading plus paragraph in narrative formats) mapped to one JSON object. A report yields many
findings; a case is one span in, one object out.

**Schema.** Fixed here, implemented in `src/llm_platform/schema.py`, mirrored column for
column in `ingest/schema.sql`, and held in step by `tests/test_schema.py`.

| Field | Type | Hard for the base model? |
|---|---|---|
| `report_id`, `page` | str, int | no |
| `location` | str (e.g. master bathroom, attic) | partly |
| `system` | enum: structural, roof, exterior, electrical, plumbing, hvac, appliances, interior, grounds, other | yes |
| `defect` | str — the observed condition in the inspector's words | yes (defect vs recommendation vs boilerplate) |
| `recommendation` | str or null | yes |
| `severity` | enum: safety, major, maintenance, cosmetic, informational (rubric in `docs/SEVERITY_RUBRIC.md`, Phase 1) | yes |
| `deficient` | bool (TREC D checkbox or equivalent) | partly |
| `photo_refs` | list of page-local photo indices | partly |

`system` and `severity` are the fields where the fine-tune is expected to carry the large
gains, and G2's per-field breakdown reports them separately. `severity` depends on a rubric
that is written in Phase 1 and frozen at G1, so that a label and a model prediction are
scored against the same text.

**One document type, several hard fields.** The alternative — a broader, shallower target —
spreads 300+ cases over more than one format and makes every per-field number noisier.
One type with four fields the base model gets wrong (`system`, `defect`, `recommendation`,
`severity`) is enough to make or break the G2 decision rule (CI of the paired macro-F1
delta excludes zero, MDE 5 pp) and leaves no room to blame the data.

## Consequences

Easier: one OCR pipeline, one case builder, one rubric; a per-field table a recruiter can
read; a `findings` table that the Phase 5 SQL agent can query without joins beyond
`reports`.

Harder: generalization claims stop at this document type; the schema cannot be changed
after G1 without re-labelling, so Phase 1 is where it must be right. Format variety
(TREC vs narrative) becomes a split-by-report concern, not a schema concern.

Revisit under: fewer than 40 public reports found (risk table, row 1 — synthetic reports
capped at 30% of cases and flagged); kappa on `severity` below 0.75 after one rubric
revision (row 3 — merge maintenance and cosmetic). A second document type is explicitly not
a change (change control) and belongs under "ideas for v0.3" in `LOG.md`.
