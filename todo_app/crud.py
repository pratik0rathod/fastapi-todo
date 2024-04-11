from sqlalchemy.orm  import Session
from fastapi import Depends
from .schema import TodoModel,FilterModel
from .database import Base,engine
from . import models
from sqlalchemy import update,select

#create table in data base
Base.metadata.create_all(engine)

# Todo crude operations 
def create_item(todo_schema:TodoModel,db:Session,user:int):
    
    item =  models.TodoItemOrm(
        title = todo_schema.title, 
        description = todo_schema.description,
        status = todo_schema.status,
        due_date = todo_schema.due_date,
        auther_id = user
        )
    
    db.add(item)
    db.commit()

    return {"Success": "Todo added succesfully"}

def read_items(db:Session,user:int):
    
    return db.query(models.TodoItemOrm).filter(models.TodoItemOrm.auther_id == user).all()


def read_a_item(db:Session,id:int,user:int):
    return db.query(models.TodoItemOrm).filter(models.TodoItemOrm.id == id,models.TodoItemOrm.auther_id == user).first()

def update_item(todo_schema:TodoModel,db:Session,id:int,user:int):
    # update_item = models.TodoItemOrm(title = todo_schema.title , description = todo_schema.description,status = todo_schema.status)    
    
    item = db.query(models.TodoItemOrm).filter(models.TodoItemOrm.id == id,models.TodoItemOrm.auther_id==user).first()
    
    if item:
        item.title = todo_schema.title
        item.description = todo_schema.description
        item.status = todo_schema.status
        db.add(item)
        db.commit()

        # item.update(update_item,synchronize_session=False)
        return  {"Message":"entery NO: "+ str(id) +" Updated successfully"}
    else:
        return {"error":"Item not found"}

def delete_item(db:Session,id:int,user:int):
    # return True
    # return db.query(models.TodoItemOrm).filter(models.TodoItemOrm.id==id).first()
    # item = db.get(models.TodoItemOrm,id)
    item =  db.query(models.TodoItemOrm).filter(models.TodoItemOrm.id==id,models.TodoItemOrm.auther_id == user).first()
    
    if item:
        db.delete(item)
        db.commit()
        return {"Message":"entery NO"+str(id)+" deleted successfully"}
    else:
        return {"error":"Item not found"}


def search_item(db:Session,user:int,filter:FilterModel):
    query = select(models.TodoItemOrm)
    query = filter.filter(query)
    query = query.filter(models.TodoItemOrm.auther_id == user)
    results = db.execute(query)
    
    return results.scalars().all()
