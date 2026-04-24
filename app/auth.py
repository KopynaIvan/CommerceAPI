import bcrypt
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlmodel import Session
from app.crud import get_session
from app.models import User
import os

ALGORITHM = os.environ["ALGORITHM"]
SECRET_KEY = os.environ["SECRET_KEY"]
oauth_scheme = OAuth2PasswordBearer("/auth/login")

def hash_password(password:str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain:str,hashed:str) -> bool:
    return bcrypt.checkpw(plain.encode(),hashed.encode())

def create_token(user_id:int) -> str:
    return jwt.encode({"user_id":user_id},SECRET_KEY, ALGORITHM)
    
def decode_token(token:str) -> int:
    decoded_token = jwt.decode(token,SECRET_KEY, ALGORITHM)
    return decoded_token["user_id"]
def get_current_user(token: str = Depends(oauth_scheme), session: Session = Depends(get_session)):
    try:
        user_id = decode_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid token")
    user = session.get(User,user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
