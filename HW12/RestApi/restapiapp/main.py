from fastapi import FastAPI
from restapiapp.database import Base, engine
from restapiapp.routers import auth, contact
import logging

# Налаштування логування
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Створення FastAPI додатку
app = FastAPI(debug=True)

# Створення всіх таблиць у базі даних, якщо вони ще не існують
Base.metadata.create_all(bind=engine)

# Підключення маршрутизаторів
app.include_router(auth.router)
app.include_router(contact.router)

# Запис логів на старт
logger.info("FastAPI app started and routers are included")
