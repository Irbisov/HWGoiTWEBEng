import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from restapiapp.models.contact import Contact
from restapiapp.schemas.contact import ContactCreate, ContactUpdate
from restapiapp.crud.contact import (
    create_contact,
    get_contacts,
    get_contact,
    update_contact,
    delete_contact,
    search_contacts,
    get_upcoming_birthdays
)


# Фікстури для тестів
@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def existing_contact():
    return Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com", owner_id=1, birthday=datetime(1990, 5, 14))


@pytest.fixture
def new_contact_data():
    return ContactCreate(first_name="Jane", last_name="Smith", email="jane.smith@example.com", birthday=datetime(1995, 6, 20))


@pytest.fixture
def updated_contact_data():
    return ContactUpdate(first_name="Janet", last_name="Smith", email="janet.smith@example.com")


# Тести
def test_create_contact(mock_db, new_contact_data):
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    contact = create_contact(mock_db, new_contact_data, owner_id=1)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert contact.first_name == new_contact_data.first_name
    assert contact.last_name == new_contact_data.last_name


def test_get_contacts(mock_db, existing_contact):
    mock_db.query().filter().offset().limit().all.return_value = [existing_contact]

    contacts = get_contacts(mock_db, skip=0, limit=10, owner_id=1)

    assert len(contacts) == 1
    assert contacts[0].id == existing_contact.id


def test_get_contact(mock_db, existing_contact):
    mock_db.query().filter().first.return_value = existing_contact

    contact = get_contact(mock_db, contact_id=1, owner_id=1)

    assert contact.id == existing_contact.id


def test_get_contact_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    contact = get_contact(mock_db, contact_id=999, owner_id=1)

    assert contact is None


def test_update_contact(mock_db, existing_contact, updated_contact_data):
    mock_db.query().filter().first.return_value = existing_contact
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    updated_contact = update_contact(mock_db, contact_id=1, contact=updated_contact_data, owner_id=1)

    assert updated_contact.first_name == updated_contact_data.first_name
    assert updated_contact.last_name == updated_contact_data.last_name
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_update_contact_not_found(mock_db, updated_contact_data):
    mock_db.query().filter().first.return_value = None

    contact = update_contact(mock_db, contact_id=999, contact=updated_contact_data, owner_id=1)

    assert contact is None


def test_delete_contact(mock_db, existing_contact):
    mock_db.query().filter().first.return_value = existing_contact
    mock_db.delete = MagicMock()
    mock_db.commit = MagicMock()

    deleted_contact = delete_contact(mock_db, contact_id=1, owner_id=1)

    assert deleted_contact.id == existing_contact.id
    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()


def test_delete_contact_not_found(mock_db):
    mock_db.query().filter().first.return_value = None

    deleted_contact = delete_contact(mock_db, contact_id=999, owner_id=1)

    assert deleted_contact is None


def test_search_contacts(mock_db, existing_contact):
    mock_db.query().filter().all.return_value = [existing_contact]

    contacts = search_contacts(mock_db, query="john", owner_id=1)

    assert len(contacts) == 1
    assert contacts[0].id == existing_contact.id


def test_get_upcoming_birthdays(mock_db, existing_contact):
    mock_db.query().filter().all.return_value = [existing_contact]

    # Використовуємо тільки дату без часу
    today = datetime.today().date()  # Беремо тільки дату без часу
    days_ahead = 30

    # Оновлюємо логіку, щоб створити контакт з датою народження в межах 30 днів
    existing_contact.birthday = today + timedelta(days=10)  # Контакт з датою народження через 10 днів

    upcoming_birthday = get_upcoming_birthdays(mock_db, days_ahead=days_ahead, owner_id=1)

    assert len(upcoming_birthday) == 1
    assert upcoming_birthday[0].id == existing_contact.id
    assert existing_contact.birthday >= today  # Перевіряємо тільки дату, без .date()
    assert existing_contact.birthday <= today + timedelta(days=days_ahead)  # Перевіряємо тільки дату




def test_get_upcoming_birthdays_empty(mock_db):
    mock_db.query().filter().all.return_value = []

    upcoming_birthday = get_upcoming_birthdays(mock_db, days_ahead=30, owner_id=1)

    assert len(upcoming_birthday) == 0
