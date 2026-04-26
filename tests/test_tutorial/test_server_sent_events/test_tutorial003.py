from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("server_sent_events", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
)
def stream_logs(name: str):
    client = _client_for(name)
    response = client.get("/logs/stream")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.headers["content-type"]).to_equal(
        "text/event-stream; charset=utf-8"
    )

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    expect(data_lines).to_have_length(3)

    # Raw_data is sent without JSON encoding (no quotes around the string).
    expect(data_lines[0]).to_equal("data: 2025-01-01 INFO  Application started")
    expect(data_lines[1]).to_equal("data: 2025-01-01 DEBUG Connected to database")
    expect(data_lines[2]).to_equal("data: 2025-01-01 WARN  High memory usage detected")


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
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
                    "/logs/stream": {
                        "get": {
                            "summary": "Stream Logs",
                            "operationId": "stream_logs_logs_stream_get",
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
