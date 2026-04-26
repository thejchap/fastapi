from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from starlette.routing import Route
from tryke import expect, test

app = FastAPI()


class APIRouteA(APIRoute):
    x_type = "A"


class APIRouteB(APIRoute):
    x_type = "B"


class APIRouteC(APIRoute):
    x_type = "C"


router_a = APIRouter(route_class=APIRouteA)
router_b = APIRouter(route_class=APIRouteB)
router_c = APIRouter(route_class=APIRouteC)


@router_a.get("/")
def get_a():
    return {"msg": "A"}


@router_b.get("/")
def get_b():
    return {"msg": "B"}


@router_c.get("/")
def get_c():
    return {"msg": "C"}


router_b.include_router(router=router_c, prefix="/c")
router_a.include_router(router=router_b, prefix="/b")
app.include_router(router=router_a, prefix="/a")


client = TestClient(app)


@test.cases(
    test.case("/a", path="/a", expected_status=200, expected_response={"msg": "A"}),
    test.case("/a/b", path="/a/b", expected_status=200, expected_response={"msg": "B"}),
    test.case(
        "/a/b/c", path="/a/b/c", expected_status=200, expected_response={"msg": "C"}
    ),
)
def get_path(path: str, expected_status: int, expected_response: dict):
    response = client.get(path)
    expect(response.status_code).to_equal(expected_status)
    expect(response.json()).to_equal(expected_response)


@test
def route_classes():
    routes = {}
    for r in app.router.routes:
        expect(r).to_be_instance_of(Route).fatal()
        routes[r.path] = r
    expect(getattr(routes["/a/"], "x_type")).to_equal("A")  # noqa: B009
    expect(getattr(routes["/a/b/"], "x_type")).to_equal("B")  # noqa: B009
    expect(getattr(routes["/a/b/c/"], "x_type")).to_equal("C")  # noqa: B009


@test
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/a/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Get A",
                            "operationId": "get_a_a__get",
                        }
                    },
                    "/a/b/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Get B",
                            "operationId": "get_b_a_b__get",
                        }
                    },
                    "/a/b/c/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Get C",
                            "operationId": "get_c_a_b_c__get",
                        }
                    },
                },
            }
        )
    )
