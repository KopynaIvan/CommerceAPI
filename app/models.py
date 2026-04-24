from typing import Optional
from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime, timezone
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str
    orders: list["Order"] = Relationship(back_populates="user")

class Category(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    products: list["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description:str
    price: float
    quantity: int
    category_id: int = Field(foreign_key="category.id")
    category: "Category" = Relationship(back_populates="products")
    orderitems: list["OrderItem"] = Relationship(back_populates="product")

class Order(SQLModel, table=True):
    id: int = Field(primary_key=True)
    total_price: float
    status: OrderStatus 
    creation_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="orders")
    orderitems: list["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    id: int = Field(primary_key=True)
    curr_price: float
    quantity: int
    product_id: int = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="orderitems")
    order_id: int = Field(foreign_key="order.id")
    order: "Order" = Relationship(back_populates="orderitems")

