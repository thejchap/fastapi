from fastapi import FastAPI
from fastapi.testclient import TestClient
from tryke import expect, test


@test
def root_path_does_not_persist_across_requests():
    app = FastAPI()

    @app.get("/")
    def read_root():  # pragma: no cover
        return {"ok": True}

    # Attacker request with a spoofed root_path
    attacker_client = TestClient(app, root_path="/evil-api")
    response1 = attacker_client.get("/openapi.json")
    data1 = response1.json()
    expect(
        any(s.get("url") == "/evil-api" for s in data1.get("servers", []))
    ).to_be_truthy()

    # Subsequent legitimate request with no root_path
    clean_client = TestClient(app)
    response2 = clean_client.get("/openapi.json")
    data2 = response2.json()
    servers = [s.get("url") for s in data2.get("servers", [])]
    expect(servers).not_.to_contain("/evil-api")


@test
def multiple_different_root_paths_do_not_accumulate():
    app = FastAPI()

    @app.get("/")
    def read_root():  # pragma: no cover
        return {"ok": True}

    for prefix in ["/path-a", "/path-b", "/path-c"]:
        c = TestClient(app, root_path=prefix)
        c.get("/openapi.json")

    # A clean request should not have any of them
    clean_client = TestClient(app)
    response = clean_client.get("/openapi.json")
    data = response.json()
    servers = [s.get("url") for s in data.get("servers", [])]
    for prefix in ["/path-a", "/path-b", "/path-c"]:
        expect(servers).not_.to_contain(prefix)


@test
def legitimate_root_path_still_appears():
    app = FastAPI()

    @app.get("/")
    def read_root():  # pragma: no cover
        return {"ok": True}

    client = TestClient(app, root_path="/api/v1")
    response = client.get("/openapi.json")
    data = response.json()
    servers = [s.get("url") for s in data.get("servers", [])]
    expect(servers).to_contain("/api/v1")


@test
def configured_servers_not_mutated():
    configured_servers = [{"url": "https://prod.example.com"}]
    app = FastAPI(servers=configured_servers)

    @app.get("/")
    def read_root():  # pragma: no cover
        return {"ok": True}

    # Request with a rogue root_path
    attacker_client = TestClient(app, root_path="/evil")
    attacker_client.get("/openapi.json")

    # The original servers list must be untouched
    expect(configured_servers).to_equal([{"url": "https://prod.example.com"}])
