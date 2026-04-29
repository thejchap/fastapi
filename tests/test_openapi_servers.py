from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI(
    servers=[
        {"url": "/", "description": "Default, relative server"},
        {
            "url": "http://staging.localhost.tiangolo.com:8000",
            "description": "Staging but actually localhost still",
        },
        {"url": "https://prod.example.com"},
    ]
)


@app.get("/foo")
def foo():
    return {"message": "Hello World"}


client = TestClient(app)


@test("Routes still work when servers list is configured")
def app_test():
    response = client.get("/foo")
    expect(response.status_code, "status code").to_equal(200)


@test("Configured servers are reflected in the OpenAPI schema")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "servers": [
                    {"url": "/", "description": "Default, relative server"},
                    {
                        "url": "http://staging.localhost.tiangolo.com:8000",
                        "description": "Staging but actually localhost still",
                    },
                    {"url": "https://prod.example.com"},
                ],
                "paths": {
                    "/foo": {
                        "get": {
                            "summary": "Foo",
                            "operationId": "foo_foo_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                        }
                    }
                },
            }
        )
    )
