#!/usr/bin/env python3

from collections import defaultdict
from itertools import combinations
import os
import re
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('..')

import aoc

lines = aoc.get_input_lines(2024, 8)
#lines = aoc.get_example_lines()

grid = []

for line in lines:
    if not len(line):
        continue
    grid.append(list(line))

w = len(grid[0])
h = len(grid)

print(f"w {w} h {h}")

antenna_types = set()

# Find the distinct antenna types:
for y in range(h):
    for x in range(w):
        value = grid[y][x]
        if value != ".":
            antenna_types.add(value)

print(antenna_types)

def in_bounds(a):
    return a[0] >= 0 and a[0] < w and a[1] >= 0 and a[1] < h

def get_antinode_positions(a, b):
    x_diff = b[0] - a[0]
    y_diff = b[1] - a[1]

    antinode_positions = []

    print("##############", a, b)

    m = 0
    while True:
        p = (a[0] - m * x_diff, a[1] - m * y_diff)
        print("  ", p)
        if in_bounds(p):
            antinode_positions.append(p)
            m += 1
        else:
            break

    m = 0
    while True:
        p = (b[0] + m * x_diff, b[1] + m * y_diff)
        if in_bounds(p):
            antinode_positions.append(p)
            m += 1
        else:
            break
    return antinode_positions

def get_pairs_of_type(antenna_type):
    antenna_coords = []
    for y in range(h):
        for x in range(w):
            if grid[y][x] == antenna_type:
                antenna_coords.append((x, y))
    return combinations(antenna_coords, 2)

result_positions = set()

for antenna_type in antenna_types:
    print("antenna_type", antenna_type)
    for pair in get_pairs_of_type(antenna_type):
        a, b = pair
        for antinode_position in get_antinode_positions(a, b):
            result_positions.add(antinode_position)

print(len(result_positions))
