from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.crud import get_session
from app.services.auth import service_login

router = APIRouter()

@router.post("/auth/login", response_model=dict)
def login(user_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    return service_login(password=user_data.password,email=user_data.username,session=session)
