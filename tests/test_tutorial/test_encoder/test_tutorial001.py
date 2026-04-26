from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str):
    mod = import_tutorial("encoder", name)
    return TestClient(mod.app), mod


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def put(name: str):
    client, mod = _client_for(name)
    fake_db = mod.fake_db

    response = client.put(
        "/items/123",
        json={
            "title": "Foo",
            "timestamp": "2023-01-01T12:00:00",
            "description": "An optional description",
        },
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(fake_db).to_contain("123")
    expect(fake_db["123"]).to_equal(
        {
            "title": "Foo",
            "timestamp": "2023-01-01T12:00:00",
            "description": "An optional description",
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def put_invalid_data(name: str):
    client, mod = _client_for(name)
    fake_db = mod.fake_db

    response = client.put(
        "/items/345",
        json={
            "title": "Foo",
            "timestamp": "not a date",
        },
    )
    expect(response.status_code).to_equal(422).fatal()
    expect(response.json()).to_equal(
        {
            "detail": [
                {
                    "loc": ["body", "timestamp"],
                    "msg": "Input should be a valid datetime or date, invalid character in year",
                    "type": "datetime_from_date_parsing",
                    "input": "not a date",
                    "ctx": {"error": "invalid character in year"},
                }
            ]
        }
    )
    expect(fake_db).not_.to_contain("345")


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def openapi_schema(name: str):
    client, _ = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/{id}": {
                        "put": {
                            "operationId": "update_item_items__id__put",
                            "parameters": [
                                {
                                    "in": "path",
                                    "name": "id",
                                    "required": True,
                                    "schema": {
                                        "title": "Id",
                                        "type": "string",
                                    },
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
                                "title": {
                                    "title": "Title",
                                    "type": "string",
                                },
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
