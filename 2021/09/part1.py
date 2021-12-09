#!/usr/bin/env python3

with open("input.txt") as f:
    number_grid = [[int(digit) for digit in line.rstrip()] for line in f]


def get_adjacent_depths(number_grid):
    width = len(number_grid[0])
    height = len(number_grid)
    for y in range(height):
        row = number_grid[y]
        for x in range(width):
            central_depth = row[x]
            adjacent_depths = []
            if x > 0:
                adjacent_depths.append(number_grid[y][x - 1])
            if x < width - 1:
                adjacent_depths.append(number_grid[y][x + 1])
            if y > 0:
                adjacent_depths.append(number_grid[y - 1][x])
            if y < height - 1:
                adjacent_depths.append(number_grid[y + 1][x])
            yield (central_depth, adjacent_depths)


sum_of_low_point_risk_levels = sum(
    depth + 1
    for depth, adjacent_depths in get_adjacent_depths(number_grid)
    if all(depth < d for d in adjacent_depths)
)

print(sum_of_low_point_risk_levels)
