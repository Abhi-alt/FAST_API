from fastapi import FastAPI, Depends, status, HTTPException, Response
from . import  schemas, model
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select

app = FastAPI()

model.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    user = model.User(name=user.name, city=user.city)
    db.add(user)
    db.commit()
    db.refresh(user)

@app.get("/all-persons", status_code=status.HTTP_200_OK)
def get_all_persons(db: Session=Depends(get_db)):
    persons = select(model.User)
    return db.scalars(persons).all()

@app.get("/user-by-id/{id}", status_code=status.HTTP_200_OK)
def get_user(id, response: Response ,db: Session = Depends(get_db)):
    user = select(model.User).where(model.User.id == id)
    resp = db.scalars(user).first()
    if not resp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"User with id {id} is not found"}
    return resp