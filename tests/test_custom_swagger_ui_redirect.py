from fastapi import FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

swagger_ui_oauth2_redirect_url = "/docs/redirect"

app = FastAPI(swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url)


@app.get("/items/")
async def read_items():
    return {"id": "foo"}


client = TestClient(app)


@test("Swagger UI uses the custom oauth2 redirect URL")
def swagger_ui():
    response = client.get("/docs")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.headers["content-type"], "content-type").to_equal(
        "text/html; charset=utf-8"
    )
    expect(response.text, "response body").to_contain("swagger-ui-dist")
    print(client.base_url)
    expect(response.text, "response body").to_contain(
        f"oauth2RedirectUrl: window.location.origin + '{swagger_ui_oauth2_redirect_url}'"
    )


@test("custom oauth2 redirect URL serves the redirect page")
def swagger_ui_oauth2_redirect():
    response = client.get(swagger_ui_oauth2_redirect_url)
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.headers["content-type"], "content-type").to_equal(
        "text/html; charset=utf-8"
    )
    expect(response.text, "response body").to_contain(
        "window.opener.swaggerUIRedirectOauth2"
    )


@test("regular routes still work with custom oauth2 redirect URL")
def response():
    response = client.get("/items/")
    expect(response.json(), "response body").to_equal({"id": "foo"})
