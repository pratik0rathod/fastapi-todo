from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "postgresql://postgres:pratik@localhost/fastapi_todo_db"

engine = create_engine(DB_URL)

session_local = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()



