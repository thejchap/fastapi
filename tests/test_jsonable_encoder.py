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


@test("jsonable_encoder handles dict with include/exclude sets")
def encode_dict():
    pet = {"name": "Firulais", "owner": {"name": "Foo"}}
    expect(jsonable_encoder(pet), "encoded dict").to_equal(
        {"name": "Firulais", "owner": {"name": "Foo"}}
    )
    expect(jsonable_encoder(pet, include={"name"}), "include={name}").to_equal(
        {"name": "Firulais"}
    )
    expect(jsonable_encoder(pet, exclude={"owner"}), "exclude={owner}").to_equal(
        {"name": "Firulais"}
    )
    expect(jsonable_encoder(pet, include={}), "include={}").to_equal({})
    expect(jsonable_encoder(pet, exclude={}), "exclude={}").to_equal(
        {
            "name": "Firulais",
            "owner": {"name": "Foo"},
        }
    )


@test("jsonable_encoder handles dict with include/exclude lists")
def encode_dict_include_exclude_list():
    pet = {"name": "Firulais", "owner": {"name": "Foo"}}
    expect(jsonable_encoder(pet), "encoded dict").to_equal(
        {"name": "Firulais", "owner": {"name": "Foo"}}
    )
    expect(jsonable_encoder(pet, include=["name"]), "include=[name]").to_equal(
        {"name": "Firulais"}
    )
    expect(jsonable_encoder(pet, exclude=["owner"]), "exclude=[owner]").to_equal(
        {"name": "Firulais"}
    )
    expect(jsonable_encoder(pet, include=[]), "include=[]").to_equal({})
    expect(jsonable_encoder(pet, exclude=[]), "exclude=[]").to_equal(
        {
            "name": "Firulais",
            "owner": {"name": "Foo"},
        }
    )


@test("jsonable_encoder handles plain classes via __dict__")
def encode_class():
    person = Person(name="Foo")
    pet = Pet(owner=person, name="Firulais")
    expect(jsonable_encoder(pet), "encoded class").to_equal(
        {"name": "Firulais", "owner": {"name": "Foo"}}
    )
    expect(jsonable_encoder(pet, include={"name"}), "include={name}").to_equal(
        {"name": "Firulais"}
    )
    expect(jsonable_encoder(pet, exclude={"owner"}), "exclude={owner}").to_equal(
        {"name": "Firulais"}
    )
    expect(jsonable_encoder(pet, include={}), "include={}").to_equal({})
    expect(jsonable_encoder(pet, exclude={}), "exclude={}").to_equal(
        {
            "name": "Firulais",
            "owner": {"name": "Foo"},
        }
    )


@test("jsonable_encoder handles classes with __iter__")
def encode_dictable():
    person = DictablePerson(name="Foo")
    pet = DictablePet(owner=person, name="Firulais")
    expect(jsonable_encoder(pet), "encoded dictable").to_equal(
        {"name": "Firulais", "owner": {"name": "Foo"}}
    )
    expect(jsonable_encoder(pet, include={"name"}), "include={name}").to_equal(
        {"name": "Firulais"}
    )
    expect(jsonable_encoder(pet, exclude={"owner"}), "exclude={owner}").to_equal(
        {"name": "Firulais"}
    )
    expect(jsonable_encoder(pet, include={}), "include={}").to_equal({})
    expect(jsonable_encoder(pet, exclude={}), "exclude={}").to_equal(
        {
            "name": "Firulais",
            "owner": {"name": "Foo"},
        }
    )


@test("jsonable_encoder handles dataclasses")
def encode_dataclass():
    item = Item(name="foo", count=100)
    expect(jsonable_encoder(item), "encoded dataclass").to_equal(
        {"name": "foo", "count": 100}
    )
    expect(jsonable_encoder(item, include={"name"}), "include={name}").to_equal(
        {"name": "foo"}
    )
    expect(jsonable_encoder(item, exclude={"count"}), "exclude={count}").to_equal(
        {"name": "foo"}
    )
    expect(jsonable_encoder(item, include={}), "include={}").to_equal({})
    expect(jsonable_encoder(item, exclude={}), "exclude={}").to_equal(
        {"name": "foo", "count": 100}
    )


