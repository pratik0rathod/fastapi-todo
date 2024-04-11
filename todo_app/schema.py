from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr
from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from .models import TodoItemOrm
from datetime import datetime


class FilterModel(Filter):
    title__like:Optional[str] = None
    description__like:Optional[str] = None
    status:Optional[bool]=None
    
    class Constants(Filter.Constants):
        model = TodoItemOrm
        search_field_name = "search"
        search_model_fields = ['title','description']


class TodoModel(BaseModel):
    title: str
    description: str | None = None
    due_date: datetime
    status: bool | None = True

class CreateTodo(TodoModel):
    user_id:int

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
