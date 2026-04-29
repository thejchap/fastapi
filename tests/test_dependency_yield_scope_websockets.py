from contextvars import ContextVar
from typing import Annotated, Any

from fastapi import Depends, FastAPI, WebSocket
from fastapi.exceptions import FastAPIError
from fastapi.testclient import TestClient
from tryke import expect, test

global_context: ContextVar[dict[str, Any]] = ContextVar("global_context", default={})  # noqa: B039


class Session:
    def __init__(self) -> None:
        self.open = True


async def dep_session() -> Any:
    s = Session()
    yield s
    s.open = False
    global_state = global_context.get()
    global_state["session_closed"] = True


SessionFuncDep = Annotated[Session, Depends(dep_session, scope="function")]
SessionRequestDep = Annotated[Session, Depends(dep_session, scope="request")]
SessionDefaultDep = Annotated[Session, Depends(dep_session)]


class NamedSession:
    def __init__(self, name: str = "default") -> None:
        self.name = name
        self.open = True


def get_named_session(session: SessionRequestDep, session_b: SessionDefaultDep) -> Any:
    assert session is session_b
    named_session = NamedSession(name="named")
    yield named_session, session_b
    named_session.open = False
    global_state = global_context.get()
    global_state["named_session_closed"] = True


NamedSessionsDep = Annotated[tuple[NamedSession, Session], Depends(get_named_session)]


def get_named_func_session(session: SessionFuncDep) -> Any:
    named_session = NamedSession(name="named")
    yield named_session, session
    named_session.open = False
    global_state = global_context.get()
    global_state["named_func_session_closed"] = True


def get_named_regular_func_session(session: SessionFuncDep) -> Any:
    named_session = NamedSession(name="named")
    return named_session, session


BrokenSessionsDep = Annotated[
    tuple[NamedSession, Session], Depends(get_named_func_session)
]
NamedSessionsFuncDep = Annotated[
    tuple[NamedSession, Session], Depends(get_named_func_session, scope="function")
]

RegularSessionsDep = Annotated[
    tuple[NamedSession, Session], Depends(get_named_regular_func_session)
]

app = FastAPI()


@app.websocket("/function-scope")
async def function_scope(websocket: WebSocket, session: SessionFuncDep) -> Any:
    await websocket.accept()
    await websocket.send_json({"is_open": session.open})


@app.websocket("/request-scope")
async def request_scope(websocket: WebSocket, session: SessionRequestDep) -> Any:
    await websocket.accept()
    await websocket.send_json({"is_open": session.open})


@app.websocket("/two-scopes")
async def get_stream_session(
    websocket: WebSocket,
    function_session: SessionFuncDep,
    request_session: SessionRequestDep,
) -> Any:
    await websocket.accept()
    await websocket.send_json(
        {"func_is_open": function_session.open, "req_is_open": request_session.open}
    )


@app.websocket("/sub")
async def get_sub(websocket: WebSocket, sessions: NamedSessionsDep) -> Any:
    await websocket.accept()
    await websocket.send_json(
        {"named_session_open": sessions[0].open, "session_open": sessions[1].open}
    )


@app.websocket("/named-function-scope")
async def get_named_function_scope(
    websocket: WebSocket, sessions: NamedSessionsFuncDep
) -> Any:
    await websocket.accept()
    await websocket.send_json(
        {"named_session_open": sessions[0].open, "session_open": sessions[1].open}
    )


@app.websocket("/regular-function-scope")
async def get_regular_function_scope(
    websocket: WebSocket, sessions: RegularSessionsDep
) -> Any:
    await websocket.accept()
    await websocket.send_json(
        {"named_session_open": sessions[0].open, "session_open": sessions[1].open}
    )


client = TestClient(app)


@test("function-scoped websocket dependency closes session on completion")
def function_scope_test() -> None:
    global_context.set({})
    global_state = global_context.get()
    with client.websocket_connect("/function-scope") as websocket:
        data = websocket.receive_json()
    expect(data["is_open"], "session was open during request").to_be(True)
    expect(global_state["session_closed"], "session_closed flag").to_be(True)


@test("request-scoped websocket dependency closes session on completion")
def request_scope_test() -> None:
    global_context.set({})
    global_state = global_context.get()
    with client.websocket_connect("/request-scope") as websocket:
        data = websocket.receive_json()
    expect(data["is_open"], "session was open during request").to_be(True)
    expect(global_state["session_closed"], "session_closed flag").to_be(True)


@test("two scopes share session lifecycle properly")
def two_scopes() -> None:
    global_context.set({})
    global_state = global_context.get()
    with client.websocket_connect("/two-scopes") as websocket:
        data = websocket.receive_json()
    expect(data["func_is_open"], "function-scoped session open").to_be(True)
    expect(data["req_is_open"], "request-scoped session open").to_be(True)
    expect(global_state["session_closed"], "session_closed flag").to_be(True)


@test("nested dependency closes both session and named session")
def sub() -> None:
    global_context.set({})
    global_state = global_context.get()
    with client.websocket_connect("/sub") as websocket:
        data = websocket.receive_json()
    expect(data["named_session_open"], "named session was open").to_be(True)
    expect(data["session_open"], "underlying session was open").to_be(True)
    expect(global_state["session_closed"], "session_closed flag").to_be(True)
    expect(
        global_state["named_session_closed"],
        "named_session_closed flag",
    ).to_be(True)


@test("request-scoped dep cannot depend on function-scoped dep")
def broken_scope() -> None:
    def _body():
        @app.websocket("/broken-scope")
        async def get_broken(
            websocket: WebSocket, sessions: BrokenSessionsDep
        ) -> Any:  # pragma: no cover
            pass

    expect(_body, "registering broken-scope websocket").to_raise(
        FastAPIError,
        match='The dependency "get_named_func_session" has a scope of "request", it cannot depend on dependencies with scope "function"',
    )


@test("named function-scoped dependency closes both sessions")
def named_function_scope() -> None:
    global_context.set({})
    global_state = global_context.get()
    with client.websocket_connect("/named-function-scope") as websocket:
        data = websocket.receive_json()
    expect(data["named_session_open"], "named session was open").to_be(True)
    expect(data["session_open"], "underlying session was open").to_be(True)
    expect(global_state["session_closed"], "session_closed flag").to_be(True)
    expect(
        global_state["named_func_session_closed"],
        "named_func_session_closed flag",
    ).to_be(True)


@test("regular (non-yield) function-scoped dependency works")
def regular_function_scope() -> None:
    global_context.set({})
    global_state = global_context.get()
    with client.websocket_connect("/regular-function-scope") as websocket:
        data = websocket.receive_json()
    expect(data["named_session_open"], "named session was open").to_be(True)
    expect(data["session_open"], "underlying session was open").to_be(True)
    expect(global_state["session_closed"], "session_closed flag").to_be(True)
