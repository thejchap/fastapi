from fastapi import APIRouter, Depends, FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()

router = APIRouter()


async def common_parameters(q: str, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/main-depends/")
async def main_depends(commons: dict = Depends(common_parameters)):
    return {"in": "main-depends", "params": commons}


@app.get("/decorator-depends/", dependencies=[Depends(common_parameters)])
async def decorator_depends():
    return {"in": "decorator-depends"}


@router.get("/router-depends/")
async def router_depends(commons: dict = Depends(common_parameters)):
    return {"in": "router-depends", "params": commons}


@router.get("/router-decorator-depends/", dependencies=[Depends(common_parameters)])
async def router_decorator_depends():
    return {"in": "router-decorator-depends"}


app.include_router(router)

client = TestClient(app)


async def overrider_dependency_simple(q: str | None = None):
    return {"q": q, "skip": 5, "limit": 10}


async def overrider_sub_dependency(k: str):
    return {"k": k}


async def overrider_dependency_with_sub(msg: dict = Depends(overrider_sub_dependency)):
    return msg


@test("missing q on /main-depends/ returns 422")
def main_depends_test():
    response = client.get("/main-depends/")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "q"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("/main-depends/ with q uses default skip and limit")
def main_depends_q_foo():
    response = client.get("/main-depends/?q=foo")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {
            "in": "main-depends",
            "params": {"q": "foo", "skip": 0, "limit": 100},
        }
    )


@test("/main-depends/ accepts q, skip, and limit query params")
def main_depends_q_foo_skip_100_limit_200():
    response = client.get("/main-depends/?q=foo&skip=100&limit=200")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {
            "in": "main-depends",
            "params": {"q": "foo", "skip": 100, "limit": 200},
        }
    )


@test("missing q on /decorator-depends/ returns 422")
def decorator_depends_test():
    response = client.get("/decorator-depends/")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "q"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("/decorator-depends/ with q returns 200")
def decorator_depends_q_foo():
    response = client.get("/decorator-depends/?q=foo")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"in": "decorator-depends"})


@test("/decorator-depends/ ignores extra params")
def decorator_depends_q_foo_skip_100_limit_200():
    response = client.get("/decorator-depends/?q=foo&skip=100&limit=200")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"in": "decorator-depends"})


@test("missing q on /router-depends/ returns 422")
def router_depends_test():
    response = client.get("/router-depends/")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "q"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("/router-depends/ with q uses default skip and limit")
def router_depends_q_foo():
    response = client.get("/router-depends/?q=foo")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {
            "in": "router-depends",
            "params": {"q": "foo", "skip": 0, "limit": 100},
        }
    )


@test("/router-depends/ accepts q, skip, and limit")
def router_depends_q_foo_skip_100_limit_200():
    response = client.get("/router-depends/?q=foo&skip=100&limit=200")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {
            "in": "router-depends",
            "params": {"q": "foo", "skip": 100, "limit": 200},
        }
    )


@test("missing q on /router-decorator-depends/ returns 422")
def router_decorator_depends_test():
    response = client.get("/router-decorator-depends/")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "q"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )


@test("/router-decorator-depends/ with q returns 200")
def router_decorator_depends_q_foo():
    response = client.get("/router-decorator-depends/?q=foo")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"in": "router-decorator-depends"}
    )


@test("/router-decorator-depends/ ignores extra params")
def router_decorator_depends_q_foo_skip_100_limit_200():
    response = client.get("/router-decorator-depends/?q=foo&skip=100&limit=200")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"in": "router-decorator-depends"}
    )


