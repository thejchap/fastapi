from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import import_tutorial


def _module_for(name: str):
    return import_tutorial("dependencies", name)


@test.cases(
    test.case("tutorial008d_py310", name="tutorial008d_py310"),
    test.case("tutorial008d_an_py310", name="tutorial008d_an_py310"),
)
def get_no_item(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    response = client.get("/items/foo")
    expect(response.status_code, "status code").to_equal(404).fatal()
    expect(response.json(), "response body").to_equal(
        {"detail": "Item not found, there's only a plumbus here"}
    )


@test.cases(
    test.case("tutorial008d_py310", name="tutorial008d_py310"),
    test.case("tutorial008d_an_py310", name="tutorial008d_an_py310"),
)
def get(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    response = client.get("/items/plumbus")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal("plumbus")


@test.cases(
    test.case("tutorial008d_py310", name="tutorial008d_py310"),
    test.case("tutorial008d_an_py310", name="tutorial008d_an_py310"),
)
def internal_error(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    expect(lambda: client.get("/items/portal-gun"), "GET /items/portal-gun").to_raise(
        mod.InternalError,
        match="The portal gun is too dangerous to be owned by Rick",
    )


@test.cases(
    test.case("tutorial008d_py310", name="tutorial008d_py310"),
    test.case("tutorial008d_an_py310", name="tutorial008d_an_py310"),
)
def internal_server_error(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app, raise_server_exceptions=False)
    response = client.get("/items/portal-gun")
    expect(response.status_code, "status code").to_equal(500).fatal()
    expect(response.text, "response text").to_equal("Internal Server Error")
