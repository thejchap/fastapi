from fastapi import FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test


@test("PEP 585 generic types work as request/response_model")
def typing():
    types = {
        list[int]: [1, 2, 3],
        dict[str, list[int]]: {"a": [1, 2, 3], "b": [4, 5, 6]},
        set[int]: [1, 2, 3],  # `set` is converted to `list`
        tuple[int, ...]: [1, 2, 3],  # `tuple` is converted to `list`
    }
    for test_type, expected in types.items():
        app = FastAPI()

        @app.post("/", response_model=test_type)
        def post_endpoint(input: test_type):
            return input

        res = TestClient(app).post("/", json=expected)
        expect(res.status_code, "status code").to_equal(200).fatal()
        expect(res.json(), "response body").to_equal(expected)
