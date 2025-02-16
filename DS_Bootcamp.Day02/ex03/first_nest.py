import os
import sys


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
        def counts(self, data):
            head, tail = zip(*data)
            return sum(head), sum(tail)

        def fractions(self, heads, tails):
            sum_ht = heads + tails
            pr_heads = heads / sum_ht * 100
            pr_tails = tails / sum_ht * 100
            return pr_heads, pr_tails


if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        res = Research(file_name)
        res_data = res.file_reader(False)
        print(res_data)

        res_calc = res.Calculations()
        h, t = res_calc.counts(res_data)
        print(h, t)

        pr_h, pr_t = res_calc.fractions(h, t)
        print(pr_h, pr_t)
