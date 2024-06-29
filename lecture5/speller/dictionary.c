#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Hash word to obtain hash value
    unsigned int index = hash(word);

    // Traverse linked list at that index in hash table
    node *cursor = table[index];
    while (cursor != NULL)
    {
        // Compare word with current node's word
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true; // Found
        }
        cursor = cursor->next;
    }

    return false; // Not found
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    return (toupper(word[0]) - 'A') % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }

    // Buffer to hold each word read from file
    char buffer[LENGTH + 1];

    // Read each word in the file
    while (fscanf(source, "%s", buffer) != EOF)
    {
        // Allocate memory for new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(source);
            return false;
        }

        // Copy word into node
        strcpy(new_node->word, buffer);
        new_node->next = NULL;

        // Hash word to obtain hash value
        unsigned int index = hash(buffer);

        // Insert node into hash table at that location
        if (table[index] == NULL)
        {
            // No collision, first node in bucket
            table[index] = new_node;
        }
        else
        {
            // Collision, insert at beginning of linked list
            new_node->next = table[index];
            table[index] = new_node;
        }
    }

    // Close the dictionary file
    fclose(source);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    unsigned int count = 0;

    // Iterate through each bucket in the hash table
    for (int i = 0; i < N; i++)
    {
        // Traverse linked list at each bucket
        node *cursor = table[i];
        while (cursor != NULL)
        {
            count++;
            cursor = cursor->next;
        }
    }

    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Iterate through each bucket in the hash table
    for (int i = 0; i < N; i++)
    {
        // Free nodes in the linked list at each bucket
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }

    return true;
}
