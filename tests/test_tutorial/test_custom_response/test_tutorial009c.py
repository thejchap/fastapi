from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import needs_orjson

_SKIP_ORJSON = needs_orjson()


if not _SKIP_ORJSON:
    from docs_src.custom_response.tutorial009c_py310 import app

    client = TestClient(app)

    @test("GET / returns pretty-printed ORJSONResponse body")
    def get():
        response = client.get("/")
        expect(response.content, "response content").to_equal(b'{\n  "message": "Hello World"\n}')
