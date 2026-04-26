from fastapi import FastAPI, Path, Query
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()


@app.get("/int/{param:int}")
def int_convertor(param: int = Path()):
    return {"int": param}


@app.get("/float/{param:float}")
def float_convertor(param: float = Path()):
    return {"float": param}


@app.get("/path/{param:path}")
def path_convertor(param: str = Path()):
    return {"path": param}


@app.get("/query/")
def query_convertor(param: str = Query()):
    return {"query": param}


client = TestClient(app)


@test
def route_converters_int():
    # Test integer conversion
    response = client.get("/int/5")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"int": 5})
    expect(app.url_path_for("int_convertor", param=5)).to_equal("/int/5")  # type: ignore


@test
def route_converters_float():
    # Test float conversion
    response = client.get("/float/25.5")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"float": 25.5})
    expect(app.url_path_for("float_convertor", param=25.5)).to_equal("/float/25.5")  # type: ignore


@test
def route_converters_path():
    # Test path conversion
    response = client.get("/path/some/example")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"path": "some/example"})


@test
def route_converters_query():
    # Test query conversion
    response = client.get("/query", params={"param": "Qué tal!"})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal({"query": "Qué tal!"})


@test
def url_path_for_path_convertor():
    expect(app.url_path_for("path_convertor", param="some/example")).to_equal(
        "/path/some/example"
    )
