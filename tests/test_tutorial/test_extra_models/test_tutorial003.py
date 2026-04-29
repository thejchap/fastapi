from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("extra_models", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
)
def get_car(name: str):
    client = _client_for(name)
    response = client.get("/items/item1")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "description": "All my friends drive a low rider",
            "type": "car",
        }
    )


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
)
def get_plane(name: str):
    client = _client_for(name)
    response = client.get("/items/item2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "description": "Music is my aeroplane, it's my aeroplane",
            "type": "plane",
            "size": 5,
        }
    )


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
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
                                                "title": "Response Read Item Items  Item Id  Get",
                                                "anyOf": [
                                                    {
                                                        "$ref": "#/components/schemas/PlaneItem"
                                                    },
                                                    {
                                                        "$ref": "#/components/schemas/CarItem"
                                                    },
                                                ],
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
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "PlaneItem": {
                            "title": "PlaneItem",
                            "required": ["description", "size"],
                            "type": "object",
                            "properties": {
                                "description": {
                                    "title": "Description",
                                    "type": "string",
                                },
                                "type": {
                                    "title": "Type",
                                    "type": "string",
                                    "default": "plane",
                                },
                                "size": {"title": "Size", "type": "integer"},
                            },
                        },
                        "CarItem": {
                            "title": "CarItem",
                            "required": ["description"],
                            "type": "object",
                            "properties": {
                                "description": {
                                    "title": "Description",
                                    "type": "string",
                                },
                                "type": {
                                    "title": "Type",
                                    "type": "string",
                                    "default": "car",
                                },
                            },
                        },
                        "ValidationError": {
                            "title": "ValidationError",
                            "required": ["loc", "msg", "type"],
                            "type": "object",
                            "properties": {
                                "ctx": {"title": "Context", "type": "object"},
                                "input": {"title": "Input"},
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
