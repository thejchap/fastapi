import importlib

from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import monkeypatch_ctx


def get_client() -> TestClient:
    from docs_src.conditional_openapi import tutorial001_py310

    importlib.reload(tutorial001_py310)

    client = TestClient(tutorial001_py310.app)
    return client


@test
def disable_openapi():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setenv("OPENAPI_URL", "")
        # Load the client after setting the env var.
        client = get_client()
        response = client.get("/openapi.json")
        expect(response.status_code).to_equal(404)
        response = client.get("/docs")
        expect(response.status_code).to_equal(404)
        response = client.get("/redoc")
        expect(response.status_code).to_equal(404)


@test
def root():
    client = get_client()
    response = client.get("/")
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"message": "Hello World"})


@test
def default_openapi():
    client = get_client()
    response = client.get("/docs")
    expect(response.status_code).to_equal(200)
    response = client.get("/redoc")
    expect(response.status_code).to_equal(200)
    response = client.get("/openapi.json")
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/": {
                        "get": {
                            "summary": "Root",
                            "operationId": "root__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                        }
                    }
                },
            }
        )
    )
