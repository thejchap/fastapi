import warnings
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import Depends, expect, fixture, test


class State(BaseModel):
    app_startup: bool = False
    app_shutdown: bool = False
    router_startup: bool = False
    router_shutdown: bool = False
    sub_router_startup: bool = False
    sub_router_shutdown: bool = False


@fixture
def state() -> State:
    return State()


@test
def router_events(state: State = Depends(state)) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        app = FastAPI()

        @app.get("/")
        def main() -> dict[str, str]:
            return {"message": "Hello World"}

        @app.on_event("startup")
        def app_startup() -> None:
            state.app_startup = True

        @app.on_event("shutdown")
        def app_shutdown() -> None:
            state.app_shutdown = True

        router = APIRouter()

        @router.on_event("startup")
        def router_startup() -> None:
            state.router_startup = True

        @router.on_event("shutdown")
        def router_shutdown() -> None:
            state.router_shutdown = True

        sub_router = APIRouter()

        @sub_router.on_event("startup")
        def sub_router_startup() -> None:
            state.sub_router_startup = True

        @sub_router.on_event("shutdown")
        def sub_router_shutdown() -> None:
            state.sub_router_shutdown = True

        router.include_router(sub_router)
        app.include_router(router)

        expect(state.app_startup).to_be(False)
        expect(state.router_startup).to_be(False)
        expect(state.sub_router_startup).to_be(False)
        expect(state.app_shutdown).to_be(False)
        expect(state.router_shutdown).to_be(False)
        expect(state.sub_router_shutdown).to_be(False)
        with TestClient(app) as client:
            expect(state.app_startup).to_be(True)
            expect(state.router_startup).to_be(True)
            expect(state.sub_router_startup).to_be(True)
            expect(state.app_shutdown).to_be(False)
            expect(state.router_shutdown).to_be(False)
            expect(state.sub_router_shutdown).to_be(False)
            response = client.get("/")
            expect(response.status_code).to_equal(200).fatal()
            expect(response.json()).to_equal({"message": "Hello World"})
        expect(state.app_startup).to_be(True)
        expect(state.router_startup).to_be(True)
        expect(state.sub_router_startup).to_be(True)
        expect(state.app_shutdown).to_be(True)
        expect(state.router_shutdown).to_be(True)
        expect(state.sub_router_shutdown).to_be(True)


@test
def app_lifespan_state(state: State = Depends(state)) -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        state.app_startup = True
        yield
        state.app_shutdown = True

    app = FastAPI(lifespan=lifespan)

    @app.get("/")
    def main() -> dict[str, str]:
        return {"message": "Hello World"}

    expect(state.app_startup).to_be(False)
    expect(state.app_shutdown).to_be(False)
    with TestClient(app) as client:
        expect(state.app_startup).to_be(True)
        expect(state.app_shutdown).to_be(False)
        response = client.get("/")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal({"message": "Hello World"})
    expect(state.app_startup).to_be(True)
    expect(state.app_shutdown).to_be(True)


@test
def router_nested_lifespan_state(state: State = Depends(state)) -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[dict[str, bool]]:
        state.app_startup = True
        yield {"app": True}
        state.app_shutdown = True

    @asynccontextmanager
    async def router_lifespan(app: FastAPI) -> AsyncGenerator[dict[str, bool]]:
        state.router_startup = True
        yield {"router": True}
        state.router_shutdown = True

    @asynccontextmanager
    async def subrouter_lifespan(app: FastAPI) -> AsyncGenerator[dict[str, bool]]:
        state.sub_router_startup = True
        yield {"sub_router": True}
        state.sub_router_shutdown = True

    sub_router = APIRouter(lifespan=subrouter_lifespan)

    router = APIRouter(lifespan=router_lifespan)
    router.include_router(sub_router)

    app = FastAPI(lifespan=lifespan)
    app.include_router(router)

    @app.get("/")
    def main(request: Request) -> dict[str, str]:
        assert request.state.app
        assert request.state.router
        assert request.state.sub_router
        return {"message": "Hello World"}

    expect(state.app_startup).to_be(False)
    expect(state.router_startup).to_be(False)
    expect(state.sub_router_startup).to_be(False)
    expect(state.app_shutdown).to_be(False)
    expect(state.router_shutdown).to_be(False)
    expect(state.sub_router_shutdown).to_be(False)

    with TestClient(app) as client:
        expect(state.app_startup).to_be(True)
        expect(state.router_startup).to_be(True)
        expect(state.sub_router_startup).to_be(True)
        expect(state.app_shutdown).to_be(False)
        expect(state.router_shutdown).to_be(False)
        expect(state.sub_router_shutdown).to_be(False)
        response = client.get("/")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal({"message": "Hello World"})

    expect(state.app_startup).to_be(True)
    expect(state.router_startup).to_be(True)
    expect(state.sub_router_startup).to_be(True)
    expect(state.app_shutdown).to_be(True)
    expect(state.router_shutdown).to_be(True)
    expect(state.sub_router_shutdown).to_be(True)


@test
def router_nested_lifespan_state_overriding_by_parent() -> None:
    @asynccontextmanager
    async def lifespan(
        app: FastAPI,
    ) -> AsyncGenerator[dict[str, str | bool]]:
        yield {
            "app_specific": True,
            "overridden": "app",
        }

    @asynccontextmanager
    async def router_lifespan(
        app: FastAPI,
    ) -> AsyncGenerator[dict[str, str | bool]]:
        yield {
            "router_specific": True,
            "overridden": "router",  # should override parent
        }

    router = APIRouter(lifespan=router_lifespan)
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)

    with TestClient(app) as client:
        expect(client.app_state).to_equal(
            {
                "app_specific": True,
                "router_specific": True,
                "overridden": "app",
            }
        )


