from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("header_params", name)
    return TestClient(mod.app)


@test.cases(
    test.case(
        "py310 default",
        name="tutorial003_py310",
        path="/items",
        headers=None,
        expected_status=200,
        expected_response={"X-Token values": None},
    ),
    test.case(
        "py310 single",
        name="tutorial003_py310",
        path="/items",
        headers={"x-token": "foo"},
        expected_status=200,
        expected_response={"X-Token values": ["foo"]},
    ),
    test.case(
        "py310 multi",
        name="tutorial003_py310",
        path="/items",
        headers=[("x-token", "foo"), ("x-token", "bar")],
        expected_status=200,
        expected_response={"X-Token values": ["foo", "bar"]},
    ),
    test.case(
        "an_py310 default",
        name="tutorial003_an_py310",
        path="/items",
        headers=None,
        expected_status=200,
        expected_response={"X-Token values": None},
    ),
    test.case(
        "an_py310 single",
        name="tutorial003_an_py310",
        path="/items",
        headers={"x-token": "foo"},
        expected_status=200,
        expected_response={"X-Token values": ["foo"]},
    ),
    test.case(
        "an_py310 multi",
        name="tutorial003_an_py310",
        path="/items",
        headers=[("x-token", "foo"), ("x-token", "bar")],
        expected_status=200,
        expected_response={"X-Token values": ["foo", "bar"]},
    ),
)
def get_items(
    name: str, path: str, headers, expected_status: int, expected_response: dict
):
    client = _client_for(name)
    response = client.get(path, headers=headers)
    expect(response.status_code, "status code").to_equal(expected_status).fatal()
    expect(response.json(), "response body").to_equal(expected_response)


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
    test.case("tutorial003_an_py310", name="tutorial003_an_py310"),
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
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "parameters": [
                                {
                                    "required": False,
                                    "schema": {
                                        "title": "X-Token",
                                        "anyOf": [
                                            {
                                                "type": "array",
                                                "items": {"type": "string"},
                                            },
                                            {"type": "null"},
                                        ],
                                    },
                                    "name": "x-token",
                                    "in": "header",
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
