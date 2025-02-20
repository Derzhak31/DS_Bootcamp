#!/bin/python
import os
import sys
import psutil


def get_lines(filename: str):
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Файл {filename} не найден!")

    with open(filename, "r") as f:
        line = f.readline()
        while line:
            yield line
            line = f.readline()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        for i in get_lines(sys.argv[1]):
            pass
        process = psutil.Process()
        memory = process.memory_info().rss
        times = process.cpu_times()
        time = times.user + times.system
        print(f"Peak Memory Usage = {memory / (1024**3):.3f} GB")
        print(f"User Mode Time + System Mode Time = {time:.2f}s")
    else:
        raise Exception("Передайте 1 аргумент - файл")
