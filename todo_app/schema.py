from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr


class TodoModel(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime
    status: bool | None = True


class User(BaseModel):
    username: str

class CreateUser(User):
    email: EmailStr
    password: str

class UserLogin(User):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TOkenData(BaseModel):
    username : str

