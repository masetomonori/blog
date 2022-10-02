from pydantic import BaseModel
from typing import List, Optional

class BlogBase(BaseModel):
    title: str
    body: str

class Blog(BlogBase):
    class Config:
        orm_mode = True

class ShowUser(BaseModel):
    name: str
    email: str

    blogs: List[Blog] = []

    class Config:
        orm_mode = True
        
class ShowBlog(BaseModel):
    title: str
    body: str
    creator : ShowUser

    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class Pxe(BaseModel):
    BootDevice: str
    BootType : str


class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_tocken: str
    token_type: str

class TokenData(BaseModel):
    enaol: Optional[str] = None






