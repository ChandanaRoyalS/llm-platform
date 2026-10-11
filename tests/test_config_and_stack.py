import httpx
import pytest

from llm_platform.config import Settings, load_settings
from llm_platform.stack import check_langfuse


def test_settings_defaults_match_compose(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LLMP_DATABASE_URL", raising=False)
    monkeypatch.delenv("LLMP_LANGFUSE_HOST", raising=False)
    s = load_settings()
    assert s.database_url == "postgresql://llm:llm@localhost:5432/llm_platform"
    assert s.langfuse_host == "http://localhost:3000"


def test_settings_read_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLMP_LANGFUSE_HOST", "http://langfuse:3000/")
    assert Settings().langfuse_host == "http://langfuse:3000/"


def _client(handler: httpx.MockTransport) -> httpx.Client:
    return httpx.Client(transport=handler)


def test_check_langfuse_returns_health_body() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/public/health"
        return httpx.Response(200, json={"status": "OK", "version": "4.0.0"})

    body = check_langfuse("http://langfuse.local/", client=_client(httpx.MockTransport(handler)))
    assert body["status"] == "OK"


def test_check_langfuse_raises_on_http_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"status": "error"})

    with pytest.raises(httpx.HTTPStatusError):
        check_langfuse("http://langfuse.local", client=_client(httpx.MockTransport(handler)))


def test_check_langfuse_rejects_non_object_body() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=["not", "an", "object"])

    with pytest.raises(ValueError, match="unexpected health body"):
        check_langfuse("http://langfuse.local", client=_client(httpx.MockTransport(handler)))
