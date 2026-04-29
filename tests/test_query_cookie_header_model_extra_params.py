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


@test("Query model with extra='allow' captures repeated values as a list")
def query_pass_extra_list():
    client = TestClient(app)
    resp = client.get(
        "/query",
        params={
            "param": "123",
            "param2": ["456", "789"],  # Pass a list of values as extra parameter
        },
    )
    expect(resp.status_code, "status code").to_equal(200)
    expect(resp.json(), "response body").to_equal(
        {
            "param": "123",
            "param2": ["456", "789"],
        }
    )


@test("Query model with extra='allow' captures a single extra value")
def query_pass_extra_single():
    client = TestClient(app)
    resp = client.get(
        "/query",
        params={
            "param": "123",
            "param2": "456",
        },
    )
    expect(resp.status_code, "status code").to_equal(200)
    expect(resp.json(), "response body").to_equal(
        {
            "param": "123",
            "param2": "456",
        }
    )


@test("Header model with extra='allow' captures repeated values as a list")
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
    expect(resp.status_code, "status code").to_equal(200)
    resp_json = resp.json()
    expect(resp_json, "response body").to_contain("param2")
    expect(resp_json["param2"], "extra param2 value").to_equal(["456", "789"])


@test("Header model with extra='allow' captures a single extra value")
def header_pass_extra_single():
    client = TestClient(app)

    resp = client.get(
        "/header",
        headers=[
            ("param", "123"),
            ("param2", "456"),
        ],
    )
    expect(resp.status_code, "status code").to_equal(200)
    resp_json = resp.json()
    expect(resp_json, "response body").to_contain("param2")
    expect(resp_json["param2"], "extra param2 value").to_equal("456")


@test("Cookie model with extra='allow' keeps only the last repeated value")
def cookie_pass_extra_list():
    client = TestClient(app)
    client.cookies = [
        ("param", "123"),
        ("param2", "456"),  # Pass a list of values as extra parameter
        ("param2", "789"),
    ]
    resp = client.get("/cookie")
    expect(resp.status_code, "status code").to_equal(200)
    resp_json = resp.json()
    expect(resp_json, "response body").to_contain("param2")
    expect(resp_json["param2"], "extra param2 value").to_equal("789")
