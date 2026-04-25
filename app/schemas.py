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
