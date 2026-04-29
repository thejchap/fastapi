from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("body_nested_models", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial009_py310", name="tutorial009_py310"),
)
def post_body(name: str):
    client = _client_for(name)
    data = {"2": 2.2, "3": 3.3}
    response = client.post("/index-weights/", json=data)
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(data)


@test.cases(
    test.case("tutorial009_py310", name="tutorial009_py310"),
)
def post_invalid_body(name: str):
    client = _client_for(name)
    data = {"foo": 2.2, "3": 3.3}
    response = client.post("/index-weights/", json=data)
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "int_parsing",
                    "loc": ["body", "foo", "[key]"],
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "input": "foo",
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial009_py310", name="tutorial009_py310"),
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
                    "/index-weights/": {
                        "post": {
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
                            "summary": "Create Index Weights",
                            "operationId": "create_index_weights_index_weights__post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "title": "Weights",
                                            "type": "object",
                                            "additionalProperties": {"type": "number"},
                                        }
                                    }
                                },
                                "required": True,
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
