from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("query_params_str_validations", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial005_py310", name="tutorial005_py310"),
    test.case("tutorial005_an_py310", name="tutorial005_an_py310"),
)
def query_params_str_validations_no_query(name: str):
    client = _client_for(name)
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {
            "items": [{"item_id": "Foo"}, {"item_id": "Bar"}],
            "q": "fixedquery",
        }
    )


@test.cases(
    test.case("tutorial005_py310", name="tutorial005_py310"),
    test.case("tutorial005_an_py310", name="tutorial005_an_py310"),
)
def query_params_str_validations_q_query(name: str):
    client = _client_for(name)
    response = client.get("/items/", params={"q": "query"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {
            "items": [{"item_id": "Foo"}, {"item_id": "Bar"}],
            "q": "query",
        }
    )


@test.cases(
    test.case("tutorial005_py310", name="tutorial005_py310"),
    test.case("tutorial005_an_py310", name="tutorial005_an_py310"),
)
def query_params_str_validations_q_short(name: str):
    client = _client_for(name)
    response = client.get("/items/", params={"q": "fa"})
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "string_too_short",
                    "loc": ["query", "q"],
                    "msg": "String should have at least 3 characters",
                    "input": "fa",
                    "ctx": {"min_length": 3},
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial005_py310", name="tutorial005_py310"),
    test.case("tutorial005_an_py310", name="tutorial005_an_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
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
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "parameters": [
                                {
                                    "required": False,
                                    "schema": {
                                        "type": "string",
                                        "default": "fixedquery",
                                        "minLength": 3,
                                        "title": "Q",
                                    },
                                    "name": "q",
                                    "in": "query",
                                }
                            ],
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
