from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from restapiapp.models.user import User
from restapiapp.schemas.user import UserCreate
from ..utils.hashing import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    # Перевірка, чи вже існує користувач з таким email
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Хешування пароля
    hashed_password = hash_password(user.password)

    # Створення нового користувача
    new_user = User(email=user.email, hashed_password=hashed_password)

    # Додавання користувача в базу
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
