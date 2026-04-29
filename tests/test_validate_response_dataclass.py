from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient
from pydantic.dataclasses import dataclass
from tryke import expect, test

app = FastAPI()


@dataclass
class Item:
    name: str
    price: float | None = None
    owner_ids: list[int] | None = None


@app.get("/items/invalid", response_model=Item)
def get_invalid():
    return {"name": "invalid", "price": "foo"}


@app.get("/items/innerinvalid", response_model=Item)
def get_innerinvalid():
    return {"name": "double invalid", "price": "foo", "owner_ids": ["foo", "bar"]}


@app.get("/items/invalidlist", response_model=list[Item])
def get_invalidlist():
    return [
        {"name": "foo"},
        {"name": "bar", "price": "bar"},
        {"name": "baz", "price": "baz"},
    ]


client = TestClient(app)


@test("Dataclass response_model raises on invalid scalar field")
def invalid():
    expect(
        lambda: client.get("/items/invalid"),
        "GET to invalid item",
    ).to_raise(ResponseValidationError)


@test("Dataclass response_model raises on invalid nested field")
def double_invalid():
    expect(
        lambda: client.get("/items/innerinvalid"),
        "GET to nested-invalid item",
    ).to_raise(ResponseValidationError)


@test("Dataclass response_model raises on invalid list element")
def invalid_list():
    expect(
        lambda: client.get("/items/invalidlist"),
        "GET to invalid list of items",
    ).to_raise(ResponseValidationError)
