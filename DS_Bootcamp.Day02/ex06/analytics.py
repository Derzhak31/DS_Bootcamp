import os
import logging
import requests
from random import randint

from config import TOKEN, chat_id


class Research:
    def __init__(self, filename):
        self.filename = filename

    def file_reader(self, has_header=True):
        logging.basicConfig(
            filename="analytics.log",
            level=logging.INFO,
            format="%(asctime)s %(message)s",
        )
        logging.info(f"Чтение файла {self.filename}")

        if not os.path.isfile(self.filename):
            logging.error(f"Файл {self.filename} не найден!")
            raise FileNotFoundError(f"Файл {self.filename} не найден!")

        with open(self.filename, "r") as f:
            text = f.read()
            lines = text.split("\n")
            if len(lines[0].split(",")) != 2 and has_header:
                logging.error(
                    f"В заголовке {self.filename} не верное количество столбцов!"
                )
                raise ValueError("В заголовке файла не верное количество столбцов!")
            content = []
            for i in lines[(1 if has_header else 0) :]:
                num = i.split(",")
                if len(num) != 2:
                    logging.error(f"В {self.filename} количество столбцов не равно 2!")
                    raise ValueError("В файле количество столбцов не равно 2!")
                if i != "1,0" and i != "0,1":
                    logging.error(f"В {self.filename} не верное значение в столбцах!")
                    raise ValueError("В файле не верное значение в столбцах!")
                content.append(list(map(int, num)))
            logging.info(f"Файл {self.filename} прочитан")
            return content

    def send_message_tg(self, message):
        logging.info("Отправка сообщения в Telegram")
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        params = {"chat_id": {chat_id}, "text": {message}}
        response = requests.get(url, params)
        if response.status_code == 200:
            logging.info("Сообщение успешно отправлено в Telegram")
        else:
            logging.error("Ошибка при отправке сообщения в Telegram")
            raise PermissionError("Ошибка в данных бота (token, chat_id)")

    class Calculations:
        def __init__(self, data):
            self.data = data

        def counts(self):
            logging.info("Вычисляется количество орлов и решек")
            head, tail = zip(*self.data)
            logging.info(f"Результат: орел-{head}; решка-{tail}")
            return sum(head), sum(tail)

        def fractions(self, heads, tails):
            logging.info("Вычисляется процентное соотношение орлов и решек")
            sum_ht = heads + tails
            pr_heads = heads / sum_ht * 100
            pr_tails = tails / sum_ht * 100
            logging.info(f"Результат: орел-{pr_heads}%; решка-{pr_tails}%")
            return pr_heads, pr_tails

    class Analytics(Calculations):
        def predict_random(self, steps):
            logging.info("Создание случайных результатов")
            if not isinstance(steps, int) or steps < 1:
                logging.error("Количество шагов не задано целым числом больше 0")
                raise ValueError("Задайте количество шагов целым числом больше 0")
            result = []
            for i in range(steps):
                a = randint(0, 1)
                b = 0 if a == 1 else 1
                result.append([a, b])
            logging.info(
                f"Случайные результататы из {steps} подбрасываний были созданы"
            )
            return result

        def predict_last(self):
            logging.info("Вычисляется последний результат подбрасывания монеты")
            return self.data[-1]

        def save_file(self, data, name_of_file, type_file="txt"):
            logging.info("Запись данных в файл")
            with open(f"{name_of_file}.{type_file}", "w") as f:
                f.write(data)
