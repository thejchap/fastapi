from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float | None = None
    owner_ids: list[int] | None = None


@app.get("/items/valid", response_model=Item)
def get_valid():
    return {"name": "valid", "price": 1.0}


@app.get("/items/coerce", response_model=Item)
def get_coerce():
    return {"name": "coerce", "price": "1.0"}


@app.get("/items/validlist", response_model=list[Item])
def get_validlist():
    return [
        {"name": "foo"},
        {"name": "bar", "price": 1.0},
        {"name": "baz", "price": 2.0, "owner_ids": [1, 2, 3]},
    ]


client = TestClient(app)


@test
def valid():
    response = client.get("/items/valid")
    response.raise_for_status()
    expect(response.json()).to_equal({"name": "valid", "price": 1.0, "owner_ids": None})


@test
def coerce():
    response = client.get("/items/coerce")
    response.raise_for_status()
    expect(response.json()).to_equal(
        {"name": "coerce", "price": 1.0, "owner_ids": None}
    )


@test
def validlist():
    response = client.get("/items/validlist")
    response.raise_for_status()
    expect(response.json()).to_equal(
        [
            {"name": "foo", "price": None, "owner_ids": None},
            {"name": "bar", "price": 1.0, "owner_ids": None},
            {"name": "baz", "price": 2.0, "owner_ids": [1, 2, 3]},
        ]
    )
