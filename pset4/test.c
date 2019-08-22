#include <stdio.h>

#include "whodunit/bmp.h"

int main()
{
    // get an int and find where it is in memory
    RGBTRIPLE triple;
    triple.rgbtRed = 0x00;
    triple.rgbtBlue = 0x00;
    triple.rgbtGreen = 0x00;
    triple = 0xff 0xff 0xff;
    char *testStr = "hello";
    printf("%c\n", *(testStr + 3));
}