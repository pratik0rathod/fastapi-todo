from .database import Base

from sqlalchemy import Column,String,Integer,Boolean,DateTime
from sqlalchemy.orm import Relationship
# from pydantic import ConfigDict

class TodoItemOrm(Base):
    
    #new Updated orm_mode is depricated
    # model_config = ConfigDict(from_attributes=True)

    __tablename__="Todo"

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    title = Column("title",String,nullable=False)
    description = Column(String)
    status = Column(Boolean,nullable=False)
    due_date =  Column(DateTime)
    # owner = Relationship("User", back_populates = "Todo")
    class Config:
        orm_mode = True


class UserOrm(Base):

    #new Updated orm_mode is depricated
    
    __tablename__  = "User"
    id = Column(Integer,primary_key=True,autoincrement=True)    
    username = Column(String,unique=True,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)

    class Config:
        orm_mode = True