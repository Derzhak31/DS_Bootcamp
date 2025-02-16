import os
import sys


class Research:
    def __init__(self, filename):
        self.filename = filename

    def file_reader(self):
        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"Файл {self.filename} не найден!")

        with open(self.filename, "r") as f:
            content = f.read()
            lines = content.split("\n")
            if len(lines[0].split(",")) != 2:
                raise ValueError("В заголовке файла не верное количество столбцов!")
            for i in lines[1:]:
                num = i.split(",")
                if len(num) != 2:
                    raise ValueError("В файле количество столбцов не равно 2!")
                if i != "1,0" and i != "0,1":
                    raise ValueError("В файле не верное значение в столбцах!")
            return content


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(Research(sys.argv[1]).file_reader())
