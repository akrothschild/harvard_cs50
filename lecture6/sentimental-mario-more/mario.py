def main():
    height = 0
    while True:
        height = input("Height: ")
        if height.isdigit():
            h = int(height)
            if 0 < h < 9:
                break

    print_blocks(h)


def print_blocks(h):
    for i in range(1, h + 1):
        for n in range(h - i):
            print(" ", end="")

        for j in range(i):
            print("#", end="")

        print("  ", end="")

        for j in range(i):
            print("#", end="")

        print()


main()
