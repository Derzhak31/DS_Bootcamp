import sys


def get_company(arg):
    COMPANIES = {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Netflix": "NFLX",
        "Tesla": "TSLA",
        "Nokia": "NOK",
    }
    STOCKS = {
        "AAPL": 287.73,
        "MSFT": 173.79,
        "NFLX": 416.90,
        "TSLA": 724.88,
        "NOK": 3.37,
    }

    for i in arg:
        ticker = i.upper()
        company = i.capitalize()

        if ticker in STOCKS:
            company = next(key for key, value in COMPANIES.items() if value == ticker)
            print(f"{ticker} is a ticker symbol for {company}")
        elif company in COMPANIES:
            print(f"{company} stock price is {STOCKS[COMPANIES[company]]}")
        else:
            print(f"{i} is an unknown company or an unknown ticker symbol")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        string = sys.argv[1].replace(" ", "").split(",")
        if string.count("") == 0:
            get_company(string)
