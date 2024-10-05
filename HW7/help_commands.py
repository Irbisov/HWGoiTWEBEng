def help_commands():
    help_text = """
    Список команд:

    Студенти:
    - create student --first_name Ім'я --last_name Прізвище --email Електронна пошта --age Вік --address Адреса --phone Телефон --gender_id ID Гендеру --group_id ID Групи --birth_date Дата народження
    - list student
    - read student --student_id ID
    - update student --student_id ID [--first_name] [--last_name] [--email] [--age] [--address] [--phone] [--gender_id] [--group_id] [--birth_date]
    - delete student --student_id ID

    Вчителі:
    - create teacher --first_name Ім'я --last_name Прізвище --email Електронна пошта --phone Телефон --address Адреса --birth_date Дата народження --age Вік --subject_id ID Предмета --gender_id ID Гендеру
    - list teacher
    - read teacher --teacher_id ID
    - update teacher --teacher_id ID [--first_name] [--last_name] [--email] [--phone] [--address] [--birth_date] [--age] [--subject_id] [--gender_id]
    - delete teacher --teacher_id ID

    Групи:
    - create group --group_name Назва
    - list group
    - read group --group_id ID
    - update group --group_id ID --group_name Назва
    - delete group --group_id ID

    Гендер:
    - create gender --gender Назва
    - list gender
    - read gender --gender_id ID
    - update gender --gender_id ID --gender Назва
    - delete gender --gender_id ID

    Предмети:
    - create subject --subject_name Назва
    - list subject
    - read subject --subject_id ID
    - update subject --subject_id ID --subject_name Назва
    - delete subject --subject_id ID

    Оцінки:
    - create mark --grade Оцінка --student_id ID студента --subject_id ID предмета --date Дата
    - list mark
    - read mark --mark_id ID
    - update mark --mark_id ID --grade Оцінка
    - delete mark --mark_id ID

    Загальні:
    - help
    """
    return help_text
