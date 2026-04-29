from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.metadata.tutorial003_py310 import app

client = TestClient(app)


@test("GET /items/ returns the items list")
def items():
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal([{"name": "Foo"}])


@test("OpenAPI schema matches snapshot")
def openapi_schema():
    response = client.get("/openapi.json")
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


@test("Default Swagger UI URL /docs returns 404 when relocated")
def swagger_ui_default_url():
    response = client.get("/docs")
    expect(response.status_code, "status code").to_equal(404)


@test("Swagger UI is served at the custom /documentation URL")
def swagger_ui_custom_url():
    response = client.get("/documentation")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.text, "response text").to_contain("<title>FastAPI - Swagger UI</title>")


@test("Default ReDoc URL /redoc returns 404 when disabled")
def redoc_ui_default_url():
    response = client.get("/redoc")
    expect(response.status_code, "status code").to_equal(404)
