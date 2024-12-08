#!/usr/bin/env python3

import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")

import aoc

lines = aoc.get_input_lines(2024, 1)

left_column = []
right_column = []

for line in lines:
    fields = line.split()
    if len(fields) != 2:
        continue
    left, right = fields
    left_column.append(left)
    right_column.append(right)

sorted_left = sorted(left_column)
sorted_right = sorted(right_column)

zipped = zip(sorted_left, sorted_right)

sum_of_differences = 0

for left, right in zipped:
    difference = abs(int(left) - int(right))
    sum_of_differences += difference

print(sum_of_differences)
