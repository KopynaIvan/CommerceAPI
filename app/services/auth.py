from fastapi import  HTTPException
from sqlmodel import Session, select
from app.models import User
from app.auth import create_token, verify_password

def service_login(password:str,email:str, session: Session):
    find_user = session.exec(select(User).where(email == User.email)).first()
    if not find_user:
        raise HTTPException(status_code=404, detail="Incorrect password or email")

    pass_verif = verify_password(password, find_user.password)
    
    if not pass_verif:
        raise HTTPException(status_code=404, detail="Incorrect password or email")
    
    token = create_token(find_user.id or 0)

    return {"access_token":token, "token_type": "bearer"}
