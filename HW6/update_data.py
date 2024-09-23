import logging
from faker import Faker
from psycopg2 import DatabaseError
from connection import create_connection

fake = Faker()

if __name__ == '__main__':

    # SQL-запит з оновленням дати народження для конкретного викладача
    sql_expression = "UPDATE teachers SET birth_date = %s WHERE teachers_id = %s"

    try:
        with create_connection() as conn:
            if conn is not None:
                cur = conn.cursor()
                try:
                    for teacher_id in range(1, 31):  # Припустимо, що у вас 31 викладач
                        birth_date = fake.date_of_birth().strftime('%d-%m')  # Формат повної дати
                        cur.execute(sql_expression, (birth_date, teacher_id))
                    conn.commit()
                except DatabaseError as err:
                    logging.error(err)
                    conn.rollback()
                finally:
                    cur.close()
            else:
                print('Error: can\'t create the database connection')
    except RuntimeError as err:
        logging.error(err)
