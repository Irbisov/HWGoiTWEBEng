from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from restapiapp.models.user import User
from restapiapp.schemas.user import UserCreate
from ..utils.hashing import hash_password
import logging

# Налаштування логування
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def get_user(db: Session, user_id: int) -> User:
    """
    Отримує користувача за його user_id.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"User with ID {user_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    logger.debug(f"User with ID {user_id} retrieved successfully.")
    return user


def get_user_by_email(db: Session, email: str) -> User:
    """
    Отримує користувача за email.
    """
    user = db.query(User).filter(User.email == email).first()
    if user:
        logger.debug(f"User with email {email} found.")
    else:
        logger.debug(f"User with email {email} not found.")
    return user


def create_user(db: Session, user: UserCreate) -> User:
    """
    Створює нового користувача після перевірки унікальності email.
    """
    try:
        # Перевірка, чи вже існує користувач з таким email
        existing_user = get_user_by_email(db, user.email)
        if existing_user:
            logger.warning(f"Attempt to register with an already registered email: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Хешування пароля
        hashed_password = hash_password(user.password)
        logger.debug(f"Password for {user.email} hashed successfully.")

        # Створення нового користувача
        new_user = User(email=user.email, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User {user.email} created successfully.")
        return new_user

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error while creating user {user.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error. Please check the provided data."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating user {user.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error. Please try again later."
        )


def verify_user_email(db: Session, email: str) -> User:
    """
    Верифікує email користувача.
    """
    try:
        # Отримання користувача за email
        user = get_user_by_email(db, email)
        if not user:
            logger.warning(f"Verification attempt for non-existent email: {email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Оновлення статусу верифікації
        user.is_verified = True
        db.commit()
        db.refresh(user)
        logger.info(f"Email {email} verified successfully.")
        return user

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to verify email {email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during email verification."
        )


def update_user_avatar(db: Session, user_id: int, avatar_url: str) -> User:
    """
    Оновлює аватар користувача за його user_id.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"User with ID {user_id} not found for avatar update.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Оновлення аватара
        user.avatar_url = avatar_url
        db.commit()
        db.refresh(user)
        logger.info(f"Avatar for user {user_id} updated successfully to {avatar_url}.")
        return user
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update avatar for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while updating avatar."
        )
