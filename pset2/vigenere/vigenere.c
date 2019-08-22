#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int increment_key(int index, int length)
{
    index += 1;
    return index % length;
}

char shift(char letter, int offset)
{
    letter += offset;
    if (letter > 'Z')
    {
        letter = ('A' - 1) + (letter % 'Z');

    }
    return letter;
}

char *encode(string phrase, string key)
{
    int keyLength = strlen(key);
    int keyIndex = 0;

    for (int i = 0; i < strlen(phrase); i++)
    {
        int offset = toupper(key[keyIndex]) - 'A';

        if (islower(phrase[i]))
        {
            phrase[i] = toupper(phrase[i]);
            phrase[i] = shift(phrase[i], offset);
            phrase[i] = tolower(phrase[i]);
            keyIndex = increment_key(keyIndex, keyLength);
        }
        else if (isupper(phrase[i]))
        {
            phrase[i] = shift(phrase[i], offset);
            keyIndex = increment_key(keyIndex, keyLength);
        }
    }
    return phrase;
}

bool contains_only_letters(string phrase)
{
    for (int i; i < strlen(phrase); i++)
    {
        if (!isalpha(phrase[i]))
        {
            return false;
        }
    }
    return true;
}

bool valid_args(int argc, string argv[])
{
    if (argc == 2 && contains_only_letters(argv[1]))
    {
        return true;
    }
    return false;
}

int main(int argc, string argv[])
{
    if (valid_args(argc, argv))
    {
        string key = argv[1];
        string phrase = get_string("plaintext:");
        phrase = encode(phrase, key);
        printf("ciphertext: %s\n", phrase);
    }
    else
    {
        printf("invalid arguments\n");
        return 1;
    }
    return 0;
}