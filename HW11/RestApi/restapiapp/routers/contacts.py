from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.ContactInDB)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)


@router.get("/", response_model=list[schemas.ContactInDB])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_contacts(db, skip=skip, limit=limit)


@router.get("/{contact_id}", response_model=schemas.ContactInDB)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.put("/{contact_id}", response_model=schemas.ContactInDB)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.delete("/{contact_id}", response_model=schemas.ContactInDB)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.get("/search/", response_model=list[schemas.ContactInDB])
def search_contacts(query: str, db: Session = Depends(get_db)):
    return crud.search_contacts(db, query=query)


@router.get("/birthdays/", response_model=list[schemas.ContactInDB])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return crud.get_upcoming_birthdays(db)
