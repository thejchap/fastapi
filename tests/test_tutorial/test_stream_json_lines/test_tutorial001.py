import json

from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("stream_json_lines", name)
    return TestClient(mod.app)


expected_items = [
    {"name": "Plumbus", "description": "A multi-purpose household device."},
    {"name": "Portal Gun", "description": "A portal opening device."},
    {"name": "Meeseeks Box", "description": "A box that summons a Meeseeks."},
]


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
    expect(response.headers["content-type"]).to_equal("application/jsonl")
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    expect(lines).to_equal(expected_items)


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
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/jsonl": {
                                            "itemSchema": {
                                                "$ref": "#/components/schemas/Item"
                                            },
                                        }
                                    },
                                }
                            },
                            "summary": "Stream Items",
                            "operationId": "stream_items_items_stream_get",
                        }
                    },
                    "/items/stream-no-async": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/jsonl": {
                                            "itemSchema": {
                                                "$ref": "#/components/schemas/Item"
                                            },
                                        }
                                    },
                                }
                            },
                            "summary": "Stream Items No Async",
                            "operationId": "stream_items_no_async_items_stream_no_async_get",
                        }
                    },
                    "/items/stream-no-annotation": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/jsonl": {
                                            "itemSchema": {},
                                        }
                                    },
                                }
                            },
                            "summary": "Stream Items No Annotation",
                            "operationId": "stream_items_no_annotation_items_stream_no_annotation_get",
                        }
                    },
                    "/items/stream-no-async-no-annotation": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/jsonl": {
                                            "itemSchema": {},
                                        }
                                    },
                                }
                            },
                            "summary": "Stream Items No Async No Annotation",
                            "operationId": "stream_items_no_async_no_annotation_items_stream_no_async_no_annotation_get",
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
