from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("path_params_numeric_validations", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case(
        "tutorial001_py310 /items/42",
        name="tutorial001_py310",
        path="/items/42",
        expected_response={"item_id": 42},
    ),
    test.case(
        "tutorial001_py310 /items/123?q",
        name="tutorial001_py310",
        path="/items/123?item-query=somequery",
        expected_response={"item_id": 123, "q": "somequery"},
    ),
    test.case(
        "tutorial001_an_py310 /items/42",
        name="tutorial001_an_py310",
        path="/items/42",
        expected_response={"item_id": 42},
    ),
    test.case(
        "tutorial001_an_py310 /items/123?q",
        name="tutorial001_an_py310",
        path="/items/123?item-query=somequery",
        expected_response={"item_id": 123, "q": "somequery"},
    ),
)
def read_items(name: str, path: str, expected_response: dict):
    client = _client_for(name)
    response = client.get(path)
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(expected_response)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def read_items_invalid_item_id(name: str):
    client = _client_for(name)
    response = client.get("/items/invalid_id")
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "input": "invalid_id",
                    "msg": "Input should be a valid integer, unable to parse string as an integer",
                    "type": "int_parsing",
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
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
                    "/items/{item_id}": {
                        "get": {
                            "summary": "Read Items",
                            "operationId": "read_items_items__item_id__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {
                                        "title": "The ID of the item to get",
                                        "type": "integer",
                                    },
                                    "name": "item_id",
                                    "in": "path",
                                },
                                {
                                    "required": False,
                                    "schema": {
                                        "anyOf": [
                                            {
                                                "type": "string",
                                            },
                                            {
                                                "type": "null",
                                            },
                                        ],
                                        "title": "Item-Query",
                                    },
                                    "name": "item-query",
                                    "in": "query",
                                },
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {},
                                        }
                                    },
                                },
                                "422": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/HTTPValidationError",
                                            },
                                        },
                                    },
                                    "description": "Validation Error",
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
                                        "$ref": "#/components/schemas/ValidationError",
                                    },
                                    "title": "Detail",
                                    "type": "array",
                                },
                            },
                            "title": "HTTPValidationError",
                            "type": "object",
                        },
                        "ValidationError": {
                            "properties": {
                                "ctx": {"title": "Context", "type": "object"},
                                "input": {"title": "Input"},
                                "loc": {
                                    "items": {
                                        "anyOf": [
                                            {
                                                "type": "string",
                                            },
                                            {
                                                "type": "integer",
                                            },
                                        ],
                                    },
                                    "title": "Location",
                                    "type": "array",
                                },
                                "msg": {
                                    "title": "Message",
                                    "type": "string",
                                },
                                "type": {
                                    "title": "Error Type",
                                    "type": "string",
                                },
                            },
                            "required": [
                                "loc",
                                "msg",
                                "type",
                            ],
                            "title": "ValidationError",
                            "type": "object",
                        },
                    },
                },
            }
        )
    )
