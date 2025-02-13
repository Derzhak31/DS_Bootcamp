import sys

clients = [
    "andrew@gmail.com",
    "jessica@gmail.com",
    "ted@mosby.com",
    "john@snow.is",
    "bill_gates@live.com",
    "mark@facebook.com",
    "elon@paypal.com",
    "jessica@gmail.com",
]
participants = [
    "walter@heisenberg.com",
    "vasily@mail.ru",
    "pinkman@yo.org",
    "jessica@gmail.com",
    "elon@paypal.com",
    "pinkman@yo.org",
    "mr@robot.gov",
    "eleven@yahoo.com",
]
recipients = ["andrew@gmail.com", "jessica@gmail.com", "john@snow.is"]


def call_center():
    return print(*(set(clients) - set(recipients)), sep=", ")


def potential_clients():
    return print(*(set(participants) - set(clients)), sep=", ")


def loyalty_program():
    return print(*(set(clients) - set(participants)), sep=", ")


def get_data(arg):
    if arg == "call_center":
        call_center()
    elif arg == "potential_clients":
        potential_clients()
    elif arg == "loyalty_program":
        loyalty_program()
    else:
        raise ValueError("Unknown args")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        get_data(sys.argv[1])
