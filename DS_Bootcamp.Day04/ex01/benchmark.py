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


def get_map(emails: list[str]):
    result = map(lambda x: x if x.endswith("@gmail.com") else None, emails)
    return list(result)


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
    maps = get_map(emails)
    enum_time = timeit.timeit(lambda: enum, number=num)
    comp_time = timeit.timeit(lambda: comp, number=num)
    map_time = timeit.timeit(lambda: maps, number=num)
    times = sorted([enum_time, comp_time, map_time])
    if enum_time == times[0]:
        print("it is better to use a loop")
    elif comp_time == times[0]:
        print("it is better to use a list comprehension")
    elif map_time == times[0]:
        print("it is better to use a map")
    print(f"{times[0]} vs {times[1]} vs {times[2]}")


if __name__ == "__main__":
    main()
