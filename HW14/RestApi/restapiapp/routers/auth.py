from fastapi import APIRouter, HTTPException, Form, File, UploadFile, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from restapiapp.database import get_db
from restapiapp.crud import user as crud
from restapiapp.schemas import user as schemas
from restapiapp.utils import auth, hashing
from restapiapp.dependencies import get_current_user
from restapiapp.config import settings
import json
import cloudinary
import cloudinary.uploader
import re
from datetime import datetime
from logging import getLogger
import jwt
from restapiapp.models.user import User

# Ініціалізація Cloudinary з конфігурацій
cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.CLOUD_API_KEY,
    api_secret=settings.CLOUD_API_SECRET,
)

# Налаштування логування
logger = getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Auth"])

# Залежність для створення сесії БД
get_db()


# 1. Реєстрація нового користувача
@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Реєстрація нового користувача.

    Відправляє токен верифікації на email нового користувача та створює обліковий запис.

    Args:
        user (schemas.UserCreate): Дані користувача для реєстрації.
        db (Session): Сесія бази даних.

    Returns:
        schemas.UserOut: Інформація про створеного користувача.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    token = auth.create_verification_token(user.email)
    await auth.send_verification_email(user.email, token)

    new_user = crud.create_user(db=db, user=user)
    return new_user


# 2. Логін користувача
@router.post("/login", response_model=schemas.Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    """
    Авторизація користувача.

    Перевіряє облікові дані користувача та повертає access і refresh токени.
    """
    user = auth.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Створення токенів
    access_token = auth.create_access_token(data={"sub": user.email})
    refresh_token = auth.create_refresh_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}




# 3. Оновлення токенів за допомогою refresh токена
@router.post("/refresh", response_model=schemas.Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Оновлення токенів за допомогою refresh токена.

    Перевіряє дійсність refresh токена та повертає нові access і refresh токени.

    Args:
        refresh_token (str): Refresh токен для оновлення.
        db (Session): Сесія бази даних.

    Returns:
        dict: Нові access та refresh токени з типом bearer.
    """
    user_email = auth.verify_token(refresh_token)
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user = crud.get_user_by_email(db, email=user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    new_access_token = auth.create_access_token(data={"sub": user.email})
    new_refresh_token = auth.create_refresh_token(data={"sub": user.email})
    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}


# 4. Оновлення аватара
@router.post("/update-avatar")
async def update_avatar(
        user: str = Form(...),  # отримуємо user через форму (JSON-стрічка)
        file: UploadFile = File(...),  # отримуємо файл
        db: Session = Depends(get_db)  # База даних
):
    """
    Оновлення аватара користувача.

    Завантажує файл аватара на Cloudinary та оновлює URL аватара в базі даних.

    Args:
        user (str): JSON-стрічка з даними користувача, що містить 'id' і 'email'.
        file (UploadFile): Завантажений файл аватара.
        db (Session): Сесія бази даних.

    Returns:
        dict: Повідомлення про успішне оновлення аватара та його URL.

    Raises:
        HTTPException: Якщо виникають проблеми з даними користувача, файлом або сервером.
    """
    allowed_extensions = ["jpg", "jpeg", "png"]
    max_file_size = 2 * 1024 * 1024  # Максимальний розмір файлу 2 MB

    try:
        # Перетворення JSON-стрічки на об'єкт Python
        user_data = json.loads(user)

        # Перевірка наявності ключів 'id' і 'email'
        if not all(key in user_data for key in ["id", "email"]):
            raise HTTPException(status_code=400, detail="User data must contain 'id' and 'email' keys")

        # Перевірка розширення файлу
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only jpg, jpeg, and png allowed.")

        # Перевірка розміру файлу
        file_content = await file.read()
        if len(file_content) > max_file_size:
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 2 MB.")

        # Санітизація імені файлу
        safe_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', file.filename)

        # Завантаження аватара на Cloudinary
        upload_result = cloudinary.uploader.upload(
            file_content,
            public_id=f"user_{user_data['id']}_{safe_filename}",
            resource_type="image"
        )

        # Отримання URL з Cloudinary
        avatar_url = upload_result.get('secure_url')
        if not avatar_url:
            raise HTTPException(status_code=500, detail="Failed to upload avatar to Cloudinary.")

        # Оновлення URL аватара в базі даних
        crud.update_user_avatar(db, user_id=user_data["id"], avatar_url=avatar_url)

        return {"message": "Avatar updated successfully", "avatar_url": avatar_url}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="User data must be a valid JSON string.")
    except HTTPException as e:
        raise e  # Перехоплення винятків HTTPException
    except Exception as e:
        logger.error(f"Error during avatar update: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")


# 5. Скидання пароля
@router.post("/reset-password")
async def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    """
    Скидання пароля за допомогою токена.

    Перевіряє дійсність токена, надісланого на email, і оновлює пароль користувача.

    Args:
        token (str): Токен для верифікації зміни пароля.
        new_password (str): Новий пароль.
        db (Session): Сесія бази даних.

    Returns:
        dict: Повідомлення про успішне оновлення пароля.
    """

    def validate_password(password: str):
        """
        Валідація пароля.

        Перевіряє мінімальну довжину, наявність літер, цифр та спеціальних символів.

        Args:
            password (str): Пароль для перевірки.

        Raises:
            HTTPException: Якщо пароль не відповідає вимогам.
        """
        if len(password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
        if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
            raise HTTPException(status_code=400, detail="Password must contain letters and numbers")
        if not re.search(r"[\W_]", password):
            raise HTTPException(status_code=400, detail="Password must contain special characters")

    validate_password(new_password)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")

        token_expiration = datetime.utcfromtimestamp(payload["exp"])
        if token_expiration < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Token expired")

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = hashing.hash_password(new_password)
    user.hashed_password = hashed_password
    db.commit()

    return {"message": "Password successfully updated"}


# 6. Повернення інформації про поточного користувача
@router.get("/me", response_model=schemas.UserOut)
def get_current_user_info(current_user: schemas.UserOut = Depends(get_current_user)):
    """
    Повертає інформацію про поточного авторизованого користувача.

    Args:
        current_user (schemas.UserOut): Поточний авторизований користувач.

    Returns:
        schemas.UserOut: Інформація про користувача.
    """
    return current_user


# 7. Перевірка email через токен
@router.get("/verify/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Перевірка email користувача за допомогою токена.

    Оновлює статус верифікації користувача в базі даних.

    Args:
        token (str): Токен для перевірки.
        db (Session): Сесія бази даних.

    Returns:
        dict: Повідомлення про успішну верифікацію email.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")

        if not email:
            raise HTTPException(status_code=400, detail="Email not found in token")

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user.is_verified = True
        db.commit()

        return {"message": "Email verified successfully."}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error during email verification: {str(e)}")


# 8. Видалення користувача
@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Видаляє користувача з бази даних за його id.

    Args:
        user_id (int): ID користувача, якого потрібно видалити.
        db (Session): Сесія бази даних.

    Returns:
        dict: Підтвердження успішного видалення.
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        # Видаляємо користувача з бази даних
        db.delete(user)
        db.commit()
        logger.info(f"User {user_id} deleted successfully.")
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error during user deletion: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
