import importlib
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import monkeypatch_ctx, tmp_path_ctx


# The original pytest version used a module-scoped fixture with a
# `workdir_lock` xdist marker so concurrent test files didn't race on
# `./static`. Tryke runs files concurrently and has no equivalent
# marker, so each test sandboxes itself in a fresh tmp_path with
# `./static` precreated and cwd pinned. The docs_src module is reloaded
# under the sandboxed cwd so its `StaticFiles(directory="static")`
# binds to the sandbox.
@contextmanager
def _client() -> Iterator[TestClient]:
    with tmp_path_ctx() as tmp, monkeypatch_ctx() as mp:
        (tmp / "static").mkdir()
        mp.chdir(tmp)
        mod = importlib.reload(
            importlib.import_module("docs_src.custom_docs_ui.tutorial001_py310")
        )
        with TestClient(mod.app) as client:
            yield client


@test("Custom /docs serves Swagger UI HTML with custom CDN URLs")
def swagger_ui_html():
    with _client() as client:
        response = client.get("/docs")
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.text, "response text").to_contain(
            "https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"
        )
        expect(response.text, "response text").to_contain(
            "https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"
        )


@test("Custom /docs/oauth2-redirect serves OAuth2 redirect HTML")
def swagger_ui_oauth2_redirect_html():
    with _client() as client:
        response = client.get("/docs/oauth2-redirect")
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.text, "response text").to_contain("window.opener.swaggerUIRedirectOauth2")


@test("Custom /redoc serves ReDoc HTML with custom CDN URL")
def redoc_html():
    with _client() as client:
        response = client.get("/redoc")
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.text, "response text").to_contain(
            "https://unpkg.com/redoc@2/bundles/redoc.standalone.js"
        )


@test("GET /users/john returns greeting")
def api():
    with _client() as client:
        response = client.get("/users/john")
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.json()["message"], "message field").to_equal("Hello john")
