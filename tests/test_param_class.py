from fastapi import FastAPI
from fastapi.params import Param
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()


@app.get("/items/")
def read_items(q: str | None = Param(default=None)):  # type: ignore
    return {"q": q}


client = TestClient(app)


@test
def default_param_query_none():
    response = client.get("/items/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"q": None})


@test
def default_param_query():
    response = client.get("/items/?q=foo")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"q": "foo"})