@test.cases(
    test.case(
        "main-depends",
        url="/main-depends/",
        status_code=200,
        expected={"in": "main-depends", "params": {"q": None, "skip": 5, "limit": 10}},
    ),
    test.case(
        "main-depends q=foo",
        url="/main-depends/?q=foo",
        status_code=200,
        expected={"in": "main-depends", "params": {"q": "foo", "skip": 5, "limit": 10}},
    ),
    test.case(
        "main-depends q=foo&skip=100&limit=200",
        url="/main-depends/?q=foo&skip=100&limit=200",
        status_code=200,
        expected={"in": "main-depends", "params": {"q": "foo", "skip": 5, "limit": 10}},
    ),
    test.case(
        "decorator-depends",
        url="/decorator-depends/",
        status_code=200,
        expected={"in": "decorator-depends"},
    ),
    test.case(
        "router-depends",
        url="/router-depends/",
        status_code=200,
        expected={
            "in": "router-depends",
            "params": {"q": None, "skip": 5, "limit": 10},
        },
    ),
    test.case(
        "router-depends q=foo",
        url="/router-depends/?q=foo",
        status_code=200,
        expected={
            "in": "router-depends",
            "params": {"q": "foo", "skip": 5, "limit": 10},
        },
    ),
    test.case(
        "router-depends q=foo&skip=100&limit=200",
        url="/router-depends/?q=foo&skip=100&limit=200",
        status_code=200,
        expected={
            "in": "router-depends",
            "params": {"q": "foo", "skip": 5, "limit": 10},
        },
    ),
    test.case(
        "router-decorator-depends",
        url="/router-decorator-depends/",
        status_code=200,
        expected={"in": "router-decorator-depends"},
    ),
)
def override_simple(url: str, status_code: int, expected: dict):
    app.dependency_overrides[common_parameters] = overrider_dependency_simple
    response = client.get(url)
    expect(response.status_code, "status code").to_equal(status_code)
    expect(response.json(), "response body").to_equal(expected)
    app.dependency_overrides = {}


@test("override with sub-dep on /main-depends/ requires k query param")
def override_with_sub_main_depends():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get("/main-depends/")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "k"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )

    app.dependency_overrides = {}


@test("override with sub-dep on /main-depends/?q=foo still demands k")
def override_with_sub__main_depends_q_foo():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get("/main-depends/?q=foo")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "k"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )

    app.dependency_overrides = {}


@test("override with sub-dep on /main-depends/?k=bar succeeds")
def override_with_sub_main_depends_k_bar():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get("/main-depends/?k=bar")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"in": "main-depends", "params": {"k": "bar"}}
    )
    app.dependency_overrides = {}


@test("override with sub-dep on /decorator-depends/ requires k")
def override_with_sub_decorator_depends():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get("/decorator-depends/")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "k"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )

    app.dependency_overrides = {}


@test("override with sub-dep on /decorator-depends/?q=foo still demands k")
def override_with_sub_decorator_depends_q_foo():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get("/decorator-depends/?q=foo")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "k"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )

    app.dependency_overrides = {}


@test("override with sub-dep on /decorator-depends/?k=bar succeeds")
def override_with_sub_decorator_depends_k_bar():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get("/decorator-depends/?k=bar")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal({"in": "decorator-depends"})
    app.dependency_overrides = {}


@test("override with sub-dep on /router-depends/ requires k")
def override_with_sub_router_depends():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get("/router-depends/")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "k"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )

    app.dependency_overrides = {}


@test("override with sub-dep on /router-depends/?q=foo still demands k")
def override_with_sub_router_depends_q_foo():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get("/router-depends/?q=foo")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "k"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )

    app.dependency_overrides = {}


@test("override with sub-dep on /router-depends/?k=bar succeeds")
def override_with_sub_router_depends_k_bar():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get("/router-depends/?k=bar")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"in": "router-depends", "params": {"k": "bar"}}
    )
    app.dependency_overrides = {}


@test("override with sub-dep on /router-decorator-depends/ requires k")
def override_with_sub_router_decorator_depends():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get("/router-decorator-depends/")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "k"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )

    app.dependency_overrides = {}


@test("override with sub-dep on /router-decorator-depends/?q=foo still demands k")
def override_with_sub_router_decorator_depends_q_foo():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get("/router-decorator-depends/?q=foo")
    expect(response.status_code, "status code").to_equal(422)
    expect(response.json(), "response body").to_equal(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "k"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    )

    app.dependency_overrides = {}


@test("override with sub-dep on /router-decorator-depends/?k=bar succeeds")
def override_with_sub_router_decorator_depends_k_bar():
    app.dependency_overrides[common_parameters] = overrider_dependency_with_sub
    response = client.get("/router-decorator-depends/?k=bar")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"in": "router-decorator-depends"}
    )
    app.dependency_overrides = {}
