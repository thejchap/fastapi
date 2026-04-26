from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("query_params", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case(
        "tutorial001_py310 /items/",
        name="tutorial001_py310",
        path="/items/",
        expected_json=[
            {"item_name": "Foo"},
            {"item_name": "Bar"},
            {"item_name": "Baz"},
        ],
    ),
    test.case(
        "tutorial001_py310 /items/?skip=1",
        name="tutorial001_py310",
        path="/items/?skip=1",
        expected_json=[{"item_name": "Bar"}, {"item_name": "Baz"}],
    ),
    test.case(
        "tutorial001_py310 /items/?skip=1&limit=1",
        name="tutorial001_py310",
        path="/items/?skip=1&limit=1",
        expected_json=[{"item_name": "Bar"}],
    ),
)
def read_user_item(name: str, path: str, expected_json: list):
    client = _client_for(name)
    response = client.get(path)
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal(expected_json)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/": {
                        "get": {
                            "summary": "Read Item",
                            "operationId": "read_item_items__get",
                            "parameters": [
                                {
                                    "required": False,
                                    "schema": {
                                        "title": "Skip",
                                        "type": "integer",
                                        "default": 0,
                                    },
                                    "name": "skip",
                                    "in": "query",
                                },
                                {
                                    "required": False,
                                    "schema": {
                                        "title": "Limit",
                                        "type": "integer",
                                        "default": 10,
                                    },
                                    "name": "limit",
                                    "in": "query",
                                },
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "422": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/HTTPValidationError",
                                            },
                                        },
                                    },
                                    "description": "Validation Error",
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
