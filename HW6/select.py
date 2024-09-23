import logging

from psycopg2 import DatabaseError

from connection import create_connection

sql_expression_all = "SELECT * FROM students WHERE student_id = %s"
sql_expression_custom_field = """
        select student_id, first_name, age
        from students
        where age > 30
        order by first_name, age desc
        limit 10;
    """
sql_expression_regex = """
    select first_name from students where first_name similar to '%(ma|am)%' limit 100;
    """
# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
query_1 = """
    SELECT s.first_name, s.last_name, ROUND(AVG(m.grade), 2) AS average_grade
    FROM students s
    JOIN marks m ON s.student_id = m.student_id
    GROUP BY s.student_id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
# 2. Знайти студента із найвищим середнім балом з певного предмета через айді предемета від 1 до 30.
query_2 = """
    SELECT s.first_name, s.last_name, ROUND(AVG(m.grade), 2) AS average_grade
    FROM students s
    JOIN marks m ON s.student_id = m.student_id
    JOIN teachers t ON m.teacher_id = t.teachers_id
    WHERE t.subject_id = %s  -- Параметр для предмета
    GROUP BY s.student_id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
# 3. Знайти середній бал у групах з певного предмета.
query_3 = """
    SELECT grp.group_name AS group_name, ROUND(AVG(m.grade), 2) AS average_grade
    FROM marks m
    JOIN students s ON m.student_id = s.student_id
    JOIN groups grp ON s.group_id = grp.group_id
    JOIN teachers t ON m.teacher_id = t.teachers_id
    WHERE t.subject_id = %s  -- Параметр для предмета
    GROUP BY grp.group_id;
    """
# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
query_4 = """
    SELECT ROUND(AVG(grade),2) AS average_grade FROM marks;
    """
# 5. Знайти які курси читає певний викладач.
query_5 = """
    SELECT subj.subjects
    FROM subject subj
    JOIN teachers t ON subj.subject_id = t.subject_id
    WHERE t.first_name = %s 
    AND t.last_name = %s;  -- Параметри для викладача
    """
# 6. Знайти список студентів у певній групі.
query_6 = """
    SELECT s.first_name, s.last_name
    FROM students s
    JOIN groups grp ON s.group_id = grp.group_id
    WHERE grp.group_name = %s;  -- Параметр для назви групи
    """
# 7. Знайти оцінки студентів у окремій групі з певного предмета.
query_7 = """
    SELECT s.first_name, s.last_name, m.grade
    FROM marks m
    JOIN students s ON m.student_id = s.student_id
    JOIN groups grp ON s.group_id = grp.group_id
    JOIN teachers t ON m.teacher_id = t.teachers_id
    WHERE grp.group_name = %s 
    AND t.subject_id = %s;  -- Параметри для групи та  індекса предмета
    """
# 8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
query_8 = """
    SELECT ROUND(AVG(grade),2) AS average_grade
    FROM marks m
    JOIN teachers t ON m.teacher_id = t.subject_id
    WHERE t.first_name = %s 
    AND t.last_name = %s;  -- Параметри для викладача
    """
# 9. Знайти список курсів, які відвідує студент.
query_9 = """
    SELECT t.subject_id
    FROM marks m
    JOIN teachers t ON m.teacher_id = t.teachers_id
    WHERE m.student_id = %s;  -- Параметр для id студента
    """
# 10. Список курсів, які певному студенту читає певний викладач.
query_10 = """
    SELECT t.subject_id
    FROM marks m
    JOIN teachers t ON m.teacher_id = t.teachers_id
    WHERE m.student_id = %s 
    AND t.first_name = %s 
    AND t.last_name = %s;  -- Параметри для студента та викладача
    """
# 11. Середній бал, який певний викладач ставить певному студентові.
query_11 = """
    SELECT ROUND(AVG(grade),2) AS average_grade
    FROM marks m
    JOIN teachers t ON m.teacher_id = t.teachers_id
    WHERE m.student_id = %s 
    AND t.first_name = %s 
    AND t.last_name = %s;  -- Параметри для студента та викладача
    """
# 12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
query_12 = """
    SELECT s.first_name, s.last_name, m.grade
    FROM marks m
    JOIN students s ON m.student_id = s.student_id
    JOIN groups grp ON s.group_id = grp.group_id
    JOIN teachers t ON m.teacher_id = t.teachers_id
    WHERE grp.group_name = %s 
    AND t.subject_id = %s 
    AND m.date = (
    SELECT MAX(date) 
    FROM marks 
    WHERE teacher_id = t.teachers_id 
    AND student_id IN (
    SELECT student_id 
    FROM students 
    WHERE group_id = grp.group_id)
    );"""

if __name__ == '__main__':
    try:
        with create_connection() as conn:
            if conn is not None:
                cur = conn.cursor()
                try:
                    # cur.execute(query_1)
                    # cur.execute(query_2, (1,))
                    # cur.execute(query_3, (1,))
                    # cur.execute(query_4)
                    # cur.execute(query_5, ('Calvin','Richardson',))
                    # cur.execute(query_6,('engineer',))
                    # cur.execute(query_7, ('engineer', 1))
                    # cur.execute(query_8,('Kristen','Taylor'))
                    # cur.execute(query_9, (1,))
                    # cur.execute(query_10, (1, 'Kristen', 'Taylor'))
                    # cur.execute(query_11, (1, 'Kristen', 'Taylor'))
                    cur.execute(query_12, ('engineer', 3))
                    # cur.execute(sql_expression_all, (4, ))
                    # cur.execute(sql_expression_custom_field)
                    # cur.execute(sql_expression_regex)
                    # print(cur.fetchone())
                    print(cur.fetchall())
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
