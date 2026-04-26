from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("server_sent_events", name)
    return TestClient(mod.app)


@test.cases(
    test.case("stream", name="tutorial001_py310", path="/items/stream"),
    test.case(
        "stream-no-async", name="tutorial001_py310", path="/items/stream-no-async"
    ),
    test.case(
        "stream-no-annotation",
        name="tutorial001_py310",
        path="/items/stream-no-annotation",
    ),
    test.case(
        "stream-no-async-no-annotation",
        name="tutorial001_py310",
        path="/items/stream-no-async-no-annotation",
    ),
)
def stream_items(name: str, path: str):
    client = _client_for(name)
    response = client.get(path)
    expect(response.status_code).to_equal(200).fatal()
    expect(response.headers["content-type"]).to_equal(
        "text/event-stream; charset=utf-8"
    )
    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    expect(data_lines).to_have_length(3)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
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
                            "summary": "Sse Items",
                            "operationId": "sse_items_items_stream_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "text/event-stream": {
                                            "itemSchema": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "string",
                                                        "contentMediaType": "application/json",
                                                        "contentSchema": {
                                                            "$ref": "#/components/schemas/Item"
                                                        },
                                                    },
                                                    "event": {"type": "string"},
                                                    "id": {"type": "string"},
                                                    "retry": {
                                                        "type": "integer",
                                                        "minimum": 0,
                                                    },
                                                },
                                                "required": ["data"],
                                            }
                                        }
                                    },
                                }
                            },
                        }
                    },
                    "/items/stream-no-async": {
                        "get": {
                            "summary": "Sse Items No Async",
                            "operationId": "sse_items_no_async_items_stream_no_async_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "text/event-stream": {
                                            "itemSchema": {
                                                "type": "object",
                                                "properties": {
                                                    "data": {
                                                        "type": "string",
                                                        "contentMediaType": "application/json",
                                                        "contentSchema": {
                                                            "$ref": "#/components/schemas/Item"
                                                        },
                                                    },
                                                    "event": {"type": "string"},
                                                    "id": {"type": "string"},
                                                    "retry": {
                                                        "type": "integer",
                                                        "minimum": 0,
                                                    },
                                                },
                                                "required": ["data"],
                                            }
                                        }
                                    },
                                }
                            },
                        }
                    },
                    "/items/stream-no-annotation": {
                        "get": {
                            "summary": "Sse Items No Annotation",
                            "operationId": "sse_items_no_annotation_items_stream_no_annotation_get",
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
                                }
                            },
                        }
                    },
                    "/items/stream-no-async-no-annotation": {
                        "get": {
                            "summary": "Sse Items No Async No Annotation",
                            "operationId": "sse_items_no_async_no_annotation_items_stream_no_async_no_annotation_get",
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
                                }
                            },
                        }
                    },
                },
                "components": {
                    "schemas": {
                        "Item": {
                            "properties": {
                                "name": {"type": "string", "title": "Name"},
                                "description": {
                                    "anyOf": [
                                        {"type": "string"},
                                        {"type": "null"},
                                    ],
                                    "title": "Description",
                                },
                            },
                            "type": "object",
                            "required": ["name", "description"],
                            "title": "Item",
                        }
                    }
                },
            }
        )
    )
