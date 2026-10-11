-- T0.4: the two tables every later phase writes to. Applied by `make up`; idempotent.
-- `reports` holds address-free metadata only (ADR-0001: the data is public sample reports,
-- and nothing identifying a property is stored). `findings` carries every field of the
-- extraction schema (src/llm_platform/schema.py) as a column, in the same order;
-- tests/test_schema.py holds the two in step.

create extension if not exists vector;

create table if not exists reports (
    report_id       text primary key,
    source_url      text,                       -- where the public sample came from (data/manifest.csv)
    retrieved_at    date,
    format          text,                       -- e.g. trec, homegauge, spectora, narrative
    page_count      integer check (page_count >= 0),
    split           text check (split in ('train', 'dev', 'test')),
    created_at      timestamptz not null default now()
);

create table if not exists findings (
    finding_id      bigserial primary key,
    report_id       text not null references reports (report_id) on delete cascade,
    page            integer not null check (page >= 1),
    location        text not null,
    system          text not null check (system in (
                        'structural', 'roof', 'exterior', 'electrical', 'plumbing',
                        'hvac', 'appliances', 'interior', 'grounds', 'other')),
    defect          text not null,
    recommendation  text,
    severity        text not null check (severity in (
                        'safety', 'major', 'maintenance', 'cosmetic', 'informational')),
    deficient       boolean not null,
    photo_refs      integer[] not null default '{}',
    created_at      timestamptz not null default now()
);

create index if not exists findings_report_severity_page
    on findings (report_id, severity, page);
