#include <stdio.h>
#include <cs50.h>

int get_height()
{
    int height = -1;

    while (height < 0 || height > 23)
    {
        height = get_int("Height: ");
    }

    return height;
}

void print_n(int n, char c)
{
    for (int i = 0; i < n; i ++)
    {
        printf("%c", c);
    }
}

void print_pyramid(int height)
{
    char BLANK = ' ';
    char BLOCK = '#';

    int blocks = 1;

    while (blocks < height + 1)
    {
        int blanks = height - blocks;

        print_n(blanks, BLANK);
        print_n(blocks, BLOCK);
        print_n(2, BLANK);
        print_n(blocks, BLOCK);
        printf("\n");

        blocks += 1;
    }
}

int main(void)
{
    int height = get_height();
    print_pyramid(height);
}