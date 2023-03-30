from fastapi import FastAPI, Depends
from . import  schemas, model
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

model.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create-user")
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    user = model.User(name=user.name, city=user.city)
    db.add(user)
    db.commit()
    db.refresh(user)