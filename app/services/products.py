from fastapi import HTTPException
from sqlmodel import Session, select
from app.models import Category, Product

def service_create_product(name: str ,description:str, price: float, quantity: int, category_id: int, session: Session):
    category = session.get(Category, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="There is no such category")

    exists = session.exec(select(Product).where(name==Product.name)).first()  
    
    if exists:
        raise HTTPException(status_code=409, detail="Such product already exists")

    product = Product(name=name, description=description, price=price, quantity=quantity, category_id=category_id)

    session.add(product)
    session.commit()
    session.refresh(product)
    
    return product

def service_list_products(session: Session):
    return session.exec(select(Product)).all()

def service_get_product(product_id: int, session: Session):
    product = session.get(Product,product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Such product doesn't exist")

    return product
