from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from restapiapp.config import settings
from restapiapp.models.user import User
from restapiapp.utils.hashing import verify_password  # Імпорт функції для перевірки пароля
import cloudinary
import cloudinary.uploader
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
import os


# Генерація токену
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# Перевірка пароля і аутентифікація
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):  # Заміна на виклик безпосередньо
        return False
    return user


# Створення refresh токена
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# Валідація токена
def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise JWTError
        return user_id
    except JWTError:
        return None


def create_verification_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


# Налаштування для FastMail
def get_fastmail_config():
    # Перевірка на правильність шляху до директорії шаблонів
    template_folder = Path(os.getenv("TEMPLATE_FOLDER", "/app/restapiapp/templates"))

    if not template_folder.is_dir():
        raise FileNotFoundError(f"TEMPLATE_FOLDER {template_folder} не існує або це не директорія.")

    return ConnectionConfig(
        MAIL_USERNAME=settings.FASTMAIL_USER,
        MAIL_PASSWORD=settings.FASTMAIL_PASSWORD,
        MAIL_FROM=settings.FASTMAIL_FROM,
        MAIL_PORT=settings.FASTMAIL_PORT,
        MAIL_SERVER=settings.FASTMAIL_SERVER,
        MAIL_STARTTLS=settings.FASTMAIL_STARTTLS,
        MAIL_SSL_TLS=settings.FASTMAIL_SSL_TLS,
        TEMPLATE_FOLDER=str(template_folder),  # Перетворюємо на рядок
    )


# Генерація та відправка листа
async def send_verification_email(email: str, token: str):
    fm = FastMail(get_fastmail_config())  # Використовуємо налаштування з ConnectionConfig

    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[email],  # список отримувачів
        body=f"Click here to verify: {settings.DATABASE_URL}/auth/verify/{token}",
        subtype="html"
    )

    try:
        await fm.send_message(message)
    except Exception as e:
        print(f"Error sending verification email: {e}")
        # Додаткова обробка помилок або логування


def upload_avatar(file):
    response = cloudinary.uploader.upload(file, folder="avatars")
    return response["secure_url"]


def create_reset_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, "your_secret_key", algorithm="HS256")
