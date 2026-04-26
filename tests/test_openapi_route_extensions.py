from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()


@app.get("/", openapi_extra={"x-custom-extension": "value"})
def route_with_extras():
    return {}


client = TestClient(app)


@test
def get_route():
    response = client.get("/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({})


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
