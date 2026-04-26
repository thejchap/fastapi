from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.metadata.tutorial001_1_py310 import app

client = TestClient(app)


@test
def items():
    response = client.get("/items/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal([{"name": "Katana"}])


@test
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {
                    "title": "ChimichangApp",
                    "summary": "Deadpool's favorite app. Nuff said.",
                    "description": "\nChimichangApp API helps you do awesome stuff. \U0001f680\n\n## Items\n\nYou can **read items**.\n\n## Users\n\nYou will be able to:\n\n* **Create users** (_not implemented_).\n* **Read users** (_not implemented_).\n",
                    "termsOfService": "http://example.com/terms/",
                    "contact": {
                        "name": "Deadpoolio the Amazing",
                        "url": "http://x-force.example.com/contact/",
                        "email": "dp@x-force.example.com",
                    },
                    "license": {
                        "name": "Apache 2.0",
                        "identifier": "Apache-2.0",
                    },
                    "version": "0.0.1",
                },
                "paths": {
                    "/items/": {
                        "get": {
                            "summary": "Read Items",
                            "operationId": "read_items_items__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                        }
                    }
                },
            }
        )
    )
