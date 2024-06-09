#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Make sure every character in argv[1] is a digit
    // Convert argv[1] from a `string` to an `int`
    int key = 0;
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (argv[1][i] >= 48 && argv[1][i] <= 57)
        {
            key = key * 10 + (argv[1][i] - 48);
        }
        else
        {
            printf("Usage: ./caesar key");
            return 1;
        }
    }

    key %= 26;

    // Prompt user for plaintext
    string plaintext = get_string("plaintext: ");
    int n = strlen(plaintext);
    char ciphertext[n];

    // For each character in the plaintext:
    // Rotate the character if it's a letter
    for (int i = 0; i <= n; i++)
    {
        int l = plaintext[i];
        if ((l >= 65 && l <= 90) || (l >= 97 && l <= 122))
        {
            int ascii = plaintext[i] + key;
            if ((isupper(plaintext[i]) && ascii > 90) || ascii > 122)
            {
                ciphertext[i] = ascii - 26;
            }
            else
            {
                ciphertext[i] = ascii;
            }
        }
        else
        {
            ciphertext[i] = plaintext[i];
        }
    }
    printf("ciphertext: %s\n", ciphertext);
    return 0;
}
