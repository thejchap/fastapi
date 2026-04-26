import importlib
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import monkeypatch_ctx, tmp_path_ctx


# Same sandboxing rationale as test_tutorial001 — see that file's note.
@contextmanager
def _client() -> Iterator[TestClient]:
    with tmp_path_ctx() as tmp, monkeypatch_ctx() as mp:
        (tmp / "static").mkdir()
        mp.chdir(tmp)
        mod = importlib.reload(
            importlib.import_module("docs_src.custom_docs_ui.tutorial002_py310")
        )
        with TestClient(mod.app) as client:
            yield client


@test
def swagger_ui_html():
    with _client() as client:
        response = client.get("/docs")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.text).to_contain("/static/swagger-ui-bundle.js")
        expect(response.text).to_contain("/static/swagger-ui.css")


@test
def swagger_ui_oauth2_redirect_html():
    with _client() as client:
        response = client.get("/docs/oauth2-redirect")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.text).to_contain("window.opener.swaggerUIRedirectOauth2")


@test
def redoc_html():
    with _client() as client:
        response = client.get("/redoc")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.text).to_contain("/static/redoc.standalone.js")


@test
def api():
    with _client() as client:
        response = client.get("/users/john")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()["message"]).to_equal("Hello john")
