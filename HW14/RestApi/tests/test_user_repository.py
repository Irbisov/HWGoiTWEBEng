import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from restapiapp.models.user import User
from restapiapp.schemas.user import UserCreate
from restapiapp.crud.user import (
    get_user,
    get_user_by_email,
    create_user,
    verify_user_email,
    update_user_avatar,
    delete_user
)


# Фікстури для тестів
@pytest.fixture
def mock_db():
    return MagicMock(Session)


@pytest.fixture
def existing_user():
    return User(id=1, email="test@example.com", hashed_password="hashed_password")


@pytest.fixture
def new_user_data():
    return UserCreate(email="newuser@example.com", password="password")


# Тести
def test_get_user(mock_db, existing_user):
    mock_db.query().filter().first.return_value = existing_user
    user = get_user(mock_db, 1)
    assert user == existing_user


def test_get_user_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    with pytest.raises(HTTPException):
        get_user(mock_db, 999)


def test_get_user_by_email(mock_db, existing_user):
    mock_db.query().filter().first.return_value = existing_user
    user = get_user_by_email(mock_db, "test@example.com")
    assert user == existing_user


def test_get_user_by_email_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    user = get_user_by_email(mock_db, "nonexistent@example.com")
    assert user is None


def test_create_user(mock_db, new_user_data):
    # Мок для перевірки, чи існує користувач
    mock_db.query().filter().first.return_value = None
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    new_user = create_user(mock_db, new_user_data)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
    assert new_user.email == new_user_data.email


def test_create_user_email_exists(mock_db, new_user_data, existing_user):
    # Мок для перевірки, чи існує користувач з таким email
    mock_db.query().filter().first.return_value = existing_user
    with pytest.raises(HTTPException):
        create_user(mock_db, new_user_data)


def test_verify_user_email(mock_db, existing_user):
    mock_db.query().filter().first.return_value = existing_user
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    user = verify_user_email(mock_db, "test@example.com")

    assert user.is_verified is True
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_verify_user_email_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    with pytest.raises(HTTPException):
        verify_user_email(mock_db, "nonexistent@example.com")


def test_update_user_avatar(mock_db, existing_user):
    mock_db.query().filter().first.return_value = existing_user
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()

    user = update_user_avatar(mock_db, 1, "new_avatar_url")

    assert user.avatar_url == "new_avatar_url"
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_update_user_avatar_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    with pytest.raises(HTTPException):
        update_user_avatar(mock_db, 999, "new_avatar_url")


def test_delete_user(mock_db, existing_user):
    mock_db.query().filter().first.return_value = existing_user
    mock_db.delete = MagicMock()
    mock_db.commit = MagicMock()

    delete_user(mock_db, 1)

    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()


def test_delete_user_not_found(mock_db):
    mock_db.query().filter().first.return_value = None
    with pytest.raises(HTTPException):
        delete_user(mock_db, 999)
