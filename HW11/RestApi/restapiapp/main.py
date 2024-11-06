from fastapi import FastAPI
from restapiapp.routers import contacts
from .database import engine
from .models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
