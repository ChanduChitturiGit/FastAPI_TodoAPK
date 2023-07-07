from fastapi import APIRouter, Depends, HTTPException 
# import APIRouter, Depends, HTTPException from 'fastapi';
from database import SessionLocal
from models import User
from typing import Annotated
from sqlalchemy.orm import Session
from schemas import token_data
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from global_exception_handler.exceptions import authenticationFailedException, authentication_exception_handler




router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]


SECRET_KEY='BnDqwcaSDPqnb23bOtjZd8Rde'
ALGORITHM='HS256'
 
def access_token(username : str, user_id : int, role : str, expire_date : timedelta):
    encode = {'sub' : username, 'id' : user_id, 'role' : role}
    expire = datetime.utcnow()+expire_date
    
    encode.update({'exp' : expire})
    
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        role : str = payload.get('role')
        
        if username is None or user_id is None or role is None:
            raise authenticationFailedException(msg="Authentication Failed.")
        return {'username' : username, 'id' : user_id, 'role' : role}
    except JWTError:
            raise authenticationFailedException(msg="Authentication Failed.")
    


def authentication(username : str, password : str,db):
    data = db.query(User).filter(username == User.username).first()
    
    if not data:
        return False
    if not bcrypt_context.verify(password,data.hashed_password):
        return False
    return data



    
@router.post('/token', response_model=token_data)
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], db : db_dependency):
    
    data = authentication(form_data.username, form_data.password, db)
    
    if data:
        token = access_token(data.username, data.id, data.role, timedelta(minutes=20))
        
        return {'access_token' : token , 'token_type' : 'bearer'}
    
    raise authenticationFailedException(msg="Authentication Failed.")