from fastapi import  HTTPException
from sqlmodel import Session, select
from app.models import User
from app.auth import hash_password 

def service_register(email: str, password: str, session: Session):
    check_existence = session.exec(select(User).where(email == User.email)).first()
    if check_existence:
        raise HTTPException(status_code=409, detail="User already registered")
    if len(password) < 6:
        raise HTTPException(status_code=401, detail="Password is too short")

    user = User(email=email, password=hash_password(password))

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def service_list_users(session: Session):
    users = session.exec(select(User)).all()
    return users
