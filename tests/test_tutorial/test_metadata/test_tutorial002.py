from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.metadata.tutorial002_py310 import app

client = TestClient(app)


@test("GET /items/ returns the items list")
def items():
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal([{"name": "Foo"}])


@test("Default /openapi.json URL returns 404 when relocated")
def get_openapi_json_default_url():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(404)


@test("OpenAPI schema is served at the custom /api/v1/openapi.json URL")
def openapi_schema():
    response = client.get("/api/v1/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {
                    "title": "FastAPI",
                    "version": "0.1.0",
                },
                "paths": {
                    "/items/": {
                        "get": {
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
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
