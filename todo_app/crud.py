from sqlalchemy.orm  import Session
from fastapi import Depends
from .schema import TodoModel
from .database import Base,engine
from . import models
from sqlalchemy import update

#create table in data base
Base.metadata.create_all(engine)

# Todo crude operations 
def create_item(todo_schema:TodoModel,db:Session):
    item =  models.TodoItemOrm(title = todo_schema.title , description = todo_schema.description,status = todo_schema.status)
    db.add(item)
    db.commit()
    return item

def read_items(db:Session):
    return db.query(models.TodoItemOrm).all()


def read_a_item(db:Session,id:int):
    return db.query(models.TodoItemOrm).filter(models.TodoItemOrm.id == id).first()

def update_item(todo_schema:TodoModel,db:Session,id:int):
    # update_item = models.TodoItemOrm(title = todo_schema.title , description = todo_schema.description,status = todo_schema.status)    
    
    item = db.query(models.TodoItemOrm).filter(models.TodoItemOrm.id == id).first()
    
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

def delete_item(db:Session,id:int):
    # return True
    # return db.query(models.TodoItemOrm).filter(models.TodoItemOrm.id==id).first()
    
    item = db.get(models.TodoItemOrm,id)
    
    if item:
        db.delete(item)
        db.commit()
        return {"Message":"entery NO"+str(id)+" deleted successfully"}
    else:
        return {"error":"Item not found"}


