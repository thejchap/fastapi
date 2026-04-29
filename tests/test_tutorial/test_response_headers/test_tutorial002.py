from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.response_headers.tutorial002_py310 import app

client = TestClient(app)


@test("path operation sets custom headers returning a JSONResponse")
def path_operation():
    response = client.get("/headers-and-object/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "Hello World"})
    expect(response.headers["X-Cat-Dog"], "X-Cat-Dog header").to_equal(
        "alone in the world"
    )
