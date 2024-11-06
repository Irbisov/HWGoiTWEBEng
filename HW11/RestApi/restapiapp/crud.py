from sqlalchemy.orm import Session
from . import models, schemas
from datetime import timedelta, date
from sqlalchemy import extract


def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Contact).offset(skip).limit(limit).all()


def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def search_contacts(db: Session, query: str):
    return db.query(models.Contact).filter(
        (models.Contact.first_name.ilike(f"%{query}%")) |
        (models.Contact.last_name.ilike(f"%{query}%")) |
        (models.Contact.email.ilike(f"%{query}%"))
    ).all()


def get_upcoming_birthdays(db: Session, days_ahead: int = 7):
    today = date.today()
    upcoming = today + timedelta(days=days_ahead)
    today_month_day = (today.month, today.day)
    upcoming_month_day = (upcoming.month, upcoming.day)
    return db.query(models.Contact).filter(
        (extract('month', models.Contact.birthday) == today_month_day[0]) &
        (extract('day', models.Contact.birthday) >= today_month_day[1]) &
        (extract('month', models.Contact.birthday) == upcoming_month_day[0]) &
        (extract('day', models.Contact.birthday) <= upcoming_month_day[1])
    ).all()
