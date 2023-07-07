from fastapi import APIRouter, Depends, HTTPException 
from database import SessionLocal
from models import Todos,User
from typing import Annotated
from sqlalchemy.orm import Session
from schemas import Todos as todos_data
from starlette import status
from routers.log import get_current_user
from global_exception_handler.exceptions import authenticationFailedException, authentication_exception_handler,dataNotFoundException, dataNotFoundException_handler

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/getAllTodosbyId/{id}')
def getAllTodosbyId(user : user_dependency,db : db_dependency,id : int):
    if user is None:
        raise authenticationFailedException(msg="Authentication Failed.")
    
    data = db.query(Todos).filter(Todos.id == id).filter(Todos.owner == user.get('id')).all()
    
    if len(data)>0:
        return data
    raise dataNotFoundException(msg="Todos data not found.")


@router.get('/getAllTodos')
def getAllTodos(user : user_dependency,db : db_dependency):
    if user is None:
        raise authenticationFailedException(msg="Authentication Failed.")
    
    data = db.query(Todos).filter(Todos.owner == user.get('id')).all()
    
    if len(data)>0:
        return data
    raise dataNotFoundException(msg="Todos data not found.")


@router.post('/addTodo', status_code=status.HTTP_204_NO_CONTENT)
async def addTodo(user : user_dependency, todos : todos_data, db : db_dependency):
    if user is None:
        raise authenticationFailedException(msg="Authentication Failed.")
    data = Todos(**todos.dict(),owner=user.get('id'))    
    db.add(data)
    db.commit()
    


@router.put('/updateTodo/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def updateTodo(user : user_dependency, db : db_dependency, todos : todos_data, id : int):
    if user is None:
        raise authenticationFailedException(msg="Authentication Failed.")
    
    data = db.query(Todos).filter(Todos.owner == user.get('id')).filter(Todos.id == id).first()
    
    
    data.task = todos.task
    data.description = todos.description
    data.priority = todos.priority
    data.complete = todos.complete
    db.add(data)
    db.commit()
    
    
@router.delete('/deleteTodo/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deleteTodo(user : user_dependency, db : db_dependency, id : int):
    if user is None:
        raise authenticationFailedException(msg="Authentication Failed.")
    data = db.query(Todos).filter(Todos.id == id).filter(Todos.owner == user.get('id')).first()
    
    if data is None:
        raise dataNotFoundException(msg="Todos data not found.")
    
    db.query(Todos).filter(Todos.id == id).filter(Todos.owner == user.get('id')).delete()
    db.commit()