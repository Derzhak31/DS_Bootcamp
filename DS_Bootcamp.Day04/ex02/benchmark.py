#!/bin/python
import sys
import timeit


def get_loop(emails: list[str]):
    result = []
    for email in emails:
        if email.endswith("@gmail.com"):
            result.append(email)
    return result


def get_list_comprehension(emails: list[str]):
    result = [email for email in emails if email.endswith("@gmail.com")]
    return result


def get_map(emails: list[str]):
    result = map(lambda x: x if x.endswith("@gmail.com") else None, emails)
    return list(result)


def get_filter(emails: list[str]):
    result = filter(lambda x: x.endswith("@gmail.com"), emails)
    return list(result)


def main(func_stmt: str, number: str):
    emails = [
        "john@gmail.com",
        "james@gmail.com",
        "alice@yahoo.com",
        "anna@live.com",
        "philipp@gmail.com",
    ] * 5
    if func_stmt not in ["loop", "list_comprehension", "map", "filter"]:
        raise Exception("Не верный аргумент - такой функции нет")
    if not number.isdigit():
        raise Exception("Второй аргумент не число")
    if int(number) < 1:
        raise Exception("Число должно быть >= 1")
    time = timeit.timeit(lambda: f"get_{func_stmt}(emails)", number=int(number))
    return time


if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            raise Exception("Не верное количество аргументов")
        else:
            func = sys.argv[1]
            num = sys.argv[2]
            print("%.9f" % main(func, num))
    except Exception as e:
        print(f"Ошибка: {e}")
