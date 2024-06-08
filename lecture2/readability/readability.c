#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Prompt the user for some text
    string text = get_string("Text: ");

    // Count the number of letters, words, and sentences in the text
    int letters = count_letters(text);

    int words = count_words(text);

    int sentences = count_sentences(text);

    // Compute the Coleman-Liau index

    int index = round(0.0588 * (float) letters * 100 / (float) words -
                      0.296 * (float) sentences * 100 / (float) words - 15.8);

    // Print the grade level
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    // Return the number of letters in text
    int letters = 0;
    for (int i = 0, n = strlen(text); i <= n; i++)
    {
        int l = toupper(text[i]);
        if (l >= 65 && l <= 90)
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    // Return the number of words in text
    int words = 1;
    for (int i = 0, n = strlen(text); i <= n; i++)
    {

        if (text[i] == ' ')
        {
            words++;
        }
    }
    return words;
}

int count_sentences(string text)
{
    // Return the number of sentences in text
    int sentences = 0;
    for (int i = 0, n = strlen(text); i <= n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            if (text[i + 1] != '.' || text[i + 1] != '!' || text[i + 1] != '?')
            {
                sentences++;
            }
        }
        int l = toupper(text[i]);
    }
    if (sentences == 0)
    {
        for (int i = 0, n = strlen(text); i <= n; i++)
        {
            int l = toupper(text[i]);
            if (l >= 65 && l <= 90)
            {
                sentences = 1;
            }
        }
    }
    return sentences;
}
