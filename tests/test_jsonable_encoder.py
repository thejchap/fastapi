import warnings
from collections import deque
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from math import isinf, isnan
from pathlib import PurePath, PurePosixPath, PureWindowsPath
from typing import TypedDict

from fastapi._compat import Undefined
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import PydanticV1NotSupportedError
from pydantic import BaseModel, Field, ValidationError
from tryke import expect, test


class Person:
    def __init__(self, name: str):
        self.name = name


class Pet:
    def __init__(self, owner: Person, name: str):
        self.owner = owner
        self.name = name


@dataclass
class Item:
    name: str
    count: int


class DictablePerson(Person):
    def __iter__(self):
        return ((k, v) for k, v in self.__dict__.items())


class DictablePet(Pet):
    def __iter__(self):
        return ((k, v) for k, v in self.__dict__.items())


class Unserializable:
    def __iter__(self):
        raise NotImplementedError()

    @property
    def __dict__(self):
        raise NotImplementedError()


class RoleEnum(Enum):
    admin = "admin"
    normal = "normal"


class ModelWithConfig(BaseModel):
    role: RoleEnum | None = None

    model_config = {"use_enum_values": True}


class ModelWithAlias(BaseModel):
    foo: str = Field(alias="Foo")


class ModelWithDefault(BaseModel):
    foo: str = ...  # type: ignore
    bar: str = "bar"
    bla: str = "bla"


@test
def encode_dict():
    pet = {"name": "Firulais", "owner": {"name": "Foo"}}
    expect(jsonable_encoder(pet)).to_equal(
        {"name": "Firulais", "owner": {"name": "Foo"}}
    )
    expect(jsonable_encoder(pet, include={"name"})).to_equal({"name": "Firulais"})
    expect(jsonable_encoder(pet, exclude={"owner"})).to_equal({"name": "Firulais"})
    expect(jsonable_encoder(pet, include={})).to_equal({})
    expect(jsonable_encoder(pet, exclude={})).to_equal(
        {
            "name": "Firulais",
            "owner": {"name": "Foo"},
        }
    )


@test
def encode_dict_include_exclude_list():
    pet = {"name": "Firulais", "owner": {"name": "Foo"}}
    expect(jsonable_encoder(pet)).to_equal(
        {"name": "Firulais", "owner": {"name": "Foo"}}
    )
    expect(jsonable_encoder(pet, include=["name"])).to_equal({"name": "Firulais"})
    expect(jsonable_encoder(pet, exclude=["owner"])).to_equal({"name": "Firulais"})
    expect(jsonable_encoder(pet, include=[])).to_equal({})
    expect(jsonable_encoder(pet, exclude=[])).to_equal(
        {
            "name": "Firulais",
            "owner": {"name": "Foo"},
        }
    )


@test
def encode_class():
    person = Person(name="Foo")
    pet = Pet(owner=person, name="Firulais")
    expect(jsonable_encoder(pet)).to_equal(
        {"name": "Firulais", "owner": {"name": "Foo"}}
    )
    expect(jsonable_encoder(pet, include={"name"})).to_equal({"name": "Firulais"})
    expect(jsonable_encoder(pet, exclude={"owner"})).to_equal({"name": "Firulais"})
    expect(jsonable_encoder(pet, include={})).to_equal({})
    expect(jsonable_encoder(pet, exclude={})).to_equal(
        {
            "name": "Firulais",
            "owner": {"name": "Foo"},
        }
    )


@test
def encode_dictable():
    person = DictablePerson(name="Foo")
    pet = DictablePet(owner=person, name="Firulais")
    expect(jsonable_encoder(pet)).to_equal(
        {"name": "Firulais", "owner": {"name": "Foo"}}
    )
    expect(jsonable_encoder(pet, include={"name"})).to_equal({"name": "Firulais"})
    expect(jsonable_encoder(pet, exclude={"owner"})).to_equal({"name": "Firulais"})
    expect(jsonable_encoder(pet, include={})).to_equal({})
    expect(jsonable_encoder(pet, exclude={})).to_equal(
        {
            "name": "Firulais",
            "owner": {"name": "Foo"},
        }
    )