@test("jsonable_encoder raises ValueError on unsupported objects")
def encode_unsupported():
    unserializable = Unserializable()
    expect(
        lambda: jsonable_encoder(unserializable),
        "encoding an unsupported object",
    ).to_raise(ValueError)


@test("jsonable_encoder uses pydantic v2 field serializers")
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
    expect(jsonable_encoder(model), "encoded model").to_equal(
        {"dt_field": "2019-01-01T08:00:00+00:00"}
    )
    subclass_model = ModelWithCustomEncoderSubclass(dt_field=datetime(2019, 1, 1, 8))
    expect(jsonable_encoder(subclass_model), "encoded subclass model").to_equal(
        {"dt_field": "2019-01-01T08:00:00+00:00"}
    )


@test("jsonable_encoder rejects pydantic v1 models with a clear error")
def json_encoder_error_with_pydanticv1():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        from pydantic import v1

    class ModelV1(v1.BaseModel):
        name: str

    data = ModelV1(name="test")
    expect(
        lambda: jsonable_encoder(data),
        "encoding a pydantic v1 model",
    ).to_raise(PydanticV1NotSupportedError)


@test("jsonable_encoder honours model_config use_enum_values")
def encode_model_with_config():
    model = ModelWithConfig(role=RoleEnum.admin)
    expect(jsonable_encoder(model), "encoded model").to_equal({"role": "admin"})


@test("Constructing a model by field name when an alias is required raises")
def encode_model_with_alias_raises():
    expect(
        lambda: ModelWithAlias(foo="Bar"),
        "constructing model with field name instead of alias",
    ).to_raise(ValidationError)


@test("jsonable_encoder uses the alias name in the encoded output")
def encode_model_with_alias():
    model = ModelWithAlias(Foo="Bar")
    expect(jsonable_encoder(model), "encoded model").to_equal({"Foo": "Bar"})


@test("jsonable_encoder honours exclude_unset/exclude_defaults/include/exclude")
def encode_model_with_default():
    model = ModelWithDefault(foo="foo", bar="bar")
    expect(jsonable_encoder(model), "encoded model").to_equal(
        {"foo": "foo", "bar": "bar", "bla": "bla"}
    )
    expect(
        jsonable_encoder(model, exclude_unset=True), "exclude_unset"
    ).to_equal({"foo": "foo", "bar": "bar"})
    expect(
        jsonable_encoder(model, exclude_defaults=True), "exclude_defaults"
    ).to_equal({"foo": "foo"})
    expect(
        jsonable_encoder(model, exclude_unset=True, exclude_defaults=True),
        "exclude_unset+exclude_defaults",
    ).to_equal({"foo": "foo"})
    expect(jsonable_encoder(model, include={"foo"}), "include={foo}").to_equal(
        {"foo": "foo"}
    )
    expect(jsonable_encoder(model, exclude={"bla"}), "exclude={bla}").to_equal(
        {"foo": "foo", "bar": "bar"}
    )
    expect(jsonable_encoder(model, include={}), "include={}").to_equal({})
    expect(jsonable_encoder(model, exclude={}), "exclude={}").to_equal(
        {
            "foo": "foo",
            "bar": "bar",
            "bla": "bla",
        }
    )


@test("custom_encoder maps a type to a custom encoder function")
def custom_encoders():
    class safe_datetime(datetime):
        pass

    class MyDict(TypedDict):
        dt_field: safe_datetime

    instance = MyDict(dt_field=safe_datetime.now())

    encoded_instance = jsonable_encoder(
        instance, custom_encoder={safe_datetime: lambda o: o.strftime("%H:%M:%S")}
    )
    expect(
        encoded_instance["dt_field"], "encoded dt_field via subclass encoder"
    ).to_equal(instance["dt_field"].strftime("%H:%M:%S"))

    encoded_instance = jsonable_encoder(
        instance, custom_encoder={datetime: lambda o: o.strftime("%H:%M:%S")}
    )
    expect(
        encoded_instance["dt_field"], "encoded dt_field via base-class encoder"
    ).to_equal(instance["dt_field"].strftime("%H:%M:%S"))

    encoded_instance2 = jsonable_encoder(instance)
    expect(
        encoded_instance2["dt_field"], "encoded dt_field with default encoder"
    ).to_equal(instance["dt_field"].isoformat())


