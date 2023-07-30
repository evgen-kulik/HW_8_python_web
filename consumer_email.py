import pika

import time

from bson import ObjectId

from connect import db

# ----блок коду для підключення до БД hw_08
from mongoengine import *
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://goitlearn:goit_web_db_mongodb@cluster0.sgtae2n.mongodb.net/hw_08?retryWrites=true&w=majority"
# обов'язково вказати 'host='
connect(host=uri, ssl=True)
client = MongoClient(uri, server_api=ServerApi("1"))

# ----

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel_email = connection.channel()

channel_email.queue_declare(queue="task_queue_email", durable=True)
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    message = body.decode()
    print(f" [x] Received {message}")
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # повертаємо (згенерований RabbitMQ) delivery_tag назад до RabbitMQ, говорячи,
    # що відправлення завершено вдало

    # імітуємо надсилання message на email (за умовами ДЗ)
    result_of_sending = send_message_to_email()
    # Змінемо логічне поле для контакту на True, перезапишемо його в БД
    if result_of_sending:
        db.contact.update_one(
            {"_id": ObjectId(message)}, {"$set": {"logic_field": True}}
        )
        print("contact.logic_field=True")


channel_email.basic_qos(prefetch_count=1)  # відправляє в consumer по одному завданню
# інакше всі завдання відправляться одразу одному consumer і він може лягти
channel_email.basic_consume(queue="task_queue_email", on_message_callback=callback)


def send_message_to_email():
    """Функція-заглушка, імітує надсилання message на email"""
    return True


if __name__ == "__main__":
    channel_email.start_consuming()
