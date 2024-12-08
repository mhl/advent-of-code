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

start_letter = "A"
word_to_find = "MAS"


def safe_get(y, x):
    if x >= w or y >= h or x < 0 or y < 0:
        return ""
    return grid[y][x]


def get_ne(start_x, start_y):
    return [
        "".join([safe_get(start_y + i, start_x + i) for i in range(-1, 2)]),
        "".join([safe_get(start_y - i, start_x - i) for i in range(-1, 2)]),
    ]


def get_nw(start_x, start_y):
    return [
        "".join([safe_get(start_y + i, start_x - i) for i in range(-1, 2)]),
        "".join([safe_get(start_y - i, start_x + i) for i in range(-1, 2)]),
    ]


sum = 0

for start_y in range(h):
    for start_x in range(w):
        if grid[start_y][start_x] == start_letter:
            nw_words = get_nw(start_x, start_y)
            ne_words = get_ne(start_x, start_y)
            if word_to_find in nw_words and word_to_find in ne_words:
                sum += 1

print(sum)
