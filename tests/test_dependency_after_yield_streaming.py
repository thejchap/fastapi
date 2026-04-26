from collections.abc import Generator
from contextlib import contextmanager
from typing import Annotated, Any

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse
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


@app.get("/data")
def get_data(session: SessionDep) -> Any:
    data = list(session)
    return data


@app.get("/stream-simple")
def get_stream_simple(session: SessionDep) -> Any:
    def iter_data():
        yield from ["x", "y", "z"]

    return StreamingResponse(iter_data())


@app.get("/stream-session")
def get_stream_session(session: SessionDep) -> Any:
    def iter_data():
        yield from session

    return StreamingResponse(iter_data())


@app.get("/broken-session-data")
def get_broken_session_data(session: BrokenSessionDep) -> Any:
    return list(session)


@app.get("/broken-session-stream")
def get_broken_session_stream(session: BrokenSessionDep) -> Any:
    def iter_data():
        yield from session

    return StreamingResponse(iter_data())


client = TestClient(app)


@test
def regular_no_stream():
    response = client.get("/data")
    expect(response.json()).to_equal(["foo", "bar", "baz"])


@test
def stream_simple():
    response = client.get("/stream-simple")
    expect(response.text).to_equal("xyz")


@test
def stream_session():
    response = client.get("/stream-session")
    expect(response.text).to_equal("foobarbaz")


@test
def broken_session_data():
    expect(lambda: client.get("/broken-session-data")).to_raise(
        ValueError, match="Session closed"
    )


@test
def broken_session_data_no_raise():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/broken-session-data")
    expect(response.status_code).to_equal(500)
    expect(response.text).to_equal("Internal Server Error")


@test
def broken_session_stream_raise():
    # Can raise ValueError on Pydantic v2 and ExceptionGroup on Pydantic v1
    # Tryke `to_raise` doesn't accept a tuple of types; both options inherit
    # from Exception, so just check for that.
    expect(lambda: client.get("/broken-session-stream")).to_raise(Exception)


@test
def broken_session_stream_no_raise():
    """
    When a dependency with yield raises after the streaming response already started
    the 200 status code is already sent, but there's still an error in the server
    afterwards, an exception is raised and captured or shown in the server logs.
    """
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/broken-session-stream")
        expect(response.status_code).to_equal(200)
        expect(response.text).to_equal("")
