FROM python:3.12-slim

# Встановлення системних залежностей, які можуть знадобитися для Poetry або вашого додатка
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо Poetry
RUN pip install poetry

# Встановлюємо робочий каталог
WORKDIR /app

# Копіюємо файли для Poetry
COPY pyproject.toml poetry.lock ./

# Встановлюємо залежності
RUN poetry install --no-root --no-dev

# Копіюємо код додатка
COPY . .

