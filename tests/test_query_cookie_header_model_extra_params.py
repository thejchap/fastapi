from fastapi import Cookie, FastAPI, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()


class Model(BaseModel):
    param: str

    model_config = {"extra": "allow"}


@app.get("/query")
async def query_model_with_extra(data: Model = Query()):
    return data


@app.get("/header")
async def header_model_with_extra(data: Model = Header()):
    return data


@app.get("/cookie")
async def cookies_model_with_extra(data: Model = Cookie()):
    return data


@test
def query_pass_extra_list():
    client = TestClient(app)
    resp = client.get(
        "/query",
        params={
            "param": "123",
            "param2": ["456", "789"],  # Pass a list of values as extra parameter
        },
    )
    expect(resp.status_code).to_equal(200)
    expect(resp.json()).to_equal(
        {
            "param": "123",
            "param2": ["456", "789"],
        }
    )


@test
def query_pass_extra_single():
    client = TestClient(app)
    resp = client.get(
        "/query",
        params={
            "param": "123",
            "param2": "456",
        },
    )
    expect(resp.status_code).to_equal(200)
    expect(resp.json()).to_equal(
        {
            "param": "123",
            "param2": "456",
        }
    )


@test
def header_pass_extra_list():
    client = TestClient(app)

    resp = client.get(
        "/header",
        headers=[
            ("param", "123"),
            ("param2", "456"),  # Pass a list of values as extra parameter
            ("param2", "789"),
        ],
    )
    expect(resp.status_code).to_equal(200)
    resp_json = resp.json()
    expect(resp_json).to_contain("param2")
    expect(resp_json["param2"]).to_equal(["456", "789"])


@test
def header_pass_extra_single():
    client = TestClient(app)

    resp = client.get(
        "/header",
        headers=[
            ("param", "123"),
            ("param2", "456"),
        ],
    )
    expect(resp.status_code).to_equal(200)
    resp_json = resp.json()
    expect(resp_json).to_contain("param2")
    expect(resp_json["param2"]).to_equal("456")


@test
def cookie_pass_extra_list():
    client = TestClient(app)
    client.cookies = [
        ("param", "123"),
        ("param2", "456"),  # Pass a list of values as extra parameter
        ("param2", "789"),
    ]
    resp = client.get("/cookie")
    expect(resp.status_code).to_equal(200)
    resp_json = resp.json()
    expect(resp_json).to_contain("param2")
    expect(resp_json["param2"]).to_equal("789")
