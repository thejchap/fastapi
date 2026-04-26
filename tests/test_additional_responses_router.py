from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel
from tryke import expect, test


class ResponseModel(BaseModel):
    message: str


app = FastAPI()
router = APIRouter()


@router.get("/a", responses={501: {"description": "Error 1"}})
async def a():
    return "a"


@router.get(
    "/b",
    responses={
        502: {"description": "Error 2"},
        "4XX": {"description": "Error with range, upper"},
    },
)
async def b():
    return "b"


@router.get(
    "/c",
    responses={
        "400": {"description": "Error with str"},
        "5xx": {"description": "Error with range, lower"},
        "default": {"description": "A default response"},
    },
)
async def c():
    return "c"


@router.get(
    "/d",
    responses={
        "400": {"description": "Error with str"},
        "5XX": {"model": ResponseModel},
        "default": {"model": ResponseModel},
    },
)
async def d():
    return "d"


app.include_router(router)


client = TestClient(app)


@test
def a_route():
    response = client.get("/a")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("a")


@test
def b_route():
    response = client.get("/b")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("b")


@test
def c_route():
    response = client.get("/c")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("c")


@test
def d_route():
    response = client.get("/d")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("d")


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
                    "/a": {
                        "get": {
                            "responses": {
                                "501": {"description": "Error 1"},
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                            },
                            "summary": "A",
                            "operationId": "a_a_get",
                        }
                    },
                    "/b": {
                        "get": {
                            "responses": {
                                "502": {"description": "Error 2"},
                                "4XX": {"description": "Error with range, upper"},
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                            },
                            "summary": "B",
                            "operationId": "b_b_get",
                        }
                    },
                    "/c": {
                        "get": {
                            "responses": {
                                "400": {"description": "Error with str"},
                                "5XX": {"description": "Error with range, lower"},
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "default": {"description": "A default response"},
                            },
                            "summary": "C",
                            "operationId": "c_c_get",
                        }
                    },
                    "/d": {
                        "get": {
                            "responses": {
                                "400": {"description": "Error with str"},
                                "5XX": {
                                    "description": "Server Error",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/ResponseModel"
                                            }
                                        }
                                    },
                                },
                                "200": {
                                    "description": "Successful Response",
                                    "content": {"application/json": {"schema": {}}},
                                },
                                "default": {
                                    "description": "Default Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "$ref": "#/components/schemas/ResponseModel"
                                            }
                                        }
                                    },
                                },
                            },
                            "summary": "D",
                            "operationId": "d_d_get",
                        }
                    },
                },
                "components": {
                    "schemas": {
                        "ResponseModel": {
                            "title": "ResponseModel",
                            "required": ["message"],
                            "type": "object",
                            "properties": {
                                "message": {"title": "Message", "type": "string"}
                            },
                        }
                    }
                },
            }
        )
    )
