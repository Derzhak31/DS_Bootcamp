import sys


def post_email(arg):
    with open(arg, "r") as f:
        email = f.read().splitlines()
    with open("employees.tsv", "w") as out_f:
        out_f.write("Name\tSurname\tE-mail\n")
        for i in email:
            name, surname = i.split("@")[0].split(".")
            out_f.write(f"{name.capitalize()}\t{surname.capitalize()}\t{i}\n")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        post_email(sys.argv[1])
