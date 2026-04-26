from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from tryke import expect, test


class CustomError(Exception):
    pass


def catching_dep() -> Any:
    try:
        yield "s"
    except CustomError as err:
        raise HTTPException(status_code=418, detail="Session error") from err


def broken_dep() -> Any:
    yield "s"
    raise ValueError("Broken after yield")


app = FastAPI()


@app.get("/catching")
def catching(d: Annotated[str, Depends(catching_dep)]) -> Any:
    raise CustomError("Simulated error during streaming")


@app.get("/broken")
def broken(d: Annotated[str, Depends(broken_dep)]) -> Any:
    return {"message": "all good?"}


client = TestClient(app)


@test
def catching_test():
    response = client.get("/catching")
    expect(response.status_code).to_equal(418)
    expect(response.json()).to_equal({"detail": "Session error"})


@test
def broken_raise():
    expect(lambda: client.get("/broken")).to_raise(
        ValueError, match="Broken after yield"
    )


@test
def broken_no_raise():
    """
    When a dependency with yield raises after the yield (not in an except), the
    response is already "successfully" sent back to the client, but there's still
    an error in the server afterwards, an exception is raised and captured or shown
    in the server logs.
    """
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/broken")
        expect(response.status_code).to_equal(200)
        expect(response.json()).to_equal({"message": "all good?"})


@test
def broken_return_finishes():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/broken")
    expect(response.status_code).to_equal(200)
    expect(response.json()).to_equal({"message": "all good?"})
