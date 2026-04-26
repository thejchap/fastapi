from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()


def set_cookie(*, response: Response):
    response.set_cookie("cookie-name", "cookie-value")
    return {}


def set_indirect_cookie(*, dep: str = Depends(set_cookie)):
    return dep


@app.get("/directCookie")
def get_direct_cookie(dep: str = Depends(set_cookie)):
    return {"dep": dep}


@app.get("/indirectCookie")
def get_indirect_cookie(dep: str = Depends(set_indirect_cookie)):
    return {"dep": dep}


client = TestClient(app)


@test
def cookie_is_set_once():
    direct_response = client.get("/directCookie")
    indirect_response = client.get("/indirectCookie")
    expect(direct_response.headers["set-cookie"]).to_equal(
        indirect_response.headers["set-cookie"]
    )
