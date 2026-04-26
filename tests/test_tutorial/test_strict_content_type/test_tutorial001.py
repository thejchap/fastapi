from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("strict_content_type", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def lax_post_without_content_type_is_parsed_as_json(name: str):
    client = _client_for(name)
    response = client.post(
        "/items/",
        content='{"name": "Foo", "price": 50.5}',
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"name": "Foo", "price": 50.5})


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def lax_post_with_json_content_type(name: str):
    client = _client_for(name)
    response = client.post(
        "/items/",
        json={"name": "Foo", "price": 50.5},
    )
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"name": "Foo", "price": 50.5})


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def lax_post_with_text_plain_is_still_rejected(name: str):
    client = _client_for(name)
    response = client.post(
        "/items/",
        content='{"name": "Foo", "price": 50.5}',
        headers={"Content-Type": "text/plain"},
    )
    expect(response.status_code).to_equal(422).fatal()
