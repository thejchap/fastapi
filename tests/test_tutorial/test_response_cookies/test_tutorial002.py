from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.response_cookies.tutorial002_py310 import app

client = TestClient(app)


@test
def path_operation():
    response = client.post("/cookie-and-object/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {"message": "Come to the dark side, we have cookies"}
    )
    expect(response.cookies["fakesession"]).to_equal("fake-cookie-session-value")
