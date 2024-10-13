import json
import logging
from mongoengine import connect
from models import Author, Quote
from connect_to_mongo import connect_mongo

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Підключення до MongoDB
try:
    connect_mongo()
    logging.info("Успішно підключено до MongoDB.")
except Exception as e:
    logging.error(f"Не вдалося підключитися до MongoDB: {e}")

def fetch_quotes_by_author(author_name):
    """Отримання цитат за ім'ям автора."""
    logging.info(f"Пошук цитат для автора: {author_name}")
    authors = Author.objects(fullname__icontains=author_name)
    if authors:
        author_ids = [author.id for author in authors]
        quotes = Quote.objects(author__in=author_ids)
        logging.info(f"Знайдено {len(quotes)} цитат для автора {author_name}.")
        return quotes
    logging.warning(f"Автор {author_name} не знайдено.")
    return None

def fetch_quotes_by_tag(tag_name):
    """Отримання цитат за тегом."""
    logging.info(f"Пошук цитат за тегом: {tag_name}")
    quotes = Quote.objects(tags__in=[tag_name])
    logging.info(f"Знайдено {len(quotes)} цитат за тегом {tag_name}.")
    return quotes

def fetch_quotes_by_tags(tag_list):
    """Отримання цитат за списком тегів."""
    logging.info(f"Пошук цитат за тегами: {tag_list}")
    quotes = Quote.objects(tags__in=tag_list)
    logging.info(f"Знайдено {len(quotes)} цитат за тегами {tag_list}.")
    return quotes

def search_quotes(command):
    """Основна функція для обробки команд."""
    try:
        if command.startswith("name:"):
            author_name = command.split(":", 1)[1].strip()
            quotes = fetch_quotes_by_author(author_name)
            if quotes:
                result = "\n".join([q.quote for q in quotes])
                print(result)
            else:
                print("Автор не знайдено.")

        elif command.startswith("tag:"):
            tag_name = command.split(":", 1)[1].strip()
            quotes = fetch_quotes_by_tag(tag_name)
            if quotes:
                result = "\n".join([q.quote for q in quotes])
                print(result)
            else:
                print("Цитат за тегом не знайдено.")

        elif command.startswith("tags:"):
            tags = command.split(":", 1)[1].strip().split(",")
            quotes = fetch_quotes_by_tags(tags)
            if quotes:
                result = "\n".join([q.quote for q in quotes])
                print(result)
            else:
                print("Цитат за зазначеними тегами не знайдено.")

        elif command == "exit":
            logging.info("Користувач завершив програму.")
            print("Завершення програми.")
            return

        else:
            logging.warning("Невірна команда.")
            print("Невірна команда. Використовуйте: name:<author>, tag:<tag>, tags:<tag1,tag2> або exit.")

    except Exception as e:
        logging.error(f"Помилка під час виконання команди: {e}")

# Цикл для прийому команд
while True:
    command = input("Введіть команду: ")
    search_quotes(command)
