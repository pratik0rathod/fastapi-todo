from passlib.context import CryptContext
from .models import UserOrm
from .schema import CreateUser
from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder


pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


def register_user(db:Session,user:CreateUser):

    user_model = UserOrm(username =user.username,email=user.email,password= hash_password(user.password))
   
    if db.query(UserOrm).filter(UserOrm.username == user_model.username).first() is not None:
        return {"error":"User with that username already exist"}
    
    if db.query(UserOrm).filter(UserOrm.email == user_model.email).first() is not None:
        return {"error":"User with that email already exist"}
    
    db.add(user_model)
    db.commit()

    return  {"Success":"User registered succesfully"}


def login_user(db:Session,user:CreateUser):
    pass 