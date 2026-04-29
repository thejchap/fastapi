from typing import Annotated

from fastapi import FastAPI, File, Form
from starlette.testclient import TestClient
from tryke import expect, test

app = FastAPI()


@app.post("/urlencoded")
async def post_url_encoded(age: Annotated[int | None, Form()] = None):
    return age


@app.post("/multipart")
async def post_multi_part(
    age: Annotated[int | None, Form()] = None,
    file: Annotated[bytes | None, File()] = None,
):
    return {"file": file, "age": age}


client = TestClient(app)


@test("Empty url-encoded form value falls back to default None")
def form_default_url_encoded():
    response = client.post("/urlencoded", data={"age": ""})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.text, "response body").to_equal("null")


@test("Empty multipart form value falls back to default None")
def form_default_multi_part():
    response = client.post("/multipart", data={"age": ""})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"file": None, "age": None})
