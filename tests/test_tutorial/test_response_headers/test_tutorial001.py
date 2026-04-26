from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.response_headers.tutorial001_py310 import app

client = TestClient(app)


@test
def path_operation():
    response = client.get("/headers/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"message": "Hello World"})
    expect(response.headers["X-Cat-Dog"]).to_equal("alone in the world")
    expect(response.headers["Content-Language"]).to_equal("en-US")
