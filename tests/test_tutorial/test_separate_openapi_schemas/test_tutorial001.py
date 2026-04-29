from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("separate_openapi_schemas", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def create_item(name: str) -> None:
    client = _client_for(name)
    response = client.post("/items/", json={"name": "Foo"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "created item").to_equal(
        {"name": "Foo", "description": None}
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def read_items(name: str) -> None:
    client = _client_for(name)
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "items list").to_equal(
        [
            {
                "name": "Portal Gun",
                "description": "Device to travel through the multi-rick-verse",
            },
            {"name": "Plumbus", "description": None},
        ]
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def openapi_schema(name: str) -> None:
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
                        "get": {
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "items": {
                                                    "$ref": "#/components/schemas/Item"
                                                },
                                                "type": "array",
                                                "title": "Response Read Items Items  Get",
                                            }
                                        }
                                    },
                                }
                            },
                        },
                        "post": {
                            "summary": "Create Item",
                            "operationId": "create_item_items__post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    }
                                },
                                "required": True,
                            },
                            "responses": {
                                "200": {
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
                        },
                    }
                },
                "components": {
                    "schemas": {
                        "HTTPValidationError": {
                            "properties": {
                                "detail": {
                                    "items": {
                                        "$ref": "#/components/schemas/ValidationError"
                                    },
                                    "type": "array",
                                    "title": "Detail",
                                }
                            },
                            "type": "object",
                            "title": "HTTPValidationError",
                        },
                        "Item": {
                            "properties": {
                                "name": {"type": "string", "title": "Name"},
                                "description": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Description",
                                },
                            },
                            "type": "object",
                            "required": ["name"],
                            "title": "Item",
                        },
                        "ValidationError": {
                            "properties": {
                                "ctx": {"title": "Context", "type": "object"},
                                "input": {"title": "Input"},
                                "loc": {
                                    "items": {
                                        "anyOf": [
                                            {"type": "string"},
                                            {"type": "integer"},
                                        ]
                                    },
                                    "type": "array",
                                    "title": "Location",
                                },
                                "msg": {"type": "string", "title": "Message"},
                                "type": {"type": "string", "title": "Error Type"},
                            },
                            "type": "object",
                            "required": ["loc", "msg", "type"],
                            "title": "ValidationError",
                        },
                    }
                },
            }
        )
    )
