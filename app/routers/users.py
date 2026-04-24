from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.auth import get_current_user
from app.crud import get_session
from app.schemas import UserCreate, UserRead
from app.services.users import service_register, service_list_users
from app.models import User

router = APIRouter()

@router.post("/users/me", response_model=UserRead)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    return service_register(**user_data.model_dump(), session=session)

@router.get("/users", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session)):
    return service_list_users(session=session)

@router.get("/users/me", response_model=UserRead)
def show_logged_user(curr_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return curr_user
