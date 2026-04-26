"""
Regression test: preserve order when using list[bytes] + File()
See https://github.com/fastapi/fastapi/discussions/14811
Fixed in PR: https://github.com/fastapi/fastapi/pull/14884
"""

from typing import Annotated

import anyio
from fastapi import FastAPI, File
from fastapi.testclient import TestClient
from starlette.datastructures import UploadFile as StarletteUploadFile
from tryke import expect, test

from ._shims import monkeypatch_ctx


@test
def list_bytes_file_preserves_order() -> None:
    app = FastAPI()

    @app.post("/upload")
    async def upload(files: Annotated[list[bytes], File()]):
        # return something that makes order obvious
        return [b[0] for b in files]

    original_read = StarletteUploadFile.read

    async def patched_read(self: StarletteUploadFile, size: int = -1) -> bytes:
        # Make the FIRST file slower *deterministically*
        if self.filename == "slow.txt":
            await anyio.sleep(0.05)
        return await original_read(self, size)

    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr(StarletteUploadFile, "read", patched_read)

        client = TestClient(app)

        files = [
            ("files", ("slow.txt", b"A" * 10, "text/plain")),
            ("files", ("fast.txt", b"B" * 10, "text/plain")),
        ]
        r = client.post("/upload", files=files)
        expect(r.status_code).to_equal(200).fatal()

        # Must preserve request order: slow first, fast second.
        expect(r.json()).to_equal([ord("A"), ord("B")])
