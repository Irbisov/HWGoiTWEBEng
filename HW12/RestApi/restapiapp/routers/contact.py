from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from restapiapp import models, schemas, crud
from restapiapp.database import SessionLocal
from datetime import datetime, timedelta

router = APIRouter(prefix="/contacts", tags=["Contacts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.contact.ContactInDB)
def create_contact(contact: schemas.contact.ContactCreate, db: Session = Depends(get_db)):
    db_contact = crud.contact.create_contact(db=db, contact=contact)
    return db_contact


@router.get("/", response_model=list[schemas.contact.ContactInDB])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.contact.get_contacts(db, skip=skip, limit=limit)


@router.get("/{contact_id}", response_model=schemas.contact.ContactInDB)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.contact.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.put("/{contact_id}", response_model=schemas.contact.ContactInDB)
def update_contact(contact_id: int, contact: schemas.contact.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.contact.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.delete("/{contact_id}", response_model=schemas.contact.ContactInDB)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.contact.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.get("/search/", response_model=list[schemas.contact.ContactInDB])
def search_contacts(query: str, db: Session = Depends(get_db)):
    return crud.contact.search_contacts(db, query=query)


@router.get("/birthdays/", response_model=list[schemas.contact.ContactInDB])
def upcoming_birthdays(db: Session = Depends(get_db), days_ahead: int = 30):
    return crud.contact.get_upcoming_birthdays(db, days_ahead=days_ahead)
