import argparse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Student, Mark, Subject, Group, Teacher, Gender
from help_commands import help_commands
from tabulate import tabulate
from functools import wraps
from datetime import datetime

# Налаштовуємо підключення до бази даних
DATABASE_URL = "postgresql://mr.green:280992@localhost:5433/dbhw7"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


# Декоратор для управління сесіями
def session_manager(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = Session()
        try:
            return func(session, *args, **kwargs)
        except Exception as e:
            print(f"Сталася помилка: {e}")
        finally:
            session.close()

    return wrapper


# Валідація дати
def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Неправильний формат дати: {date_str}. Використовуйте YYYY-MM-DD.")
        return None


# CRUD операції для Gender
@session_manager
def create_gender(session, gender):
    new_gender = Gender(gender=gender)
    session.add(new_gender)
    session.commit()
    print(f"Гендера '{gender}' створено")


@session_manager
def list_genders(session):
    genders = session.query(Gender).all()
    table = [[g.gender_id, g.gender] for g in genders]
    print(tabulate(table, headers=["ID", "Гендер"]))


@session_manager
def read_gender(session, gender_id):
    gender = session.query(Gender).filter_by(gender_id=gender_id).first()
    if gender:
        print(f"Гендер з ID {gender_id}: {gender.gender}")
    else:
        print(f"Гендер з ID {gender_id} не знайдений")


@session_manager
def update_gender(session, gender_id, gender):
    g = session.query(Gender).filter_by(gender_id=gender_id).first()
    if g:
        g.gender = gender
        session.commit()
        print(f"Гендер з ID {gender_id} оновлено")
    else:
        print(f"Гендер з ID {gender_id} не знайдений")


@session_manager
def delete_gender(session, gender_id):
    gender = session.query(Gender).filter_by(gender_id=gender_id).first()
    if gender is None:
        print(f"Гендер з ID {gender_id} не знайдений")
        return
    session.delete(gender)
    session.commit()
    print(f"Гендер з ID {gender_id} успішно видалено")


# CRUD операції для Subject
@session_manager
def create_subject(session, subject_name, teachers_id=None):
    new_subject = Subject(subjects=subject_name, teacher_id=teachers_id)
    session.add(new_subject)
    session.commit()
    print(f"Предмет '{subject_name}' створено")


@session_manager
def list_subjects(session):
    subjects = session.query(Subject).all()
    table = [[s.subject_id, s.subjects] for s in subjects]
    print(tabulate(table, headers=["ID", "Назва предмета"]))


@session_manager
def read_subject(session, subject_id):
    subject = session.query(Subject).filter_by(subject_id=subject_id).first()
    if subject:
        print(f"Предмет з ID {subject_id}: {subject.subjects}")
    else:
        print(f"Предмет з ID {subject_id} не знайдений")


@session_manager
def update_subject(session, subject_id, subject_name):
    s = session.query(Subject).filter_by(subject_id=subject_id).first()
    if s:
        s.subjects = subject_name
        session.commit()
        print(f"Предмет з ID {subject_id} оновлено")
    else:
        print(f"Предмет з ID {subject_id} не знайдений")


@session_manager
def delete_subject(session, subject_id):
    s = session.query(Subject).filter_by(subject_id=subject_id).first()
    if s:
        session.delete(s)
        session.commit()
        print(f"Предмет з ID {subject_id} видалено")
    else:
        print(f"Предмет з ID {subject_id} не знайдений")


# CRUD операції для Group
@session_manager
def create_group(session, group_name):
    new_group = Group(group_name=group_name)
    session.add(new_group)
    session.commit()
    print(f"Група '{group_name}' створена")


@session_manager
def list_groups(session):
    groups = session.query(Group).all()
    table = [[g.group_id, g.group_name] for g in groups]
    print(tabulate(table, headers=["ID", "Назва групи"]))


@session_manager
def read_group(session, group_id):
    group = session.query(Group).filter_by(group_id=group_id).first()
    if group:
        print(f"Група з ID {group_id}: {group.group_name}")
    else:
        print(f"Група з ID {group_id} не знайдена")


@session_manager
def update_group(session, group_id, group_name):
    g = session.query(Group).filter_by(group_id=group_id).first()
    if g:
        g.group_name = group_name
        session.commit()
        print(f"Група з ID {group_id} оновлена")
    else:
        print(f"Група з ID {group_id} не знайдена")


@session_manager
def delete_group(session, group_id):
    g = session.query(Group).filter_by(group_id=group_id).first()
    if g:
        session.delete(g)
        session.commit()
        print(f"Група з ID {group_id} видалена")
    else:
        print(f"Група з ID {group_id} не знайдена")


# CRUD операції для Mark
@session_manager
def create_mark(session, grade, student_id, subject_id, date):
    new_mark = Mark(grade=grade, student_id=student_id, subject_id=subject_id, date=date)
    session.add(new_mark)
    session.commit()
    print(f"Оцінка {grade} для студента з ID {student_id} створена")


@session_manager
def list_marks(session):
    marks = session.query(Mark).all()
    table = [[m.mark_id, m.student_id, m.subject_id, m.grade, m.date] for m in marks]
    print(tabulate(table, headers=["ID", "Студент ID", "Предмет ID", "Оцінка", "Дата"]))


@session_manager
def read_mark(session, mark_id):
    mark = session.query(Mark).filter_by(mark_id=mark_id).first()
    if mark:
        print(
            f"Оцінка з ID {mark_id}: Студент ID: {mark.student_id}, Предмет ID: {mark.subject_id}, Оцінка: {mark.grade}, Дата: {mark.date}")
    else:
        print(f"Оцінка з ID {mark_id} не знайдена")


@session_manager
def update_mark(session, mark_id, grade, student_id, subject_id, date_of):
    # Знайти запис за ID
    m = session.query(Mark).filter_by(mark_id=mark_id).first()

    if m:
        # Оновити відповідні поля
        m.grade = grade
        m.student_id = student_id
        m.subject_id = subject_id
        m.date_of = date_of

        # Зберегти зміни
        session.commit()
        print(f"Оцінка з ID {mark_id} оновлена")
    else:
        print(f"Оцінка з ID {mark_id} не знайдена")



@session_manager
def delete_mark(session, mark_id):
    m = session.query(Mark).filter_by(mark_id=mark_id).first()
    if m:
        session.delete(m)
        session.commit()
        print(f"Оцінка з ID {mark_id} видалена")
    else:
        print(f"Оцінка з ID {mark_id} не знайдена")


# CRUD операції для Student
@session_manager
def create_student(session, first_name, last_name, email, age, address, phone, gender_id, group_id, birth_date):
    if birth_date is None:
        return
    new_student = Student(
        first_name=first_name,
        last_name=last_name,
        email=email,
        age=age,
        address=address,
        phone=phone,
        gender_id=gender_id,
        group_id=group_id,
        birth_date=birth_date
    )
    session.add(new_student)
    session.commit()
    print(f"Студента {first_name} {last_name} створено")


@session_manager
def list_students(session):
    students = session.query(Student).all()
    table = [[s.student_id, s.first_name, s.last_name, s.email, s.age, s.address, s.phone, s.gender_id, s.group_id,
              s.birth_date] for s in students]
    print(tabulate(table,
                   headers=["ID", "Ім'я", "Прізвище", "Електронна пошта", "Вік", "Адреса", "Телефон", "Гендер ID",
                            "Група ID", "Дата народження"]))


@session_manager
def read_student(session, student_id):
    student = session.query(Student).filter_by(student_id=student_id).first()
    if student:
        print(
            f"Студент з ID {student_id}: {student.first_name} {student.last_name}, email: {student.email}, вік: {student.age}")
    else:
        print(f"Студент з ID {student_id} не знайдений")


@session_manager
def update_student(session, student_id, first_name, last_name, email, age, city, phone, group_id, gender_id, birth_date):
    # Знайти запис за ID студента
    student = session.query(Student).filter_by(student_id=student_id).first()

    if student:
        # Оновлення полів студента
        student.first_name = first_name
        student.last_name = last_name
        student.email = email
        student.age = age
        student.city = city
        student.phone = phone
        student.group_id = group_id
        student.gender_id = gender_id
        student.birth_date = birth_date

        # Збереження змін
        session.commit()
        print(f"Студент з ID {student_id} оновлений")
    else:
        print(f"Студент з ID {student_id} не знайдений")



@session_manager
def delete_student(session, student_id):
    student = session.query(Student).filter_by(student_id=student_id).first()
    if student:
        session.delete(student)
        session.commit()
        print(f"Студент з ID {student_id} видалений")
    else:
        print(f"Студент з ID {student_id} не знайдений")


@session_manager
def list_teachers(session):
    teachers = session.query(Teacher).all()
    table = [[t.teachers_id, t.first_name, t.last_name, t.email, t.phone, t.gender_id, t.birth_date] for t in teachers]
    print(tabulate(table,
                   headers=["ID", "Ім'я", "Прізвище", "Електронна пошта", "Телефон", "Гендер ID", "Дата народження"]))


@session_manager
def read_teacher(session, teacher_id):
    teacher = session.query(Teacher).filter_by(teachers_id=teacher_id).first()
    if teacher:
        print(f"Вчитель з ID {teacher_id}: {teacher.first_name} {teacher.last_name}, email: {teacher.email}")
    else:
        print(f"Вчитель з ID {teacher_id} не знайдений")


@session_manager
def update_teacher(session, teacher_id, first_name, last_name, email, phone, address, birth_date, age, subject_id):
    # Знайти запис за ID вчителя
    teacher = session.query(Teacher).filter_by(teachers_id=teacher_id).first()

    if teacher:
        # Оновлення полів вчителя
        teacher.first_name = first_name
        teacher.last_name = last_name
        teacher.email = email
        teacher.phone = phone
        teacher.address = address
        teacher.birth_date = birth_date
        teacher.age = age
        teacher.subject_id = subject_id

        # Збереження змін
        session.commit()
        print(f"Вчитель з ID {teacher_id} оновлений")
    else:
        print(f"Вчитель з ID {teacher_id} не знайдений")



@session_manager
def delete_teacher(session, teacher_id):
    teacher = session.query(Teacher).filter_by(teacher_id=teacher_id).first()
    if teacher:
        session.delete(teacher)
        session.commit()
        print(f"Вчитель з ID {teacher_id} видалений")
    else:
        print(f"Вчитель з ID {teacher_id} не знайдений")


@session_manager
def create_teacher(session, first_name, last_name, email, phone, address, birth_date, age, gender_id):
    new_teacher = Teacher(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        address=address,
        birth_date=birth_date,
        age=age,
        gender_id=gender_id
    )
    session.add(new_teacher)
    session.commit()
    print(f"Вчителя {first_name} {last_name} створено")


def main():
    parser = argparse.ArgumentParser(description="Система управління студентами")

    parser.add_argument('-a', '--action', choices=['create', 'read', 'update', 'delete', 'list', 'help'],
                        help="Команда, яку потрібно виконати.", required=True)
    parser.add_argument('-t', '--type', choices=['student', 'gender', 'group', 'mark', 'subject', 'teacher'],
                        help='Тип об\'єкта.', required=True)

    # Додайте аргументи для кожного типу об\'єкта
    parser.add_argument('--subject_id', type=int, help='ID предмета вчителя')
    parser.add_argument('--teacher_id', type=int, help='ID вчителя')
    parser.add_argument('--first_name', type=str, help='Ім\'я персони')
    parser.add_argument('--last_name', type=str, help='Прізвище персони')
    parser.add_argument('--email', type=str, help='Email персони')
    parser.add_argument('--age', type=int, help='Вік персони')
    parser.add_argument('--address', type=str, help='Адреса персони')
    parser.add_argument('--phone', type=str, help='Телефон студента')
    parser.add_argument('--group_id', type=int, help='ID групи студента')
    parser.add_argument('--gender_id', type=int, help='ID гендера студента')
    parser.add_argument('--birth_date', type=str, help='Дата народження персони (DD-MM)')
    parser.add_argument('--student_id', type=int, help='ID студента')
    parser.add_argument('--gender', type=str, help='Гендер')
    parser.add_argument('--group_name', type=str, help='Назва групи')
    parser.add_argument('--mark_id', type=int, help='ID оцінки')
    parser.add_argument('--grade', type=float, help='Оцінка')
    parser.add_argument('--date', type=str, help='Дата оцінки (YYYY-MM-DD)')
    parser.add_argument('--subject_name', type=str, help='Назва предмета')

    args = parser.parse_args()

    if args.command == 'create':
        if args.type == 'student':
            create_student(args.first_name, args.last_name, args.email, args.age, args.address, args.phone,
                           args.group_id, args.gender_id, args.birth_date)
        elif args.type == 'gender':
            create_gender(args.gender)
        elif args.type == 'group':
            create_group(args.group_name)
        elif args.type == 'mark':
            create_mark(args.grade, args.student_id, args.subject_id, args.date)
        elif args.type == 'subject':
            create_subject(args.subject_name)
        elif args.type == 'teacher':
            create_teacher(args.first_name, args.last_name, args.email, args.phone, args.address, args.birth_date,
                           args.age, args.subject_id)

    elif args.command == 'list':
        if args.type == 'student':
            list_students()
        elif args.type == 'gender':
            list_genders()
        elif args.type == 'group':
            list_groups()
        elif args.type == 'mark':
            list_marks()
        elif args.type == 'subject':
            list_subjects()
        elif args.type == 'teacher':
            list_teachers()

    elif args.command == 'read':
        if args.type == 'student':
            read_student(args.student_id)
        elif args.type == 'gender':
            read_gender(args.gender_id)
        elif args.type == 'group':
            read_group(args.group_id)
        elif args.type == 'mark':
            read_mark(args.mark_id)
        elif args.type == 'subject':
            read_subject(args.subject_id)
        elif args.type == 'teacher':
            read_teacher(args.teacher_id)

    elif args.command == 'update':
        if args.type == 'student':
            update_student(args.student_id, args.first_name, args.last_name, args.email, args.age, args.address,
                           args.phone, args.group_id, args.gender_id, args.birth_date)
        elif args.type == 'gender':
            update_gender(args.gender_id, args.gender)
        elif args.type == 'group':
            update_group(args.group_id, args.group_name)
        elif args.type == 'mark':
            update_mark(args.mark_id, args.grade)
        elif args.type == 'subject':
            update_subject(args.subject_id, args.subject_name)
        elif args.type == 'teacher':
            update_teacher(args.teacher_id, args.first_name, args.last_name, args.email, args.phone, args.address,
                           args.birth_date, args.age, args.subject_id)

    elif args.command == 'delete':
        if args.type == 'student':
            delete_student(args.student_id)
        elif args.type == 'gender':
            delete_gender(args.gender_id)
        elif args.type == 'group':
            delete_group(args.group_id)
        elif args.type == 'mark':
            delete_mark(args.mark_id)
        elif args.type == 'subject':
            delete_subject(args.subject_id)
        elif args.type == 'teacher':
            delete_teacher(args.teacher_id)

    elif args.command == 'help':
        print(help_commands())


if __name__ == "__main__":
    main()
