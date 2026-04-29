from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.response_cookies.tutorial002_py310 import app

client = TestClient(app)


@test("path operation sets a cookie returning a JSONResponse")
def path_operation():
    response = client.post("/cookie-and-object/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"message": "Come to the dark side, we have cookies"}
    )
    expect(response.cookies["fakesession"], "cookie value").to_equal(
        "fake-cookie-session-value"
    )
