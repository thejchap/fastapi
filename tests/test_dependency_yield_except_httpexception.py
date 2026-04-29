from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from tryke import Depends as TrykeDepends
from tryke import expect, fixture, test

initial_fake_database = {"rick": "Rick Sanchez"}

fake_database = initial_fake_database.copy()

initial_state = {"except": False, "finally": False}

state = initial_state.copy()

app = FastAPI()


async def get_database():
    temp_database = fake_database.copy()
    try:
        yield temp_database
        fake_database.update(temp_database)
    except HTTPException:
        state["except"] = True
        raise
    finally:
        state["finally"] = True


@app.put("/invalid-user/{user_id}")
def put_invalid_user(
    user_id: str, name: str = Body(), db: dict = Depends(get_database)
):
    db[user_id] = name
    raise HTTPException(status_code=400, detail="Invalid user")


@app.put("/user/{user_id}")
def put_user(user_id: str, name: str = Body(), db: dict = Depends(get_database)):
    db[user_id] = name
    return {"message": "OK"}


@fixture
def reset_state_and_db() -> None:
    global fake_database
    global state
    fake_database = initial_fake_database.copy()
    state = initial_state.copy()


client = TestClient(app)


@test("HTTPException raised in endpoint reaches dependency's except clause")
def dependency_gets_exception(_=TrykeDepends(reset_state_and_db)):
    expect(state["except"], "except flag before request").to_be(False)
    expect(state["finally"], "finally flag before request").to_be(False)
    response = client.put("/invalid-user/rick", json="Morty")
    expect(response.status_code, "status code").to_equal(400).fatal()
    expect(response.json(), "response body").to_equal({"detail": "Invalid user"})
    expect(state["except"], "except flag after request").to_be(True)
    expect(state["finally"], "finally flag after request").to_be(True)
    expect(fake_database["rick"], "rick row should not be updated").to_equal(
        "Rick Sanchez"
    )


@test("successful request runs only finally, not except")
def dependency_no_exception(_=TrykeDepends(reset_state_and_db)):
    expect(state["except"], "except flag before request").to_be(False)
    expect(state["finally"], "finally flag before request").to_be(False)
    response = client.put("/user/rick", json="Morty")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"message": "OK"})
    expect(state["except"], "except flag after request").to_be(False)
    expect(state["finally"], "finally flag after request").to_be(True)
    expect(fake_database["rick"], "rick row should be updated").to_equal("Morty")
