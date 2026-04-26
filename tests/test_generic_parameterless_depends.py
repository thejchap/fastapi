from typing import Annotated, TypeVar

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

app = FastAPI()

T = TypeVar("T")

Dep = Annotated[T, Depends()]


class A:
    pass


class B:
    pass


@app.get("/a")
async def a(dep: Dep[A]):
    return {"cls": dep.__class__.__name__}


@app.get("/b")
async def b(dep: Dep[B]):
    return {"cls": dep.__class__.__name__}


client = TestClient(app)


@test
def generic_parameterless_depends():
    response = client.get("/a")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"cls": "A"})

    response = client.get("/b")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"cls": "B"})


@test
def openapi_schema():
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "openapi": "3.1.0",
                "paths": {
                    "/a": {
                        "get": {
                            "operationId": "a_a_get",
                            "responses": {
                                "200": {
                                    "content": {"application/json": {"schema": {}}},
                                    "description": "Successful Response",
                                }
                            },
                            "summary": "A",
                        }
                    },
                    "/b": {
                        "get": {
                            "operationId": "b_b_get",
                            "responses": {
                                "200": {
                                    "content": {"application/json": {"schema": {}}},
                                    "description": "Successful Response",
                                }
                            },
                            "summary": "B",
                        }
                    },
                },
            }
        )
    )
