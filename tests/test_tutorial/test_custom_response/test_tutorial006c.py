from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.custom_response.tutorial006c_py310 import app

client = TestClient(app)


@test
def redirect_status_code():
    response = client.get("/pydantic", follow_redirects=False)
    expect(response.status_code).to_equal(302)
    expect(response.headers["location"]).to_equal("https://docs.pydantic.dev/")


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
                    "/pydantic": {
                        "get": {
                            "summary": "Redirect Pydantic",
                            "operationId": "redirect_pydantic_pydantic_get",
                            "responses": {
                                "302": {"description": "Successful Response"}
                            },
                        }
                    }
                },
            }
        )
    )
