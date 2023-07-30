import random

import pika

from model_of_contact_additional import Contact
from faker import Faker


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
# канал для відправлення смс
channel_sms = connection.channel()
channel_sms.exchange_declare(exchange="task_mock", exchange_type="direct")
channel_sms.queue_declare(queue="task_queue_sms", durable=True)  # "task_queue_sms" - назва черги
# durable=True для збереження даних при нештатних ситуаціях, але знижує швидкість
channel_sms.queue_bind(exchange="task_mock", queue="task_queue_sms")

# канал для відправлення email
channel_email = connection.channel()
channel_email.exchange_declare(exchange="task_mock", exchange_type="direct")
channel_email.queue_declare(queue="task_queue_email", durable=True)  # "task_queue_email" - назва черги
# durable=True для збереження даних при нештатних ситуаціях, але знижує швидкість
channel_email.queue_bind(exchange="task_mock", queue="task_queue_email")



def create_fake_сontact():
    """Генерує фейковий контакт та одразу записує його в БД hw_08.
    Дані про БД прописано в models_of_contact.py"""

    fake = Faker()
    contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        address=fake.address(),
        tel_number=fake.phone_number(),
        shipping=random.choice(['SMS', 'email'])
    ).save()  # logic_field установлен по дефолту False
    return contact


def main():
    # згенеруємо фейкові контакти
    for i in range(5):
        fake_contact = create_fake_сontact()  # контакт одразу записується до БД hw_08
        message = str(fake_contact.id)  # автоматичне id з БД

        # Поміщаємо у чергу SMS-чергу та email-чергу RabbitMQ повідомлення message
        if fake_contact.shipping == 'SMS':
            channel_sms.basic_publish(
                exchange="task_mock",
                routing_key="task_queue_sms",
                body=message.encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )
            print(" [x] Sent by SMS %r" % message)
        elif fake_contact.shipping == 'email':
            channel_email.basic_publish(
                exchange="task_mock",
                routing_key="task_queue_email",
                body=message.encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )
            print(" [x] Sent by email %r" % message)
    connection.close()


if __name__ == "__main__":
    main()
