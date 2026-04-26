import http

from fastapi import FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test


@test
def no_content():
    app = FastAPI()

    @app.get("/no-content", status_code=http.HTTPStatus.NO_CONTENT)
    def return_no_content() -> "None":
        return

    client = TestClient(app)
    response = client.get("/no-content")
    expect(response.status_code).to_equal(http.HTTPStatus.NO_CONTENT).fatal()
    expect(response.content).to_be_falsy()
