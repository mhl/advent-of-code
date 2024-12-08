#!/usr/bin/env python3

from collections import defaultdict
import os
import re
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")

import aoc

lines = aoc.get_input_lines(2024, 6)
# lines = aoc.get_example_lines()

grid = []

for line in lines:
    if not len(line):
        continue
    grid.append(list(line))

w = len(grid[0])
h = len(grid)

print(f"w {w} h {h}")

start_x = None
start_y = None

# Find the start position:
for y in range(h):
    for x in range(w):
        print("considering grid:", grid[y][x])
        if grid[y][x] == "^":
            start_x = x
            start_y = y
            break
    if start_x is not None:
        break

print("Guard found at:", (x, y))

positions_covered = set()

x = start_x
y = start_y

v = (0, -1)


def get_new_position(old_x, old_y):
    global v
    candidate_new_x = old_x + v[0]
    candidate_new_y = old_y + v[1]
    if (
        candidate_new_x < 0
        or candidate_new_x >= w
        or candidate_new_y < 0
        or candidate_new_y >= h
    ):
        return (None, None)
    if grid[candidate_new_y][candidate_new_x] == "#":
        # v = (v[1], -v[0])
        v = (-v[1], v[0])
        return get_new_position(old_x, old_y)
    return (candidate_new_x, candidate_new_y)


while x >= 0 and x < w and y >= 0 and y < h:
    positions_covered.add((x, y))
    x, y = get_new_position(x, y)
    print("new x:", x, "new y:", y)
    if x is None:
        break
    grid[y][x] = "X"

for y in range(h):
    print("".join(grid[y]))

print(len(positions_covered))
