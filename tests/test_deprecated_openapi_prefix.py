from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI(openapi_prefix="/api/v1")


@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


client = TestClient(app)


@test("openapi_prefix sets the root_path for the request")
def main():
    response = client.get("/app")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "response body").to_equal(
        {"message": "Hello World", "root_path": "/api/v1"}
    )


@test("OpenAPI schema servers include the openapi_prefix")
def openapi():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200)
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/app": {
                        "get": {
                            "summary": "Read Main",
                            "operationId": "read_main_app_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                        }
                    }
                },
                "servers": [{"url": "/api/v1"}],
            }
        )
    )
