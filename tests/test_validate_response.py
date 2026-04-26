from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float | None = None
    owner_ids: list[int] | None = None


@app.get("/items/invalid", response_model=Item)
def get_invalid():
    return {"name": "invalid", "price": "foo"}


@app.get("/items/invalidnone", response_model=Item)
def get_invalid_none():
    return None


@app.get("/items/validnone", response_model=Item | None)
def get_valid_none(send_none: bool = False):
    if send_none:
        return None
    else:
        return {"name": "invalid", "price": 3.2}


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
def invalid_none():
    expect(lambda: client.get("/items/invalidnone")).to_raise(ResponseValidationError)


@test
def valid_none_data():
    response = client.get("/items/validnone")
    data = response.json()
    expect(response.status_code).to_equal(200)
    expect(data).to_equal({"name": "invalid", "price": 3.2, "owner_ids": None})


@test
def valid_none_none():
    response = client.get("/items/validnone", params={"send_none": "true"})
    data = response.json()
    expect(response.status_code).to_equal(200)
    expect(data).to_be_none()


@test
def double_invalid():
    expect(lambda: client.get("/items/innerinvalid")).to_raise(ResponseValidationError)


@test
def invalid_list():
    expect(lambda: client.get("/items/invalidlist")).to_raise(ResponseValidationError)
