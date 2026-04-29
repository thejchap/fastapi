from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.extending_openapi.tutorial001_py310 import app

client = TestClient(app)


@test("GET /items/ returns the items list")
def root():
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
                    "title": "Custom title",
                    "summary": "This is a very custom OpenAPI schema",
                    "description": "Here's a longer description of the custom **OpenAPI** schema",
                    "version": "2.5.0",
                    "x-logo": {
                        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
                    },
                },
                "paths": {
                    "/items/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                        }
                    }
                },
            }
        )
    )
    openapi_schema = response.json()
    # Request again to test the custom cache.
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(openapi_schema)
