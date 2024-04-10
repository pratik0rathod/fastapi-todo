from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr

class TodoModel(BaseModel):
    title :str
    description :str|None= None
    due_date:datetime
    status: bool | None = True

class User(BaseModel):
    username:str
    email:EmailStr

class CreateUser(User):
    password:str
    