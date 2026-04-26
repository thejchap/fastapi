from dirty_equals import IsList
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("body_nested_models", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
)
def put_all(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/123",
        json={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
            "tags": ["foo", "bar", "foo"],
            "images": [
                {"url": "http://example.com/image.png", "name": "example image"}
            ],
        },
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "item_id": 123,
            "item": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
                "tags": IsList("foo", "bar", check_order=False),
                "images": [
                    {"url": "http://example.com/image.png", "name": "example image"}
                ],
            },
        }
    )


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
)
def put_only_required(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/5",
        json={"name": "Foo", "price": 35.4},
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "item_id": 5,
            "item": {
                "name": "Foo",
                "description": None,
                "price": 35.4,
                "tax": None,
                "tags": [],
                "images": None,
            },
        }
    )


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
)
def put_empty_body(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/5",
        json={},
    )
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "loc": ["body", "name"],
                    "input": {},
                    "msg": "Field required",
                    "type": "missing",
                },
                {
                    "loc": ["body", "price"],
                    "input": {},
                    "msg": "Field required",
                    "type": "missing",
                },
            ]
        }
    )


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
)
def put_images_not_list(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/5",
        json={
            "name": "Foo",
            "price": 35.4,
            "images": {"url": "http://example.com/image.png", "name": "example image"},
        },
    )
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "loc": ["body", "images"],
                    "input": {
                        "url": "http://example.com/image.png",
                        "name": "example image",
                    },
                    "msg": "Input should be a valid list",
                    "type": "list_type",
                },
            ]
        }
    )


@test.cases(
    test.case("tutorial006_py310", name="tutorial006_py310"),
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
                        "put": {
                            "parameters": [
                                {
                                    "in": "path",
                                    "name": "item_id",
                                    "required": True,
                                    "schema": {
                                        "title": "Item Id",
                                        "type": "integer",
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
                            "summary": "Update Item",
                            "operationId": "update_item_items__item_id__put",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Item",
                                        }
                                    }
                                },
                                "required": True,
                            },
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "Image": {
                            "properties": {
                                "url": {
                                    "title": "Url",
                                    "type": "string",
                                    "format": "uri",
                                    "maxLength": 2083,
                                    "minLength": 1,
                                },
                                "name": {
                                    "title": "Name",
                                    "type": "string",
                                },
                            },
                            "required": ["url", "name"],
                            "title": "Image",
                            "type": "object",
                        },
                        "Item": {
                            "properties": {
                                "name": {
                                    "title": "Name",
                                    "type": "string",
                                },
                                "description": {
                                    "title": "Description",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                                "price": {
                                    "title": "Price",
                                    "type": "number",
                                },
                                "tax": {
                                    "title": "Tax",
                                    "anyOf": [{"type": "number"}, {"type": "null"}],
                                },
                                "tags": {
                                    "title": "Tags",
                                    "default": [],
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "uniqueItems": True,
                                },
                                "images": {
                                    "anyOf": [
                                        {
                                            "items": {
                                                "$ref": "#/components/schemas/Image",
                                            },
                                            "type": "array",
                                        },
                                        {
                                            "type": "null",
                                        },
                                    ],
                                    "title": "Images",
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
