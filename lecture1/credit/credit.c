#include <cs50.h>
#include <stdio.h>

int checksum(long number);
void card_type(long number);

int main(void)
{
    long number;
    do
    {
        number = get_long("Number: ");
    }
    while (number < 0);

    if (checksum(number) == 1)
    {

        card_type(number);
    }
    else
    {
        printf("INVALID\n");
    }
}

int checksum(long number)
{
    int sum = 0;
    for (int i = 1; i <= 16; i++)
    {
        if (i % 2 == 0)
        {
            int reminder = number % 10;
            number = (number - reminder) / 10;
            if (reminder * 2 > 9)
            {
                sum = sum + (reminder * 2) % 10 + ((reminder * 2) - (reminder * 2) % 10) / 10;
            }
            else
            {
                sum = sum + (reminder * 2);
            }
        }
        else
        {
            int reminder = number % 10;
            number = (number - reminder) / 10;
            sum = sum + reminder;
        }
    }
    if (sum % 10 == 0)
    {

        return 1;
    }
    else
    {

        return 0;
    }
}

void card_type(long number)
{
    int visa16 = (number / 1000000000000000);
    int visa13 = (number / 1000000000000);
    int amex = (number / 10000000000000);
    int mc = (number / 100000000000000);
    if (visa16 == 4 || visa13 == 4)
    {
        printf("VISA\n");
    }
    else if (amex == 34 || amex == 37)
    {
        printf("AMEX\n");
    }
    else if (mc == 51 || mc == 52 || mc == 53 || mc == 54 || mc == 55)
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
