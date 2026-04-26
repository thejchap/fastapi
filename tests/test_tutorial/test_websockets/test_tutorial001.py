from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
from tryke import expect, test

from docs_src.websockets_.tutorial001_py310 import app

client = TestClient(app)


@test
def main():
    response = client.get("/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.content).to_contain(b"<!DOCTYPE html>")


@test
def websocket():
    def _body():
        with client.websocket_connect("/ws") as ws:
            message = "Message one"
            ws.send_text(message)
            data = ws.receive_text()
            expect(data).to_equal(f"Message text was: {message}")
            message = "Message two"
            ws.send_text(message)
            data = ws.receive_text()
            expect(data).to_equal(f"Message text was: {message}")

    expect(_body).to_raise(WebSocketDisconnect)
