from fastapi.testclient import TestClient
from tryke import expect, test

from .app import app


@test
def recursive():
    client = TestClient(app)
    response = client.get("/items/recursive")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "sub_items": [{"name": "subitem", "sub_items": []}],
            "name": "item",
        }
    )

    response = client.get("/items/recursive-submodel")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "name": "item",
            "sub_items1": [
                {
                    "name": "subitem",
                    "sub_items2": [
                        {
                            "name": "subsubitem",
                            "sub_items1": [{"name": "subsubsubitem", "sub_items2": []}],
                        }
                    ],
                }
            ],
        }
    )
