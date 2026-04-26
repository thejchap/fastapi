import json

from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()
state = {
    "/async": "asyncgen not started",
    "/sync": "generator not started",
    "/async_raise": "asyncgen raise not started",
    "/sync_raise": "generator raise not started",
    "context_a": "not started a",
    "context_b": "not started b",
    "bg": "not set",
    "sync_bg": "not set",
}

errors = []


async def get_state():
    return state


class AsyncDependencyError(Exception):
    pass


class SyncDependencyError(Exception):
    pass


class OtherDependencyError(Exception):
    pass


async def asyncgen_state(state: dict[str, str] = Depends(get_state)):
    state["/async"] = "asyncgen started"
    yield state["/async"]
    state["/async"] = "asyncgen completed"


def generator_state(state: dict[str, str] = Depends(get_state)):
    state["/sync"] = "generator started"
    yield state["/sync"]
    state["/sync"] = "generator completed"


async def asyncgen_state_try(state: dict[str, str] = Depends(get_state)):
    state["/async_raise"] = "asyncgen raise started"
    try:
        yield state["/async_raise"]
    except AsyncDependencyError:
        errors.append("/async_raise")
        raise
    finally:
        state["/async_raise"] = "asyncgen raise finalized"


def generator_state_try(state: dict[str, str] = Depends(get_state)):
    state["/sync_raise"] = "generator raise started"
    try:
        yield state["/sync_raise"]
    except SyncDependencyError:
        errors.append("/sync_raise")
        raise
    finally:
        state["/sync_raise"] = "generator raise finalized"


async def context_a(state: dict = Depends(get_state)):
    state["context_a"] = "started a"
    try:
        yield state
    finally:
        state["context_a"] = "finished a"


async def context_b(state: dict = Depends(context_a)):
    state["context_b"] = "started b"
    try:
        yield state
    finally:
        state["context_b"] = f"finished b with a: {state['context_a']}"


@app.get("/async")
async def get_async(state: str = Depends(asyncgen_state)):
    return state


@app.get("/sync")
async def get_sync(state: str = Depends(generator_state)):
    return state


@app.get("/async_raise")
async def get_async_raise(state: str = Depends(asyncgen_state_try)):
    assert state == "asyncgen raise started"
    raise AsyncDependencyError()


@app.get("/sync_raise")
async def get_sync_raise(state: str = Depends(generator_state_try)):
    assert state == "generator raise started"
    raise SyncDependencyError()


@app.get("/async_raise_other")
async def get_async_raise_other(state: str = Depends(asyncgen_state_try)):
    assert state == "asyncgen raise started"
    raise OtherDependencyError()


@app.get("/sync_raise_other")
async def get_sync_raise_other(state: str = Depends(generator_state_try)):
    assert state == "generator raise started"
    raise OtherDependencyError()


@app.get("/context_b")
async def get_context_b(state: dict = Depends(context_b)):
    return state


@app.get("/context_b_raise")
async def get_context_b_raise(state: dict = Depends(context_b)):
    assert state["context_b"] == "started b"
    assert state["context_a"] == "started a"
    raise OtherDependencyError()


@app.get("/context_b_bg")
async def get_context_b_bg(tasks: BackgroundTasks, state: dict = Depends(context_b)):
    async def bg(state: dict):
        state["bg"] = f"bg set - b: {state['context_b']} - a: {state['context_a']}"

    tasks.add_task(bg, state)
    return state


# Sync versions


@app.get("/sync_async")
def get_sync_async(state: str = Depends(asyncgen_state)):
    return state


@app.get("/sync_sync")
def get_sync_sync(state: str = Depends(generator_state)):
    return state


@app.get("/sync_async_raise")
def get_sync_async_raise(state: str = Depends(asyncgen_state_try)):
    assert state == "asyncgen raise started"
    raise AsyncDependencyError()


