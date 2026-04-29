from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.cors.tutorial001_py310 import app


@test("CORS middleware adds access-control headers for allowed origin")
def cors():
    client = TestClient(app)
    # Test pre-flight response.
    headers = {
        "Origin": "https://localhost.tiangolo.com",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "X-Example",
    }
    response = client.options("/", headers=headers)
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.text, "response text").to_equal("OK")
    expect(response.headers["access-control-allow-origin"], "access-control-allow-origin header").to_equal(
        "https://localhost.tiangolo.com"
    )
    expect(response.headers["access-control-allow-headers"], "access-control-allow-headers header").to_equal("X-Example")

    # Test standard response.
    headers = {"Origin": "https://localhost.tiangolo.com"}
    response = client.get("/", headers=headers)
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "Hello World"})
    expect(response.headers["access-control-allow-origin"], "access-control-allow-origin header").to_equal(
        "https://localhost.tiangolo.com"
    )

    # Test non-CORS response.
    response = client.get("/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "Hello World"})
    expect(response.headers, "response headers").not_.to_contain("access-control-allow-origin")
