from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("dependencies", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial008b_py310", name="tutorial008b_py310"),
    test.case("tutorial008b_an_py310", name="tutorial008b_an_py310"),
)
def get_no_item(name: str):
    client = _client_for(name)
    response = client.get("/items/foo")
    expect(response.status_code, "status code").to_equal(404).fatal()
    expect(response.json(), "response body").to_equal({"detail": "Item not found"})


@test.cases(
    test.case("tutorial008b_py310", name="tutorial008b_py310"),
    test.case("tutorial008b_an_py310", name="tutorial008b_an_py310"),
)
def owner_error(name: str):
    client = _client_for(name)
    response = client.get("/items/plumbus")
    expect(response.status_code, "status code").to_equal(400).fatal()
    expect(response.json(), "response body").to_equal({"detail": "Owner error: Rick"})


@test.cases(
    test.case("tutorial008b_py310", name="tutorial008b_py310"),
    test.case("tutorial008b_an_py310", name="tutorial008b_an_py310"),
)
def get_item(name: str):
    client = _client_for(name)
    response = client.get("/items/portal-gun")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"description": "Gun to create portals", "owner": "Rick"}
    )
