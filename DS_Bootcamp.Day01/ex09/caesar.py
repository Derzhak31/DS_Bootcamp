import sys


def get_caesar(code, text, shift):
    result = []
    for char in text:
        if "a" <= char <= "z":
            base = ord("a")
            shifted_char = chr(
                (ord(char) - base + shift * (1 if code == "encode" else -1)) % 26 + base
            )
            result.append(shifted_char)
        elif "A" <= char <= "Z":
            base = ord("A")
            shifted_char = chr(
                (ord(char) - base + shift * (1 if code == "encode" else -1)) % 26 + base
            )
            result.append(shifted_char)
        else:
            result.append(char)
    print("".join(result))


if __name__ == "__main__":
    cirilic = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    if len(sys.argv) == 4 and sys.argv[1] in ["encode", "decode"]:
        if cirilic.isdisjoint(sys.argv[2].lower()):
            get_caesar(sys.argv[1], sys.argv[2], int(sys.argv[3]))
        else:
            print("Скрипт пока не поддерживает ваш язык")
    else:
        print("Неверно указаны аргументы!")
