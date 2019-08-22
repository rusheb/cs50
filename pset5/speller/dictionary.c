// Implements a dictionary's functionality
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "dictionary.h"
#include <string.h>
#include <ctype.h>

typedef struct node
{
    bool isWord;
    struct node *children[27];
}
node;
node *root = NULL;
int dictionarySize;

int charToInt(char c)
{
    if (c == '\'')
    {
        return 26;
    }
    else
    {
        return (int) c - 97;
    }
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    node *subWord = root;

    const char *t;
    for (t = word; *t != '\0'; t++)
    {
        int index = charToInt(tolower(*t));
        if (subWord->children[index] == NULL)
        {
            return false;
        }
        subWord = subWord->children[index];
    }

    return (subWord->isWord);
}

void initialiseNode(node *node)
{
    for (int i = 0; i < 27; i++)
    {
        node->children[i] = NULL;
    }
    node->isWord = false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    dictionarySize = 0;

    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", dictionary);
        return 3;
    }

    char word[LENGTH + 1];

    root = malloc(sizeof(node));
    initialiseNode(root);

    node *currentNode;
    node *childNode;
    // for each word in the dictionary file
    while (fscanf(file, "%s", word) != EOF)
    {
        currentNode = root;
        int index = 0;
        while (word[index] != '\0')
        {
            int childIndex = charToInt(word[index++]);

            // add child node if necessary
            childNode = currentNode->children[childIndex];
            if (childNode == NULL)
            {
                childNode = malloc(sizeof(node));
                if (childNode == NULL)
                {
                    fprintf(stderr, "malloc failed");
                    return false;
                }
                initialiseNode(childNode);
                currentNode->children[childIndex] = childNode;
            }
            // advance to child node
            currentNode = childNode;
        }
        // mark the end of the word
        currentNode->isWord = true;
        dictionarySize++;
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return dictionarySize;
    return 0;
}

bool unloadNode(node *nodeToCheck)
{
    for (int i = 0; i < 27; i++)
    {
        if (nodeToCheck->children[i] != NULL)
        {
            unloadNode(nodeToCheck->children[i]);
        }
    }
    free(nodeToCheck);
    return true;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *pointer = root;
    return unloadNode(pointer);
}