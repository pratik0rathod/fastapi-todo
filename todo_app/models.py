from .database import Base

from sqlalchemy import Column,String,Integer,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship
# from pydantic import ConfigDict


class UserOrm(Base):

    #new Updated orm_mode is depricated
    
    __tablename__  = "User"

    id = Column(Integer,primary_key=True,autoincrement=True)    
    username = Column(String,unique=True,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)

    class Config:
        orm_mode = True


        
class TodoItemOrm(Base):
    
    #new Updated orm_mode is depricated
    # model_config = ConfigDict(from_attributes=True)

    __tablename__="Todo"

    id = Column("id",Integer,primary_key=True,autoincrement=True)
    title = Column("title",String,nullable=False)
    description = Column(String)
    status = Column(Boolean,nullable=False)
    due_date =  Column(DateTime)
    auther_id = Column(Integer,ForeignKey("User.id"))
    owner = relationship(UserOrm, backref="parent")

    class Config:
        orm_mode = True
