from pathlib import Path

from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from tryke import expect, test

from ..._shims import monkeypatch_ctx, tmp_path_ctx


def _build_client(static_dir: Path) -> TestClient:
    sample_file = static_dir / "sample.txt"
    sample_file.write_text("This is a sample static file.")
    # Reload the docs_src module fresh because StaticFiles binds the
    # `directory="static"` at module import time relative to the current
    # working directory.
    import importlib

    from docs_src.static_files import tutorial001_py310

    importlib.reload(tutorial001_py310)
    return TestClient(tutorial001_py310.app)


@test
def static_files():
    with tmp_path_ctx() as tmp_path, monkeypatch_ctx() as mp:
        mp.chdir(tmp_path)
        static_dir = tmp_path / "static"
        static_dir.mkdir()
        with _build_client(static_dir) as client:
            response = client.get("/static/sample.txt")
            expect(response.status_code).to_equal(200).fatal()
            expect(response.text).to_equal("This is a sample static file.")


@test
def static_files_not_found():
    with tmp_path_ctx() as tmp_path, monkeypatch_ctx() as mp:
        mp.chdir(tmp_path)
        static_dir = tmp_path / "static"
        static_dir.mkdir()
        with _build_client(static_dir) as client:
            response = client.get("/static/non_existent_file.txt")
            expect(response.status_code).to_equal(404).fatal()


@test
def openapi_schema():
    with tmp_path_ctx() as tmp_path, monkeypatch_ctx() as mp:
        mp.chdir(tmp_path)
        static_dir = tmp_path / "static"
        static_dir.mkdir()
        with _build_client(static_dir) as client:
            response = client.get("/openapi.json")
            expect(response.status_code).to_equal(200).fatal()
            expect(response.json()).to_equal(
                snapshot(
                    {
                        "openapi": "3.1.0",
                        "info": {"title": "FastAPI", "version": "0.1.0"},
                        "paths": {},
                    }
                )
            )
