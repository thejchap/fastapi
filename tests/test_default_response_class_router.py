from fastapi import APIRouter, FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.testclient import TestClient
from tryke import expect, test


class OverrideResponse(JSONResponse):
    media_type = "application/x-override"


app = FastAPI()
router_a = APIRouter()
router_a_a = APIRouter()
router_a_b_override = APIRouter()  # Overrides default class
router_b_override = APIRouter()  # Overrides default class
router_b_a = APIRouter()
router_b_a_c_override = APIRouter()  # Overrides default class again


@app.get("/")
def get_root():
    return {"msg": "Hello World"}


@app.get("/override", response_class=PlainTextResponse)
def get_path_override():
    return "Hello World"


@router_a.get("/")
def get_a():
    return {"msg": "Hello A"}


@router_a.get("/override", response_class=PlainTextResponse)
def get_a_path_override():
    return "Hello A"


@router_a_a.get("/")
def get_a_a():
    return {"msg": "Hello A A"}


@router_a_a.get("/override", response_class=PlainTextResponse)
def get_a_a_path_override():
    return "Hello A A"


@router_a_b_override.get("/")
def get_a_b():
    return "Hello A B"


@router_a_b_override.get("/override", response_class=HTMLResponse)
def get_a_b_path_override():
    return "Hello A B"


@router_b_override.get("/")
def get_b():
    return "Hello B"


@router_b_override.get("/override", response_class=HTMLResponse)
def get_b_path_override():
    return "Hello B"


@router_b_a.get("/")
def get_b_a():
    return "Hello B A"


@router_b_a.get("/override", response_class=HTMLResponse)
def get_b_a_path_override():
    return "Hello B A"


@router_b_a_c_override.get("/")
def get_b_a_c():
    return "Hello B A C"


@router_b_a_c_override.get("/override", response_class=OverrideResponse)
def get_b_a_c_path_override():
    return {"msg": "Hello B A C"}


router_b_a.include_router(
    router_b_a_c_override, prefix="/c", default_response_class=HTMLResponse
)
router_b_override.include_router(router_b_a, prefix="/a")
router_a.include_router(router_a_a, prefix="/a")
router_a.include_router(
    router_a_b_override, prefix="/b", default_response_class=PlainTextResponse
)
app.include_router(router_a, prefix="/a")
app.include_router(
    router_b_override, prefix="/b", default_response_class=PlainTextResponse
)


client = TestClient(app)

json_type = "application/json"
text_type = "text/plain; charset=utf-8"
html_type = "text/html; charset=utf-8"
override_type = "application/x-override"


@test("app root falls back to JSON response")
def app_test():
    with client:
        response = client.get("/")
    expect(response.json(), "response body").to_equal({"msg": "Hello World"})
    expect(response.headers["content-type"], "content-type").to_equal(json_type)


@test("app /override uses PlainTextResponse from operation")
def app_override():
    with client:
        response = client.get("/override")
    expect(response.content, "response content").to_equal(b"Hello World")
    expect(response.headers["content-type"], "content-type").to_equal(text_type)


@test("router_a inherits app's default JSON response")
def router_a_test():
    with client:
        response = client.get("/a")
    expect(response.json(), "response body").to_equal({"msg": "Hello A"})
    expect(response.headers["content-type"], "content-type").to_equal(json_type)


@test("router_a override on path uses PlainTextResponse")
def router_a_override():
    with client:
        response = client.get("/a/override")
    expect(response.content, "response content").to_equal(b"Hello A")
    expect(response.headers["content-type"], "content-type").to_equal(text_type)


@test("router_a_a inherits JSON response down to nested routes")
def router_a_a_test():
    with client:
        response = client.get("/a/a")
    expect(response.json(), "response body").to_equal({"msg": "Hello A A"})
    expect(response.headers["content-type"], "content-type").to_equal(json_type)


@test("router_a_a /override path uses PlainTextResponse")
def router_a_a_override():
    with client:
        response = client.get("/a/a/override")
    expect(response.content, "response content").to_equal(b"Hello A A")
    expect(response.headers["content-type"], "content-type").to_equal(text_type)


@test("router_a_b uses include_router default PlainTextResponse")
def router_a_b():
    with client:
        response = client.get("/a/b")
    expect(response.content, "response content").to_equal(b"Hello A B")
    expect(response.headers["content-type"], "content-type").to_equal(text_type)


@test("router_a_b /override path uses HTMLResponse from operation")
def router_a_b_override():
    with client:
        response = client.get("/a/b/override")
    expect(response.content, "response content").to_equal(b"Hello A B")
    expect(response.headers["content-type"], "content-type").to_equal(html_type)


@test("router_b uses include_router default PlainTextResponse")
def router_b():
    with client:
        response = client.get("/b")
    expect(response.content, "response content").to_equal(b"Hello B")
    expect(response.headers["content-type"], "content-type").to_equal(text_type)


@test("router_b /override path uses HTMLResponse from operation")
def router_b_override():
    with client:
        response = client.get("/b/override")
    expect(response.content, "response content").to_equal(b"Hello B")
    expect(response.headers["content-type"], "content-type").to_equal(html_type)


@test("router_b_a inherits PlainTextResponse from parent include_router")
def router_b_a():
    with client:
        response = client.get("/b/a")
    expect(response.content, "response content").to_equal(b"Hello B A")
    expect(response.headers["content-type"], "content-type").to_equal(text_type)


@test("router_b_a /override path uses HTMLResponse from operation")
def router_b_a_override():
    with client:
        response = client.get("/b/a/override")
    expect(response.content, "response content").to_equal(b"Hello B A")
    expect(response.headers["content-type"], "content-type").to_equal(html_type)


@test("router_b_a_c uses HTMLResponse from include_router default")
def router_b_a_c():
    with client:
        response = client.get("/b/a/c")
    expect(response.content, "response content").to_equal(b"Hello B A C")
    expect(response.headers["content-type"], "content-type").to_equal(html_type)


@test("router_b_a_c /override uses OverrideResponse from operation")
def router_b_a_c_override():
    with client:
        response = client.get("/b/a/c/override")
    expect(response.json(), "response body").to_equal({"msg": "Hello B A C"})
    expect(response.headers["content-type"], "content-type").to_equal(override_type)
