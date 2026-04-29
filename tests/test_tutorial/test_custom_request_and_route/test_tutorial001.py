import gzip
import json

from fastapi import Request
from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("custom_request_and_route", name)

    @mod.app.get("/check-class")
    async def check_gzip_request(request: Request):
        return {"request_class": type(request).__name__}

    return TestClient(mod.app)


@test.cases(
    test.case("py310 compress", name="tutorial001_py310", compress=True),
    test.case("py310 plain", name="tutorial001_py310", compress=False),
    test.case("an_py310 compress", name="tutorial001_an_py310", compress=True),
    test.case("an_py310 plain", name="tutorial001_an_py310", compress=False),
)
def gzip_request(name: str, compress: bool):
    client = _client_for(name)
    n = 1000
    headers: dict[str, str] = {}
    body = [1] * n
    data = json.dumps(body).encode()
    if compress:
        data = gzip.compress(data)
        headers["Content-Encoding"] = "gzip"
    headers["Content-Type"] = "application/json"
    response = client.post("/sum", content=data, headers=headers)
    expect(response.json(), "response body").to_equal({"sum": n})


@test.cases(
    test.case("tutorial001_py310", name="tutorial001_py310"),
    test.case("tutorial001_an_py310", name="tutorial001_an_py310"),
)
def request_class(name: str):
    client = _client_for(name)
    response = client.get("/check-class")
    expect(response.json(), "response body").to_equal({"request_class": "GzipRequest"})
