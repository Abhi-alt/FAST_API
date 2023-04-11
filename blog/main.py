from fastapi import FastAPI
from . import   model
from .database import engine
from .routers import blog, users

app = FastAPI()

model.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(users.router)
