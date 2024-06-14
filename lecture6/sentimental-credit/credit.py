def main():
    while True:
        try:
            number = int(input("Number: "))
            if number > 0:
                break
        except ValueError:
            continue

    if checksum(number):
        print(card_type(number))
    else:
        print("INVALID")


def checksum(number):
    sum = 0
    number_str = str(number)
    l = len(number_str)

    for i in range(l - 2, -1, -2):
        digit = int(number_str[i])
        double_digit = digit * 2
        if double_digit > 9:
            sum += (double_digit % 10) + (double_digit // 10)
        else:
            sum += double_digit

    for i in range(l - 1, -1, -2):
        sum += int(number_str[i])

    return sum % 10 == 0


def card_type(number):
    number_str = str(number)
    visa16 = number_str.startswith("4") and len(number_str) == 16
    visa13 = number_str.startswith("4") and len(number_str) == 13
    amex = number_str.startswith(("34", "37")) and len(number_str) == 15
    mc = number_str.startswith(tuple(str(i) for i in range(51, 56))) and len(number_str) == 16

    if visa16 or visa13:
        return "VISA"
    elif amex:
        return "AMEX"
    elif mc:
        return "MASTERCARD"
    else:
        return "INVALID"


main()
