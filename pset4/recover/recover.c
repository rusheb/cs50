#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

void openNewJpgForWriting(FILE **outptr, int fileCount)
{
    fclose(*outptr);
    char fileName[8];
    sprintf(fileName, "%03i.jpg", fileCount);
    *outptr = fopen(fileName, "w");
}

bool blockStartsWithJpgHeader(unsigned char buffer[512])
{
    unsigned int signature = 0;
    signature |= (unsigned int) buffer[0] << 24;
    signature |= (unsigned int) buffer[1] << 16;
    signature |= (unsigned int) buffer[2] << 8;
    signature |= (unsigned int) buffer[3];

    return (signature >= 4292411360 && signature <= 4292411375);
}

void recoverJpgs(FILE **inptr)
{
    unsigned char buffer[512];
    int fileCount = 0;
    FILE *outptr = fopen("temp", "w");

    // read through the file 1 block (512 bytes) at a time
    while (fread(buffer, sizeof(buffer), 1, *inptr) == 1)
    {
        if (blockStartsWithJpgHeader(buffer))
        {
            openNewJpgForWriting(&outptr, fileCount);
            fileCount++;
        }

        fwrite(buffer, sizeof(buffer), 1, outptr);
    }

    // clean up
    remove("temp");
    fclose(outptr);
}

int main(int argc, char *argv[])
{
    if (argc == 2)
    {
        char *infile = argv[1];
        FILE *inptr = fopen(infile, "r");
        if (inptr == NULL)
        {
            fprintf(stderr, "Could not open %s.\n", infile);
            return 2;
        }

        recoverJpgs(&inptr);
        fclose(inptr);
        return 0;
    }
    else
    {
        fprintf(stderr, "Usage: recover filename\n");
        return 1;
    }
}