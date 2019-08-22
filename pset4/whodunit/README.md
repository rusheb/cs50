# Questions

## What's `stdint.h`?

stdint.h provides a set of typedefs that specify exact-width integer types.
These can be signed or unsigned.
so int8_t is an 8-bit integer with a sign (between -2^7 and 2^7)
   uint16_t is a 16-bit integer without a sign (between 0 and 2^16)

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

exact widths allow us to know exactly where in memory everything is being kept.
having several different exact widths is more efficient since we don't need to use more memory than we require.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

1, 4, 4, 2

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

BM

## What's the difference between `bfSize` and `biSize`?

bfSize: "The size, in bytes, of the bitmap file."
biSize: "The number of bytes required by the structure." i.e. the size of the info header

## What does it mean if `biHeight` is negative?

Indicates a top-down dib (the file is read from the upper left corner).

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

* if a large enough block of memory to open the file cannot be found
* if you don't have the correct permissions
* file doesn't exist

## Why is the third argument to `fread` always `1` in our code?

We are reading one element at a time and we have already defined the size of the structs
(BMAPFILEHEADER, BMAPINFOHEADER, RGBTRIPLE)

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

1

## What does `fseek` do?

int `fseek(FILE *stream, long int offset, int whence)`
"sets the file position of the stream to a given offset" (tutorialspoint)

so `fseek(inptr, padding, SEEK_CUR)` would skip over the size of the padding

## What is `SEEK_CUR`?

The current position of the file pointer (the position we have reached, reading the file)

## Whodunit?

It was Professor Plum with the candlestick in the library
