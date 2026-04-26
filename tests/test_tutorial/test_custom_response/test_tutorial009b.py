from pathlib import Path

from fastapi.testclient import TestClient
from tryke import expect, test

from docs_src.custom_response import tutorial009b_py310
from docs_src.custom_response.tutorial009b_py310 import app

from ..._shims import tmp_path_ctx

client = TestClient(app)


@test
def get():
    with tmp_path_ctx() as tmp_path:
        file_path: Path = tmp_path / "large-video-file.mp4"
        tutorial009b_py310.some_file_path = str(file_path)
        test_content = b"Fake video bytes"
        file_path.write_bytes(test_content)
        response = client.get("/")
        expect(response.content).to_equal(test_content)
