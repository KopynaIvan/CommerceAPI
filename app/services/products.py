from fastapi import HTTPException
from sqlmodel import Session, select
from app.models import Category, Product
from app.cache import get_cached, invalidate_cache, set_cached

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
    
    invalidate_cache("products")

    return product

def service_list_products(session: Session):
    product = get_cached("product")

    if product:
        return product

    products = session.exec(select(Product)).all()
    set_cached("product",[p.model_dump() for p in products])

    return products

def service_get_product(product_id: int, session: Session):
    product = session.get(Product,product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Such product doesn't exist")

    return product
