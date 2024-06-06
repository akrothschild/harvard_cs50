#include <cs50.h>
#include <stdio.h>

void print_height(int height);

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height <= 0 || height > 8);

    print_height(height);
}

void print_height(int height)
{
    for (int i = 1; i <= height; i++)
    {
        for (int n = height - i; n > 0; n--)
        {
            printf(" ");
        }
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }

        printf("  ");

        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }

        printf("\n");
    }
}
