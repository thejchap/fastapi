from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("response_directly", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def path_operation(name: str):
    client = _client_for(name)
    response = client.put(
        "/items/1",
        json={
            "title": "Foo",
            "timestamp": "2023-01-01T12:00:00",
            "description": "A test item",
        },
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "description": "A test item",
            "timestamp": "2023-01-01T12:00:00",
            "title": "Foo",
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def openapi_schema_pv2(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "OpenAPI schema").to_equal(
        snapshot(
            {
                "info": {
                    "title": "FastAPI",
                    "version": "0.1.0",
                },
                "openapi": "3.1.0",
                "paths": {
                    "/items/{id}": {
                        "put": {
                            "operationId": "update_item_items__id__put",
                            "parameters": [
                                {
                                    "in": "path",
                                    "name": "id",
                                    "required": True,
                                    "schema": {"title": "Id", "type": "string"},
                                },
                            ],
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Item",
                                        },
                                    },
                                },
                                "required": True,
                            },
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {"schema": {}},
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
                            "summary": "Update Item",
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
                        "Item": {
                            "properties": {
                                "description": {
                                    "anyOf": [
                                        {"type": "string"},
                                        {"type": "null"},
                                    ],
                                    "title": "Description",
                                },
                                "timestamp": {
                                    "format": "date-time",
                                    "title": "Timestamp",
                                    "type": "string",
                                },
                                "title": {"title": "Title", "type": "string"},
                            },
                            "required": [
                                "title",
                                "timestamp",
                            ],
                            "title": "Item",
                            "type": "object",
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
                                        ],
                                    },
                                    "title": "Location",
                                    "type": "array",
                                },
                                "msg": {"title": "Message", "type": "string"},
                                "type": {"title": "Error Type", "type": "string"},
                            },
                            "required": ["loc", "msg", "type"],
                            "title": "ValidationError",
                            "type": "object",
                        },
                    },
                },
            }
        )
    )
