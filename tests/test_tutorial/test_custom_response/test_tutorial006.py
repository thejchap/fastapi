from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.custom_response.tutorial006_py310 import app

client = TestClient(app)


@test("GET /typer returns RedirectResponse to typer.tiangolo.com")
def get():
    response = client.get("/typer", follow_redirects=False)
    expect(response.status_code, "status code").to_equal(307).fatal()
    expect(response.headers["location"], "location header").to_equal("https://typer.tiangolo.com")


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
                    "/typer": {
                        "get": {
                            "summary": "Redirect Typer",
                            "operationId": "redirect_typer_typer_get",
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
