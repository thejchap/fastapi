from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.advanced_middleware.tutorial002_py310 import app


@test
def middleware():
    client = TestClient(app, base_url="http://example.com")
    response = client.get("/")
    expect(response.status_code).to_equal(200).fatal()
    client = TestClient(app, base_url="http://subdomain.example.com")
    response = client.get("/")
    expect(response.status_code).to_equal(200).fatal()
    client = TestClient(app, base_url="http://invalidhost")
    response = client.get("/")
    expect(response.status_code).to_equal(400).fatal()
