from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from faker import Faker
from Random_date import random_date
import random
from models import Student, Group, Teacher, Subject, Mark, Gender, Base

# Налаштовуємо підключення до бази даних
DATABASE_URL = "postgresql://mr.green:280992@localhost:5433/dbhw7"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Створюємо екземпляр Faker для генерації випадкових даних
fake = Faker()


# Функція для заповнення бази даних
def seed_database():
    genders = [Gender(gender="male"), Gender(gender="female")]
    session.add_all(genders)
    session.commit()

    # Створення груп
    groups = [Group(group_name=f"navigation"), Group(group_name=f"engineer"), Group(group_name=f"electric"),
              Group(group_name=f"workers port")]
    session.add_all(groups)
    session.commit()

    marine_academy_subjects = [
        "Navigation", "Marine Engineering", "Maritime Law", "Ship Management", "Seamanship",
        "Maritime Safety", "Oceanography", "Marine Electronics", "Cargo Handling and Stowage",
        "Ship Stability", "Marine Meteorology", "Environmental Protection", "Naval Architecture",
        "Shipboard Operations", "Radar Navigation", "Port Operations", "Marine Communication Systems",
        "Maritime Economics", "Global Maritime Distress and Safety Systems (GMDSS)", "Marine Surveying"
    ]

    # Створення викладачів
    teachers = []
    for _ in range(len(marine_academy_subjects)):
        teacher = Teacher(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            age=random.randint(30, 60),
            address=fake.address(),
            phone=fake.phone_number(),
            gender_id=random.choice(genders).gender_id,
            birth_date=fake.date_of_birth().strftime('%d-%m')
        )
        teachers.append(teacher)

    session.add_all(teachers)
    session.commit()  # Коміт для викладачів, щоб отримати їх id

    # Створення предметів
    subjects = []
    for i, subject_name in enumerate(marine_academy_subjects):
        subject = Subject(subjects=subject_name, teacher_id=teachers[i].teachers_id)  # Прив'язка до викладача
        subjects.append(subject)

    session.add_all(subjects)
    session.commit()

    # Створення студентів
    students = []
    for group_id in range(1, 5):  # 4 групи
        for _ in range(32):  # 32 студента на групу
            student = Student(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                age=random.randint(16, 33),
                address=fake.address(),
                phone=fake.phone_number(),
                group_id=group_id,
                gender_id=random.choice(genders).gender_id,
                birth_date=fake.date_of_birth().strftime('%d-%m')
            )
            students.append(student)

    session.add_all(students)
    session.commit()

    # Створення оцінок
    marks = []
    for student in students:
        for _ in range(random.randint(10, 20)):  # До 20 оцінок для кожного студента
            mark = Mark(
                student_id=student.student_id,
                subject_id=random.choice(subjects).subject_id,
                grade=random.randint(0, 12),
                date=random_date().strftime('%d-%m-%Y')
            )
            marks.append(mark)

    session.add_all(marks)
    session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    seed_database()

    print("База даних успішно заповнена випадковими даними!")
