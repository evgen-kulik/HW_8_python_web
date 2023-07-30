"""
Передача даних (зі створенням колекцій autor та quote) до БД hw_08
з файлів authors.json та quotes.json. Опис моделей виконано в models.py.
"""


from models import Author, Quote
import json


if __name__ == "__main__":
    # прочитаємо .json
    with open("authors.json", "r", encoding="utf-8") as fh:
        data_authors = json.load(fh)
    with open("quotes.json", "r", encoding="utf-8") as fh:
        data_quotes = json.load(fh)

    # запишемо дані в БД (.save())
    author_1 = Author(
        fullname=data_authors[0]["fullname"],
        born_date=data_authors[0]["born_date"],
        born_location=data_authors[0]["born_location"],
        description=data_authors[0]["description"],
    ).save()
    author_2 = Author(
        fullname=data_authors[1]["fullname"],
        born_date=data_authors[1]["born_date"],
        born_location=data_authors[1]["born_location"],
        description=data_authors[1]["description"],
    ).save()

    for i in data_quotes:
        if i["author"] == author_1.fullname:
            quote = Quote(tags=i["tags"], author=author_1, quote=i["quote"]).save()
        else:
            quote = Quote(tags=i["tags"], author=author_2, quote=i["quote"]).save()
