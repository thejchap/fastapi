from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("cookie_param_models", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def cookie_param_model(name: str):
    client = _client_for(name)
    with client as c:
        c.cookies.set("session_id", "123")
        c.cookies.set("fatebook_tracker", "456")
        c.cookies.set("googall_tracker", "789")
        response = c.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "session_id": "123",
            "fatebook_tracker": "456",
            "googall_tracker": "789",
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def cookie_param_model_defaults(name: str):
    client = _client_for(name)
    with client as c:
        c.cookies.set("session_id", "123")
        response = c.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "session_id": "123",
            "fatebook_tracker": None,
            "googall_tracker": None,
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def cookie_param_model_invalid(name: str):
    client = _client_for(name)
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["cookie", "session_id"],
                        "msg": "Field required",
                        "input": {},
                    }
                ]
            }
        )
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def cookie_param_model_extra(name: str):
    client = _client_for(name)
    with client as c:
        c.cookies.set("session_id", "123")
        c.cookies.set("extra", "track-me-here-too")
        response = c.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {"session_id": "123", "fatebook_tracker": None, "googall_tracker": None}
        )
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
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
                                    "name": "session_id",
                                    "in": "cookie",
                                    "required": True,
                                    "schema": {"type": "string", "title": "Session Id"},
                                },
                                {
                                    "name": "fatebook_tracker",
                                    "in": "cookie",
                                    "required": False,
                                    "schema": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "Fatebook Tracker",
                                    },
                                },
                                {
                                    "name": "googall_tracker",
                                    "in": "cookie",
                                    "required": False,
                                    "schema": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "Googall Tracker",
                                    },
                                },
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
