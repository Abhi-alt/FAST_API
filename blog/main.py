from fastapi import FastAPI, Depends, status, HTTPException, Response
from . import  schemas, model
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import select, update

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

@app.delete("/delete-user/{id}", status_code=status.HTTP_200_OK)
def delete_user(id: int, db: Session=Depends(get_db)):
    user = db.get(model.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} is not found in the database")
    db.delete(user)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"User with id {id} is deleted successfully from database")

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

@app.put('/update-user/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, resp: schemas.User, db: Session=Depends(get_db)):
    user = db.get(model.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such user exists with id {id}")
    stmt = update(model.User).where(model.User.id == id).values({"city" : resp.city, "name": resp.name}) #can be improved. Try hitting db once only
    db.execute(stmt)
    db.commit()
    return {"message": "User Detail Updated"}