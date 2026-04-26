from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.custom_response.tutorial007_py310 import app

client = TestClient(app)


@test
def get():
    fake_content = b"some fake video bytes"
    response = client.get("/")
    expect(response.content).to_equal(fake_content * 10)