@test("custom_encoder applies to enum values")
def custom_enum_encoders():
    def custom_enum_encoder(v: Enum):
        return v.value.lower()

    class MyEnum(Enum):
        ENUM_VAL_1 = "ENUM_VAL_1"

    instance = MyEnum.ENUM_VAL_1

    encoded_instance = jsonable_encoder(
        instance, custom_encoder={MyEnum: custom_enum_encoder}
    )
    expect(encoded_instance, "encoded enum").to_equal(custom_enum_encoder(instance))


@test("jsonable_encoder serializes PurePath fields as strings")
def encode_model_with_pure_path():
    class ModelWithPath(BaseModel):
        path: PurePath

        model_config = {"arbitrary_types_allowed": True}

    test_path = PurePath("/foo", "bar")
    obj = ModelWithPath(path=test_path)
    expect(jsonable_encoder(obj), "encoded model").to_equal({"path": str(test_path)})


@test("jsonable_encoder serializes PurePosixPath fields with posix separators")
def encode_model_with_pure_posix_path():
    class ModelWithPath(BaseModel):
        path: PurePosixPath

        model_config = {"arbitrary_types_allowed": True}

    obj = ModelWithPath(path=PurePosixPath("/foo", "bar"))
    expect(jsonable_encoder(obj), "encoded model").to_equal({"path": "/foo/bar"})


@test("jsonable_encoder serializes PureWindowsPath fields with windows separators")
def encode_model_with_pure_windows_path():
    class ModelWithPath(BaseModel):
        path: PureWindowsPath

        model_config = {"arbitrary_types_allowed": True}

    obj = ModelWithPath(path=PureWindowsPath("/foo", "bar"))
    expect(jsonable_encoder(obj), "encoded model").to_equal({"path": "\\foo\\bar"})


@test("jsonable_encoder serializes a bare PurePath value")
def encode_pure_path():
    test_path = PurePath("/foo", "bar")

    expect(
        jsonable_encoder({"path": test_path}), "encoded path dict"
    ).to_equal({"path": str(test_path)})


@test("jsonable_encoder converts Decimal floats to JSON floats")
def decimal_encoder_float():
    data = {"value": Decimal(1.23)}
    expect(jsonable_encoder(data), "encoded dict").to_equal({"value": 1.23})


@test("jsonable_encoder converts Decimal ints to JSON ints")
def decimal_encoder_int():
    data = {"value": Decimal(2)}
    expect(jsonable_encoder(data), "encoded dict").to_equal({"value": 2})


@test("jsonable_encoder preserves Decimal NaN as a float NaN")
def decimal_encoder_nan():
    data = {"value": Decimal("NaN")}
    expect(
        isnan(jsonable_encoder(data)["value"]), "encoded value is nan"
    ).to_be_truthy()


@test("jsonable_encoder preserves Decimal infinity as a float infinity")
def decimal_encoder_infinity():
    data = {"value": Decimal("Infinity")}
    expect(
        isinf(jsonable_encoder(data)["value"]), "encoded +inf is inf"
    ).to_be_truthy()
    data = {"value": Decimal("-Infinity")}
    expect(
        isinf(jsonable_encoder(data)["value"]), "encoded -inf is inf"
    ).to_be_truthy()


@test("jsonable_encoder recurses into deque elements")
def encode_deque_encodes_child_models():
    class Model(BaseModel):
        test: str

    dq = deque([Model(test="test")])

    expect(jsonable_encoder(dq)[0]["test"], "encoded child model field").to_equal(
        "test"
    )


@test("jsonable_encoder maps PydanticUndefined to None")
def encode_pydantic_undefined():
    data = {"value": Undefined}
    expect(jsonable_encoder(data), "encoded dict").to_equal({"value": None})


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
        expect(jsonable_encoder(data), "encoded color").to_equal({"color": "blue"})
