from unittest.mock import patch

from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends, expect, fixture, test

from docs_src.body.tutorial001_py310 import app


@fixture
def client() -> TestClient:
    return TestClient(app)


@test
def body_float(client: TestClient = Depends(client)):
    response = client.post("/items/", json={"name": "Foo", "price": 50.5})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "name": "Foo",
            "price": 50.5,
            "description": None,
            "tax": None,
        }
    )


@test
def post_with_str_float(client: TestClient = Depends(client)):
    response = client.post("/items/", json={"name": "Foo", "price": "50.5"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "name": "Foo",
            "price": 50.5,
            "description": None,
            "tax": None,
        }
    )


@test
def post_with_str_float_description(client: TestClient = Depends(client)):
    response = client.post(
        "/items/", json={"name": "Foo", "price": "50.5", "description": "Some Foo"}
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "name": "Foo",
            "price": 50.5,
            "description": "Some Foo",
            "tax": None,
        }
    )


@test
def post_with_str_float_description_tax(client: TestClient = Depends(client)):
    response = client.post(
        "/items/",
        json={"name": "Foo", "price": "50.5", "description": "Some Foo", "tax": 0.3},
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "name": "Foo",
            "price": 50.5,
            "description": "Some Foo",
            "tax": 0.3,
        }
    )


@test
def post_with_only_name(client: TestClient = Depends(client)):
    response = client.post("/items/", json={"name": "Foo"})
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "price"],
                    "msg": "Field required",
                    "input": {"name": "Foo"},
                }
            ]
        }
    )


@test
def post_with_only_name_price(client: TestClient = Depends(client)):
    response = client.post("/items/", json={"name": "Foo", "price": "twenty"})
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "float_parsing",
                    "loc": ["body", "price"],
                    "msg": "Input should be a valid number, unable to parse string as a number",
                    "input": "twenty",
                }
            ]
        }
    )


@test
def post_with_no_data(client: TestClient = Depends(client)):
    response = client.post("/items/", json={})
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "name"],
                    "msg": "Field required",
                    "input": {},
                },
                {
                    "type": "missing",
                    "loc": ["body", "price"],
                    "msg": "Field required",
                    "input": {},
                },
            ]
        }
    )


@test
def post_with_none(client: TestClient = Depends(client)):
    response = client.post("/items/", json=None)
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test
def post_broken_body(client: TestClient = Depends(client)):
    response = client.post(
        "/items/",
        headers={"content-type": "application/json"},
        content="{some broken json}",
    )
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "json_invalid",
                    "loc": ["body", 1],
                    "msg": "JSON decode error",
                    "input": {},
                    "ctx": {
                        "error": "Expecting property name enclosed in double quotes"
                    },
                }
            ]
        }
    )


@test
def post_form_for_json(client: TestClient = Depends(client)):
    response = client.post("/items/", data={"name": "Foo", "price": 50.5})
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "model_attributes_type",
                    "loc": ["body"],
                    "msg": "Input should be a valid dictionary or object to extract fields from",
                    "input": "name=Foo&price=50.5",
                }
            ]
        }
    )


@test
def explicit_content_type(client: TestClient = Depends(client)):
    response = client.post(
        "/items/",
        content='{"name": "Foo", "price": 50.5}',
        headers={"Content-Type": "application/json"},
    )
    expect(response.status_code).to_equal(200)


@test
def geo_json(client: TestClient = Depends(client)):
    response = client.post(
        "/items/",
        content='{"name": "Foo", "price": 50.5}',
        headers={"Content-Type": "application/geo+json"},
    )
    expect(response.status_code).to_equal(200)


@test
def no_content_type_json(client: TestClient = Depends(client)):
    response = client.post(
        "/items/",
        content='{"name": "Foo", "price": 50.5}',
    )
    expect(response.status_code).to_equal(422)


@test
def wrong_headers(client: TestClient = Depends(client)):
    data = '{"name": "Foo", "price": 50.5}'
    response = client.post(
        "/items/", content=data, headers={"Content-Type": "text/plain"}
    )
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "model_attributes_type",
                    "loc": ["body"],
                    "msg": "Input should be a valid dictionary or object to extract fields from",
                    "input": '{"name": "Foo", "price": 50.5}',
                }
            ]
        }
    )

    response = client.post(
        "/items/", content=data, headers={"Content-Type": "application/geo+json-seq"}
    )
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "model_attributes_type",
                    "loc": ["body"],
                    "msg": "Input should be a valid dictionary or object to extract fields from",
                    "input": '{"name": "Foo", "price": 50.5}',
                }
            ]
        }
    )

    response = client.post(
        "/items/", content=data, headers={"Content-Type": "application/not-really-json"}
    )
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "type": "model_attributes_type",
                    "loc": ["body"],
                    "msg": "Input should be a valid dictionary or object to extract fields from",
                    "input": '{"name": "Foo", "price": 50.5}',
                }
            ]
        }
    )


@test
def other_exceptions(client: TestClient = Depends(client)):
    with patch("json.loads", side_effect=Exception):
        response = client.post("/items/", json={"test": "test2"})
        expect(response.status_code).to_equal(400)


@test
def openapi_schema(client: TestClient = Depends(client)):
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
                            "summary": "Create Item",
                            "operationId": "create_item_items__post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    }
                                },
                                "required": True,
                            },
                        }
                    }
                },
                "components": {
                    "schemas": {
                        "Item": {
                            "title": "Item",
                            "required": ["name", "price"],
                            "type": "object",
                            "properties": {
                                "name": {"title": "Name", "type": "string"},
                                "price": {"title": "Price", "type": "number"},
                                "description": {
                                    "title": "Description",
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                },
                                "tax": {
                                    "title": "Tax",
                                    "anyOf": [{"type": "number"}, {"type": "null"}],
                                },
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
