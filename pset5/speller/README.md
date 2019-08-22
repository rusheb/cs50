# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

> "an invented long word said to mean a lung disease caused by inhaling very fine ash and sand dust"

## According to its man page, what does `getrusage` do?

Returns resource usage measures for processes.
The resources include CPU time, data size, faults, signals received

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Passing by reference is faster.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

For each character
    If it's an alphabetic character or an apostrophe, add the letter to the
    current index of `word` and increment it.
    Check if the max word length has been exceeded, keep reading characters
    until the end of the word is reached and then reset `word`, to ignore
    the rest.
    If it's a digit, keep reading to the end of the word and reset.
    If it's none of these (e.g. it's a space or other punctuation)
    it signifies the end of the word. Add a NUL to terminate the word
    and use `check()` to see if the word is in the dict. Reset the
    index and go back to start of loop to read in the next word.


## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like
`"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

`fscanf` uses conversion arguments e.g. `%s` to specify what kind of characters will be matched. It might convert other
characters if it encounters them? `%s` would match any non-whitespace characters so full stops might be included in a word?
`fscanf` doesn't let us keep track of exactly how many characters we have read, which could lead to a segmentation fault.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

We don't want them to be changed by the function, so it's safer to declare them as `const`.