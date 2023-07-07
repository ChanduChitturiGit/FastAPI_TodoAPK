from fastapi import APIRouter, Depends, HTTPException 
from database import SessionLocal
from models import User,Todos
from typing import Annotated
from sqlalchemy.orm import Session
from schemas import token_data
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from schemas import Todos as todos_data
from starlette import status
from routers.log import get_current_user
from global_exception_handler.exceptions import authenticationFailedException

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/getAllUsers')
def getAllUsers(user : user_dependency,db : db_dependency):
    if user is None or user.get('role') !='admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed.')
    
    data_li = db.query(User).filter(User.role == 'user').all()
    
    if len(data_li)<1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Users data is not found.')
    
    ele=[]
    for data in data_li:
        result = User(
            id = data.id,
            email = data.email,
            username = data.username,
            )
        ele.append(result)
    return ele
    # return db.query(User).all()


@router.get('/getUserbyId/{id}')
def getUserbyId(ud : user_dependency, db : db_dependency, id : int):
    if ud is None or ud.get('role')!='admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed.")
    data = db.query(User).filter(User.id==id).first()
    if data is not None:
        result = User(
            id = data.id,
            email = data.email,
            username = data.username,
        )
        return result
    raise HTTPException(status_code=404, detail='User does not exists.')


@router.delete('/deleteUser/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(ud : user_dependency,db : db_dependency, id : int):
    if ud is None or ud.get('role')!='admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed.")
    
    user_data = db.query(User).filter(User.id == id).first()
    
    
    if user_data is None:
        raise HTTPException(status_code=404,detail='User Not found.')
    
    db.query(Todos).filter(Todos.owner == id).delete()
    db.query(User).filter(User.id==id).delete()
    db.commit()