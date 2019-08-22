#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main()
{
    char * fraction;
    strcpy(fraction, "1/4");
    int numerator = atoi(strtok(fraction, "/"));
    int denominator = atoi(strtok(NULL, "/"));

    int duration = numerator * 8 / denominator;
    return duration;
}