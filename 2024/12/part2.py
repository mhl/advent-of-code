#!/usr/bin/env python3

from collections import defaultdict
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")

import aoc

lines = aoc.get_input_lines(2024, 12)
#lines = aoc.get_example_lines()

grid = []

for line in lines:
    if not len(line):
        continue
    grid.append(list(line))

w = len(grid[0])
h = len(grid)

print(f"w {w} h {h}")

def print_grid(grid_to_print):
    for y in range(h):
        print("".join(grid_to_print[y]))

def in_bounds(a):
    return a[0] >= 0 and a[0] < w and a[1] >= 0 and a[1] < h

def get_neighbours(p):
    result = []
    for offset_y in (-1, 0, 1):
        for offset_x in (-1, 0, 1):
            if offset_x == offset_y:
                continue
            # Uncomment to include diagonals
            if not (offset_x == 0 or offset_y == 0):
                continue
            coord = (p[0] + offset_x, p[1] + offset_y)
            result.append({
                "coord": coord,
                "offset": (offset_x, offset_y)
            })
    return result

def edge_sort_key(edge_data):
    offset = edge_data["offset_to_outside"]
    p = edge_data["point_inside"]
    if offset[0] != 0:
        return (offset, p[0], p[1])
    else:
        return (offset, p[1], p[0])

def find_region(p):
    plant_type = grid[p[1]][p[0]]
    next_points_to_consider = set([p])
    perimeter = 0
    area = 0
    already_counted_in_this_region = set()

    edge_data = []

    while len(next_points_to_consider):
        new_next_points_to_consider = set()
        for new_point in next_points_to_consider:
            new_value = grid[new_point[1]][new_point[0]]
            area += 1
            already_counted_in_this_region.add(new_point)
            points_already_dealt_with.add(new_point)
            grid[new_point[1]][new_point[0]] = "."
            for neighbour_data in get_neighbours(new_point):
                neighbour = neighbour_data["coord"]
                offset = neighbour_data["offset"]
                if neighbour in already_counted_in_this_region:
                    continue
                if not in_bounds(neighbour) or grid[neighbour[1]][neighbour[0]] != plant_type:
                    edge_data.append({
                        "point_inside": new_point,
                        "offset_to_outside": offset,
                    })
                    perimeter += 1
                    continue
                new_next_points_to_consider.add(neighbour)
        next_points_to_consider = new_next_points_to_consider

    sorted_edges = sorted(edge_data, key=edge_sort_key)

    number_of_sides = 0
    for i, edge_datum in enumerate(sorted_edges):
        i_pos = edge_datum["point_inside"]
        i_offset = edge_datum["offset_to_outside"]
        if i >= len(sorted_edges) - 1:
            number_of_sides += 1
            break
        j_pos = sorted_edges[i + 1]["point_inside"]
        j_offset = sorted_edges[i + 1]["offset_to_outside"]
        if i_offset != j_offset:
            number_of_sides += 1
            continue
        # Now we know the two we're comparing are the same offset
        # Is the offset vertical, and are they adjacent horizontally?
        if i_offset[0] == 0 and (i_pos[1] == j_pos[1]) and (abs(i_pos[0] - j_pos[0]) == 1):
            continue
        # Is the offset horizontal, and are they adjacent vertically?
        if i_offset[1] == 0 and (i_pos[0] == j_pos[0]) and (abs(i_pos[1] - j_pos[1]) == 1):
            continue
        number_of_sides += 1

    return area, perimeter, number_of_sides

points_already_dealt_with = set()
sum = 0

print_grid(grid)

for y in range(h):
    for x in range(w):
        if (x, y) in points_already_dealt_with:
            continue
        area, perimeter, number_of_sides = find_region((x, y))
        print("got area", area, "perimeter", perimeter, "number_of_sides", number_of_sides)
        print("grid now looks like:")
        print_grid(grid)
        sum += area * number_of_sides

print(sum)
