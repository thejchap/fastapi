# Ref: https://github.com/fastapi/fastapi/discussions/6024#discussioncomment-8541913


from typing import Annotated

from fastapi import Depends, FastAPI, Security
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient
from tryke import Depends as TrykeDepends
from tryke import expect, fixture, test


@fixture
def call_counts() -> dict[str, int]:
    return {
        "get_db_session": 0,
        "get_current_user": 0,
        "get_user_me": 0,
        "get_user_items": 0,
    }


@fixture
def app(call_counts: dict[str, int] = TrykeDepends(call_counts)) -> FastAPI:
    def get_db_session():
        call_counts["get_db_session"] += 1
        return f"db_session_{call_counts['get_db_session']}"

    def get_current_user(
        security_scopes: SecurityScopes,
        db_session: Annotated[str, Depends(get_db_session)],
    ):
        call_counts["get_current_user"] += 1
        return {
            "user": f"user_{call_counts['get_current_user']}",
            "scopes": security_scopes.scopes,
            "db_session": db_session,
        }

    def get_user_me(
        current_user: Annotated[dict, Security(get_current_user, scopes=["me"])],
    ):
        call_counts["get_user_me"] += 1
        return {
            "user_me": f"user_me_{call_counts['get_user_me']}",
            "current_user": current_user,
        }

    def get_user_items(
        user_me: Annotated[dict, Depends(get_user_me)],
    ):
        call_counts["get_user_items"] += 1
        return {
            "user_items": f"user_items_{call_counts['get_user_items']}",
            "user_me": user_me,
        }

    app = FastAPI()

    @app.get("/")
    def path_operation(
        user_me: Annotated[dict, Depends(get_user_me)],
        user_items: Annotated[dict, Security(get_user_items, scopes=["items"])],
    ):
        return {
            "user_me": user_me,
            "user_items": user_items,
        }

    return app


@fixture
def client(app: FastAPI = TrykeDepends(app)) -> TestClient:
    return TestClient(app)


@test("Sub-dependencies with different Security scopes are cached per scope set")
def security_scopes_sub_dependency_caching(
    client: TestClient = TrykeDepends(client),
    call_counts: dict[str, int] = TrykeDepends(call_counts),
):
    response = client.get("/")

    expect(response.status_code, "status code").to_equal(200)
    expect(call_counts["get_db_session"], "get_db_session call count").to_equal(1)
    expect(call_counts["get_current_user"], "get_current_user call count").to_equal(2)
    expect(call_counts["get_user_me"], "get_user_me call count").to_equal(2)
    expect(call_counts["get_user_items"], "get_user_items call count").to_equal(1)
    expect(response.json(), "response body").to_equal(
        {
            "user_me": {
                "user_me": "user_me_1",
                "current_user": {
                    "user": "user_1",
                    "scopes": ["me"],
                    "db_session": "db_session_1",
                },
            },
            "user_items": {
                "user_items": "user_items_1",
                "user_me": {
                    "user_me": "user_me_2",
                    "current_user": {
                        "user": "user_2",
                        "scopes": ["items", "me"],
                        "db_session": "db_session_1",
                    },
                },
            },
        }
    )
