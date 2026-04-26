from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.routing import APIRoute, APIWebSocketRoute
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()


@app.get("/users/{user_id}")
async def get_user(user_id: str, request: Request):
    route: APIRoute = request.scope["route"]
    return {"user_id": user_id, "path": route.path}


@app.websocket("/items/{item_id}")
async def websocket_item(item_id: str, websocket: WebSocket):
    route: APIWebSocketRoute = websocket.scope["route"]
    await websocket.accept()
    await websocket.send_json({"item_id": item_id, "path": route.path})


client = TestClient(app)


@test
def get():
    response = client.get("/users/rick")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"user_id": "rick", "path": "/users/{user_id}"})


@test
def invalid_method_doesnt_match():
    response = client.post("/users/rick")
    expect(response.status_code).to_equal(405).fatal()


@test
def invalid_path_doesnt_match():
    response = client.post("/usersx/rick")
    expect(response.status_code).to_equal(404).fatal()


@test
def websocket():
    with client.websocket_connect("/items/portal-gun") as websocket:
        data = websocket.receive_json()
        expect(data).to_equal({"item_id": "portal-gun", "path": "/items/{item_id}"})


@test
def websocket_invalid_path_doesnt_match():
    def _body() -> None:
        with client.websocket_connect("/itemsx/portal-gun"):
            pass  # pragma: no cover

    expect(_body).to_raise(WebSocketDisconnect)