@test
def merged_no_return_lifespans_return_none() -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        yield

    @asynccontextmanager
    async def router_lifespan(app: FastAPI) -> AsyncGenerator[None]:
        yield

    router = APIRouter(lifespan=router_lifespan)
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)

    with TestClient(app) as client:
        expect(client.app_state).to_be_falsy()


@test
def merged_mixed_state_lifespans() -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        yield

    @asynccontextmanager
    async def router_lifespan(app: FastAPI) -> AsyncGenerator[dict[str, bool]]:
        yield {"router": True}

    @asynccontextmanager
    async def sub_router_lifespan(app: FastAPI) -> AsyncGenerator[None]:
        yield

    sub_router = APIRouter(lifespan=sub_router_lifespan)
    router = APIRouter(lifespan=router_lifespan)
    app = FastAPI(lifespan=lifespan)
    router.include_router(sub_router)
    app.include_router(router)

    with TestClient(app) as client:
        expect(client.app_state).to_equal({"router": True})


@test
def router_async_shutdown_handler(state: State = Depends(state)) -> None:
    """Test that async on_shutdown event handlers are called correctly, for coverage."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        app = FastAPI()

        @app.get("/")
        def main() -> dict[str, str]:
            return {"message": "Hello World"}

        @app.on_event("shutdown")
        async def app_shutdown() -> None:
            state.app_shutdown = True

        expect(state.app_shutdown).to_be(False)
        with TestClient(app) as client:
            expect(state.app_shutdown).to_be(False)
            response = client.get("/")
            expect(response.status_code).to_equal(200).fatal()
        expect(state.app_shutdown).to_be(True)


@test
def router_sync_generator_lifespan(state: State = Depends(state)) -> None:
    """Test that a sync generator lifespan works via _wrap_gen_lifespan_context."""
    from collections.abc import Generator

    def lifespan(app: FastAPI) -> Generator[None]:
        state.app_startup = True
        yield
        state.app_shutdown = True

    app = FastAPI(lifespan=lifespan)  # type: ignore[arg-type]

    @app.get("/")
    def main() -> dict[str, str]:
        return {"message": "Hello World"}

    expect(state.app_startup).to_be(False)
    expect(state.app_shutdown).to_be(False)
    with TestClient(app) as client:
        expect(state.app_startup).to_be(True)
        expect(state.app_shutdown).to_be(False)
        response = client.get("/")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal({"message": "Hello World"})
    expect(state.app_startup).to_be(True)
    expect(state.app_shutdown).to_be(True)


@test
def router_async_generator_lifespan(state: State = Depends(state)) -> None:
    """Test that an async generator lifespan (not wrapped) works."""

    async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
        state.app_startup = True
        yield
        state.app_shutdown = True

    app = FastAPI(lifespan=lifespan)  # type: ignore[arg-type]

    @app.get("/")
    def main() -> dict[str, str]:
        return {"message": "Hello World"}

    expect(state.app_startup).to_be(False)
    expect(state.app_shutdown).to_be(False)
    with TestClient(app) as client:
        expect(state.app_startup).to_be(True)
        expect(state.app_shutdown).to_be(False)
        response = client.get("/")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal({"message": "Hello World"})
    expect(state.app_startup).to_be(True)
    expect(state.app_shutdown).to_be(True)


@test
def startup_shutdown_handlers_as_parameters(state: State = Depends(state)) -> None:
    """Test that startup/shutdown handlers passed as parameters to FastAPI are called correctly."""

    def app_startup() -> None:
        state.app_startup = True

    def app_shutdown() -> None:
        state.app_shutdown = True

    app = FastAPI(on_startup=[app_startup], on_shutdown=[app_shutdown])

    @app.get("/")
    def main() -> dict[str, str]:
        return {"message": "Hello World"}

    def router_startup() -> None:
        state.router_startup = True

    def router_shutdown() -> None:
        state.router_shutdown = True

    router = APIRouter(on_startup=[router_startup], on_shutdown=[router_shutdown])

    def sub_router_startup() -> None:
        state.sub_router_startup = True

    def sub_router_shutdown() -> None:
        state.sub_router_shutdown = True

    sub_router = APIRouter(
        on_startup=[sub_router_startup], on_shutdown=[sub_router_shutdown]
    )

    router.include_router(sub_router)
    app.include_router(router)

    expect(state.app_startup).to_be(False)
    expect(state.router_startup).to_be(False)
    expect(state.sub_router_startup).to_be(False)
    expect(state.app_shutdown).to_be(False)
    expect(state.router_shutdown).to_be(False)
    expect(state.sub_router_shutdown).to_be(False)
    with TestClient(app) as client:
        expect(state.app_startup).to_be(True)
        expect(state.router_startup).to_be(True)
        expect(state.sub_router_startup).to_be(True)
        expect(state.app_shutdown).to_be(False)
        expect(state.router_shutdown).to_be(False)
        expect(state.sub_router_shutdown).to_be(False)
        response = client.get("/")
        expect(response.status_code).to_equal(200).fatal()
        expect(response.json()).to_equal({"message": "Hello World"})
    expect(state.app_startup).to_be(True)
    expect(state.router_startup).to_be(True)
    expect(state.sub_router_startup).to_be(True)
    expect(state.app_shutdown).to_be(True)
    expect(state.router_shutdown).to_be(True)
    expect(state.sub_router_shutdown).to_be(True)
