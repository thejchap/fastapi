import warnings

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.dependencies.utils import (
    multipart_incorrect_install_error,
    multipart_not_installed_error,
)
from tryke import expect, test

from ._shims import monkeypatch_ctx


@test("Form param raises a helpful error when python-multipart is misinstalled")
def incorrect_multipart_installed_form():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr("python_multipart.__version__", "0.0.12")
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            import multipart.multipart as _mp

            monkeypatch.delattr(_mp, "parse_options_header", raising=False)

        def _body():
            app = FastAPI()

            @app.post("/")
            async def root(username: str = Form()):
                return username  # pragma: nocover

        expect(_body, "registering a Form route").to_raise(
            RuntimeError, match=multipart_incorrect_install_error
        )


@test("UploadFile route raises a helpful error when python-multipart is misinstalled")
def incorrect_multipart_installed_file_upload():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr("python_multipart.__version__", "0.0.12")
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            import multipart.multipart as _mp

            monkeypatch.delattr(_mp, "parse_options_header", raising=False)

        def _body():
            app = FastAPI()

            @app.post("/")
            async def root(f: UploadFile = File()):
                return f  # pragma: nocover

        expect(_body, "registering an UploadFile route").to_raise(
            RuntimeError, match=multipart_incorrect_install_error
        )


@test("bytes File route raises a helpful error when python-multipart is misinstalled")
def incorrect_multipart_installed_file_bytes():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr("python_multipart.__version__", "0.0.12")
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            import multipart.multipart as _mp

            monkeypatch.delattr(_mp, "parse_options_header", raising=False)

        def _body():
            app = FastAPI()

            @app.post("/")
            async def root(f: bytes = File()):
                return f  # pragma: nocover

        expect(_body, "registering a bytes File route").to_raise(
            RuntimeError, match=multipart_incorrect_install_error
        )


@test("Multi-Form route raises a helpful error when python-multipart is misinstalled")
def incorrect_multipart_installed_multi_form():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr("python_multipart.__version__", "0.0.12")
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            import multipart.multipart as _mp

            monkeypatch.delattr(_mp, "parse_options_header", raising=False)

        def _body():
            app = FastAPI()

            @app.post("/")
            async def root(username: str = Form(), password: str = Form()):
                return username  # pragma: nocover

        expect(_body, "registering a multi-Form route").to_raise(
            RuntimeError, match=multipart_incorrect_install_error
        )


@test("Form+File route raises a helpful error when python-multipart is misinstalled")
def incorrect_multipart_installed_form_file():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr("python_multipart.__version__", "0.0.12")
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            import multipart.multipart as _mp

            monkeypatch.delattr(_mp, "parse_options_header", raising=False)

        def _body():
            app = FastAPI()

            @app.post("/")
            async def root(username: str = Form(), f: UploadFile = File()):
                return username  # pragma: nocover

        expect(_body, "registering a Form+File route").to_raise(
            RuntimeError, match=multipart_incorrect_install_error
        )


@test("Form route raises a helpful error when python-multipart is missing")
def no_multipart_installed():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr("python_multipart.__version__", "0.0.12")
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            import multipart as _multipart

            monkeypatch.delattr(_multipart, "__version__", raising=False)

            def _body():
                app = FastAPI()

                @app.post("/")
                async def root(username: str = Form()):
                    return username  # pragma: nocover

            expect(_body, "registering a Form route").to_raise(
                RuntimeError, match=multipart_not_installed_error
            )


@test("UploadFile route raises a helpful error when python-multipart is missing")
def no_multipart_installed_file():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr("python_multipart.__version__", "0.0.12")
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            import multipart as _multipart

            monkeypatch.delattr(_multipart, "__version__", raising=False)

            def _body():
                app = FastAPI()

                @app.post("/")
                async def root(f: UploadFile = File()):
                    return f  # pragma: nocover

            expect(_body, "registering an UploadFile route").to_raise(
                RuntimeError, match=multipart_not_installed_error
            )


@test("bytes File route raises a helpful error when python-multipart is missing")
def no_multipart_installed_file_bytes():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr("python_multipart.__version__", "0.0.12")
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            import multipart as _multipart

            monkeypatch.delattr(_multipart, "__version__", raising=False)

            def _body():
                app = FastAPI()

                @app.post("/")
                async def root(f: bytes = File()):
                    return f  # pragma: nocover

            expect(_body, "registering a bytes File route").to_raise(
                RuntimeError, match=multipart_not_installed_error
            )


@test("Multi-Form route raises a helpful error when python-multipart is missing")
def no_multipart_installed_multi_form():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr("python_multipart.__version__", "0.0.12")
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            import multipart as _multipart

            monkeypatch.delattr(_multipart, "__version__", raising=False)

            def _body():
                app = FastAPI()

                @app.post("/")
                async def root(username: str = Form(), password: str = Form()):
                    return username  # pragma: nocover

            expect(_body, "registering a multi-Form route").to_raise(
                RuntimeError, match=multipart_not_installed_error
            )


@test("Form+File route raises a helpful error when python-multipart is missing")
def no_multipart_installed_form_file():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr("python_multipart.__version__", "0.0.12")
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            import multipart as _multipart

            monkeypatch.delattr(_multipart, "__version__", raising=False)

            def _body():
                app = FastAPI()

                @app.post("/")
                async def root(username: str = Form(), f: UploadFile = File()):
                    return username  # pragma: nocover

            expect(_body, "registering a Form+File route").to_raise(
                RuntimeError, match=multipart_not_installed_error
            )


@test("Old python-multipart installs work without error")
def old_multipart_installed():
    with monkeypatch_ctx() as monkeypatch:
        monkeypatch.setattr("python_multipart.__version__", "0.0.12")
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            app = FastAPI()

            @app.post("/")
            async def root(username: str = Form()):
                return username  # pragma: nocover
