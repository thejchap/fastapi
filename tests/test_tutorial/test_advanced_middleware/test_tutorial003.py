from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.advanced_middleware.tutorial003_py310 import app


@app.get("/large")
async def large():
    return PlainTextResponse("x" * 4000, status_code=200)


client = TestClient(app)


@test("GZip middleware compresses large responses")
def middleware():
    response = client.get("/large", headers={"accept-encoding": "gzip"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.text, "decoded response text").to_equal("x" * 4000)
    expect(response.headers["Content-Encoding"], "content-encoding header").to_equal(
        "gzip"
    )
    expect(
        int(response.headers["Content-Length"]), "content-length"
    ).to_be_less_than(4000)
    response = client.get("/")
    expect(response.status_code, "root status code").to_equal(200).fatal()
