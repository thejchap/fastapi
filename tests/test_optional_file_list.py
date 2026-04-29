from fastapi import FastAPI, File
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()


@app.post("/files")
async def upload_files(files: list[bytes] | None = File(None)):
    if files is None:
        return {"files_count": 0}
    return {"files_count": len(files), "sizes": [len(f) for f in files]}


@test("Optional list[bytes] file is populated when files are uploaded")
def optional_bytes_list():
    client = TestClient(app)
    response = client.post(
        "/files",
        files=[("files", b"content1"), ("files", b"content2")],
    )
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"files_count": 2, "sizes": [8, 8]}
    )


@test("Optional list[bytes] file falls back to None when no files are sent")
def optional_bytes_list_no_files():
    client = TestClient(app)
    response = client.post("/files")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"files_count": 0})
