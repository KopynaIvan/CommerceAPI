from sqlmodel import Session, select
from app.models import Category
from fastapi import HTTPException

def service_create_category(name: str, session: Session):
    existing = session.exec(select(Category).where(name == Category.name)).first()

    if existing:
        raise HTTPException(status_code=409, detail="Such category already exists")

    category = Category(name=name)

    session.add(category)
    session.commit()
    session.refresh(category)
    
    return category

def service_list_categories(session: Session):
    return session.exec(select(Category)).all()

