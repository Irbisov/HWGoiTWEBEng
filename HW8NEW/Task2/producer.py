import random
from faker import Faker
from models import Contact
from connect_to_mongo import connect_mongo
import pika

connect_mongo()
fake = Faker()

# Налаштування RabbitM

credentials = pika.PlainCredentials('user', 'password')  # Використовуйте свої облікові дані
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)

channel = connection.channel()

# Створення черги
channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')


def generate_fake_contact():
    fullname = fake.name()
    email = fake.email()
    phone_number = fake.phone_number()
    preferred_method = random.choice(["email", "sms"])

    contact = Contact(fullname=fullname, email=email, phone_number=phone_number, preferred_method=preferred_method)
    contact.save()
    return contact


for _ in range(10):  # Генеруємо 10 контактів
    contact = generate_fake_contact()
    message = str(contact.id)  # Використовуємо ObjectID
    if contact.preferred_method == "email":
        channel.basic_publish(exchange='', routing_key='email_queue', body=message)
    else:
        channel.basic_publish(exchange='', routing_key='sms_queue', body=message)

print("Всі контакти надіслано у чергу.")
connection.close()
