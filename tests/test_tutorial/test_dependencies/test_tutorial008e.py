from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("dependencies", name)
    client = TestClient(mod.app)
    return client


@test.cases(
    test.case("tutorial008e_py310", name="tutorial008e_py310"),
    test.case("tutorial008e_an_py310", name="tutorial008e_an_py310"),
)
def get_users_me(name: str):
    client = _client_for(name)
    response = client.get("/users/me")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("Rick")
