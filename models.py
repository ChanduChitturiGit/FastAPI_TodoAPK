from sqlalchemy import Boolean, Column, Integer, String
from database import Base
from sqlalchemy.sql.schema import ForeignKey


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username=Column(String,unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    
class Todos(Base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String)
    description = Column(String)
    priority = Column(String)
    complete = Column(Boolean, default=False)
    owner = Column(Integer, ForeignKey("users.id"))
