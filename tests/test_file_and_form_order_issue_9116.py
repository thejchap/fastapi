"""
Regression test, Error 422 if Form is declared before File
See https://github.com/tiangolo/fastapi/discussions/9116
"""

from typing import Annotated

from fastapi import FastAPI, File, Form
from fastapi.testclient import TestClient
from tryke import expect, test

from ._shims import tmp_path_ctx

app = FastAPI()


@app.post("/file_before_form")
def file_before_form(
    file: bytes = File(),
    city: str = Form(),
):
    return {"file_content": file, "city": city}


@app.post("/file_after_form")
def file_after_form(
    city: str = Form(),
    file: bytes = File(),
):
    return {"file_content": file, "city": city}


@app.post("/file_list_before_form")
def file_list_before_form(
    files: Annotated[list[bytes], File()],
    city: Annotated[str, Form()],
):
    return {"file_contents": files, "city": city}


@app.post("/file_list_after_form")
def file_list_after_form(
    city: Annotated[str, Form()],
    files: Annotated[list[bytes], File()],
):
    return {"file_contents": files, "city": city}


client = TestClient(app)


@test.cases(
    test.case("file_before_form", endpoint_path="/file_before_form"),
    test.case("file_after_form", endpoint_path="/file_after_form"),
)
def file_form_order(endpoint_path: str):
    with tmp_path_ctx() as tmp_path:
        tmp_file_1 = tmp_path / "example1.txt"
        tmp_file_1.write_text("foo")
        response = client.post(
            url=endpoint_path,
            data={"city": "Thimphou"},
            files={"file": (tmp_file_1.name, tmp_file_1.read_bytes())},
        )
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.json(), "response body").to_equal(
            {"file_content": "foo", "city": "Thimphou"}
        )


@test.cases(
    test.case("file_list_before_form", endpoint_path="/file_list_before_form"),
    test.case("file_list_after_form", endpoint_path="/file_list_after_form"),
)
def file_list_form_order(endpoint_path: str):
    with tmp_path_ctx() as tmp_path:
        tmp_file_1 = tmp_path / "example1.txt"
        tmp_file_1.write_text("foo")
        tmp_file_2 = tmp_path / "example2.txt"
        tmp_file_2.write_text("bar")
        response = client.post(
            url=endpoint_path,
            data={"city": "Thimphou"},
            files=(
                ("files", (tmp_file_1.name, tmp_file_1.read_bytes())),
                ("files", (tmp_file_2.name, tmp_file_2.read_bytes())),
            ),
        )
        expect(response.status_code, "status code").to_equal(200).fatal()
        expect(response.json(), "response body").to_equal(
            {"file_contents": ["foo", "bar"], "city": "Thimphou"}
        )
