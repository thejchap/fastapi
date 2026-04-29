from inline_snapshot import snapshot
from tryke import expect, test

from docs_src.app_testing.tutorial001_py310 import client, test_read_main


@test("tutorial001 test_read_main runs")
def main():
    test_read_main()


# Pytest discovered the imported `test_read_main` here at module scope; mirror
# that by re-invoking it under a dedicated tryke test.
@test("tutorial001 re-imported test_read_main runs again")
def read_main():
    test_read_main()


@test("OpenAPI schema for tutorial001")
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "OpenAPI schema").to_equal(
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
