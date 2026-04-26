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


@test
def use_empty():
    with client:
        response = client.get("/prefix")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal(["OK"])

        response = client.get("/prefix/")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal(["OK"])


@test
def include_empty():
    # If both include and router.path are empty - it should raise exception
    expect(lambda: app.include_router(router)).to_raise(FastAPIError)
