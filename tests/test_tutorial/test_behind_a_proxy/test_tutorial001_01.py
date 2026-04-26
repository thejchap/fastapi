from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.behind_a_proxy.tutorial001_01_py310 import app

client = TestClient(
    app,
    base_url="https://example.com",
    follow_redirects=False,
)


@test
def redirect() -> None:
    response = client.get("/items")
    expect(response.status_code).to_equal(307).fatal()
    expect(response.headers["location"]).to_equal("https://example.com/items/")


@test
def no_redirect() -> None:
    response = client.get("/items/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(["plumbus", "portal gun"])
