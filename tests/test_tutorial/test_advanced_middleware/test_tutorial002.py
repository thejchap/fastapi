from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.advanced_middleware.tutorial002_py310 import app


@test("TrustedHost middleware accepts allowed hosts")
def middleware():
    client = TestClient(app, base_url="http://example.com")
    response = client.get("/")
    expect(response.status_code, "example.com status").to_equal(200).fatal()
    client = TestClient(app, base_url="http://subdomain.example.com")
    response = client.get("/")
    expect(response.status_code, "subdomain.example.com status").to_equal(200).fatal()
    client = TestClient(app, base_url="http://invalidhost")
    response = client.get("/")
    expect(response.status_code, "invalidhost status").to_equal(400).fatal()
