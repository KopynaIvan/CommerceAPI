from fastapi import FastAPI
from app.routers import auth, users, categories, products, orders, webhooks

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(webhooks.router)
