from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from .. import schemas, database, hashing, model

router = APIRouter()
get_db = database.get_db
Hash = hashing.Hash

@router.post("/create-user", status_code=status.HTTP_201_CREATED, tags=["user"])
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    pasword = Hash.password_hash(user.password)
    user = model.User(name=user.name, city=user.city, password=pasword)
    db.add(user)
    db.commit()
    db.refresh(user)

@router.delete("/delete-user/{id}", status_code=status.HTTP_200_OK, tags=["user"])
def delete_user(id: int, db: Session=Depends(get_db)):
    user = db.get(model.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} is not found in the database")
    db.delete(user)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"User with id {id} is deleted successfully from database")

@router.get("/all-persons", status_code=status.HTTP_200_OK, response_model=list[schemas.GetUser], tags=["user"])
def get_all_persons(db: Session=Depends(get_db)):
    persons = select(model.User)
    return db.scalars(persons).all()

@router.get("/user-by-id/{id}", status_code=status.HTTP_200_OK, response_model=schemas.GetUser, tags=["user"])
def get_user(id, response: Response ,db: Session = Depends(get_db)):
    user = select(model.User).where(model.User.id == id)
    resp = db.scalars(user).first()
    if not resp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"User with id {id} is not found"}
    return resp

@router.put('/update-user/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["user"])
def update_user(id: int, resp: schemas.User, db: Session=Depends(get_db)):
    user = db.get(model.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such user exists with id {id}")
    stmt = update(model.User).where(model.User.id == id).values({"city" : resp.city, "name": resp.name}) #can be improved. Try hitting db once only
    db.execute(stmt)
    db.commit()
    return {"message": "User Detail Updated"}
