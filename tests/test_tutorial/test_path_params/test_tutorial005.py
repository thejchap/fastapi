from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.path_params.tutorial005_py310 import app

client = TestClient(app)


@test("GET /models/alexnet returns the alexnet response")
def get_enums_alexnet():
    response = client.get("/models/alexnet")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"model_name": "alexnet", "message": "Deep Learning FTW!"}
    )


@test("GET /models/lenet returns the lenet response")
def get_enums_lenet():
    response = client.get("/models/lenet")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"model_name": "lenet", "message": "LeCNN all the images"}
    )


@test("GET /models/resnet returns the resnet response")
def get_enums_resnet():
    response = client.get("/models/resnet")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"model_name": "resnet", "message": "Have some residuals"}
    )


@test("GET /models/{name} rejects an invalid enum value")
def get_enums_invalid():
    response = client.get("/models/foo")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "enum",
                    "loc": ["path", "model_name"],
                    "msg": "Input should be 'alexnet', 'resnet' or 'lenet'",
                    "input": "foo",
                    "ctx": {"expected": "'alexnet', 'resnet' or 'lenet'"},
                }
            ]
        }
    )


@test("OpenAPI schema matches the snapshot")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/models/{model_name}": {
                        "get": {
                            "summary": "Get Model",
                            "operationId": "get_model_models__model_name__get",
                            "parameters": [
                                {
                                    "required": True,
                                    "schema": {
                                        "$ref": "#/components/schemas/ModelName"
                                    },
                                    "name": "model_name",
                                    "in": "path",
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
                        "ModelName": {
                            "title": "ModelName",
                            "enum": ["alexnet", "resnet", "lenet"],
                            "type": "string",
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
                    }
                },
            }
        )
    )
