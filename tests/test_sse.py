import asyncio
import time
from collections.abc import AsyncIterable, Iterable

import fastapi.routing
from fastapi import APIRouter, FastAPI
from fastapi.responses import EventSourceResponse
from fastapi.sse import ServerSentEvent
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import Depends, expect, fixture, test

from ._shims import monkeypatch_ctx


class Item(BaseModel):
    name: str
    description: str | None = None


items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]


app = FastAPI()


@app.get("/items/stream", response_class=EventSourceResponse)
async def sse_items() -> AsyncIterable[Item]:
    for item in items:
        yield item


@app.get("/items/stream-sync", response_class=EventSourceResponse)
def sse_items_sync() -> Iterable[Item]:
    yield from items


@app.get("/items/stream-no-annotation", response_class=EventSourceResponse)
async def sse_items_no_annotation():
    for item in items:
        yield item


@app.get("/items/stream-sync-no-annotation", response_class=EventSourceResponse)
def sse_items_sync_no_annotation():
    yield from items


@app.get("/items/stream-dict", response_class=EventSourceResponse)
async def sse_items_dict():
    for item in items:
        yield {"name": item.name, "description": item.description}


@app.get("/items/stream-sse-event", response_class=EventSourceResponse)
async def sse_items_event():
    yield ServerSentEvent(data="hello", event="greeting", id="1")
    yield ServerSentEvent(data={"key": "value"}, event="json-data", id="2")
    yield ServerSentEvent(comment="just a comment")
    yield ServerSentEvent(data="retry-test", retry=5000)


@app.get("/items/stream-mixed", response_class=EventSourceResponse)
async def sse_items_mixed() -> AsyncIterable[Item]:
    yield items[0]
    yield ServerSentEvent(data="custom-event", event="special")
    yield items[1]


@app.get("/items/stream-string", response_class=EventSourceResponse)
async def sse_items_string():
    yield ServerSentEvent(data="plain text data")


@app.post("/items/stream-post", response_class=EventSourceResponse)
async def sse_items_post() -> AsyncIterable[Item]:
    for item in items:
        yield item


@app.get("/items/stream-raw", response_class=EventSourceResponse)
async def sse_items_raw():
    yield ServerSentEvent(raw_data="plain text without quotes")
    yield ServerSentEvent(raw_data="<div>html fragment</div>", event="html")
    yield ServerSentEvent(raw_data="cpu,87.3,1709145600", event="csv")


router = APIRouter()


@router.get("/events", response_class=EventSourceResponse)
async def stream_events():
    yield {"msg": "hello"}
    yield {"msg": "world"}


app.include_router(router, prefix="/api")


@fixture
def client():
    with TestClient(app) as c:
        yield c


@test
def async_generator_with_model(client: TestClient = Depends(client)):
    response = client.get("/items/stream")
    expect(response.status_code).to_equal(200)
    expect(response.headers["content-type"]).to_equal(
        "text/event-stream; charset=utf-8"
    )
    expect(response.headers["cache-control"]).to_equal("no-cache")
    expect(response.headers["x-accel-buffering"]).to_equal("no")

    lines = response.text.strip().split("\n")
    data_lines = [line for line in lines if line.startswith("data: ")]
    expect(data_lines).to_have_length(3).fatal()
    expect(
        '"name":"Plumbus"' in data_lines[0] or '"name": "Plumbus"' in data_lines[0]
    ).to_be_truthy()
    expect(
        '"name":"Portal Gun"' in data_lines[1]
        or '"name": "Portal Gun"' in data_lines[1]
    ).to_be_truthy()
    expect(
        '"name":"Meeseeks Box"' in data_lines[2]
        or '"name": "Meeseeks Box"' in data_lines[2]
    ).to_be_truthy()


@test
def sync_generator_with_model(client: TestClient = Depends(client)):
    response = client.get("/items/stream-sync")
    expect(response.status_code).to_equal(200)
    expect(response.headers["content-type"]).to_equal(
        "text/event-stream; charset=utf-8"
    )

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    expect(data_lines).to_have_length(3)


@test
def async_generator_no_annotation(client: TestClient = Depends(client)):
    response = client.get("/items/stream-no-annotation")
    expect(response.status_code).to_equal(200)
    expect(response.headers["content-type"]).to_equal(
        "text/event-stream; charset=utf-8"
    )

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    expect(data_lines).to_have_length(3)


@test
def sync_generator_no_annotation(client: TestClient = Depends(client)):
    response = client.get("/items/stream-sync-no-annotation")
    expect(response.status_code).to_equal(200)
    expect(response.headers["content-type"]).to_equal(
        "text/event-stream; charset=utf-8"
    )

    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    expect(data_lines).to_have_length(3)


@test
def dict_items(client: TestClient = Depends(client)):
    response = client.get("/items/stream-dict")
    expect(response.status_code).to_equal(200)
    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    expect(data_lines).to_have_length(3).fatal()
    expect(data_lines[0]).to_contain('"name"')


