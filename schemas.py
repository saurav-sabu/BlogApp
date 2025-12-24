from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(Blog):
    pass

class User(BaseModel):
    name: str
    email: str
    password: str