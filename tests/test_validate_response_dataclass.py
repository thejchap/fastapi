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


@test
def invalid():
    expect(lambda: client.get("/items/invalid")).to_raise(ResponseValidationError)


@test
def double_invalid():
    expect(lambda: client.get("/items/innerinvalid")).to_raise(ResponseValidationError)


@test
def invalid_list():
    expect(lambda: client.get("/items/invalidlist")).to_raise(ResponseValidationError)
