from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Завантаження змінних середовища з .env файлу
load_dotenv()


class Settings(BaseSettings):
    # JWT налаштування
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Налаштування бази даних
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    # Налаштування дебагу
    DEBUG: bool = False

    # Налаштування Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    # Налаштування SMTP
    SMTP_SERVER: str
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str

    # Налаштування для FastMail
    FASTMAIL_USER: str
    FASTMAIL_PASSWORD: str
    FASTMAIL_FROM: str
    FASTMAIL_SERVER: str
    FASTMAIL_PORT: int = 587
    FASTMAIL_TLS: bool = True
    FASTMAIL_SSL: bool = False
    FASTMAIL_TEMPLATE_FOLDER: str = "templates"  # Шлях до шаблонів для FastMail
    FASTMAIL_STARTTLS: bool = os.getenv("FASTMAIL_STARTTLS", "False").lower() in ("true", "1", "yes")
    FASTMAIL_SSL_TLS: bool = os.getenv("FASTMAIL_SSL_TLS", "False").lower() in ("true", "1", "yes")
    # URL фронтенду
    FRONTEND_URL: str

    # Налаштування для Cloudinary
    CLOUD_API_KEY: str
    CLOUD_NAME: str
    CLOUD_API_SECRET: str

    class Config:
        # Вказуємо на шлях до .env файлу
        env_file = ".env"


# Ініціалізація налаштувань
settings = Settings()
