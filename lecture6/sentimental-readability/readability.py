from cs50 import get_string
import re
from math import ceil


def count_letters(text):
    # Return the number of letters in text
    letters = sum(1 for char in text if char.isalpha())
    return letters


def count_words(text):
    # Split the text into words using whitespace as the delimiter
    words = text.split()
    # Return the number of words
    return len(words)


def count_sentences(text):
    # Return the number of sentences in text
    sentences = len(re.findall(r'[.!?]', text))
    return sentences


def main():
    # Prompt the user for some text
    text = get_string("Text: ")

    # Count the number of letters, words, and sentences in the text
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # Calculate the average number of letters and sentences per 100 words
    L = letters * 100 / words
    S = sentences * 100 / words

    # Compute the Coleman-Liau index
    index = round(0.0588 * L - 0.296 * S - 15.8)

    # Print the grade level
    if index > 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


main()
