#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

typedef struct
{
    char letter;
    int value;
} game;
const int n = 26;

int main(void)
{
    // INITIALIZE
    game scrabble[] = {
        {.letter = 'A', .value = 1}, {.letter = 'B', .value = 3},  {.letter = 'C', .value = 3},
        {.letter = 'D', .value = 2}, {.letter = 'E', .value = 1},  {.letter = 'F', .value = 4},
        {.letter = 'G', .value = 2}, {.letter = 'H', .value = 4},  {.letter = 'I', .value = 1},
        {.letter = 'J', .value = 8}, {.letter = 'K', .value = 5},  {.letter = 'L', .value = 1},
        {.letter = 'M', .value = 3}, {.letter = 'N', .value = 1},  {.letter = 'O', .value = 1},
        {.letter = 'P', .value = 3}, {.letter = 'Q', .value = 10}, {.letter = 'R', .value = 1},
        {.letter = 'S', .value = 1}, {.letter = 'T', .value = 1},  {.letter = 'U', .value = 1},
        {.letter = 'V', .value = 4}, {.letter = 'W', .value = 4},  {.letter = 'X', .value = 8},
        {.letter = 'Y', .value = 4}, {.letter = 'Z', .value = 10},
    };

    // Prompt the user for two words
    string player1 = get_string("Player1: ");
    string player2 = get_string("Player2: ");
    int p1count = 0;
    int p2count = 0;

    // Compute the score of each word
    int i = 0;
    while (player1[i] != '\0')
    {
        for (int j = 0; j < n; j++)
            if (scrabble[j].letter == toupper(player1[i]))
            {
                p1count += scrabble[j].value;
            }
        i++;
    }

    i = 0;
    while (player2[i] != '\0')
    {
        for (int j = 0; j < n; j++)
            if (scrabble[j].letter == toupper(player2[i]))
            {
                p2count += scrabble[j].value;
            }
        i++;
    }
    printf("Player 1 count: %i\n", p1count);
    printf("Player 2 count: %i\n", p2count);

    // Print the winner
    if (p1count > p2count)
    {
        printf("Player 1 wins!\n");
        return 0;
    }
    else if (p2count > p1count)
    {
        printf("Player 2 wins!\n");
        return 0;
    }
    else
    {
        printf("Tie!\n");
        return 0;
    }
}
