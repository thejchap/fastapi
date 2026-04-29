from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.exceptions import FastAPIDeprecationWarning
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ._shims import expect_warning


def get_client():
    app = FastAPI()
    with expect_warning(FastAPIDeprecationWarning):

        @app.post("/items/")
        async def read_items(
            q: Annotated[str | None, Form(regex="^fixedquery$")] = None,
        ):
            if q:
                return f"Hello {q}"
            else:
                return "Hello World"

    client = TestClient(app)
    return client


@test("Form regex param can be omitted")
def no_query():
    client = get_client()
    response = client.post("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("Hello World")


@test("Form regex param accepts matching value")
def q_fixedquery():
    client = get_client()
    response = client.post("/items/", data={"q": "fixedquery"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("Hello fixedquery")


@test("Form regex param rejects non-matching value")
def query_nonregexquery():
    client = get_client()
    response = client.post("/items/", data={"q": "nonregexquery"})
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "string_pattern_mismatch",
                    "loc": ["body", "q"],
                    "msg": "String should match pattern '^fixedquery$'",
                    "input": "nonregexquery",
                    "ctx": {"pattern": "^fixedquery$"},
                }
            ]
        }
    )


@test("OpenAPI schema documents Form regex param")
def openapi_schema():
    client = get_client()
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/": {
                        "post": {
                            "summary": "Read Items",
                            "operationId": "read_items_items__post",
                            "requestBody": {
                                "content": {
                                    "application/x-www-form-urlencoded": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Body_read_items_items__post"
                                        }
                                    }
                                }
                            },
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
                        "Body_read_items_items__post": {
                            "properties": {
                                "q": {
                                    "anyOf": [
                                        {"type": "string", "pattern": "^fixedquery$"},
                                        {"type": "null"},
                                    ],
                                    "title": "Q",
                                }
                            },
                            "type": "object",
                            "title": "Body_read_items_items__post",
                        },
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
