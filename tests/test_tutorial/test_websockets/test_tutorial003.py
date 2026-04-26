import time

from fastapi.testclient import TestClient
from tryke import expect, test

from ..._shims import import_tutorial


def _module_for(name: str):
    return import_tutorial("websockets_", name)


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
)
def get(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    response = client.get("/")
    expect(response.text).to_equal(mod.html)


@test.cases(
    test.case("tutorial003_py310", name="tutorial003_py310"),
)
def websocket_handle_disconnection(name: str):
    mod = _module_for(name)
    client = TestClient(mod.app)
    with (
        client.websocket_connect("/ws/1234") as connection,
        client.websocket_connect("/ws/5678") as connection_two,
    ):
        connection.send_text("Hello from 1234")
        data1 = connection.receive_text()
        expect(data1).to_equal("You wrote: Hello from 1234")
        time.sleep(0.01)  # Give server time to process broadcast
        data2 = connection_two.receive_text()
        client1_says = "Client #1234 says: Hello from 1234"
        expect(data2).to_equal(client1_says)
        data1 = connection.receive_text()
        expect(data1).to_equal(client1_says)
        connection_two.close()
        time.sleep(0.01)  # Give server time to process broadcast
        data1 = connection.receive_text()
        expect(data1).to_equal("Client #5678 left the chat")
