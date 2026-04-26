from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()

router_lax = APIRouter(prefix="/lax", strict_content_type=False)
router_strict = APIRouter(prefix="/strict", strict_content_type=True)
router_default = APIRouter(prefix="/default")


@router_lax.post("/items/")
async def router_lax_post(data: dict):
    return data


@router_strict.post("/items/")
async def router_strict_post(data: dict):
    return data


@router_default.post("/items/")
async def router_default_post(data: dict):
    return data


app.include_router(router_lax)
app.include_router(router_strict)
app.include_router(router_default)

client = TestClient(app)


@test
def lax_router_on_strict_app_accepts_no_content_type():
    response = client.post("/lax/items/", content='{"key": "value"}')
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"key": "value"})


@test
def strict_router_on_strict_app_rejects_no_content_type():
    response = client.post("/strict/items/", content='{"key": "value"}')
    expect(response.status_code).to_equal(422)


@test
def default_router_inherits_strict_from_app():
    response = client.post("/default/items/", content='{"key": "value"}')
    expect(response.status_code).to_equal(422)


@test
def lax_router_accepts_json_content_type():
    response = client.post("/lax/items/", json={"key": "value"})
    expect(response.status_code).to_equal(200)


@test
def strict_router_accepts_json_content_type():
    response = client.post("/strict/items/", json={"key": "value"})
    expect(response.status_code).to_equal(200)


@test
def default_router_accepts_json_content_type():
    response = client.post("/default/items/", json={"key": "value"})
    expect(response.status_code).to_equal(200)
