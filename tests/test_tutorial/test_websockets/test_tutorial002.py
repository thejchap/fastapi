from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
from tryke import expect, test

from ..._shims import import_tutorial


def _app_for(name: str) -> FastAPI:
    mod = import_tutorial("websockets_", name)
    return mod.app


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def main(name: str):
    app = _app_for(name)
    client = TestClient(app)
    response = client.get("/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.content, "HTML body").to_contain(b"<!DOCTYPE html>")


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def websocket_with_cookie(name: str):
    app = _app_for(name)
    client = TestClient(app, cookies={"session": "fakesession"})

    def _body():
        with client.websocket_connect("/items/foo/ws") as ws:
            message = "Message one"
            ws.send_text(message)
            data = ws.receive_text()
            expect(data, "cookie/token line").to_equal(
                "Session cookie or query token value is: fakesession"
            )
            data = ws.receive_text()
            expect(data, "echo for message one").to_equal(
                f"Message text was: {message}, for item ID: foo"
            )
            message = "Message two"
            ws.send_text(message)
            data = ws.receive_text()
            expect(data, "cookie/token line").to_equal(
                "Session cookie or query token value is: fakesession"
            )
            data = ws.receive_text()
            expect(data, "echo for message two").to_equal(
                f"Message text was: {message}, for item ID: foo"
            )

    expect(_body, "running websocket interaction").to_raise(WebSocketDisconnect)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def websocket_with_header(name: str):
    app = _app_for(name)
    client = TestClient(app)

    def _body():
        with client.websocket_connect("/items/bar/ws?token=some-token") as ws:
            message = "Message one"
            ws.send_text(message)
            data = ws.receive_text()
            expect(data, "cookie/token line").to_equal(
                "Session cookie or query token value is: some-token"
            )
            data = ws.receive_text()
            expect(data, "echo for message one").to_equal(
                f"Message text was: {message}, for item ID: bar"
            )
            message = "Message two"
            ws.send_text(message)
            data = ws.receive_text()
            expect(data, "cookie/token line").to_equal(
                "Session cookie or query token value is: some-token"
            )
            data = ws.receive_text()
            expect(data, "echo for message two").to_equal(
                f"Message text was: {message}, for item ID: bar"
            )

    expect(_body, "running websocket interaction").to_raise(WebSocketDisconnect)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def websocket_with_header_and_query(name: str):
    app = _app_for(name)
    client = TestClient(app)

    def _body():
        with client.websocket_connect("/items/2/ws?q=3&token=some-token") as ws:
            message = "Message one"
            ws.send_text(message)
            data = ws.receive_text()
            expect(data, "cookie/token line").to_equal(
                "Session cookie or query token value is: some-token"
            )
            data = ws.receive_text()
            expect(data, "query parameter line").to_equal("Query parameter q is: 3")
            data = ws.receive_text()
            expect(data, "echo for message one").to_equal(
                f"Message text was: {message}, for item ID: 2"
            )
            message = "Message two"
            ws.send_text(message)
            data = ws.receive_text()
            expect(data, "cookie/token line").to_equal(
                "Session cookie or query token value is: some-token"
            )
            data = ws.receive_text()
            expect(data, "query parameter line").to_equal("Query parameter q is: 3")
            data = ws.receive_text()
            expect(data, "echo for message two").to_equal(
                f"Message text was: {message}, for item ID: 2"
            )

    expect(_body, "running websocket interaction").to_raise(WebSocketDisconnect)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def websocket_no_credentials(name: str):
    app = _app_for(name)
    client = TestClient(app)

    def _body():
        with client.websocket_connect("/items/foo/ws"):
            raise AssertionError(
                "did not raise WebSocketDisconnect on __enter__"
            )  # pragma: no cover

    expect(_body, "connecting without credentials").to_raise(WebSocketDisconnect)


@test.cases(
    test.case("tutorial002_py310", name="tutorial002_py310"),
    test.case("tutorial002_an_py310", name="tutorial002_an_py310"),
)
def websocket_invalid_data(name: str):
    app = _app_for(name)
    client = TestClient(app)

    def _body():
        with client.websocket_connect("/items/foo/ws?q=bar&token=some-token"):
            raise AssertionError(
                "did not raise WebSocketDisconnect on __enter__"
            )  # pragma: no cover

    expect(_body, "connecting with invalid q").to_raise(WebSocketDisconnect)
