# Проект: Email та SMS Розсилка з Використанням RabbitMQ

## Опис
Цей проект реалізує систему розсилки електронних листів та SMS-повідомлень контактам за допомогою RabbitMQ. Проект використовує MongoDB для зберігання контактної інформації та RabbitMQ для управління повідомленнями.

## Архітектура
Проект складається з наступних компонентів:
- **producer.py**: Генерує фейкові контакти, зберігає їх у базі даних MongoDB і відправляє повідомлення в чергу RabbitMQ.
- **consumer_email.py**: Отримує повідомлення з черги RabbitMQ та імітує надсилання електронних листів. Після успішного надсилання змінює статус контакту в базі даних.
- **consumer_sms.py**: Отримує повідомлення з черги RabbitMQ та імітує надсилання SMS-повідомлень. Після успішного надсилання змінює статус контакту в базі даних.
- **Docker Compose**: Використовується для налаштування контейнерів RabbitMQ та MongoDB.

## Вимоги
- Python 3.12
- RabbitMQ
- MongoDB
- Бібліотеки:
  - pika
  - mongoengine
  - dotenv

## Налаштування
1. Клонувати репозиторій:
   ```bash
   git clone <URL вашого репозиторію>
   cd <ім'я_папки_з_репозиторієм>
