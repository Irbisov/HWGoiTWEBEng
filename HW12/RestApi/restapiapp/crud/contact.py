from sqlalchemy.orm import Session
from restapiapp import models, schemas
from datetime import datetime, timedelta


def create_contact(db: Session, contact: schemas.contact.ContactCreate):
    existing_contact = db.query(models.contact.Contact).filter(models.contact.Contact.email == contact.email).first()
    if existing_contact:
        raise ValueError(f"A contact with email {contact.email} already exists.")

    db_contact = models.contact.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.contact.Contact).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int):
    return db.query(models.contact.Contact).filter(models.contact.Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, contact: schemas.contact.ContactUpdate):
    db_contact = db.query(models.contact.Contact).filter(models.contact.Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.contact.Contact).filter(models.contact.Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def search_contacts(db: Session, query: str):
    return db.query(models.contact.Contact).filter(
        models.contact.Contact.first_name.ilike(f"%{query}%") |
        models.contact.Contact.last_name.ilike(f"%{query}%") |
        models.contact.Contact.email.ilike(f"%{query}%")
    ).all()


def get_upcoming_birthdays(db: Session, days_ahead: int = 30):
    today = datetime.today()
    upcoming_date = today + timedelta(days=days_ahead)
    return db.query(models.contact.Contact).filter(
        models.contact.Contact.birthday >= today,
        models.contact.Contact.birthday <= upcoming_date
    ).all()
