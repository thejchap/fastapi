from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import Depends as TrykeDepends
from tryke import expect, fixture, test

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import AsyncGenerator


class DummyClient:
    async def get_people(self) -> list:
        return ["John Doe", "Jane Doe"]

    async def close(self) -> None:
        pass


async def get_client() -> AsyncGenerator[DummyClient]:
    client = DummyClient()
    yield client
    await client.close()


Client = Annotated[DummyClient, Depends(get_client)]


@fixture
def client() -> TestClient:
    app = FastAPI()

    @app.get("/")
    async def get_people(client: Client) -> list:
        return await client.get_people()

    return TestClient(app)


@test
def get(client: TestClient = TrykeDepends(client)):
    response = client.get("/")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(["John Doe", "Jane Doe"])


@test
def openapi_schema(client: TestClient = TrykeDepends(client)):
    response = client.get("/openapi.json")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "openapi": "3.1.0",
                "info": {"title": "FastAPI", "version": "0.1.0"},
                "paths": {
                    "/": {
                        "get": {
                            "summary": "Get People",
                            "operationId": "get_people__get",
                            "responses": {
                                "200": {
                                    "description": "Successful Response",
                                    "content": {
                                        "application/json": {
                                            "schema": {
                                                "items": {},
                                                "type": "array",
                                                "title": "Response Get People  Get",
                                            }
                                        }
                                    },
                                }
                            },
                        }
                    }
                },
            }
        )
    )
