#!/usr/bin/env python3

import math

with open("input.txt") as f:
    number_grid = [[int(digit) for digit in line.rstrip()] for line in f]

height = len(number_grid)
width = len(number_grid[0])

unallocated_points = set(
    (x, y) for y in range(height) for x in range(width) if number_grid[y][x] < 9
)


def find_adjacent_points(point):
    x, y = point
    adjacent_points = []
    if x > 0:
        adjacent_points.append((x - 1, y))
    if x < width - 1:
        adjacent_points.append((x + 1, y))
    if y > 0:
        adjacent_points.append((x, y - 1))
    if y < height - 1:
        adjacent_points.append((x, y + 1))
    return adjacent_points


def find_basin(start_point):
    basin_points = []
    next_points_to_explore = set([start_point])
    while next_points_to_explore:
        n = next_points_to_explore.pop()
        basin_points.append(n)
        unallocated_points.remove(n)
        next_points_to_explore.update(
            point for point in find_adjacent_points(n) if point in unallocated_points
        )
    return basin_points


all_basins = []
try:
    while next_point := next(iter(unallocated_points)):
        all_basins.append(find_basin(next_point))
except StopIteration as e:
    pass

all_basins.sort(reverse=True, key=lambda b: len(b))

print(math.prod(len(b) for b in all_basins[:3]))
