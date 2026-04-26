from fastapi.testclient import TestClient
from inline_snapshot import Is, snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("custom_response", name)
    return TestClient(mod.app)


html_contents = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """


@test.cases(
    test.case("tutorial002_py310", mod_name="tutorial002_py310"),
    test.case("tutorial003_py310", mod_name="tutorial003_py310"),
    test.case("tutorial004_py310", mod_name="tutorial004_py310"),
)
def get_custom_response(mod_name: str):
    client = _client_for(mod_name)
    response = client.get("/items/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.text).to_equal(html_contents)


@test.cases(
    test.case("tutorial002_py310", mod_name="tutorial002_py310"),
    test.case("tutorial003_py310", mod_name="tutorial003_py310"),
    test.case("tutorial004_py310", mod_name="tutorial004_py310"),
)
def openapi_schema(mod_name: str):
    client = _client_for(mod_name)
    if mod_name.startswith("tutorial003"):
        response_content = {"application/json": {"schema": {}}}
    else:
        response_content = {"text/html": {"schema": {"type": "string"}}}

    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/items/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": Is(response_content),
                                }
                            },
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                        }
                    }
                },
            }
        )
    )
