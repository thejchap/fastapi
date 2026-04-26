import os
from pathlib import Path

from fastapi.testclient import TestClient
from tryke import Depends, expect, fixture, test


@fixture
def client():
    static_dir: Path = Path(os.getcwd()) / "static"
    created = not static_dir.exists()
    static_dir.mkdir(exist_ok=True)
    from docs_src.custom_docs_ui.tutorial002_py310 import app

    with TestClient(app) as client:
        yield client
    if created and static_dir.exists():
        static_dir.rmdir()


@test
def swagger_ui_html(client: TestClient = Depends(client)):
    response = client.get("/docs")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.text).to_contain("/static/swagger-ui-bundle.js")
    expect(response.text).to_contain("/static/swagger-ui.css")


@test
def swagger_ui_oauth2_redirect_html(client: TestClient = Depends(client)):
    response = client.get("/docs/oauth2-redirect")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.text).to_contain("window.opener.swaggerUIRedirectOauth2")


@test
def redoc_html(client: TestClient = Depends(client)):
    response = client.get("/redoc")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.text).to_contain("/static/redoc.standalone.js")


@test
def api(client: TestClient = Depends(client)):
    response = client.get("/users/john")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()["message"]).to_equal("Hello john")
