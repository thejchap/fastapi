from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()


async def response_status_setter(response: Response):
    response.status_code = 201


async def parent_dep(result=Depends(response_status_setter)):
    return result


@app.get("/", dependencies=[Depends(parent_dep)])
async def get_main():
    return {"msg": "Hello World"}


client = TestClient(app)


@test("nested dependency can set Response.status_code")
def dependency_set_status_code():
    response = client.get("/")
    expect(response.status_code, "status code").to_equal(201).fatal()
    expect(response.json(), "response body").to_equal({"msg": "Hello World"})
