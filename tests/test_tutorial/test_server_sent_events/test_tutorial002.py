from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("server_sent_events", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def stream_items(name: str):
    client = _client_for(name)
    response = client.get("/items/stream")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.headers["content-type"], "content-type header").to_equal(
        "text/event-stream; charset=utf-8"
    )

    lines = response.text.strip().split("\n")

    # First event is a comment-only event.
    expect(lines[0], "first line (comment)").to_equal(": stream of item updates")

    event_lines = [line for line in lines if line.startswith("event: ")]
    expect(event_lines, "event lines").to_have_length(3)
    expect(
        all(line == "event: item_update" for line in event_lines),
        "all events are item_update",
    ).to_be_truthy()

    data_lines = [line for line in lines if line.startswith("data: ")]
    expect(data_lines, "data lines").to_have_length(3)

    id_lines = [line for line in lines if line.startswith("id: ")]
    expect(id_lines, "id lines").to_equal(["id: 1", "id: 2", "id: 3"])

    retry_lines = [line for line in lines if line.startswith("retry: ")]
    expect(retry_lines, "retry lines").to_have_length(3)
    expect(
        all(line == "retry: 5000" for line in retry_lines),
        "all retry values are 5000",
    ).to_be_truthy()


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
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
                    "/items/stream": {
                        "get": {
                            "summary": "Stream Items",
                            "operationId": "stream_items_items_stream_get",
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
                    }
                },
            }
        )
    )
