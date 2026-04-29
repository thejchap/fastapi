from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
from tryke import expect, test

from docs_src.websockets_.tutorial001_py310 import app

client = TestClient(app)


@test("websockets tutorial001 serves the demo HTML page")
def main():
    response = client.get("/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.content, "HTML body").to_contain(b"<!DOCTYPE html>")


@test("websocket echoes text messages then disconnects")
def websocket():
    def _body():
        with client.websocket_connect("/ws") as ws:
            message = "Message one"
            ws.send_text(message)
            data = ws.receive_text()
            expect(data, "echo for message one").to_equal(
                f"Message text was: {message}"
            )
            message = "Message two"
            ws.send_text(message)
            data = ws.receive_text()
            expect(data, "echo for message two").to_equal(
                f"Message text was: {message}"
            )

    expect(_body, "running websocket interaction").to_raise(WebSocketDisconnect)