@test
def post_method_sse(client: TestClient = Depends(client)):
    """SSE should work with POST (needed for MCP compatibility)."""
    response = client.post("/items/stream-post")
    expect(response.status_code).to_equal(200)
    expect(response.headers["content-type"]).to_equal(
        "text/event-stream; charset=utf-8"
    )
    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    expect(data_lines).to_have_length(3)


@test
def sse_events_with_fields(client: TestClient = Depends(client)):
    response = client.get("/items/stream-sse-event")
    expect(response.status_code).to_equal(200)
    text = response.text

    expect(text).to_contain("event: greeting\n")
    expect(text).to_contain('data: "hello"\n')
    expect(text).to_contain("id: 1\n")

    expect(text).to_contain("event: json-data\n")
    expect(text).to_contain("id: 2\n")
    expect(text).to_contain('data: {"key": "value"}\n')

    expect(text).to_contain(": just a comment\n")

    expect(text).to_contain("retry: 5000\n")
    expect(text).to_contain('data: "retry-test"\n')


@test
def mixed_plain_and_sse_events(client: TestClient = Depends(client)):
    response = client.get("/items/stream-mixed")
    expect(response.status_code).to_equal(200)
    text = response.text

    expect(text).to_contain("event: special\n")
    expect(text).to_contain('data: "custom-event"\n')
    expect(text).to_contain('"name"')


@test
def string_data_json_encoded(client: TestClient = Depends(client)):
    """Strings are always JSON-encoded (quoted)."""
    response = client.get("/items/stream-string")
    expect(response.status_code).to_equal(200)
    expect(response.text).to_contain('data: "plain text data"\n')


@test
def server_sent_event_null_id_rejected():
    expect(lambda: ServerSentEvent(data="test", id="has\0null")).to_raise(
        ValueError, match="null"
    )


@test
def server_sent_event_negative_retry_rejected():
    expect(lambda: ServerSentEvent(data="test", retry=-1)).to_raise(ValueError)


@test
def server_sent_event_float_retry_rejected():
    expect(lambda: ServerSentEvent(data="test", retry=1.5)).to_raise(ValueError)  # type: ignore[arg-type]


@test
def raw_data_sent_without_json_encoding(client: TestClient = Depends(client)):
    """raw_data is sent as-is, not JSON-encoded."""
    response = client.get("/items/stream-raw")
    expect(response.status_code).to_equal(200)
    text = response.text

    # raw_data should appear without JSON quotes
    expect(text).to_contain("data: plain text without quotes\n")
    # Not JSON-quoted
    expect('data: "plain text without quotes"' in text).to_be_falsy()

    expect(text).to_contain("event: html\n")
    expect(text).to_contain("data: <div>html fragment</div>\n")

    expect(text).to_contain("event: csv\n")
    expect(text).to_contain("data: cpu,87.3,1709145600\n")


@test
def data_and_raw_data_mutually_exclusive():
    """Cannot set both data and raw_data."""
    expect(lambda: ServerSentEvent(data="json", raw_data="raw")).to_raise(
        ValueError, match="Cannot set both"
    )


@test
def sse_on_router_included_in_app(client: TestClient = Depends(client)):
    response = client.get("/api/events")
    expect(response.status_code).to_equal(200)
    expect(response.headers["content-type"]).to_equal(
        "text/event-stream; charset=utf-8"
    )
    data_lines = [
        line for line in response.text.strip().split("\n") if line.startswith("data: ")
    ]
    expect(data_lines).to_have_length(2)


# Keepalive ping tests


keepalive_app = FastAPI()


@keepalive_app.get("/slow-async", response_class=EventSourceResponse)
async def slow_async_stream():
    yield {"n": 1}
    # Sleep longer than the (monkeypatched) ping interval so a keepalive
    # comment is emitted before the next item.
    await asyncio.sleep(0.3)
    yield {"n": 2}


@keepalive_app.get("/slow-sync", response_class=EventSourceResponse)
def slow_sync_stream():
    yield {"n": 1}
    time.sleep(0.3)
    yield {"n": 2}


@test
def keepalive_ping_async():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr(fastapi.routing, "_PING_INTERVAL", 0.05)
        with TestClient(keepalive_app) as c:
            response = c.get("/slow-async")
    expect(response.status_code).to_equal(200)
    text = response.text
    # The keepalive comment ": ping" should appear between the two data events
    expect(text).to_contain(": ping\n")
    data_lines = [line for line in text.split("\n") if line.startswith("data: ")]
    expect(data_lines).to_have_length(2)


@test
def keepalive_ping_sync():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr(fastapi.routing, "_PING_INTERVAL", 0.05)
        with TestClient(keepalive_app) as c:
            response = c.get("/slow-sync")
    expect(response.status_code).to_equal(200)
    text = response.text
    expect(text).to_contain(": ping\n")
    data_lines = [line for line in text.split("\n") if line.startswith("data: ")]
    expect(data_lines).to_have_length(2)


@test
def no_keepalive_when_fast(client: TestClient = Depends(client)):
    """No keepalive comment when items arrive quickly."""
    response = client.get("/items/stream")
    expect(response.status_code).to_equal(200)
    # KEEPALIVE_COMMENT is ": ping\n\n".
    expect(": ping\n" in response.text).to_be_falsy()
