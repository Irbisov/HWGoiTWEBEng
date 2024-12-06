import pytest
from restapiapp.schemas.user import UserCreate
from restapiapp.utils.auth import create_verification_token
from fastapi.testclient import TestClient
from restapiapp.main import app

# Фікстура для клієнта
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

# Фікстура для нового користувача
@pytest.fixture
def new_user():
    return UserCreate(email="test@example.com", password="password123")


# 1. Тест для реєстрації нового користувача
def test_register(client, new_user):
    response = client.post("/auth/register", json=new_user.dict())
    assert response.status_code == 201
    assert response.json()["email"] == new_user.email
    assert "id" in response.json()


# 2. Тест для реєстрації користувача з вже зареєстрованою email
def test_register_existing_user(client, new_user):
    client.post("/auth/register", json=new_user.dict())  # Реєстрація
    response = client.post("/auth/register", json=new_user.dict())  # Повторна реєстрація
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


# 3. Тест для логіну
def test_login(client, new_user):
    client.post("/auth/register", json=new_user.dict())  # Реєстрація
    login_data = {"username": new_user.email, "password": new_user.password}
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


# 4. Тест для перевірки email
def test_verify_email(client, new_user):
    client.post("/auth/register", json=new_user.dict())  # Реєстрація
    token = create_verification_token(new_user.email)
    response = client.get(f"/auth/verify/{token}")
    assert response.status_code == 200
    assert response.json()["message"] == "Email verified successfully."


# 5. Тест для скидання пароля
def test_reset_password(client, new_user):
    client.post("/auth/register", json=new_user.dict())  # Реєстрація
    token = create_verification_token(new_user.email)
    response = client.post("/auth/reset-password", json={"token": token, "new_password": "new_password123"})
    assert response.status_code == 200
    assert response.json()["message"] == "Password successfully updated"
