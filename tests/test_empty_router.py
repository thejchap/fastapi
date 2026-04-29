from fastapi import APIRouter, FastAPI
from fastapi.exceptions import FastAPIError
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()

router = APIRouter()


@router.get("")
def get_empty():
    return ["OK"]


app.include_router(router, prefix="/prefix")


client = TestClient(app)


@test("router with empty path mounted under prefix is reachable")
def use_empty():
    with client:
        response = client.get("/prefix")
        expect(response.status_code, "status code (no slash)").to_equal(200).fatal()
        expect(response.json(), "response body (no slash)").to_equal(["OK"])

        response = client.get("/prefix/")
        expect(response.status_code, "status code (slash)").to_equal(200).fatal()
        expect(response.json(), "response body (slash)").to_equal(["OK"])


@test("including empty router under empty prefix raises FastAPIError")
def include_empty():
    # If both include and router.path are empty - it should raise exception
    expect(
        lambda: app.include_router(router),
        "include_router with empty prefix",
    ).to_raise(FastAPIError)
