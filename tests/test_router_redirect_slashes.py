from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test


@test("redirect_slashes=True redirects /hello to /hello/")
def redirect_slashes_enabled():
    app = FastAPI()
    router = APIRouter()

    @router.get("/hello/")
    def hello_page() -> str:
        return "Hello, World!"

    app.include_router(router)

    client = TestClient(app)

    response = client.get("/hello/", follow_redirects=False)
    expect(response.status_code, "status code for /hello/").to_equal(200).fatal()

    response = client.get("/hello", follow_redirects=False)
    expect(response.status_code, "status code for /hello").to_equal(307).fatal()


@test("redirect_slashes=False returns 404 for /hello")
def redirect_slashes_disabled():
    app = FastAPI(redirect_slashes=False)
    router = APIRouter()

    @router.get("/hello/")
    def hello_page() -> str:
        return "Hello, World!"

    app.include_router(router)

    client = TestClient(app)

    response = client.get("/hello/", follow_redirects=False)
    expect(response.status_code, "status code for /hello/").to_equal(200).fatal()

    response = client.get("/hello", follow_redirects=False)
    expect(response.status_code, "status code for /hello").to_equal(404).fatal()
