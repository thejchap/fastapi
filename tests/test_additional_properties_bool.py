from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, ConfigDict
from tryke import expect, test


class FooBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Foo(FooBaseModel):
    pass


app = FastAPI()


@app.post("/")
async def post(
    foo: Foo | None = None,
):
    return foo


client = TestClient(app)


@test
def call_invalid():
    response = client.post("/", json={"foo": {"bar": "baz"}})
    expect(response.status_code).to_equal(422)


@test
def call_valid():
    response = client.post("/", json={})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({})


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
                    "/": {
                        "post": {
                            "summary": "Post",
                            "operationId": "post__post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "anyOf": [
                                                {"$ref": "#/components/schemas/Foo"},
                                                {"type": "null"},
                                            ],
                                            "title": "Foo",
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
                        "Foo": {
                            "properties": {},
                            "additionalProperties": False,
                            "type": "object",
                            "title": "Foo",
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
