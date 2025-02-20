#!/bin/python
import timeit


def loop(emails: list[str]):
    result = []
    for email in emails:
        if email.endswith("@gmail.com"):
            result.append(email)
    return result


def list_comprehension(emails: list[str]):
    result = [email for email in emails if email.endswith("@gmail.com")]
    return result


def main():
    emails = [
        "john@gmail.com",
        "james@gmail.com",
        "alice@yahoo.com",
        "anna@live.com",
        "philipp@gmail.com",
    ] * 5
    num = 90000000
    enum = loop(emails)
    comp = list_comprehension(emails)
    enum_time = timeit.timeit(lambda: enum, number=num)
    comp_time = timeit.timeit(lambda: comp, number=num)
    if enum_time >= comp_time:
        print("it is better to use a list comprehension")
        print(f"{comp_time} vs {enum_time}")
    else:
        print("it is better to use a loop")
        print(f"{enum_time} vs {comp_time}")


if __name__ == "__main__":
    main()
