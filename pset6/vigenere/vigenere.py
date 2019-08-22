from cs50 import get_string

import sys


def main() -> int:
    if len(sys.argv) == 2:
        key = Key(sys.argv[1])
        phrase = get_string('plaintext:  ')

        ciphertext = encode(phrase, key)

        print(f'ciphertext: {ciphertext}')
        sys.exit(0)
    else:
        print("Usage: vigenere.py key")
        sys.exit(1)


def encode(phrase, key) -> str:
    result = ''
    for c in phrase:
        offset = key.offset()

        if c.isupper():
            letter = shift(c, offset)
            key.increment()
        elif c.islower():
            letter = shift(c.upper(), offset).lower()
            key.increment()
        else:
            letter = c

        result += letter
    return result


def shift(char, offset) -> chr:
    shifted = chr(ord(char) + offset)

    if ord(shifted) > ord('Z'):
        shifted = chr(ord(shifted) - 26)

    return shifted


class Key:
    def __init__(self, value):
        if not value.isalpha():
            print('Key must contain only letters')
            sys.exit(1)
        self.value = value.upper()
        self.index = 0

    def increment(self) -> None:
        self.index = (self.index + 1) % len(self.value)

    def offset(self) -> int:
        return ord(self.value[self.index]) - ord('A')


if __name__ == "__main__":
    main()