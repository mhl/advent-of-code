#!/usr/bin/env python3

import os
import re
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")

import aoc

lines = aoc.get_input_lines(2024, 4)
# lines = aoc.get_example_lines()

grid = []

for line in lines:
    if not len(line):
        continue
    letters = list(line)
    grid.append(letters)

w = len(grid[0])
h = len(grid)

word_to_find = "XMAS"


def safe_get(y, x):
    if x >= w or y >= h or x < 0 or y < 0:
        return ""
    return grid[y][x]


def get_all_words(start_x, start_y):
    return [
        "".join(
            [safe_get(start_y, start_x + i) for i in range(len(word_to_find))]
        ),  # h_right
        "".join(
            [safe_get(start_y, start_x - i) for i in range(len(word_to_find))]
        ),  # h_left
        "".join(
            [safe_get(start_y + i, start_x) for i in range(len(word_to_find))]
        ),  # v_down
        "".join(
            [safe_get(start_y - i, start_x) for i in range(len(word_to_find))]
        ),  # v_up
        "".join(
            [safe_get(start_y + i, start_x + i) for i in range(len(word_to_find))]
        ),  # d_down_right
        "".join(
            [safe_get(start_y + i, start_x - i) for i in range(len(word_to_find))]
        ),  # d_down_left
        "".join(
            [safe_get(start_y - i, start_x + i) for i in range(len(word_to_find))]
        ),  # d_up_right
        "".join(
            [safe_get(start_y - i, start_x - i) for i in range(len(word_to_find))]
        ),  # d_up_left
    ]


sum = 0

for start_y in range(h):
    for start_x in range(w):
        if grid[start_y][start_x] == word_to_find[0]:
            words = get_all_words(start_x, start_y)
            if start_y == 9 and start_x == 1:
                print(words)
            print(
                f"   at row {start_y}, column {start_x}, found the word in these directions: {words}"
            )
            correct_words = [i for i, word in enumerate(words) if word == word_to_find]
            print(
                f"   at row {start_y}, column {start_x}, found the word in these directions: {correct_words}"
            )
            sum += len(correct_words)

print(sum)
