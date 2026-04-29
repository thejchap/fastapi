import warnings

from inline_snapshot import snapshot
from starlette.testclient import TestClient
from tryke import Depends, expect, fixture, test

warnings.filterwarnings(
    "ignore",
    message=r"The 'lia' package has been renamed to 'cross_web'\..*",
    category=DeprecationWarning,
)

from docs_src.graphql_.tutorial001_py310 import app  # noqa: E402


@fixture
def client() -> TestClient:
    return TestClient(app)


@test("GraphQL query returns the user data")
def query(client: TestClient = Depends(client)):
    response = client.post("/graphql", json={"query": "{ user { name, age } }"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"data": {"user": {"name": "Patrick", "age": 100}}}
    )


@test("OpenAPI schema matches snapshot")
def openapi(client: TestClient = Depends(client)):
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        snapshot(
            {
                "info": {
                    "title": "FastAPI",
                    "version": "0.1.0",
                },
                "openapi": "3.1.0",
                "paths": {
                    "/graphql": {
                        "get": {
                            "operationId": "handle_http_get_graphql_get",
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {
                                            "schema": {},
                                        },
                                    },
                                    "description": "The GraphiQL integrated development environment.",
                                },
                                "404": {
                                    "description": "Not found if GraphiQL or query via GET are not enabled.",
                                },
                            },
                            "summary": "Handle Http Get",
                        },
                        "post": {
                            "operationId": "handle_http_post_graphql_post",
                            "responses": {
                                "200": {
                                    "content": {
                                        "application/json": {
                                            "schema": {},
                                        },
                                    },
                                    "description": "Successful Response",
                                },
                            },
                            "summary": "Handle Http Post",
                        },
                    },
                },
            }
        )
    )
