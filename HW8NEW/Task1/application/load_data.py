import json
import logging
from mongoengine import connect
from models import Author, Quote
from connect_to_mongo import connect_mongo

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,  # Рівень логування
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_load.log"),  # Логування у файл
        logging.StreamHandler()  # Вивід в консоль
    ]
)

# Підключення до MongoDB
try:
    connect_mongo()
    logging.info("Підключення до MongoDB успішне.")
except Exception as e:
    logging.error(f"Помилка підключення до MongoDB: {e}")
    exit()

# Завантаження авторів
try:
    with open('authors.json') as f:
        authors_data = json.load(f)
        for author in authors_data:
            new_author = Author(
                fullname=author['fullname'],
                born_date=author['born_date'],
                born_location=author['born_location'],
                description=author['description']
            )
            new_author.save()
            logging.info(f"Автор додано: {author['fullname']}")
except Exception as e:
    logging.error(f"Помилка завантаження авторів: {e}")

# Завантаження цитат
try:
    with open('quotes.json') as f:
        quotes_data = json.load(f)
        for quote in quotes_data:
            author = Author.objects(fullname=quote['author']).first()
            if author:
                new_quote = Quote(
                    tags=quote['tags'],
                    author=author,
                    quote=quote['quote']
                )
                new_quote.save()
                logging.info(f"Цитата додана: \"{quote['quote']}\" автор: {quote['author']}")
            else:
                logging.warning(f"Автор не знайдено для цитати: \"{quote['quote']}\"")
except Exception as e:
    logging.error(f"Помилка завантаження цитат: {e}")

logging.info("Завершення процесу завантаження.")
