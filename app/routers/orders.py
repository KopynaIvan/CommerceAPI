from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.crud import get_session
from app.schemas import OrderCreate,  OrderRead, OrderStatusUpdate
from app.services.orders import service_create_order, service_update_order_status
from app.auth import get_current_user
from app.models import OrderStatus, User, Order
from app.services.stripe import service_create_payment_intent

router = APIRouter()

@router.post("/orders", response_model= OrderRead)
def create_order(items: OrderCreate, curr_user: User = Depends(get_current_user) , session: Session = Depends(get_session)):
    return service_create_order(items=items.items, user_id=curr_user.id or 0, session=session)

@router.patch("/orders/{order_id}/status", response_model= OrderRead)
def update_order_status(order_id: int, new_status: OrderStatusUpdate, session: Session = Depends(get_session)):
    return service_update_order_status(order_id=order_id, new_status=new_status.status,session=session)

@router.post("/orders/{order_id}/pay")
def create_payment_intent(order_id: int, curr_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    
    if not order:
        raise HTTPException(status_code=404, detail="such order does not exist")
    
    if not order.user_id == curr_user.id:
        raise HTTPException(status_code=403, detail="User is not eligible to proceed with this order")
    
    if order.status != OrderStatus.pending:
        raise HTTPException(status_code=400, detail="You can not pay for this order")

    assert order.id is not None

    return service_create_payment_intent(amount=order.total_price,order_id=order.id )
    

