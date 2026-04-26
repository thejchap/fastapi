from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from starlette.responses import JSONResponse
from tryke import expect, test


def http_exception_handler(request, exception):
    return JSONResponse({"exception": "http-exception"})


def request_validation_exception_handler(request, exception):
    return JSONResponse({"exception": "request-validation"})


def server_error_exception_handler(request, exception):
    return JSONResponse(status_code=500, content={"exception": "server-error"})


app = FastAPI(
    exception_handlers={
        HTTPException: http_exception_handler,
        RequestValidationError: request_validation_exception_handler,
        Exception: server_error_exception_handler,
    }
)

client = TestClient(app)


def raise_value_error():
    raise ValueError()


def dependency_with_yield():
    yield raise_value_error()


@app.get("/dependency-with-yield", dependencies=[Depends(dependency_with_yield)])
def with_yield(): ...


@app.get("/http-exception")
def route_with_http_exception():
    raise HTTPException(status_code=400)


@app.get("/request-validation/{param}/")
def route_with_request_validation_exception(param: int):
    pass  # pragma: no cover


@app.get("/server-error")
def route_with_server_error():
    raise RuntimeError("Oops!")


@test
def override_http_exception():
    response = client.get("/http-exception")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"exception": "http-exception"})


@test
def override_request_validation_exception():
    response = client.get("/request-validation/invalid")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"exception": "request-validation"})


@test
def override_server_error_exception_raises():
    expect(lambda: client.get("/server-error")).to_raise(RuntimeError)


@test
def override_server_error_exception_response():
    local_client = TestClient(app, raise_server_exceptions=False)
    response = local_client.get("/server-error")
    expect(response.status_code).to_equal(500).fatal()
    expect(response.json()).to_equal({"exception": "server-error"})


@test
def traceback_for_dependency_with_yield():
    local_client = TestClient(app, raise_server_exceptions=True)
    captured: ValueError | None = None
    tb = None
    try:
        local_client.get("/dependency-with-yield")
    except ValueError as exc:
        captured = exc
        tb = exc.__traceback__
    expect(captured).not_.to_be_none().fatal()
    # Walk to the deepest frame.
    last = tb
    while last is not None and last.tb_next is not None:
        last = last.tb_next
    expect(last).not_.to_be_none().fatal()
    expect(last.tb_frame.f_code.co_filename).to_equal(__file__)
    expect(last.tb_lineno).to_equal(raise_value_error.__code__.co_firstlineno + 1)
