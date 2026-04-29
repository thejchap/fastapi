from fastapi.testclient import TestClient
from tryke import Depends, expect, fixture, test

from docs_src.custom_request_and_route.tutorial003_py310 import app


@fixture
def client() -> TestClient:
    return TestClient(app)


@test("GET / returns response without X-Response-Time header")
def get(client: TestClient = Depends(client)):
    response = client.get("/")
    expect(response.json(), "response body").to_equal({"message": "Not timed"})
    expect("X-Response-Time" in response.headers, "X-Response-Time header present").to_be_falsy()


@test("GET /timed adds X-Response-Time header")
def get_timed(client: TestClient = Depends(client)):
    response = client.get("/timed")
    expect(response.json(), "response body").to_equal({"message": "It's the time of my life"})
    expect("X-Response-Time" in response.headers, "X-Response-Time header present").to_be_truthy()
    expect(
        float(response.headers["X-Response-Time"]) >= 0, "X-Response-Time is non-negative"
    ).to_be_truthy()
