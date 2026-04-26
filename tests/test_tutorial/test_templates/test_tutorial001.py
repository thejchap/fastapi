import os
import shutil

from fastapi.testclient import TestClient
from tryke import expect, test


@test
def main():
    if os.path.isdir("./static"):  # pragma: nocover
        shutil.rmtree("./static")
    if os.path.isdir("./templates"):  # pragma: nocover
        shutil.rmtree("./templates")
    shutil.copytree("./docs_src/templates/templates/", "./templates")
    shutil.copytree("./docs_src/templates/static/", "./static")
    from docs_src.templates.tutorial001_py310 import app

    client = TestClient(app)
    response = client.get("/items/foo")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.content).to_contain(
        b'<h1><a href="http://testserver/items/foo">Item ID: foo</a></h1>'
    )
    response = client.get("/static/styles.css")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.content).to_contain(b"color: green;")
    shutil.rmtree("./templates")
    shutil.rmtree("./static")
