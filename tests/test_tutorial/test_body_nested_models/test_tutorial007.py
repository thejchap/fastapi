from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("body_nested_models", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
)
def post_all(name: str):
    client = _client_for(name)
    data = {
        "name": "Special Offer",
        "description": "This is a special offer",
        "price": 38.6,
        "items": [
            {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
                "tags": ["foo"],
                "images": [
                    {
                        "url": "http://example.com/image.png",
                        "name": "example image",
                    }
                ],
            }
        ],
    }

    response = client.post(
        "/offers/",
        json=data,
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(data)


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
)
def put_only_required(name: str):
    client = _client_for(name)
    response = client.post(
        "/offers/",
        json={
            "name": "Special Offer",
            "price": 38.6,
            "items": [
                {
                    "name": "Foo",
                    "price": 35.4,
                    "images": [
                        {
                            "url": "http://example.com/image.png",
                            "name": "example image",
                        }
                    ],
                }
            ],
        },
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "name": "Special Offer",
            "description": None,
            "price": 38.6,
            "items": [
                {
                    "name": "Foo",
                    "description": None,
                    "price": 35.4,
                    "tax": None,
                    "tags": [],
                    "images": [
                        {
                            "url": "http://example.com/image.png",
                            "name": "example image",
                        }
                    ],
                }
            ],
        }
    )


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
)
def put_empty_body(name: str):
    client = _client_for(name)
    response = client.post(
        "/offers/",
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
                {
                    "loc": ["body", "items"],
                    "input": {},
                    "msg": "Field required",
                    "type": "missing",
                },
            ]
        }
    )


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
)
def put_missing_required_in_items(name: str):
    client = _client_for(name)
    response = client.post(
        "/offers/",
        json={
            "name": "Special Offer",
            "price": 38.6,
            "items": [{}],
        },
    )
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "loc": ["body", "items", 0, "name"],
                    "input": {},
                    "msg": "Field required",
                    "type": "missing",
                },
                {
                    "loc": ["body", "items", 0, "price"],
                    "input": {},
                    "msg": "Field required",
                    "type": "missing",
                },
            ]
        }
    )


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
)
def put_missing_required_in_images(name: str):
    client = _client_for(name)
    response = client.post(
        "/offers/",
        json={
            "name": "Special Offer",
            "price": 38.6,
            "items": [
                {"name": "Foo", "price": 35.4, "images": [{}]},
            ],
        },
    )
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "loc": ["body", "items", 0, "images", 0, "url"],
                    "input": {},
                    "msg": "Field required",
                    "type": "missing",
                },
                {
                    "loc": ["body", "items", 0, "images", 0, "name"],
                    "input": {},
                    "msg": "Field required",
                    "type": "missing",
                },
            ]
        }
    )


@test.cases(
    test.case("tutorial007_py310", name="tutorial007_py310"),
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
                    "/offers/": {
                        "post": {
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
                            "summary": "Create Offer",
                            "operationId": "create_offer_offers__post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Offer",
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
                        "Offer": {
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
                                "items": {
                                    "title": "Items",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Item"},
                                },
                            },
                            "required": ["name", "price", "items"],
                            "title": "Offer",
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
