from fastapi import FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI(swagger_ui_oauth2_redirect_url=None)


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
    expect(response.text).not_.to_contain("oauth2RedirectUrl")


@test
def swagger_ui_no_oauth2_redirect():
    response = client.get("/docs/oauth2-redirect")
    expect(response.status_code).to_equal(404)


@test
def response():
    response = client.get("/items/")
    expect(response.json()).to_equal({"id": "foo"})
