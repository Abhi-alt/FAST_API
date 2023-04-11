from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from .. import schemas, database, model

router = APIRouter()
get_db = database.get_db


@router.post("/create-blog", status_code=status.HTTP_201_CREATED, tags=["blog"])
def create_blog(req: schemas.Blog, db: Session=Depends(get_db)):
    blog = model.Blog(title= req.title, body=req.body, creator_id = req.id)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return {"msg": f"Blog created"}

@router.get("/all-blogs", status_code=status.HTTP_200_OK, response_model=list[schemas.GetBlog], tags=["blog"])
def get_all_blogs(db: Session=Depends(get_db)):
    blogs = select(model.Blog)
    return db.scalars(blogs).all()
