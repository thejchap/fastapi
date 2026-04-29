import inspect

from fastapi import APIRouter, FastAPI
from tryke import expect, test

method_names = ["get", "put", "post", "delete", "options", "head", "patch", "trace"]


@test("HTTP method decorators share a consistent signature")
def signatures_consistency():
    base_sig = inspect.signature(APIRouter.get)
    for method_name in method_names:
        router_method = getattr(APIRouter, method_name)
        app_method = getattr(FastAPI, method_name)
        router_sig = inspect.signature(router_method)
        app_sig = inspect.signature(app_method)
        param: inspect.Parameter
        for key, param in base_sig.parameters.items():
            router_param: inspect.Parameter = router_sig.parameters[key]
            app_param: inspect.Parameter = app_sig.parameters[key]
            expect(param.annotation, f"APIRouter.{method_name}({key}) annotation").to_equal(
                router_param.annotation
            )
            expect(param.annotation, f"FastAPI.{method_name}({key}) annotation").to_equal(
                app_param.annotation
            )
            expect(param.default, f"APIRouter.{method_name}({key}) default").to_equal(
                router_param.default
            )
            expect(param.default, f"FastAPI.{method_name}({key}) default").to_equal(
                app_param.default
            )