@test
def encode_dataclass():
    item = Item(name="foo", count=100)
    expect(jsonable_encoder(item)).to_equal({"name": "foo", "count": 100})
    expect(jsonable_encoder(item, include={"name"})).to_equal({"name": "foo"})
    expect(jsonable_encoder(item, exclude={"count"})).to_equal({"name": "foo"})
    expect(jsonable_encoder(item, include={})).to_equal({})
    expect(jsonable_encoder(item, exclude={})).to_equal({"name": "foo", "count": 100})


@test
def encode_unsupported():
    unserializable = Unserializable()
    expect(lambda: jsonable_encoder(unserializable)).to_raise(ValueError)


@test
def encode_custom_json_encoders_model_pydanticv2():
    from pydantic import field_serializer

    class ModelWithCustomEncoder(BaseModel):
        dt_field: datetime

        @field_serializer("dt_field")
        def serialize_dt_field(self, dt):
            return dt.replace(microsecond=0, tzinfo=UTC).isoformat()

    class ModelWithCustomEncoderSubclass(ModelWithCustomEncoder):
        pass

    model = ModelWithCustomEncoder(dt_field=datetime(2019, 1, 1, 8))
    expect(jsonable_encoder(model)).to_equal({"dt_field": "2019-01-01T08:00:00+00:00"})
    subclass_model = ModelWithCustomEncoderSubclass(dt_field=datetime(2019, 1, 1, 8))
    expect(jsonable_encoder(subclass_model)).to_equal(
        {"dt_field": "2019-01-01T08:00:00+00:00"}
    )


@test
def json_encoder_error_with_pydanticv1():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        from pydantic import v1

    class ModelV1(v1.BaseModel):
        name: str

    data = ModelV1(name="test")
    expect(lambda: jsonable_encoder(data)).to_raise(PydanticV1NotSupportedError)


@test
def encode_model_with_config():
    model = ModelWithConfig(role=RoleEnum.admin)
    expect(jsonable_encoder(model)).to_equal({"role": "admin"})


@test
def encode_model_with_alias_raises():
    expect(lambda: ModelWithAlias(foo="Bar")).to_raise(ValidationError)


@test
def encode_model_with_alias():
    model = ModelWithAlias(Foo="Bar")
    expect(jsonable_encoder(model)).to_equal({"Foo": "Bar"})


@test
def encode_model_with_default():
    model = ModelWithDefault(foo="foo", bar="bar")
    expect(jsonable_encoder(model)).to_equal({"foo": "foo", "bar": "bar", "bla": "bla"})
    expect(jsonable_encoder(model, exclude_unset=True)).to_equal(
        {"foo": "foo", "bar": "bar"}
    )
    expect(jsonable_encoder(model, exclude_defaults=True)).to_equal({"foo": "foo"})
    expect(jsonable_encoder(model, exclude_unset=True, exclude_defaults=True)).to_equal(
        {"foo": "foo"}
    )
    expect(jsonable_encoder(model, include={"foo"})).to_equal({"foo": "foo"})
    expect(jsonable_encoder(model, exclude={"bla"})).to_equal(
        {"foo": "foo", "bar": "bar"}
    )
    expect(jsonable_encoder(model, include={})).to_equal({})
    expect(jsonable_encoder(model, exclude={})).to_equal(
        {
            "foo": "foo",
            "bar": "bar",
            "bla": "bla",
        }
    )


