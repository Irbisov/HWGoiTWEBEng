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


def get_or_create_author(cursor, name, bio='NEW', birthdate="NEW"):
    """Функція для отримання author_id або створення нового автора."""
    try:
        cursor.execute("SELECT id FROM quotes_author WHERE name = %s", (name,))
        result = cursor.fetchone()

        if result:
            logger.info(f"Автор знайдений: {name}")
            return result[0]  # Повертає author_id
        else:
            cursor.execute(
                "INSERT INTO quotes_author (name, bio, birthdate) VALUES (%s, %s, %s) RETURNING id",
                (name, bio, birthdate)
            )
            author_id = cursor.fetchone()[0]
            logger.info(f"Автор створений: {name} з ID {author_id}")
            return author_id
    except Exception as e:
        logger.error(f"Помилка при створенні автора {name}: {e}")
        # Скасовуємо транзакцію, якщо сталася помилка
        cursor.connection.rollback()
        return None



def get_or_create_tag(cursor, name):
    """Функція для отримання id тегу або створення нового тегу."""
    try:
        cursor.execute("SELECT id FROM quotes_tag WHERE name = %s", (name,))
        result = cursor.fetchone()

        if result:
            logger.info(f"Тег знайдений: {name}")
            return result[0]
        else:
            cursor.execute("INSERT INTO quotes_tag (name) VALUES (%s) RETURNING id", (name,))
            tag_id = cursor.fetchone()[0]
            logger.info(f"Тег створено: {name} з ID {tag_id}")
            return tag_id
    except Exception as e:
        logger.error(f"Помилка при додаванні тегу {name}: {e}")
        return None


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
        mongo_collection = mongo_db["quote"]

        postgres_conn = create_postgres_connection("postgres://mr.green:280992@localhost:5432/dbhw101")
        if postgres_conn is not None:
            postgres_cursor = postgres_conn.cursor()

            total_records = mongo_collection.count_documents({})
            logger.info(f"Знайдено {total_records} записів у MongoDB.")

            records = mongo_collection.find()
            for record in records:
                try:
                    text = record.get('text')
                    author_name = record.get('author')
                    tags = record.get('tags', [])

                    if text is None or author_name is None:
                        logger.warning(f"Пропускаю запис, оскільки відсутні обов'язкові поля: {record}")
                        continue

                    author_id = get_or_create_author(postgres_cursor, author_name)

                    if author_id is None:
                        logger.warning(f"Пропускаю запис через помилку при створенні автора: {author_name}")
                        continue

                    postgres_cursor.execute(
                        "INSERT INTO quotes_quote (author_id, text) VALUES (%s, %s) RETURNING id",
                        (author_id, text)
                    )
                    quote_id = postgres_cursor.fetchone()[0]

                    for tag_name in tags:
                        tag_id = get_or_create_tag(postgres_cursor, tag_name)
                        if tag_id is not None:
                            postgres_cursor.execute(
                                "INSERT INTO quotes_quote_tags (quote_id, tag_id) VALUES (%s, %s)",
                                (quote_id, tag_id)
                            )

                    postgres_conn.commit()

                except Exception as e:
                    logger.error(f"Помилка під час обробки запису {record}: {e}")
                    postgres_conn.rollback()

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
