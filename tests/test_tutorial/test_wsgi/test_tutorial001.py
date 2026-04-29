from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.wsgi.tutorial001_py310 import app

client = TestClient(app)


@test("WSGIMiddleware serves the mounted Flask app")
def flask():
    response = client.get("/v1/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.text, "Flask response body").to_equal("Hello, World from Flask!")


@test("FastAPI routes work alongside the mounted WSGI app")
def app_v2():
    response = client.get("/v2")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "Hello World"})
