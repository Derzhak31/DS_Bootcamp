import sys


def gen_letter(arg):
    with open("employees.tsv", "r") as f:
        for i in f:
            name, surname, email = i.strip().split("\t")
            if email == arg:
                print(
                    f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires."
                )


if __name__ == "__main__":
    if len(sys.argv) == 2:
        gen_letter(sys.argv[1])
