from types import ModuleType

from tryke import expect, test

from ..._shims import import_tutorial


def _module_for(name: str) -> ModuleType:
    return import_tutorial("dependency_testing", name)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def override_in_items_run(name: str):
    test_module = _module_for(name)
    test_override_in_items = test_module.test_override_in_items
    test_override_in_items()


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def override_in_items_with_q_run(name: str):
    test_module = _module_for(name)
    test_override_in_items_with_q = test_module.test_override_in_items_with_q
    test_override_in_items_with_q()


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def override_in_items_with_params_run(name: str):
    test_module = _module_for(name)
    test_override_in_items_with_params = test_module.test_override_in_items_with_params
    test_override_in_items_with_params()


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def override_in_users(name: str):
    test_module = _module_for(name)
    client = test_module.client
    response = client.get("/users/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "message": "Hello Users!",
            "params": {"q": None, "skip": 5, "limit": 10},
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def override_in_users_with_q(name: str):
    test_module = _module_for(name)
    client = test_module.client
    response = client.get("/users/?q=foo")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "message": "Hello Users!",
            "params": {"q": "foo", "skip": 5, "limit": 10},
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def override_in_users_with_params(name: str):
    test_module = _module_for(name)
    client = test_module.client
    response = client.get("/users/?q=foo&skip=100&limit=200")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "message": "Hello Users!",
            "params": {"q": "foo", "skip": 5, "limit": 10},
        }
    )


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def normal_app(name: str):
    test_module = _module_for(name)
    app = test_module.app
    client = test_module.client
    app.dependency_overrides = None
    response = client.get("/items/?q=foo&skip=100&limit=200")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {
            "message": "Hello Items!",
            "params": {"q": "foo", "skip": 100, "limit": 200},
        }
    )
