from fastapi import Body, FastAPI, Query
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()


@app.get("/query")
def read_query(q: str | None):
    return q


@app.get("/explicit-query")
def read_explicit_query(q: str | None = Query()):
    return q


@app.post("/body-embed")
def send_body_embed(b: str | None = Body(embed=True)):
    return b


client = TestClient(app)


@test
def required_nonable_query_invalid():
    response = client.get("/query")
    expect(response.status_code).to_equal(422).fatal()


@test
def required_noneable_query_value():
    response = client.get("/query", params={"q": "foo"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo")


@test
def required_nonable_explicit_query_invalid():
    response = client.get("/explicit-query")
    expect(response.status_code).to_equal(422).fatal()


@test
def required_nonable_explicit_query_value():
    response = client.get("/explicit-query", params={"q": "foo"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo")


@test
def required_nonable_body_embed_no_content():
    response = client.post("/body-embed")
    expect(response.status_code).to_equal(422).fatal()


@test
def required_nonable_body_embed_invalid():
    response = client.post("/body-embed", json={"invalid": "invalid"})
    expect(response.status_code).to_equal(422).fatal()


@test
def required_noneable_body_embed_value():
    response = client.post("/body-embed", json={"b": "foo"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("foo")