@test
def custom_encoders():
    class safe_datetime(datetime):
        pass

    class MyDict(TypedDict):
        dt_field: safe_datetime

    instance = MyDict(dt_field=safe_datetime.now())

    encoded_instance = jsonable_encoder(
        instance, custom_encoder={safe_datetime: lambda o: o.strftime("%H:%M:%S")}
    )
    expect(encoded_instance["dt_field"]).to_equal(
        instance["dt_field"].strftime("%H:%M:%S")
    )

    encoded_instance = jsonable_encoder(
        instance, custom_encoder={datetime: lambda o: o.strftime("%H:%M:%S")}
    )
    expect(encoded_instance["dt_field"]).to_equal(
        instance["dt_field"].strftime("%H:%M:%S")
    )

    encoded_instance2 = jsonable_encoder(instance)
    expect(encoded_instance2["dt_field"]).to_equal(instance["dt_field"].isoformat())


@test
def custom_enum_encoders():
    def custom_enum_encoder(v: Enum):
        return v.value.lower()

    class MyEnum(Enum):
        ENUM_VAL_1 = "ENUM_VAL_1"

    instance = MyEnum.ENUM_VAL_1

    encoded_instance = jsonable_encoder(
        instance, custom_encoder={MyEnum: custom_enum_encoder}
    )
    expect(encoded_instance).to_equal(custom_enum_encoder(instance))


@test
def encode_model_with_pure_path():
    class ModelWithPath(BaseModel):
        path: PurePath

        model_config = {"arbitrary_types_allowed": True}

    test_path = PurePath("/foo", "bar")
    obj = ModelWithPath(path=test_path)
    expect(jsonable_encoder(obj)).to_equal({"path": str(test_path)})


@test
def encode_model_with_pure_posix_path():
    class ModelWithPath(BaseModel):
        path: PurePosixPath

        model_config = {"arbitrary_types_allowed": True}

    obj = ModelWithPath(path=PurePosixPath("/foo", "bar"))
    expect(jsonable_encoder(obj)).to_equal({"path": "/foo/bar"})


@test
def encode_model_with_pure_windows_path():
    class ModelWithPath(BaseModel):
        path: PureWindowsPath

        model_config = {"arbitrary_types_allowed": True}

    obj = ModelWithPath(path=PureWindowsPath("/foo", "bar"))
    expect(jsonable_encoder(obj)).to_equal({"path": "\\foo\\bar"})


@test
def encode_pure_path():
    test_path = PurePath("/foo", "bar")

    expect(jsonable_encoder({"path": test_path})).to_equal({"path": str(test_path)})


@test
def decimal_encoder_float():
    data = {"value": Decimal(1.23)}
    expect(jsonable_encoder(data)).to_equal({"value": 1.23})


@test
def decimal_encoder_int():
    data = {"value": Decimal(2)}
    expect(jsonable_encoder(data)).to_equal({"value": 2})


@test
def decimal_encoder_nan():
    data = {"value": Decimal("NaN")}
    expect(isnan(jsonable_encoder(data)["value"])).to_be_truthy()


@test
def decimal_encoder_infinity():
    data = {"value": Decimal("Infinity")}
    expect(isinf(jsonable_encoder(data)["value"])).to_be_truthy()
    data = {"value": Decimal("-Infinity")}
    expect(isinf(jsonable_encoder(data)["value"])).to_be_truthy()


@test
def encode_deque_encodes_child_models():
    class Model(BaseModel):
        test: str

    dq = deque([Model(test="test")])

    expect(jsonable_encoder(dq)[0]["test"]).to_equal("test")


@test
def encode_pydantic_undefined():
    data = {"value": Undefined}
    expect(jsonable_encoder(data)).to_equal({"value": None})


@test.cases(
    test.case("pydantic.color", module_path="pydantic.color"),
    test.case("pydantic_extra_types.color", module_path="pydantic_extra_types.color"),
)
def encode_color(module_path: str):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        try:
            Color = __import__(module_path, fromlist=["Color"]).Color
        except ImportError:  # pragma: no cover
            return  # Skip when not installed.

        data = {"color": Color("blue")}
        expect(jsonable_encoder(data)).to_equal({"color": "blue"})
