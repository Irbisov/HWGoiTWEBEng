from mongoengine import Document, StringField, EmailField, BooleanField


class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True)
    phone_number = StringField(required=False)  # Додаткове поле для телефону
    sent = BooleanField(default=False)  # Логічне поле для статусу відправлення
    preferred_method = StringField(choices=["email", "sms"], required=True)  # Метод надсилання
