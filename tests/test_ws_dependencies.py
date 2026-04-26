import json
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, WebSocket
from fastapi.testclient import TestClient
from tryke import expect, test


def dependency_list() -> list[str]:
    return []


DepList = Annotated[list[str], Depends(dependency_list)]


def create_dependency(name: str):
    def fun(deps: DepList):
        deps.append(name)

    return Depends(fun)


router = APIRouter(dependencies=[create_dependency("router")])
prefix_router = APIRouter(dependencies=[create_dependency("prefix_router")])
app = FastAPI(dependencies=[create_dependency("app")])


@app.websocket("/", dependencies=[create_dependency("index")])
async def index(websocket: WebSocket, deps: DepList):
    await websocket.accept()
    await websocket.send_text(json.dumps(deps))
    await websocket.close()


@router.websocket("/router", dependencies=[create_dependency("routerindex")])
async def routerindex(websocket: WebSocket, deps: DepList):
    await websocket.accept()
    await websocket.send_text(json.dumps(deps))
    await websocket.close()


@prefix_router.websocket("/", dependencies=[create_dependency("routerprefixindex")])
async def routerprefixindex(websocket: WebSocket, deps: DepList):
    await websocket.accept()
    await websocket.send_text(json.dumps(deps))
    await websocket.close()


app.include_router(router, dependencies=[create_dependency("router2")])
app.include_router(
    prefix_router, prefix="/prefix", dependencies=[create_dependency("prefix_router2")]
)


@test
def index_ws():
    client = TestClient(app)
    with client.websocket_connect("/") as websocket:
        data = json.loads(websocket.receive_text())
        expect(data).to_equal(["app", "index"])


@test
def routerindex_ws():
    client = TestClient(app)
    with client.websocket_connect("/router") as websocket:
        data = json.loads(websocket.receive_text())
        expect(data).to_equal(["app", "router2", "router", "routerindex"])


@test
def routerprefixindex_ws():
    client = TestClient(app)
    with client.websocket_connect("/prefix/") as websocket:
        data = json.loads(websocket.receive_text())
        expect(data).to_equal(
            ["app", "prefix_router2", "prefix_router", "routerprefixindex"]
        )
