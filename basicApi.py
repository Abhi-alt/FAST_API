from fastapi import FastAPI, Path

app = FastAPI();
person = {
    1: {
        "name": "Abhishek Kumar",
        "age": 27,
        "role": "UI Developer"
    }
}
@app.get("/")
def get_Name():
    return {"name": "Abhishek", "age": 27}

@app.get("/get-person/{person_id}")
def get_person(person_id: int = Path(description="ID of the person you want to view", gt=0, lt=5)):
    return person[person_id]