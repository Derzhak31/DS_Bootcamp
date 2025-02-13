def data_types():
    data = [21, "school", 2.1, True, [], {}, (), set()]
    out = "["
    for i in data:
        out += type(i).__name__ + ", "
    print(out[:-2] + "]")


if __name__ == "__main__":
    data_types()
