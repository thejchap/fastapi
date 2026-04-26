from functools import partial

from fastapi import FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test


def main(some_arg, q: str | None = None):
    return {"some_arg": some_arg, "q": q}


endpoint = partial(main, "foo")

app = FastAPI()

app.get("/")(endpoint)


client = TestClient(app)


@test
def partial_endpoint():
    response = client.get("/?q=bar")
    data = response.json()
    expect(data).to_equal({"some_arg": "foo", "q": "bar"})
