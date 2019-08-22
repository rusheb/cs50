from cs50 import get_int
from math import floor


def main():
    card_number = get_int("Number: ")

    if (is_valid(card_number)):
        print(get_provider(card_number))
    else:
        print("INVALID\n")


def is_valid(card_number):
    digits = double_alternate_digits(card_number)
    sum = sum_elements_by_digit(digits)
    return (sum % 10 == 0)


def double_alternate_digits(number):
    num_as_string = str(number)

    result = []
    position = len(num_as_string) - 1
    counter = 0
    while (position >= 0):
        digit = int(num_as_string[position])

        if (counter % 2):
            digit *= 2

        result.append(digit)

        position -= 1
        counter += 1

    return result


def sum_elements_by_digit(input):
    sum = 0
    for element in input:
        if element < 10:
            sum += element
        else:
            string = str(element)
            for digit in string:
                sum += int(digit)

    return sum


def get_provider(raw_card_number):
    starts_with = int(str(raw_card_number)[:2])
    length = len(str(raw_card_number))

    if (starts_with == 34 or starts_with == 37) and length == 15:
        return "AMEX"
    elif (40 <= starts_with and starts_with <= 49 and
          (length == 13 or length == 16)):
        return "VISA"
    elif (51 <= starts_with and starts_with <= 55) and (length == 16):
        return "MASTERCARD"
    else:
        return "INVALID"


if __name__ == '__main__':
    main()