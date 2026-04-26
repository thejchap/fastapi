from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("dependencies", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case(
        "tutorial011_py310 /query-checker/",
        name="tutorial011_py310",
        path="/query-checker/",
        expected_status=200,
        expected_response={"fixed_content_in_query": False},
    ),
    test.case(
        "tutorial011_py310 /query-checker/?q=qwerty",
        name="tutorial011_py310",
        path="/query-checker/?q=qwerty",
        expected_status=200,
        expected_response={"fixed_content_in_query": False},
    ),
    test.case(
        "tutorial011_py310 /query-checker/?q=foobar",
        name="tutorial011_py310",
        path="/query-checker/?q=foobar",
        expected_status=200,
        expected_response={"fixed_content_in_query": True},
    ),
    test.case(
        "tutorial011_an_py310 /query-checker/",
        name="tutorial011_an_py310",
        path="/query-checker/",
        expected_status=200,
        expected_response={"fixed_content_in_query": False},
    ),
    test.case(
        "tutorial011_an_py310 /query-checker/?q=qwerty",
        name="tutorial011_an_py310",
        path="/query-checker/?q=qwerty",
        expected_status=200,
        expected_response={"fixed_content_in_query": False},
    ),
    test.case(
        "tutorial011_an_py310 /query-checker/?q=foobar",
        name="tutorial011_an_py310",
        path="/query-checker/?q=foobar",
        expected_status=200,
        expected_response={"fixed_content_in_query": True},
    ),
)
def get(name: str, path: str, expected_status: int, expected_response: dict):
    client = _client_for(name)
    response = client.get(path)
    expect(response.status_code).to_equal(expected_status)
    expect(response.json()).to_equal(expected_response)


@test.cases(
    test.case("tutorial011_py310", name="tutorial011_py310"),
    test.case("tutorial011_an_py310", name="tutorial011_an_py310"),
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
                    "/query-checker/": {
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
                            "summary": "Read Query Check",
                            "operationId": "read_query_check_query_checker__get",
                            "parameters": [
                                {
                                    "required": False,
                                    "schema": {
                                        "type": "string",
                                        "default": "",
                                        "title": "Q",
                                    },
                                    "name": "q",
                                    "in": "query",
                                },
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
