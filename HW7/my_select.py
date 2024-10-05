from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from models import Student, Mark, Subject, Group, Teacher, Base


# Налаштовуємо підключення до бази даних
DATABASE_URL = "postgresql://mr.green:280992@localhost:5433/dbhw7"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    with Session() as session:
        results = session.query(
            Student.first_name,
            Student.last_name,
            func.avg(Mark.grade).label("average_grade")
        ).join(Mark).group_by(Student.student_id).order_by(func.avg(Mark.grade).desc()).limit(5).all()
    return results


def select_2(subject_id):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    with Session() as session:
        results = session.query(
            Student.first_name,
            Student.last_name,
            func.avg(Mark.grade).label("average_grade")
        ).join(Mark).filter(Mark.subject_id == subject_id).group_by(Student.student_id).order_by(
            func.avg(Mark.grade).desc()).first()
    return results


def select_3(subject_id):
    """Знайти середній бал у групах з певного предмета."""
    with Session() as session:
        results = session.query(
            Group.group_name,
            func.avg(Mark.grade).label("average_grade")
        ).select_from(Group).join(Student).join(Mark).filter(Mark.subject_id == subject_id).group_by(Group.group_id).all()
    return results



def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    with Session() as session:
        average_grade = session.query(func.avg(Mark.grade)).scalar()
    return round(average_grade, 2)  # Змінено на округлення до 2 знаків


def select_5(teacher_id):
    """Знайти які курси читає певний викладач."""
    with Session() as session:
        results = session.query(Subject.subjects).filter(Subject.teacher_id == teacher_id).all()
    return results


def select_6(group_id):
    """Знайти список студентів у певній групі."""
    with Session() as session:
        results = session.query(Student.first_name, Student.last_name).filter(Student.group_id == group_id).all()
    return results


def select_7(group_id, subject_id):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    with Session() as session:
        results = session.query(
            Student.first_name,
            Student.last_name,
            Mark.grade
        ).join(Group).join(Mark).filter(Group.group_id == group_id, Mark.subject_id == subject_id).all()
    return results


def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    with Session() as session:
        results = session.query(func.avg(Mark.grade)).join(Subject).filter(Subject.teacher_id == teacher_id).scalar()
    return round(results, 2)  # Змінено на округлення до 2 знаків


def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент."""
    with Session() as session:
        results = session.query(Subject.subjects).join(Mark).filter(Mark.student_id == student_id).distinct().all()
    return results


def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач."""
    with Session() as session:
        results = (
            session.query(Subject.subjects)
            .join(Mark, Mark.subject_id == Subject.subject_id)
            .join(Student, Student.student_id == Mark.student_id)
            .filter(Student.student_id == student_id, Subject.teacher_id == teacher_id)
            .all()
        )
    return results

def select_11(student_id, teacher_id):
    """Середній бал, який певний викладач ставить певному студентові."""
    with Session() as session:
        average_grade = session.query(func.avg(Mark.grade).label("average_grade")) \
            .join(Subject).join(Student) \
            .filter(Subject.teacher_id == teacher_id, Student.student_id == student_id) \
            .scalar()
    return round(average_grade, 2) if average_grade is not None else None


def select_12(group_id, subject_id):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    with Session() as session:
        # Знайдемо останню дату заняття
        last_date_subquery = session.query(func.max(Mark.date)) \
            .join(Student) \
            .filter(Student.group_id == group_id, Mark.subject_id == subject_id) \
            .scalar_subquery()  # Використання scalar_subquery()

        # Отримаємо оцінки студентів на останньому занятті
        results = session.query(
            Student.first_name,
            Student.last_name,
            Mark.grade
        ).join(Group).join(Mark) \
            .filter(Group.group_id == group_id, 
                    Mark.subject_id == subject_id,
                    Mark.date == last_date_subquery) \
            .all()
    return results

if __name__ == '__main__':
    print(1, select_1())
    print(2, select_2(1))
    print(3, select_3(1))
    print(4, select_4())
    print(5, select_5(1))
    print(6, select_6(1))
    print(7, select_7(1, 1))
    print(8, select_8(1))
    print(9, select_9(1))
    print(10, select_10(5, 11))
    print(11, select_11(5, 11))
    print(12, select_12(4, 11))
