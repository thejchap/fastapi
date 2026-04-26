from fastapi import FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

swagger_ui_oauth2_redirect_url = "/docs/redirect"

app = FastAPI(swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url)


@app.get("/items/")
async def read_items():
    return {"id": "foo"}


client = TestClient(app)


@test
def swagger_ui():
    response = client.get("/docs")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.headers["content-type"]).to_equal("text/html; charset=utf-8")
    expect(response.text).to_contain("swagger-ui-dist")
    print(client.base_url)
    expect(response.text).to_contain(
        f"oauth2RedirectUrl: window.location.origin + '{swagger_ui_oauth2_redirect_url}'"
    )


@test
def swagger_ui_oauth2_redirect():
    response = client.get(swagger_ui_oauth2_redirect_url)
    expect(response.status_code).to_equal(200).fatal()
    expect(response.headers["content-type"]).to_equal("text/html; charset=utf-8")
    expect(response.text).to_contain("window.opener.swaggerUIRedirectOauth2")


@test
def response():
    response = client.get("/items/")
    expect(response.json()).to_equal({"id": "foo"})
