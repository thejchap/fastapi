from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.app_testing.app_a_py310.test_main import client, test_read_main


@test
def main():
    test_read_main()


# Pytest discovered the imported `test_read_main` here at module scope; mirror
# that by re-invoking it under a dedicated tryke test.
@test
def read_main():
    test_read_main()


@test
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/": {
                        "get": {
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                }
                            },
                            "summary": "Read Main",
                            "operationId": "read_main__get",
                        }
                    }
                },
            }
        )
    )
