from cs50 import get_int

BLANK = ' '
BLOCK = '#'


def main():
    height = get_int("Height: ")
    while height < 0 or height > 23:
        height = get_int("Height: ")

    blocks = 1
    for i in range(height):
        blanks = height - blocks
        print_row(blanks, blocks)
        blocks += 1


def print_row(outside, inside):
    print_n(outside, BLANK)
    print_n(inside, BLOCK)
    print_n(2, BLANK)
    print_n(inside, BLOCK)
    print()


def print_n(n, c):
    for i in range(n):
        print(c, end='')


if __name__ == "__main__":
    main()