from .database import Base

from sqlalchemy import Column,String,Integer,Boolean,DateTime
# from pydantic import ConfigDict

class TodoItemOrm(Base):
    
    #new Updated orm_mode is depricated
    # model_config = ConfigDict(from_attributes=True)

    __tablename__="Todo"

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    title = Column("title",String)
    description = Column(String)
    status = Column(Boolean)
    due_date =  Column(DateTime)

    class Config:
        orm_mode = True


class UserOrm(Base):

    #new Updated orm_mode is depricated
    
    __tablename__  = "User"
    user_id = Column("id",Integer,unique=True,autoincrement=True)    
    username = Column(String,primary_key=True)
    email = Column(String,unique=True)
    password = Column(String)

    class Config:
        orm_mode = True

