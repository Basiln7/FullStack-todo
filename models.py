from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)

class CreateUser(BaseModel):
    name: str
    password: str

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)
    task_description = Column(String)

class CreateTask(BaseModel):
    task_name: str
    task_description: str