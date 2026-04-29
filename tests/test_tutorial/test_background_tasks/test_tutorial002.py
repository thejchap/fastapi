import os
from pathlib import Path

from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import import_tutorial


def _client_for(name: str) -> TestClient:
    mod = import_tutorial("background_tasks", name)
    return TestClient(mod.app)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def background_tasks_tutorial002(name: str):
    client = _client_for(name)
    log = Path("log.txt")
    if log.is_file():
        os.remove(log)  # pragma: no cover
    response = client.post("/send-notification/foo@example.com?q=some-query")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "Message sent"})
    with open("./log.txt") as f:
        expect(f.read(), "log file contents").to_contain(
            "found query: some-query\nmessage to foo@example.com"
        )
