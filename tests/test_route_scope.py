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


@test("APIRoute is exposed via request.scope['route']")
def get():
    response = client.get("/users/rick")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"user_id": "rick", "path": "/users/{user_id}"}
    )


@test("invalid HTTP method returns 405")
def invalid_method_doesnt_match():
    response = client.post("/users/rick")
    expect(response.status_code, "status code").to_equal(405).fatal()


@test("invalid path returns 404")
def invalid_path_doesnt_match():
    response = client.post("/usersx/rick")
    expect(response.status_code, "status code").to_equal(404).fatal()


@test("APIWebSocketRoute is exposed via websocket.scope['route']")
def websocket():
    with client.websocket_connect("/items/portal-gun") as websocket:
        data = websocket.receive_json()
        expect(data, "websocket message").to_equal(
            {"item_id": "portal-gun", "path": "/items/{item_id}"}
        )


@test("invalid websocket path raises WebSocketDisconnect")
def websocket_invalid_path_doesnt_match():
    def _body() -> None:
        with client.websocket_connect("/itemsx/portal-gun"):
            pass  # pragma: no cover

    expect(_body, "connect to invalid websocket path").to_raise(WebSocketDisconnect)
