import os
import sys
from random import randint


class Research:
    def __init__(self, filename):
        self.filename = filename

    def file_reader(self, has_header=True):
        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"Файл {self.filename} не найден!")

        with open(self.filename, "r") as f:
            text = f.read()
            lines = text.split("\n")
            if len(lines[0].split(",")) != 2 and has_header:
                raise ValueError("В заголовке файла не верное количество столбцов!")
            content = []
            for i in lines[(1 if has_header else 0) :]:
                num = i.split(",")
                if len(num) != 2:
                    raise ValueError("В файле количество столбцов не равно 2!")
                if i != "1,0" and i != "0,1":
                    raise ValueError("В файле не верное значение в столбцах!")
                content.append(list(map(int, num)))
            return content

    class Calculations:
        def __init__(self, data):
            self.data = data

        def counts(self):
            head, tail = zip(*self.data)
            return sum(head), sum(tail)

        def fractions(self, heads, tails):
            sum_ht = heads + tails
            pr_heads = heads / sum_ht * 100
            pr_tails = tails / sum_ht * 100
            return pr_heads, pr_tails

    class Analytics(Calculations):
        def predict_random(self, steps):
            result = []
            for i in range(steps):
                a = randint(0, 1)
                b = 0 if a == 1 else 1
                result.append([a, b])
            return result

        def predict_last(self):
            return self.data[-1]


if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        res = Research(file_name)
        res_data = res.file_reader()
        res_calc = res.Calculations(res_data)
        print(res_data)

        h, t = res_calc.counts()
        print(h, t)

        pr_h, pr_t = res_calc.fractions(h, t)
        print(pr_h, pr_t)

        res_analytics = res.Analytics(res_data)
        data_analytics = res_analytics.predict_random(3)
        print(data_analytics)
        print(res_analytics.predict_last())
