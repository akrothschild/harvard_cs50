cmake_minimum_required(VERSION 3.28)
project(harvard_cs50 C)

set(CMAKE_C_STANDARD 11)

add_library(harvard_cs50 STATIC library.c
        mario.c
        main.c)
