from main import *


def test_commands():
    # Створення
    print("Створення записів:")
    # create_gender("Чоловік")
    # create_gender("Жінка")
    create_group("Група 1")
    create_group("Група 2")
    create_subject("Математика",1)
    create_subject("Фізика", 2)
    create_student("Іван", "Іваненко", "ivan@example.com", 20, "Київ", "1234567890", 1, 1, "01-01")
    create_student("Олена", "Петренко", "elena@example.com", 21, "Львів", "0987654321", 2, 2, "02-02")
    create_teacher("Олександр", "Сидоренко", "alexander@example.com", "0676543210", "Харків", "03-03", 39, 1)
    create_mark(5.0, 1, 1, "2023-05-10")
    create_mark(4.0, 5, 5, "2023-05-12")

    # # Читання
    print("\nЧитання записів:")
    read_student(1)
    read_student(3)
    read_teacher(1)
    read_subject(1)
    read_group(1)
    read_gender(1)
    read_mark(1)
    #
    # # Оновлення
    print("\nОновлення записів:")
    update_student(1, "Іван", "Іваненко", "ivan_new@example.com", 21, "Київ", "1234567890", 1, 1, "2003-01-01")
    update_teacher(1, "Олександр", "Сидоренко", "alexander_new@example.com", "0676543210", "Харків", "1985-03-03", 40,
                   1)
    update_group(1, "Група 1 нова")
    update_mark(5, 5.0, 1, 1, "2023-05-10")
    # update_gender(1, "Чоловік")
    update_subject(1, "Математика нова")
    #
    print("\nПісля оновлення:")
    read_student(1)
    read_teacher(1)
    read_group(1)
    read_mark(1)
    read_gender(1)
    read_subject(1)
    # # Видалення
    print("\nВидалення записів:")
    delete_mark(4)
    delete_student(56)
    #
    print("\nПісля видалення:")
    read_student(1)
    read_student(2)  # Потрібно буде повернути None
    read_mark(1)  # Потрібно буде повернути None


# Виклик тестування
if __name__ == "__main__":
    test_commands()
