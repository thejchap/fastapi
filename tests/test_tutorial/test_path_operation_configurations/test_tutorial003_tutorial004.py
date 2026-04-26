from textwrap import dedent

from dirty_equals import IsList
from fastapi.testclient import TestClient
from inline_snapshot import Is, snapshot
from tryke import expect, test

from ..._shims import import_tutorial

DESCRIPTIONS = {
    "tutorial003": "Create an item with all the information, name, description, price, tax and a set of unique tags",
    "tutorial004": dedent("""
        Create an item with all the information:

        - **name**: each item must have a name
        - **description**: a long description
        - **price**: required
        - **tax**: if the item doesn't have tax, you can omit this
        - **tags**: a set of unique tag strings for this item
    """).strip(),
}


def _client_for(mod_name: str) -> TestClient:
    mod = import_tutorial("path_operation_configuration", mod_name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial003_py310", mod_name="tutorial003_py310"),
    test.case("tutorial004_py310", mod_name="tutorial004_py310"),
)
def post_items(mod_name: str):
    client = _client_for(mod_name)
    response = client.post(
        "/items/",
        json={
            "name": "Foo",
            "description": "Item description",
            "price": 42.0,
            "tax": 3.2,
            "tags": ["bar", "baz"],
        },
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "name": "Foo",
            "description": "Item description",
            "price": 42.0,
            "tax": 3.2,
            "tags": IsList("bar", "baz", check_order=False),
        }
    )


@test.cases(
    test.case("tutorial003_py310", mod_name="tutorial003_py310"),
    test.case("tutorial004_py310", mod_name="tutorial004_py310"),
)
def openapi_schema(mod_name: str):
    client = _client_for(mod_name)
    short_name = mod_name[:11]

    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/": {
                        "post": {
                            "summary": "Create an item",
                            "description": Is(DESCRIPTIONS[short_name]),
                            "operationId": "create_item_items__post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    }
                                },
                                "required": True,
                            },
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/Item"
                                            }
                                        }
                                    },
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
                        },
                    },
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
                        "Item": {
                            "properties": {
                                "description": {
                                    "anyOf": [
                                        {
                                            "type": "string",
                                        },
                                        {
                                            "type": "null",
                                        },
                                    ],
                                    "title": "Description",
                                },
                                "name": {
                                    "title": "Name",
                                    "type": "string",
                                },
                                "price": {
                                    "title": "Price",
                                    "type": "number",
                                },
                                "tags": {
                                    "default": [],
                                    "items": {
                                        "type": "string",
                                    },
                                    "title": "Tags",
                                    "type": "array",
                                    "uniqueItems": True,
                                },
                                "tax": {
                                    "anyOf": [
                                        {
                                            "type": "number",
                                        },
                                        {
                                            "type": "null",
                                        },
                                    ],
                                    "title": "Tax",
                                },
                            },
                            "required": [
                                "name",
                                "price",
                            ],
                            "title": "Item",
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
