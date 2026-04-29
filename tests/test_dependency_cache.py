from fastapi import Depends, FastAPI, Security
from fastapi.testclient import TestClient
from tryke import expect, test

app = FastAPI()

counter_holder = {"counter": 0}


async def dep_counter():
    counter_holder["counter"] += 1
    return counter_holder["counter"]


async def super_dep(count: int = Depends(dep_counter)):
    return count


@app.get("/counter/")
async def get_counter(count: int = Depends(dep_counter)):
    return {"counter": count}


@app.get("/sub-counter/")
async def get_sub_counter(
    subcount: int = Depends(super_dep), count: int = Depends(dep_counter)
):
    return {"counter": count, "subcounter": subcount}


@app.get("/sub-counter-no-cache/")
async def get_sub_counter_no_cache(
    subcount: int = Depends(super_dep),
    count: int = Depends(dep_counter, use_cache=False),
):
    return {"counter": count, "subcounter": subcount}


@app.get("/scope-counter")
async def get_scope_counter(
    count: int = Security(dep_counter),
    scope_count_1: int = Security(dep_counter, scopes=["scope"]),
    scope_count_2: int = Security(dep_counter, scopes=["scope"]),
):
    return {
        "counter": count,
        "scope_counter_1": scope_count_1,
        "scope_counter_2": scope_count_2,
    }


client = TestClient(app)


@test("counter dependency increments once per request")
def normal_counter():
    counter_holder["counter"] = 0
    response = client.get("/counter/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"counter": 1})
    response = client.get("/counter/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal({"counter": 2})


@test("sub-dependency reuses cache within a request")
def sub_counter():
    counter_holder["counter"] = 0
    response = client.get("/sub-counter/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"counter": 1, "subcounter": 1}
    )
    response = client.get("/sub-counter/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"counter": 2, "subcounter": 2}
    )


@test("use_cache=False causes the dependency to run twice")
def sub_counter_no_cache():
    counter_holder["counter"] = 0
    response = client.get("/sub-counter-no-cache/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"counter": 2, "subcounter": 1}
    )
    response = client.get("/sub-counter-no-cache/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"counter": 4, "subcounter": 3}
    )


@test("Security dependencies cache distinctly per scope set")
def security_cache():
    counter_holder["counter"] = 0
    response = client.get("/scope-counter/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"counter": 1, "scope_counter_1": 2, "scope_counter_2": 2}
    )
    response = client.get("/scope-counter/")
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(response.json(), "response body").to_equal(
        {"counter": 3, "scope_counter_1": 4, "scope_counter_2": 4}
    )
