from fastapi import FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

app_default = FastAPI()


@app_default.post("/items/")
async def app_default_post(data: dict):
    return data


app_lax = FastAPI(strict_content_type=False)


@app_lax.post("/items/")
async def app_lax_post(data: dict):
    return data


client_default = TestClient(app_default)
client_lax = TestClient(app_lax)


@test("Default strict app rejects POST without content-type")
def default_strict_rejects_no_content_type():
    response = client_default.post("/items/", content='{"key": "value"}')
    expect(response.status_code, "status code").to_equal(422)


@test("Default strict app accepts POST with JSON content-type")
def default_strict_accepts_json_content_type():
    response = client_default.post("/items/", json={"key": "value"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"key": "value"})


@test("Lax app accepts POST without content-type")
def lax_accepts_no_content_type():
    response = client_lax.post("/items/", content='{"key": "value"}')
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"key": "value"})


@test("Lax app accepts POST with JSON content-type")
def lax_accepts_json_content_type():
    response = client_lax.post("/items/", json={"key": "value"})
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"key": "value"})
