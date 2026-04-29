from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()


@app.get("/", openapi_extra={"x-custom-extension": "value"})
def route_with_extras():
    return {}


client = TestClient(app)


@test("Routes with openapi_extra still serve their handler")
def get_route():
    response = client.get("/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({})


@test("Per-route openapi_extra ends up in the OpenAPI schema")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                            },
                            "summary": "Route With Extras",
                            "operationId": "route_with_extras__get",
                            "x-custom-extension": "value",
                        }
                    },
                },
            }
        )
    )
