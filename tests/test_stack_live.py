"""T0.3/T0.4: connects to the local stack. Run with `make test-stack` after `make up`."""

import pytest

from llm_platform.config import load_settings
from llm_platform.stack import check_langfuse, check_postgres

pytestmark = pytest.mark.stack


def test_postgres_with_pgvector_and_schema() -> None:
    status = check_postgres(load_settings().database_url)
    assert status.version.startswith("PostgreSQL 16")
    assert status.pgvector_available, "pgvector extension is not available on this server"
    assert status.pgvector is not None, "pgvector extension is not installed (make up applies it)"
    assert "reports" in status.tables
    assert "findings" in status.tables


def test_langfuse_is_healthy() -> None:
    body = check_langfuse(load_settings().langfuse_host)
    assert body.get("status") == "OK"
