from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.crud import get_session
from app.schemas import CategoryRead, CategoryCreate
from app.services.categories import service_create_category, service_list_categories

router = APIRouter()

@router.post("/categories", response_model=CategoryRead)
def create_category(category_data: CategoryCreate, session: Session = Depends(get_session)):
    return service_create_category(**category_data.model_dump(), session=session)

@router.get("/categories", response_model=list[CategoryRead])
def list_categories(session: Session = Depends(get_session)):
    return service_list_categories(session=session)
