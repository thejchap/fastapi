from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()
router = APIRouter()


@router.route("/items/")
def read_items(request: Request):
    return JSONResponse({"hello": "world"})


app.include_router(router)

client = TestClient(app)


@test("APIRouter.route handles plain Starlette routes")
def sub_router():
    response = client.get("/items/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"hello": "world"})
