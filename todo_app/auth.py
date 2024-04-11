from passlib.context import CryptContext
from .models import UserOrm
from .schema import CreateUser,UserLogin,Token
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from jose import JWTError,jwt

from fastapi import HTTPException,status,Depends
from typing import Annotated

from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

SECRET_KEY = "my-secret-c22014d6a3aae2712f8f182bcaef3d1b843026e992e6adacb54709a7e91b3125"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(expires_delta)
   
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def decode_token(token):
    
    decoded = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    
    return decoded

     
def get_current_user(token:Annotated[str,Depends(oauth2_scheme)]):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
    
        data = decode_token(token) 
        return data["user"]
    
    except JWTError:
        raise credentials_exception
    

# Work with Routes 

def register_user(db:Session,user:CreateUser):
    user_model = UserOrm(username =user.username,email=user.email,password= hash_password(user.password))
   
    if db.query(UserOrm).filter(UserOrm.username == user_model.username).first() is not None:
        return {"error":"User with that username already exist"}
    
    if db.query(UserOrm).filter(UserOrm.email == user_model.email).first() is not None:
        return {"error":"User with that email already exist"}
    
    db.add(user_model)
    db.commit()

    return  {"Success":"User registered succesfully"}


def get_user(db:Session,user:int):
    print(user)
    user = db.query(UserOrm).filter(UserOrm.id==user).first()
    return user

def login_user(db:Session,user_login_details:UserLogin):
    user = db.query(UserOrm).filter(UserOrm.username == user_login_details.username).first()

    if user is not None:
    
        if verify_password(user_login_details.password,user.password):
            #User verified now we need to create access token
            
            token = create_access_token({"user":user.id},ACCESS_TOKEN_EXPIRE_MINUTES)

            return Token(access_token=token,token_type='Bearer')
    
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


def update_user(db:Session,user_details:CreateUser,user_id:id):
    
    user = db.query(UserOrm).filter(UserOrm.id == user_id).first()
    
    check_username = db.query(UserOrm).filter(UserOrm.username ==  user_details.username).first()
    check_email = db.query(UserOrm).filter(UserOrm.email ==  user_details.email).first()
    
    #checking if username/email avaiable or not and checking is he even trying to update it 
    if check_username is not None:
        if check_username.username != user.username:
            return {"Error":"Username is taken please use diffent usename"}
    
    if check_email is not None:
        if check_email.email != user.email:
            return {"Error":"Email is taken please use diffent Email"}
        

    # if db.query(UserOrm).filter(UserOrm.email ==  user_details.email).first() is not None:
    #     return {"Error":"Email is taken please use diffrent email"}


    user.email = user_details.email
    user.password = hash_password(user_details.password) 
    user.username = user_details.username

    db.add(user)
    db.commit()
    
    # print(jsonable_encoder(user))
    return {"Succes":"succesfully updated"}
