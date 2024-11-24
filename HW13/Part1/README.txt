
# Django REST API Project

## Опис

Цей проект представляє собою REST API для управління контактами користувачів. Він реалізує автентифікацію та авторизацію за допомогою JWT токенів, забезпечує CRUD операції для контактів, а також можливість пошуку контактів та фільтрації за категоріями. Для управління користувачами використовуються стандартні моделі Django, а дані зберігаються в PostgreSQL базі даних.

## Функціональність

- **User Authentication**: Реалізовано реєстрацію, вхід, вихід користувачів.
- **JWT Tokens**: Для захисту API використовується JSON Web Tokens (JWT).
- **CRUD Operations**: Операції створення, читання, оновлення та видалення контактів.
- **Пошук**: Пошук контактів за категорією.
- **Профіль користувача**: Кожен користувач може переглядати та редагувати свій профіль.

## Технології

- Django 5.1.2
- Django REST Framework
- PostgreSQL
- JWT для аутентифікації
- Docker (для контейнеризації проекту)

## Встановлення

### Крок 1: Клонуйте репозиторій

```bash
git clone <URL вашого репозиторію>
cd <назва проекту>
```

### Крок 2: Створіть віртуальне середовище та активуйте його

```bash
python3 -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate
```

### Крок 3: Встановіть залежності

```bash
poetry
```

### Крок 4: Налаштуйте базу даних

Налаштуйте підключення до бази даних у файлі `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Крок 5: Виконайте міграції

```bash
python manage.py migrate
```

### Крок 6: Створіть суперкористувача

```bash
python manage.py createsuperuser
```

### Крок 7: Запустіть сервер

```bash
python manage.py runserver
```

## Використання

### Реєстрація користувача

POST `/auth/register/`
- Параметри:
  - `username`
  - `email`
  - `password`
  - `password2` (підтвердження пароля)

### Вхід користувача

POST `/auth/login/`
- Параметри:
  - `username`
  - `password`

### Створення контакту

POST `/contacts/`
- Параметри:
  - `name`
  - `email`
  - `phone_number`

### Перегляд контактів

GET `/contacts/`

### Оновлення контакту

PUT `/contacts/<id>/`
- Параметри:
  - `name`
  - `email`
  - `phone_number`

### Видалення контакту

DELETE `/contacts/<id>/`

### Пошук контактів

GET `/contacts/search/`
- Параметри:
  - `category` (фільтрація за категорією)
