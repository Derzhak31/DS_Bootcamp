import sys


def output_price(arg):
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
    if arg not in STOCKS:
        print("Unknown ticker")
    else:
        company = next(key for key, value in COMPANIES.items() if value == arg)
        print(company, STOCKS[arg])


if __name__ == "__main__":
    if len(sys.argv) == 2:
        output_price(sys.argv[1].upper())
