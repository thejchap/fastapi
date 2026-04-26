import json
from typing import AsyncIterable, Iterable  # noqa: UP035 to test coverage

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import expect, test


class Item(BaseModel):
    name: str


app = FastAPI()


@app.get("/items/stream-bare-async")
async def stream_bare_async() -> AsyncIterable:
    yield {"name": "foo"}


@app.get("/items/stream-bare-sync")
def stream_bare_sync() -> Iterable:
    yield {"name": "bar"}


client = TestClient(app)


@test
def stream_bare_async_iterable():
    response = client.get("/items/stream-bare-async")
    expect(response.status_code).to_equal(200)
    expect(response.headers["content-type"]).to_equal("application/jsonl")
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    expect(lines).to_equal([{"name": "foo"}])


@test
def stream_bare_sync_iterable():
    response = client.get("/items/stream-bare-sync")
    expect(response.status_code).to_equal(200)
    expect(response.headers["content-type"]).to_equal("application/jsonl")
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    expect(lines).to_equal([{"name": "bar"}])
