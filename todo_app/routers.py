from fastapi import APIRouter, Depends, HTTPException,Form,Query
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from .database import session_local
from . import crud,auth
from .schema import TodoModel,CreateUser,CreateTodo,FilterModel
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi_filter import FilterDepends
from typing import Annotated
from .auth import get_current_user,decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter(prefix="/auth", tags=['user'])

todo_router = APIRouter(prefix="/todo", tags=['Todo'])

# Todo app auths


def get_db():
    db = session_local()
    try:
        yield db
    except Exception as e:
        db.close()
        print(e)

        raise e

# Todo items


@todo_router.get("/all")
async def todo_get_all(db:Annotated[Session,Depends(get_db)] ,user: Annotated[str, Depends(get_current_user)]):
   
    try:
        data = crud.read_items(db,user)
   
        return {"Todo Items": jsonable_encoder(data)}
    # print(data)
    except Exception as e:
        print(e)
        return HTTPException(status_code=400, detail={"message": "internal server error"})


@todo_router.get("/item/{todo_id}")
async def todo_get_item(db:Annotated[Session,Depends(get_db)],todo_id: int,user: Annotated[str, Depends(get_current_user)]):
    try:
        data = crud.read_a_item(db,todo_id,user)
        return {"Todo Item": jsonable_encoder(data)}
    except Exception as e: 
        print(e)
        return HTTPException(status_code=400, detail={"message": "internal server error"})



@todo_router.post("/add")
async def todo_create_item(todo: TodoModel, db: Annotated[Session, Depends(get_db)],user: Annotated[str, Depends(get_current_user)]):
    try:
        data = crud.create_item(todo, db,user)
        return {"Todo Items": jsonable_encoder(data)}
    
    except Exception as e:
        print(e)
        return HTTPException(status_code=400, detail={"message": "internal server error"})

@todo_router.post("/search")
async def todo_item_search(db:Annotated[Session,Depends(get_db)],user: Annotated[str, Depends(get_current_user)],filter:Annotated[FilterModel,Depends(FilterModel)]):
    
    return jsonable_encoder(crud.search_item(db,user,filter))


@todo_router.delete("/delete/{todo_id}")
async def todo_delete_item(db: Annotated[Session, Depends(get_db)], todo_id: int,user: Annotated[str, Depends(get_current_user)]):
    try:
        data = crud.delete_item(db, todo_id,user)
        print(jsonable_encoder(data))
        return {"Entery Deleted": jsonable_encoder(data)}
    
    except Exception as e:
        print(e)
        return HTTPException(status_code=400, detail={"message": "internal server error"})


@todo_router.put("/update/{todo_id}")
async def todo_update_item(db: Annotated[Session, Depends(get_db)],item:TodoModel, todo_id: int,user: Annotated[str, Depends(get_current_user)]):
    try:
        data = crud.update_item(item,db,todo_id,user)
        print(jsonable_encoder(data))
        return {"Entery Deleted": jsonable_encoder(data)}
    except Exception as e:
        print(e)
        return HTTPException(status_code=400, detail={"message": "internal server error"})




@auth_router.get("/me")
async def user_me(db: Annotated[Session, Depends(get_db)],token: Annotated[str, Depends(get_current_user)]):
    return jsonable_encoder(auth.get_user(db,token))


@auth_router.post("/login")
async def user_login(db: Annotated[Session, Depends(get_db)],login_details: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # try:
    return auth.login_user(db, login_details)
   

@auth_router.post("/register")
async def user_register(db:Annotated[Session,Depends(get_db)],registerForm:CreateUser):
    try:
        message = auth.register_user(db,registerForm)
        print(message)
    except Exception as e:
        print(e)

    return {"message": message}


@auth_router.put("/update")
async def user_update(db:Annotated[Session,Depends(get_db)],update_details:Annotated[CreateUser,None],user: Annotated[str, Depends(get_current_user)]):
    try:
    
        return auth.update_user(db,update_details,user)
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail={"Message":"Internal server error"})
    
# delete user from db

@auth_router.delete("/delete")
async def user_delete(db:Annotated[Session,Depends(get_db)],confirm:Annotated[str,Form()],user_id:Annotated[str,Depends(get_current_user)]):
    return auth.delete_user(db,confirm,user_id)

