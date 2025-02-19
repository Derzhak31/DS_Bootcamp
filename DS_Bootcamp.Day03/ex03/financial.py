#!/bin/python
import sys
import time
import requests
from bs4 import BeautifulSoup


def main(ticker, field):
    url = f"https://finance.yahoo.com/quote/{ticker}/financials/?p={ticker}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        raise Exception("Неверно указан тикер")
    soup = BeautifulSoup(response.text, "html.parser")
    resp_ticker = soup.find("h1", class_="yf-xxbei9")
    if resp_ticker is None:
        raise Exception("Неверно указан тикер")
    elif resp_ticker.text[-len(ticker) - 1 : -1] != ticker:
        raise Exception("Неверно указан тикер")
    soup_field = soup.find_all("div", class_="row lv-0 yf-t22klz")
    data_field = None
    time.sleep(5)
    for row in soup_field:
        name_field = row.find("div", class_="rowTitle").text
        if name_field.lower() == field.lower():
            data_field = [name_field]
            for col in row.find_all("div", class_="column")[1:]:
                data_field.append(col.text.strip())
    if data_field is None:
        raise Exception("Неверно указано поле поиска")
    return print(tuple(data_field))


if __name__ == "__main__":
    try:
        if len(sys.argv) == 3:
            main(sys.argv[1].upper(), sys.argv[2])
        else:
            print("Укажите 2 аргумента")
    except Exception as e:
        print(f"Ошибка: {e}")
