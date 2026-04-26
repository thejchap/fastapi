from fastapi import Depends, FastAPI
from fastapi.requests import HTTPConnection
from fastapi.testclient import TestClient
from starlette.websockets import WebSocket
from tryke import expect, test

app = FastAPI()
app.state.value = 42


async def extract_value_from_http_connection(conn: HTTPConnection):
    return conn.app.state.value


@app.get("/http")
async def get_value_by_http(value: int = Depends(extract_value_from_http_connection)):
    return value


@app.websocket("/ws")
async def get_value_by_ws(
    websocket: WebSocket, value: int = Depends(extract_value_from_http_connection)
):
    await websocket.accept()
    await websocket.send_json(value)
    await websocket.close()


client = TestClient(app)


@test
def value_extracting_by_http():
    response = client.get("/http")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(42)


@test
def value_extracting_by_ws():
    with client.websocket_connect("/ws") as websocket:
        expect(websocket.receive_json()).to_equal(42)
