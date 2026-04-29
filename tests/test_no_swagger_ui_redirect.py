from fastapi import FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI(swagger_ui_oauth2_redirect_url=None)


@app.get("/items/")
async def read_items():
    return {"id": "foo"}


client = TestClient(app)


@test("/docs page omits oauth2 redirect helper when disabled")
def swagger_ui():
    response = client.get("/docs")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.headers["content-type"], "content-type header").to_equal(
        "text/html; charset=utf-8"
    )
    expect(response.text, "swagger UI HTML").to_contain("swagger-ui-dist")
    print(client.base_url)
    expect(response.text, "swagger UI HTML").not_.to_contain("oauth2RedirectUrl")


@test("/docs/oauth2-redirect returns 404 when disabled")
def swagger_ui_no_oauth2_redirect():
    response = client.get("/docs/oauth2-redirect")
    expect(response.status_code, "status code").to_equal(404)


@test("Regular routes still respond")
def response():
    response = client.get("/items/")
    expect(response.json(), "response body").to_equal({"id": "foo"})
