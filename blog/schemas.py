from pydantic import BaseModel

class Blog(BaseModel):
    id: int
    title: str
    body: str

class BlogModel(Blog):
    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    city: str
    password: str
    blogs: list[BlogModel] = []

class GetUser(BaseModel):
    name: str
    city: str
    class Config():
        orm_mode = True

class GetBlog(Blog):
    creator: GetUser
    class Config():
        orm_mode = True
