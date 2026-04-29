from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("dataclasses_", name)
    client = TestClient(mod.app)
    client.headers.clear()
    return client


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def get_item(name: str):
    client = _client_for(name)
    response = client.get("/items/next")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "name": "Island In The Moon",
            "price": 12.99,
            "description": "A place to be playin' and havin' fun",
            "tags": ["breater"],
            "tax": None,
        }
    )


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
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
                    "/items/next": {
                        "get": {
                            "summary": "Read Next Item",
                            "operationId": "read_next_item_items_next_get",
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
                                }
                            },
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "Item": {
                            "title": "Item",
                            "required": ["name", "price"],
                            "type": "object",
                            "properties": {
                                "name": {"title": "Name", "type": "string"},
                                "price": {"title": "Price", "type": "number"},
                                "tags": {
                                    "title": "Tags",
                                    "type": "array",
                                    "items": {"type": "string"},
                                },
                                "description": {
                                    "title": "Description",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                                "tax": {
                                    "title": "Tax",
                                    "anyOf": [{"type": "number"}, {"type": "null"}],
                                },
                            },
                        }
                    }
                },
            }
        )
    )
