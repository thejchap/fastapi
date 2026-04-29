from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.exceptions import FastAPIDeprecationWarning
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ._shims import expect_warning


def get_client():
    app = FastAPI()
    with expect_warning(FastAPIDeprecationWarning):

        @app.get("/items/")
        async def read_items(
            q: Annotated[str | None, Query(regex="^fixedquery$")] = None,
        ):
            if q:
                return f"Hello {q}"
            else:
                return "Hello World"

    client = TestClient(app)
    return client


@test("Query regex param can be omitted")
def query_params_str_validations_no_query():
    client = get_client()
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("Hello World")


@test("Query regex param accepts matching value")
def query_params_str_validations_q_fixedquery():
    client = get_client()
    response = client.get("/items/", params={"q": "fixedquery"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("Hello fixedquery")


@test("Query regex param rejects non-matching value")
def query_params_str_validations_item_query_nonregexquery():
    client = get_client()
    response = client.get("/items/", params={"q": "nonregexquery"})
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "string_pattern_mismatch",
                    "loc": ["query", "q"],
                    "msg": "String should match pattern '^fixedquery$'",
                    "input": "nonregexquery",
                    "ctx": {"pattern": "^fixedquery$"},
                }
            ]
        }
    )


@test("OpenAPI schema documents Query regex param")
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
                        "get": {
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "parameters": [
                                {
                                    "name": "q",
                                    "in": "query",
                                    "required": False,
                                    "schema": {
                                        "anyOf": [
                                            {
                                                "type": "string",
                                                "pattern": "^fixedquery$",
                                            },
                                            {"type": "null"},
                                        ],
                                        "title": "Q",
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
