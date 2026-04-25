from fastapi import FastAPI
from app.routers import auth, users, categories

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
