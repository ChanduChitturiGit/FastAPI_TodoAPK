from fastapi import APIRouter, Depends, HTTPException 
from database import SessionLocal
from models import User,Todos
from typing import Annotated
from sqlalchemy.orm import Session
from schemas import User as user
from starlette import status
from passlib.context import CryptContext
from .log import get_current_user
from global_exception_handler.exceptions import authenticationFailedException, authentication_exception_handler,dataNotFoundException, dataNotFoundException_handler



router=APIRouter(
    prefix='/user',
    tags=['user']
)

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]


@router.get('/getUserbyId')
def getUserbyId(ud : user_dependency,db:db_dependency):
    if ud is None:
        raise authenticationFailedException(msg="Authentication Failed.")
    data = db.query(User).filter(User.id==ud.get('id')).first()
    if data is not None:
        return data
    raise dataNotFoundException(msg="User data not found.")
    
    
@router.put('/updateUser/{id}', status_code=status.HTTP_204_NO_CONTENT)
def updateUser(ud : user_dependency,db : db_dependency, id : int, data : user):
    if ud is None:
        raise authenticationFailedException(msg="Authentication Failed.")
    
    user_data = db.query(User).filter(User.id == id).first()
    
    if user_data is None:
        raise dataNotFoundException(msg="User data not found.")
    
    user_data.email=data.email
    user_data.hashed_password=data.hashed_password
    # user_data.role="user"
    db.add(user_data)
    db.commit()
    

@router.delete('/deleteUser/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(ud : user_dependency,db : db_dependency, id : int):
    if ud is None:
        raise authenticationFailedException(msg="Authentication Failed.")
    
    user_data = db.query(User).filter(User.id == id).first()
    
    if user_data is None:
        raise dataNotFoundException(msg="User data not found.")
    
    db.query(Todos).filter(Todos.owner == id).delete()
    db.query(User).filter(User.id==id).delete()
    db.commit()
    
