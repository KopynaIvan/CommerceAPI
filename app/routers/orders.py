from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.crud import get_session
from app.schemas import OrderCreate, OrderItemCreate, OrderRead, OrderItemRead
from app.services.orders import service_create_order
from app.auth import get_current_user
from app.models import User

router = APIRouter()

@router.post("/orders", response_model= OrderRead)
def create_order(items: OrderCreate, curr_user: User = Depends(get_current_user) , session: Session = Depends(get_session)):
    return service_create_order(items=items.items, user_id=curr_user.id or 0, session=session)

