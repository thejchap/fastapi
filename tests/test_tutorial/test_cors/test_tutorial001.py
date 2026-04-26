from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.cors.tutorial001_py310 import app


@test
def cors():
    client = TestClient(app)
    # Test pre-flight response.
    headers = {
        "Origin": "https://localhost.tiangolo.com",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "X-Example",
    }
    response = client.options("/", headers=headers)
    expect(response.status_code).to_equal(200).fatal()
    expect(response.text).to_equal("OK")
    expect(response.headers["access-control-allow-origin"]).to_equal(
        "https://localhost.tiangolo.com"
    )
    expect(response.headers["access-control-allow-headers"]).to_equal("X-Example")

    # Test standard response.
    headers = {"Origin": "https://localhost.tiangolo.com"}
    response = client.get("/", headers=headers)
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"message": "Hello World"})
    expect(response.headers["access-control-allow-origin"]).to_equal(
        "https://localhost.tiangolo.com"
    )

    # Test non-CORS response.
    response = client.get("/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"message": "Hello World"})
    expect(response.headers).not_.to_contain("access-control-allow-origin")
