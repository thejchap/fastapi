from collections.abc import Generator
from contextlib import contextmanager
from typing import Annotated, Any

from fastapi import Depends, FastAPI, WebSocket
from fastapi.testclient import TestClient
from tryke import expect, test


class Session:
    def __init__(self) -> None:
        self.data = ["foo", "bar", "baz"]
        self.open = True

    def __iter__(self) -> Generator[str]:
        for item in self.data:
            if self.open:
                yield item
            else:
                raise ValueError("Session closed")


@contextmanager
def acquire_session() -> Generator[Session]:
    session = Session()
    try:
        yield session
    finally:
        session.open = False


def dep_session() -> Any:
    with acquire_session() as s:
        yield s


def broken_dep_session() -> Any:
    with acquire_session() as s:
        s.open = False
        yield s


SessionDep = Annotated[Session, Depends(dep_session)]
BrokenSessionDep = Annotated[Session, Depends(broken_dep_session)]

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: SessionDep):
    await websocket.accept()
    for item in session:
        await websocket.send_text(f"{item}")


@app.websocket("/ws-broken")
async def websocket_endpoint_broken(websocket: WebSocket, session: BrokenSessionDep):
    await websocket.accept()
    for item in session:
        await websocket.send_text(f"{item}")  # pragma no cover


client = TestClient(app)


@test("websocket endpoint streams session items yielded by dependency")
def websocket_dependency_after_yield():
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        expect(data, "first message").to_equal("foo")
        data = websocket.receive_text()
        expect(data, "second message").to_equal("bar")
        data = websocket.receive_text()
        expect(data, "third message").to_equal("baz")


@test("broken session raises when websocket connects")
def websocket_dependency_after_yield_broken():
    def _body():
        with client.websocket_connect("/ws-broken"):
            pass  # pragma no cover

    expect(_body, "connecting to /ws-broken").to_raise(
        ValueError, match="Session closed"
    )
