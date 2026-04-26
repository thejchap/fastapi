from dirty_equals import IsPartialDict
from fastapi import Cookie, FastAPI, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from tryke import expect, test

app = FastAPI()


class Model(BaseModel):
    param: str = Field(alias="param_alias")


@app.get("/query")
async def query_model(data: Model = Query()):
    return {"param": data.param}


@app.get("/header")
async def header_model(data: Model = Header()):
    return {"param": data.param}


@app.get("/cookie")
async def cookie_model(data: Model = Cookie()):
    return {"param": data.param}


@test
def query_model_with_alias():
    client = TestClient(app)
    response = client.get("/query", params={"param_alias": "value"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"param": "value"})


@test
def header_model_with_alias():
    client = TestClient(app)
    response = client.get("/header", headers={"param_alias": "value"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"param": "value"})


@test
def cookie_model_with_alias():
    client = TestClient(app)
    client.cookies.set("param_alias", "value")
    response = client.get("/cookie")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"param": "value"})


@test
def query_model_with_alias_by_name():
    client = TestClient(app)
    response = client.get("/query", params={"param": "value"})
    expect(response.status_code).to_equal(422).fatal()
    details = response.json()
    expect(details["detail"][0]["input"]).to_equal({"param": "value"})


@test
def header_model_with_alias_by_name():
    client = TestClient(app)
    response = client.get("/header", headers={"param": "value"})
    expect(response.status_code).to_equal(422).fatal()
    details = response.json()
    expect(details["detail"][0]["input"]).to_equal(IsPartialDict({"param": "value"}))


@test
def cookie_model_with_alias_by_name():
    client = TestClient(app)
    client.cookies.set("param", "value")
    response = client.get("/cookie")
    expect(response.status_code).to_equal(422).fatal()
    details = response.json()
    expect(details["detail"][0]["input"]).to_equal({"param": "value"})
