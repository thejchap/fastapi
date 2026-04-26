import functools

from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    Header,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.middleware import Middleware
from fastapi.testclient import TestClient
from tryke import expect, test

router = APIRouter()
prefix_router = APIRouter()
native_prefix_route = APIRouter(prefix="/native")
app = FastAPI()


@app.websocket_route("/")
async def index(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, world!")
    await websocket.close()


@router.websocket_route("/router")
async def routerindex(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router!")
    await websocket.close()


@prefix_router.websocket_route("/")
async def routerprefixindex(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router with prefix!")
    await websocket.close()


@router.websocket("/router2")
async def routerindex2(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router!")
    await websocket.close()


@router.websocket("/router/{pathparam:path}")
async def routerindexparams(websocket: WebSocket, pathparam: str, queryparam: str):
    await websocket.accept()
    await websocket.send_text(pathparam)
    await websocket.send_text(queryparam)
    await websocket.close()


async def ws_dependency():
    return "Socket Dependency"


@router.websocket("/router-ws-depends/")
async def router_ws_decorator_depends(
    websocket: WebSocket, data=Depends(ws_dependency)
):
    await websocket.accept()
    await websocket.send_text(data)
    await websocket.close()


@native_prefix_route.websocket("/")
async def router_native_prefix_ws(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello, router with native prefix!")
    await websocket.close()


async def ws_dependency_err():
    raise NotImplementedError()


@router.websocket("/depends-err/")
async def router_ws_depends_err(websocket: WebSocket, data=Depends(ws_dependency_err)):
    pass  # pragma: no cover


async def ws_dependency_validate(x_missing: str = Header()):
    pass  # pragma: no cover


@router.websocket("/depends-validate/")
async def router_ws_depends_validate(
    websocket: WebSocket, data=Depends(ws_dependency_validate)
):
    pass  # pragma: no cover


class CustomError(Exception):
    pass


@router.websocket("/custom_error/")
async def router_ws_custom_error(websocket: WebSocket):
    raise CustomError()


def make_app(app=None, **kwargs):
    app = app or FastAPI(**kwargs)
    app.include_router(router)
    app.include_router(prefix_router, prefix="/prefix")
    app.include_router(native_prefix_route)
    return app


app = make_app(app)


@test
def app_root():
    client = TestClient(app)
    with client.websocket_connect("/") as websocket:
        data = websocket.receive_text()
        expect(data).to_equal("Hello, world!")


@test
def ws_router():
    client = TestClient(app)
    with client.websocket_connect("/router") as websocket:
        data = websocket.receive_text()
        expect(data).to_equal("Hello, router!")


@test
def ws_prefix_router():
    client = TestClient(app)
    with client.websocket_connect("/prefix/") as websocket:
        data = websocket.receive_text()
        expect(data).to_equal("Hello, router with prefix!")


@test
def ws_native_prefix_router():
    client = TestClient(app)
    with client.websocket_connect("/native/") as websocket:
        data = websocket.receive_text()
        expect(data).to_equal("Hello, router with native prefix!")


@test
def ws_router2():
    client = TestClient(app)
    with client.websocket_connect("/router2") as websocket:
        data = websocket.receive_text()
        expect(data).to_equal("Hello, router!")


@test
def router_ws_depends():
    client = TestClient(app)
    with client.websocket_connect("/router-ws-depends/") as websocket:
        expect(websocket.receive_text()).to_equal("Socket Dependency")


@test
def router_ws_depends_with_override():
    client = TestClient(app)
    app.dependency_overrides[ws_dependency] = lambda: "Override"  # noqa: E731
    with client.websocket_connect("/router-ws-depends/") as websocket:
        expect(websocket.receive_text()).to_equal("Override")


@test
def router_with_params():
    client = TestClient(app)
    with client.websocket_connect(
        "/router/path/to/file?queryparam=a_query_param"
    ) as websocket:
        data = websocket.receive_text()
        expect(data).to_equal("path/to/file")
        data = websocket.receive_text()
        expect(data).to_equal("a_query_param")


# Verify that a websocket connection to a non-existent endpoing returns in a
# shutdown.
@test
def wrong_uri():
    client = TestClient(app)
    raised: WebSocketDisconnect | None = None
    try:
        with client.websocket_connect("/no-router/"):
            pass  # pragma: no cover
    except WebSocketDisconnect as exc:
        raised = exc
    expect(raised).not_.to_be_none().fatal()
    expect(raised.code).to_equal(status.WS_1000_NORMAL_CLOSURE)


def websocket_middleware(middleware_func):
    """
    Helper to create a Starlette pure websocket middleware
    """

    def middleware_constructor(app):
        @functools.wraps(app)
        async def wrapped_app(scope, receive, send):
            if scope["type"] != "websocket":
                return await app(scope, receive, send)  # pragma: no cover

            async def call_next():
                return await app(scope, receive, send)

            websocket = WebSocket(scope, receive=receive, send=send)
            return await middleware_func(websocket, call_next)

        return wrapped_app

    return middleware_constructor


# Verify that a validation in a dependency invokes the correct exception
# handler.
@test
def depend_validation():
    caught = []

    @websocket_middleware
    async def catcher(websocket, call_next):
        try:
            return await call_next()
        except Exception as e:  # pragma: no cover
            caught.append(e)
            raise

    myapp = make_app(middleware=[Middleware(catcher)])

    client = TestClient(myapp)
    raised: WebSocketDisconnect | None = None
    try:
        with client.websocket_connect("/depends-validate/"):
            pass  # pragma: no cover
    except WebSocketDisconnect as exc:
        raised = exc
    expect(raised).not_.to_be_none().fatal()
    # the validation error does produce a close message
    expect(raised.code).to_equal(status.WS_1008_POLICY_VIOLATION)
    # and no error is leaked
    expect(caught).to_equal([])


# Verify that it is possible to write custom WebSocket middleware to catch
# errors.
@test
def depend_err_middleware():
    @websocket_middleware
    async def errorhandler(websocket: WebSocket, call_next):
        try:
            return await call_next()
        except Exception as e:
            await websocket.close(code=status.WS_1006_ABNORMAL_CLOSURE, reason=repr(e))

    myapp = make_app(middleware=[Middleware(errorhandler)])
    client = TestClient(myapp)
    raised: WebSocketDisconnect | None = None
    try:
        with client.websocket_connect("/depends-err/"):
            pass  # pragma: no cover
    except WebSocketDisconnect as exc:
        raised = exc
    expect(raised).not_.to_be_none().fatal()
    expect(raised.code).to_equal(status.WS_1006_ABNORMAL_CLOSURE)
    expect(raised.reason).to_contain("NotImplementedError")


# Verify that it is possible to write a custom WebSocket exception handler.
@test
def depend_err_handler():
    async def custom_handler(websocket: WebSocket, exc: CustomError) -> None:
        await websocket.close(1002, "foo")

    myapp = make_app(exception_handlers={CustomError: custom_handler})
    client = TestClient(myapp)
    raised: WebSocketDisconnect | None = None
    try:
        with client.websocket_connect("/custom_error/"):
            pass  # pragma: no cover
    except WebSocketDisconnect as exc:
        raised = exc
    expect(raised).not_.to_be_none().fatal()
    expect(raised.code).to_equal(1002)
    expect(raised.reason).to_contain("foo")
