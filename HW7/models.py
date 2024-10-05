from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from contextlib import contextmanager
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Базовий клас для декларативних моделей
Base = declarative_base()


class Gender(Base):
    __tablename__ = 'gender'

    gender_id = Column(Integer, primary_key=True)
    gender = Column(String(10), nullable=False)

    # Взаємозв'язок з таблицею студентів і викладачів
    students = relationship("Student", back_populates="gender")
    teachers = relationship("Teacher", back_populates="gender")


class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(Integer, primary_key=True)
    group_name = Column(String(50), nullable=False)

    # Взаємозв'язок з таблицею студентів
    students = relationship("Student", back_populates="group")



class Mark(Base):
    __tablename__ = 'marks'

    mark_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    subject_id = Column(Integer, ForeignKey('subject.subject_id'))
    grade = Column(Integer, CheckConstraint('grade >= 0 AND grade <= 13'))  # Оцінка від 0 до 13
    date = Column(String(50), nullable=False)

    # Взаємозв'язки з таблицями студентів і викладачів
    student = relationship("Student", back_populates="marks")
    subject = relationship("Subject", back_populates="marks")


class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    age = Column(Integer, CheckConstraint('age >= 0'))
    address = Column(String(200))
    phone = Column(String(50))
    group_id = Column(Integer, ForeignKey('groups.group_id'))
    gender_id = Column(Integer, ForeignKey('gender.gender_id'))
    birth_date = Column(String(50), nullable=False)

    # Взаємозв'язки
    group = relationship("Group", back_populates="students")
    gender = relationship("Gender", back_populates="students")
    marks = relationship("Mark", back_populates="student")


class Subject(Base):
    __tablename__ = 'subject'

    subject_id = Column(Integer, primary_key=True)
    subjects = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.teachers_id'))  # Зовнішній ключ на teachers_id

    # Взаємозв'язок з викладачами
    teacher = relationship("Teacher", back_populates="subjects")  # Видалено foreign_keys
    marks = relationship("Mark", back_populates="subject")


class Teacher(Base):
    __tablename__ = 'teachers'

    teachers_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    age = Column(Integer, CheckConstraint('age >= 0'))
    address = Column(String(200))
    phone = Column(String(50))
    gender_id = Column(Integer, ForeignKey('gender.gender_id'))  # ForeignKey на гендер
    birth_date = Column(String(50), nullable=False)

    # Взаємозв'язки
    subjects = relationship("Subject", back_populates="teacher")  # Додано subjects
    gender = relationship("Gender", back_populates="teachers")


def init_db():
    DATABASE_URL = "postgresql://mr.green:280992@172.21.0.2:5432/dbhw7"
    engine = create_engine(DATABASE_URL, future=True)
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error in DB operation: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == '__main__':
    init_db()
