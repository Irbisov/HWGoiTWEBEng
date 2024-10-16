import json
import logging
from mongoengine import Document, StringField, ListField
from connect_to_mongo import connect_mongo
import warnings
from cryptography.utils import CryptographyDeprecationWarning

# Ігноруємо попередження
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mongo_import.log'),  # Логування в файл
        logging.StreamHandler()  # Логування в термінал
    ]
)

# Підключення до MongoDB
connect_mongo()


# Визначення моделей
class Quote(Document):
    text = StringField(required=True)
    author = StringField(required=True)
    tags = ListField(StringField())


class Author(Document):
    name = StringField(required=True)
    birthdate = StringField()
    bio = StringField()


# Завантаження цитат у MongoDB
def load_quotes():
    try:
        logging.info("Спроба завантаження цитат...")
        with open('quotes_scraper/quotes.json') as f:
            quotes = json.load(f)
            for quote in quotes:
                Quote(**quote).save()
        logging.info(f"Успішно завантажено {len(quotes)} цитат до MongoDB.")
    except Exception as e:
        logging.error(f"Помилка під час завантаження цитат: {e}")


# Завантаження авторів у MongoDB
def load_authors():
    try:
        logging.info("Спроба завантаження авторів...")
        with open('quotes_scraper/authors.json') as f:
            authors = json.load(f)
            for author in authors:
                Author(**author).save()
        logging.info(f"Успішно завантажено {len(authors)} авторів до MongoDB.")
    except Exception as e:
        logging.error(f"Помилка під час завантаження авторів: {e}")


if __name__ == '__main__':
    logging.info("Початок завантаження даних у MongoDB.")
    load_quotes()
    load_authors()
    logging.info("Завершено завантаження даних у MongoDB.")
