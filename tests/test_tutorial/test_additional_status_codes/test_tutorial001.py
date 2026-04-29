from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("additional_status_codes", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def update(name: str):
    client = _client_for(name)
    response = client.put("/items/foo", json={"name": "Wrestlers"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"name": "Wrestlers", "size": None})


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def create(name: str):
    client = _client_for(name)
    response = client.put("/items/red", json={"name": "Chillies"})
    expect(response.status_code, "status code").to_equal(201).fatal()
    expect(response.json(), "response body").to_equal({"name": "Chillies", "size": None})
