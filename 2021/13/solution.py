#!/usr/bin/env python3

from collections import namedtuple
import re

Fold = namedtuple("Fold", ["axis", "index"])

points_set = set()
folds = []
with open("input.txt") as f:
    for line in f:
        m = re.search(r"^(\d+),(\d+)$", line)
        if m:
            points_set.add(tuple(int(s) for s in m.groups()))
            continue
        m = re.search(r"^fold along ([xy])=(\d+)$", line)
        if m:
            folds.append(
                Fold(axis=({"x": 0, "y": 1}[m.group(1)]), index=int(m.group(2)))
            )


def do_fold(points, fold):
    # Add the points that stay the same
    new_points = set(point for point in points if point[fold.axis] < fold.index)
    # Fold over the other points
    for point in points:
        if point[fold.axis] < fold.index:
            continue
        new_axis_value = 2 * fold.index - point[fold.axis]
        new_point_list = [None, None]
        new_point_list[fold.axis] = new_axis_value
        new_point_list[1 - fold.axis] = point[1 - fold.axis]
        new_points.add(tuple(new_point_list))
    return new_points

on_first_fold = True
for fold in folds:
    points_set = do_fold(points_set, fold)
    if on_first_fold:
        print(len(points_set))
        on_first_fold = False

width = 1 + max(x for x, _ in points_set)
height = 1 + max(y for _, y in points_set)

grid = [[" "] * width for y in range(height)]
for x, y in points_set:
    grid[y][x] = "#"

for row in grid:
    print("".join(row))
