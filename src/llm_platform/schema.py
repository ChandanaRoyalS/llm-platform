"""The extraction schema, fixed in Phase 1 and recorded in ADR-0001.

One `Finding` is the target of every training case, the shape the fine-tuned model is
asked to emit, and one row of the `findings` table (`ingest/schema.sql`). The three
definitions must stay in step; `tests/test_schema.py` holds the column list to this one.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class System(StrEnum):
    """The building system a finding belongs to."""

    STRUCTURAL = "structural"
    ROOF = "roof"
    EXTERIOR = "exterior"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    HVAC = "hvac"
    APPLIANCES = "appliances"
    INTERIOR = "interior"
    GROUNDS = "grounds"
    OTHER = "other"


class Severity(StrEnum):
    """Graded per docs/SEVERITY_RUBRIC.md (written in Phase 1, frozen at G1)."""

    SAFETY = "safety"
    MAJOR = "major"
    MAINTENANCE = "maintenance"
    COSMETIC = "cosmetic"
    INFORMATIONAL = "informational"


# Summary order: safety first, informational last (Phase 5 `load_findings` and `summarize`).
SEVERITY_ORDER: tuple[Severity, ...] = (
    Severity.SAFETY,
    Severity.MAJOR,
    Severity.MAINTENANCE,
    Severity.COSMETIC,
    Severity.INFORMATIONAL,
)


class Finding(BaseModel):
    """One extracted finding. Field order matches the ADR-0001 table."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    report_id: str = Field(min_length=1)
    page: int = Field(ge=1)
    location: str = Field(min_length=1, description="e.g. master bathroom, attic")
    system: System
    defect: str = Field(
        min_length=1, description="the observed condition, in the inspector's words"
    )
    recommendation: str | None = None
    severity: Severity
    deficient: bool = Field(description="TREC D checkbox or equivalent")
    photo_refs: list[int] = Field(default_factory=list, description="page-local photo indices")


FIELD_NAMES: tuple[str, ...] = tuple(Finding.model_fields)
