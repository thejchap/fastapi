from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("header_param_models", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def header_param_model(name: str):
    client = _client_for(name)
    response = client.get(
        "/items/",
        headers=[
            ("save-data", "true"),
            ("if-modified-since", "yesterday"),
            ("traceparent", "123"),
            ("x-tag", "one"),
            ("x-tag", "two"),
        ],
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "host": "testserver",
            "save_data": True,
            "if_modified_since": "yesterday",
            "traceparent": "123",
            "x_tag": ["one", "two"],
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def header_param_model_defaults(name: str):
    client = _client_for(name)
    response = client.get("/items/", headers=[("save-data", "true")])
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "host": "testserver",
            "save_data": True,
            "if_modified_since": None,
            "traceparent": None,
            "x_tag": [],
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def header_param_model_invalid(name: str):
    client = _client_for(name)
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["header", "save_data"],
                        "msg": "Field required",
                        "input": {
                            "x_tag": [],
                            "host": "testserver",
                            "accept": "*/*",
                            "accept-encoding": "gzip, deflate",
                            "connection": "keep-alive",
                            "user-agent": "testclient",
                        },
                    }
                ]
            }
        )
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def header_param_model_extra(name: str):
    client = _client_for(name)
    response = client.get(
        "/items/", headers=[("save-data", "true"), ("tool", "plumbus")]
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "host": "testserver",
                "save_data": True,
                "if_modified_since": None,
                "traceparent": None,
                "x_tag": [],
            }
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
                                    "name": "host",
                                    "in": "header",
                                    "required": True,
                                    "schema": {"type": "string", "title": "Host"},
                                },
                                {
                                    "name": "save-data",
                                    "in": "header",
                                    "required": True,
                                    "schema": {"type": "boolean", "title": "Save Data"},
                                },
                                {
                                    "name": "if-modified-since",
                                    "in": "header",
                                    "required": False,
                                    "schema": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "If Modified Since",
                                    },
                                },
                                {
                                    "name": "traceparent",
                                    "in": "header",
                                    "required": False,
                                    "schema": {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "Traceparent",
                                    },
                                },
                                {
                                    "name": "x-tag",
                                    "in": "header",
                                    "required": False,
                                    "schema": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "default": [],
                                        "title": "X Tag",
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
