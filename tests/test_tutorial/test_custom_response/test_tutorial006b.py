from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.custom_response.tutorial006b_py310 import app

client = TestClient(app)


@test("GET /fastapi redirects to fastapi.tiangolo.com via response_class")
def redirect_response_class():
    response = client.get("/fastapi", follow_redirects=False)
    expect(response.status_code, "status code").to_equal(307)
    expect(response.headers["location"], "location header").to_equal("https://fastapi.tiangolo.com")


@test("OpenAPI schema matches snapshot")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "openapi schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/fastapi": {
                        "get": {
                            "summary": "Redirect Fastapi",
                            "operationId": "redirect_fastapi_fastapi_get",
                            "responses": {
                                "307": {"description": "Successful Response"}
                            },
                        }
                    }
                },
            }
        )
    )
