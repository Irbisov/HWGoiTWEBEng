# Виберіть базовий образ з Python
FROM python:3.10

# Встановлення робочої директорії в контейнері
WORKDIR /app

# Копіюйте файл requirements.txt і встановіть залежності (якщо у вас є)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копіюйте всі файли в робочу директорію контейнера
COPY . .

# Відкрийте порти 3000 для HTTP-сервера і 5000 для сокет-сервера
EXPOSE 3000
EXPOSE 5000

# Запустіть сокет-сервер і HTTP-сервер одночасно
CMD ["python3", "main.py", "&", "python3","socket_server.py"]