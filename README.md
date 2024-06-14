# Harvard CS50 2024
Code to train cs50 course. Solutions to problem sets.
Currently, I am using online VS Code from Harvard. If you code offline, download cs50 library.
All "green" but I would recommend to think yourself. 
Course itself and Problem sets are great to train your skills.

# Usage:
Done to use on Harvard VM. To use locally include cs50 library 
To run:
`
clang -fsanitize=integer -fsanitize=undefined -ggdb3 -O0 -std=c11 -Wall -Werror -Wextra -Wno-sign-compare -Wshadow    temp.c  -lcrypt -lcs50 -lm -o temp
`