from fastapi import FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

swagger_ui_init_oauth = {"clientId": "the-foo-clients", "appName": "The Predendapp"}

app = FastAPI(swagger_ui_init_oauth=swagger_ui_init_oauth)


@app.get("/items/")
async def read_items():
    return {"id": "foo"}


client = TestClient(app)


@test
def swagger_ui():
    response = client.get("/docs")
    expect(response.status_code).to_equal(200).fatal()
    print(response.text)
    expect(response.text).to_contain("ui.initOAuth")
    expect(response.text).to_contain('"appName": "The Predendapp"')
    expect(response.text).to_contain('"clientId": "the-foo-clients"')


@test
def response():
    response = client.get("/items/")
    expect(response.json()).to_equal({"id": "foo"})
