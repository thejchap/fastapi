from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("server_sent_events", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
)
def stream_all_items(name: str):
    client = _client_for(name)
    response = client.get("/items/stream")
    expect(response.status_code).to_equal(200).fatal()

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    expect(data_lines).to_have_length(3)

    id_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("id: ")
    ]
    expect(id_lines).to_equal(["id: 0", "id: 1", "id: 2"])


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
)
def resume_from_last_event_id(name: str):
    client = _client_for(name)
    response = client.get(
        "/items/stream",
        headers={"last-event-id": "0"},
    )
    expect(response.status_code).to_equal(200).fatal()

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    expect(data_lines).to_have_length(2)

    id_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("id: ")
    ]
    expect(id_lines).to_equal(["id: 1", "id: 2"])


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
)
def resume_from_last_item(name: str):
    client = _client_for(name)
    response = client.get(
        "/items/stream",
        headers={"last-event-id": "1"},
    )
    expect(response.status_code).to_equal(200).fatal()

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    expect(data_lines).to_have_length(1)

    id_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("id: ")
    ]
    expect(id_lines).to_equal(["id: 2"])


@test.cases(
    test.case("tutorial004_py310", name="tutorial004_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/stream": {
                        "get": {
                            "summary": "Stream Items",
                            "operationId": "stream_items_items_stream_get",
                            "parameters": [
                                {
                                    "name": "last-event-id",
                                    "in": "header",
                                    "required": False,
                                    "schema": {
                                        "anyOf": [
                                            {"type": "integer"},
                                            {"type": "null"},
                                        ],
                                        "title": "Last-Event-Id",
                                    },
                                }
                            ],
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "text/event-stream": {
                                            "itemSchema": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {"type": "string"},
                                                    "event": {"type": "string"},
                                                    "id": {"type": "string"},
                                                    "retry": {
                                                        "type": "integer",
                                                        "minimum": 0,
                                                    },
                                                },
                                            }
                                        }
                                    },
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
                                "input": {"title": "Input"},
                                "ctx": {"type": "object", "title": "Context"},
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
