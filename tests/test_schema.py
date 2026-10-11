import re
from pathlib import Path

import pytest
from pydantic import ValidationError

from llm_platform.schema import FIELD_NAMES, SEVERITY_ORDER, Finding, Severity, System

ROOT = Path(__file__).resolve().parents[1]


def _finding(**overrides: object) -> Finding:
    base: dict[str, object] = {
        "report_id": "r-001",
        "page": 12,
        "location": "attic",
        "system": "electrical",
        "defect": "Open junction box with exposed splices",
        "recommendation": "Install a cover plate",
        "severity": "safety",
        "deficient": True,
        "photo_refs": [1, 2],
    }
    base.update(overrides)
    return Finding.model_validate(base)


def test_field_order_matches_adr_0001() -> None:
    assert FIELD_NAMES == (
        "report_id",
        "page",
        "location",
        "system",
        "defect",
        "recommendation",
        "severity",
        "deficient",
        "photo_refs",
    )


def test_enums_match_the_plan() -> None:
    assert [s.value for s in System] == [
        "structural",
        "roof",
        "exterior",
        "electrical",
        "plumbing",
        "hvac",
        "appliances",
        "interior",
        "grounds",
        "other",
    ]
    assert [s.value for s in Severity] == [
        "safety",
        "major",
        "maintenance",
        "cosmetic",
        "informational",
    ]
    assert tuple(Severity) == SEVERITY_ORDER


def test_valid_finding_round_trips_as_json() -> None:
    f = _finding()
    assert Finding.model_validate_json(f.model_dump_json()) == f


def test_recommendation_is_nullable_and_photo_refs_default_empty() -> None:
    f = _finding(recommendation=None, photo_refs=[])
    assert f.recommendation is None
    assert f.photo_refs == []
    g = Finding.model_validate(
        {k: v for k, v in _finding().model_dump().items() if k not in {"photo_refs"}}
    )
    assert g.photo_refs == []


@pytest.mark.parametrize(
    "bad",
    [
        {"system": "garage"},
        {"severity": "critical"},
        {"page": 0},
        {"defect": ""},
        {"deficient": "maybe"},
        {"extra_field": 1},
    ],
)
def test_invalid_findings_are_rejected(bad: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        _finding(**bad)


def test_findings_table_has_every_schema_field_as_a_column() -> None:
    """T0.4: `findings` carries every schema field as a column, in schema order."""
    sql = (ROOT / "ingest" / "schema.sql").read_text()
    m = re.search(r"create table if not exists findings \((.*?)\n\);", sql, re.S | re.I)
    assert m, "findings table not found in ingest/schema.sql"
    columns = [
        line.strip().split()[0]
        for line in m.group(1).splitlines()
        if line.strip() and not line.strip().startswith(("--", "primary", "constraint", "unique"))
    ]
    for name in FIELD_NAMES:
        assert name in columns, f"column {name} missing from findings"
    in_schema_order = [c for c in columns if c in FIELD_NAMES]
    assert in_schema_order == list(FIELD_NAMES)
