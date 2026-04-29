from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("response_status_code", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def create_item(name: str):
    client = _client_for(name)
    response = client.post("/items/", params={"name": "Test Item"})
    expect(response.status_code, "status code").to_equal(201).fatal()
    expect(response.json(), "response body").to_equal({"name": "Test Item"})


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "OpenAPI schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/": {
                        "post": {
                            "parameters": [
                                {
                                    "name": "name",
                                    "in": "query",
                                    "required": True,
                                    "schema": {"title": "Name", "type": "string"},
                                }
                            ],
                            "summary": "Create Item",
                            "operationId": "create_item_items__post",
                            "responses": {
                                "201": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "422": {
                                    "description": "Validation Error",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/HTTPValidationError"
                                            }
                                        }
                                    },
                                },
                            },
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "ValidationError": {
                            "title": "ValidationError",
                            "required": ["loc", "msg", "type"],
                            "type": "object",
                            "properties": {
                                "loc": {
                                    "title": "Location",
                                    "type": "array",
                                    "items": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "integer"},
                                        ]
                                    },
                                },
                                "msg": {"title": "Message", "type": "string"},
                                "type": {"title": "Error Type", "type": "string"},
                                "input": {"title": "Input"},
                                "ctx": {"title": "Context", "type": "object"},
                            },
                        },
                        "HTTPValidationError": {
                            "title": "HTTPValidationError",
                            "type": "object",
                            "properties": {
                                "detail": {
                                    "title": "Detail",
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/ValidationError"
                                    },
                                }
                            },
                        },
                    }
                },
            }
        )
    )
