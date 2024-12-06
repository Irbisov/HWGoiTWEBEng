from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from restapiapp.models.contact import Contact
from restapiapp.schemas.contact import ContactCreate, ContactUpdate


def create_contact(db: Session, contact: ContactCreate, owner_id: int):
    db_contact = Contact(**contact.dict(), owner_id=owner_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, skip: int, limit: int, owner_id: int):
    return db.query(Contact).filter(Contact.owner_id == owner_id).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int, owner_id: int):
    return db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()


def update_contact(db: Session, contact_id: int, contact: ContactUpdate, owner_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()
    if db_contact:
        for key, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int, owner_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def search_contacts(db: Session, query: str, owner_id: int):
    return db.query(Contact).filter(
        Contact.owner_id == owner_id,
        (Contact.first_name.ilike(f"%{query}%")) |
        (Contact.last_name.ilike(f"%{query}%")) |
        (Contact.email.ilike(f"%{query}%"))
    ).all()


def get_upcoming_birthdays(db: Session, days_ahead: int, owner_id: int):
    today = datetime.today()
    upcoming_birthdays = db.query(Contact).filter(
        Contact.owner_id == owner_id,  # Фільтруємо за owner_id
        Contact.birthday >= today,
        Contact.birthday <= today + timedelta(days=days_ahead)
    ).all()
    return upcoming_birthdays