@app.get("/sync_sync_raise")
def get_sync_sync_raise(state: str = Depends(generator_state_try)):
    assert state == "generator raise started"
    raise SyncDependencyError()


@app.get("/sync_async_raise_other")
def get_sync_async_raise_other(state: str = Depends(asyncgen_state_try)):
    assert state == "asyncgen raise started"
    raise OtherDependencyError()


@app.get("/sync_sync_raise_other")
def get_sync_sync_raise_other(state: str = Depends(generator_state_try)):
    assert state == "generator raise started"
    raise OtherDependencyError()


@app.get("/sync_context_b")
def get_sync_context_b(state: dict = Depends(context_b)):
    return state


@app.get("/sync_context_b_raise")
def get_sync_context_b_raise(state: dict = Depends(context_b)):
    assert state["context_b"] == "started b"
    assert state["context_a"] == "started a"
    raise OtherDependencyError()


@app.get("/sync_context_b_bg")
async def get_sync_context_b_bg(
    tasks: BackgroundTasks, state: dict = Depends(context_b)
):
    async def bg(state: dict):
        state["sync_bg"] = (
            f"sync_bg set - b: {state['context_b']} - a: {state['context_a']}"
        )

    tasks.add_task(bg, state)
    return state


@app.middleware("http")
async def middleware(request, call_next):
    response: StreamingResponse = await call_next(request)
    response.headers["x-state"] = json.dumps(state.copy())
    return response


client = TestClient(app)


@test
def async_state():
    expect(state["/async"]).to_equal("asyncgen not started")
    response = client.get("/async")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("asyncgen started")
    expect(state["/async"]).to_equal("asyncgen completed")


@test
def sync_state():
    expect(state["/sync"]).to_equal("generator not started")
    response = client.get("/sync")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("generator started")
    expect(state["/sync"]).to_equal("generator completed")


@test
def async_raise_other():
    expect(state["/async_raise"]).to_equal("asyncgen raise not started")
    expect(lambda: client.get("/async_raise_other")).to_raise(OtherDependencyError)
    expect(state["/async_raise"]).to_equal("asyncgen raise finalized")
    expect(errors).not_.to_contain("/async_raise")


@test
def sync_raise_other():
    expect(state["/sync_raise"]).to_equal("generator raise not started")
    expect(lambda: client.get("/sync_raise_other")).to_raise(OtherDependencyError)
    expect(state["/sync_raise"]).to_equal("generator raise finalized")
    expect(errors).not_.to_contain("/sync_raise")


@test
def async_raise_raises():
    expect(lambda: client.get("/async_raise")).to_raise(AsyncDependencyError)
    expect(state["/async_raise"]).to_equal("asyncgen raise finalized")
    expect(errors).to_contain("/async_raise")
    errors.clear()


@test
def async_raise_server_error():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/async_raise")
    expect(response.status_code).to_equal(500).fatal()
    expect(state["/async_raise"]).to_equal("asyncgen raise finalized")
    expect(errors).to_contain("/async_raise")
    errors.clear()


@test
def context_b_test():
    response = client.get("/context_b")
    data = response.json()
    expect(data["context_b"]).to_equal("started b")
    expect(data["context_a"]).to_equal("started a")
    expect(state["context_b"]).to_equal("finished b with a: started a")
    expect(state["context_a"]).to_equal("finished a")


@test
def context_b_raise():
    expect(lambda: client.get("/context_b_raise")).to_raise(OtherDependencyError)
    expect(state["context_b"]).to_equal("finished b with a: started a")
    expect(state["context_a"]).to_equal("finished a")


