from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("extra_models", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
)
def get_items(name: str):
    client = _client_for(name)
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        [
            {"name": "Foo", "description": "There comes my hero"},
            {"name": "Red", "description": "It's my aeroplane"},
        ]
    )


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
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
                    "/items/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "title": "Response Read Items Items  Get",
                                                "type": "array",
                                                "items": {
                                                    "$ref": "#/components/schemas/Item"
                                                },
                                            }
                                        }
                                    },
                                }
                            },
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "Item": {
                            "title": "Item",
                            "required": ["name", "description"],
                            "type": "object",
                            "properties": {
                                "name": {"title": "Name", "type": "string"},
                                "description": {
                                    "title": "Description",
                                    "type": "string",
                                },
                            },
                        }
                    }
                },
            }
        )
    )
