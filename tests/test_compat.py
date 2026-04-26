from fastapi import FastAPI, UploadFile
from fastapi._compat import (
    Undefined,
    is_uploadfile_sequence_annotation,
)
from fastapi._compat.shared import is_bytes_sequence_annotation
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict
from pydantic.fields import FieldInfo
from tryke import expect, test


@test
def model_field_default_required():
    from fastapi._compat import v2

    # For coverage
    field_info = FieldInfo(annotation=str)
    field = v2.ModelField(name="foo", field_info=field_info)
    expect(field.default).to_be(Undefined)


@test
def complex():
    app = FastAPI()

    @app.post("/")
    def foo(foo: str | list[int]):
        return foo

    client = TestClient(app)

    response = client.post("/", json="bar")
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal("bar")

    response2 = client.post("/", json=[1, 2])
    expect(response2.status_code).to_equal(200).fatal()
    expect(response2.json()).to_equal([1, 2])


@test
def propagates_pydantic2_model_config():
    app = FastAPI()

    class Missing:
        def __bool__(self):
            return False

    class EmbeddedModel(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)
        value: str | Missing = Missing()

    class Model(BaseModel):
        model_config = ConfigDict(
            arbitrary_types_allowed=True,
        )
        value: str | Missing = Missing()
        embedded_model: EmbeddedModel = EmbeddedModel()

    @app.post("/")
    def foo(req: Model) -> dict[str, str | None]:
        return {
            "value": req.value or None,
            "embedded_value": req.embedded_model.value or None,
        }

    client = TestClient(app)

    response = client.post("/", json={})
    expect(response.status_code).to_equal(200).fatal()
    expect(response.json()).to_equal(
        {
            "value": None,
            "embedded_value": None,
        }
    )

    response2 = client.post(
        "/", json={"value": "foo", "embedded_model": {"value": "bar"}}
    )
    expect(response2.status_code).to_equal(200).fatal()
    expect(response2.json()).to_equal(
        {
            "value": "foo",
            "embedded_value": "bar",
        }
    )


@test
def is_bytes_sequence_annotation_union():
    # For coverage
    # TODO: in theory this would allow declaring types that could be lists of bytes
    # to be read from files and other types, but I'm not even sure it's a good idea
    # to support it as a first class "feature"
    expect(is_bytes_sequence_annotation(list[str] | list[bytes])).to_be_truthy()


@test
def is_uploadfile_sequence_annotation_test():
    # For coverage
    # TODO: in theory this would allow declaring types that could be lists of UploadFile
    # and other types, but I'm not even sure it's a good idea to support it as a first
    # class "feature"
    expect(
        is_uploadfile_sequence_annotation(list[str] | list[UploadFile])
    ).to_be_truthy()


@test
def serialize_sequence_value_with_optional_list():
    """Test that serialize_sequence_value handles optional lists correctly."""
    from fastapi._compat import v2

    field_info = FieldInfo(annotation=list[str] | None)
    field = v2.ModelField(name="items", field_info=field_info)
    result = v2.serialize_sequence_value(field=field, value=["a", "b", "c"])
    expect(result).to_equal(["a", "b", "c"])
    expect(result).to_be_instance_of(list)


@test
def serialize_sequence_value_with_optional_list_pipe_union():
    """Test that serialize_sequence_value handles optional lists correctly (with new syntax)."""
    from fastapi._compat import v2

    field_info = FieldInfo(annotation=list[str] | None)
    field = v2.ModelField(name="items", field_info=field_info)
    result = v2.serialize_sequence_value(field=field, value=["a", "b", "c"])
    expect(result).to_equal(["a", "b", "c"])
    expect(result).to_be_instance_of(list)


@test
def serialize_sequence_value_with_none_first_in_union():
    """Test that serialize_sequence_value handles Union[None, List[...]] correctly."""
    from typing import Union

    from fastapi._compat import v2

    # Use Union[None, list[str]] to ensure None comes first in the union args
    field_info = FieldInfo(annotation=Union[None, list[str]])  # noqa: UP007
    field = v2.ModelField(name="items", field_info=field_info)
    result = v2.serialize_sequence_value(field=field, value=["x", "y"])
    expect(result).to_equal(["x", "y"])
    expect(result).to_be_instance_of(list)
