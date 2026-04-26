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


@test
def app_test():
    response = client.get("/foo")
    expect(response.status_code).to_equal(200)


@test
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
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
