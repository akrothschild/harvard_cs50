#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

typedef struct
{
    char plain;
    char key;
} cypher;

int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Check if the key comtains 26 characters
    char *key = argv[1];
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }

    // Handle non alphabetical chars
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Usage: ./substitution key\n");
            return 1;
        }
        int duplicates = 0;
        for (int j = 0; j < 26; j++)
        {
            if (toupper(key[i]) == toupper(key[j]))
            {
                duplicates++;
            }
        }
        if (duplicates > 1)
        {
            printf("Usage: ./substitution key\n");
            return 1;
        }
    }

    cypher code[26];
    for (int i = 0; i < 26; i++)
    {
        // Initialize the cipher struct
        code[i].plain = 'A' + i;
        code[i].key = toupper(key[i]);
    };

    // Prompt user for plaintext
    string plaintext = get_string("plaintext: ");
    int n = strlen(plaintext);

    // Allocate memory for ciphertext
    char ciphertext[n + 1];

    // Encrypt the plaintext
    for (int i = 0; i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            char letter = plaintext[i];
            if (isupper(letter))
            {
                ciphertext[i] = code[letter - 'A'].key;
            }
            else
            {
                ciphertext[i] = tolower(code[letter - 'a'].key);
            }
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }
    // Null-terminate the ciphertext
    ciphertext[n] = '\0';

    // Print the ciphertext
    printf("ciphertext: %s\n", ciphertext);
    return 0;
}
