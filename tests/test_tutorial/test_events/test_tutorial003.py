from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.events.tutorial003_py310 import (
    app,
    fake_answer_to_everything_ml_model,
    ml_models,
)


@test("Lifespan loads ml_models on startup and clears them on shutdown")
def events():
    expect(ml_models, "ml_models state").to_be_falsy()
    with TestClient(app) as client:
        expect(ml_models["answer_to_everything"], "ml_models entry").to_equal(
            fake_answer_to_everything_ml_model
        )
        response = client.get("/predict", params={"x": 2})
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.json(), "response body").to_equal({"result": 84.0})
    expect(ml_models, "ml_models state").to_be_falsy()


@test("OpenAPI schema matches snapshot")
def openapi_schema():
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.json(), "response body").to_equal(
            snapshot(
                {
                    "openapi": "3.1.0",
                    "info": {"title": "FastAPI", "version": "0.1.0"},
                    "paths": {
                        "/predict": {
                            "get": {
                                "summary": "Predict",
                                "operationId": "predict_predict_get",
                                "parameters": [
                                    {
                                        "required": True,
                                        "schema": {"title": "X", "type": "number"},
                                        "name": "x",
                                        "in": "query",
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
                            "ValidationError": {
                                "title": "ValidationError",
                                "required": ["loc", "msg", "type"],
                                "type": "object",
                                "properties": {
                                    "ctx": {"title": "Context", "type": "object"},
                                    "input": {"title": "Input"},
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
                                },
                            },
                        }
                    },
                }
            )
        )
