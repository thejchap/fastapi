from typing import Annotated

from fastapi import FastAPI, HTTPException, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def process_auth(
    credentials: Annotated[str | None, Security(oauth2_scheme)],
    security_scopes: SecurityScopes,
):
    # This is an incorrect way of using it, this is not checking if the scopes are
    # provided by the token, only if the endpoint is requesting them, but the test
    # here is just to check if FastAPI is indeed registering and passing the scopes
    # correctly when using Security with parameterless dependencies.
    if "a" not in security_scopes.scopes or "b" not in security_scopes.scopes:
        raise HTTPException(detail="a or b not in scopes", status_code=401)
    return {"token": credentials, "scopes": security_scopes.scopes}


@app.get("/get-credentials")
def get_credentials(
    credentials: Annotated[dict, Security(process_auth, scopes=["a", "b"])],
):
    return credentials


@app.get(
    "/parameterless-with-scopes",
    dependencies=[Security(process_auth, scopes=["a", "b"])],
)
def get_parameterless_with_scopes():
    return {"status": "ok"}


@app.get(
    "/parameterless-without-scopes",
    dependencies=[Security(process_auth)],
)
def get_parameterless_without_scopes():
    return {"status": "ok"}


client = TestClient(app)


@test("Security() with scopes passes credentials and scopes through")
def get_credentials_test():
    response = client.get("/get-credentials", headers={"authorization": "Bearer token"})
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"token": "token", "scopes": ["a", "b"]}
    )


@test("parameterless Security with scopes accepts request")
def parameterless_with_scopes():
    response = client.get(
        "/parameterless-with-scopes", headers={"authorization": "Bearer token"}
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"status": "ok"})


@test("parameterless Security without scopes rejects request")
def parameterless_without_scopes():
    response = client.get(
        "/parameterless-without-scopes", headers={"authorization": "Bearer token"}
    )
    expect(response.status_code, "status code").to_equal(401).fatal()
    expect(response.json(), "response body").to_equal(
        {"detail": "a or b not in scopes"}
    )


@test("calling endpoint directly returns the static body")
def call_get_parameterless_without_scopes_for_coverage():
    expect(get_parameterless_without_scopes(), "endpoint return value").to_equal(
        {"status": "ok"}
    )
