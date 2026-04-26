from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from dirty_equals import IsUUID
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test


@dataclass
class Item:
    id: uuid.UUID
    name: str
    price: float
    tags: list[str] = field(default_factory=list)
    description: str | None = None
    tax: float | None = None


app = FastAPI()


@app.get("/item", response_model=Item)
async def read_item():
    return {
        "id": uuid.uuid4(),
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be playin' and havin' fun",
        "tags": ["breater"],
    }


client = TestClient(app)


@test
def annotations():
    response = client.get("/item")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        snapshot(
            {
                "id": IsUUID(),
                "name": "Island In The Moon",
                "price": 12.99,
                "tags": ["breater"],
                "description": "A place to be playin' and havin' fun",
                "tax": None,
            }
        )
    )
