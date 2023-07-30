"""
Скрипт підключення до БД hw_08. Написаний для перевірки з'єднання з хмарною БД.
"""


# Далі іде скопійований блок коду з корективами з Connecting with MongoDB Driver
# -------------------------------------------
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://goitlearn:goit_web_db_mongodb@cluster0.sgtae2n.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# -------------------------------------------
db = client.hw_08


if __name__ == '__main__':
    # Виведемо те, що лежить в quote
    results = db.quote.find()
    # print(results)
    for result in results:
        print(result)