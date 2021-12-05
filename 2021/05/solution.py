#!/usr/bin/env python3

from collections import Counter


def parse_input_line(line):
    coord_strings = line.split(" -> ")
    return tuple(
        tuple(int(c) for c in coord_string.split(",")) for coord_string in coord_strings
    )


with open("input.txt") as f:
    all_line_ends = tuple(parse_input_line(line) for line in f)


orthogonal_line_ends = tuple(
    l for l in all_line_ends if l[0][0] == l[1][0] or l[0][1] == l[1][1]
)


def inclusive_range(start, end):
    if start <= end:
        return range(start, end + 1)
    else:
        return range(start, end - 1, -1)


def get_line_points(line_ends):
    first, last = line_ends
    x_range = inclusive_range(first[0], last[0])
    y_range = inclusive_range(first[1], last[1])

    if first[1] == last[1]:
        return tuple((x, first[1]) for x in x_range)
    if first[0] == last[0]:
        return tuple((first[0], y) for y in y_range)

    x_diff = abs(first[0] - last[0])
    y_diff = abs(first[1] - last[1])
    if x_diff == y_diff:
        return tuple(zip(x_range, y_range))

    raise Exception("Line is neither orthogonal nor diagonal")


orthogonal_lines_points_counter = Counter()
for line_ends in orthogonal_line_ends:
    orthogonal_lines_points_counter.update(get_line_points(line_ends))
print(sum(1 for v in orthogonal_lines_points_counter.values() if v >= 2))

all_lines_points_counter = Counter()
for line_ends in all_line_ends:
    all_lines_points_counter.update(get_line_points(line_ends))
print(sum(1 for v in all_lines_points_counter.values() if v >= 2))
