import json
import logging
import redis
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

# Підключення до Redis
try:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, socket_timeout=10)  # Збільшено до 10 секунд
    logging.info("Успішно підключено до Redis.")
except Exception as e:
    logging.error(f"Не вдалося підключитися до Redis: {e}")


def fetch_quotes_by_author(author_name):
    """Отримання цитат за ім'ям автора."""
    logging.info(f"Пошук цитат для автора: {author_name}")
    try:
        authors = Author.objects(fullname__icontains=author_name)
        if authors:
            author_ids = [author.id for author in authors]
            quotes = Quote.objects(author__in=author_ids)
            logging.info(f"Знайдено {len(quotes)} цитат для автора {author_name}.")
            return quotes
        logging.warning(f"Автор {author_name} не знайдено.")
        return None
    except Exception as e:
        logging.error(f"Помилка при пошуку автора: {e}")
        return None


def fetch_quotes_by_tag(tag_name):
    """Отримання цитат за тегом."""
    logging.info(f"Пошук цитат за тегом: {tag_name}")
    try:
        quotes = Quote.objects(tags__in=[tag_name])
        logging.info(f"Знайдено {len(quotes)} цитат за тегом {tag_name}.")
        return quotes
    except Exception as e:
        logging.error(f"Помилка при пошуку тегу: {e}")
        return None


def fetch_quotes_by_tags(tag_list):
    """Отримання цитат за списком тегів."""
    logging.info(f"Пошук цитат за тегами: {tag_list}")
    try:
        quotes = Quote.objects(tags__in=tag_list)
        logging.info(f"Знайдено {len(quotes)} цитат за тегами {tag_list}.")
        return quotes
    except Exception as e:
        logging.error(f"Помилка при пошуку тегів: {e}")
        return None


def cache_results(key, result):
    """Кешування результатів у Redis."""
    try:
        redis_client.set(key, json.dumps(result), ex=3600)  # Кешувати на 1 годину
    except Exception as e:
        logging.error(f"Помилка при кешуванні результатів: {e}")


def get_cached_results(key):
    """Отримання кешованих результатів з Redis."""
    try:
        cached_result = redis_client.get(key)
        if cached_result:
            logging.info(f"Використання кешу для ключа: {key}")
            return json.loads(cached_result)
        return None
    except Exception as e:
        logging.error(f"Помилка при отриманні кешу: {e}")
        return None


def search_quotes(command):
    """Основна функція для обробки команд."""
    try:
        if command.startswith("name:"):
            author_name = command.split(":", 1)[1].strip()
            if len(author_name) < 3:
                logging.warning("Скорочене ім'я автора занадто коротке.")
                print("Ім'я автора повинно містити щонайменше 3 символи.")
                return

            cached_quotes = get_cached_results(f"name:{author_name}")
            if cached_quotes:
                result = "\n".join(cached_quotes)
                print(result)
                return

            quotes = fetch_quotes_by_author(author_name)
            if quotes:
                result = "\n".join([q.quote for q in quotes])
                print(result)
                cache_results(f"name:{author_name}", [q.quote for q in quotes])
            else:
                print("Автор не знайдено.")

        elif command.startswith("tag:"):
            tag_name = command.split(":", 1)[1].strip()
            if len(tag_name) < 3:
                logging.warning("Скорочений тег занадто короткий.")
                print("Тег повинен містити щонайменше 3 символи.")
                return

            cached_quotes = get_cached_results(f"tag:{tag_name}")
            if cached_quotes:
                result = "\n".join(cached_quotes)
                print(result)
                return

            quotes = fetch_quotes_by_tag(tag_name)
            if quotes:
                result = "\n".join([q.quote for q in quotes])
                print(result)
                cache_results(f"tag:{tag_name}", [q.quote for q in quotes])
            else:
                print("Цитат за тегом не знайдено.")

        elif command.startswith("tags:"):
            tags = command.split(":", 1)[1].strip().split(",")
            tags = [tag.strip() for tag in tags if len(tag.strip()) >= 2]

            if not tags:
                print("Всі теги занадто короткі.")
                return

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
