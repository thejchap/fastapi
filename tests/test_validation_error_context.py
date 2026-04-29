from fastapi import FastAPI, Request, WebSocket
from fastapi.exceptions import (
    RequestValidationError,
    ResponseValidationError,
    WebSocketRequestValidationError,
)
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import expect, test


class Item(BaseModel):
    id: int
    name: str


class ExceptionCapture:
    def __init__(self):
        self.exception = None

    def capture(self, exc):
        self.exception = exc
        return exc


app = FastAPI()
sub_app = FastAPI()
captured_exception = ExceptionCapture()

app.mount(path="/sub", app=sub_app)


@app.exception_handler(RequestValidationError)
@sub_app.exception_handler(RequestValidationError)
async def request_validation_handler(request: Request, exc: RequestValidationError):
    captured_exception.capture(exc)
    raise exc


@app.exception_handler(ResponseValidationError)
@sub_app.exception_handler(ResponseValidationError)
async def response_validation_handler(_: Request, exc: ResponseValidationError):
    captured_exception.capture(exc)
    raise exc


@app.exception_handler(WebSocketRequestValidationError)
@sub_app.exception_handler(WebSocketRequestValidationError)
async def websocket_validation_handler(
    websocket: WebSocket, exc: WebSocketRequestValidationError
):
    captured_exception.capture(exc)
    raise exc


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}  # pragma: no cover


@app.get("/items/", response_model=Item)
def get_item():
    return {"name": "Widget"}


@sub_app.get("/items/", response_model=Item)
def get_sub_item():
    return {"name": "Widget"}  # pragma: no cover


@app.websocket("/ws/{item_id}")
async def websocket_endpoint(websocket: WebSocket, item_id: int):
    await websocket.accept()  # pragma: no cover
    await websocket.send_text(f"Item: {item_id}")  # pragma: no cover
    await websocket.close()  # pragma: no cover


@sub_app.websocket("/ws/{item_id}")
async def subapp_websocket_endpoint(websocket: WebSocket, item_id: int):
    await websocket.accept()  # pragma: no cover
    await websocket.send_text(f"Item: {item_id}")  # pragma: no cover
    await websocket.close()  # pragma: no cover


client = TestClient(app)


@test("RequestValidationError contains endpoint name and path")
def request_validation_error_includes_endpoint_context():
    captured_exception.exception = None
    try:
        client.get("/users/invalid")
    except Exception:
        pass

    expect(captured_exception.exception, "captured exception").not_.to_be_none().fatal()
    error_str = str(captured_exception.exception)
    expect(error_str, "error string").to_contain("get_user")
    expect(error_str, "error string").to_contain("/users/")


@test("ResponseValidationError contains endpoint name and path")
def response_validation_error_includes_endpoint_context():
    captured_exception.exception = None
    try:
        client.get("/items/")
    except Exception:
        pass

    expect(captured_exception.exception, "captured exception").not_.to_be_none().fatal()
    error_str = str(captured_exception.exception)
    expect(error_str, "error string").to_contain("get_item")
    expect(error_str, "error string").to_contain("/items/")


@test("WebSocketRequestValidationError contains endpoint name and path")
def websocket_validation_error_includes_endpoint_context():
    captured_exception.exception = None
    try:
        with client.websocket_connect("/ws/invalid"):
            pass  # pragma: no cover
    except Exception:
        pass

    expect(captured_exception.exception, "captured exception").not_.to_be_none().fatal()
    error_str = str(captured_exception.exception)
    expect(error_str, "error string").to_contain("websocket_endpoint")
    expect(error_str, "error string").to_contain("/ws/")


@test("Sub-app RequestValidationError contains endpoint name and path")
def subapp_request_validation_error_includes_endpoint_context():
    captured_exception.exception = None
    try:
        client.get("/sub/items/")
    except Exception:
        pass

    expect(captured_exception.exception, "captured exception").not_.to_be_none().fatal()
    error_str = str(captured_exception.exception)
    expect(error_str, "error string").to_contain("get_sub_item")
    expect(error_str, "error string").to_contain("/sub/items/")


@test("Sub-app WebSocketRequestValidationError contains endpoint name and path")
def subapp_websocket_validation_error_includes_endpoint_context():
    captured_exception.exception = None
    try:
        with client.websocket_connect("/sub/ws/invalid"):
            pass  # pragma: no cover
    except Exception:
        pass

    expect(captured_exception.exception, "captured exception").not_.to_be_none().fatal()
    error_str = str(captured_exception.exception)
    expect(error_str, "error string").to_contain("subapp_websocket_endpoint")
    expect(error_str, "error string").to_contain("/sub/ws/")


@test("RequestValidationError with only path emits 'Endpoint:' line")
def validation_error_with_only_path():
    errors = [{"type": "missing", "loc": ("body", "name"), "msg": "Field required"}]
    exc = RequestValidationError(errors, endpoint_ctx={"path": "GET /api/test"})
    error_str = str(exc)
    expect(error_str, "error string").to_contain("Endpoint: GET /api/test")
    expect('File "' in error_str, "no File line in error").to_be_falsy()


@test("RequestValidationError with empty context omits endpoint header")
def validation_error_with_no_context():
    errors = [{"type": "missing", "loc": ("body", "name"), "msg": "Field required"}]
    exc = RequestValidationError(errors, endpoint_ctx={})
    error_str = str(exc)
    expect(error_str, "error string").to_contain("1 validation error:")
    expect("Endpoint" in error_str, "no Endpoint line in error").to_be_falsy()
    expect('File "' in error_str, "no File line in error").to_be_falsy()
