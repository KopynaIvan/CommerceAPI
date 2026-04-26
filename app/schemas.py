from datetime import datetime
from sqlmodel import SQLModel

class UserCreate(SQLModel):
    email: str
    password:str

class UserRead(SQLModel):
    id: int
    email: str

class CategoryCreate(SQLModel):
    name: str

class CategoryRead(SQLModel):
    id: int
    name: str

class ProductCreate(SQLModel):
    name: str
    description:str
    price: float
    quantity: int
    category_id: int

class ProductRead(SQLModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

class OrderItemCreate(SQLModel):
    product_id: int
    quantity: int

class OrderItemRead(SQLModel):
    id: int
    product_id: int
    quantity: int
    curr_price: float

class OrderCreate(SQLModel):
    items: list[OrderItemCreate]

class OrderRead(SQLModel):
    id: int
    total_price: float
    status: str
    creation_time: datetime
    # items: list[OrderItemRead]
