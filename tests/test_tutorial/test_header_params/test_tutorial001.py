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
        name="tutorial001_py310",
        path="/items",
        headers=None,
        expected_status=200,
        expected_response={"User-Agent": "testclient"},
    ),
    test.case(
        "py310 invalid header",
        name="tutorial001_py310",
        path="/items",
        headers={"X-Header": "notvalid"},
        expected_status=200,
        expected_response={"User-Agent": "testclient"},
    ),
    test.case(
        "py310 ua header",
        name="tutorial001_py310",
        path="/items",
        headers={"User-Agent": "FastAPI test"},
        expected_status=200,
        expected_response={"User-Agent": "FastAPI test"},
    ),
    test.case(
        "an_py310 default",
        name="tutorial001_an_py310",
        path="/items",
        headers=None,
        expected_status=200,
        expected_response={"User-Agent": "testclient"},
    ),
    test.case(
        "an_py310 invalid header",
        name="tutorial001_an_py310",
        path="/items",
        headers={"X-Header": "notvalid"},
        expected_status=200,
        expected_response={"User-Agent": "testclient"},
    ),
    test.case(
        "an_py310 ua header",
        name="tutorial001_an_py310",
        path="/items",
        headers={"User-Agent": "FastAPI test"},
        expected_status=200,
        expected_response={"User-Agent": "FastAPI test"},
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
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
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
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "User-Agent",
                                    },
                                    "name": "user-agent",
                                    "in": "header",
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
