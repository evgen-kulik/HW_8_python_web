"""
Пошук цитат за тегом, за ім'ям автора або набором тегів.
Скрипт виконується в нескінченному циклі і за допомогою звичайного оператора input приймає команди у
наступному форматі - команда: значення.
Приклад:
name: Steve Martin — знайти та повернути список всіх цитат автора Steve Martin;
tag:life — знайти та повернути список цитат для тегу life;
tags:life,live — знайти та повернути список цитат, де є теги life або live
(примітка: без пробілів між тегами life, live);
exit — завершити виконання скрипту.
Виведення результатів пошуку лише у форматі utf-8
"""


from models import Author, Quote
import redis  # для кешування
from redis_lru import RedisLRU  # для кешування


# напишемо скрипт для забезпечення функції кешування
client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache  # обгорнули в цей декоратор для кешування за допомогою redis
def search_by_name(name: str) -> list:
    """Знаходить і повертає список цитат автора за його ім'ям"""

    lst = []
    # __startswith - каже, що якщо fullname починається з name
    # (див. https://docs.mongoengine.org/guide/querying.html#string-queries)
    for author in Author.objects(fullname__startswith=name):
        for quote in Quote.objects(author=author.id):
            # to_mongo().to_dict() - приводить object до вигляду dict
            lst.append(quote.to_mongo().to_dict()["quote"].encode("utf-8"))
    return lst


@cache  # обгорнули в цей декоратор для кешування за допомогою redis
def search_by_tag(tag: str) -> list:
    """Знаходить і повертає список цитат для тегу"""

    lst = []
    for quote in Quote.objects(
        tags__startswith=tag
    ):  # тут чомусь цей метод не працює для неповного тегу
        # to_mongo().to_dict() - приводить object до вигляду dict
        lst.append(quote.to_mongo().to_dict()["quote"].encode("utf-8"))
    return lst


def search_by_tags(tags: str) -> list:
    """Знаходить і повертає список цитат де є перелічені теги (примітка: без пробілів між тегами)"""

    lst = []
    list_of_tags = tags.split(",")  # парсимо введені теги
    for i in list_of_tags:
        for quote in Quote.objects(tags=i):
            # to_mongo().to_dict() - приводить object до вигляду dict
            lst.append(quote.to_mongo().to_dict()["quote"].encode("utf-8"))
    return lst


if __name__ == "__main__":
    command = str(input('Enter your command for research (to finish enter "exit"): '))
    while command != "exit":
        if command[:4] == "name":
            result = search_by_name(command[6:])
            print(result)
        elif command[:4] == "tag:":
            result = search_by_tag(command[4:])
            print(result)
        elif command[:4] == "tags":
            result = search_by_tags(command[5:])
            print(result)
        command = str(input("Enter your command for research: "))
