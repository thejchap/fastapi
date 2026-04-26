from dirty_equals import IsOneOf
from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("custom_request_and_route", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def endpoint_works(name: str):
    client = _client_for(name)
    response = client.post("/", json=[1, 2, 3])
    expect(response.json()).to_equal(6)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def exception_handler_body_access(name: str):
    client = _client_for(name)
    response = client.post("/", json={"numbers": [1, 2, 3]})
    expect(response.json()).to_equal(
        {
            "detail": {
                "errors": [
                    {
                        "type": "list_type",
                        "loc": ["body"],
                        "msg": "Input should be a valid list",
                        "input": {"numbers": [1, 2, 3]},
                    }
                ],
                # httpx 0.28.0 switches to compact JSON https://github.com/encode/httpx/issues/3363
                "body": IsOneOf('{"numbers": [1, 2, 3]}', '{"numbers":[1,2,3]}'),
            }
        }
    )
