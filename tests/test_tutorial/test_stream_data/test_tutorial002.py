from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_and_mod(name: str):
    mod = import_tutorial("stream_data", name)
    return TestClient(mod.app), mod


@test.cases(
    test.case("stream", name="tutorial002_py310", path="/image/stream"),
    test.case(
        "stream-no-async", name="tutorial002_py310", path="/image/stream-no-async"
    ),
    test.case(
        "stream-no-async-yield-from",
        name="tutorial002_py310",
        path="/image/stream-no-async-yield-from",
    ),
    test.case(
        "stream-no-annotation",
        name="tutorial002_py310",
        path="/image/stream-no-annotation",
    ),
    test.case(
        "stream-no-async-no-annotation",
        name="tutorial002_py310",
        path="/image/stream-no-async-no-annotation",
    ),
)
def stream_image(name: str, path: str):
    client, mod = _client_and_mod(name)
    response = client.get(path)
    expect(response.status_code).to_equal(200).fatal()
    expect(response.headers["content-type"]).to_equal("image/png")
    expect(response.content).to_equal(mod.binary_image)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
)
def openapi_schema(name: str):
    client, _ = _client_and_mod(name)
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/image/stream": {
                        "get": {
                            "summary": "Stream Image",
                            "operationId": "stream_image_image_stream_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "image/png": {"schema": {"type": "string"}}
                                    },
                                }
                            },
                        }
                    },
                    "/image/stream-no-async": {
                        "get": {
                            "summary": "Stream Image No Async",
                            "operationId": "stream_image_no_async_image_stream_no_async_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "image/png": {"schema": {"type": "string"}}
                                    },
                                }
                            },
                        }
                    },
                    "/image/stream-no-async-yield-from": {
                        "get": {
                            "summary": "Stream Image No Async Yield From",
                            "operationId": "stream_image_no_async_yield_from_image_stream_no_async_yield_from_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "image/png": {"schema": {"type": "string"}}
                                    },
                                }
                            },
                        }
                    },
                    "/image/stream-no-annotation": {
                        "get": {
                            "summary": "Stream Image No Annotation",
                            "operationId": "stream_image_no_annotation_image_stream_no_annotation_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "image/png": {"schema": {"type": "string"}}
                                    },
                                }
                            },
                        }
                    },
                    "/image/stream-no-async-no-annotation": {
                        "get": {
                            "summary": "Stream Image No Async No Annotation",
                            "operationId": "stream_image_no_async_no_annotation_image_stream_no_async_no_annotation_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "image/png": {"schema": {"type": "string"}}
                                    },
                                }
                            },
                        }
                    },
                },
            }
        )
    )
