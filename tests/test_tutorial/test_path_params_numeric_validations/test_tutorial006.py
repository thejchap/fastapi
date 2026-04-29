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
        "tutorial006_py310 /items/0",
        name="tutorial006_py310",
        path="/items/0?q=&size=0.1",
        expected_response={"item_id": 0, "size": 0.1},
    ),
    test.case(
        "tutorial006_py310 /items/1000",
        name="tutorial006_py310",
        path="/items/1000?q=somequery&size=10.4",
        expected_response={"item_id": 1000, "q": "somequery", "size": 10.4},
    ),
    test.case(
        "tutorial006_an_py310 /items/0",
        name="tutorial006_an_py310",
        path="/items/0?q=&size=0.1",
        expected_response={"item_id": 0, "size": 0.1},
    ),
    test.case(
        "tutorial006_an_py310 /items/1000",
        name="tutorial006_an_py310",
        path="/items/1000?q=somequery&size=10.4",
        expected_response={"item_id": 1000, "q": "somequery", "size": 10.4},
    ),
)
def read_items(name: str, path: str, expected_response: dict):
    client = _client_for(name)
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(expected_response)


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
    test.case("tutorial006_an_py310", name="tutorial006_an_py310"),
)
def read_items_item_id_less_than_zero(name: str):
    client = _client_for(name)
    response = client.get("/items/-1?q=somequery&size=5")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "input": "-1",
                    "msg": "Input should be greater than or equal to 0",
                    "type": "greater_than_equal",
                    "ctx": {"ge": 0},
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
    test.case("tutorial006_an_py310", name="tutorial006_an_py310"),
)
def read_items_item_id_greater_than_one_thousand(name: str):
    client = _client_for(name)
    response = client.get("/items/1001?q=somequery&size=5")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "loc": ["path", "item_id"],
                    "input": "1001",
                    "msg": "Input should be less than or equal to 1000",
                    "type": "less_than_equal",
                    "ctx": {"le": 1000},
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
    test.case("tutorial006_an_py310", name="tutorial006_an_py310"),
)
def read_items_size_too_small(name: str):
    client = _client_for(name)
    response = client.get("/items/1?q=somequery&size=0.0")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "loc": ["query", "size"],
                    "input": "0.0",
                    "msg": "Input should be greater than 0",
                    "type": "greater_than",
                    "ctx": {"gt": 0.0},
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
    test.case("tutorial006_an_py310", name="tutorial006_an_py310"),
)
def read_items_size_too_large(name: str):
    client = _client_for(name)
    response = client.get("/items/1?q=somequery&size=10.5")
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "loc": ["query", "size"],
                    "input": "10.5",
                    "msg": "Input should be less than 10.5",
                    "type": "less_than",
                    "ctx": {"lt": 10.5},
                }
            ]
        }
    )


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
    test.case("tutorial006_an_py310", name="tutorial006_an_py310"),
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
                                        "minimum": 0,
                                        "maximum": 1000,
                                    },
                                    "name": "item_id",
                                    "in": "path",
                                },
                                {
                                    "required": True,
                                    "schema": {
                                        "type": "string",
                                        "title": "Q",
                                    },
                                    "name": "q",
                                    "in": "query",
                                },
                                {
                                    "in": "query",
                                    "name": "size",
                                    "required": True,
                                    "schema": {
                                        "exclusiveMaximum": 10.5,
                                        "exclusiveMinimum": 0,
                                        "title": "Size",
                                        "type": "number",
                                    },
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
