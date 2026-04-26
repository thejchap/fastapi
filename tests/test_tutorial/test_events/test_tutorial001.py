from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends, expect, fixture, test

from ..._shims import expect_warning


@fixture(per="file")
def app() -> FastAPI:
    with expect_warning(DeprecationWarning):
        from docs_src.events.tutorial001_py310 import app as _app
    return _app


@test
def events(app: FastAPI = Depends(app)):
    with TestClient(app) as client:
        response = client.get("/items/foo")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal({"name": "Fighters"})


@test
def openapi_schema(app: FastAPI = Depends(app)):
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal(
            snapshot(
                {
                    "openapi": "3.1.0",
                    "info": {"title": "FastAPI", "version": "0.1.0"},
                    "paths": {
                        "/items/{item_id}": {
                            "get": {
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
                                "summary": "Read Items",
                                "operationId": "read_items_items__item_id__get",
                                "parameters": [
                                    {
                                        "required": True,
                                        "schema": {
                                            "title": "Item Id",
                                            "type": "string",
                                        },
                                        "name": "item_id",
                                        "in": "path",
                                    }
                                ],
                            }
                        }
                    },
                    "components": {
                        "schemas": {
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
