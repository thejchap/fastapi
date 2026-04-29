from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.path_params.tutorial001_py310 import app

client = TestClient(app)


@test.cases(
    test.case("integer id", item_id=1, expected_response={"item_id": "1"}),
    test.case("string id", item_id="alice", expected_response={"item_id": "alice"}),
)
def get_items(item_id, expected_response):
    response = client.get(f"/items/{item_id}")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(expected_response)


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
                    "/items/{item_id}": {
                        "get": {
                            "operationId": "read_item_items__item_id__get",
                            "parameters": [
                                {
                                    "in": "path",
                                    "name": "item_id",
                                    "required": True,
                                    "schema": {
                                        "title": "Item Id",
                                    },
                                },
                            ],
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {
                                            "schema": {},
                                        },
                                    },
                                    "description": "Successful Response",
                                },
                                "422": {
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/HTTPValidationError",
                                            },
                                        },
                                    },
                                    "description": "Validation Error",
                                },
                            },
                            "summary": "Read Item",
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
