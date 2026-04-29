import os
from pathlib import Path

from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.background_tasks.tutorial001_py310 import app

client = TestClient(app)


@test("Background task writes notification to log")
def background_tasks_tutorial001():
    log = Path("log.txt")
    if log.is_file():
        os.remove(log)  # pragma: no cover
    response = client.post("/send-notification/foo@example.com")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"message": "Notification sent in the background"}
    )
    with open("./log.txt") as f:
        expect(f.read(), "log file contents").to_contain(
            "notification for foo@example.com: some notification"
        )
