import logging
from psycopg2 import DatabaseError
from connection import create_connection

# Налаштування базового логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_table(conn, sql_expression):
    """
    Створює таблицю у базі даних за допомогою SQL-запиту.

    Параметри:
        conn (psycopg2.Connection): з'єднання з базою даних.
        sql_expression (str): SQL-запит для створення таблиці.
    """
    c = conn.cursor()
    try:
        logger.info("Виконання SQL-запиту для створення таблиці...")
        c.execute(sql_expression)
        conn.commit()
        logger.info("Таблицю успішно створено.")
    except DatabaseError as err:
        logger.error(f"Помилка під час створення таблиці: {err}")
        conn.rollback()
    finally:
        c.close()


if __name__ == '__main__':
    sql_expression = """CREATE TABLE IF NOT EXISTS teachers (
        teachers_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        age INT CHECK (age >= 0),
        address VARCHAR(200),
        phone VARCHAR(50),
        subject_id INT REFERENCES subject(subject_id),
        gender_id INT REFERENCES gender_id(gender_id),
        birth_date VARCHAR(50) NOT NULL
        
    );"""

    try:
        with create_connection() as conn:
            if conn is not None:
                logger.info("Створення таблиці у базі даних...")
                create_table(conn, sql_expression)
            else:
                logger.error("Не вдалося створити з'єднання з базою даних.")
    except RuntimeError as err:
        logger.error(f"Помилка під час створення з'єднання: {err}")
