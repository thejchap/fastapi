from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.wsgi.tutorial001_py310 import app

client = TestClient(app)


@test
def flask():
    response = client.get("/v1/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.text).to_equal("Hello, World from Flask!")


@test
def app_v2():
    response = client.get("/v2")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"message": "Hello World"})
