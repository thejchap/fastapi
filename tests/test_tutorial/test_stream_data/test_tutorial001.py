from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("stream_data", name)
    return TestClient(mod.app)


expected_text = (
    ""
    "Rick: (stumbles in drunkenly, and turns on the lights)"
    " Morty! You gotta come on. You got--... you gotta come with me."
    "Morty: (rubs his eyes) What, Rick? What's going on?"
    "Rick: I got a surprise for you, Morty."
    "Morty: It's the middle of the night. What are you talking about?"
    "Rick: (spills alcohol on Morty's bed) Come on, I got a surprise for you."
    " (drags Morty by the ankle) Come on, hurry up."
    " (pulls Morty out of his bed and into the hall)"
    "Morty: Ow! Ow! You're tugging me too hard!"
    "Rick: We gotta go, gotta get outta here, come on."
    " Got a surprise for you Morty."
)


@test.cases(
    test.case("stream", name="tutorial001_py310", path="/story/stream"),
    test.case(
        "stream-no-async", name="tutorial001_py310", path="/story/stream-no-async"
    ),
    test.case(
        "stream-no-annotation",
        name="tutorial001_py310",
        path="/story/stream-no-annotation",
    ),
    test.case(
        "stream-no-async-no-annotation",
        name="tutorial001_py310",
        path="/story/stream-no-async-no-annotation",
    ),
    test.case("stream-bytes", name="tutorial001_py310", path="/story/stream-bytes"),
    test.case(
        "stream-no-async-bytes",
        name="tutorial001_py310",
        path="/story/stream-no-async-bytes",
    ),
    test.case(
        "stream-no-annotation-bytes",
        name="tutorial001_py310",
        path="/story/stream-no-annotation-bytes",
    ),
    test.case(
        "stream-no-async-no-annotation-bytes",
        name="tutorial001_py310",
        path="/story/stream-no-async-no-annotation-bytes",
    ),
)
def stream_story(name: str, path: str):
    client = _client_for(name)
    response = client.get(path)
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.text, "streamed body").to_equal(expected_text)


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
)
def openapi_schema(name: str):
    client = _client_for(name)
    response = client.get("/openapi.json")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "OpenAPI schema").to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/story/stream": {
                        "get": {
                            "summary": "Stream Story",
                            "operationId": "stream_story_story_stream_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                }
                            },
                        }
                    },
                    "/story/stream-no-async": {
                        "get": {
                            "summary": "Stream Story No Async",
                            "operationId": "stream_story_no_async_story_stream_no_async_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                }
                            },
                        }
                    },
                    "/story/stream-no-annotation": {
                        "get": {
                            "summary": "Stream Story No Annotation",
                            "operationId": "stream_story_no_annotation_story_stream_no_annotation_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                }
                            },
                        }
                    },
                    "/story/stream-no-async-no-annotation": {
                        "get": {
                            "summary": "Stream Story No Async No Annotation",
                            "operationId": "stream_story_no_async_no_annotation_story_stream_no_async_no_annotation_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                }
                            },
                        }
                    },
                    "/story/stream-bytes": {
                        "get": {
                            "summary": "Stream Story Bytes",
                            "operationId": "stream_story_bytes_story_stream_bytes_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                }
                            },
                        }
                    },
                    "/story/stream-no-async-bytes": {
                        "get": {
                            "summary": "Stream Story No Async Bytes",
                            "operationId": "stream_story_no_async_bytes_story_stream_no_async_bytes_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                }
                            },
                        }
                    },
                    "/story/stream-no-annotation-bytes": {
                        "get": {
                            "summary": "Stream Story No Annotation Bytes",
                            "operationId": "stream_story_no_annotation_bytes_story_stream_no_annotation_bytes_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                }
                            },
                        }
                    },
                    "/story/stream-no-async-no-annotation-bytes": {
                        "get": {
                            "summary": "Stream Story No Async No Annotation Bytes",
                            "operationId": "stream_story_no_async_no_annotation_bytes_story_stream_no_async_no_annotation_bytes_get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                }
                            },
                        }
                    },
                },
            }
        )
    )
