from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None


class ContactCreate(ContactBase):
    """
    Використовується для створення нового контакту. Успадковує всі поля з ContactBase.
    """
    pass


class ContactUpdate(BaseModel):
    """
    Використовується для оновлення контакту. Всі поля необов'язкові, дозволяючи часткове оновлення.
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None


class ContactInDB(ContactBase):
    """
    Модель, яка представляє контакт в базі даних.
    """
    id: int

    class Config:
        from_attributes = True
