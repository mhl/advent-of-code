#!/usr/bin/env python3

from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
import os
import re
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")

import aoc

lines = aoc.get_input_lines(2024, 10)
# lines = aoc.get_example_lines()

grid = []

for line in lines:
    if not len(line):
        continue
    grid.append([int(s) for s in line])

w = len(grid[0])
h = len(grid)

print(f"w {w} h {h}")

def in_bounds(a):
    return a[0] >= 0 and a[0] < w and a[1] >= 0 and a[1] < h

def get_neighbours(p):
    result = []
    for offset_y in (- 1, 0, 1):
        for offset_x in (- 1, 0, 1):
            if offset_x == offset_y:
                continue
            # Uncomment to include diagonals
            if not (offset_x == 0 or offset_y == 0):
                continue
            coord = (p[0] + offset_x, p[1] + offset_y)
            if in_bounds(coord):
                result.append(coord)
    return result

def find_paths_to_end_points(start_paths, value_at_start_points):
    if value_at_start_points == 9:
        return start_paths
    new_start_paths = set()
    for start_path in start_paths:
        for neighbour in get_neighbours(start_path[0]):
            neighbour_value = grid[neighbour[1]][neighbour[0]]
            if neighbour_value == value_at_start_points + 1:
                extended_path = (neighbour,) + start_path
                new_start_paths.add(extended_path)
    if not len(new_start_paths):
        return []
    return find_paths_to_end_points(new_start_paths, value_at_start_points + 1)

sum = 0

for y in range(h):
    for x in range(w):
        value = grid[y][x]
        if value == 0:
            end_paths = find_paths_to_end_points([((x, y),)], 0)
            sum += len(end_paths)

print(sum)
