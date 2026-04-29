from fastapi import FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

swagger_ui_init_oauth = {"clientId": "the-foo-clients", "appName": "The Predendapp"}

app = FastAPI(swagger_ui_init_oauth=swagger_ui_init_oauth)


@app.get("/items/")
async def read_items():
    return {"id": "foo"}


client = TestClient(app)


@test("Swagger UI HTML embeds initOAuth with configured values")
def swagger_ui():
    response = client.get("/docs")
    expect(response.status_code, "status code").to_equal(200).fatal()
    print(response.text)
    expect(response.text, "Swagger UI body").to_contain("ui.initOAuth")
    expect(response.text, "Swagger UI body").to_contain('"appName": "The Predendapp"')
    expect(response.text, "Swagger UI body").to_contain('"clientId": "the-foo-clients"')


@test("Endpoint still works alongside Swagger UI initOAuth config")
def response():
    response = client.get("/items/")
    expect(response.json(), "response body").to_equal({"id": "foo"})
