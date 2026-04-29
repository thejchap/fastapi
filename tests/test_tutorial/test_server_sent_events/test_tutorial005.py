from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("server_sent_events", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial005_py310", name="tutorial005_py310"),
)
def stream_chat(name: str):
    client = _client_for(name)
    response = client.post(
        "/chat/stream",
        json={"text": "hello world"},
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.headers["content-type"], "content-type header").to_equal(
        "text/event-stream; charset=utf-8"
    )

    lines = response.text.strip().split("\n")

    event_lines = [line for line in lines if line.startswith("event: ")]
    expect(event_lines, "event lines").to_equal(
        [
            "event: token",
            "event: token",
            "event: done",
        ]
    )

    data_lines = [line for line in lines if line.startswith("data: ")]
    expect(data_lines, "data lines").to_equal(
        [
            'data: "hello"',
            'data: "world"',
            "data: [DONE]",
        ]
    )


@test.cases(
    test.case("tutorial005_py310", name="tutorial005_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "OpenAPI schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/chat/stream": {
                        "post": {
                            "summary": "Stream Chat",
                            "operationId": "stream_chat_chat_stream_post",
                            "requestBody": {
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Prompt"
                                        }
                                    }
                                },
                                "required": True,
                            },
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
                        "Prompt": {
                            "properties": {"text": {"type": "string", "title": "Text"}},
                            "type": "object",
                            "required": ["text"],
                            "title": "Prompt",
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
