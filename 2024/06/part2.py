#!/usr/bin/env python3

from collections import defaultdict
import copy
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
        if grid[y][x] == "^":
            start_x = x
            start_y = y
            break
    if start_x is not None:
        break

print("Guard found at:", (x, y))


def get_new_position(grid, old_x, old_y, v):
    candidate_new_x = old_x + v[0]
    candidate_new_y = old_y + v[1]
    if (
        candidate_new_x < 0
        or candidate_new_x >= w
        or candidate_new_y < 0
        or candidate_new_y >= h
    ):
        return (None, None), None
    if old_x == 4 and old_y == 6:
        print("candidate would be:")
    if grid[candidate_new_y][candidate_new_x] in ("#", "O"):
        v = (-v[1], v[0])
        return get_new_position(grid, old_x, old_y, v)
    return (candidate_new_x, candidate_new_y), v


def run_through_grid(grid):
    x = start_x
    y = start_y
    v = (0, -1)
    grid_with_path = copy.deepcopy(grid)
    points_on_path = set()
    looping = False
    while x >= 0 and x < w and y >= 0 and y < h:
        points_on_path.add(((x, y), v))
        grid_with_path[y][x] = "X"
        (x, y), v = get_new_position(grid, x, y, v)
        if x is None:
            break
        if ((x, y), v) in points_on_path:
            looping = True
            break
    return {
        "looping": looping,
        "points_on_path": points_on_path,
        "grid_with_path": grid_with_path,
    }


def print_grid(grid_to_print):
    for y in range(h):
        print("".join(grid_to_print[y]))


first_run_through_result = run_through_grid(grid)

possible_obstacle_positions = set(
    (x, y) for ((x, y), v) in first_run_through_result["points_on_path"]
)

number_that_loop = 0

for new_obstacle_x, new_obstacle_y in possible_obstacle_positions:
    grid_with_obstacle = copy.deepcopy(grid)
    grid_with_obstacle[new_obstacle_y][new_obstacle_x] = "O"
    result = run_through_grid(grid_with_obstacle)
    if result["looping"]:
        number_that_loop += 1

print(number_that_loop)