@test
def background_tasks():
    response = client.get("/context_b_bg")
    data = response.json()
    expect(data["context_b"]).to_equal("started b")
    expect(data["context_a"]).to_equal("started a")
    expect(data["bg"]).to_equal("not set")
    middleware_state = json.loads(response.headers["x-state"])
    expect(middleware_state["context_b"]).to_equal("started b")
    expect(middleware_state["context_a"]).to_equal("started a")
    expect(middleware_state["bg"]).to_equal("not set")
    expect(state["context_b"]).to_equal("finished b with a: started a")
    expect(state["context_a"]).to_equal("finished a")
    expect(state["bg"]).to_equal("bg set - b: started b - a: started a")


@test
def sync_raise_raises():
    expect(lambda: client.get("/sync_raise")).to_raise(SyncDependencyError)
    expect(state["/sync_raise"]).to_equal("generator raise finalized")
    expect(errors).to_contain("/sync_raise")
    errors.clear()


@test
def sync_raise_server_error():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/sync_raise")
    expect(response.status_code).to_equal(500).fatal()
    expect(state["/sync_raise"]).to_equal("generator raise finalized")
    expect(errors).to_contain("/sync_raise")
    errors.clear()


@test
def sync_async_state():
    response = client.get("/sync_async")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("asyncgen started")
    expect(state["/async"]).to_equal("asyncgen completed")


@test
def sync_sync_state():
    response = client.get("/sync_sync")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("generator started")
    expect(state["/sync"]).to_equal("generator completed")


@test
def sync_async_raise_other():
    expect(lambda: client.get("/sync_async_raise_other")).to_raise(OtherDependencyError)
    expect(state["/async_raise"]).to_equal("asyncgen raise finalized")
    expect(errors).not_.to_contain("/async_raise")


@test
def sync_sync_raise_other():
    expect(lambda: client.get("/sync_sync_raise_other")).to_raise(OtherDependencyError)
    expect(state["/sync_raise"]).to_equal("generator raise finalized")
    expect(errors).not_.to_contain("/sync_raise")


@test
def sync_async_raise_raises():
    expect(lambda: client.get("/sync_async_raise")).to_raise(AsyncDependencyError)
    expect(state["/async_raise"]).to_equal("asyncgen raise finalized")
    expect(errors).to_contain("/async_raise")
    errors.clear()


@test
def sync_async_raise_server_error():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/sync_async_raise")
    expect(response.status_code).to_equal(500).fatal()
    expect(state["/async_raise"]).to_equal("asyncgen raise finalized")
    expect(errors).to_contain("/async_raise")
    errors.clear()


@test
def sync_sync_raise_raises():
    expect(lambda: client.get("/sync_sync_raise")).to_raise(SyncDependencyError)
    expect(state["/sync_raise"]).to_equal("generator raise finalized")
    expect(errors).to_contain("/sync_raise")
    errors.clear()


@test
def sync_sync_raise_server_error():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/sync_sync_raise")
    expect(response.status_code).to_equal(500).fatal()
    expect(state["/sync_raise"]).to_equal("generator raise finalized")
    expect(errors).to_contain("/sync_raise")
    errors.clear()


@test
def sync_context_b():
    response = client.get("/sync_context_b")
    data = response.json()
    expect(data["context_b"]).to_equal("started b")
    expect(data["context_a"]).to_equal("started a")
    expect(state["context_b"]).to_equal("finished b with a: started a")
    expect(state["context_a"]).to_equal("finished a")


@test
def sync_context_b_raise():
    expect(lambda: client.get("/sync_context_b_raise")).to_raise(OtherDependencyError)
    expect(state["context_b"]).to_equal("finished b with a: started a")
    expect(state["context_a"]).to_equal("finished a")


@test
def sync_background_tasks():
    response = client.get("/sync_context_b_bg")
    data = response.json()
    expect(data["context_b"]).to_equal("started b")
    expect(data["context_a"]).to_equal("started a")
    expect(data["sync_bg"]).to_equal("not set")
    expect(state["context_b"]).to_equal("finished b with a: started a")
    expect(state["context_a"]).to_equal("finished a")
    expect(state["sync_bg"]).to_equal("sync_bg set - b: started b - a: started a")
