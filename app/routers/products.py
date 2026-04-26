from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.crud import get_session
from app.schemas import ProductCreate, ProductRead
from app.services.products import service_create_product, service_get_product, service_list_products

router = APIRouter()

@router.post("/products", response_model=ProductRead)
def create_product(product_data: ProductCreate, session: Session = Depends(get_session)):
    return service_create_product(**product_data.model_dump(), session=session)

@router.get("/products", response_model=list[ProductRead])
def list_products(session: Session = Depends(get_session)):
    return service_list_products(session=session)

@router.get("/products/{product_id}")
def get_product(product_id: int, session: Session = Depends(get_session)):
    return service_get_product(product_id=product_id, session=session)
