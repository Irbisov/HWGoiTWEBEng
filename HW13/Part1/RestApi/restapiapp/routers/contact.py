from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from restapiapp import schemas, crud
from restapiapp.dependencies import get_current_user
from restapiapp.models.user import User
from fastapi_limiter.depends import RateLimiter
from restapiapp.database import get_db

router = APIRouter(prefix="/contacts", tags=["Contacts"])

# Залежність для створення сесії БД
get_db()


# 1. Створення нового контакту
@router.post("/", response_model=schemas.contact.ContactInDB, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def create_contact(
        contact: schemas.contact.ContactCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Створення нового контакту.
    """
    return crud.contact.create_contact(db=db, contact=contact, owner_id=current_user.id)


# 2. Отримання списку контактів поточного користувача
@router.get("/", response_model=list[schemas.contact.ContactInDB])
def read_contacts(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Отримання списку контактів поточного користувача.
    """
    return crud.contact.get_contacts(db, skip=skip, limit=limit, owner_id=current_user.id)


# 3. Отримання одного контакту за ID
@router.get("/{contact_id}", response_model=schemas.contact.ContactInDB)
def read_contact(
        contact_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Отримання одного контакту за ID.
    """
    db_contact = crud.contact.get_contact(db, contact_id=contact_id, owner_id=current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


# 4. Пошук контактів за ключовим словом
@router.get("/search/", response_model=list[schemas.contact.ContactInDB])
def search_contacts(
        query: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Пошук контактів за ключовим словом.
    """
    return crud.contact.search_contacts(db, query=query, owner_id=current_user.id)


# 5. Отримання контактів з днями народження, які відбудуться протягом `days_ahead` днів
@router.get("/birthdays/", response_model=list[schemas.contact.ContactInDB])
def upcoming_birthdays(
        days_ahead: int = 30,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Отримання контактів з днями народження, які відбудуться протягом `days_ahead` днів.
    """
    return crud.contact.get_upcoming_birthdays(db, days_ahead=days_ahead, owner_id=current_user.id)


# 6. Оновлення існуючого контакту
@router.put("/{contact_id}", response_model=schemas.contact.ContactInDB)
def update_contact(
        contact_id: int,
        contact: schemas.contact.ContactUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Оновлення існуючого контакту.
    """
    db_contact = crud.contact.update_contact(db, contact_id=contact_id, contact=contact, owner_id=current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


# 7. Видалення контакту
@router.delete("/{contact_id}")
def delete_contact(
        contact_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Видалення контакту.
    """
    db_contact = crud.contact.delete_contact(db, contact_id=contact_id, owner_id=current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}
