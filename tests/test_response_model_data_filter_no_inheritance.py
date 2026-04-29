from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from tryke import expect, test

app = FastAPI()


class UserCreate(BaseModel):
    email: str
    password: str


class UserDB(BaseModel):
    email: str
    hashed_password: str


class User(BaseModel):
    email: str


class PetDB(BaseModel):
    name: str
    owner: UserDB


class PetOut(BaseModel):
    name: str
    owner: User


@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    return user


@app.get("/pets/{pet_id}", response_model=PetOut)
async def read_pet(pet_id: int):
    user = UserDB(
        email="johndoe@example.com",
        hashed_password="secrethashed",
    )
    pet = PetDB(name="Nibbler", owner=user)
    return pet


@app.get("/pets/", response_model=list[PetOut])
async def read_pets():
    user = UserDB(
        email="johndoe@example.com",
        hashed_password="secrethashed",
    )
    pet1 = PetDB(name="Nibbler", owner=user)
    pet2 = PetDB(name="Zoidberg", owner=user)
    return [pet1, pet2]


client = TestClient(app)


@test("response_model filters fields without inheritance")
def filter_top_level_model():
    response = client.post(
        "/users", json={"email": "johndoe@example.com", "password": "secret"}
    )
    expect(response.json(), "response body").to_equal({"email": "johndoe@example.com"})


@test("response_model filters nested model fields")
def filter_second_level_model():
    response = client.get("/pets/1")
    expect(response.json(), "response body").to_equal(
        {
            "name": "Nibbler",
            "owner": {"email": "johndoe@example.com"},
        }
    )


@test("list response_model filters each item's nested fields")
def list_of_models():
    response = client.get("/pets/")
    expect(response.json(), "response body").to_equal(
        [
            {"name": "Nibbler", "owner": {"email": "johndoe@example.com"}},
            {"name": "Zoidberg", "owner": {"email": "johndoe@example.com"}},
        ]
    )
