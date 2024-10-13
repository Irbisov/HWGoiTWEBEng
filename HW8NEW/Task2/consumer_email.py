import pika
from models import Contact
from connect_to_mongo import connect_mongo

connect_mongo()


def send_email(contact):
    # Функція-заглушка для надсилання email
    print(f"Email надіслано на адресу: {contact.email}")


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.sent:
        send_email(contact)
        contact.sent = True
        contact.save()
        print(f"Email контакт {contact.fullname} оброблено.")


# Налаштування RabbitMQ
credentials = pika.PlainCredentials('user', 'password')  # Використовуйте свої облікові дані
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)

channel = connection.channel()

channel.queue_declare(queue='email_queue')

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Очікування email повідомлень. Для виходу натисніть CTRL+C')
channel.start_consuming()
