import random
import logging
from faker import Faker
from random import randint
from psycopg2 import DatabaseError
from connection import create_connection

# Ініціалізація Faker і налаштування
fake = Faker()
COUNT = 30

# Генерація послідовності чисел від 1 до 30 і їх перемішування
subject_ids = list(range(1, 31))
random.shuffle(subject_ids)

# Ініціалізація лічильника для використання унікальних груп
subject_index = 0


def insert_data(conn, sql_expression):
    global subject_index  # Вказуємо, що використовуємо глобальну змінну
    cur = conn.cursor()
    used_emails = set()  # Зберігання вже використаних електронних адрес
    try:
        for _ in range(COUNT):
            while True:
                email = fake.email()
                if email not in used_emails:  # Перевірка на унікальність
                    used_emails.add(email)  # Додаємо до набору
                    break

            # Форматування дати народження
            birth_date = fake.date_of_birth().strftime('%Y-%m-%d')

            cur.execute(sql_expression, (
                fake.first_name()[:20], fake.last_name()[:20], email,
                fake.phone_number()[:20], birth_date))
        conn.commit()
    except DatabaseError as err:
        logging.error(err)
        conn.rollback()
    finally:
        cur.close()


if __name__ == '__main__':
    # SQL-запит для вставки даних
    sql_expression = """
    INSERT INTO contacts(
        first_name, last_name, email, phone, birthday
    ) VALUES(%s, %s, %s, %s, %s)
    """

    try:
        with create_connection() as conn:
            if conn is not None:
                insert_data(conn, sql_expression)
            else:
                print("Error: can't create the database connection")
    except RuntimeError as err:
        logging.error(err)
