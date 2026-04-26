from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("query_params_str_validations", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial014_py310", name="tutorial014_py310"),
    test.case("tutorial014_an_py310", name="tutorial014_an_py310"),
)
def hidden_query(name: str):
    client = _client_for(name)
    response = client.get("/items?hidden_query=somevalue")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"hidden_query": "somevalue"})


@test.cases(
    test.case("tutorial014_py310", name="tutorial014_py310"),
    test.case("tutorial014_an_py310", name="tutorial014_an_py310"),
)
def no_hidden_query(name: str):
    client = _client_for(name)
    response = client.get("/items")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"hidden_query": "Not found"})


@test.cases(
    test.case("tutorial014_py310", name="tutorial014_py310"),
    test.case("tutorial014_an_py310", name="tutorial014_an_py310"),
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
                    "/items/": {
                        "get": {
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
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
                        }
                    }
                },
                "components": {
                    "schemas": {
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
