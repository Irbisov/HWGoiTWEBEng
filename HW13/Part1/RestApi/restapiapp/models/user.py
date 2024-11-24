from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from restapiapp.database import Base
from sqlalchemy import Boolean


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    contacts = relationship("Contact", back_populates="user")
    is_verified = Column(Boolean, default=False)


# Хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
