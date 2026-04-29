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
    test.case("tutorial003_py310", name="tutorial003_py310"),
)
def post_authors_item(name: str):
    client = _client_for(name)
    response = client.post(
        "/authors/foo/items/",
        json=[{"name": "Bar"}, {"name": "Baz", "description": "Drop the Baz"}],
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "name": "foo",
            "items": [
                {"name": "Bar", "description": None},
                {"name": "Baz", "description": "Drop the Baz"},
            ],
        }
    )


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
)
def get_authors(name: str):
    client = _client_for(name)
    response = client.get("/authors/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        [
            {
                "name": "Breaters",
                "items": [
                    {
                        "name": "Island In The Moon",
                        "description": "A place to be playin' and havin' fun",
                    },
                    {"name": "Holy Buddies", "description": None},
                ],
            },
            {
                "name": "System of an Up",
                "items": [
                    {
                        "name": "Salt",
                        "description": "The kombucha mushroom people's favorite",
                    },
                    {"name": "Pad Thai", "description": None},
                    {
                        "name": "Lonely Night",
                        "description": "The mostests lonliest nightiest of allest",
                    },
                ],
            },
        ]
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
                    "/authors/{author_id}/items/": {
                        "post": {
                            "summary": "Create Author Items",
                            "operationId": "create_author_items_authors__author_id__items__post",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Author Id", "type": "string"},
                                    "name": "author_id",
                                    "in": "path",
                                }
                            ],
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "title": "Items",
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/Item"
                                            },
                                        }
                                    }
                                },
                                "required": True,
                            },
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Author"
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
                        }
                    },
                    "/authors/": {
                        "get": {
                            "summary": "Get Authors",
                            "operationId": "get_authors_authors__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "title": "Response Get Authors Authors  Get",
                                                "type": "array",
                                                "items": {
                                                    "$ref": "#/components/schemas/Author"
                                                },
                                            }
                                        }
                                    },
                                }
                            },
                        }
                    },
                },
                "components": {
                    "schemas": {
                        "Author": {
                            "title": "Author",
                            "required": ["name"],
                            "type": "object",
                            "properties": {
                                "name": {"title": "Name", "type": "string"},
                                "items": {
                                    "title": "Items",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Item"},
                                },
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
                        "Item": {
                            "title": "Item",
                            "required": ["name"],
                            "type": "object",
                            "properties": {
                                "name": {"title": "Name", "type": "string"},
                                "description": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Description",
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
                    }
                },
            }
        )
    )
