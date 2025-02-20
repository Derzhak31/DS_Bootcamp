#!/bin/python
import sys
import timeit
from functools import reduce


def get_loop(steps: int):
    sum = 0
    for i in range(1, steps + 1):
        sum += i * i
    return sum


def get_reduce(steps: int):
    result = reduce(
        lambda acc, step: acc + step * step, [step for step in range(1, steps + 1)], 0
    )
    return result


def main(func_stmt: str, number: str, steps: str):
    if func_stmt not in ["loop", "reduce"]:
        raise Exception("Не верный аргумент - такой функции нет")
    if not number.isdigit() or not steps.isdigit():
        raise Exception("Второй и третий аргументы должны быть числом")
    if int(number) < 1 or int(steps) < 1:
        raise Exception("Второй и третий аргументы должны быть >= 1")
    time = timeit.timeit(lambda: f"get_{func_stmt}(int(steps))", number=int(number))
    return time


if __name__ == "__main__":
    try:
        if len(sys.argv) != 4:
            raise Exception("Не верное количество аргументов")
        else:
            func = sys.argv[1]
            num = sys.argv[2]
            step = sys.argv[3]
            print("%.9f" % main(func, num, step))
    except Exception as e:
        print(f"Ошибка: {e}")
