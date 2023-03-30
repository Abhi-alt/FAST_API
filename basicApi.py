from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI();
persons = {
    0: {
        "name": "Abhishek Kumar",
        "age": 27,
        "role": "UI Developer"
    },
    1: {
        "name": "XYZ",
        "age": 34,
        "role": "TSM"
    },
    2: {
        "name": "ZSR",
        "age": 24,
        "role": "Software Developer"
    }
}
@app.get("/")
def get_Name():
    return {"name": "Abhishek", "age": 27}

@app.get("/get-person/{person_id}")
def get_person(person_id: int = Path(description="ID of the person you want to view", gt=0, lt=5)):
    return persons[person_id]

@app.get("/get-person-by-name")
def get_person_by_name(name : str):
    for person_id in persons:
        if persons[person_id]["name"] == name:
            return persons[person_id]
    return {"msg": "Data not found"}

class Persons(BaseModel):
    name: str
    age: int
    role: str
    id: int

@app.post("/add-person")
def add_person(person: Persons):
    for person_id in persons:
        if person_id == person.id:
            return {"msg": "This id details already exists"}
    persons[person.id] = {
        "name": person.name,
        "age": person.age,
        "role": person.role
    }

@app.get("/get-persons")
def get_persons():
    return persons