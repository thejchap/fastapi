from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.advanced_middleware.tutorial001_py310 import app


@test
def middleware():
    client = TestClient(app, base_url="https://testserver")
    response = client.get("/")
    expect(response.status_code).to_equal(200).fatal()

    client = TestClient(app)
    response = client.get("/", follow_redirects=False)
    expect(response.status_code).to_equal(307).fatal()
    expect(response.headers["location"]).to_equal("https://testserver/")
