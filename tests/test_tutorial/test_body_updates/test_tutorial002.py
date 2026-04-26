from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("body_updates", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def get(name: str):
    client = _client_for(name)
    response = client.get("/items/baz")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "name": "Baz",
            "description": None,
            "price": 50.2,
            "tax": 10.5,
            "tags": [],
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def patch_all(name: str):
    client = _client_for(name)
    response = client.patch(
        "/items/foo",
        json={
            "name": "Fooz",
            "description": "Item description",
            "price": 3,
            "tax": 10.5,
            "tags": ["tag1", "tag2"],
        },
    )
    expect(response.json()).to_equal(
        {
            "name": "Fooz",
            "description": "Item description",
            "price": 3,
            "tax": 10.5,
            "tags": ["tag1", "tag2"],
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def patch_name(name: str):
    client = _client_for(name)
    response = client.patch(
        "/items/bar",
        json={"name": "Barz"},
    )
    expect(response.json()).to_equal(
        {
            "name": "Barz",
            "description": "The bartenders",
            "price": 62,
            "tax": 20.2,
            "tags": [],
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/{item_id}": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Item"
                                            }
                                        }
                                    },
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
                            "summary": "Read Item",
                            "operationId": "read_item_items__item_id__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Item Id", "type": "string"},
                                    "name": "item_id",
                                    "in": "path",
                                }
                            ],
                        },
                        "patch": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Item"
                                            }
                                        }
                                    },
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
                            "summary": "Update Item",
                            "operationId": "update_item_items__item_id__patch",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Item Id", "type": "string"},
                                    "name": "item_id",
                                    "in": "path",
                                }
                            ],
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    }
                                },
                                "required": True,
                            },
                        },
                    }
                },
                "components": {
                    "schemas": {
                        "Item": {
                            "type": "object",
                            "title": "Item",
                            "properties": {
                                "name": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Name",
                                },
                                "description": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Description",
                                },
                                "price": {
                                    "anyOf": [{"type": "number"}, {"type": "null"}],
                                    "title": "Price",
                                },
                                "tax": {
                                    "title": "Tax",
                                    "type": "number",
                                    "default": 10.5,
                                },
                                "tags": {
                                    "title": "Tags",
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "default": [],
                                },
                            },
                        },
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
