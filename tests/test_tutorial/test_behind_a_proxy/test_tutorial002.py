from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.behind_a_proxy.tutorial002_py310 import app

client = TestClient(app)


@test("GET /app returns the configured root_path")
def main():
    response = client.get("/app")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"message": "Hello World", "root_path": "/api/v1"}
    )


@test("OpenAPI schema includes the configured server")
def openapi():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/app": {
                        "get": {
                            "summary": "Read Main",
                            "operationId": "read_main_app_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                        }
                    }
                },
                "servers": [{"url": "/api/v1"}],
            }
        )
    )
