#!/bin/python
import timeit
import random
from collections import Counter


def my_function(nums: list[int]):
    result = {}
    for i in nums:
        if i not in result:
            result[i] = 0
        result[i] += 1
    return result


def counters(nums: list[int]):
    result = Counter(nums)
    return dict(result)


def my_top(nums: list[int]):
    result = {}
    for i in nums:
        if i not in result:
            result[i] = 0
        result[i] += 1
    sort_res = sorted(result.items(), key=lambda item: item[1], reverse=True)
    return dict(sort_res[:10])


def counter_top(nums: list[int]):
    result = Counter(nums).most_common(10)
    return dict(result)


def main():
    elems = [random.randint(0, 100) for i in range(1000000)]
    func1 = timeit.timeit(lambda: my_function(elems), number=1)
    func2 = timeit.timeit(lambda: counters(elems), number=1)
    func3 = timeit.timeit(lambda: my_top(elems), number=1)
    func4 = timeit.timeit(lambda: counter_top(elems), number=1)
    print("my function: %.6f" % func1)
    print("Counter: %.6f" % func2)
    print("my top: %.6f" % func3)
    print("Counter's top: %.6f" % func4)


if __name__ == "__main__":
    main()
