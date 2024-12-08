#!/usr/bin/env python3

import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")

import aoc

lines = aoc.get_input_lines(2024, 2)
# lines = aoc.get_example_lines()


def is_safe(levels):
    differences = [levels[i] - levels[i - 1] for i in range(1, len(levels))]
    increasing = None
    for difference in differences:
        if difference == 0:
            return False
        if increasing is None:
            increasing = difference > 0
        elif (increasing and difference < 0) or (not increasing and difference > 0):
            return False
        if abs(difference) > 3:
            return False
    return True


safe_lines_count = 0

for line in lines:
    if not line:
        continue
    levels = [int(x) for x in line.split()]
    if is_safe(levels):
        safe_lines_count += 1

print(safe_lines_count)
