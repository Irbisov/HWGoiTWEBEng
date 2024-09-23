import logging
import psycopg2
from contextlib import contextmanager
from psycopg2 import OperationalError, DatabaseError

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@contextmanager
def create_connection(host='localhost', database='my_database', user='mr.green', password='280992'):
    conn = None
    try:
        # Підключення до бази даних
        logger.info("Підключення до бази даних...")
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        yield conn
    except OperationalError as err:
        logger.error(f"Помилка підключення до бази даних: {err}")
        raise RuntimeError(f"Не вдалося підключитися до бази даних: {err}")
    finally:
        if conn is not None:
            conn.close()
            logger.info("З'єднання з базою даних закрито.")
