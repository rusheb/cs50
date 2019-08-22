#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <cs50.h>
#include <crypt.h>

char ALPHABET[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
int alphabetSize = 52;

int max_length = 4;

void check(char *guess, char *salt, char *hash)
{
    string hashedGuess = crypt(guess, salt);
    if (!strcmp(hash, hashedGuess))
    {
        printf("%s\n", guess);
        free(guess);
        exit(0);
    }
}

// recursively fill the buffer and check it each time
void brute_force(char *buf, int index, int length, string salt, string hash)
{
    for (int i = 0; i < alphabetSize; i++)
    {
        sprintf(buf + index, "%c", ALPHABET[i]);

        if (index < length)
        {
            brute_force(buf, index + 1, length, salt, hash);
        }
        else
        {
            check(buf, salt, hash);
        }
    }
}

char *crack(string hash, string salt)
{
    // create a buffer big enough to hold the longest possible password
    char *buf = (char *) malloc(max_length + 1);

    // brute force
    for (int length = 0; length < max_length; length++)
    {
        brute_force(buf, 0, length, salt, hash);
    }
    return "";
}

bool valid_args(int argc, string argv[])
{
    if (argc == 2)
    {
        return true;
    }
    return false;
}

int main(int argc, string argv[])
{
    if (valid_args(argc, argv))
    {
        string hash = argv[1];

        char salt[3];
        strncpy(salt, hash, 2); // salt is first 2 characters of hash

        string password = crack(hash, salt);
    }
    else
    {
        printf("Invalid arguments\n");
        return 1;
    }
    return 0;
}