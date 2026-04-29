from typing import Any

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict
from tryke import expect, test


@test("response_model serializes ORM-mode model attributes")
def read_with_orm_mode() -> None:
    class PersonBase(BaseModel):
        name: str
        lastname: str

    class Person(PersonBase):
        @property
        def full_name(self) -> str:
            return f"{self.name} {self.lastname}"

        model_config = ConfigDict(from_attributes=True)

    class PersonCreate(PersonBase):
        pass

    class PersonRead(PersonBase):
        full_name: str

        model_config = {"from_attributes": True}

    app = FastAPI()

    @app.post("/people/", response_model=PersonRead)
    def create_person(person: PersonCreate) -> Any:
        db_person = Person.model_validate(person)
        return db_person

    client = TestClient(app)

    person_data = {"name": "Dive", "lastname": "Wilson"}
    response = client.post("/people/", json=person_data)
    data = response.json()
    expect(response.status_code, "status code").to_equal(200).fatal()
    expect(data["name"], "name field").to_equal(person_data["name"])
    expect(data["lastname"], "lastname field").to_equal(person_data["lastname"])
    expect(data["full_name"], "full_name property").to_equal(
        person_data["name"] + " " + person_data["lastname"]
    )
