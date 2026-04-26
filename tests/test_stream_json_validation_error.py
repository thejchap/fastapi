from collections.abc import AsyncIterable, Iterable

from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import expect, test


class Item(BaseModel):
    name: str
    price: float


app = FastAPI()


@app.get("/items/stream-invalid")
async def stream_items_invalid() -> AsyncIterable[Item]:
    yield {"name": "valid", "price": 1.0}
    yield {"name": "invalid", "price": "not-a-number"}


@app.get("/items/stream-invalid-sync")
def stream_items_invalid_sync() -> Iterable[Item]:
    yield {"name": "valid", "price": 1.0}
    yield {"name": "invalid", "price": "not-a-number"}


client = TestClient(app)


@test
def stream_json_validation_error_async():
    expect(lambda: client.get("/items/stream-invalid")).to_raise(
        ResponseValidationError
    )


@test
def stream_json_validation_error_sync():
    expect(lambda: client.get("/items/stream-invalid-sync")).to_raise(
        ResponseValidationError
    )
