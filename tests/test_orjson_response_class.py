import importlib.util
import warnings

from tryke import expect, test

_HAS_ORJSON = importlib.util.find_spec("orjson") is not None

if _HAS_ORJSON:
    from fastapi import FastAPI
    from fastapi.exceptions import FastAPIDeprecationWarning
    from fastapi.responses import ORJSONResponse
    from fastapi.testclient import TestClient
    from sqlalchemy.sql.elements import quoted_name

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        app = FastAPI(default_response_class=ORJSONResponse)

    @app.get("/orjson_non_str_keys")
    def get_orjson_non_str_keys():
        key = quoted_name(value="msg", quote=False)
        return {key: "Hello World", 1: 1}

    client = TestClient(app)


@test.skip_if(not _HAS_ORJSON, reason="requires orjson")
@test
def orjson_non_str_keys():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FastAPIDeprecationWarning)
        with client:
            response = client.get("/orjson_non_str_keys")
    expect(response.json()).to_equal({"msg": "Hello World", "1": 1})
