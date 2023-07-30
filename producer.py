import pika

from model_of_contact import Contact
from faker import Faker


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange="task_mock", exchange_type="direct")
channel.queue_declare(queue="task_queue", durable=True)
# durable=True для збереження даних при нештатних ситуаціях, але знижує швидкість
channel.queue_bind(exchange="task_mock", queue="task_queue")


def create_fake_сontact():
    """Генерує фейковий контакт та одразу записує його в БД hw_08.
    Дані про БД прописано в models_of_contact.py"""

    fake = Faker()
    contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        address=fake.address(),
    ).save()  # logic_field установлен по дефолту False
    return contact


def main():
    # згенеруємо фейкові контакти
    for i in range(5):
        fake_contact = create_fake_сontact()  # контакт одразу записується до БД hw_08
        message = str(fake_contact.id)  # автоматичне id з БД
        # Поміщаємо у чергу RabbitMQ повідомлення message
        channel.basic_publish(
            exchange="task_mock",
            routing_key="task_queue",
            body=message.encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        print(" [x] Sent %r" % message)
    connection.close()


if __name__ == "__main__":
    main()
