from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()

router = APIRouter()


@router.get("/users/{id}")
def read_user(segment: str, id: str):
    return {"segment": segment, "id": id}


app.include_router(router, prefix="/{segment}")


client = TestClient(app)


@test("router prefix template parameter is captured")
def get():
    response = client.get("/seg/users/foo")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"segment": "seg", "id": "foo"})
