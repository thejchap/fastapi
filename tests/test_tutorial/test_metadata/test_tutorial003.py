from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.metadata.tutorial003_py310 import app

client = TestClient(app)


@test
def items():
    response = client.get("/items/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal([{"name": "Foo"}])


@test
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
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


@test
def swagger_ui_default_url():
    response = client.get("/docs")
    expect(response.status_code).to_equal(404)


@test
def swagger_ui_custom_url():
    response = client.get("/documentation")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.text).to_contain("<title>FastAPI - Swagger UI</title>")


@test
def redoc_ui_default_url():
    response = client.get("/redoc")
    expect(response.status_code).to_equal(404)
