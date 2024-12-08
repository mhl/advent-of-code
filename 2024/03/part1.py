#!/usr/bin/env python3

import os
import re
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")

import aoc

lines = aoc.get_input_lines(2024, 3)

sum = 0

for line in lines:
    if not len(line):
        continue
    for match in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line):
        sum += int(match[0]) * int(match[1])

print(sum)
