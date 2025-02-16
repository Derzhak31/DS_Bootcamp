class Research:
    def file_reader(self):
        with open("data.csv", "r") as f:
            content = f.read()
            return content


if __name__ == "__main__":
    print(Research().file_reader())
