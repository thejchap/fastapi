from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test


@test
def redirect_slashes_enabled():
    app = FastAPI()
    router = APIRouter()

    @router.get("/hello/")
    def hello_page() -> str:
        return "Hello, World!"

    app.include_router(router)

    client = TestClient(app)

    response = client.get("/hello/", follow_redirects=False)
    expect(response.status_code).to_equal(200).fatal()

    response = client.get("/hello", follow_redirects=False)
    expect(response.status_code).to_equal(307).fatal()


@test
def redirect_slashes_disabled():
    app = FastAPI(redirect_slashes=False)
    router = APIRouter()

    @router.get("/hello/")
    def hello_page() -> str:
        return "Hello, World!"

    app.include_router(router)

    client = TestClient(app)

    response = client.get("/hello/", follow_redirects=False)
    expect(response.status_code).to_equal(200).fatal()

    response = client.get("/hello", follow_redirects=False)
    expect(response.status_code).to_equal(404).fatal()
