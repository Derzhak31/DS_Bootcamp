class Must_read:
    filename = "data.csv"

    with open(filename, "r") as f:
        content = f.read()
        print(content)


if __name__ == "__main__":
    Must_read()
