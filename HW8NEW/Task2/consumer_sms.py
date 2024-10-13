import pika
from models import Contact
from connect_to_mongo import connect_mongo

connect_mongo()


def send_sms(contact):
    # Функція-заглушка для надсилання SMS
    print(f"SMS надіслано на номер: {contact.phone_number}")


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()
    if contact and not contact.sent:
        send_sms(contact)
        contact.sent = True
        contact.save()
        print(f"SMS контакт {contact.fullname} оброблено.")


# Налаштування RabbitMQ

credentials = pika.PlainCredentials('user', 'password')  # Використовуйте свої облікові дані
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)

channel = connection.channel()

channel.queue_declare(queue='sms_queue')

channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print('Очікування SMS повідомлень. Для виходу натисніть CTRL+C')
channel.start_consuming()
