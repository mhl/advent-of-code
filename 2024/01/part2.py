#!/usr/bin/env python3

from collections import Counter
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
    left_column.append(int(left))
    right_column.append(int(right))

counter = Counter(right_column)

total = 0

for left in left_column:
    total += left * counter[left]

print(total)
