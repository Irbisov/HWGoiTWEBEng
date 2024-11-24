FROM python:3.12-slim

# Оновлення пакетів і встановлення залежностей
RUN apt-get update -y && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Встановлення Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Додаємо Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Створюємо робочий каталог
WORKDIR /app

# Копіюємо pyproject.toml та poetry.lock
COPY pyproject.toml poetry.lock ./

# Копіюємо wait-for-it скрипт
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Встановлюємо залежності
RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-dev

# Копіюємо решту файлів (замість копіювання всього зразу, щоб кешувати залежності)
COPY restapiapp /app/restapiapp
COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock

# Вивести значення PORT для перевірки
RUN echo "PORT is set to $PORT"

# Відкриваємо порт для додатку
EXPOSE 8000

# Команда для запуску додатку з правильним портом
CMD ["sh", "-c", "/wait-for-it.sh db:5432 -- poetry run uvicorn restapiapp.main:app --host 0.0.0.0 --port 8000"]

