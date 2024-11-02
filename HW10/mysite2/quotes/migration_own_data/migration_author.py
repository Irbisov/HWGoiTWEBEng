import logging
from pymongo import MongoClient
import psycopg2

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


def get_or_create_author(cursor, author_name, birthdate, bio):
    """Функція для отримання або створення автора."""
    try:
        # Перевіряємо, чи існує автор
        cursor.execute(
            "SELECT id FROM quotes_author WHERE name = %s",
            (author_name,)
        )
        result = cursor.fetchone()
        if result:
            logger.info(f"Автор '{author_name}' вже існує з ID {result[0]}.")
            return result[0]  # Повертаємо існуючий ID

        # Якщо автора немає, створюємо нового
        cursor.execute(
            "INSERT INTO quotes_author (name, birthdate, bio) VALUES (%s, %s, %s) RETURNING id",
            (author_name, birthdate, bio)
        )
        author_id = cursor.fetchone()[0]
        logger.info(f"Автор '{author_name}' успішно доданий з ID {author_id}.")
        return author_id

    except Exception as e:
        logger.error(f"Помилка при отриманні або створенні автора '{author_name}': {e}")
        return None

# Зміна в основній функції міграції
def migrate_data():
    """Функція для міграції даних з MongoDB в PostgreSQL."""
    logger.info("Починаю міграцію даних з MongoDB в PostgreSQL.")
    postgres_cursor = None
    postgres_conn = None
    mongo_client = None

    try:
        mongo_client = MongoClient(
            "mongodb+srv://barabaca:280992@cluster0.xik54.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        )
        mongo_db = mongo_client["mydb_scrap"]
        mongo_collection = mongo_db["author"]

        postgres_conn = create_postgres_connection("postgres://mr.green:280992@localhost:5432/dbhw101")
        if postgres_conn is not None:
            postgres_cursor = postgres_conn.cursor()

            total_records = mongo_collection.count_documents({})
            logger.info(f"Знайдено {total_records} записів у MongoDB.")

            records = mongo_collection.find()
            for record in records:
                try:
                    author_name = record.get('name')
                    birthdate = record.get('birthdate')
                    bio = record.get('bio')

                    if author_name is None:
                        logger.warning(f"Пропускаю запис через відсутність імені автора: {record}")
                        continue

                    # Викликаємо функцію для отримання або створення автора
                    author_id = get_or_create_author(postgres_cursor, author_name, birthdate, bio)

                    # Далі можна додавати цитати, якщо це необхідно

                    postgres_conn.commit()  # Фіксуємо зміни

                except Exception as e:
                    logger.error(f"Помилка під час обробки запису {record}: {e}")
                    postgres_conn.rollback()  # Відкочуємо зміни у випадку помилки

            logger.info("Міграція даних завершена.")
        else:
            logger.error("Не вдалося встановити з'єднання з PostgreSQL. Міграція не може бути завершена.")

    except Exception as e:
        logger.error(f"Помилка під час міграції: {e}")

    finally:
        if postgres_cursor:
            postgres_cursor.close()
        if postgres_conn:
            postgres_conn.close()
        if mongo_client:
            mongo_client.close()


if __name__ == "__main__":
    migrate_data()
