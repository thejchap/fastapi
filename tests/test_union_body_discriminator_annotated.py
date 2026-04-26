# Ref: https://github.com/fastapi/fastapi/discussions/14495

from typing import Annotated

from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel
from tryke import Depends, expect, fixture, test


@fixture
def client() -> TestClient:
    from fastapi import Body
    from pydantic import Discriminator, Tag

    class Cat(BaseModel):
        pet_type: str = "cat"
        meows: int

    class Dog(BaseModel):
        pet_type: str = "dog"
        barks: float

    def get_pet_type(v):
        assert isinstance(v, dict)
        return v.get("pet_type", "")

    Pet = Annotated[
        Annotated[Cat, Tag("cat")] | Annotated[Dog, Tag("dog")],
        Discriminator(get_pet_type),
    ]

    app = FastAPI()

    @app.post("/pet/assignment")
    async def create_pet_assignment(pet: Pet = Body()):
        return pet

    @app.post("/pet/annotated")
    async def create_pet_annotated(pet: Annotated[Pet, Body()]):
        return pet

    return TestClient(app)


@test
def union_body_discriminator_assignment(client: TestClient = Depends(client)) -> None:
    response = client.post("/pet/assignment", json={"pet_type": "cat", "meows": 5})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"pet_type": "cat", "meows": 5})


@test
def union_body_discriminator_annotated(client: TestClient = Depends(client)) -> None:
    response = client.post("/pet/annotated", json={"pet_type": "dog", "barks": 3.5})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"pet_type": "dog", "barks": 3.5})


@test
def openapi_schema(client: TestClient = Depends(client)) -> None:
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/pet/assignment": {
                        "post": {
                            "summary": "Create Pet Assignment",
                            "operationId": "create_pet_assignment_pet_assignment_post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "anyOf": [
                                                {"$ref": "#/components/schemas/Cat"},
                                                {"$ref": "#/components/schemas/Dog"},
                                            ],
                                            "title": "Pet",
                                        }
                                    }
                                },
                                "required": True,
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
                    },
                    "/pet/annotated": {
                        "post": {
                            "summary": "Create Pet Annotated",
                            "operationId": "create_pet_annotated_pet_annotated_post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "oneOf": [
                                                {"$ref": "#/components/schemas/Cat"},
                                                {"$ref": "#/components/schemas/Dog"},
                                            ],
                                            "title": "Pet",
                                        }
                                    }
                                },
                                "required": True,
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
                    },
                },
                "components": {
                    "schemas": {
                        "Cat": {
                            "properties": {
                                "pet_type": {
                                    "type": "string",
                                    "title": "Pet Type",
                                    "default": "cat",
                                },
                                "meows": {"type": "integer", "title": "Meows"},
                            },
                            "type": "object",
                            "required": ["meows"],
                            "title": "Cat",
                        },
                        "Dog": {
                            "properties": {
                                "pet_type": {
                                    "type": "string",
                                    "title": "Pet Type",
                                    "default": "dog",
                                },
                                "barks": {"type": "number", "title": "Barks"},
                            },
                            "type": "object",
                            "required": ["barks"],
                            "title": "Dog",
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
