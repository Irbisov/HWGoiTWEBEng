from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


# Модель для реєстрації нового користувача
class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True  # Включаємо підтримку ORM для відображення об'єктів SQLAlchemy


# Модель для відповіді з токенами
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"  # Додаємо тип токену (за замовчуванням "bearer")


class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    avatar_url: str

