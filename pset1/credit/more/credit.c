#include <stdio.h>
#include <cs50.h>
#include <math.h>

int countDigits(long long x)
{
    return floor(log10(x)) + 1;
}

void getArrayFromNumber(int arr[], int size, long long number)
{
    for (int i = 0; i < size; i++)
    {
        int digit = number % 10;
        arr[size - i - 1] = digit;
        number /= 10;
    }
}

void doubleAlternateDigits(int card_number[], int size)
{
    int index_to_double = size - 2;
    int j = 0;

    while (index_to_double > -1)
    {
        card_number[index_to_double] *= 2;
        index_to_double -= 2;
        j += 1;
    }
}

int arraySum(int arr[], int size)
{
    int sum = 0;
    for (int i = 0; i < size; i++)
    {
        int element = arr[i];
        if (element > 9)
        {
            int sub_elements[2];
            getArrayFromNumber(sub_elements, 2, element);
            sum += sub_elements[0];
            sum += sub_elements[1];
        }
        else
        {
            sum += arr[i];
        }
    }
    return sum;
}

bool isValid(int sum)
{
    return sum % 10 == 0;
}

string getProvider(long long raw_card_number, int size)
{
    long long first_digits = raw_card_number;
    while (first_digits > 99)
    {
        first_digits /= 10;
    }

    if ((first_digits == 34 || first_digits == 37) && size == 15)
    {
        return "AMEX\n";
    }
    else if ((40 <= first_digits && first_digits <= 49) && (size == 13 || size == 16))
    {
        return "VISA\n";
    }
    else if ((51 <= first_digits && first_digits <= 55) && (size == 16))
    {
        return "MASTERCARD\n";
    }
    else
    {
        return "INVALID\n";
    }
}



int main(void)
{
    long long raw_card_number = get_long_long("Number: ");
    int size = countDigits(raw_card_number);
    string provider = getProvider(raw_card_number, size);

    int card_number[size];
    getArrayFromNumber(card_number, size, raw_card_number);

    doubleAlternateDigits(card_number, size);

    int sum = arraySum(card_number, size);

    if (isValid(sum))
    {
        printf("%s", provider);
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}