"""
Описує модель контакту для наповнення БД hw_08.
На основі моделі producer.py генерує певну кількість фейкових контактів та записує їх у БД.
"""


from mongoengine import *


uri = "mongodb+srv://goitlearn:goit_web_db_mongodb@cluster0.sgtae2n.mongodb.net/hw_08?retryWrites=true&w=majority"
# обов'язково вказати 'host='
connect(host=uri, ssl=True)


# Описуємо колекцію Contact
class Contact(Document):
    fullname = StringField(max_length=50)
    email = StringField(max_length=50)
    address = StringField()
    tel_number = StringField(max_length=50)
    shipping = StringField(max_length=10)  # спосіб відправлення SMS або email
    logic_field = BooleanField(
        default=False
    )  # додаткове, означає, що повідомлення контакту не надіслано і повинно стати True, коли буде відправлено
