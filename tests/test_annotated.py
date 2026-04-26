from typing import Annotated

from fastapi import APIRouter, FastAPI, Query
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()


@app.get("/default")
async def default(foo: Annotated[str, Query()] = "foo"):
    return {"foo": foo}


@app.get("/required")
async def required(foo: Annotated[str, Query(min_length=1)]):
    return {"foo": foo}


@app.get("/multiple")
async def multiple(foo: Annotated[str, object(), Query(min_length=1)]):
    return {"foo": foo}


@app.get("/unrelated")
async def unrelated(foo: Annotated[str, object()]):
    return {"foo": foo}


client = TestClient(app)

foo_is_missing = {
    "detail": [
        {
            "loc": ["query", "foo"],
            "msg": "Field required",
            "type": "missing",
            "input": None,
        }
    ]
}
foo_is_short = {
    "detail": [
        {
            "ctx": {"min_length": 1},
            "loc": ["query", "foo"],
            "msg": "String should have at least 1 character",
            "type": "string_too_short",
            "input": "",
        }
    ]
}


@test.cases(
    test.case(
        "default",
        path="/default",
        expected_status=200,
        expected_response={"foo": "foo"},
    ),
    test.case(
        "default with foo",
        path="/default?foo=bar",
        expected_status=200,
        expected_response={"foo": "bar"},
    ),
    test.case(
        "required with foo",
        path="/required?foo=bar",
        expected_status=200,
        expected_response={"foo": "bar"},
    ),
    test.case(
        "required missing",
        path="/required",
        expected_status=422,
        expected_response=foo_is_missing,
    ),
    test.case(
        "required empty",
        path="/required?foo=",
        expected_status=422,
        expected_response=foo_is_short,
    ),
    test.case(
        "multiple with foo",
        path="/multiple?foo=bar",
        expected_status=200,
        expected_response={"foo": "bar"},
    ),
    test.case(
        "multiple missing",
        path="/multiple",
        expected_status=422,
        expected_response=foo_is_missing,
    ),
    test.case(
        "multiple empty",
        path="/multiple?foo=",
        expected_status=422,
        expected_response=foo_is_short,
    ),
    test.case(
        "unrelated with foo",
        path="/unrelated?foo=bar",
        expected_status=200,
        expected_response={"foo": "bar"},
    ),
    test.case(
        "unrelated missing",
        path="/unrelated",
        expected_status=422,
        expected_response=foo_is_missing,
    ),
)
def get(path: str, expected_status: int, expected_response: dict):
    response = client.get(path)
    expect(response.status_code).to_equal(expected_status)
    expect(response.json()).to_equal(expected_response)


@test
def multiple_path():
    app = FastAPI()

    @app.get("/test1")
    @app.get("/test2")
    async def test_route(var: Annotated[str, Query()] = "bar"):
        return {"foo": var}

    client = TestClient(app)
    response = client.get("/test1")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"foo": "bar"})

    response = client.get("/test1", params={"var": "baz"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"foo": "baz"})

    response = client.get("/test2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"foo": "bar"})

    response = client.get("/test2", params={"var": "baz"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"foo": "baz"})


@test
def nested_router():
    app = FastAPI()

    router = APIRouter(prefix="/nested")

    @router.get("/test")
    async def test_route(var: Annotated[str, Query()] = "bar"):
        return {"foo": var}

    app.include_router(router)

    client = TestClient(app)

    response = client.get("/nested/test")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"foo": "bar"})


@test
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/default": {
                        "get": {
                            "summary": "Default",
                            "operationId": "default_default_get",
                            "parameters": [
                                {
                                    "required": False,
                                    "schema": {
                                        "title": "Foo",
                                        "type": "string",
                                        "default": "foo",
                                    },
                                    "name": "foo",
                                    "in": "query",
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
                    },
                    "/required": {
                        "get": {
                            "summary": "Required",
                            "operationId": "required_required_get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {
                                        "title": "Foo",
                                        "minLength": 1,
                                        "type": "string",
                                    },
                                    "name": "foo",
                                    "in": "query",
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
                    },
                    "/multiple": {
                        "get": {
                            "summary": "Multiple",
                            "operationId": "multiple_multiple_get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {
                                        "title": "Foo",
                                        "minLength": 1,
                                        "type": "string",
                                    },
                                    "name": "foo",
                                    "in": "query",
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
                    },
                    "/unrelated": {
                        "get": {
                            "summary": "Unrelated",
                            "operationId": "unrelated_unrelated_get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {"title": "Foo", "type": "string"},
                                    "name": "foo",
                                    "in": "query",
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
                    },
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
