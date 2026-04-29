from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.configure_swagger_ui.tutorial002_py310 import app

client = TestClient(app)


@test("Swagger UI HTML reflects custom syntaxHighlight theme")
def swagger_ui():
    response = client.get("/docs")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.text, "response text").not_.to_contain('"syntaxHighlight": false')
    expect(response.text, "response text").to_contain('"syntaxHighlight": {"theme": "obsidian"}')
    expect(response.text, "response text").to_contain('"dom_id": "#swagger-ui"')
    expect(response.text, "response text").to_contain("presets: [")
    expect(response.text, "response text").to_contain("SwaggerUIBundle.presets.apis,")
    expect(response.text, "response text").to_contain("SwaggerUIBundle.SwaggerUIStandalonePreset")
    expect(response.text, "response text").to_contain('"layout": "BaseLayout",')
    expect(response.text, "response text").to_contain('"deepLinking": true,')
    expect(response.text, "response text").to_contain('"showExtensions": true,')
    expect(response.text, "response text").to_contain('"showCommonExtensions": true,')


@test("GET /users/foo returns greeting")
def get_users():
    response = client.get("/users/foo")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "Hello foo"})
