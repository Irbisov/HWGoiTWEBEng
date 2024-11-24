import logging
from pymongo import MongoClient
import psycopg2
import json

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_postgres_connection(uri):
    """Функція для створення з'єднання з PostgreSQL."""
    try:
        connection = psycopg2.connect(uri)
        logger.info("Успішне з'єднання з PostgreSQL.")
        return connection
    except Exception as e:
        logger.error(f"Помилка під час з'єднання з PostgreSQL: {e}")
        return None


def create_table_if_not_exists(cursor):
    """Функція для створення таблиці quotes_tag, якщо вона не існує."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quotes_tag (
        id SERIAL PRIMARY KEY,
        tags TEXT UNIQUE NOT NULL
    );
    """)
    logger.info("Таблиця quotes_tag перевірена або створена.")


def migrate_data():
    """Функція для міграції даних з MongoDB в PostgreSQL."""
    logger.info("Починаю міграцію даних з MongoDB в PostgreSQL.")
    postgres_cursor = None
    postgres_conn = None
    mongo_client = None  # Додано для закриття з'єднання

    try:
        # Підключення до MongoDB
        mongo_client = MongoClient(
            "mongodb+srv://barabaca:280992@cluster0.xik54.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        )
        mongo_db = mongo_client["mydb_scrap"]
        mongo_collection = mongo_db["quote"]

        # Підключення до PostgreSQL
        postgres_conn = create_postgres_connection("postgres://mr.green:280992@localhost:5432/dbhw101")
        if postgres_conn is not None:
            postgres_cursor = postgres_conn.cursor()

            # Створення таблиці, якщо вона не існує
            create_table_if_not_exists(postgres_cursor)

            # Підрахунок записів у MongoDB
            total_records = mongo_collection.count_documents({})
            logger.info(f"Знайдено {total_records} записів у MongoDB.")

            unique_tags = set()  # Використання множини для зберігання унікальних тегів

            records = mongo_collection.find()
            for record in records:
                tags = record.get('tags', [])  # Перевірка наявності тегів
                unique_tags.update(tags)  # Додаємо теги до множини

            # Вставка унікальних тегів в PostgreSQL
            for tag in unique_tags:
                try:
                    postgres_cursor.execute(
                        "INSERT INTO quotes_tag(name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                        (tag,)
                    )
                    postgres_conn.commit()  # Збереження транзакції

                except Exception as e:
                    logger.error(f"Помилка під час вставки тегу '{tag}': {e}")
                    postgres_conn.rollback()  # Відкатити транзакцію у разі помилки

            logger.info("Міграція даних завершена.")
        else:
            logger.error("Не вдалося встановити з'єднання з PostgreSQL. Міграція не може бути завершена.")

    except Exception as e:
        logger.error(f"Помилка під час міграції: {e}")

    finally:
        # Закриття курсорів і з'єднань
        if postgres_cursor:
            postgres_cursor.close()
        if postgres_conn:
            postgres_conn.close()
        if mongo_client:
            mongo_client.close()


if __name__ == "__main__":
    migrate_data()
