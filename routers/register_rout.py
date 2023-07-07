from fastapi import APIRouter, Depends, HTTPException 
from database import SessionLocal
from models import User,Todos
from typing import Annotated
from sqlalchemy.orm import Session
from schemas import User as user
from starlette import status
from passlib.context import CryptContext
from .log import get_current_user


router=APIRouter(
    prefix='/register',
    tags=['register']
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


@router.post('/register', status_code=status.HTTP_204_NO_CONTENT)
def register(db : db_dependency,data:user):
    user_data = User(
        email = data.email,
        username = data.username,
        # role = "user",
        hashed_password = bcrypt_context.hash(data.password)
    )
    
    db.add(user_data)
    db.commit()