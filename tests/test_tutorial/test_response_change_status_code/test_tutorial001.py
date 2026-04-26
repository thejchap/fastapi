from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.response_change_status_code.tutorial001_py310 import app

client = TestClient(app)


@test
def path_operation():
    response = client.put("/get-or-create-task/foo")
    print(response.content)
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("Listen to the Bar Fighters")
    response = client.put("/get-or-create-task/bar")
    expect(response.status_code).to_equal(201).fatal()
    expect(response.json()).to_equal("This didn't exist before")
