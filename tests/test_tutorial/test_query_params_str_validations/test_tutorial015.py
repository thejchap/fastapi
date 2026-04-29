from dirty_equals import IsStr
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("query_params_str_validations", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial015_an_py310", name="tutorial015_an_py310"),
)
def get_random_item(name: str):
    client = _client_for(name)
    response = client.get("/items")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"id": IsStr(), "name": IsStr()})


@test.cases(
    test.case("tutorial015_an_py310", name="tutorial015_an_py310"),
)
def get_item(name: str):
    client = _client_for(name)
    response = client.get("/items?id=isbn-9781529046137")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "id": "isbn-9781529046137",
            "name": "The Hitchhiker's Guide to the Galaxy",
        }
    )


@test.cases(
    test.case("tutorial015_an_py310", name="tutorial015_an_py310"),
)
def get_item_does_not_exist(name: str):
    client = _client_for(name)
    response = client.get("/items?id=isbn-nope")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"id": "isbn-nope", "name": None})


@test.cases(
    test.case("tutorial015_an_py310", name="tutorial015_an_py310"),
)
def get_invalid_item(name: str):
    client = _client_for(name)
    response = client.get("/items?id=wtf-yes")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "detail": [
                    {
                        "type": "value_error",
                        "loc": ["query", "id"],
                        "msg": 'Value error, Invalid ID format, it must start with "isbn-" or "imdb-"',
                        "input": "wtf-yes",
                        "ctx": {"error": {}},
                    }
                ]
            }
        )
    )


@test.cases(
    test.case("tutorial015_an_py310", name="tutorial015_an_py310"),
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
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "parameters": [
                                {
                                    "name": "id",
                                    "in": "query",
                                    "required": False,
                                    "schema": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "Id",
                                    },
                                }
                            ],
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
