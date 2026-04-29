from decimal import Decimal

from dirty_equals import IsOneOf
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, condecimal
from tryke import expect, test

app = FastAPI()


class Item(BaseModel):
    name: str
    age: condecimal(gt=Decimal(0.0))  # type: ignore


@app.post("/items/")
def save_item_no_body(item: list[Item]):
    return {"item": item}


client = TestClient(app)


@test("List body of valid items is accepted")
def put_correct_body():
    response = client.post("/items/", json=[{"name": "Foo", "age": 5}])
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "item": [
                    {
                        "name": "Foo",
                        "age": "5",
                    }
                ]
            }
        )
    )


@test("Out-of-range decimal field returns a 422 with greater-than error")
def jsonable_encoder_requiring_error():
    response = client.post("/items/", json=[{"name": "Foo", "age": -1.0}])
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "greater_than",
                    "loc": ["body", 0, "age"],
                    "msg": "Input should be greater than 0",
                    "input": -1.0,
                    "ctx": {"gt": 0},
                }
            ]
        }
    )


@test("Multiple invalid items report errors for each list element")
def put_incorrect_body_multiple():
    response = client.post("/items/", json=[{"age": "five"}, {"age": "six"}])
    expect(response.status_code, "status code").to_equal(422).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", 0, "name"],
                    "msg": "Field required",
                    "input": {"age": "five"},
                },
                {
                    "type": "decimal_parsing",
                    "loc": ["body", 0, "age"],
                    "msg": "Input should be a valid decimal",
                    "input": "five",
                },
                {
                    "type": "missing",
                    "loc": ["body", 1, "name"],
                    "msg": "Field required",
                    "input": {"age": "six"},
                },
                {
                    "type": "decimal_parsing",
                    "loc": ["body", 1, "age"],
                    "msg": "Input should be a valid decimal",
                    "input": "six",
                },
            ]
        }
    )


@test("List body endpoint produces the expected OpenAPI schema")
def openapi_schema():
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
                            "summary": "Save Item No Body",
                            "operationId": "save_item_no_body_items__post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "title": "Item",
                                            "type": "array",
                                            "items": {
                                                "$ref": "#/components/schemas/Item"
                                            },
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
                        "Item": {
                            "title": "Item",
                            "required": ["name", "age"],
                            "type": "object",
                            "properties": {
                                "name": {"title": "Name", "type": "string"},
                                "age": {
                                    "title": "Age",
                                    "anyOf": [
                                        {"exclusiveMinimum": 0.0, "type": "number"},
                                        IsOneOf(
                                            # pydantic < 2.12.0
                                            {"type": "string"},
                                            # pydantic >= 2.12.0
                                            {
                                                "type": "string",
                                                "pattern": r"^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$",
                                            },
                                        ),
                                    ],
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
