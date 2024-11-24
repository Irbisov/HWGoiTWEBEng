from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi_limiter import FastAPILimiter
from starlette.requests import Request
from starlette.responses import JSONResponse
from restapiapp.database import Base, engine, SessionLocal
from restapiapp.routers import auth, contact
import logging
import os
import redis.asyncio as aioredis
from sqlalchemy import text
from time import sleep
import sys


# Налаштування логування
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG", "False").lower() in ("true", "1", "yes") else logging.INFO)
logger = logging.getLogger(__name__)

# Функція для перевірки з'єднання з PostgreSQL
def check_postgres_connection():
    retries = 5
    while retries > 0:
        try:
            # Використовуємо SQLAlchemy для перевірки з'єднання
            with SessionLocal() as session:
                session.execute(text("SELECT 1"))
            logger.info("PostgreSQL is up!")
            break
        except Exception as e:
            logger.error(f"PostgreSQL connection error: {e}")
            sleep(5)
            retries -= 1
            if retries == 0:
                logger.error("Failed to connect to PostgreSQL after several attempts.")
                sys.exit(1)

# Викликаємо перевірку при запуску
check_postgres_connection()

# Створення FastAPI додатку
app = FastAPI(debug=os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"))

# Middleware для підтримки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Створення таблиць у базі даних
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error on {request.url}: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.on_event("startup")
async def startup_event():
    # Ініціалізація Redis
    try:
        redis = await aioredis.from_url("redis://redis:6379", encoding="utf-8", decode_responses=True)
        await redis.ping()
        app.state.redis = redis
        logger.info("Redis cache initialized.")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")

    # Ініціалізація FastAPILimiter
    try:
        await FastAPILimiter.init(app.state.redis)
        logger.info("FastAPILimiter initialized.")
    except Exception as e:
        logger.error(f"FastAPILimiter initialization failed: {e}")

    # Перевірка з'єднання з PostgreSQL
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        logger.info("Database connection established.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")


@app.get("/health")
async def health_check():
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        if app.state.redis:
            await app.state.redis.ping()
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "error", "details": str(e)}


# Додавання роутерів
app.include_router(auth.router, tags=["Auth"])
app.include_router(contact.router, tags=["Contacts"])

logger.info("FastAPI app initialized and routers are included.")
