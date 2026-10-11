"""Connectivity checks for the local stack (T0.3). Used by `make test-stack`."""

from __future__ import annotations

from dataclasses import dataclass

import httpx
import psycopg


@dataclass(frozen=True)
class PostgresStatus:
    version: str
    pgvector: str | None
    tables: tuple[str, ...]


def check_postgres(database_url: str) -> PostgresStatus:
    """Connect, read the server version, the pgvector version, and the public tables."""
    with psycopg.connect(database_url, connect_timeout=5) as conn, conn.cursor() as cur:
        cur.execute("select version()")
        row = cur.fetchone()
        version = str(row[0]) if row else ""
        cur.execute("select extversion from pg_extension where extname = 'vector'")
        ext = cur.fetchone()
        pgvector = str(ext[0]) if ext else None
        cur.execute(
            "select table_name from information_schema.tables "
            "where table_schema = 'public' order by table_name"
        )
        tables = tuple(str(r[0]) for r in cur.fetchall())
    return PostgresStatus(version=version, pgvector=pgvector, tables=tables)


def check_langfuse(host: str, client: httpx.Client | None = None) -> dict[str, object]:
    """Hit Langfuse's public health endpoint and return its JSON body."""
    url = host.rstrip("/") + "/api/public/health"
    own = client is None
    c = client or httpx.Client(timeout=10)
    try:
        resp = c.get(url)
        resp.raise_for_status()
        body = resp.json()
    finally:
        if own:
            c.close()
    if not isinstance(body, dict):
        raise ValueError(f"unexpected health body from {url}: {body!r}")
    return dict(body)
