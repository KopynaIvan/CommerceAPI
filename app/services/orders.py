from sqlmodel import Session
from fastapi import HTTPException

from app.models import OrderStatus, Product, Order, OrderItem

def service_create_order(items: list, user_id: int, session: Session):
    total_price = 0
    products = {}
    for item in items:
        existing_product = session.get(Product, item.product_id)
        
        products[item.product_id] = existing_product

        if not existing_product:
            raise HTTPException(status_code=404, detail="Such product does not exist")
        
        if not existing_product.quantity:
            raise HTTPException(status_code=404, detail="Product is out of stock")

        total_price += existing_product.price * item.quantity
    
    order = Order(total_price=total_price, status=OrderStatus.pending,user_id=user_id)
    session.add(order)
    session.flush()
    assert order.id is not None

    for item in items:
        existing_product = products[item.product_id]

        if not existing_product:
            raise HTTPException(status_code=404, detail="Such product does not exist")
        
        if not existing_product.quantity:
            raise HTTPException(status_code=404, detail="Product is out of stock")

        order_item = OrderItem(curr_price=existing_product.price, quantity=item.quantity, product_id=existing_product.id, order_id=order.id )
        session.add(order_item)

        existing_product.quantity -= item.quantity
        session.add(existing_product)

    session.commit()
    
    return order
